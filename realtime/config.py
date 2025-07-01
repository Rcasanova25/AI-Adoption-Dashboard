"""
Configuration management system for data sources and API connections
"""

import asyncio
import logging
import json
import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pathlib import Path
import yaml
from dataclasses import asdict

from .models import (
    DataSourceConfig, DataSourceCredentials, RateLimitConfig, 
    RetryConfig, AuthenticationType, DataSourceType,
    DataValidationRule, ConnectionPoolConfig
)

logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Configuration-related errors"""
    pass

class ConfigManager:
    """Manages data source configurations"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or "config/datasources")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.configs: Dict[str, DataSourceConfig] = {}
        self._file_watchers: Dict[str, float] = {}  # file -> last_modified
        self._lock = asyncio.Lock()
        
        # Environment variable prefixes for sensitive data
        self.env_prefixes = {
            'api_key': 'DATASOURCE_{source_id}_API_KEY',
            'bearer_token': 'DATASOURCE_{source_id}_BEARER_TOKEN',
            'username': 'DATASOURCE_{source_id}_USERNAME',
            'password': 'DATASOURCE_{source_id}_PASSWORD'
        }
    
    async def load_config(self, source_id: str) -> Optional[DataSourceConfig]:
        """Load configuration for a specific source"""
        config_file = self.config_dir / f"{source_id}.yaml"
        
        if not config_file.exists():
            logger.warning(f"Configuration file not found: {config_file}")
            return None
        
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Apply environment variable substitutions
            config_data = self._apply_env_substitutions(config_data, source_id)
            
            # Create and validate config
            config = DataSourceConfig(**config_data)
            
            async with self._lock:
                self.configs[source_id] = config
                self._file_watchers[str(config_file)] = config_file.stat().st_mtime
            
            logger.info(f"Loaded configuration for {source_id}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config for {source_id}: {e}")
            raise ConfigurationError(f"Failed to load config for {source_id}: {e}")
    
    async def save_config(self, config: DataSourceConfig, encrypt_secrets: bool = True):
        """Save configuration to file"""
        config_file = self.config_dir / f"{config.source_id}.yaml"
        
        try:
            # Convert to dict and handle sensitive data
            config_dict = asdict(config)
            
            if encrypt_secrets:
                # Replace sensitive values with environment variable references
                config_dict = self._replace_with_env_vars(config_dict, config.source_id)
            
            with open(config_file, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, sort_keys=False)
            
            async with self._lock:
                self.configs[config.source_id] = config
                self._file_watchers[str(config_file)] = config_file.stat().st_mtime
            
            logger.info(f"Saved configuration for {config.source_id}")
            
        except Exception as e:
            logger.error(f"Error saving config for {config.source_id}: {e}")
            raise ConfigurationError(f"Failed to save config for {config.source_id}: {e}")
    
    async def load_all_configs(self) -> Dict[str, DataSourceConfig]:
        """Load all configuration files"""
        configs = {}
        
        for config_file in self.config_dir.glob("*.yaml"):
            source_id = config_file.stem
            try:
                config = await self.load_config(source_id)
                if config:
                    configs[source_id] = config
            except Exception as e:
                logger.error(f"Failed to load config {source_id}: {e}")
        
        return configs
    
    async def delete_config(self, source_id: str) -> bool:
        """Delete a configuration"""
        config_file = self.config_dir / f"{source_id}.yaml"
        
        try:
            if config_file.exists():
                config_file.unlink()
            
            async with self._lock:
                if source_id in self.configs:
                    del self.configs[source_id]
                
                file_path = str(config_file)
                if file_path in self._file_watchers:
                    del self._file_watchers[file_path]
            
            logger.info(f"Deleted configuration for {source_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting config for {source_id}: {e}")
            return False
    
    async def get_config(self, source_id: str) -> Optional[DataSourceConfig]:
        """Get configuration from memory or load from file"""
        async with self._lock:
            if source_id in self.configs:
                return self.configs[source_id]
        
        return await self.load_config(source_id)
    
    async def list_configs(self) -> List[str]:
        """List all available configuration IDs"""
        config_files = list(self.config_dir.glob("*.yaml"))
        return [f.stem for f in config_files]
    
    async def watch_config_changes(self, callback: callable):
        """Watch for configuration file changes"""
        while True:
            try:
                await self._check_file_changes(callback)
                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Error watching config changes: {e}")
                await asyncio.sleep(30)  # Wait longer on error
    
    async def _check_file_changes(self, callback: callable):
        """Check for file changes and reload if needed"""
        for config_file in self.config_dir.glob("*.yaml"):
            file_path = str(config_file)
            current_mtime = config_file.stat().st_mtime
            last_mtime = self._file_watchers.get(file_path, 0)
            
            if current_mtime > last_mtime:
                source_id = config_file.stem
                logger.info(f"Configuration file changed: {source_id}")
                
                try:
                    config = await self.load_config(source_id)
                    if config and callback:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(source_id, config)
                        else:
                            callback(source_id, config)
                except Exception as e:
                    logger.error(f"Error reloading config {source_id}: {e}")
    
    def _apply_env_substitutions(self, config_data: Dict[str, Any], source_id: str) -> Dict[str, Any]:
        """Apply environment variable substitutions"""
        if 'credentials' in config_data:
            creds = config_data['credentials']
            
            # Check for API key
            api_key_env = self.env_prefixes['api_key'].format(source_id=source_id.upper())
            if api_key_env in os.environ:
                creds['api_key'] = os.environ[api_key_env]
            
            # Check for bearer token
            token_env = self.env_prefixes['bearer_token'].format(source_id=source_id.upper())
            if token_env in os.environ:
                creds['bearer_token'] = os.environ[token_env]
            
            # Check for username/password
            username_env = self.env_prefixes['username'].format(source_id=source_id.upper())
            password_env = self.env_prefixes['password'].format(source_id=source_id.upper())
            
            if username_env in os.environ:
                creds['username'] = os.environ[username_env]
            if password_env in os.environ:
                creds['password'] = os.environ[password_env]
        
        return config_data
    
    def _replace_with_env_vars(self, config_dict: Dict[str, Any], source_id: str) -> Dict[str, Any]:
        """Replace sensitive values with environment variable references"""
        if 'credentials' in config_dict:
            creds = config_dict['credentials']
            
            # Replace sensitive values with placeholders
            if creds.get('api_key'):
                creds['api_key'] = f"${{{self.env_prefixes['api_key'].format(source_id=source_id.upper())}}}"
            
            if creds.get('bearer_token'):
                creds['bearer_token'] = f"${{{self.env_prefixes['bearer_token'].format(source_id=source_id.upper())}}}"
            
            if creds.get('username'):
                creds['username'] = f"${{{self.env_prefixes['username'].format(source_id=source_id.upper())}}}"
            
            if creds.get('password'):
                creds['password'] = f"${{{self.env_prefixes['password'].format(source_id=source_id.upper())}}}"
        
        return config_dict
    
    async def validate_config(self, config: DataSourceConfig) -> List[str]:
        """Validate a configuration and return any errors"""
        errors = []
        
        try:
            # Basic validation is handled by Pydantic
            # Additional custom validation
            
            if config.source_type == DataSourceType.REST_API and not config.base_url:
                errors.append("base_url is required for REST API sources")
            
            if config.credentials.auth_type == AuthenticationType.API_KEY and not config.credentials.api_key:
                errors.append("api_key is required when using API key authentication")
            
            if config.credentials.auth_type == AuthenticationType.BEARER_TOKEN and not config.credentials.bearer_token:
                errors.append("bearer_token is required when using bearer token authentication")
            
            if (config.credentials.auth_type == AuthenticationType.BASIC_AUTH and 
                (not config.credentials.username or not config.credentials.password)):
                errors.append("username and password are required for basic authentication")
            
            # Validate rate limits are reasonable
            if config.rate_limit.requests_per_second > 100:
                errors.append("requests_per_second seems too high (>100)")
            
            if config.timeout > 300:
                errors.append("timeout is very high (>300 seconds)")
            
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        return errors
    
    async def create_template_config(self, source_id: str, source_type: DataSourceType) -> DataSourceConfig:
        """Create a template configuration for a source type"""
        template_configs = {
            DataSourceType.REST_API: {
                'source_id': source_id,
                'name': f'{source_id.title()} API',
                'description': f'REST API integration for {source_id}',
                'source_type': DataSourceType.REST_API,
                'base_url': 'https://api.example.com',
                'endpoint': '/v1/data',
                'method': 'GET',
                'credentials': {
                    'auth_type': AuthenticationType.API_KEY,
                    'api_key': 'your-api-key-here'
                },
                'rate_limit': {
                    'requests_per_second': 1.0,
                    'requests_per_minute': 60,
                    'burst_limit': 5
                },
                'retry_config': {
                    'max_attempts': 3,
                    'initial_delay': 1.0,
                    'max_delay': 30.0
                },
                'update_interval': '5m',
                'timeout': 30.0
            }
        }
        
        config_data = template_configs.get(source_type, template_configs[DataSourceType.REST_API])
        config_data['source_id'] = source_id
        config_data['source_type'] = source_type
        
        # Convert string intervals to timedelta
        if isinstance(config_data.get('update_interval'), str):
            config_data['update_interval'] = self._parse_time_string(config_data['update_interval'])
        
        return DataSourceConfig(**config_data)
    
    def _parse_time_string(self, time_str: str) -> timedelta:
        """Parse time string like '5m', '1h', '30s' into timedelta"""
        time_str = time_str.strip().lower()
        
        if time_str.endswith('s'):
            return timedelta(seconds=int(time_str[:-1]))
        elif time_str.endswith('m'):
            return timedelta(minutes=int(time_str[:-1]))
        elif time_str.endswith('h'):
            return timedelta(hours=int(time_str[:-1]))
        elif time_str.endswith('d'):
            return timedelta(days=int(time_str[:-1]))
        else:
            # Default to minutes if no unit specified
            return timedelta(minutes=int(time_str))

class ConfigUI:
    """User interface for configuration management"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
    
    def render_config_form(self, config: Optional[DataSourceConfig] = None) -> Dict[str, Any]:
        """Render configuration form data for UI"""
        if config:
            form_data = {
                'source_id': config.source_id,
                'name': config.name,
                'description': config.description or '',
                'source_type': config.source_type.value,
                'enabled': config.enabled,
                'base_url': config.base_url or '',
                'endpoint': config.endpoint or '',
                'method': config.method.value,
                'auth_type': config.credentials.auth_type.value,
                'api_key': '***' if config.credentials.api_key else '',
                'bearer_token': '***' if config.credentials.bearer_token else '',
                'username': config.credentials.username or '',
                'password': '***' if config.credentials.password else '',
                'requests_per_second': config.rate_limit.requests_per_second,
                'requests_per_minute': config.rate_limit.requests_per_minute,
                'max_attempts': config.retry_config.max_attempts,
                'initial_delay': config.retry_config.initial_delay,
                'update_interval': int(config.update_interval.total_seconds() / 60),  # Convert to minutes
                'timeout': config.timeout,
                'real_time': config.real_time
            }
        else:
            # Default values for new config
            form_data = {
                'source_id': '',
                'name': '',
                'description': '',
                'source_type': DataSourceType.REST_API.value,
                'enabled': True,
                'base_url': '',
                'endpoint': '',
                'method': 'GET',
                'auth_type': AuthenticationType.NONE.value,
                'api_key': '',
                'bearer_token': '',
                'username': '',
                'password': '',
                'requests_per_second': 1.0,
                'requests_per_minute': 60,
                'max_attempts': 3,
                'initial_delay': 1.0,
                'update_interval': 5,  # minutes
                'timeout': 30.0,
                'real_time': False
            }
        
        return form_data
    
    async def process_form_data(self, form_data: Dict[str, Any]) -> DataSourceConfig:
        """Process form data and create/update configuration"""
        # Handle credentials
        credentials_data = {
            'auth_type': form_data.get('auth_type', AuthenticationType.NONE.value)
        }
        
        # Only include credentials if they're not masked
        if form_data.get('api_key') and form_data['api_key'] != '***':
            credentials_data['api_key'] = form_data['api_key']
        
        if form_data.get('bearer_token') and form_data['bearer_token'] != '***':
            credentials_data['bearer_token'] = form_data['bearer_token']
        
        if form_data.get('username'):
            credentials_data['username'] = form_data['username']
        
        if form_data.get('password') and form_data['password'] != '***':
            credentials_data['password'] = form_data['password']
        
        # Create configuration
        config_data = {
            'source_id': form_data['source_id'],
            'name': form_data['name'],
            'description': form_data.get('description'),
            'source_type': form_data['source_type'],
            'enabled': form_data.get('enabled', True),
            'base_url': form_data.get('base_url'),
            'endpoint': form_data.get('endpoint'),
            'method': form_data.get('method', 'GET'),
            'credentials': credentials_data,
            'rate_limit': {
                'requests_per_second': float(form_data.get('requests_per_second', 1.0)),
                'requests_per_minute': int(form_data.get('requests_per_minute', 60))
            },
            'retry_config': {
                'max_attempts': int(form_data.get('max_attempts', 3)),
                'initial_delay': float(form_data.get('initial_delay', 1.0))
            },
            'update_interval': timedelta(minutes=int(form_data.get('update_interval', 5))),
            'timeout': float(form_data.get('timeout', 30.0)),
            'real_time': form_data.get('real_time', False)
        }
        
        return DataSourceConfig(**config_data)

# Global config manager instance
_global_config_manager: Optional[ConfigManager] = None

def get_global_config_manager(config_dir: Optional[str] = None) -> ConfigManager:
    """Get the global configuration manager instance"""
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = ConfigManager(config_dir)
    return _global_config_manager