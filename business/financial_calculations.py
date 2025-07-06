"""Core financial calculations for AI investment analysis.

This module provides industry-standard financial calculations including
NPV, IRR, TCO, and risk-adjusted returns for AI adoption decisions.
"""

import logging
from typing import List, Optional, Tuple
import numpy as np
from scipy import optimize

logger = logging.getLogger(__name__)


def calculate_npv(
    cash_flows: List[float], 
    discount_rate: float, 
    initial_investment: float
) -> float:
    """Calculate Net Present Value of an investment.
    
    Args:
        cash_flows: List of annual cash flows (positive = inflows, negative = outflows)
        discount_rate: Annual discount rate (e.g., 0.10 for 10%)
        initial_investment: Initial investment amount (positive number)
        
    Returns:
        Net Present Value
        
    Example:
        >>> calculate_npv([100, 200, 300], 0.10, 500)
        -18.30  # Negative NPV indicates investment doesn't meet return threshold
    """
    npv = -initial_investment
    
    for i, cash_flow in enumerate(cash_flows):
        # Discount each cash flow to present value
        npv += cash_flow / ((1 + discount_rate) ** (i + 1))
    
    logger.debug(f"NPV calculation: initial={initial_investment}, rate={discount_rate}, NPV={npv:.2f}")
    return round(npv, 2)


def calculate_irr(
    cash_flows: List[float], 
    initial_investment: float,
    max_iterations: int = 1000
) -> Optional[float]:
    """Calculate Internal Rate of Return.
    
    Args:
        cash_flows: List of annual cash flows
        initial_investment: Initial investment amount (positive number)
        max_iterations: Maximum iterations for solver
        
    Returns:
        IRR as a decimal (e.g., 0.15 for 15%) or None if no solution
        
    Example:
        >>> calculate_irr([100, 200, 300], 500)
        0.1234  # 12.34% IRR
    """
    # Create cash flow series including initial investment
    all_cash_flows = [-initial_investment] + cash_flows
    
    try:
        # Use numpy's IRR function or scipy optimization
        # Define NPV function for root finding
        def npv_func(rate):
            return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(all_cash_flows))
        
        # Find rate where NPV = 0
        result = optimize.brentq(npv_func, -0.99, 10, maxiter=max_iterations)
        
        logger.debug(f"IRR calculation: initial={initial_investment}, IRR={result:.4f}")
        return round(result, 4)
        
    except (ValueError, RuntimeError) as e:
        logger.warning(f"IRR calculation failed: {e}")
        return None


def calculate_tco(
    initial_cost: float,
    annual_operating_costs: List[float],
    maintenance_rate: float = 0.15,
    discount_rate: float = 0.0
) -> dict:
    """Calculate Total Cost of Ownership.
    
    Args:
        initial_cost: Initial implementation cost
        annual_operating_costs: List of annual operating costs
        maintenance_rate: Annual maintenance as % of initial cost (default 15%)
        discount_rate: Discount rate for present value (default 0 = nominal)
        
    Returns:
        Dictionary with TCO breakdown
        
    Example:
        >>> calculate_tco(100000, [20000, 20000, 20000], 0.15, 0.05)
        {'initial_cost': 100000, 'operating_costs': 60000, ...}
    """
    years = len(annual_operating_costs)
    
    # Calculate maintenance costs
    maintenance_costs = [initial_cost * maintenance_rate for _ in range(years)]
    
    # Calculate present value of costs if discount rate provided
    if discount_rate > 0:
        pv_operating = sum(cost / ((1 + discount_rate) ** (i + 1)) 
                          for i, cost in enumerate(annual_operating_costs))
        pv_maintenance = sum(cost / ((1 + discount_rate) ** (i + 1)) 
                           for i, cost in enumerate(maintenance_costs))
    else:
        pv_operating = sum(annual_operating_costs)
        pv_maintenance = sum(maintenance_costs)
    
    total_tco = initial_cost + pv_operating + pv_maintenance
    
    return {
        'initial_cost': initial_cost,
        'operating_costs': pv_operating,
        'maintenance_costs': pv_maintenance,
        'total_tco': total_tco,
        'annual_tco': total_tco / years,
        'years': years
    }


def calculate_payback_period(
    initial_investment: float,
    annual_cash_flows: List[float],
    consider_time_value: bool = False,
    discount_rate: float = 0.0
) -> Optional[float]:
    """Calculate payback period with optional discounting.
    
    Args:
        initial_investment: Initial investment amount
        annual_cash_flows: List of annual net cash flows
        consider_time_value: Whether to use discounted payback
        discount_rate: Discount rate if considering time value
        
    Returns:
        Payback period in years (fractional) or None if never paid back
    """
    cumulative_cash_flow = 0
    remaining_investment = initial_investment
    
    for year, cash_flow in enumerate(annual_cash_flows):
        # Apply discount if requested
        if consider_time_value and discount_rate > 0:
            discounted_cf = cash_flow / ((1 + discount_rate) ** (year + 1))
        else:
            discounted_cf = cash_flow
            
        cumulative_cash_flow += discounted_cf
        
        if cumulative_cash_flow >= initial_investment:
            # Calculate fractional year
            prev_cumulative = cumulative_cash_flow - discounted_cf
            fraction = (initial_investment - prev_cumulative) / discounted_cf
            return year + fraction
    
    return None  # Investment never paid back


def calculate_risk_adjusted_return(
    expected_return: float,
    risk_level: str,
    risk_free_rate: float = 0.03,
    risk_premiums: Optional[dict] = None
) -> dict:
    """Calculate risk-adjusted returns using CAPM-like approach.
    
    Args:
        expected_return: Expected annual return (as decimal)
        risk_level: 'Low', 'Medium', 'High', or 'Very High'
        risk_free_rate: Risk-free rate (default 3%)
        risk_premiums: Optional custom risk premiums by level
        
    Returns:
        Dictionary with risk-adjusted metrics
    """
    # Default risk premiums for AI investments
    default_premiums = {
        'Low': 0.05,      # 5% risk premium
        'Medium': 0.10,   # 10% risk premium
        'High': 0.20,     # 20% risk premium
        'Very High': 0.35 # 35% risk premium
    }
    
    premiums = risk_premiums or default_premiums
    risk_premium = premiums.get(risk_level, 0.10)
    
    # Required return = risk-free rate + risk premium
    required_return = risk_free_rate + risk_premium
    
    # Sharpe ratio calculation (simplified)
    excess_return = expected_return - risk_free_rate
    sharpe_ratio = excess_return / risk_premium if risk_premium > 0 else 0
    
    # Risk-adjusted return (using simplified approach)
    risk_adjusted_return = expected_return - (risk_premium * 0.5)  # Haircut for risk
    
    return {
        'expected_return': expected_return,
        'required_return': required_return,
        'risk_premium': risk_premium,
        'risk_adjusted_return': risk_adjusted_return,
        'sharpe_ratio': round(sharpe_ratio, 2),
        'meets_threshold': expected_return >= required_return
    }


def calculate_ai_productivity_roi(
    num_employees: int,
    avg_salary: float,
    productivity_gain_pct: float,
    implementation_cost: float,
    annual_ai_cost: float,
    years: int = 3
) -> dict:
    """Calculate ROI specifically for AI-driven productivity improvements.
    
    Args:
        num_employees: Number of employees affected
        avg_salary: Average annual salary
        productivity_gain_pct: Expected productivity gain (e.g., 0.20 for 20%)
        implementation_cost: One-time implementation cost
        annual_ai_cost: Annual AI licensing/operation cost
        years: Number of years to analyze
        
    Returns:
        Dictionary with detailed ROI breakdown
    """
    # Calculate annual productivity value
    total_salary_base = num_employees * avg_salary
    annual_productivity_value = total_salary_base * productivity_gain_pct
    
    # Calculate cash flows
    cash_flows = []
    for year in range(years):
        net_cash_flow = annual_productivity_value - annual_ai_cost
        cash_flows.append(net_cash_flow)
    
    # Calculate financial metrics
    npv = calculate_npv(cash_flows, 0.10, implementation_cost)  # 10% discount rate
    irr = calculate_irr(cash_flows, implementation_cost)
    payback = calculate_payback_period(implementation_cost, cash_flows)
    
    # Simple ROI calculation
    total_benefit = sum(cash_flows)
    total_cost = implementation_cost + (annual_ai_cost * years)
    simple_roi = ((total_benefit - total_cost) / total_cost) * 100
    
    return {
        'annual_productivity_value': annual_productivity_value,
        'total_benefit': total_benefit,
        'total_cost': total_cost,
        'simple_roi_pct': round(simple_roi, 1),
        'npv': npv,
        'irr': irr,
        'payback_years': payback,
        'benefit_cost_ratio': round(total_benefit / total_cost, 2) if total_cost > 0 else 0
    }


def calculate_break_even_analysis(
    fixed_costs: float,
    variable_cost_per_unit: float,
    price_per_unit: float,
    max_capacity: Optional[int] = None
) -> dict:
    """Calculate break-even point for AI-enabled products/services.
    
    Args:
        fixed_costs: Total fixed costs
        variable_cost_per_unit: Variable cost per unit
        price_per_unit: Selling price per unit
        max_capacity: Optional maximum capacity constraint
        
    Returns:
        Dictionary with break-even metrics
    """
    # Contribution margin per unit
    contribution_margin = price_per_unit - variable_cost_per_unit
    
    if contribution_margin <= 0:
        return {
            'break_even_units': None,
            'break_even_revenue': None,
            'contribution_margin': contribution_margin,
            'feasible': False,
            'reason': 'Negative or zero contribution margin'
        }
    
    # Break-even in units
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    
    # Check against capacity
    feasible = True
    reason = 'Break-even achievable'
    
    if max_capacity and break_even_units > max_capacity:
        feasible = False
        reason = f'Break-even ({break_even_units:.0f}) exceeds capacity ({max_capacity})'
    
    return {
        'break_even_units': round(break_even_units, 0),
        'break_even_revenue': round(break_even_revenue, 2),
        'contribution_margin': contribution_margin,
        'contribution_margin_ratio': contribution_margin / price_per_unit,
        'feasible': feasible,
        'reason': reason,
        'safety_margin_at_capacity': (
            ((max_capacity * contribution_margin - fixed_costs) / (max_capacity * contribution_margin) * 100)
            if max_capacity and feasible else None
        )
    }