"""
Data models and validation for AI Adoption Dashboard
Uses Pydantic for robust data validation and type safety
"""

from typing import Any, Dict, List, Optional, Union, Literal, Type
from datetime import datetime
import pandas as pd
import logging
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationInfo

logger = logging.getLogger(__name__)


class HistoricalDataPoint(BaseModel):
    """Model for historical AI adoption data points"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    year: int = Field(..., ge=2017, le=2025, description="Year of the data point")
    ai_use: float = Field(..., ge=0, le=100, description="Overall AI adoption percentage")
    genai_use: float = Field(..., ge=0, le=100, description="Generative AI adoption percentage")
    
    @field_validator('genai_use')
    @classmethod
    def genai_cannot_exceed_ai(cls, v, info: ValidationInfo):
        """GenAI adoption cannot exceed overall AI adoption"""
        if info.data and 'ai_use' in info.data and v > info.data['ai_use']:
            raise ValueError("GenAI adoption cannot exceed overall AI adoption")
        return v
    
    @field_validator('year')
    @classmethod
    def year_must_be_reasonable(cls, v):
        """Ensure year is within reasonable bounds"""
        if v < 2017 or v > 2025:
            raise ValueError("Year must be between 2017 and 2025")
        return v


class SectorData(BaseModel):
    """Model for sector-specific AI adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    sector: str = Field(..., min_length=2, max_length=50, description="Industry sector name")
    adoption_rate: Optional[float] = Field(None, ge=0, le=100, description="AI adoption rate percentage")
    genai_adoption: Optional[float] = Field(None, ge=0, le=100, description="GenAI adoption rate percentage")
    avg_roi: Optional[float] = Field(None, gt=0, le=10, description="Average ROI multiplier")
    firm_weighted: Optional[float] = Field(None, ge=0, le=100, description="Firm-weighted adoption rate")
    employment_weighted: Optional[float] = Field(None, ge=0, le=100, description="Employment-weighted adoption rate")
    
    @field_validator('sector')
    @classmethod
    def sector_must_be_valid(cls, v):
        """Validate sector names against known list"""
        allowed_sectors = {
            'Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
            'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government',
            'Information', 'Professional Services', 'Finance & Insurance', 'Retail Trade', 'Construction'
        }
        if v not in allowed_sectors:
            logger.warning(f'Sector "{v}" not in predefined list: {allowed_sectors}')
        return v
    
    @field_validator('genai_adoption')
    @classmethod
    def genai_cannot_exceed_overall(cls, v, info: ValidationInfo):
        """GenAI adoption cannot exceed overall adoption"""
        if info.data and 'adoption_rate' in info.data and v and info.data['adoption_rate'] and v > info.data['adoption_rate']:
            raise ValueError("GenAI adoption cannot exceed overall adoption rate")
        return v
    
    @field_validator('avg_roi')
    @classmethod
    def roi_must_be_reasonable(cls, v):
        """ROI should be reasonable (typically 0.5x to 10x)"""
        if v < 0.1:
            raise ValueError(f'ROI {v}x is unreasonably low')
        if v > 20:
            logger.warning(f'ROI {v}x is unusually high - please verify')
        return v


class FirmSizeData(BaseModel):
    """Model for firm size adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    size: str = Field(..., description="Employee size range (e.g., '1-4', '5000+')")
    adoption: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    
    @field_validator('size')
    @classmethod
    def validate_size_format(cls, v):
        """Validate size format contains numbers or follows expected patterns"""
        import re
        # Allow patterns like "1-4", "5000+", "Small (1-50)"
        if not re.search(r'\d', v):
            raise ValueError(f'Size "{v}" must contain numeric information')
        return v
    
    @field_validator('adoption')
    @classmethod
    def adoption_correlation_check(cls, v, info: ValidationInfo):
        """Larger firms typically have higher adoption rates"""
        if info.data and 'size' in info.data:
            size = info.data['size']
            # Basic correlation check - larger firms should have higher adoption
            if '1-4' in size and v > 10:
                raise ValueError("Very small firms (1-4 employees) typically have low adoption rates")
        return v


class InvestmentData(BaseModel):
    """Model for AI investment data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    year: int = Field(..., ge=2014, le=2030, description="Investment year")
    total_investment: float = Field(..., ge=0, description="Total AI investment in billions USD")
    genai_investment: Optional[float] = Field(None, ge=0, description="GenAI investment in billions USD")
    us_investment: Optional[float] = Field(None, ge=0, description="US investment in billions USD")
    china_investment: Optional[float] = Field(None, ge=0, description="China investment in billions USD")
    uk_investment: Optional[float] = Field(None, ge=0, description="UK investment in billions USD")
    
    @field_validator('genai_investment')
    @classmethod
    def genai_cannot_exceed_total(cls, v, info: ValidationInfo):
        """GenAI investment cannot exceed total investment"""
        if info.data and 'total_investment' in info.data and v and info.data['total_investment'] and v > info.data['total_investment']:
            raise ValueError("GenAI investment cannot exceed total investment")
        return v
    
    @field_validator('us_investment', 'china_investment', 'uk_investment')
    @classmethod
    def regional_cannot_exceed_total(cls, v, info: ValidationInfo):
        """Regional investment cannot exceed total investment"""
        if info.data and 'total_investment' in info.data and v and info.data['total_investment'] and v > info.data['total_investment']:
            raise ValueError("Regional investment cannot exceed total investment")
        return v
    
    @field_validator('total_investment')
    @classmethod
    def investment_growth_check(cls, v, info: ValidationInfo):
        """Investment should generally increase over time"""
        if info.data and 'year' in info.data:
            year = info.data['year']
            # Basic growth expectation - later years should have higher investment
            if year >= 2023 and v < 50:  # 2023+ should have significant investment
                raise ValueError("Recent years should have substantial AI investment")
        return v


class FinancialImpactData(BaseModel):
    """Model for financial impact by business function"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    function: str = Field(..., min_length=2, max_length=50, description="Business function name")
    companies_reporting_cost_savings: float = Field(..., ge=0, le=100, description="% of companies reporting cost savings")
    companies_reporting_revenue_gains: float = Field(..., ge=0, le=100, description="% of companies reporting revenue gains")
    avg_cost_reduction: Optional[float] = Field(None, ge=0, le=100, description="Average cost reduction percentage")
    avg_revenue_increase: Optional[float] = Field(None, ge=0, le=200, description="Average revenue increase percentage")
    
    @field_validator('function')
    @classmethod
    def function_must_be_business_related(cls, v):
        """Validate business function names"""
        valid_functions = {
            'Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering',
            'Product Development', 'IT', 'HR', 'Finance', 'Operations', 'Customer Service',
            'Research & Development', 'Legal', 'Procurement'
        }
        if v not in valid_functions:
            logger.warning(f'Function "{v}" not in standard business functions list')
        return v
    
    @field_validator('avg_cost_reduction')
    @classmethod
    def cost_reduction_reasonable(cls, v):
        """Cost reduction should be reasonable"""
        if v is not None and v > 50:
            logger.warning(f'Cost reduction {v}% is very high - please verify')
        return v


class GeographicData(BaseModel):
    """Model for geographic AI adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    city: str = Field(..., min_length=2, max_length=50, description="City name")
    state: str = Field(..., min_length=2, max_length=50, description="State name")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    rate: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    state_code: str = Field(..., min_length=2, max_length=2, description="Two-letter state code")
    population_millions: Optional[float] = Field(None, gt=0, description="Population in millions")
    gdp_billions: Optional[float] = Field(None, gt=0, description="GDP in billions USD")
    
    @field_validator('state_code')
    @classmethod
    def state_code_format(cls, v):
        """State code should be uppercase"""
        return v.upper()
    
    @field_validator('rate')
    @classmethod
    def rate_correlation_check(cls, v, info: ValidationInfo):
        """Large cities typically have higher adoption rates"""
        if info.data and 'population_millions' in info.data and info.data['population_millions']:
            population = info.data['population_millions']
            if population > 5 and v < 5:  # Large cities should have higher rates
                raise ValueError("Large cities typically have higher AI adoption rates")
        return v


class TokenEconomicsData(BaseModel):
    """Model for token economics data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., min_length=3, max_length=50, description="AI model name")
    cost_per_million_input: float = Field(..., ge=0, description="Cost per million input tokens in USD")
    cost_per_million_output: float = Field(..., ge=0, description="Cost per million output tokens in USD")
    context_window: Optional[int] = Field(None, gt=0, description="Context window size in tokens")
    tokens_per_second: Optional[float] = Field(None, gt=0, description="Processing speed in tokens per second")
    
    @field_validator('cost_per_million_input', 'cost_per_million_output')
    @classmethod
    def cost_reasonable(cls, v):
        """Token costs should be reasonable"""
        if v > 100:
            logger.warning(f'Token cost ${v} per million seems very high')
        if v < 0.001:
            logger.warning(f'Token cost ${v} per million seems very low')
        return v
    
    @field_validator('context_window')
    @classmethod
    def context_window_reasonable(cls, v):
        """Context window should be reasonable"""
        if v is not None:
            if v < 1000:
                logger.warning(f'Context window {v} tokens seems small')
            if v > 2000000:
                logger.warning(f'Context window {v} tokens seems very large')
        return v


class AIMaturityData(BaseModel):
    """Model for AI technology maturity assessment"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    technology: str = Field(..., min_length=3, max_length=50, description="Technology name")
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    maturity: Literal[
        'Innovation Trigger', 'Peak of Expectations', 'Trough of Disillusionment',
        'Slope of Enlightenment', 'Plateau of Productivity'
    ] = Field(..., description="Gartner Hype Cycle stage")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0=low risk, 100=high risk)")
    time_to_value: int = Field(..., gt=0, le=10, description="Expected time to value in years")
    
    @field_validator('technology')
    @classmethod
    def technology_name_valid(cls, v):
        """Validate technology names"""
        valid_technologies = {
            'Machine Learning', 'Deep Learning', 'Natural Language Processing',
            'Computer Vision', 'Robotic Process Automation', 'Predictive Analytics',
            'Generative AI', 'Large Language Models', 'Computer Vision',
            'Speech Recognition', 'Recommendation Systems', 'Autonomous Systems'
        }
        if v not in valid_technologies:
            logger.warning(f'Technology "{v}" not in standard list')
        return v
    
    @field_validator('risk_score')
    @classmethod
    def risk_score_correlation(cls, v, info: ValidationInfo):
        """Risk score should correlate with maturity stage"""
        if info.data and 'maturity' in info.data:
            maturity = info.data['maturity']
            # Higher risk for early stages
            if maturity in ['Innovation Trigger', 'Peak of Expectations'] and v < 70:
                raise ValueError("Early maturity stages should have higher risk scores")
        return v


class ProductivityData(BaseModel):
    """Model for productivity research data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    year: int = Field(..., description="Year of data point")
    productivity_growth: float = Field(..., description="Productivity growth (%)")
    young_workers_share: float = Field(..., description="Share of young workers (%)")
    
    @field_validator('productivity_growth')
    @classmethod
    def productivity_growth_reasonable(cls, v):
        """Productivity growth should be reasonable"""
        if v > 50:
            logger.warning(f'Productivity growth {v}% is very high - please verify')
        return v


class ProductivityBySkillData(BaseModel):
    """Model for productivity by skill level"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill_level: str = Field(..., description="Skill level category")
    productivity_gain: float = Field(..., description="Productivity gain (%)")
    skill_gap_reduction: float = Field(..., description="Skill gap reduction (%)")
    
    @field_validator('skill_level')
    @classmethod
    def skill_level_valid(cls, v):
        """Validate skill level categories"""
        valid_levels = {'Low', 'Medium', 'High', 'Expert', 'Beginner', 'Advanced'}
        if v not in valid_levels:
            logger.warning(f'Skill level "{v}" not in standard categories')
        return v


class AIProductivityEstimatesData(BaseModel):
    """Model for AI productivity estimates"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    source: str = Field(..., description="Source of estimate")
    annual_impact: float = Field(..., description="Annual impact (%)")
    
    @field_validator('source')
    @classmethod
    def source_valid(cls, v):
        """Validate source names"""
        valid_sources = {'Conservative', 'Moderate', 'Optimistic', 'Aggressive'}
        if v not in valid_sources:
            logger.warning(f'Source "{v}" not in standard categories')
        return v


class OECDG7AdoptionData(BaseModel):
    """Model for OECD G7 adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    country: str = Field(..., description="G7 country name")
    adoption_rate: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    genai_adoption: Optional[float] = Field(None, ge=0, le=100, description="GenAI adoption rate")
    digital_readiness: Optional[float] = Field(None, ge=0, le=100, description="Digital readiness score")
    
    @field_validator('country')
    @classmethod
    def country_must_be_g7(cls, v):
        """Validate G7 country names"""
        g7_countries = {'Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States'}
        if v not in g7_countries:
            logger.warning(f'Country "{v}" not in G7 list')
        return v


class OECDApplicationsData(BaseModel):
    """Model for OECD AI applications data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    application: str = Field(..., description="AI application name")
    usage_rate: float = Field(..., description="Usage rate (%)")
    category: str = Field(..., description="Application category")
    
    @field_validator('application')
    @classmethod
    def application_name_valid(cls, v):
        """Validate AI application names"""
        valid_applications = {
            'Customer Service', 'Marketing', 'Sales', 'Product Development',
            'Supply Chain', 'HR', 'Finance', 'IT Operations', 'Research',
            'Quality Control', 'Predictive Maintenance', 'Fraud Detection'
        }
        if v not in valid_applications:
            logger.warning(f'Application "{v}" not in standard list')
        return v


class BarriersData(BaseModel):
    """Model for AI adoption barriers"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    barrier: str = Field(..., description="Barrier description")
    percentage: float = Field(..., description="Percentage of companies reporting barrier")
    
    @field_validator('barrier')
    @classmethod
    def barrier_name_valid(cls, v):
        """Validate barrier names"""
        valid_barriers = {
            'Lack of Skills', 'High Costs', 'Data Quality Issues', 'Integration Challenges',
            'Security Concerns', 'Regulatory Uncertainty', 'Change Management', 'ROI Uncertainty'
        }
        if v not in valid_barriers:
            logger.warning(f'Barrier "{v}" not in standard list')
        return v


class SupportEffectivenessData(BaseModel):
    """Model for support effectiveness data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    support_type: str = Field(..., description="Type of support")
    effectiveness_score: float = Field(..., description="Effectiveness score")
    
    @field_validator('support_type')
    @classmethod
    def support_type_valid(cls, v):
        """Validate support types"""
        valid_types = {
            'Training Programs', 'Consulting Services', 'Technical Support',
            'Financial Incentives', 'Regulatory Guidance', 'Best Practices'
        }
        if v not in valid_types:
            logger.warning(f'Support type "{v}" not in standard list')
        return v


class RegionalGrowthData(BaseModel):
    """Model for regional growth data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    region: str = Field(..., description="Geographic region")
    growth_2024: float = Field(..., description="Growth in 2024 (%)")
    adoption_rate: float = Field(..., description="Current adoption rate (%)")
    investment_growth: float = Field(..., description="Investment growth (%)")
    
    @field_validator('region')
    @classmethod
    def region_name_valid(cls, v):
        """Validate region names"""
        valid_regions = {
            'North America', 'Europe', 'Asia Pacific', 'Latin America',
            'Middle East', 'Africa', 'Global'
        }
        if v not in valid_regions:
            logger.warning(f'Region "{v}" not in standard list')
        return v


class AICostReductionData(BaseModel):
    """Model for AI cost reduction data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., description="AI model name")
    cost_per_million_tokens: float = Field(..., ge=0, description="Cost per million tokens in USD")
    reduction_factor: Optional[float] = Field(None, gt=0, description="Cost reduction factor")
    
    @field_validator('cost_per_million_tokens')
    @classmethod
    def cost_reasonable(cls, v):
        """Cost should be reasonable"""
        if v > 100:
            logger.warning(f'Cost {v} per million tokens seems high')
        return v


class AIPerceptionData(BaseModel):
    """Model for AI perception data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    generation: str = Field(..., description="Generation name")
    expect_job_change: float = Field(..., description="% expecting job change")
    expect_job_replacement: float = Field(..., description="% expecting job replacement")
    
    @field_validator('generation')
    @classmethod
    def generation_valid(cls, v):
        """Validate generation names"""
        valid_generations = {
            'GenAI 2025', 'GenAI 2030', 'GenAI 2040', 'GenAI 2050'
        }
        if v not in valid_generations:
            logger.warning(f'Generation "{v}" not in standard list')
        return v


class TrainingEmissionsData(BaseModel):
    """Model for AI training emissions data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., description="AI model name")
    carbon_tons: float = Field(..., description="Emissions in tons of CO2")
    
    @field_validator('carbon_tons')
    @classmethod
    def emissions_reasonable(cls, v):
        """Emissions should be reasonable"""
        if v > 1000000:  # 1 million kg CO2
            logger.warning(f'Emissions {v} kg CO2 seems very high')
        return v


class SkillGapData(BaseModel):
    """Model for skill gap analysis data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill: str = Field(..., description="Skill name")
    gap_severity: float = Field(..., description="Gap severity (%)")
    training_initiatives: float = Field(..., description="Training initiatives (%)")
    
    @field_validator('skill')
    @classmethod
    def skill_name_valid(cls, v):
        """Validate skill names"""
        valid_skills = {
            'Machine Learning', 'Data Science', 'Python Programming', 'AI Ethics',
            'Natural Language Processing', 'Computer Vision', 'Cloud Computing',
            'Data Engineering', 'AI Governance', 'Prompt Engineering'
        }
        if v not in valid_skills:
            logger.warning(f'Skill "{v}" not in standard list')
        return v
    
    @field_validator('gap_severity')
    @classmethod
    def gap_severity_reasonable(cls, v):
        """Gap severity should be reasonable"""
        if v > 100:
            logger.warning(f'Gap severity {v}% is very high - please verify')
        return v


class AIGovernanceData(BaseModel):
    """Model for AI governance data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    aspect: str = Field(..., description="Governance aspect")
    adoption_rate: float = Field(..., description="Adoption rate (%)")
    maturity_score: float = Field(..., description="Maturity score (out of 5)")
    
    @field_validator('aspect')
    @classmethod
    def governance_area_valid(cls, v):
        """Validate governance areas"""
        valid_areas = {
            'Data Privacy', 'Algorithmic Bias', 'Transparency', 'Accountability',
            'Security', 'Compliance', 'Ethics Review', 'Risk Management'
        }
        if v not in valid_areas:
            logger.warning(f'Governance area "{v}" not in standard list')
        return v


class GenAI2025Data(BaseModel):
    """Model for GenAI 2025 data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    function: str = Field(..., description="Business function")
    adoption: float = Field(..., description="GenAI adoption (%)")
    
    @field_validator('function')
    @classmethod
    def function_valid(cls, v):
        """Validate function names"""
        valid_functions = {
            'Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering',
            'Product Development', 'IT', 'HR', 'Finance', 'Operations', 'Customer Service',
            'Research & Development', 'Legal', 'Procurement'
        }
        if v not in valid_functions:
            logger.warning(f'Function "{v}" not in standard business functions list')
        return v


class TokenUsagePatternsData(BaseModel):
    """Model for token usage patterns"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    use_case: str = Field(..., description="Use case")
    avg_input_tokens: float = Field(..., description="Average input tokens")
    avg_output_tokens: float = Field(..., description="Average output tokens")
    input_output_ratio: float = Field(..., description="Input/output ratio")
    
    @field_validator('use_case')
    @classmethod
    def use_case_valid(cls, v):
        """Validate use case names"""
        valid_use_cases = {
            'Conversational', 'Document Processing', 'Code Generation',
            'Creative Writing', 'Analysis', 'Translation'
        }
        if v not in valid_use_cases:
            logger.warning(f'Use case "{v}" not in standard list')
        return v


class TokenOptimizationData(BaseModel):
    """Model for token optimization data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    strategy: str = Field(..., description="Optimization strategy")
    cost_reduction: float = Field(..., description="Cost reduction (%)")
    implementation_complexity: float = Field(..., description="Implementation complexity (1-5)")
    time_to_implement: float = Field(..., description="Time to implement (days)")
    
    @field_validator('strategy')
    @classmethod
    def strategy_valid(cls, v):
        """Validate optimization strategies"""
        valid_strategies = {
            'Prompt Engineering', 'Context Window Optimization', 'Model Selection',
            'Batch Processing', 'Caching', 'Compression'
        }
        if v not in valid_strategies:
            logger.warning(f'Strategy "{v}" not in standard list')
        return v


class TokenPricingEvolutionData(BaseModel):
    """Model for token pricing evolution"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: datetime = Field(..., description="Date of pricing")
    avg_price_input: float = Field(..., description="Average input token price")
    avg_price_output: float = Field(..., description="Average output token price")
    models_available: int = Field(..., description="Number of models available")
    
    @field_validator('date')
    @classmethod
    def date_format_valid(cls, v):
        """Validate date format"""
        import re
        if not re.match(r'\d{4}-\d{2}-\d{2}', v):
            logger.warning(f'Date "{v}" not in YYYY-MM-DD format')
        return v


class StateData(BaseModel):
    """Model for state-level data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    state: str = Field(..., description="State name")
    state_code: str = Field(..., min_length=2, max_length=2, description="Two-letter state code")
    rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    adoption_rate: Optional[float] = Field(None, ge=0, le=100, description="Adoption rate percentage (alias)")
    population_millions: Optional[float] = Field(None, gt=0, description="Population in millions")

    @field_validator('state')
    @classmethod
    def state_name_valid(cls, v):
        """Validate US state names"""
        us_states = {
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
            'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
            'Wisconsin', 'Wyoming'
        }
        if v not in us_states:
            logger.warning(f'State "{v}" not in US states list')
        return v


class TechStackData(BaseModel):
    """Model for technology stack data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    technology: str = Field(..., description="Technology name")
    percentage: float = Field(..., ge=0, le=100, description="Usage percentage")
    
    @field_validator('technology')
    @classmethod
    def technology_valid(cls, v):
        """Validate technology names"""
        valid_technologies = {
            'Cloud-based AI', 'On-premise AI', 'Hybrid AI', 'Edge AI',
            'Multi-technology', 'Single Platform', 'Custom Solutions'
        }
        if v not in valid_technologies:
            logger.warning(f'Technology "{v}" not in standard list')
        return v


class ValidationResult(BaseModel):
    """Model for data validation results"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    is_valid: bool = Field(..., description="Whether validation passed")
    error_message: Optional[str] = Field(None, description="Error message if validation failed")
    warning_messages: List[str] = Field(default_factory=list, description="Warning messages")
    validated_rows: int = Field(..., ge=0, description="Number of rows validated")
    total_rows: int = Field(..., ge=0, description="Total number of rows")
    
    @field_validator('validated_rows')
    @classmethod
    def validated_cannot_exceed_total(cls, v, info: ValidationInfo):
        """Validated rows cannot exceed total rows"""
        if info.data and 'total_rows' in info.data and v > info.data['total_rows']:
            raise ValueError("Validated rows cannot exceed total rows")
        return v


class DatasetInfo(BaseModel):
    """Model for dataset metadata"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str = Field(..., min_length=1, description="Dataset name")
    description: str = Field(..., min_length=1, description="Dataset description")
    source: str = Field(..., min_length=1, description="Data source")
    last_updated: datetime = Field(..., description="Last update timestamp")
    row_count: int = Field(..., ge=0, description="Number of rows")
    column_count: int = Field(..., ge=0, description="Number of columns")
    validation_status: ValidationResult = Field(..., description="Validation result")


# Model registry for easy access - UPDATED with all datasets
MODEL_REGISTRY: Dict[str, Type[BaseModel]] = {
    "historical_data": HistoricalDataPoint,
    "sector_2018": SectorData,
    "sector_2025": SectorData,
    "firm_size": FirmSizeData,
    "ai_maturity": AIMaturityData,
    "geographic": GeographicData,
    "state_data": StateData,
    "tech_stack": TechStackData,
    "productivity_data": ProductivityData,
    "productivity_by_skill": ProductivityBySkillData,
    "ai_productivity_estimates": AIProductivityEstimatesData,
    "oecd_g7_adoption": OECDG7AdoptionData,
    "oecd_applications": OECDApplicationsData,
    "barriers_data": BarriersData,
    "support_effectiveness": SupportEffectivenessData,
    "ai_investment_data": InvestmentData,
    "regional_growth": RegionalGrowthData,
    "ai_cost_reduction": AICostReductionData,
    "financial_impact": FinancialImpactData,
    "ai_perception": AIPerceptionData,
    "training_emissions": TrainingEmissionsData,
    "skill_gap_data": SkillGapData,
    "ai_governance": AIGovernanceData,
    "genai_2025": GenAI2025Data,
    "token_economics": TokenEconomicsData,
    "token_usage_patterns": TokenUsagePatternsData,
    "token_optimization": TokenOptimizationData,
    "token_pricing_evolution": TokenPricingEvolutionData
}


def validate_dataframe(
    df: pd.DataFrame, 
    model: Type[BaseModel], 
    sample_size: int = 100
) -> ValidationResult:
    """
    Validate a DataFrame against a Pydantic model
    
    Args:
        df: DataFrame to validate
        model: Pydantic model to validate against
        sample_size: Number of rows to validate (for performance)
    
    Returns:
        ValidationResult with validation status
    """
    if df is None or df.empty:
        return ValidationResult(
            is_valid=False,
            error_message="DataFrame is None or empty",
            total_rows=0,
            validated_rows=0
        )
    
    total_rows = len(df)
    sample_df = df.head(sample_size) if total_rows > sample_size else df
    validated_rows = 0
    errors = []
    warnings = []
    
    for idx, row in sample_df.iterrows():
        try:
            # Validate row using Pydantic model
            validated_row = model(**row.to_dict())
            validated_rows += 1
            
            # Collect any warnings from model validation
            # (Pydantic warnings are typically logged, not raised)
            
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")
            if len(errors) >= 10:  # Limit error reporting
                break
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors) if errors else None
    
    return ValidationResult(
        is_valid=is_valid,
        error_message=error_message,
        warning_messages=warnings,
        validated_rows=validated_rows,
        total_rows=total_rows
    )


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> ValidationResult:
    """
    Validate that DataFrame has required columns
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
    
    Returns:
        ValidationResult with validation status
    """
    if df is None:
        return ValidationResult(
            is_valid=False,
            error_message="DataFrame is None",
            total_rows=0,
            validated_rows=0
        )
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in required_columns]
    
    warnings = []
    if extra_columns:
        warnings.append(f"Extra columns found: {extra_columns}")
    
    if missing_columns:
        return ValidationResult(
            is_valid=False,
            error_message=f"Missing required columns: {missing_columns}",
            warning_messages=warnings,
            total_rows=len(df),
            validated_rows=0
        )
    
    return ValidationResult(
        is_valid=True,
        error_message=None,
        warning_messages=warnings,
        validated_rows=len(df),
        total_rows=len(df)
    )


def get_model_for_dataset(dataset_name: str) -> Optional[Type[BaseModel]]:
    """Get the appropriate Pydantic model for a dataset"""
    return MODEL_REGISTRY.get(dataset_name)


def validate_dataset(df: pd.DataFrame, dataset_name: str) -> ValidationResult:
    """
    Validate a dataset using its registered model
    
    Args:
        df: DataFrame to validate
        dataset_name: Name of the dataset
    
    Returns:
        ValidationResult with validation status
    """
    model = get_model_for_dataset(dataset_name)
    if model is None:
        return ValidationResult(
            is_valid=False,
            error_message=f"No validation model found for dataset: {dataset_name}",
            total_rows=len(df) if df is not None else 0,
            validated_rows=0
        )
    
    return validate_dataframe(df, model)


def safe_validate_data(df: pd.DataFrame, dataset_name: str, show_warnings: bool = True) -> ValidationResult:
    """
    Safely validate data with user-friendly output
    
    Args:
        df: DataFrame to validate
        dataset_name: Name of the dataset
        show_warnings: Whether to display warnings in UI
    
    Returns:
        ValidationResult object with validation status and errors
    """
    try:
        result = validate_dataset(df, dataset_name)
        
        if result.is_valid:
            logger.info(f"✅ {dataset_name} validation passed ({result.validated_rows}/{result.total_rows} rows)")
        else:
            logger.error(f"❌ {dataset_name} validation failed: {result.error_message}")
            if show_warnings:
                import streamlit as st
                st.error(f"Data validation failed for {dataset_name}: {result.error_message}")
        return result
        
    except Exception as e:
        logger.error(f"Validation error for {dataset_name}: {e}")
        return ValidationResult(
            is_valid=False,
            error_message=str(e),
            warning_messages=[],
            validated_rows=0,
            total_rows=0
        )