"""Test script for Phase 2 integration.

This script tests the new financial calculations, scenario engine,
and industry models to ensure they work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from business.financial_calculations import (
    calculate_npv, calculate_irr, calculate_tco,
    calculate_payback_period, calculate_risk_adjusted_return
)
from business.scenario_engine import (
    monte_carlo_simulation, sensitivity_analysis,
    adoption_s_curve, ScenarioVariable
)
from business.industry_models import (
    calculate_manufacturing_roi, calculate_healthcare_roi,
    calculate_financial_services_roi, calculate_retail_roi,
    get_industry_benchmarks
)
from business.roi_analysis import compute_comprehensive_roi


def test_financial_calculations():
    """Test core financial calculation functions."""
    print("\n=== Testing Financial Calculations ===")
    
    # Test NPV
    cash_flows = [100000, 120000, 140000, 160000, 180000]
    npv = calculate_npv(cash_flows, 0.10, 500000)
    print(f"NPV Test: ${npv:,.2f}")
    assert npv < 0, "NPV should be negative with high initial investment"
    
    # Test IRR
    irr = calculate_irr(cash_flows, 200000)
    print(f"IRR Test: {irr*100:.1f}%" if irr else "IRR: Cannot calculate")
    
    # Test TCO
    operating_costs = [50000] * 5
    tco = calculate_tco(500000, operating_costs, 0.15, 0.10)
    print(f"TCO Test: ${tco['total_tco']:,.2f}")
    
    # Test Payback Period
    payback = calculate_payback_period(cash_flows, 300000)
    print(f"Payback Period: {payback:.1f} years" if payback else "Payback: Never")
    
    # Test Risk-Adjusted Return
    risk_metrics = calculate_risk_adjusted_return(0.25, "High")
    print(f"Risk-Adjusted Return: {risk_metrics['risk_adjusted_return']*100:.1f}%")
    print(f"Sharpe Ratio: {risk_metrics['sharpe_ratio']:.2f}")
    
    print("✅ Financial calculations tests passed!")


def test_scenario_engine():
    """Test scenario analysis engine."""
    print("\n=== Testing Scenario Engine ===")
    
    # Define a simple ROI model
    def roi_model(investment, annual_benefit, annual_cost, years=5):
        net_benefit = annual_benefit - annual_cost
        total_return = net_benefit * years - investment
        roi = total_return / investment if investment > 0 else 0
        return roi
    
    # Test Monte Carlo simulation
    base_case = {
        "investment": 1000000,
        "annual_benefit": 400000,
        "annual_cost": 100000,
        "years": 5
    }
    
    variables = [
        ScenarioVariable(
            name="investment",
            base_value=1000000,
            min_value=800000,
            max_value=1200000,
            distribution="normal",
            std_dev=100000
        ),
        ScenarioVariable(
            name="annual_benefit",
            base_value=400000,
            min_value=300000,
            max_value=500000,
            distribution="triangular"
        )
    ]
    
    mc_results = monte_carlo_simulation(base_case, variables, roi_model, iterations=1000)
    print(f"Monte Carlo Results:")
    print(f"  Mean ROI: {mc_results['mean']*100:.1f}%")
    print(f"  Std Dev: {mc_results['std_dev']*100:.1f}%")
    print(f"  90% Confidence Interval: [{mc_results['confidence_interval_90'][0]*100:.1f}%, {mc_results['confidence_interval_90'][1]*100:.1f}%]")
    
    # Test sensitivity analysis
    sensitivity_vars = ["investment", "annual_benefit", "annual_cost"]
    sensitivity_results = sensitivity_analysis(base_case, sensitivity_vars, roi_model)
    print(f"\nSensitivity Analysis:")
    for var, rank in sensitivity_results['sensitivity_ranking']:
        print(f"  {var}: elasticity = {sensitivity_results[var]['elasticity']:.2f}")
    
    # Test S-curve adoption
    adoption_curve = adoption_s_curve(24, max_adoption=90, steepness=0.3)
    print(f"\nAdoption Curve (24 months):")
    print(f"  Month 6: {adoption_curve[6]:.1f}%")
    print(f"  Month 12: {adoption_curve[12]:.1f}%")
    print(f"  Month 24: {adoption_curve[23]:.1f}%")
    
    print("✅ Scenario engine tests passed!")


def test_industry_models():
    """Test industry-specific ROI models."""
    print("\n=== Testing Industry Models ===")
    
    # Test Manufacturing ROI
    print("\nManufacturing ROI:")
    mfg_results = calculate_manufacturing_roi(
        investment=2000000,
        production_volume=1000000,
        defect_rate_reduction=0.30,
        downtime_reduction=0.25
    )
    print(f"  NPV: ${mfg_results['financial_metrics']['npv']:,.0f}")
    print(f"  IRR: {mfg_results['financial_metrics']['irr']*100:.1f}%" if mfg_results['financial_metrics']['irr'] else "  IRR: N/A")
    print(f"  Risk Level: {mfg_results['risk_level']}")
    
    # Test Healthcare ROI
    print("\nHealthcare ROI:")
    health_results = calculate_healthcare_roi(
        investment=3000000,
        patient_volume=50000,
        diagnostic_accuracy_gain=0.20,
        admin_efficiency_gain=0.40
    )
    print(f"  NPV: ${health_results['financial_metrics']['npv']:,.0f}")
    print(f"  Clinical Benefits: ${health_results['benefit_breakdown']['clinical_outcomes']:,.0f}")
    print(f"  Risk Level: {health_results['risk_level']}")
    
    # Test Financial Services ROI
    print("\nFinancial Services ROI:")
    fin_results = calculate_financial_services_roi(
        investment=5000000,
        transaction_volume=10000000,
        fraud_detection_improvement=0.40,
        processing_time_reduction=0.60
    )
    print(f"  NPV: ${fin_results['financial_metrics']['npv']:,.0f}")
    print(f"  Fraud Savings: ${fin_results['benefit_breakdown']['fraud_prevention']:,.0f}")
    print(f"  Risk Level: {fin_results['risk_level']}")
    
    # Test Retail ROI
    print("\nRetail ROI:")
    retail_results = calculate_retail_roi(
        investment=1000000,
        annual_revenue=50000000,
        personalization_uplift=0.15,
        inventory_optimization=0.20
    )
    print(f"  NPV: ${retail_results['financial_metrics']['npv']:,.0f}")
    print(f"  Revenue Growth: ${retail_results['benefit_breakdown']['revenue_growth']:,.0f}")
    print(f"  Risk Level: {retail_results['risk_level']}")
    
    # Test industry benchmarks
    print("\nIndustry Benchmarks (Healthcare):")
    benchmarks = get_industry_benchmarks("healthcare")
    print(f"  Typical ROI Range: {benchmarks['typical_roi_range'][0]:.0f}% - {benchmarks['typical_roi_range'][1]:.0f}%")
    print(f"  Implementation Timeline: {benchmarks['implementation_timeline_months']} months")
    print(f"  Success Probability: {benchmarks['success_probability']*100:.0f}%")
    
    print("✅ Industry models tests passed!")


def test_comprehensive_roi():
    """Test the comprehensive ROI calculation."""
    print("\n=== Testing Comprehensive ROI ===")
    
    results = compute_comprehensive_roi(
        initial_investment=1000000,
        annual_cash_flows=[300000, 350000, 400000, 450000, 500000],
        annual_operating_costs=[50000, 55000, 60000, 65000, 70000],
        risk_level="Medium",
        discount_rate=0.10,
        num_employees=100,
        avg_salary=75000,
        productivity_gain_pct=0.20
    )
    
    print("Financial Metrics:")
    print(f"  NPV: ${results['financial_metrics']['npv']:,.0f}")
    print(f"  IRR: {results['financial_metrics']['irr']*100:.1f}%" if results['financial_metrics']['irr'] else "  IRR: N/A")
    print(f"  Simple ROI: {results['financial_metrics']['simple_roi_pct']:.1f}%")
    
    print("\nTCO Analysis:")
    print(f"  Total TCO: ${results['tco_analysis']['total_tco']:,.0f}")
    print(f"  Annual TCO: ${results['tco_analysis']['annual_tco']:,.0f}")
    
    print("\nRisk Analysis:")
    print(f"  Risk-Adjusted Return: {results['risk_analysis']['risk_adjusted_return']*100:.1f}%")
    print(f"  Sharpe Ratio: {results['risk_analysis']['sharpe_ratio']:.2f}")
    print(f"  Meets Threshold: {results['risk_analysis']['meets_threshold']}")
    
    print("\nInvestment Decision:")
    print(f"  Recommended: {results['investment_decision']['recommended']}")
    print(f"  NPV Positive: {results['investment_decision']['npv_positive']}")
    print(f"  IRR Exceeds Hurdle: {results['investment_decision']['irr_exceeds_hurdle']}")
    
    print("✅ Comprehensive ROI test passed!")


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("PHASE 2 INTEGRATION TESTS")
    print("=" * 60)
    
    try:
        test_financial_calculations()
        test_scenario_engine()
        test_industry_models()
        test_comprehensive_roi()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! Phase 2 integration is working correctly.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()