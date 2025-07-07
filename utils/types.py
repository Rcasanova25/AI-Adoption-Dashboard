"""Type definitions for the AI Adoption Dashboard."""

from typing import Any, Dict, List, Optional, TypedDict, Union

import pandas as pd


class DashboardData(TypedDict, total=False):
    """Type definition for dashboard data structure.

    This matches the consolidated data structure used in app.py load_data function.
    """

    # Historical trends data
    historical_data: pd.DataFrame

    # Sector adoption data
    sector_2018: pd.DataFrame
    sector_2025: pd.DataFrame

    # Firm size analysis
    firm_size: pd.DataFrame

    # AI maturity data
    ai_maturity: pd.DataFrame

    # Geographic data
    geographic: pd.DataFrame
    state_data: pd.DataFrame

    # Financial and investment data
    financial_impact: pd.DataFrame
    ai_investment_data: pd.DataFrame

    # Additional data from various sources
    adoption_trends: pd.DataFrame
    use_cases: pd.DataFrame
    investment_trends: pd.DataFrame
    productivity_gains: pd.DataFrame
    cost_trends: pd.DataFrame
    token_economics: pd.DataFrame

    # Economic impact data
    gdp_impact: pd.DataFrame
    labor_impact: pd.DataFrame

    # Industry and technology data
    industry_adoption: pd.DataFrame
    technology_stack: pd.DataFrame
    barriers_support: pd.DataFrame

    # Regional and governance data
    regional_growth: pd.DataFrame
    ai_governance: pd.DataFrame
    environmental_impact: pd.DataFrame

    # Skills and workforce data
    skill_gap_analysis: pd.DataFrame
    workforce_impact: pd.DataFrame

    # ROI and cost analysis
    roi_analysis: pd.DataFrame
    ai_cost_trends: pd.DataFrame

    # Research and academic data
    academic_research: pd.DataFrame
    productivity_research: pd.DataFrame

    # OECD specific findings
    oecd_findings: pd.DataFrame
    oecd_recommendations: pd.DataFrame

    # Source metadata
    sources: Dict[str, Any]
    last_updated: str


class MetricData(TypedDict):
    """Type definition for metric card data."""

    label: str
    value: str
    delta: Optional[str]
    insight: Optional[str]
    trend: Optional[List[float]]


class ChartConfig(TypedDict, total=False):
    """Type definition for chart configuration."""

    title: str
    x_label: str
    y_label: str
    color_scheme: str
    chart_type: str
    height: int
    width: int
    show_legend: bool
    show_grid: bool


class ViewConfig(TypedDict):
    """Type definition for view configuration."""

    name: str
    title: str
    description: str
    icon: str
    requires_data: List[str]
    persona_relevant: List[str]


class PersonaConfig(TypedDict):
    """Type definition for persona configuration."""

    name: str
    description: str
    priorities: List[str]
    recommended_views: List[str]
    key_metrics: List[str]





class PerformanceMetrics(TypedDict):
    """Type definition for performance metrics."""

    load_time: float
    memory_mb: float
    cpu_percent: float
    
    response_time: float
    active_users: int


class ErrorInfo(TypedDict):
    """Type definition for error information."""

    timestamp: str
    error_type: str
    error_message: str
    severity: str
    category: str
    context: Dict[str, Any]
    traceback: str


class DataSourceInfo(TypedDict):
    """Type definition for data source information."""

    name: str
    type: str
    path: str
    last_updated: str
    size_mb: float
    status: str  # 'loaded', 'error', 'pending'
    error: Optional[str]


class FilterConfig(TypedDict, total=False):
    """Type definition for data filter configuration."""

    years: Optional[List[int]]
    sectors: Optional[List[str]]
    regions: Optional[List[str]]
    technologies: Optional[List[str]]
    company_sizes: Optional[List[str]]


class ThemeConfig(TypedDict):
    """Type definition for theme configuration."""

    name: str
    primary_color: str
    secondary_color: str
    background_color: str
    text_color: str
    font_family: str
    font_size: int


class AccessibilityConfig(TypedDict):
    """Type definition for accessibility configuration."""

    high_contrast: bool
    font_size_multiplier: float
    screen_reader_mode: bool
    keyboard_navigation: bool
    reduced_motion: bool


class CacheConfig(TypedDict):
    """Type definition for cache configuration."""
    
    max_size: int
    ttl_seconds: int
    enabled: bool
    backend: str  # 'memory', 'redis', 'disk'
    eviction_policy: str  # 'lru', 'fifo', 'lfu'


# Type aliases for common data structures
DataFrameDict = Dict[str, pd.DataFrame]
MetricDict = Dict[str, MetricData]
ConfigDict = Dict[str, Any]

# Union types for flexible data handling
ChartData = Union[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]
ViewData = Union[DashboardData, DataFrameDict, Dict[str, Any]]

# Optional type helpers
OptionalDataFrame = Optional[pd.DataFrame]
OptionalDict = Optional[Dict[str, Any]]
OptionalList = Optional[List[Any]]
