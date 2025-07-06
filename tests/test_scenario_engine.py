"""Unit tests for scenario engine module.

Tests Monte Carlo simulation, sensitivity analysis, and other
scenario planning functions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import numpy as np
import pandas as pd
from business.scenario_engine import (
    ScenarioVariable,
    monte_carlo_simulation,
    sensitivity_analysis,
    adoption_s_curve,
    technology_correlation_matrix,
    scenario_comparison,
    create_scenario_tornado_chart
)


class TestScenarioEngine(unittest.TestCase):
    """Test suite for scenario engine functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Simple test model function
        self.test_model = lambda x, y: x * y
        
        # More complex model for ROI
        def roi_model(investment, revenue, cost, years=5):
            net_benefit = (revenue - cost) * years
            return (net_benefit - investment) / investment if investment > 0 else 0
        self.roi_model = roi_model
        
    def test_scenario_variable_creation(self):
        """Test ScenarioVariable dataclass creation."""
        var = ScenarioVariable(
            name="test_var",
            base_value=100,
            min_value=50,
            max_value=150,
            distribution="normal",
            std_dev=20
        )
        
        self.assertEqual(var.name, "test_var")
        self.assertEqual(var.base_value, 100)
        self.assertEqual(var.distribution, "normal")
        self.assertEqual(var.std_dev, 20)
        
    def test_monte_carlo_basic(self):
        """Test basic Monte Carlo simulation."""
        base_case = {"x": 10, "y": 5}
        variables = [
            ScenarioVariable("x", 10, 8, 12, "uniform"),
            ScenarioVariable("y", 5, 4, 6, "uniform")
        ]
        
        results = monte_carlo_simulation(
            base_case, variables, self.test_model, iterations=1000
        )
        
        # Check structure
        self.assertIn('mean', results)
        self.assertIn('std_dev', results)
        self.assertIn('percentiles', results)
        self.assertIn('correlations', results)
        
        # Mean should be close to base case (10 * 5 = 50)
        self.assertAlmostEqual(results['mean'], 50, delta=2)
        
        # Check percentiles exist
        self.assertIn('p5', results['percentiles'])
        self.assertIn('p95', results['percentiles'])
        
    def test_monte_carlo_distributions(self):
        """Test different distribution types in Monte Carlo."""
        base_case = {"value": 100}
        
        # Test normal distribution
        normal_var = [ScenarioVariable("value", 100, 50, 150, "normal", std_dev=20)]
        normal_results = monte_carlo_simulation(
            base_case, normal_var, lambda value: value, iterations=10000
        )
        # Should be centered around 100
        self.assertAlmostEqual(normal_results['mean'], 100, delta=5)
        
        # Test uniform distribution
        uniform_var = [ScenarioVariable("value", 100, 0, 200, "uniform")]
        uniform_results = monte_carlo_simulation(
            base_case, uniform_var, lambda value: value, iterations=10000
        )
        # Mean of uniform(0, 200) should be 100
        self.assertAlmostEqual(uniform_results['mean'], 100, delta=5)
        
        # Test triangular distribution
        triangular_var = [ScenarioVariable("value", 100, 50, 150, "triangular", mode=100)]
        triangular_results = monte_carlo_simulation(
            base_case, triangular_var, lambda value: value, iterations=10000
        )
        # Mode at 100, should be centered there
        self.assertAlmostEqual(triangular_results['mean'], 100, delta=5)
        
    def test_monte_carlo_correlations(self):
        """Test correlation calculation in Monte Carlo."""
        # Model where output = 2*x - y (positive correlation with x, negative with y)
        def correlation_model(x, y):
            return 2 * x - y
        
        base_case = {"x": 10, "y": 5}
        variables = [
            ScenarioVariable("x", 10, 5, 15, "uniform"),
            ScenarioVariable("y", 5, 0, 10, "uniform")
        ]
        
        results = monte_carlo_simulation(
            base_case, variables, correlation_model, iterations=5000
        )
        
        # x should have positive correlation
        self.assertGreater(results['correlations']['x']['correlation'], 0.8)
        self.assertTrue(results['correlations']['x']['significant'])
        
        # y should have negative correlation
        self.assertLess(results['correlations']['y']['correlation'], -0.4)
        self.assertTrue(results['correlations']['y']['significant'])
        
    def test_monte_carlo_confidence_intervals(self):
        """Test confidence interval calculations."""
        base_case = {"value": 100}
        variables = [ScenarioVariable("value", 100, 80, 120, "uniform")]
        
        results = monte_carlo_simulation(
            base_case, variables, lambda value: value, 
            iterations=10000,
            confidence_levels=[0.10, 0.90]
        )
        
        # 90% confidence interval for uniform(80, 120)
        ci_low, ci_high = results['confidence_interval_90']
        self.assertAlmostEqual(ci_low, 84, delta=2)  # 10th percentile
        self.assertAlmostEqual(ci_high, 116, delta=2)  # 90th percentile
        
    def test_sensitivity_analysis_basic(self):
        """Test basic sensitivity analysis."""
        base_case = {"investment": 100000, "revenue": 50000, "cost": 20000}
        variables = ["investment", "revenue", "cost"]
        
        results = sensitivity_analysis(
            base_case, variables, self.roi_model, 
            variation_pct=0.20, steps=3
        )
        
        # Check structure
        self.assertIn('base_result', results)
        self.assertIn('sensitivity_ranking', results)
        
        # Revenue should have positive elasticity
        self.assertGreater(results['revenue']['elasticity'], 0)
        
        # Cost should have negative elasticity
        self.assertLess(results['cost']['elasticity'], 0)
        
        # Investment should have negative elasticity
        self.assertLess(results['investment']['elasticity'], 0)
        
    def test_sensitivity_analysis_ranking(self):
        """Test sensitivity ranking."""
        # Model highly sensitive to x, less to y
        def sensitive_model(x, y):
            return x**2 + y
        
        base_case = {"x": 10, "y": 5}
        results = sensitivity_analysis(
            base_case, ["x", "y"], sensitive_model
        )
        
        # x should rank higher than y
        ranking = results['sensitivity_ranking']
        x_rank = next(i for i, (var, _) in enumerate(ranking) if var == 'x')
        y_rank = next(i for i, (var, _) in enumerate(ranking) if var == 'y')
        self.assertLess(x_rank, y_rank)  # x comes first (more sensitive)
        
    def test_adoption_s_curve_basic(self):
        """Test S-curve adoption pattern generation."""
        # 12-month adoption curve
        curve = adoption_s_curve(12, max_adoption=100, steepness=0.5)
        
        self.assertEqual(len(curve), 12)
        
        # Should start low and end high
        self.assertLess(curve[0], 20)  # Low initial adoption
        self.assertGreater(curve[-1], 80)  # High final adoption
        
        # Should be monotonically increasing
        for i in range(1, len(curve)):
            self.assertGreaterEqual(curve[i], curve[i-1])
            
    def test_adoption_s_curve_parameters(self):
        """Test S-curve with different parameters."""
        # Test max adoption limit
        curve = adoption_s_curve(24, max_adoption=75)
        self.assertLessEqual(max(curve), 75)
        
        # Test inflection point
        early_inflection = adoption_s_curve(20, inflection_point=5, steepness=0.5)
        late_inflection = adoption_s_curve(20, inflection_point=15, steepness=0.5)
        
        # Early inflection should have higher adoption at month 10
        self.assertGreater(early_inflection[10], late_inflection[10])
        
        # Test steepness
        gentle_curve = adoption_s_curve(20, steepness=0.2)
        steep_curve = adoption_s_curve(20, steepness=0.8)
        
        # Steep curve should have more dramatic change around inflection
        mid_point = 10
        gentle_range = gentle_curve[mid_point+2] - gentle_curve[mid_point-2]
        steep_range = steep_curve[mid_point+2] - steep_curve[mid_point-2]
        self.assertGreater(steep_range, gentle_range)
        
    def test_technology_correlation_matrix(self):
        """Test technology correlation matrix generation."""
        technologies = ["AI", "IoT", "Blockchain", "5G"]
        
        # Test complementary technologies
        comp_matrix = technology_correlation_matrix(technologies, "complementary")
        n = len(technologies)
        
        # Check dimensions
        self.assertEqual(comp_matrix.shape, (n, n))
        
        # Diagonal should be 1
        for i in range(n):
            self.assertEqual(comp_matrix[i, i], 1.0)
            
        # Should be symmetric
        for i in range(n):
            for j in range(n):
                self.assertEqual(comp_matrix[i, j], comp_matrix[j, i])
                
        # Complementary should have mostly positive correlations
        off_diagonal = comp_matrix[np.triu_indices(n, k=1)]
        self.assertGreater(np.mean(off_diagonal), 0)
        
        # Test competitive technologies
        comp_matrix = technology_correlation_matrix(technologies, "competitive")
        off_diagonal = comp_matrix[np.triu_indices(n, k=1)]
        self.assertLess(np.mean(off_diagonal), 0)
        
    def test_scenario_comparison(self):
        """Test scenario comparison functionality."""
        scenarios = {
            "Conservative": {"investment": 100000, "revenue": 30000, "cost": 10000},
            "Base": {"investment": 150000, "revenue": 50000, "cost": 15000},
            "Optimistic": {"investment": 200000, "revenue": 80000, "cost": 20000}
        }
        
        df = scenario_comparison(scenarios, self.roi_model)
        
        # Check structure
        self.assertEqual(len(df), 3)
        self.assertIn('scenario', df.columns)
        self.assertIn('result', df.columns)
        
        # Verify scenario names
        self.assertListEqual(
            df['scenario'].tolist(), 
            ['Conservative', 'Base', 'Optimistic']
        )
        
        # Results should be different
        self.assertNotEqual(df['result'].iloc[0], df['result'].iloc[1])
        
    def test_scenario_comparison_with_metrics(self):
        """Test scenario comparison with specific metrics."""
        def complex_model(investment, revenue, cost):
            roi = (revenue - cost) / investment
            payback = investment / (revenue - cost)
            return {
                'roi': roi,
                'payback': payback,
                'profit': revenue - cost
            }
        
        scenarios = {
            "Scenario A": {"investment": 100000, "revenue": 50000, "cost": 20000},
            "Scenario B": {"investment": 150000, "revenue": 70000, "cost": 25000}
        }
        
        df = scenario_comparison(
            scenarios, complex_model, 
            metrics_to_compare=['roi', 'payback']
        )
        
        # Should only have requested metrics
        self.assertIn('roi', df.columns)
        self.assertIn('payback', df.columns)
        self.assertEqual(len(df.columns), 3)  # scenario + 2 metrics
        
    def test_tornado_chart_data(self):
        """Test tornado chart data creation."""
        # Create sample sensitivity results
        sensitivity_results = {
            'base_result': 100,
            'var1': {
                'values': [
                    {'result': 80}, {'result': 90}, {'result': 100}, 
                    {'result': 110}, {'result': 120}
                ],
                'elasticity': 1.5
            },
            'var2': {
                'values': [
                    {'result': 95}, {'result': 97}, {'result': 100}, 
                    {'result': 103}, {'result': 105}
                ],
                'elasticity': 0.5
            }
        }
        
        tornado_data = create_scenario_tornado_chart(sensitivity_results)
        
        # Check structure
        self.assertEqual(tornado_data['base_result'], 100)
        self.assertEqual(len(tornado_data['data']), 2)
        
        # Should be sorted by range (var1 should be first)
        self.assertEqual(tornado_data['data'][0]['variable'], 'var1')
        self.assertEqual(tornado_data['data'][0]['range'], 40)  # 120 - 80
        
        # Check deviations
        self.assertEqual(tornado_data['data'][0]['min_deviation'], -20)  # 80 - 100
        self.assertEqual(tornado_data['data'][0]['max_deviation'], 20)   # 120 - 100
        
    def test_tornado_chart_with_names(self):
        """Test tornado chart with variable name mapping."""
        sensitivity_results = {
            'base_result': 50,
            'inv': {'values': [{'result': 40}, {'result': 60}], 'elasticity': 1.0},
            'rev': {'values': [{'result': 45}, {'result': 55}], 'elasticity': 0.5}
        }
        
        variable_names = {'inv': 'Investment', 'rev': 'Revenue'}
        tornado_data = create_scenario_tornado_chart(sensitivity_results, variable_names)
        
        # Should use display names
        variables = [d['variable'] for d in tornado_data['data']]
        self.assertIn('Investment', variables)
        self.assertIn('Revenue', variables)
        
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        # Empty variables list for Monte Carlo
        results = monte_carlo_simulation(
            {"x": 10}, [], lambda x: x, iterations=100
        )
        # Should return base case result
        self.assertEqual(results['mean'], 10)
        
        # Zero variation in sensitivity analysis
        base_case = {"x": 100}
        results = sensitivity_analysis(
            base_case, ["x"], lambda x: x, variation_pct=0.0
        )
        # Elasticity should be undefined or 0
        self.assertEqual(results['x']['elasticity'], 0)
        
        # Single time period S-curve
        curve = adoption_s_curve(1)
        self.assertEqual(len(curve), 1)
        
        # Empty technology list
        matrix = technology_correlation_matrix([])
        self.assertEqual(matrix.shape, (0, 0))


if __name__ == '__main__':
    unittest.main(verbosity=2)