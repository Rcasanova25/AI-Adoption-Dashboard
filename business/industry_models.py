"""Industry-specific financial models for AI adoption.

This module provides tailored financial models for different industries,
accounting for sector-specific characteristics, constraints, and opportunities.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np

from .financial_calculations import (
    calculate_npv,
    calculate_irr,
    calculate_tco,
    calculate_payback_period,
    calculate_ai_productivity_roi
)

logger = logging.getLogger(__name__)


@dataclass
class IndustryProfile:
    """Profile defining industry-specific characteristics."""
    name: str
    typical_margin: float  # Operating margin
    labor_intensity: float  # Labor cost as % of revenue
    tech_maturity: float  # 0-1 scale
    regulatory_burden: float  # 0-1 scale
    data_availability: float  # 0-1 scale
    competitive_pressure: float  # 0-1 scale
    typical_project_size: Tuple[float, float]  # Min, max investment
    implementation_speed: float  # Relative speed factor
    

# Industry profiles based on research
INDUSTRY_PROFILES = {
    "manufacturing": IndustryProfile(
        name="Manufacturing",
        typical_margin=0.12,
        labor_intensity=0.25,
        tech_maturity=0.7,
        regulatory_burden=0.6,
        data_availability=0.8,
        competitive_pressure=0.8,
        typical_project_size=(100000, 5000000),
        implementation_speed=0.8
    ),
    "healthcare": IndustryProfile(
        name="Healthcare",
        typical_margin=0.08,
        labor_intensity=0.55,
        tech_maturity=0.5,
        regulatory_burden=0.9,
        data_availability=0.7,
        competitive_pressure=0.6,
        typical_project_size=(200000, 10000000),
        implementation_speed=0.6
    ),
    "financial_services": IndustryProfile(
        name="Financial Services",
        typical_margin=0.25,
        labor_intensity=0.45,
        tech_maturity=0.9,
        regulatory_burden=0.8,
        data_availability=0.9,
        competitive_pressure=0.9,
        typical_project_size=(500000, 20000000),
        implementation_speed=1.2
    ),
    "retail": IndustryProfile(
        name="Retail & E-commerce",
        typical_margin=0.05,
        labor_intensity=0.30,
        tech_maturity=0.8,
        regulatory_burden=0.3,
        data_availability=0.85,
        competitive_pressure=0.95,
        typical_project_size=(50000, 2000000),
        implementation_speed=1.0
    ),
    "technology": IndustryProfile(
        name="Technology",
        typical_margin=0.20,
        labor_intensity=0.60,
        tech_maturity=0.95,
        regulatory_burden=0.4,
        data_availability=0.95,
        competitive_pressure=0.85,
        typical_project_size=(100000, 10000000),
        implementation_speed=1.5
    ),
    "energy": IndustryProfile(
        name="Energy & Utilities",
        typical_margin=0.15,
        labor_intensity=0.20,
        tech_maturity=0.6,
        regulatory_burden=0.85,
        data_availability=0.75,
        competitive_pressure=0.5,
        typical_project_size=(500000, 15000000),
        implementation_speed=0.7
    ),
    "government": IndustryProfile(
        name="Government & Public Sector",
        typical_margin=0.0,  # Non-profit focus
        labor_intensity=0.70,
        tech_maturity=0.4,
        regulatory_burden=0.95,
        data_availability=0.6,
        competitive_pressure=0.2,
        typical_project_size=(200000, 5000000),
        implementation_speed=0.5
    ),
    "education": IndustryProfile(
        name="Education",
        typical_margin=0.03,
        labor_intensity=0.65,
        tech_maturity=0.5,
        regulatory_burden=0.7,
        data_availability=0.65,
        competitive_pressure=0.4,
        typical_project_size=(50000, 1000000),
        implementation_speed=0.6
    )
}


def calculate_manufacturing_roi(
    investment: float,
    production_volume: float,
    defect_rate_reduction: float = 0.30,
    downtime_reduction: float = 0.25,
    labor_productivity_gain: float = 0.20,
    energy_efficiency_gain: float = 0.15,
    years: int = 5
) -> Dict:
    """
    Calculate ROI for manufacturing AI implementation.
    
    Focuses on:
    - Quality improvement (defect reduction)
    - Predictive maintenance (downtime reduction)
    - Process optimization (productivity)
    - Energy efficiency
    
    Args:
        investment: Initial AI investment
        production_volume: Annual production volume in units
        defect_rate_reduction: Expected reduction in defect rate (0-1)
        downtime_reduction: Expected reduction in downtime (0-1)
        labor_productivity_gain: Expected productivity improvement (0-1)
        energy_efficiency_gain: Expected energy savings (0-1)
        years: Analysis period
        
    Returns:
        Dictionary with financial metrics and recommendations
    """
    profile = INDUSTRY_PROFILES["manufacturing"]
    
    # Industry-specific assumptions
    avg_unit_value = 100  # Average value per unit produced
    current_defect_rate = 0.03  # 3% baseline defect rate
    annual_downtime_hours = 200  # Baseline downtime
    hourly_production_loss = production_volume * avg_unit_value / (365 * 24)
    energy_cost_per_unit = 5
    
    # Calculate annual benefits
    quality_savings = production_volume * avg_unit_value * current_defect_rate * defect_rate_reduction
    downtime_savings = annual_downtime_hours * downtime_reduction * hourly_production_loss
    productivity_value = production_volume * avg_unit_value * profile.labor_intensity * labor_productivity_gain
    energy_savings = production_volume * energy_cost_per_unit * energy_efficiency_gain
    
    total_annual_benefit = quality_savings + downtime_savings + productivity_value + energy_savings
    
    # Operating costs (15% of investment annually for manufacturing)
    annual_operating_cost = investment * 0.15
    
    # Cash flows
    annual_cash_flows = [total_annual_benefit - annual_operating_cost] * years
    
    # Calculate metrics
    npv = calculate_npv(annual_cash_flows, 0.10, investment)
    irr = calculate_irr(annual_cash_flows, investment)
    payback = calculate_payback_period(annual_cash_flows, investment)
    
    # Industry-specific insights
    insights = []
    if defect_rate_reduction > 0.25:
        insights.append("Significant quality improvements justify investment")
    if downtime_reduction > 0.20:
        insights.append("Predictive maintenance provides strong ROI")
    if profile.competitive_pressure > 0.7:
        insights.append("High competitive pressure makes AI adoption critical")
        
    return {
        "financial_metrics": {
            "npv": npv,
            "irr": irr,
            "payback_years": payback,
            "total_benefit": sum(annual_cash_flows) + investment
        },
        "benefit_breakdown": {
            "quality_improvement": quality_savings,
            "downtime_reduction": downtime_savings,
            "productivity_gain": productivity_value,
            "energy_savings": energy_savings
        },
        "industry_factors": {
            "tech_maturity": profile.tech_maturity,
            "implementation_complexity": 1 - profile.implementation_speed,
            "regulatory_risk": profile.regulatory_burden
        },
        "recommendations": insights,
        "risk_level": "Medium" if profile.tech_maturity > 0.6 else "High"
    }


def calculate_healthcare_roi(
    investment: float,
    patient_volume: float,
    diagnostic_accuracy_gain: float = 0.20,
    patient_wait_reduction: float = 0.30,
    admin_efficiency_gain: float = 0.40,
    readmission_reduction: float = 0.15,
    years: int = 5
) -> Dict:
    """
    Calculate ROI for healthcare AI implementation.
    
    Focuses on:
    - Clinical outcomes (diagnostic accuracy, readmissions)
    - Operational efficiency (wait times, admin tasks)
    - Patient satisfaction
    - Regulatory compliance
    
    Args:
        investment: Initial AI investment
        patient_volume: Annual patient volume
        diagnostic_accuracy_gain: Improvement in diagnostic accuracy (0-1)
        patient_wait_reduction: Reduction in patient wait times (0-1)
        admin_efficiency_gain: Reduction in administrative burden (0-1)
        readmission_reduction: Reduction in readmission rates (0-1)
        years: Analysis period
        
    Returns:
        Dictionary with financial metrics and recommendations
    """
    profile = INDUSTRY_PROFILES["healthcare"]
    
    # Healthcare-specific assumptions
    avg_patient_value = 500  # Average revenue per patient
    misdiagnosis_cost = 5000  # Cost of misdiagnosis
    current_misdiagnosis_rate = 0.05  # 5% baseline
    readmission_cost = 10000  # Average readmission cost
    current_readmission_rate = 0.15  # 15% baseline
    admin_cost_per_patient = 50
    
    # Calculate annual benefits
    diagnostic_value = patient_volume * current_misdiagnosis_rate * diagnostic_accuracy_gain * misdiagnosis_cost
    efficiency_value = patient_volume * patient_wait_reduction * 100  # Value of reduced wait times
    admin_savings = patient_volume * admin_cost_per_patient * admin_efficiency_gain
    readmission_savings = patient_volume * current_readmission_rate * readmission_reduction * readmission_cost
    
    total_annual_benefit = diagnostic_value + efficiency_value + admin_savings + readmission_savings
    
    # Higher operating costs due to regulatory compliance (20% of investment)
    annual_operating_cost = investment * 0.20
    
    # Additional compliance costs
    annual_compliance_cost = investment * 0.05
    
    # Cash flows
    annual_cash_flows = [total_annual_benefit - annual_operating_cost - annual_compliance_cost] * years
    
    # Calculate metrics with higher discount rate due to regulatory risk
    npv = calculate_npv(annual_cash_flows, 0.12, investment)
    irr = calculate_irr(annual_cash_flows, investment)
    payback = calculate_payback_period(annual_cash_flows, investment)
    
    # Healthcare-specific insights
    insights = []
    if diagnostic_accuracy_gain > 0.15:
        insights.append("Clinical outcome improvements provide strong justification")
    if profile.regulatory_burden > 0.8:
        insights.append("High regulatory requirements increase implementation timeline")
    if readmission_reduction > 0.10:
        insights.append("Readmission reduction aligns with value-based care incentives")
        
    return {
        "financial_metrics": {
            "npv": npv,
            "irr": irr,
            "payback_years": payback,
            "total_benefit": sum(annual_cash_flows) + investment
        },
        "benefit_breakdown": {
            "clinical_outcomes": diagnostic_value + readmission_savings,
            "operational_efficiency": efficiency_value + admin_savings,
            "compliance_costs": annual_compliance_cost * years
        },
        "industry_factors": {
            "regulatory_burden": profile.regulatory_burden,
            "data_privacy_requirements": 0.95,
            "implementation_complexity": 1 - profile.implementation_speed
        },
        "recommendations": insights,
        "risk_level": "High" if profile.regulatory_burden > 0.8 else "Medium"
    }


def calculate_financial_services_roi(
    investment: float,
    transaction_volume: float,
    fraud_detection_improvement: float = 0.40,
    processing_time_reduction: float = 0.60,
    compliance_automation: float = 0.50,
    customer_experience_gain: float = 0.30,
    years: int = 5
) -> Dict:
    """
    Calculate ROI for financial services AI implementation.
    
    Focuses on:
    - Fraud detection and prevention
    - Transaction processing efficiency
    - Regulatory compliance automation
    - Customer experience enhancement
    
    Args:
        investment: Initial AI investment
        transaction_volume: Annual transaction volume
        fraud_detection_improvement: Improvement in fraud detection (0-1)
        processing_time_reduction: Reduction in processing time (0-1)
        compliance_automation: Automation of compliance tasks (0-1)
        customer_experience_gain: Improvement in customer satisfaction (0-1)
        years: Analysis period
        
    Returns:
        Dictionary with financial metrics and recommendations
    """
    profile = INDUSTRY_PROFILES["financial_services"]
    
    # Financial services assumptions
    avg_transaction_value = 1000
    current_fraud_rate = 0.002  # 0.2% fraud rate
    fraud_loss_multiplier = 2.5  # Total loss is 2.5x transaction value
    processing_cost_per_transaction = 5
    compliance_cost_per_transaction = 3
    customer_acquisition_cost = 200
    
    # Calculate annual benefits
    fraud_savings = transaction_volume * avg_transaction_value * current_fraud_rate * fraud_detection_improvement * fraud_loss_multiplier
    processing_savings = transaction_volume * processing_cost_per_transaction * processing_time_reduction
    compliance_savings = transaction_volume * compliance_cost_per_transaction * compliance_automation
    customer_value = transaction_volume * 0.1 * customer_experience_gain * customer_acquisition_cost  # Retention value
    
    total_annual_benefit = fraud_savings + processing_savings + compliance_savings + customer_value
    
    # Operating costs (18% of investment for fintech)
    annual_operating_cost = investment * 0.18
    
    # Cash flows
    annual_cash_flows = [total_annual_benefit - annual_operating_cost] * years
    
    # Calculate metrics
    npv = calculate_npv(annual_cash_flows, 0.10, investment)
    irr = calculate_irr(annual_cash_flows, investment)
    payback = calculate_payback_period(annual_cash_flows, investment)
    
    # Financial services insights
    insights = []
    if fraud_detection_improvement > 0.30:
        insights.append("Fraud prevention provides immediate and significant ROI")
    if profile.tech_maturity > 0.8:
        insights.append("High tech maturity enables rapid implementation")
    if compliance_automation > 0.40:
        insights.append("Compliance automation reduces regulatory risk")
        
    return {
        "financial_metrics": {
            "npv": npv,
            "irr": irr,
            "payback_years": payback,
            "total_benefit": sum(annual_cash_flows) + investment
        },
        "benefit_breakdown": {
            "fraud_prevention": fraud_savings,
            "operational_efficiency": processing_savings,
            "compliance_savings": compliance_savings,
            "customer_retention": customer_value
        },
        "industry_factors": {
            "tech_maturity": profile.tech_maturity,
            "competitive_advantage": profile.competitive_pressure,
            "regulatory_compliance": profile.regulatory_burden
        },
        "recommendations": insights,
        "risk_level": "Low" if profile.tech_maturity > 0.8 else "Medium"
    }


def calculate_retail_roi(
    investment: float,
    annual_revenue: float,
    personalization_uplift: float = 0.15,
    inventory_optimization: float = 0.20,
    customer_service_automation: float = 0.50,
    supply_chain_efficiency: float = 0.25,
    years: int = 5
) -> Dict:
    """
    Calculate ROI for retail/e-commerce AI implementation.
    
    Focuses on:
    - Personalization and recommendation engines
    - Inventory management optimization
    - Customer service automation
    - Supply chain optimization
    
    Args:
        investment: Initial AI investment
        annual_revenue: Annual revenue
        personalization_uplift: Revenue increase from personalization (0-1)
        inventory_optimization: Reduction in inventory costs (0-1)
        customer_service_automation: Automation of customer service (0-1)
        supply_chain_efficiency: Improvement in supply chain (0-1)
        years: Analysis period
        
    Returns:
        Dictionary with financial metrics and recommendations
    """
    profile = INDUSTRY_PROFILES["retail"]
    
    # Retail-specific assumptions
    inventory_carrying_cost = annual_revenue * 0.25  # 25% of revenue in inventory
    customer_service_cost = annual_revenue * 0.03  # 3% of revenue
    supply_chain_cost = annual_revenue * 0.15  # 15% of revenue
    
    # Calculate annual benefits
    personalization_revenue = annual_revenue * personalization_uplift
    inventory_savings = inventory_carrying_cost * inventory_optimization
    service_savings = customer_service_cost * customer_service_automation
    supply_chain_savings = supply_chain_cost * supply_chain_efficiency
    
    total_annual_benefit = personalization_revenue + inventory_savings + service_savings + supply_chain_savings
    
    # Operating costs (12% of investment for retail)
    annual_operating_cost = investment * 0.12
    
    # Cash flows
    annual_cash_flows = [total_annual_benefit - annual_operating_cost] * years
    
    # Calculate metrics
    npv = calculate_npv(annual_cash_flows, 0.10, investment)
    irr = calculate_irr(annual_cash_flows, investment)
    payback = calculate_payback_period(annual_cash_flows, investment)
    
    # Retail insights
    insights = []
    if personalization_uplift > 0.10:
        insights.append("Personalization drives significant revenue growth")
    if profile.competitive_pressure > 0.9:
        insights.append("Extreme competitive pressure makes AI essential")
    if inventory_optimization > 0.15:
        insights.append("Inventory optimization provides quick wins")
        
    return {
        "financial_metrics": {
            "npv": npv,
            "irr": irr,
            "payback_years": payback,
            "total_benefit": sum(annual_cash_flows) + investment
        },
        "benefit_breakdown": {
            "revenue_growth": personalization_revenue,
            "inventory_savings": inventory_savings,
            "service_automation": service_savings,
            "supply_chain_savings": supply_chain_savings
        },
        "industry_factors": {
            "competitive_pressure": profile.competitive_pressure,
            "customer_expectations": 0.9,
            "implementation_speed": profile.implementation_speed
        },
        "recommendations": insights,
        "risk_level": "Low" if profile.tech_maturity > 0.7 else "Medium"
    }


def get_industry_benchmarks(industry: str) -> Dict:
    """
    Get industry-specific benchmarks and best practices.
    
    Args:
        industry: Industry identifier
        
    Returns:
        Dictionary with benchmarks and recommendations
    """
    if industry not in INDUSTRY_PROFILES:
        return {"error": f"Unknown industry: {industry}"}
        
    profile = INDUSTRY_PROFILES[industry]
    
    # Calculate industry-specific benchmarks
    benchmarks = {
        "typical_roi_range": (
            150 + profile.tech_maturity * 100,
            250 + profile.tech_maturity * 200
        ),
        "implementation_timeline_months": int(12 / profile.implementation_speed),
        "success_probability": 0.4 + profile.tech_maturity * 0.4,
        "typical_investment_range": profile.typical_project_size,
        "key_success_factors": [],
        "common_pitfalls": [],
        "recommended_use_cases": []
    }
    
    # Industry-specific success factors
    if profile.tech_maturity > 0.7:
        benchmarks["key_success_factors"].append("Leverage existing tech infrastructure")
    if profile.data_availability > 0.8:
        benchmarks["key_success_factors"].append("Rich data enables advanced analytics")
    if profile.competitive_pressure > 0.7:
        benchmarks["key_success_factors"].append("Competitive pressure drives adoption")
        
    # Common pitfalls
    if profile.regulatory_burden > 0.7:
        benchmarks["common_pitfalls"].append("Underestimating regulatory compliance")
    if profile.tech_maturity < 0.5:
        benchmarks["common_pitfalls"].append("Lack of technical infrastructure")
    if profile.labor_intensity > 0.5:
        benchmarks["common_pitfalls"].append("Change management challenges")
        
    # Recommended use cases by industry
    use_cases = {
        "manufacturing": ["Predictive maintenance", "Quality control", "Supply chain optimization"],
        "healthcare": ["Diagnostic assistance", "Patient flow optimization", "Drug discovery"],
        "financial_services": ["Fraud detection", "Risk assessment", "Algorithmic trading"],
        "retail": ["Recommendation engines", "Inventory optimization", "Dynamic pricing"],
        "technology": ["Code generation", "Bug detection", "Performance optimization"],
        "energy": ["Demand forecasting", "Grid optimization", "Predictive maintenance"],
        "government": ["Document processing", "Citizen services", "Resource allocation"],
        "education": ["Personalized learning", "Student retention", "Administrative automation"]
    }
    
    benchmarks["recommended_use_cases"] = use_cases.get(industry, [])
    
    return benchmarks


def select_optimal_ai_strategy(
    industry: str,
    company_size: str,
    budget: float,
    timeline_months: int,
    strategic_goals: List[str]
) -> Dict:
    """
    Recommend optimal AI strategy based on industry and constraints.
    
    Args:
        industry: Industry identifier
        company_size: Small, Medium, Large, Enterprise
        budget: Available budget
        timeline_months: Implementation timeline
        strategic_goals: List of strategic objectives
        
    Returns:
        Dictionary with recommended strategy and implementation plan
    """
    if industry not in INDUSTRY_PROFILES:
        return {"error": f"Unknown industry: {industry}"}
        
    profile = INDUSTRY_PROFILES[industry]
    
    # Adjust recommendations based on company size
    size_factors = {
        "Small": {"budget_multiplier": 0.5, "timeline_multiplier": 1.5, "risk_tolerance": "Low"},
        "Medium": {"budget_multiplier": 1.0, "timeline_multiplier": 1.0, "risk_tolerance": "Medium"},
        "Large": {"budget_multiplier": 2.0, "timeline_multiplier": 0.8, "risk_tolerance": "Medium"},
        "Enterprise": {"budget_multiplier": 5.0, "timeline_multiplier": 0.6, "risk_tolerance": "High"}
    }
    
    size_factor = size_factors.get(company_size, size_factors["Medium"])
    
    # Check budget feasibility
    min_budget, max_budget = profile.typical_project_size
    adjusted_min = min_budget * size_factor["budget_multiplier"]
    adjusted_max = max_budget * size_factor["budget_multiplier"]
    
    if budget < adjusted_min:
        return {
            "feasibility": "Limited",
            "recommendation": "Consider pilot project or phased approach",
            "suggested_budget": adjusted_min
        }
    
    # Calculate implementation phases
    implementation_months = int(timeline_months * size_factor["timeline_multiplier"] / profile.implementation_speed)
    
    # Strategic recommendations
    strategy = {
        "feasibility": "High" if budget > adjusted_min * 1.5 else "Medium",
        "recommended_approach": "",
        "priority_use_cases": [],
        "implementation_phases": [],
        "expected_roi_range": get_industry_benchmarks(industry)["typical_roi_range"],
        "risk_mitigation": [],
        "success_factors": []
    }
    
    # Determine approach based on goals and industry
    if "cost_reduction" in strategic_goals and profile.labor_intensity > 0.4:
        strategy["recommended_approach"] = "Process automation and efficiency focus"
        strategy["priority_use_cases"].append("Workflow automation")
    elif "revenue_growth" in strategic_goals and profile.competitive_pressure > 0.7:
        strategy["recommended_approach"] = "Customer experience and innovation focus"
        strategy["priority_use_cases"].append("Personalization and recommendations")
    else:
        strategy["recommended_approach"] = "Balanced efficiency and growth approach"
        
    # Implementation phases
    phases = []
    if implementation_months <= 6:
        phases.append({"phase": 1, "duration": implementation_months, "focus": "Single high-impact use case"})
    else:
        phase_duration = implementation_months // 3
        phases.extend([
            {"phase": 1, "duration": phase_duration, "focus": "Pilot and proof of concept"},
            {"phase": 2, "duration": phase_duration, "focus": "Scale successful pilots"},
            {"phase": 3, "duration": phase_duration, "focus": "Enterprise integration"}
        ])
    
    strategy["implementation_phases"] = phases
    
    # Risk mitigation strategies
    if profile.regulatory_burden > 0.7:
        strategy["risk_mitigation"].append("Early regulatory compliance review")
    if profile.tech_maturity < 0.6:
        strategy["risk_mitigation"].append("Invest in technical infrastructure")
    if size_factor["risk_tolerance"] == "Low":
        strategy["risk_mitigation"].append("Start with low-risk pilot projects")
        
    return strategy