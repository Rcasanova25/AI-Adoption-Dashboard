"""
Views module for AI Adoption Dashboard
Each view is modularized into its own function for better maintainability
"""

from .historical_trends import show_historical_trends
from .industry_analysis import show_industry_analysis
from .financial_impact import show_financial_impact
from .investment_trends import show_investment_trends
from .regional_growth import show_regional_growth
from .ai_cost_trends import show_ai_cost_trends
from .token_economics import show_token_economics
from .labor_impact import show_labor_impact
from .environmental_impact import show_environmental_impact
from .adoption_rates import show_adoption_rates
from .skill_gap_analysis import show_skill_gap_analysis
from .ai_governance import show_ai_governance
from .productivity_research import show_productivity_research
from .firm_size_analysis import show_firm_size_analysis
from .technology_stack import show_technology_stack
from .ai_maturity import show_ai_technology_maturity
from .geographic_distribution import show_geographic_distribution
from .oecd_findings import show_oecd_2025_findings
from .barriers_support import show_barriers_support
from .roi_analysis import show_roi_analysis
from .causal_analysis import show_causal_analysis
from .bibliography import show_bibliography_sources

__all__ = [
    'show_historical_trends',
    'show_industry_analysis', 
    'show_financial_impact',
    'show_investment_trends',
    'show_regional_growth',
    'show_ai_cost_trends',
    'show_token_economics',
    'show_labor_impact',
    'show_environmental_impact',
    'show_adoption_rates',
    'show_skill_gap_analysis',
    'show_ai_governance',
    'show_productivity_research',
    'show_firm_size_analysis',
    'show_technology_stack',
    'show_ai_technology_maturity',
    'show_geographic_distribution',
    'show_oecd_2025_findings',
    'show_barriers_support',
    'show_roi_analysis',
    'show_causal_analysis',
    'show_bibliography_sources'
]