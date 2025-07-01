"""
Configuration module - Start here!
This replaces all the hardcoded values scattered throughout your app.py
"""

from dataclasses import dataclass
from typing import Dict, List, Literal


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