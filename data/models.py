"""
Data models and validation for AI Adoption Dashboard
Uses Pydantic for robust data validation and type safety
"""

from typing import Dict, List, Optional, Union, Literal
from datetime import datetime
import pandas as pd
import logging

# Handle Pydantic version compatibility
try:
    from pydantic import BaseModel, Field, validator
    from pydantic import ConfigDict
    PYDANTIC_V2 = True
except ImportError:
    try:
        from pydantic import BaseModel, Field, validator
        PYDANTIC_V2 = False
        ConfigDict = None
    except ImportError:
        # Fallback: create mock classes if Pydantic not available
        class BaseModel:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
        
        def Field(*args, **kwargs):
            return None
            
        def validator(*args, **kwargs):
            def decorator(func):
                return func
            return decorator
            
        PYDANTIC_V2 = False
        ConfigDict = None

logger = logging.getLogger(__name__)


class HistoricalDataPoint(BaseModel):
    """Model for historical AI adoption data points"""
    if PYDANTIC_V2 and ConfigDict:
        model_config = ConfigDict(str_strip_whitespace=True)
    
    year: int = Field(..., ge=2017, le=2025, description="Year of the data point")
    ai_use: float = Field(..., ge=0, le=100, description="Overall AI adoption percentage")
    genai_use: float = Field(..., ge=0, le=100, description="Generative AI adoption percentage")
    
    @validator('genai_use')
    def genai_cannot_exceed_ai(cls, v, values):
        """GenAI adoption cannot exceed overall AI adoption"""
        if 'ai_use' in values and v > values['ai_use']:
            raise ValueError(f'GenAI adoption ({v}%) cannot exceed overall AI adoption ({values["ai_use"]}%)')
        return v
    
    @validator('year')
    def year_must_be_reasonable(cls, v):
        """Ensure year is within reasonable bounds"""
        if v < 2010 or v > 2030:
            raise ValueError(f'Year {v} is outside reasonable bounds (2010-2030)')
        return v


class SectorData(BaseModel):
    """Model for sector-specific AI adoption data"""
    if PYDANTIC_V2 and ConfigDict:
        model_config = ConfigDict(str_strip_whitespace=True)
    
    sector: str = Field(..., min_length=2, max_length=50, description="Industry sector name")
    adoption_rate: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    genai_adoption: Optional[float] = Field(None, ge=0, le=100, description="GenAI adoption rate percentage")
    avg_roi: float = Field(..., gt=0, le=10, description="Average ROI multiplier")
    
    @validator('sector')
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
    
    @validator('genai_adoption')
    def genai_cannot_exceed_overall(cls, v, values):
        """GenAI adoption cannot exceed overall adoption"""
        if v is not None and 'adoption_rate' in values and v > values['adoption_rate']:
            raise ValueError(f'GenAI adoption ({v}%) cannot exceed overall adoption ({values["adoption_rate"]}%)')
        return v
    
    @validator('avg_roi')
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
    
    @validator('size')
    def validate_size_format(cls, v):
        """Validate size format contains numbers or follows expected patterns"""
        import re
        # Allow patterns like "1-4", "5000+", "Small (1-50)"
        if not re.search(r'\d', v):
            raise ValueError(f'Size "{v}" must contain numeric information')
        return v
    
    @validator('adoption')
    def adoption_correlation_check(cls, v, values):
        """Larger firms typically have higher adoption rates"""
        size_str = values.get('size', '')
        
        # Extract rough size for correlation check
        if '5000+' in size_str or '2500-4999' in size_str:
            if v < 20:
                logger.warning(f'Large firm adoption rate {v}% seems low')
        elif '1-4' in size_str or '5-9' in size_str:
            if v > 50:
                logger.warning(f'Small firm adoption rate {v}% seems high')
        
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
    
    @validator('genai_investment')
    def genai_cannot_exceed_total(cls, v, values):
        """GenAI investment cannot exceed total investment"""
        if v is not None and 'total_investment' in values:
            if v > values['total_investment']:
                raise ValueError(f'GenAI investment ({v}B) cannot exceed total investment ({values["total_investment"]}B)')
        return v
    
    @validator('us_investment', 'china_investment', 'uk_investment')
    def regional_cannot_exceed_total(cls, v, values):
        """Regional investment cannot exceed total investment"""
        if v is not None and 'total_investment' in values:
            if v > values['total_investment']:
                raise ValueError(f'Regional investment ({v}B) cannot exceed total investment ({values["total_investment"]}B)')
        return v
    
    @validator('total_investment')
    def investment_growth_check(cls, v, values):
        """Investment should generally increase over time"""
        year = values.get('year')
        if year and year >= 2020 and v < 50:
            logger.warning(f'Investment {v}B seems low for year {year}')
        return v


class FinancialImpactData(BaseModel):
    """Model for financial impact by business function"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    function: str = Field(..., min_length=2, max_length=50, description="Business function name")
    companies_reporting_cost_savings: float = Field(..., ge=0, le=100, description="% of companies reporting cost savings")
    companies_reporting_revenue_gains: float = Field(..., ge=0, le=100, description="% of companies reporting revenue gains")
    avg_cost_reduction: Optional[float] = Field(None, ge=0, le=100, description="Average cost reduction percentage")
    avg_revenue_increase: Optional[float] = Field(None, ge=0, le=200, description="Average revenue increase percentage")
    
    @validator('function')
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
    
    @validator('avg_cost_reduction')
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
    
    @validator('state_code')
    def state_code_format(cls, v):
        """State code should be uppercase"""
        return v.upper()
    
    @validator('rate')
    def rate_correlation_check(cls, v, values):
        """Large cities typically have higher adoption rates"""
        city = values.get('city', '')
        if any(large_city in city for large_city in ['San Francisco', 'New York', 'Seattle', 'Boston']):
            if v < 5:
                logger.warning(f'Adoption rate {v}% seems low for major tech city {city}')
        return v


class TokenEconomicsData(BaseModel):
    """Model for token economics data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., min_length=3, max_length=50, description="AI model name")
    cost_per_million_input: float = Field(..., ge=0, description="Cost per million input tokens in USD")
    cost_per_million_output: float = Field(..., ge=0, description="Cost per million output tokens in USD")
    context_window: Optional[int] = Field(None, gt=0, description="Context window size in tokens")
    tokens_per_second: Optional[float] = Field(None, gt=0, description="Processing speed in tokens per second")
    
    @validator('cost_per_million_input', 'cost_per_million_output')
    def cost_reasonable(cls, v):
        """Token costs should be reasonable"""
        if v > 100:
            logger.warning(f'Token cost ${v} per million seems very high')
        if v < 0.001:
            logger.warning(f'Token cost ${v} per million seems very low')
        return v
    
    @validator('context_window')
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
    
    @validator('technology')
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
    
    @validator('risk_score')
    def risk_score_correlation(cls, v, values):
        """Risk score should correlate with maturity stage"""
        maturity = values.get('maturity')
        if maturity == 'Innovation Trigger' and v < 70:
            logger.warning(f'Innovation Trigger technology should have high risk score')
        elif maturity == 'Plateau of Productivity' and v > 30:
            logger.warning(f'Plateau technology should have low risk score')
        return v


class ProductivityData(BaseModel):
    """Model for productivity research data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    function: str = Field(..., min_length=2, max_length=50, description="Business function")
    productivity_gain: float = Field(..., ge=0, le=1000, description="Productivity gain percentage")
    confidence_level: Optional[str] = Field(None, description="Confidence level (High/Medium/Low)")
    
    @validator('productivity_gain')
    def productivity_gain_reasonable(cls, v):
        """Productivity gains should be reasonable"""
        if v > 500:
            logger.warning(f'Productivity gain {v}% is very high - please verify')
        return v


class ProductivityBySkillData(BaseModel):
    """Model for productivity by skill level"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill_level: str = Field(..., description="Skill level category")
    productivity_gain: float = Field(..., ge=0, le=1000, description="Productivity gain percentage")
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    
    @validator('skill_level')
    def skill_level_valid(cls, v):
        """Validate skill level categories"""
        valid_levels = {'Low', 'Medium', 'High', 'Expert', 'Beginner', 'Advanced'}
        if v not in valid_levels:
            logger.warning(f'Skill level "{v}" not in standard categories')
        return v


class AIProductivityEstimatesData(BaseModel):
    """Model for AI productivity estimates"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    estimate_type: str = Field(..., description="Type of productivity estimate")
    value: float = Field(..., ge=0, description="Productivity value")
    
    @validator('estimate_type')
    def estimate_type_valid(cls, v):
        """Validate estimate types"""
        valid_types = {'Conservative', 'Moderate', 'Optimistic', 'Aggressive'}
        if v not in valid_types:
            logger.warning(f'Estimate type "{v}" not in standard categories')
        return v


class OECDG7AdoptionData(BaseModel):
    """Model for OECD G7 adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    country: str = Field(..., description="G7 country name")
    adoption_rate: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    genai_adoption: Optional[float] = Field(None, ge=0, le=100, description="GenAI adoption rate")
    digital_readiness: Optional[float] = Field(None, ge=0, le=100, description="Digital readiness score")
    
    @validator('country')
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
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    impact_score: Optional[float] = Field(None, ge=0, le=10, description="Impact score (0-10)")
    
    @validator('application')
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
    percentage: float = Field(..., ge=0, le=100, description="Percentage of companies reporting barrier")
    
    @validator('barrier')
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
    effectiveness_score: float = Field(..., ge=0, le=10, description="Effectiveness score (0-10)")
    
    @validator('support_type')
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
    growth_rate: float = Field(..., ge=-100, le=1000, description="Growth rate percentage")
    adoption_rate: float = Field(..., ge=0, le=100, description="Current adoption rate")
    investment_level: Optional[str] = Field(None, description="Investment level category")
    
    @validator('region')
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
    
    @validator('cost_per_million_tokens')
    def cost_reasonable(cls, v):
        """Cost should be reasonable"""
        if v > 100:
            logger.warning(f'Cost {v} per million tokens seems high')
        return v


class AIPerceptionData(BaseModel):
    """Model for AI perception data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    perception: str = Field(..., description="Perception category")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of respondents")
    sentiment: Optional[str] = Field(None, description="Sentiment (Positive/Negative/Neutral)")
    
    @validator('perception')
    def perception_valid(cls, v):
        """Validate perception categories"""
        valid_perceptions = {
            'Job Enhancement', 'Job Replacement', 'Productivity Boost',
            'Quality Improvement', 'Cost Reduction', 'Innovation Driver'
        }
        if v not in valid_perceptions:
            logger.warning(f'Perception "{v}" not in standard list')
        return v


class TrainingEmissionsData(BaseModel):
    """Model for AI training emissions data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., description="AI model name")
    emissions_kg_co2: float = Field(..., ge=0, description="Emissions in kg CO2")
    
    @validator('emissions_kg_co2')
    def emissions_reasonable(cls, v):
        """Emissions should be reasonable"""
        if v > 1000000:  # 1 million kg CO2
            logger.warning(f'Emissions {v} kg CO2 seems very high')
        return v


class SkillGapData(BaseModel):
    """Model for skill gap analysis data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill: str = Field(..., description="Skill name")
    demand_percentage: float = Field(..., ge=0, le=100, description="Demand percentage")
    supply_percentage: float = Field(..., ge=0, le=100, description="Supply percentage")
    
    @validator('skill')
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
    
    @validator('supply_percentage')
    def supply_cannot_exceed_demand(cls, v, values):
        """Supply should not exceed demand by too much"""
        demand = values.get('demand_percentage')
        if demand is not None and v > demand * 1.5:
            logger.warning(f'Supply {v}% significantly exceeds demand {demand}%')
        return v


class AIGovernanceData(BaseModel):
    """Model for AI governance data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    governance_area: str = Field(..., description="Governance area")
    implementation_rate: float = Field(..., ge=0, le=100, description="Implementation rate percentage")
    maturity_level: Optional[str] = Field(None, description="Maturity level")
    
    @validator('governance_area')
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
    
    sector: str = Field(..., description="Industry sector")
    genai_adoption: float = Field(..., ge=0, le=100, description="GenAI adoption rate percentage")
    
    @validator('sector')
    def sector_must_be_valid(cls, v):
        """Validate sector names"""
        allowed_sectors = {
            'Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
            'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'
        }
        if v not in allowed_sectors:
            logger.warning(f'Sector "{v}" not in predefined list')
        return v


class TokenUsagePatternsData(BaseModel):
    """Model for token usage patterns"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    pattern_type: str = Field(..., description="Usage pattern type")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of usage")
    efficiency_score: Optional[float] = Field(None, ge=0, le=10, description="Efficiency score")
    
    @validator('pattern_type')
    def pattern_type_valid(cls, v):
        """Validate pattern types"""
        valid_patterns = {
            'Conversational', 'Document Processing', 'Code Generation',
            'Creative Writing', 'Analysis', 'Translation'
        }
        if v not in valid_patterns:
            logger.warning(f'Pattern type "{v}" not in standard list')
        return v


class TokenOptimizationData(BaseModel):
    """Model for token optimization data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    optimization_technique: str = Field(..., description="Optimization technique")
    efficiency_gain: float = Field(..., ge=0, le=100, description="Efficiency gain percentage")
    complexity_score: Optional[float] = Field(None, ge=0, le=10, description="Complexity score")
    
    @validator('optimization_technique')
    def technique_valid(cls, v):
        """Validate optimization techniques"""
        valid_techniques = {
            'Prompt Engineering', 'Context Window Optimization', 'Model Selection',
            'Batch Processing', 'Caching', 'Compression'
        }
        if v not in valid_techniques:
            logger.warning(f'Technique "{v}" not in standard list')
        return v


class TokenPricingEvolutionData(BaseModel):
    """Model for token pricing evolution"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: str = Field(..., description="Date of pricing")
    avg_price_input: float = Field(..., ge=0, description="Average input token price")
    avg_price_output: float = Field(..., ge=0, description="Average output token price")
    model_count: Optional[int] = Field(None, gt=0, description="Number of models in sample")
    
    @validator('date')
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
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    population_millions: Optional[float] = Field(None, gt=0, description="Population in millions")
    
    @validator('state')
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
    
    @validator('technology')
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
    
    @validator('validated_rows')
    def validated_cannot_exceed_total(cls, v, values):
        """Validated rows cannot exceed total rows"""
        total = values.get('total_rows')
        if total is not None and v > total:
            logger.warning(f'Validated rows ({v}) exceeded total rows ({total}), capping to {total}')
            return total
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


class ProductivityData(BaseModel):
    """Model for productivity research data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    function: str = Field(..., min_length=2, max_length=50, description="Business function")
    productivity_gain: float = Field(..., ge=0, le=1000, description="Productivity gain percentage")
    confidence_level: Optional[str] = Field(None, description="Confidence level (High/Medium/Low)")
    
    @validator('productivity_gain')
    def productivity_gain_reasonable(cls, v):
        """Productivity gains should be reasonable"""
        if v > 500:
            logger.warning(f'Productivity gain {v}% is very high - please verify')
        return v


class ProductivityBySkillData(BaseModel):
    """Model for productivity by skill level"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill_level: str = Field(..., description="Skill level category")
    productivity_gain: float = Field(..., ge=0, le=1000, description="Productivity gain percentage")
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    
    @validator('skill_level')
    def skill_level_valid(cls, v):
        """Validate skill level categories"""
        valid_levels = {'Low', 'Medium', 'High', 'Expert', 'Beginner', 'Advanced'}
        if v not in valid_levels:
            logger.warning(f'Skill level "{v}" not in standard categories')
        return v


class AIProductivityEstimatesData(BaseModel):
    """Model for AI productivity estimates"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    estimate_type: str = Field(..., description="Type of productivity estimate")
    value: float = Field(..., ge=0, description="Productivity value")
    
    @validator('estimate_type')
    def estimate_type_valid(cls, v):
        """Validate estimate types"""
        valid_types = {'Conservative', 'Moderate', 'Optimistic', 'Aggressive'}
        if v not in valid_types:
            logger.warning(f'Estimate type "{v}" not in standard categories')
        return v


class OECDG7AdoptionData(BaseModel):
    """Model for OECD G7 adoption data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    country: str = Field(..., description="G7 country name")
    adoption_rate: float = Field(..., ge=0, le=100, description="AI adoption rate percentage")
    genai_adoption: Optional[float] = Field(None, ge=0, le=100, description="GenAI adoption rate")
    digital_readiness: Optional[float] = Field(None, ge=0, le=100, description="Digital readiness score")
    
    @validator('country')
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
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    impact_score: Optional[float] = Field(None, ge=0, le=10, description="Impact score (0-10)")
    
    @validator('application')
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
    percentage: float = Field(..., ge=0, le=100, description="Percentage of companies reporting barrier")
    
    @validator('barrier')
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
    effectiveness_score: float = Field(..., ge=0, le=10, description="Effectiveness score (0-10)")
    
    @validator('support_type')
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
    growth_rate: float = Field(..., ge=-100, le=1000, description="Growth rate percentage")
    adoption_rate: float = Field(..., ge=0, le=100, description="Current adoption rate")
    investment_level: Optional[str] = Field(None, description="Investment level category")
    
    @validator('region')
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
    
    @validator('cost_per_million_tokens')
    def cost_reasonable(cls, v):
        """Cost should be reasonable"""
        if v > 100:
            logger.warning(f'Cost {v} per million tokens seems high')
        return v


class AIPerceptionData(BaseModel):
    """Model for AI perception data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    perception: str = Field(..., description="Perception category")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of respondents")
    sentiment: Optional[str] = Field(None, description="Sentiment (Positive/Negative/Neutral)")
    
    @validator('perception')
    def perception_valid(cls, v):
        """Validate perception categories"""
        valid_perceptions = {
            'Job Enhancement', 'Job Replacement', 'Productivity Boost',
            'Quality Improvement', 'Cost Reduction', 'Innovation Driver'
        }
        if v not in valid_perceptions:
            logger.warning(f'Perception "{v}" not in standard list')
        return v


class TrainingEmissionsData(BaseModel):
    """Model for AI training emissions data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    model: str = Field(..., description="AI model name")
    emissions_kg_co2: float = Field(..., ge=0, description="Emissions in kg CO2")
    
    @validator('emissions_kg_co2')
    def emissions_reasonable(cls, v):
        """Emissions should be reasonable"""
        if v > 1000000:  # 1 million kg CO2
            logger.warning(f'Emissions {v} kg CO2 seems very high')
        return v


class SkillGapData(BaseModel):
    """Model for skill gap analysis data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    skill: str = Field(..., description="Skill name")
    demand_percentage: float = Field(..., ge=0, le=100, description="Demand percentage")
    supply_percentage: float = Field(..., ge=0, le=100, description="Supply percentage")
    
    @validator('skill')
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
    
    @validator('supply_percentage')
    def supply_cannot_exceed_demand(cls, v, values):
        """Supply should not exceed demand by too much"""
        demand = values.get('demand_percentage')
        if demand is not None and v > demand * 1.5:
            logger.warning(f'Supply {v}% significantly exceeds demand {demand}%')
        return v


class AIGovernanceData(BaseModel):
    """Model for AI governance data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    governance_area: str = Field(..., description="Governance area")
    implementation_rate: float = Field(..., ge=0, le=100, description="Implementation rate percentage")
    maturity_level: Optional[str] = Field(None, description="Maturity level")
    
    @validator('governance_area')
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
    
    sector: str = Field(..., description="Industry sector")
    genai_adoption: float = Field(..., ge=0, le=100, description="GenAI adoption rate percentage")
    
    @validator('sector')
    def sector_must_be_valid(cls, v):
        """Validate sector names"""
        allowed_sectors = {
            'Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
            'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'
        }
        if v not in allowed_sectors:
            logger.warning(f'Sector "{v}" not in predefined list')
        return v


class TokenUsagePatternsData(BaseModel):
    """Model for token usage patterns"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    pattern_type: str = Field(..., description="Usage pattern type")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of usage")
    efficiency_score: Optional[float] = Field(None, ge=0, le=10, description="Efficiency score")
    
    @validator('pattern_type')
    def pattern_type_valid(cls, v):
        """Validate pattern types"""
        valid_patterns = {
            'Conversational', 'Document Processing', 'Code Generation',
            'Creative Writing', 'Analysis', 'Translation'
        }
        if v not in valid_patterns:
            logger.warning(f'Pattern type "{v}" not in standard list')
        return v


class TokenOptimizationData(BaseModel):
    """Model for token optimization data"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    optimization_technique: str = Field(..., description="Optimization technique")
    efficiency_gain: float = Field(..., ge=0, le=100, description="Efficiency gain percentage")
    complexity_score: Optional[float] = Field(None, ge=0, le=10, description="Complexity score")
    
    @validator('optimization_technique')
    def technique_valid(cls, v):
        """Validate optimization techniques"""
        valid_techniques = {
            'Prompt Engineering', 'Context Window Optimization', 'Model Selection',
            'Batch Processing', 'Caching', 'Compression'
        }
        if v not in valid_techniques:
            logger.warning(f'Technique "{v}" not in standard list')
        return v


class TokenPricingEvolutionData(BaseModel):
    """Model for token pricing evolution"""
    model_config = ConfigDict(str_strip_whitespace=True)
    
    date: str = Field(..., description="Date of pricing")
    avg_price_input: float = Field(..., ge=0, description="Average input token price")
    avg_price_output: float = Field(..., ge=0, description="Average output token price")
    model_count: Optional[int] = Field(None, gt=0, description="Number of models in sample")
    
    @validator('date')
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
    adoption_rate: float = Field(..., ge=0, le=100, description="Adoption rate percentage")
    population_millions: Optional[float] = Field(None, gt=0, description="Population in millions")
    
    @validator('state')
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
    
    @validator('technology')
    def technology_valid(cls, v):
        """Validate technology names"""
        valid_technologies = {
            'Cloud-based AI', 'On-premise AI', 'Hybrid AI', 'Edge AI',
            'Multi-technology', 'Single Platform', 'Custom Solutions'
        }
        if v not in valid_technologies:
            logger.warning(f'Technology "{v}" not in standard list')
        return v


# Model registry for easy access - UPDATED with all datasets
MODEL_REGISTRY: Dict[str, BaseModel] = {
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
    model: BaseModel, 
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
        warning_messages=warnings,
        validated_rows=len(df),
        total_rows=len(df)
    )


def get_model_for_dataset(dataset_name: str) -> Optional[BaseModel]:
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


def safe_validate_data(df: pd.DataFrame, dataset_name: str, show_warnings: bool = True) -> bool:
    """
    Safely validate data with user-friendly output
    
    Args:
        df: DataFrame to validate
        dataset_name: Name of the dataset
        show_warnings: Whether to display warnings in UI
    
    Returns:
        True if validation passes, False otherwise
    """
    try:
        result = validate_dataset(df, dataset_name)
        
        if result.is_valid:
            logger.info(f"✅ {dataset_name} validation passed ({result.validated_rows}/{result.total_rows} rows)")
            return True
        else:
            logger.error(f"❌ {dataset_name} validation failed: {result.error_message}")
            if show_warnings:
                import streamlit as st
                st.error(f"Data validation failed for {dataset_name}: {result.error_message}")
            return False
            
    except Exception as e:
        logger.error(f"Validation error for {dataset_name}: {e}")
        return False