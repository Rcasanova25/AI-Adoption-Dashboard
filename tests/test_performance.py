"""Performance tests for caching and parallel processing.

This module tests the performance improvements from caching
and parallel processing implementations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import unittest
from business.financial_calculations_cached import (
    calculate_npv,
    calculate_irr,
    get_cache_statistics,
    clear_calculation_cache
)
from business.scenario_engine import ScenarioVariable
from business.scenario_engine_parallel import (
    monte_carlo_simulation_parallel,
    sensitivity_analysis_parallel,
    get_optimal_process_count,
    estimate_simulation_time
)


class TestCachePerformance(unittest.TestCase):
    """Test cache performance improvements."""
    
    def setUp(self):
        """Clear cache before each test."""
        clear_calculation_cache()
        
    def test_npv_cache_performance(self):
        """Test NPV calculation caching performance."""
        cash_flows = [100000, 120000, 140000, 160000, 180000]
        discount_rate = 0.10
        investment = 500000
        
        # First calculation (cache miss)
        start_time = time.time()
        result1 = calculate_npv(cash_flows, discount_rate, investment)
        first_call_time = time.time() - start_time
        
        # Second calculation (cache hit)
        start_time = time.time()
        result2 = calculate_npv(cash_flows, discount_rate, investment)
        second_call_time = time.time() - start_time
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        # Second call should be significantly faster
        self.assertLess(second_call_time, first_call_time * 0.5)
        
        # Check cache statistics
        stats = get_cache_statistics()
        self.assertGreater(stats['npv']['hit_count'], 0)
        
        print(f"\nNPV Cache Performance:")
        print(f"  First call:  {first_call_time*1000:.2f}ms")
        print(f"  Second call: {second_call_time*1000:.2f}ms")
        print(f"  Speedup:     {first_call_time/second_call_time:.1f}x")
        
    def test_cache_hit_rate(self):
        """Test cache hit rate with multiple calculations."""
        # Perform various calculations
        test_cases = [
            ([50000, 60000, 70000], 0.08, 150000),
            ([80000, 90000, 100000], 0.10, 200000),
            ([50000, 60000, 70000], 0.08, 150000),  # Duplicate
            ([80000, 90000, 100000], 0.10, 200000),  # Duplicate
        ]
        
        for cash_flows, rate, investment in test_cases:
            calculate_npv(cash_flows, rate, investment)
            
        stats = get_cache_statistics()
        npv_stats = stats['npv']
        
        # Should have 50% hit rate (2 hits out of 4 calls)
        self.assertEqual(npv_stats['hit_count'] + npv_stats['miss_count'], 4)
        self.assertAlmostEqual(npv_stats['hit_rate'], 0.5, places=1)
        
        print(f"\nCache Hit Rate Test:")
        print(f"  Total calls: {npv_stats['hit_count'] + npv_stats['miss_count']}")
        print(f"  Cache hits:  {npv_stats['hit_count']}")
        print(f"  Hit rate:    {npv_stats['hit_rate']*100:.1f}%")


class TestParallelProcessing(unittest.TestCase):
    """Test parallel processing performance."""
    
    def test_monte_carlo_parallel_speedup(self):
        """Test parallel Monte Carlo simulation speedup."""
        # Simple test model
        def test_model(x, y):
            return x * y + x ** 2 - y ** 2
            
        base_case = {"x": 10, "y": 5}
        variables = [
            ScenarioVariable("x", 10, 5, 15, "uniform"),
            ScenarioVariable("y", 5, 2, 8, "uniform")
        ]
        
        # Test with different iteration counts
        iteration_counts = [1000, 5000]
        
        for iterations in iteration_counts:
            # Single process timing
            start_time = time.time()
            result_single = monte_carlo_simulation_parallel(
                base_case, variables, test_model, 
                iterations=iterations, n_processes=1
            )
            single_time = time.time() - start_time
            
            # Clear cache for fair comparison
            clear_calculation_cache()
            
            # Multi-process timing
            n_processes = min(4, get_optimal_process_count(iterations))
            start_time = time.time()
            result_multi = monte_carlo_simulation_parallel(
                base_case, variables, test_model,
                iterations=iterations, n_processes=n_processes
            )
            multi_time = time.time() - start_time
            
            # Results should be similar (allowing for randomness)
            self.assertAlmostEqual(
                result_single['mean'], 
                result_multi['mean'], 
                delta=abs(result_single['mean'] * 0.1)
            )
            
            speedup = single_time / multi_time if multi_time > 0 else 1.0
            
            print(f"\nMonte Carlo Parallel Performance ({iterations} iterations):")
            print(f"  Single process: {single_time:.2f}s")
            print(f"  {n_processes} processes:   {multi_time:.2f}s")
            print(f"  Speedup:        {speedup:.1f}x")
            
            # For larger simulations, expect some speedup
            if iterations >= 5000 and n_processes > 1:
                self.assertGreater(speedup, 1.2)
                
    def test_optimal_process_count(self):
        """Test optimal process count determination."""
        test_cases = [
            (500, 1),      # Small: single process
            (2000, 2),     # Medium: 2 processes
            (10000, 4),    # Large: 4 processes (capped)
            (50000, None), # Very large: all CPUs
        ]
        
        for iterations, expected_max in test_cases:
            optimal = get_optimal_process_count(iterations)
            
            if expected_max is not None:
                self.assertLessEqual(optimal, expected_max)
            
            print(f"Iterations: {iterations:6d} → {optimal} processes")
            
    def test_simulation_time_estimation(self):
        """Test simulation time estimation accuracy."""
        test_cases = [
            (1000, 2, "simple"),
            (5000, 4, "medium"),
            (10000, 6, "complex"),
        ]
        
        print("\nSimulation Time Estimates:")
        for iterations, vars, complexity in test_cases:
            estimated_time = estimate_simulation_time(
                iterations, vars, complexity
            )
            print(f"  {iterations:5d} iterations, {vars} vars, {complexity:7s}: "
                  f"{estimated_time:6.2f}s")
            
            # Basic sanity checks
            self.assertGreater(estimated_time, 0)
            self.assertLess(estimated_time, 600)  # Less than 10 minutes
            
    def test_cache_with_parallel(self):
        """Test that caching works with parallel processing."""
        def simple_model(a, b):
            return a + b
            
        base_case = {"a": 100, "b": 200}
        variables = [
            ScenarioVariable("a", 100, 50, 150, "uniform"),
            ScenarioVariable("b", 200, 100, 300, "uniform")
        ]
        
        # First run (cache miss)
        start_time = time.time()
        result1 = monte_carlo_simulation_parallel(
            base_case, variables, simple_model, iterations=2000
        )
        first_time = time.time() - start_time
        
        # Second run (cache hit)
        start_time = time.time()
        result2 = monte_carlo_simulation_parallel(
            base_case, variables, simple_model, iterations=2000
        )
        cache_time = time.time() - start_time
        
        # Should get exact same result from cache
        self.assertEqual(result1['iterations'], result2['iterations'])
        self.assertEqual(result1['mean'], result2['mean'])
        
        # Cache should be much faster
        self.assertLess(cache_time, first_time * 0.1)
        
        print(f"\nCache + Parallel Performance:")
        print(f"  First run:  {first_time:.3f}s")
        print(f"  Cache hit:  {cache_time:.3f}s")
        print(f"  Speedup:    {first_time/cache_time:.0f}x")


class TestPerformanceIntegration(unittest.TestCase):
    """Integration tests for performance features."""
    
    def test_end_to_end_performance(self):
        """Test end-to-end performance with caching and parallel processing."""
        # Complex financial model
        def financial_model(revenue, cost, growth_rate, discount_rate):
            years = 5
            npv = 0
            for year in range(years):
                annual_revenue = revenue * ((1 + growth_rate) ** year)
                annual_profit = annual_revenue - cost
                npv += annual_profit / ((1 + discount_rate) ** (year + 1))
            return npv
            
        base_case = {
            "revenue": 1000000,
            "cost": 600000,
            "growth_rate": 0.10,
            "discount_rate": 0.08
        }
        
        variables = [
            ScenarioVariable("revenue", 1000000, 800000, 1200000, "normal", std_dev=100000),
            ScenarioVariable("cost", 600000, 500000, 700000, "uniform"),
            ScenarioVariable("growth_rate", 0.10, 0.05, 0.15, "triangular", mode=0.10),
        ]
        
        print("\nEnd-to-End Performance Test:")
        
        # Run 1: No cache, establish baseline
        clear_calculation_cache()
        start_time = time.time()
        result1 = monte_carlo_simulation_parallel(
            base_case, variables, financial_model, 
            iterations=5000, n_processes=2
        )
        baseline_time = time.time() - start_time
        print(f"  Baseline (no cache): {baseline_time:.2f}s")
        
        # Run 2: With cache
        start_time = time.time()
        result2 = monte_carlo_simulation_parallel(
            base_case, variables, financial_model, 
            iterations=5000, n_processes=2
        )
        cached_time = time.time() - start_time
        print(f"  With cache:          {cached_time:.2f}s")
        print(f"  Cache speedup:       {baseline_time/cached_time:.0f}x")
        
        # Verify results are identical (from cache)
        self.assertEqual(result1['mean'], result2['mean'])
        
        # Cache should provide massive speedup
        self.assertLess(cached_time, baseline_time * 0.1)


if __name__ == '__main__':
    unittest.main(verbosity=2)