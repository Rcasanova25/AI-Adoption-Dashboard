"""Data models for AI adoption metrics."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class AdoptionMetrics(BaseModel):
    """Core AI adoption metrics."""

    year: int = Field(..., ge=2017, le=2030)
    overall_adoption: float = Field(..., ge=0, le=100, description="Overall AI adoption percentage")
    genai_adoption: float = Field(
        ..., ge=0, le=100, description="Generative AI adoption percentage"
    )
    predictive_adoption: float = Field(
        ..., ge=0, le=100, description="Predictive AI adoption percentage"
    )
    nlp_adoption: float = Field(..., ge=0, le=100, description="NLP adoption percentage")
    computer_vision_adoption: float = Field(
        ..., ge=0, le=100, description="Computer Vision adoption percentage"
    )
    robotics_adoption: float = Field(..., ge=0, le=100, description="Robotics adoption percentage")

    @field_validator("overall_adoption", "genai_adoption", "predictive_adoption", 
                     "nlp_adoption", "computer_vision_adoption", "robotics_adoption")
    def validate_percentage(cls, v):
        """Ensure adoption rates are valid percentages."""
        if not 0 <= v <= 100:
            raise ValueError(f"Adoption rate must be between 0 and 100, got {v}")
        return v


class SectorAdoption(BaseModel):
    """Sector-specific AI adoption data."""

    sector: str = Field(..., description="Industry sector name")
    year: int = Field(..., ge=2017, le=2030)
    adoption_rate: float = Field(..., ge=0, le=100)
    genai_adoption: Optional[float] = Field(None, ge=0, le=100)
    investment_millions: Optional[float] = Field(None, ge=0)
    use_cases: List[str] = Field(default_factory=list)
    maturity_score: Optional[float] = Field(None, ge=0, le=5)
    barriers: List[str] = Field(default_factory=list)

    model_config = {"str_strip_whitespace": True}


class GeographicAdoption(BaseModel):
    """Geographic AI adoption data."""

    location: str = Field(..., description="City, state, or country")
    location_type: str = Field(..., pattern="^(city|state|country)$")
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    adoption_rate: float = Field(..., ge=0, le=100)
    year: int = Field(..., ge=2017, le=2030)
    ai_companies: Optional[int] = Field(None, ge=0)
    research_institutions: Optional[int] = Field(None, ge=0)
    investment_millions: Optional[float] = Field(None, ge=0)
    talent_availability_score: Optional[float] = Field(None, ge=0, le=10)

    @field_validator("location_type")
    def validate_location_type(cls, v):
        """Ensure location type is valid."""
        valid_types = {"city", "state", "country"}
        if v not in valid_types:
            raise ValueError(f"Location type must be one of {valid_types}")
        return v
