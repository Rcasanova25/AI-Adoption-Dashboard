"""Enhanced financial calculations with caching support.

This module wraps the core financial calculations with caching
to improve performance for repeated calculations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from utils.cache_manager import cache_financial_calculation, calculation_cache
from .financial_calculations import (
    calculate_npv as _calculate_npv,
    calculate_irr as _calculate_irr,
    calculate_tco as _calculate_tco,
    calculate_payback_period as _calculate_payback_period,
    calculate_risk_adjusted_return as _calculate_risk_adjusted_return,
    calculate_ai_productivity_roi as _calculate_ai_productivity_roi,
    calculate_break_even_analysis as _calculate_break_even_analysis
)


@cache_financial_calculation
def calculate_npv(
    cash_flows: List[float], 
    discount_rate: float, 
    initial_investment: float
) -> float:
    """Calculate Net Present Value with caching.
    
    This is a cached version of the NPV calculation that stores results
    for repeated calculations with the same parameters.
    
    Args:
        cash_flows: List of annual cash flows
        discount_rate: Annual discount rate
        initial_investment: Initial investment amount
        
    Returns:
        Net Present Value
    """
    # Check manual cache first for even faster access
    cached_result = calculation_cache.get_npv(
        cash_flows, discount_rate, initial_investment
    )
    if cached_result is not None:
        return cached_result
        
    # Calculate NPV
    result = _calculate_npv(cash_flows, discount_rate, initial_investment)
    
    # Store in specialized cache
    calculation_cache.cache_npv(
        cash_flows, discount_rate, initial_investment, result
    )
    
    return result


@cache_financial_calculation
def calculate_irr(
    cash_flows: List[float], 
    initial_investment: float,
    max_iterations: int = 1000
) -> Optional[float]:
    """Calculate Internal Rate of Return with caching.
    
    Cached version of IRR calculation for improved performance.
    
    Args:
        cash_flows: List of annual cash flows
        initial_investment: Initial investment amount
        max_iterations: Maximum iterations for solver
        
    Returns:
        Internal Rate of Return or None if not found
    """
    return _calculate_irr(cash_flows, initial_investment, max_iterations)


@cache_financial_calculation
def calculate_tco(
    initial_investment: float,
    annual_operating_costs: List[float],
    maintenance_rate: float = 0.15,
    discount_rate: float = 0.10
) -> dict:
    """Calculate Total Cost of Ownership with caching.
    
    Cached version of TCO calculation.
    
    Args:
        initial_investment: Initial investment amount
        annual_operating_costs: List of annual operating costs
        maintenance_rate: Annual maintenance as % of initial investment
        discount_rate: Discount rate for NPV calculation
        
    Returns:
        Dictionary with TCO breakdown
    """
    return _calculate_tco(
        initial_investment, annual_operating_costs, 
        maintenance_rate, discount_rate
    )


@cache_financial_calculation
def calculate_payback_period(
    cash_flows: List[float],
    initial_investment: float,
    discount_rate: Optional[float] = None
) -> Optional[float]:
    """Calculate payback period with caching.
    
    Cached version of payback period calculation.
    
    Args:
        cash_flows: List of annual cash flows
        initial_investment: Initial investment amount
        discount_rate: Optional discount rate for discounted payback
        
    Returns:
        Payback period in years or None if never
    """
    return _calculate_payback_period(
        cash_flows, initial_investment, discount_rate
    )


@cache_financial_calculation
def calculate_risk_adjusted_return(
    expected_return: float,
    risk_level: str = "Medium"
) -> dict:
    """Calculate risk-adjusted return metrics with caching.
    
    Cached version of risk-adjusted return calculation.
    
    Args:
        expected_return: Expected annual return rate
        risk_level: Risk level (Low, Medium, High, Very High)
        
    Returns:
        Dictionary with risk metrics
    """
    return _calculate_risk_adjusted_return(expected_return, risk_level)


@cache_financial_calculation
def calculate_ai_productivity_roi(
    num_employees: int,
    avg_salary: float,
    productivity_gain_pct: float,
    implementation_cost: float,
    annual_ai_cost: float,
    years: int = 5,
    discount_rate: float = 0.10
) -> dict:
    """Calculate ROI from AI-driven productivity gains with caching.
    
    Cached version of AI productivity ROI calculation.
    
    Args:
        num_employees: Number of employees affected
        avg_salary: Average annual salary
        productivity_gain_pct: Expected productivity gain (0-1)
        implementation_cost: One-time implementation cost
        annual_ai_cost: Annual AI system cost
        years: Analysis period
        discount_rate: Discount rate for NPV
        
    Returns:
        Dictionary with productivity ROI metrics
    """
    return _calculate_ai_productivity_roi(
        num_employees, avg_salary, productivity_gain_pct,
        implementation_cost, annual_ai_cost, years, discount_rate
    )


@cache_financial_calculation
def calculate_break_even_analysis(
    fixed_costs: float,
    variable_cost_per_unit: Optional[float] = None,
    price_per_unit: Optional[float] = None,
    variable_cost_ratio: Optional[float] = None,
    ai_fixed_cost_reduction: float = 0.20,
    ai_variable_cost_reduction: float = 0.15
) -> dict:
    """Calculate break-even analysis with AI impact with caching.
    
    Cached version of break-even analysis.
    
    Args:
        fixed_costs: Annual fixed costs
        variable_cost_per_unit: Variable cost per unit (for unit-based)
        price_per_unit: Price per unit (for unit-based)
        variable_cost_ratio: Variable cost as % of revenue (for revenue-based)
        ai_fixed_cost_reduction: Expected reduction in fixed costs
        ai_variable_cost_reduction: Expected reduction in variable costs
        
    Returns:
        Dictionary with break-even analysis
    """
    return _calculate_break_even_analysis(
        fixed_costs, variable_cost_per_unit, price_per_unit,
        variable_cost_ratio, ai_fixed_cost_reduction, ai_variable_cost_reduction
    )


# Cache management functions
def get_cache_statistics():
    """Get cache performance statistics.
    
    Returns:
        Dictionary with cache statistics for all calculation types
    """
    return calculation_cache.get_all_stats()


def clear_calculation_cache():
    """Clear all calculation caches.
    
    Use this when underlying data changes or to free memory.
    """
    calculation_cache.clear_all()
    
    # Also clear decorator caches
    calculate_npv.clear_cache()
    calculate_irr.clear_cache()
    calculate_tco.clear_cache()
    calculate_payback_period.clear_cache()
    calculate_risk_adjusted_return.clear_cache()
    calculate_ai_productivity_roi.clear_cache()
    calculate_break_even_analysis.clear_cache()


# Export the same interface as the original module
__all__ = [
    'calculate_npv',
    'calculate_irr',
    'calculate_tco',
    'calculate_payback_period',
    'calculate_risk_adjusted_return',
    'calculate_ai_productivity_roi',
    'calculate_break_even_analysis',
    'get_cache_statistics',
    'clear_calculation_cache'
]