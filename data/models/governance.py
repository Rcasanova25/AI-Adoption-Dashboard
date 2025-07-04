"""AI governance and policy data models."""

from typing import Optional, List
from pydantic import BaseModel, Field


class GovernanceMetrics(BaseModel):
    """AI governance implementation metrics."""
    governance_area: str = Field(..., description="Area of governance")
    implementation_rate_percent: float = Field(..., ge=0, le=100)
    maturity_score: float = Field(..., ge=0, le=10)
    compliance_status: str = Field(..., pattern="^(None|Partial|Full)$")
    regulatory_requirements: List[str] = Field(default_factory=list)
    best_practices_adopted: Optional[int] = Field(None, ge=0)
    

class PolicyFramework(BaseModel):
    """AI policy framework model."""
    country_or_region: str = Field(..., description="Country or region name")
    policy_name: str = Field(..., description="Name of AI policy or framework")
    policy_type: str = Field(..., pattern="^(Regulation|Guidelines|Framework|Strategy|Law)$")
    implementation_year: int = Field(..., ge=2015, le=2030)
    maturity_level: str = Field(..., pattern="^(Draft|Proposed|Adopted|Implemented|Enforced)$")
    scope: List[str] = Field(default_factory=list, description="Areas covered by policy")
    enforcement_mechanism: Optional[str] = None
    penalties_defined: bool = Field(False)
    innovation_impact_score: Optional[float] = Field(None, ge=-10, le=10)