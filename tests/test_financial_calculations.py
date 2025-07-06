"""Unit tests for financial calculations module.

Tests all financial calculation functions to ensure accuracy
and proper handling of edge cases.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
from business.financial_calculations import (
    calculate_npv,
    calculate_irr,
    calculate_tco,
    calculate_payback_period,
    calculate_risk_adjusted_return,
    calculate_ai_productivity_roi,
    calculate_break_even_analysis
)


class TestFinancialCalculations(unittest.TestCase):
    """Test suite for financial calculation functions."""
    
    def test_npv_positive(self):
        """Test NPV calculation with positive result."""
        cash_flows = [150000, 150000, 150000, 150000, 150000]
        npv = calculate_npv(cash_flows, 0.10, 500000)
        # Expected: sum of PV of cash flows - initial investment
        # PV = 150000/(1.1)^1 + 150000/(1.1)^2 + ... + 150000/(1.1)^5
        expected = 568618.17 - 500000  # Approximately 68,618
        self.assertAlmostEqual(npv, expected, delta=1000)
        
    def test_npv_negative(self):
        """Test NPV calculation with negative result."""
        cash_flows = [50000, 50000, 50000, 50000, 50000]
        npv = calculate_npv(cash_flows, 0.10, 500000)
        self.assertLess(npv, 0)
        
    def test_npv_zero_discount_rate(self):
        """Test NPV with zero discount rate."""
        cash_flows = [100000, 100000, 100000]
        npv = calculate_npv(cash_flows, 0.0, 250000)
        # With 0% discount, NPV = sum of cash flows - initial investment
        self.assertEqual(npv, 50000)
        
    def test_npv_high_discount_rate(self):
        """Test NPV with very high discount rate."""
        cash_flows = [1000000] * 5
        npv = calculate_npv(cash_flows, 0.50, 1000000)
        # High discount rate should significantly reduce NPV
        self.assertLess(npv, 1000000)  # Much less than undiscounted sum
        
    def test_irr_normal_case(self):
        """Test IRR calculation for normal investment."""
        cash_flows = [100000, 100000, 100000, 100000]
        irr = calculate_irr(cash_flows, 250000)
        # Should be around 21.86%
        self.assertIsNotNone(irr)
        self.assertAlmostEqual(irr, 0.2186, places=3)
        
    def test_irr_break_even(self):
        """Test IRR when NPV is exactly zero."""
        # If we invest 100 and get back 110 in one year, IRR = 10%
        cash_flows = [110]
        irr = calculate_irr(cash_flows, 100)
        self.assertAlmostEqual(irr, 0.10, places=4)
        
    def test_irr_no_positive_flows(self):
        """Test IRR with only negative cash flows."""
        cash_flows = [-1000, -1000, -1000]
        irr = calculate_irr(cash_flows, 10000)
        self.assertIsNone(irr)
        
    def test_irr_multiple_sign_changes(self):
        """Test IRR with multiple sign changes (may have multiple roots)."""
        cash_flows = [1000, -2000, 1500]
        irr = calculate_irr(cash_flows, 500)
        # Should find one of the valid IRRs
        self.assertIsNotNone(irr)
        
    def test_tco_basic(self):
        """Test basic TCO calculation."""
        initial = 100000
        operating = [20000, 20000, 20000, 20000, 20000]
        result = calculate_tco(initial, operating, 0.15, 0.10)
        
        self.assertEqual(result['initial_cost'], initial)
        self.assertGreater(result['total_tco'], initial)
        self.assertEqual(result['years'], 5)
        
    def test_tco_with_zero_maintenance(self):
        """Test TCO with no maintenance costs."""
        initial = 100000
        operating = [10000] * 3
        result = calculate_tco(initial, operating, 0.0, 0.10)
        
        # Maintenance should be 0
        self.assertEqual(result['maintenance_costs'], 0)
        
    def test_payback_period_simple(self):
        """Test simple payback period calculation."""
        cash_flows = [50000, 50000, 50000, 50000]
        payback = calculate_payback_period(cash_flows, 100000)
        self.assertEqual(payback, 2.0)
        
    def test_payback_period_fractional(self):
        """Test payback period with fractional year."""
        cash_flows = [40000, 40000, 40000, 40000]
        payback = calculate_payback_period(cash_flows, 100000)
        self.assertAlmostEqual(payback, 2.5, places=1)
        
    def test_payback_period_never(self):
        """Test payback period when investment is never recovered."""
        cash_flows = [10000, 10000, 10000]
        payback = calculate_payback_period(cash_flows, 100000)
        self.assertIsNone(payback)
        
    def test_payback_period_discounted(self):
        """Test discounted payback period."""
        cash_flows = [60000, 60000, 60000, 60000]
        payback = calculate_payback_period(cash_flows, 150000, discount_rate=0.10)
        # Discounted payback should be longer than simple payback
        simple_payback = calculate_payback_period(cash_flows, 150000)
        self.assertGreater(payback, simple_payback)
        
    def test_risk_adjusted_return_low_risk(self):
        """Test risk-adjusted return for low risk investment."""
        result = calculate_risk_adjusted_return(0.20, "Low")
        
        self.assertGreater(result['risk_adjusted_return'], 0.15)
        self.assertTrue(result['meets_threshold'])
        self.assertGreater(result['sharpe_ratio'], 1.0)
        
    def test_risk_adjusted_return_high_risk(self):
        """Test risk-adjusted return for high risk investment."""
        result = calculate_risk_adjusted_return(0.20, "High")
        
        self.assertLess(result['risk_adjusted_return'], 0.20)
        self.assertLess(result['sharpe_ratio'], result['required_return'])
        
    def test_risk_adjusted_return_very_high_risk(self):
        """Test risk-adjusted return for very high risk investment."""
        result = calculate_risk_adjusted_return(0.25, "Very High")
        
        self.assertLess(result['risk_adjusted_return'], 0.25)
        self.assertEqual(result['risk_premium'], 0.08)
        
    def test_ai_productivity_roi(self):
        """Test AI productivity ROI calculation."""
        result = calculate_ai_productivity_roi(
            num_employees=100,
            avg_salary=80000,
            productivity_gain_pct=0.20,
            implementation_cost=500000,
            annual_ai_cost=100000,
            years=5
        )
        
        # Annual productivity value should be 20% of total salary cost
        expected_annual_value = 100 * 80000 * 0.20
        self.assertEqual(result['annual_productivity_value'], expected_annual_value)
        
        # Total benefit should be annual value * years
        self.assertEqual(result['total_benefit'], expected_annual_value * 5)
        
        # NPV should account for time value
        self.assertLess(result['npv'], result['total_benefit'] - 500000)
        
    def test_ai_productivity_roi_edge_cases(self):
        """Test AI productivity ROI with edge cases."""
        # Zero productivity gain
        result = calculate_ai_productivity_roi(
            num_employees=50,
            avg_salary=60000,
            productivity_gain_pct=0.0,
            implementation_cost=100000,
            annual_ai_cost=10000,
            years=3
        )
        self.assertEqual(result['annual_productivity_value'], 0)
        self.assertLess(result['npv'], 0)  # Should be negative
        
    def test_break_even_analysis_units(self):
        """Test break-even analysis for unit-based calculation."""
        result = calculate_break_even_analysis(
            fixed_costs=100000,
            variable_cost_per_unit=50,
            price_per_unit=100,
            ai_fixed_cost_reduction=0.20,
            ai_variable_cost_reduction=0.10
        )
        
        # Original break-even: 100000 / (100 - 50) = 2000 units
        self.assertEqual(result['original_breakeven_units'], 2000)
        
        # With AI: 80000 / (100 - 45) = ~1454 units
        self.assertLess(result['ai_breakeven_units'], 2000)
        self.assertGreater(result['improvement_percentage'], 0)
        
    def test_break_even_analysis_revenue(self):
        """Test break-even analysis for revenue-based calculation."""
        result = calculate_break_even_analysis(
            fixed_costs=500000,
            variable_cost_ratio=0.60,
            ai_fixed_cost_reduction=0.15,
            ai_variable_cost_reduction=0.05
        )
        
        # Original break-even: 500000 / (1 - 0.60) = 1,250,000
        self.assertEqual(result['original_breakeven_revenue'], 1250000)
        
        # With AI, both fixed and variable costs reduce
        self.assertLess(result['ai_breakeven_revenue'], 1250000)
        
    def test_break_even_analysis_invalid_inputs(self):
        """Test break-even analysis with invalid inputs."""
        # Price less than variable cost
        result = calculate_break_even_analysis(
            fixed_costs=100000,
            variable_cost_per_unit=100,
            price_per_unit=80,  # Less than variable cost
            ai_fixed_cost_reduction=0.10,
            ai_variable_cost_reduction=0.05
        )
        
        # Should indicate infinite break-even
        self.assertEqual(result['original_breakeven_units'], float('inf'))
        
    def test_edge_cases_empty_lists(self):
        """Test functions with empty cash flow lists."""
        # NPV with empty cash flows
        npv = calculate_npv([], 0.10, 100000)
        self.assertEqual(npv, -100000)
        
        # IRR with empty cash flows
        irr = calculate_irr([], 100000)
        self.assertIsNone(irr)
        
        # Payback with empty cash flows
        payback = calculate_payback_period([], 100000)
        self.assertIsNone(payback)
        
    def test_negative_discount_rates(self):
        """Test calculations with negative discount rates."""
        # NPV with negative discount rate (rare but possible in deflation)
        cash_flows = [100000, 100000]
        npv = calculate_npv(cash_flows, -0.02, 150000)
        # With negative rate, future cash flows are worth MORE
        self.assertGreater(npv, 50000)  # Greater than undiscounted sum - investment


if __name__ == '__main__':
    unittest.main(verbosity=2)