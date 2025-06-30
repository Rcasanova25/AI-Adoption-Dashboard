"""
Configuration module - Start here!
This replaces all the hardcoded values scattered throughout your app.py
"""

from dataclasses import dataclass
from typing import Dict, List


# Replace the hardcoded feature flags from your app.py lines 12-19
@dataclass
class FeatureFlags:
    EXECUTIVE_MODE: bool = True
    VISUAL_REDESIGN: bool = True
    STRATEGIC_CALLOUTS: bool = True
    COMPETITIVE_HOMEPAGE: bool = False


# Replace the scattered view lists from your app.py lines 21-45
class ViewType:
    COMPETITIVE_POSITION = "🎯 Competitive Position Assessor"
    INVESTMENT_ENGINE = "💰 Investment Decision Engine"
    REGULATORY_RADAR = "⚖️ Regulatory Risk Radar"
    HISTORICAL_TRENDS = "Historical Trends"
    INDUSTRY_ANALYSIS = "Industry Analysis"
    FINANCIAL_IMPACT = "Financial Impact"
    # Add all your other views here


# Replace hardcoded thresholds scattered throughout
@dataclass
class MetricThresholds:
    MIN_ROI: float = 2.5
    STRONG_ROI: float = 3.0
    HIGH_ADOPTION_RATE: float = 70.0
    COMPETITIVE_THRESHOLD: float = 25.0


# Replace hardcoded UI values
@dataclass
class UIConfig:
    PAGE_TITLE: str = "AI Adoption Dashboard | 2018-2025 Analysis"
    PAGE_ICON: str = "🤖"
    LAYOUT: str = "wide"
    CHART_HEIGHT: int = 500
    CACHE_TTL: int = 3600


# Replace hardcoded default values from your dynamic_metrics function
@dataclass
class DataConfig:
    DEFAULT_ADOPTION_RATE: float = 78.0
    DEFAULT_GENAI_RATE: float = 71.0
    DEFAULT_COST_REDUCTION: str = "280x cheaper"
    DEFAULT_INVESTMENT_VALUE: str = "$252.3B"


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


# For backward compatibility with your existing code
ALL_VIEWS = [
    ViewType.COMPETITIVE_POSITION,
    ViewType.INVESTMENT_ENGINE,
    ViewType.REGULATORY_RADAR,
    ViewType.HISTORICAL_TRENDS,
    ViewType.INDUSTRY_ANALYSIS,
    ViewType.FINANCIAL_IMPACT,
    # ... add all your views
]

FEATURE_FLAGS = {
    'executive_mode': FeatureFlags.EXECUTIVE_MODE,
    'visual_redesign': FeatureFlags.VISUAL_REDESIGN,
    'strategic_callouts': FeatureFlags.STRATEGIC_CALLOUTS,
    'competitive_homepage': FeatureFlags.COMPETITIVE_HOMEPAGE
}