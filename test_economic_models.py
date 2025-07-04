"""Test script to verify accurate economic model implementations."""

import sys
sys.path.append('/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard')

from components.economic_models import AIEconomicModels, EconomicParameters

def test_productivity_calculations():
    """Test productivity gain calculations."""
    print("\n=== Testing Productivity Gain Calculations ===")
    
    models = AIEconomicModels()
    
    # Test different industries
    industries = ["Technology", "Financial Services", "Healthcare", "Manufacturing"]
    
    for industry in industries:
        result = models.calculate_productivity_gain(
            revenue=100_000_000,  # $100M
            years=3,
            industry=industry,
            skill_level="Mixed",
            adoption_maturity=0.5
        )
        
        print(f"\n{industry}:")
        print(f"  - Industry baseline: {result['industry_baseline']:.1f}%")
        print(f"  - Skill-adjusted gain: {result['skill_adjusted_gain']:.1f}%")
        print(f"  - Time-adjusted factor: {result['time_adjusted_factor']:.2f}")
        print(f"  - Final productivity gain: {result['productivity_gain_percentage']:.1f}%")
        print(f"  - Annual improvement: ${result['annual_productivity_improvement']:,.0f}")


def test_market_value_calculations():
    """Test market value impact calculations."""
    print("\n\n=== Testing Market Value Impact Calculations ===")
    
    models = AIEconomicModels()
    
    # Test different adoption levels
    adoption_levels = [25, 50, 75]
    
    for adoption in adoption_levels:
        result = models.calculate_market_value_impact(
            revenue=100_000_000,  # $100M
            industry="Technology",
            ai_adoption_level=adoption,
            competitive_position="Average"
        )
        
        print(f"\nAdoption Level: {adoption}%")
        print(f"  - Market value increase: ${result['market_value_increase']:,.0f}")
        print(f"  - Percentage increase: {result['market_value_increase_percentage']:.1f}%")
        print(f"  - P/E ratio: {result['pe_ratio']:.1f}x")
        print(f"  - Network effect multiplier: {result['network_effect_multiplier']:.2f}x")
        print(f"  - Adoption premium: {result['adoption_premium']:.1f}%")


def test_payback_calculations():
    """Test payback period calculations."""
    print("\n\n=== Testing Payback Period Calculations ===")
    
    models = AIEconomicModels()
    
    # Test different industries
    industries = ["Technology", "Healthcare", "Manufacturing"]
    
    for industry in industries:
        result = models.calculate_payback_period(
            investment=1_000_000,
            annual_benefit=2_500_000,
            industry=industry,
            implementation_complexity="Medium"
        )
        
        print(f"\n{industry}:")
        print(f"  - Payback period: {result['payback_months']:.0f} months ({result['payback_years']:.1f} years)")
        print(f"  - Base payback: {result['base_payback_months']:.0f} months")
        print(f"  - Ramp-up period: {result['ramp_up_months']:.0f} months")
        print(f"  - Learning curve: {result['learning_curve_months']:.0f} months")
        print(f"  - Total implementation: {result['total_implementation_months']:.0f} months")


def test_roi_calculations():
    """Test ROI calculations with industry-specific parameters."""
    print("\n\n=== Testing ROI Calculations ===")
    
    models = AIEconomicModels()
    
    result = models.calculate_roi_with_real_data(
        investment=1_000_000,
        use_case="Customer Service Automation",
        implementation_years=3,
        company_size="Large",
        current_efficiency=1.0,
        industry="Financial Services"
    )
    
    print("\nFinancial Services - Customer Service Automation:")
    print(f"  - Total ROI: {result['total_roi_percentage']:.0f}%")
    print(f"  - NPV: ${result['npv']:,.0f}")
    print(f"  - Payback period: {result['payback_period_years']:.1f} years")
    print(f"  - Efficiency gain: {result['efficiency_gain_percentage']:.0f}%")
    print(f"  - Industry productivity gain: {result['industry_productivity_gain']:.0f}%")
    print(f"  - Learning curve impact: {result['learning_curve_impact']:.0f}%")
    print(f"  - IRR: {result['irr']:.1f}%")


def validate_models():
    """Validate that models are using accurate data."""
    print("\n\n=== Validating Model Accuracy ===")
    
    models = AIEconomicModels()
    validations = models.validate_calculations()
    
    print("\nValidation Results:")
    for check, passed in validations.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {check}: {status}")
    
    # Check data sources
    print("\n\nData Sources:")
    sources = models.get_data_sources()
    for source_type, source in sources.items():
        print(f"  - {source_type}: {source}")


def compare_old_vs_new():
    """Compare old fixed multipliers vs new accurate models."""
    print("\n\n=== Comparing Old vs New Calculations ===")
    
    models = AIEconomicModels()
    revenue = 100_000_000
    years = 3
    
    # Old calculation (fixed 0.3% multiplier)
    old_productivity_gain = revenue * 0.003 * years
    
    # New calculation
    new_result = models.calculate_productivity_gain(
        revenue=revenue,
        years=years,
        industry="Technology",
        skill_level="Mixed",
        adoption_maturity=0.5
    )
    
    print(f"\nProductivity Gain Comparison (Technology, 3 years):")
    print(f"  Old (0.3% fixed): ${old_productivity_gain:,.0f}")
    print(f"  New (data-driven): ${new_result['cumulative_productivity_gain']:,.0f}")
    print(f"  Difference: {(new_result['cumulative_productivity_gain'] / old_productivity_gain - 1) * 100:.0f}% higher")
    
    # Old market value calculation (fixed 0.15% multiplier)
    old_market_impact = revenue * 0.0015
    
    # New calculation
    new_market = models.calculate_market_value_impact(
        revenue=revenue,
        industry="Technology",
        ai_adoption_level=50,
        competitive_position="Average"
    )
    
    print(f"\nMarket Value Impact Comparison:")
    print(f"  Old (0.15% fixed): ${old_market_impact:,.0f}")
    print(f"  New (data-driven): ${new_market['market_value_increase']:,.0f}")
    print(f"  Difference: {(new_market['market_value_increase'] / old_market_impact - 1) * 100:.0f}% higher")


if __name__ == "__main__":
    print("Testing Accurate Economic Models Implementation")
    print("=" * 50)
    
    test_productivity_calculations()
    test_market_value_calculations()
    test_payback_calculations()
    test_roi_calculations()
    validate_models()
    compare_old_vs_new()
    
    print("\n\nAll tests completed!")