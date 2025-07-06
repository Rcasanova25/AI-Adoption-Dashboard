"""Business logic modules for AI Adoption Dashboard.

This package contains business logic for economic analysis,
financial calculations, and industry-specific models.
"""

from .economic_scenarios import *
from .financial_calculations import *
from .financial_calculations_cached import *
from .industry_models import *
from .labor_impact import *
from .policy_simulation import *
from .roi_analysis import *
from .scenario_engine import *
from .scenario_engine_parallel import *

__all__ = [
    # Economic scenarios
    'calculate_gdp_impact',
    'generate_growth_scenarios',
    
    # Financial calculations
    'calculate_npv',
    'calculate_irr',
    'calculate_tco',
    'calculate_payback_period',
    'calculate_risk_adjusted_return',
    'calculate_ai_productivity_roi',
    'calculate_break_even_analysis',
    
    # Industry models
    'calculate_manufacturing_roi',
    'calculate_healthcare_roi',
    'calculate_financial_services_roi',
    'calculate_retail_roi',
    'get_industry_benchmarks',
    'select_optimal_ai_strategy',
    'INDUSTRY_PROFILES',
    
    # Labor impact
    'calculate_workforce_transformation',
    'project_job_displacement',
    
    # Policy simulation
    'PolicyScenario',
    'simulate_policy_impact',
    
    # ROI analysis
    'compute_roi',
    'compute_comprehensive_roi',
    'analyze_roi_by_company_size',
    
    # Scenario engine
    'ScenarioVariable',
    'monte_carlo_simulation',
    'sensitivity_analysis',
    'adoption_s_curve',
    'technology_correlation_matrix',
    'scenario_comparison',
    'create_scenario_tornado_chart',
]