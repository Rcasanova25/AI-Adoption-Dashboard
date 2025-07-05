"""ROI and investment case analysis for AI adoption."""

from data.models.economics import ROIMetrics


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
