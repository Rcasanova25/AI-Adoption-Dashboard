"""Workforce impact and skills data models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class WorkforceImpact(BaseModel):
    """Workforce impact metrics from AI adoption."""

    job_category: str = Field(..., description="Job category or occupation")
    automation_risk_percent: float = Field(..., ge=0, le=100)
    augmentation_potential_percent: float = Field(..., ge=0, le=100)
    jobs_displaced: Optional[int] = Field(None, ge=0)
    jobs_created: Optional[int] = Field(None, ge=0)
    net_employment_change: Optional[int] = None
    reskilling_required: str = Field(..., pattern="^(Low|Medium|High|Critical)$")
    timeline_years: int = Field(..., ge=0, le=20)


class SkillGaps(BaseModel):
    """Skills gap analysis model."""

    skill_category: str = Field(..., description="Skill category name")
    demand_index: float = Field(..., ge=0, le=100, description="Demand level (0-100)")
    supply_index: float = Field(..., ge=0, le=100, description="Supply level (0-100)")
    gap_severity: str = Field(..., pattern="^(Low|Medium|High|Critical)$")
    training_time_months: Optional[int] = Field(None, ge=0)
    salary_premium_percent: Optional[float] = Field(None, ge=0)


class ProductivityMetrics(BaseModel):
    """Worker productivity metrics."""

    worker_category: str = Field(..., description="Category of workers")
    baseline_productivity: float = Field(100.0, description="Baseline productivity index")
    ai_enhanced_productivity: float = Field(..., ge=0)
    productivity_gain_percent: float = Field(..., ge=-100, le=500)
    implementation_cost_per_worker: Optional[float] = Field(None, ge=0)
    training_hours_required: Optional[int] = Field(None, ge=0)
    adoption_rate_percent: Optional[float] = Field(None, ge=0, le=100)
