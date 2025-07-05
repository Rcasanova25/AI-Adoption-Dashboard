"""Views module for AI Adoption Dashboard.

This module contains all the individual view components extracted from the main app.py file.
Each view is a self-contained module with its own render function.
"""

from .adoption_rates import render as render_adoption_rates
from .ai_cost_trends import render as render_ai_cost_trends
from .ai_governance import render as render_ai_governance
from .ai_technology_maturity import render as render_ai_technology_maturity
from .barriers_support import render as render_barriers_support

# Import base view components
from .base import BaseView, ViewMetadata, ViewRegistry
from .bibliography_sources import render as render_bibliography_sources

# Import all view modules
from .competitive_assessment import render as render_competitive_assessment
from .environmental_impact import render as render_environmental_impact
from .financial_impact import render as render_financial_impact
from .firm_size_analysis import render as render_firm_size_analysis
from .geographic_distribution import render as render_geographic_distribution
from .historical_trends import render as render_historical_trends
from .industry_analysis import render as render_industry_analysis
from .investment_trends import render as render_investment_trends
from .labor_impact import render as render_labor_impact
from .oecd_2025_findings import render as render_oecd_2025_findings
from .productivity_research import render as render_productivity_research
from .regional_growth import render as render_regional_growth
from .roi_analysis import render as render_roi_analysis
from .skill_gap_analysis import render as render_skill_gap_analysis
from .technology_stack import render as render_technology_stack
from .token_economics import render as render_token_economics

# Create VIEW_REGISTRY mapping view names to render functions
VIEW_REGISTRY = {
    "Competitive Assessment": render_competitive_assessment,
    "Historical Trends": render_historical_trends,
    "Industry Analysis": render_industry_analysis,
    "Financial Impact": render_financial_impact,
    "Investment Trends": render_investment_trends,
    "Regional Growth": render_regional_growth,
    "AI Cost Trends": render_ai_cost_trends,
    "Token Economics": render_token_economics,
    "Labor Impact": render_labor_impact,
    "Environmental Impact": render_environmental_impact,
    "Adoption Rates": render_adoption_rates,
    "Productivity Research": render_productivity_research,
    "Skill Gap Analysis": render_skill_gap_analysis,
    "AI Governance": render_ai_governance,
    "Firm Size Analysis": render_firm_size_analysis,
    "Technology Stack": render_technology_stack,
    "AI Technology Maturity": render_ai_technology_maturity,
    "Geographic Distribution": render_geographic_distribution,
    "OECD 2025 Findings": render_oecd_2025_findings,
    "Barriers & Support": render_barriers_support,
    "ROI Analysis": render_roi_analysis,
    "Bibliography & Sources": render_bibliography_sources,
}

# Export the registry and base components for use in app.py
__all__ = ["VIEW_REGISTRY", "ViewRegistry", "BaseView", "ViewMetadata"]
