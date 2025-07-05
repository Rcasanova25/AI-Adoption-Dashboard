"""Economic impact and ROI data models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class EconomicImpact(BaseModel):
    """Economic impact metrics for AI adoption."""

    metric: str = Field(..., description="Economic metric name")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Unit of measurement")
    year: int = Field(..., ge=2020, le=2035)
    confidence_interval_low: Optional[float] = None
    confidence_interval_high: Optional[float] = None
    source: str = Field(..., description="Data source")

    model_config = {"str_strip_whitespace": True}


class ROIMetrics(BaseModel):
    """Return on Investment metrics for AI implementations."""

    implementation_type: str = Field(..., description="Type of AI implementation")
    initial_investment: float = Field(..., ge=0, description="Initial investment amount")
    payback_period_months: int = Field(..., ge=0)
    total_roi_percent: float = Field(..., description="Total ROI percentage")
    annual_savings: float = Field(..., ge=0)
    productivity_gain_percent: float = Field(..., ge=0, le=500)
    breakeven_months: Optional[int] = Field(None, ge=0)
    risk_level: str = Field(..., pattern="^(Low|Medium|High|Very High)$")


class TokenEconomics(BaseModel):
    """Token pricing and economics model."""

    date: str = Field(..., description="Date of pricing")
    model: str = Field(..., description="AI model name")
    price_per_thousand_tokens: float = Field(..., ge=0)
    tokens_per_dollar: float = Field(..., ge=0)
    cost_reduction_factor: float = Field(..., ge=0)
    performance_score: Optional[float] = Field(None, ge=0, le=10)
    market_share_percent: Optional[float] = Field(None, ge=0, le=100)


class ProductivityMetrics(BaseModel):
    """Productivity impact metrics."""

    category: str = Field(..., description="Worker or task category")
    productivity_gain_percent: float = Field(..., ge=-100, le=500)
    time_saved_hours_per_week: float = Field(..., ge=0, le=40)
    quality_improvement_percent: Optional[float] = Field(None, ge=-100, le=500)
    adoption_difficulty: str = Field(..., pattern="^(Low|Medium|High)$")
    implementation_time_weeks: Optional[int] = Field(None, ge=0)
