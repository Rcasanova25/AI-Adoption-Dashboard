"""ROI and investment case analysis for AI adoption.

Enhanced with comprehensive financial calculations including NPV, IRR,
and risk-adjusted returns for sophisticated investment analysis.
"""

from typing import Dict, List, Optional
from data.models.economics import ROIMetrics
from .financial_calculations import (
    calculate_npv,
    calculate_irr,
    calculate_tco,
    calculate_risk_adjusted_return,
    calculate_ai_productivity_roi
)


def compute_roi(
    initial_investment: float,
    annual_savings: float,
    payback_period_months: int,
    risk_level: str = "Medium",
    productivity_gain_percent: float = 0.0,
) -> ROIMetrics:
    """
    Compute ROI metrics for an AI implementation.
    Args:
        initial_investment: Initial investment amount
        annual_savings: Annual cost savings
        payback_period_months: Payback period in months
        risk_level: Risk level (Low, Medium, High, Very High)
        productivity_gain_percent: Productivity gain percentage
    Returns:
        ROIMetrics object
    """
    total_roi_percent = (
        (annual_savings * (12 / payback_period_months)) / initial_investment * 100
        if payback_period_months > 0
        else 0
    )
    breakeven_months = payback_period_months if payback_period_months > 0 else None
    return ROIMetrics(
        implementation_type="AI",
        initial_investment=initial_investment,
        payback_period_months=payback_period_months,
        total_roi_percent=total_roi_percent,
        annual_savings=annual_savings,
        productivity_gain_percent=productivity_gain_percent,
        breakeven_months=breakeven_months,
        risk_level=risk_level,
    )


def compute_comprehensive_roi(
    initial_investment: float,
    annual_cash_flows: List[float],
    annual_operating_costs: List[float],
    risk_level: str = "Medium",
    discount_rate: float = 0.10,
    num_employees: Optional[int] = None,
    avg_salary: Optional[float] = None,
    productivity_gain_pct: Optional[float] = None
) -> Dict:
    """
    Compute comprehensive ROI metrics including NPV, IRR, and risk adjustments.
    
    Args:
        initial_investment: Initial investment amount
        annual_cash_flows: List of annual net cash flows (revenue - costs)
        annual_operating_costs: List of annual operating costs
        risk_level: Risk level (Low, Medium, High, Very High)
        discount_rate: Discount rate for NPV calculation
        num_employees: Number of employees affected (for productivity ROI)
        avg_salary: Average salary (for productivity ROI)
        productivity_gain_pct: Expected productivity gain
        
    Returns:
        Dictionary with comprehensive ROI metrics
    """
    # Calculate basic financial metrics
    npv = calculate_npv(annual_cash_flows, discount_rate, initial_investment)
    irr = calculate_irr(annual_cash_flows, initial_investment)
    
    # Calculate TCO
    tco_analysis = calculate_tco(
        initial_investment,
        annual_operating_costs,
        maintenance_rate=0.15,
        discount_rate=discount_rate
    )
    
    # Calculate risk-adjusted returns
    expected_return = irr if irr else sum(annual_cash_flows) / len(annual_cash_flows) / initial_investment
    risk_metrics = calculate_risk_adjusted_return(expected_return, risk_level)
    
    # Calculate productivity ROI if employee data provided
    productivity_roi = None
    if all([num_employees, avg_salary, productivity_gain_pct]):
        annual_ai_cost = sum(annual_operating_costs) / len(annual_operating_costs)
        productivity_roi = calculate_ai_productivity_roi(
            num_employees=num_employees,
            avg_salary=avg_salary,
            productivity_gain_pct=productivity_gain_pct,
            implementation_cost=initial_investment,
            annual_ai_cost=annual_ai_cost,
            years=len(annual_cash_flows)
        )
    
    # Calculate simple metrics
    total_return = sum(annual_cash_flows)
    simple_roi = ((total_return - initial_investment) / initial_investment) * 100
    
    # Compile comprehensive results
    return {
        'financial_metrics': {
            'npv': npv,
            'irr': irr,
            'simple_roi_pct': round(simple_roi, 1),
            'payback_years': initial_investment / (total_return / len(annual_cash_flows)) if total_return > 0 else None
        },
        'tco_analysis': tco_analysis,
        'risk_analysis': risk_metrics,
        'productivity_analysis': productivity_roi,
        'investment_decision': {
            'recommended': npv > 0 and risk_metrics['meets_threshold'],
            'npv_positive': npv > 0,
            'irr_exceeds_hurdle': irr and irr > discount_rate,
            'risk_acceptable': risk_metrics['meets_threshold']
        }
    }


def analyze_roi_by_company_size(
    company_size: str,
    ai_use_case: str,
    industry: str = "General"
) -> Dict:
    """
    Provide ROI benchmarks based on company size and use case.
    
    Args:
        company_size: 'Small', 'Medium', 'Large', 'Enterprise'
        ai_use_case: Type of AI implementation
        industry: Industry sector
        
    Returns:
        Dictionary with ROI benchmarks and recommendations
    """
    # Size-based investment ranges
    size_profiles = {
        'Small': {
            'typical_investment': (50000, 200000),
            'payback_expectation': 18,  # months
            'success_rate': 0.45,
            'common_risks': ['Resource constraints', 'Limited expertise', 'Change management']
        },
        'Medium': {
            'typical_investment': (200000, 1000000),
            'payback_expectation': 15,
            'success_rate': 0.65,
            'common_risks': ['Integration complexity', 'Scaling challenges']
        },
        'Large': {
            'typical_investment': (1000000, 5000000),
            'payback_expectation': 12,
            'success_rate': 0.75,
            'common_risks': ['Organizational inertia', 'Legacy systems']
        },
        'Enterprise': {
            'typical_investment': (5000000, 50000000),
            'payback_expectation': 18,
            'success_rate': 0.85,
            'common_risks': ['Governance complexity', 'Multi-stakeholder alignment']
        }
    }
    
    # Use case ROI multipliers
    use_case_multipliers = {
        'Customer Service': 2.5,
        'Process Automation': 3.2,
        'Predictive Analytics': 2.8,
        'Supply Chain': 2.2,
        'Marketing Personalization': 3.5,
        'Fraud Detection': 4.0,
        'Quality Control': 2.7
    }
    
    profile = size_profiles.get(company_size, size_profiles['Medium'])
    roi_multiplier = use_case_multipliers.get(ai_use_case, 2.5)
    
    # Calculate expected ROI range
    min_investment, max_investment = profile['typical_investment']
    expected_roi_low = (roi_multiplier - 0.5) * 100
    expected_roi_high = (roi_multiplier + 0.5) * 100
    
    return {
        'company_size': company_size,
        'investment_range': profile['typical_investment'],
        'expected_roi_range': (expected_roi_low, expected_roi_high),
        'typical_payback_months': profile['payback_expectation'],
        'success_probability': profile['success_rate'],
        'key_risks': profile['common_risks'],
        'recommendation': f"For {company_size} companies implementing {ai_use_case}, "
                         f"expect {expected_roi_low:.0f}-{expected_roi_high:.0f}% ROI "
                         f"with {profile['payback_expectation']} month payback period."
    }
