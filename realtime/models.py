"""
Data models for real-time integration system
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)

class DataSourceType(str, Enum):
    """Types of data sources supported"""
    REST_API = "rest_api"
    WEBSOCKET = "websocket"
    DATABASE = "database"
    FILE_FEED = "file_feed"
    STREAM = "stream"

class APIMethod(str, Enum):
    """HTTP methods supported"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class DataStatus(str, Enum):
    """Data status states"""
    PENDING = "pending"
    LOADING = "loading"
    SUCCESS = "success"
    ERROR = "error"
    STALE = "stale"
    CACHED = "cached"

class AuthenticationType(str, Enum):
    """Authentication types"""
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    BASIC_AUTH = "basic_auth"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"

class DataSourceCredentials(BaseModel):
    """Credentials for data source authentication"""
    auth_type: AuthenticationType = AuthenticationType.NONE
    api_key: Optional[str] = None
    bearer_token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    oauth_config: Optional[Dict[str, Any]] = None
    custom_headers: Optional[Dict[str, str]] = None
    
    class Config:
        extra = "forbid"

class RateLimitConfig(BaseModel):
    """Rate limiting configuration"""
    requests_per_second: float = Field(default=1.0, gt=0)
    requests_per_minute: int = Field(default=60, gt=0)
    requests_per_hour: int = Field(default=3600, gt=0)
    burst_limit: int = Field(default=10, gt=0)
    
    class Config:
        extra = "forbid"

class RetryConfig(BaseModel):
    """Retry configuration for failed requests"""
    max_attempts: int = Field(default=3, ge=1, le=10)
    initial_delay: float = Field(default=1.0, gt=0)
    max_delay: float = Field(default=60.0, gt=0)
    exponential_base: float = Field(default=2.0, gt=1)
    jitter: bool = True
    
    class Config:
        extra = "forbid"

class DataValidationRule(BaseModel):
    """Data validation rule"""
    field_name: str
    rule_type: str  # required, type, range, regex, custom
    rule_config: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    
    class Config:
        extra = "forbid"

class DataSourceConfig(BaseModel):
    """Configuration for a data source"""
    source_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    source_type: DataSourceType
    enabled: bool = True
    
    # Connection settings
    base_url: Optional[str] = None
    endpoint: Optional[str] = None
    method: APIMethod = APIMethod.GET
    
    # Authentication
    credentials: DataSourceCredentials = Field(default_factory=DataSourceCredentials)
    
    # Rate limiting and retry
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    
    # Data handling
    data_format: str = "json"  # json, xml, csv, etc.
    data_mapping: Optional[Dict[str, str]] = None
    validation_rules: List[DataValidationRule] = Field(default_factory=list)
    
    # Update frequency
    update_interval: timedelta = Field(default=timedelta(minutes=5))
    real_time: bool = False
    
    # Caching
    cache_duration: timedelta = Field(default=timedelta(hours=1))
    cache_key_template: Optional[str] = None
    
    # Monitoring
    timeout: float = Field(default=30.0, gt=0)
    health_check_interval: timedelta = Field(default=timedelta(minutes=1))
    
    class Config:
        extra = "forbid"
        use_enum_values = True

class DataRecord(BaseModel):
    """A single data record with metadata"""
    source_id: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        extra = "forbid"

class DataStreamState(BaseModel):
    """State of a data stream"""
    source_id: str
    status: DataStatus = DataStatus.PENDING
    last_update: Optional[datetime] = None
    last_success: Optional[datetime] = None
    last_error: Optional[datetime] = None
    error_message: Optional[str] = None
    error_count: int = 0
    total_records: int = 0
    
    # Performance metrics
    avg_response_time: float = 0.0
    success_rate: float = 100.0
    
    class Config:
        extra = "forbid"

class APIResponse(BaseModel):
    """Response from an API call"""
    source_id: str
    status_code: int
    data: Any = None
    headers: Dict[str, str] = Field(default_factory=dict)
    response_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300
    
    class Config:
        extra = "forbid"

class DataChangeEvent(BaseModel):
    """Event representing a data change"""
    source_id: str
    change_type: str  # insert, update, delete
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    changed_fields: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        extra = "forbid"

class HealthStatus(BaseModel):
    """Health status of a data source"""
    source_id: str
    is_healthy: bool = True
    response_time: Optional[float] = None
    last_check: datetime = Field(default_factory=datetime.utcnow)
    consecutive_failures: int = 0
    uptime_percentage: float = 100.0
    issues: List[str] = Field(default_factory=list)
    
    class Config:
        extra = "forbid"

class NotificationEvent(BaseModel):
    """Notification event for real-time updates"""
    event_type: str
    source_id: str
    message: str
    severity: str = "info"  # info, warning, error, critical
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        extra = "forbid"

class ConnectionPoolConfig(BaseModel):
    """Configuration for connection pooling"""
    max_connections: int = Field(default=100, gt=0)
    max_connections_per_host: int = Field(default=30, gt=0)
    connection_timeout: float = Field(default=30.0, gt=0)
    read_timeout: float = Field(default=60.0, gt=0)
    keepalive_timeout: float = Field(default=30.0, gt=0)
    enable_ssl_verification: bool = True
    
    class Config:
        extra = "forbid"

# Utility functions
def create_default_data_source(source_id: str, name: str, base_url: str) -> DataSourceConfig:
    """Create a default data source configuration"""
    return DataSourceConfig(
        source_id=source_id,
        name=name,
        source_type=DataSourceType.REST_API,
        base_url=base_url
    )

def validate_data_against_rules(data: Dict[str, Any], rules: List[DataValidationRule]) -> List[str]:
    """Validate data against validation rules"""
    errors = []
    for rule in rules:
        try:
            field_value = data.get(rule.field_name)
            
            if rule.rule_type == "required" and field_value is None:
                errors.append(rule.error_message or f"Field {rule.field_name} is required")
            elif rule.rule_type == "type" and field_value is not None:
                expected_type = rule.rule_config.get("type")
                if expected_type and not isinstance(field_value, eval(expected_type)):
                    errors.append(rule.error_message or f"Field {rule.field_name} must be of type {expected_type}")
            # Add more validation rules as needed
            
        except Exception as e:
            logger.error(f"Error validating rule {rule.field_name}: {e}")
            errors.append(f"Validation error for {rule.field_name}")
    
    return errors