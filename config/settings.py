"""Configuration settings for AI Adoption Dashboard.

This module provides environment variable management and default settings
for the application, supporting both Windows (WSL) and Linux systems.
"""

import os
from pathlib import Path
from typing import Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip loading
    pass


class Settings:
    """Application settings with environment variable support."""
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Resources path - supports environment variable override
    RESOURCES_PATH = os.getenv(
        'AI_ADOPTION_RESOURCES_PATH',
        str(BASE_DIR / 'AI adoption resources')
    )
    
    # Data directories
    DATA_DIR = BASE_DIR / 'data'
    CACHE_DIR = BASE_DIR / '.cache'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Performance settings
    CACHE_MEMORY_SIZE = int(os.getenv('CACHE_MEMORY_SIZE', '200'))
    CACHE_MEMORY_TTL = int(os.getenv('CACHE_MEMORY_TTL', '600'))
    CACHE_DISK_SIZE = int(os.getenv('CACHE_DISK_SIZE', str(2 * 1024**3)))
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv(
        'LOG_FORMAT',
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # API settings (if needed in future)
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    
    @classmethod
    def get_resources_path(cls) -> Path:
        """Get the resources path as a Path object.
        
        Returns:
            Path object for the resources directory
        """
        return Path(cls.RESOURCES_PATH)
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        directories = [
            cls.get_resources_path(),
            cls.DATA_DIR,
            cls.CACHE_DIR,
            cls.LOGS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_resources_path(cls) -> bool:
        """Validate that the resources path exists and is accessible.
        
        Returns:
            True if resources path is valid, False otherwise
        """
        resources_path = cls.get_resources_path()
        return resources_path.exists() and resources_path.is_dir()
    
    @classmethod
    def get_resource_file(cls, relative_path: str) -> Optional[Path]:
        """Get a resource file path.
        
        Args:
            relative_path: Path relative to resources directory
            
        Returns:
            Full path to the resource file if it exists, None otherwise
        """
        full_path = cls.get_resources_path() / relative_path
        return full_path if full_path.exists() else None
    
    @classmethod
    def get_settings_dict(cls) -> dict:
        """Get all settings as a dictionary.
        
        Returns:
            Dictionary of all settings
        """
        return {
            'BASE_DIR': str(cls.BASE_DIR),
            'RESOURCES_PATH': cls.RESOURCES_PATH,
            'DATA_DIR': str(cls.DATA_DIR),
            'CACHE_DIR': str(cls.CACHE_DIR),
            'LOGS_DIR': str(cls.LOGS_DIR),
            'CACHE_MEMORY_SIZE': cls.CACHE_MEMORY_SIZE,
            'CACHE_MEMORY_TTL': cls.CACHE_MEMORY_TTL,
            'CACHE_DISK_SIZE': cls.CACHE_DISK_SIZE,
            'MAX_WORKERS': cls.MAX_WORKERS,
            'LOG_LEVEL': cls.LOG_LEVEL,
            'DEBUG': cls.DEBUG,
            'API_TIMEOUT': cls.API_TIMEOUT
        }


# Create a singleton instance
settings = Settings()