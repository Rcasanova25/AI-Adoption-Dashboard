"""
Environment-specific Configuration Management
Implements Pydantic BaseSettings for robust configuration handling
Backward compatible with existing configuration structure
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional
from pathlib import Path
from pydantic import BaseSettings, Field, validator
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Environment(str, Enum):
    """Application environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Replace the hardcoded feature flags from your app.py lines 12-19
@dataclass
class FeatureFlags:
    EXECUTIVE_MODE: bool = True
    VISUAL_REDESIGN: bool = True
    STRATEGIC_CALLOUTS: bool = True
    COMPETITIVE_HOMEPAGE: bool = False


# Replace the scattered view lists from your app.py lines 21-45
class ViewType:
    # Executive Views
    STRATEGIC_BRIEF = "🚀 Strategic Brief"
    COMPETITIVE_POSITION = "⚖️ Competitive Position"
    INVESTMENT_CASE = "💰 Investment Case"
    MARKET_INTELLIGENCE = "📊 Market Intelligence"
    ACTION_PLANNING = "🎯 Action Planning"
    
    # Detailed Views
    COMPETITIVE_POSITION_ASSESSOR = "🎯 Competitive Position Assessor"
    INVESTMENT_ENGINE = "💰 Investment Decision Engine"
    REGULATORY_RADAR = "⚖️ Regulatory Risk Radar"
    HISTORICAL_TRENDS = "Historical Trends"
    INDUSTRY_ANALYSIS = "Industry Analysis"
    FINANCIAL_IMPACT = "Financial Impact"
    ROI_ANALYSIS = "ROI Analysis"
    ADOPTION_RATES = "Adoption Rates"
    FIRM_SIZE_ANALYSIS = "🏭 Firm Size Analysis"
    GEOGRAPHIC_DISTRIBUTION = "Geographic Distribution"
    TECHNOLOGY_STACK = "Technology Stack"
    AI_COST_TRENDS = "AI Cost Trends"
    PRODUCTIVITY_RESEARCH = "Productivity Research"
    LABOR_IMPACT = "Labor Impact"
    ENVIRONMENTAL_IMPACT = "Environmental Impact"
    AI_GOVERNANCE = "⚖️ AI Governance"
    SKILL_GAP_ANALYSIS = "🎓 Skill Gap Analysis"
    BARRIERS_SUPPORT = "🚧 Barriers & Support"
    TOKEN_ECONOMICS = "Token Economics"
    INVESTMENT_TRENDS = "Investment Trends"
    REGIONAL_GROWTH = "Regional Growth"
    AI_TECHNOLOGY_MATURITY = "🤖 AI Technology Maturity"
    OECD_FINDINGS = "🌍 OECD 2025 Findings"
    BIBLIOGRAPHY_SOURCES = "Bibliography & Sources"


# Replace hardcoded thresholds scattered throughout
@dataclass
class MetricThresholds:
    MIN_ROI: float = 2.5
    STRONG_ROI: float = 3.0
    HIGH_ADOPTION_RATE: float = 70.0
    COMPETITIVE_THRESHOLD: float = 25.0
    CRITICAL_URGENCY: int = 8
    HIGH_URGENCY: int = 6


# Replace hardcoded UI values
@dataclass
class UIConfig:
    PAGE_TITLE: str = "AI Adoption Dashboard | 2018-2025 Analysis"
    PAGE_ICON: str = "🤖"
    LAYOUT: Literal["wide", "centered"] = "wide"
    CHART_HEIGHT: int = 500
    CACHE_TTL: int = 3600


class DashboardSettings(BaseSettings):
    """
    Comprehensive dashboard configuration with environment-specific settings
    """
    
    # Environment and deployment
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Application environment")
    debug: bool = Field(default=True, description="Enable debug mode")
    
    # Application settings
    app_title: str = Field(default="AI Adoption Dashboard", description="Dashboard title")
    app_version: str = Field(default="2.2.1", description="Application version")
    page_icon: str = Field(default="🤖", description="Page icon")
    
    # Data settings
    data_directory: Path = Field(default=Path("data"), description="Data files directory")
    cache_ttl_seconds: int = Field(default=3600, ge=60, le=86400, description="Cache TTL in seconds")
    max_file_size_mb: int = Field(default=50, ge=1, le=500, description="Max upload file size in MB")
    
    # Performance settings
    enable_memory_monitoring: bool = Field(default=True, description="Enable memory monitoring")
    memory_warning_threshold_mb: int = Field(default=512, ge=100, description="Memory warning threshold")
    memory_critical_threshold_mb: int = Field(default=1024, ge=500, description="Memory critical threshold")
    max_chart_points: int = Field(default=1000, ge=100, le=10000, description="Max points in charts")
    
    # Security settings
    allowed_file_extensions: List[str] = Field(
        default=[".csv", ".xlsx", ".json"], 
        description="Allowed file extensions for uploads"
    )
    enable_file_validation: bool = Field(default=True, description="Enable file content validation")
    
    # Logging settings
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")
    enable_performance_logging: bool = Field(default=True, description="Enable performance logging")
    
    # Feature flags
    enable_advanced_analytics: bool = Field(default=True, description="Enable advanced analytics features")
    enable_export_features: bool = Field(default=True, description="Enable data export features")
    enable_user_uploads: bool = Field(default=True, description="Enable user file uploads")
    enable_ai_insights: bool = Field(default=True, description="Enable AI-powered insights")
    
    # External services (for future extensions)
    api_timeout_seconds: int = Field(default=30, ge=5, le=300, description="API timeout in seconds")
    retry_attempts: int = Field(default=3, ge=1, le=10, description="Number of retry attempts")
    
    # Data quality settings
    min_data_quality_score: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum data quality score")
    outlier_detection_threshold: float = Field(default=1.5, ge=1.0, le=5.0, description="Outlier detection threshold")
    
    @validator('data_directory')
    def validate_data_directory(cls, v):
        """Ensure data directory exists"""
        if isinstance(v, str):
            v = Path(v)
        
        # Create directory if it doesn't exist
        try:
            v.mkdir(parents=True, exist_ok=True)
            logger.info(f"Data directory validated: {v}")
        except Exception as e:
            logger.warning(f"Could not create data directory {v}: {e}")
        
        return v
    
    @validator('memory_critical_threshold_mb')
    def critical_must_exceed_warning(cls, v, values):
        """Critical threshold must be higher than warning threshold"""
        if 'memory_warning_threshold_mb' in values and v <= values['memory_warning_threshold_mb']:
            raise ValueError("Critical threshold must be higher than warning threshold")
        return v
    
    @validator('allowed_file_extensions')
    def validate_file_extensions(cls, v):
        """Ensure all extensions start with dot"""
        validated = []
        for ext in v:
            if not ext.startswith('.'):
                ext = f'.{ext}'
            validated.append(ext.lower())
        return validated
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefixes
        env_prefix = "DASHBOARD_"
        
        # Field aliases for environment variables
        fields = {
            'data_directory': {'env': 'DATA_DIR'},
            'log_file': {'env': 'LOG_FILE'},
            'debug': {'env': 'DEBUG'},
            'environment': {'env': 'ENV'}
        }


class ProductionSettings(DashboardSettings):
    """Production-specific settings with security hardening"""
    
    debug: bool = Field(default=False, description="Debug disabled in production")
    environment: Environment = Field(default=Environment.PRODUCTION)
    log_level: LogLevel = Field(default=LogLevel.WARNING, description="Higher log level for production")
    cache_ttl_seconds: int = Field(default=7200, description="Longer cache in production")
    enable_performance_logging: bool = Field(default=False, description="Reduce logging overhead")
    
    # Stricter security settings
    max_file_size_mb: int = Field(default=25, description="Smaller max file size")
    allowed_file_extensions: List[str] = Field(default=[".csv"], description="Only CSV in production")


class DevelopmentSettings(DashboardSettings):
    """Development-specific settings with enhanced debugging"""
    
    debug: bool = Field(default=True, description="Debug enabled in development")
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    log_level: LogLevel = Field(default=LogLevel.DEBUG, description="Verbose logging for development")
    cache_ttl_seconds: int = Field(default=300, description="Short cache for development")
    enable_performance_logging: bool = Field(default=True, description="Full performance logging")
    
    # More permissive settings for development
    max_file_size_mb: int = Field(default=100, description="Larger files for testing")
    memory_warning_threshold_mb: int = Field(default=256, description="Lower threshold for testing")


class TestingSettings(DashboardSettings):
    """Testing-specific settings"""
    
    debug: bool = Field(default=True, description="Debug enabled for testing")
    environment: Environment = Field(default=Environment.TESTING)
    log_level: LogLevel = Field(default=LogLevel.DEBUG, description="Verbose logging for tests")
    cache_ttl_seconds: int = Field(default=60, description="Very short cache for tests")
    
    # Minimal resources for testing
    max_chart_points: int = Field(default=100, description="Small datasets for tests")
    memory_warning_threshold_mb: int = Field(default=128, description="Low threshold for tests")
    max_file_size_mb: int = Field(default=10, description="Small files for tests")


# Replace hardcoded default values from your dynamic_metrics function
@dataclass
class DataConfig:
    DEFAULT_ADOPTION_RATE: float = 78.0
    DEFAULT_GENAI_RATE: float = 71.0
    DEFAULT_COST_REDUCTION: str = "280x cheaper"
    DEFAULT_INVESTMENT_VALUE: str = "$252.3B"
    DEFAULT_MARKET_DELTA: str = "+23pp vs 2023"
    DEFAULT_GENAI_DELTA: str = "+38pp vs 2023"
    DEFAULT_INVESTMENT_DELTA: str = "+44.5% YoY"
    DEFAULT_COST_PERIOD: str = "Since Nov 2022"
    DEFAULT_AVG_ROI: str = "3.2x"
    DEFAULT_ROI_DESC: str = "Across sectors"


# Main configuration class
class DashboardConfig:
    VERSION: str = "2.2.1"
    
    # Sub-configurations
    METRICS = MetricThresholds()
    UI = UIConfig()
    DATA = DataConfig()
    FEATURES = FeatureFlags()
    
    @classmethod
    def is_feature_enabled(cls, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return getattr(cls.FEATURES, feature_name.upper(), False)


# Complete view list for backward compatibility
ALL_VIEWS = [
    # Executive Views
    ViewType.STRATEGIC_BRIEF,
    ViewType.COMPETITIVE_POSITION,
    ViewType.INVESTMENT_CASE,
    ViewType.MARKET_INTELLIGENCE,
    ViewType.ACTION_PLANNING,
    
    # Detailed Views
    ViewType.COMPETITIVE_POSITION_ASSESSOR,
    ViewType.INVESTMENT_ENGINE,
    ViewType.REGULATORY_RADAR,
    ViewType.HISTORICAL_TRENDS,
    ViewType.INDUSTRY_ANALYSIS,
    ViewType.FINANCIAL_IMPACT,
    ViewType.ROI_ANALYSIS,
    ViewType.ADOPTION_RATES,
    ViewType.FIRM_SIZE_ANALYSIS,
    ViewType.GEOGRAPHIC_DISTRIBUTION,
    ViewType.TECHNOLOGY_STACK,
    ViewType.AI_COST_TRENDS,
    ViewType.PRODUCTIVITY_RESEARCH,
    ViewType.LABOR_IMPACT,
    ViewType.ENVIRONMENTAL_IMPACT,
    ViewType.AI_GOVERNANCE,
    ViewType.SKILL_GAP_ANALYSIS,
    ViewType.BARRIERS_SUPPORT,
    ViewType.TOKEN_ECONOMICS,
    ViewType.INVESTMENT_TRENDS,
    ViewType.REGIONAL_GROWTH,
    ViewType.AI_TECHNOLOGY_MATURITY,
    ViewType.OECD_FINDINGS,
    ViewType.BIBLIOGRAPHY_SOURCES,
]

FEATURE_FLAGS = {
    'executive_mode': FeatureFlags.EXECUTIVE_MODE,
    'visual_redesign': FeatureFlags.VISUAL_REDESIGN,
    'strategic_callouts': FeatureFlags.STRATEGIC_CALLOUTS,
    'competitive_homepage': FeatureFlags.COMPETITIVE_HOMEPAGE
}


def get_settings() -> DashboardSettings:
    """
    Get settings based on environment with automatic detection
    
    Returns:
        Appropriate settings instance based on environment
    """
    env = os.getenv("DASHBOARD_ENV", "development").lower()
    
    settings_map = {
        "production": ProductionSettings,
        "staging": ProductionSettings,  # Use production settings for staging
        "development": DevelopmentSettings,
        "testing": TestingSettings
    }
    
    settings_class = settings_map.get(env, DevelopmentSettings)
    
    try:
        settings = settings_class()
        logger.info(f"Loaded {settings_class.__name__} for environment: {env}")
        return settings
    except Exception as e:
        logger.error(f"Failed to load settings for environment {env}: {e}")
        # Fallback to development settings
        logger.info("Falling back to development settings")
        return DevelopmentSettings()


def validate_settings(settings: DashboardSettings) -> List[str]:
    """
    Validate settings and return any warnings
    
    Args:
        settings: Settings instance to validate
        
    Returns:
        List of validation warnings
    """
    warnings = []
    
    # Check data directory accessibility
    if not settings.data_directory.exists():
        warnings.append(f"Data directory does not exist: {settings.data_directory}")
    elif not os.access(settings.data_directory, os.R_OK):
        warnings.append(f"Data directory is not readable: {settings.data_directory}")
    
    # Check log file accessibility if specified
    if settings.log_file:
        log_path = Path(settings.log_file)
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            # Test write access
            with open(log_path, 'a') as f:
                pass
        except Exception as e:
            warnings.append(f"Cannot write to log file {settings.log_file}: {e}")
    
    # Validate memory thresholds
    if settings.memory_critical_threshold_mb <= settings.memory_warning_threshold_mb:
        warnings.append("Critical memory threshold should be higher than warning threshold")
    
    # Check feature flag consistency
    if not settings.enable_user_uploads and settings.max_file_size_mb > 0:
        warnings.append("File uploads disabled but max file size is configured")
    
    return warnings


def setup_logging(settings: DashboardSettings) -> None:
    """
    Configure logging based on settings
    
    Args:
        settings: Settings instance with logging configuration
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging_config = {
        'level': getattr(logging, settings.log_level.upper()),
        'format': log_format,
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
    
    if settings.log_file:
        logging_config['filename'] = settings.log_file
        logging_config['filemode'] = 'a'
    
    logging.basicConfig(**logging_config)
    
    # Set specific logger levels
    if settings.environment == Environment.PRODUCTION:
        # Reduce noise in production
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger.info(f"Logging configured: level={settings.log_level}, file={settings.log_file}")


# Global settings instance
_settings: Optional[DashboardSettings] = None


def get_global_settings() -> DashboardSettings:
    """
    Get global settings instance (singleton pattern)
    
    Returns:
        Global settings instance
    """
    global _settings
    if _settings is None:
        _settings = get_settings()
        
        # Validate settings and log warnings
        warnings = validate_settings(_settings)
        for warning in warnings:
            logger.warning(f"Settings validation: {warning}")
        
        # Setup logging
        setup_logging(_settings)
    
    return _settings


def reload_settings() -> DashboardSettings:
    """
    Force reload of settings (useful for testing)
    
    Returns:
        Reloaded settings instance
    """
    global _settings
    _settings = None
    return get_global_settings()


# Convenience access to common settings
def is_debug() -> bool:
    """Check if debug mode is enabled"""
    return get_global_settings().debug


def is_production() -> bool:
    """Check if running in production"""
    return get_global_settings().environment == Environment.PRODUCTION


def get_data_directory() -> Path:
    """Get configured data directory"""
    return get_global_settings().data_directory


def get_cache_ttl() -> int:
    """Get cache TTL in seconds"""
    return get_global_settings().cache_ttl_seconds


def is_feature_enabled(feature_name: str) -> bool:
    """
    Check if a feature is enabled
    
    Args:
        feature_name: Name of the feature flag
        
    Returns:
        True if feature is enabled
    """
    settings = get_global_settings()
    feature_attr = f"enable_{feature_name}"
    return getattr(settings, feature_attr, False)