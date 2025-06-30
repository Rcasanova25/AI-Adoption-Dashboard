#!/usr/bin/env python3
"""
Test Chart Optimization System

This script tests the chart optimization features to ensure they work correctly.
"""

import unittest
import pandas as pd
import numpy as np
import time
from datetime import datetime
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from performance.chart_optimization import (
    ChartConfig,
    DataDownsampler,
    ChartOptimizer,
    LazyChartLoader,
    OptimizedCharts
)

class TestChartOptimization(unittest.TestCase):
    """Test cases for chart optimization system"""
    
    def setUp(self):
        """Set up test data"""
        # Create test dataset
        dates = pd.date_range('2020-01-01', periods=10000, freq='D')
        self.test_data = pd.DataFrame({
            'date': dates,
            'value': np.cumsum(np.random.randn(10000)) + 100,
            'trend': np.linspace(50, 150, 10000) + np.random.randn(10000) * 10,
            'category': np.random.choice(['A', 'B', 'C', 'D'], 10000),
            'size': np.random.randint(10, 100, 10000)
        })
        
        # Create chart optimizer
        self.config = ChartConfig(max_points=1000, enable_webgl=True)
        self.optimizer = ChartOptimizer(self.config)
        self.charts = OptimizedCharts(self.optimizer)
    
    def test_chart_config(self):
        """Test ChartConfig initialization"""
        config = ChartConfig()
        self.assertEqual(config.max_points, 5000)
        self.assertEqual(config.downsampling_method, "lttb")
        self.assertTrue(config.enable_webgl)
        self.assertTrue(config.optimize_layout)
        self.assertTrue(config.lazy_loading)
        self.assertTrue(config.cache_charts)
        self.assertTrue(config.compression)
        
        # Test custom config
        custom_config = ChartConfig(
            max_points=2000,
            downsampling_method="random",
            enable_webgl=False
        )
        self.assertEqual(custom_config.max_points, 2000)
        self.assertEqual(custom_config.downsampling_method, "random")
        self.assertFalse(custom_config.enable_webgl)
    
    def test_data_downsampler_lttb(self):
        """Test LTTB downsampling"""
        # Test with small dataset (no downsampling needed)
        small_data = self.test_data.head(500)
        result = DataDownsampler.largest_triangle_three_buckets(
            small_data, 'date', 'value', 1000
        )
        self.assertEqual(len(result), len(small_data))
        
        # Test with large dataset
        large_data = self.test_data.head(5000)
        result = DataDownsampler.largest_triangle_three_buckets(
            large_data, 'date', 'value', 1000
        )
        self.assertEqual(len(result), 1000)
        self.assertTrue(result['date'].iloc[0] == large_data['date'].iloc[0])
        self.assertTrue(result['date'].iloc[-1] == large_data['date'].iloc[-1])
    
    def test_data_downsampler_random(self):
        """Test random downsampling"""
        large_data = self.test_data.head(5000)
        result = DataDownsampler.random_sampling(large_data, 1000)
        self.assertEqual(len(result), 1000)
        self.assertTrue(result['date'].iloc[0] == large_data['date'].iloc[0])
        self.assertTrue(result['date'].iloc[-1] == large_data['date'].iloc[-1])
    
    def test_data_downsampler_every_nth(self):
        """Test every nth downsampling"""
        large_data = self.test_data.head(5000)
        result = DataDownsampler.every_nth_sampling(large_data, 1000)
        self.assertEqual(len(result), 1000)
        self.assertTrue(result['date'].iloc[0] == large_data['date'].iloc[0])
        self.assertTrue(result['date'].iloc[-1] == large_data['date'].iloc[-1])
    
    def test_data_downsampler_class_method(self):
        """Test the class method for downsampling"""
        large_data = self.test_data.head(5000)
        
        # Test LTTB
        result_lttb = DataDownsampler.downsample(
            large_data, 'date', 'value', 1000, 'lttb'
        )
        self.assertEqual(len(result_lttb), 1000)
        
        # Test random
        result_random = DataDownsampler.downsample(
            large_data, 'date', 'value', 1000, 'random'
        )
        self.assertEqual(len(result_random), 1000)
        
        # Test every_nth
        result_every_nth = DataDownsampler.downsample(
            large_data, 'date', 'value', 1000, 'every_nth'
        )
        self.assertEqual(len(result_every_nth), 1000)
        
        # Test invalid method
        with self.assertRaises(ValueError):
            DataDownsampler.downsample(
                large_data, 'date', 'value', 1000, 'invalid_method'
            )
    
    def test_chart_optimizer_initialization(self):
        """Test ChartOptimizer initialization"""
        optimizer = ChartOptimizer()
        self.assertIsNotNone(optimizer.config)
        self.assertEqual(optimizer.config.max_points, 5000)
        self.assertIsInstance(optimizer.chart_cache, dict)
        self.assertIsInstance(optimizer.performance_stats, dict)
    
    def test_chart_optimizer_optimize_layout(self):
        """Test layout optimization"""
        import plotly.graph_objects as go
        
        # Create a simple figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
        
        # Optimize layout
        optimized_fig = self.optimizer.optimize_layout(fig)
        
        # Check that optimizations were applied
        self.assertIn('transition', optimized_fig.layout)
        self.assertIn('margin', optimized_fig.layout)
        self.assertIn('hovermode', optimized_fig.layout)
    
    def test_chart_optimizer_optimize_traces(self):
        """Test trace optimization"""
        import plotly.graph_objects as go
        
        # Create a figure with large dataset
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(2000)),
            y=list(range(2000)),
            mode='lines+markers'
        ))
        
        # Optimize traces
        optimized_fig = self.optimizer.optimize_traces(fig, 2000)
        
        # Check that optimizations were applied
        trace = optimized_fig.data[0]
        if hasattr(trace, 'marker') and trace.marker:
            self.assertLessEqual(trace.marker.size, 6)  # Should be reduced for large datasets
    
    def test_chart_optimizer_create_optimized_chart(self):
        """Test optimized chart creation"""
        def simple_chart_func(data, **kwargs):
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['date'],
                y=data['value'],
                mode='lines'
            ))
            return fig
        
        # Create optimized chart
        fig = self.optimizer.create_optimized_chart(
            simple_chart_func,
            self.test_data.head(5000),
            "test_chart"
        )
        
        # Check that chart was created
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)
        
        # Check performance stats
        self.assertIn("test_chart", self.optimizer.performance_stats)
        stats = self.optimizer.performance_stats["test_chart"]
        self.assertIn('execution_time', stats)
        self.assertIn('original_points', stats)
        self.assertIn('rendered_points', stats)
    
    def test_chart_optimizer_cache(self):
        """Test chart caching"""
        def simple_chart_func(data, **kwargs):
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['date'], y=data['value']))
            return fig
        
        # Create chart twice
        fig1 = self.optimizer.create_optimized_chart(
            simple_chart_func,
            self.test_data.head(1000),
            "cache_test"
        )
        
        fig2 = self.optimizer.create_optimized_chart(
            simple_chart_func,
            self.test_data.head(1000),
            "cache_test"
        )
        
        # Both should be the same (cached)
        self.assertEqual(fig1, fig2)
    
    def test_chart_optimizer_performance_report(self):
        """Test performance report generation"""
        # Create some charts first
        def simple_chart_func(data, **kwargs):
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['date'], y=data['value']))
            return fig
        
        self.optimizer.create_optimized_chart(
            simple_chart_func,
            self.test_data.head(1000),
            "report_test"
        )
        
        # Get performance report
        report = self.optimizer.get_performance_report()
        
        # Check report structure
        self.assertIn('total_charts', report)
        self.assertIn('average_render_time', report)
        self.assertIn('cache_hits', report)
        self.assertIn('performance_breakdown', report)
        
        self.assertGreater(report['total_charts'], 0)
        self.assertGreaterEqual(report['average_render_time'], 0)
    
    def test_lazy_chart_loader(self):
        """Test lazy chart loader"""
        loader = LazyChartLoader()
        
        # Test registration
        def test_chart_func():
            import plotly.graph_objects as go
            return go.Figure()
        
        loader.register_chart("test_chart", test_chart_func)
        self.assertIn("test_chart", loader.chart_queue)
        
        # Test loading
        fig = loader.load_chart_on_demand("test_chart")
        self.assertIsNotNone(fig)
        self.assertIn("test_chart", loader.loaded_charts)
        
        # Test non-existent chart
        fig = loader.load_chart_on_demand("non_existent")
        self.assertIsNone(fig)
    
    def test_optimized_charts_time_series(self):
        """Test optimized time series chart creation"""
        fig = self.charts.create_time_series(
            self.test_data.head(2000),
            'date',
            ['value', 'trend'],
            "Test Time Series"
        )
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 2)  # Two traces for two y columns
    
    def test_optimized_charts_bar_chart(self):
        """Test optimized bar chart creation"""
        # Create aggregated data for bar chart
        bar_data = self.test_data.groupby('category').agg({
            'value': 'sum'
        }).reset_index()
        
        fig = self.charts.create_bar_chart(
            bar_data,
            'category',
            'value',
            "Test Bar Chart"
        )
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)  # One trace for bar chart
    
    def test_optimized_charts_scatter_plot(self):
        """Test optimized scatter plot creation"""
        fig = self.charts.create_scatter_plot(
            self.test_data.head(1000),
            'value',
            'trend',
            size_col='size',
            color_col='size',
            title="Test Scatter Plot"
        )
        
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)  # One trace for scatter plot
    
    def test_performance_improvement(self):
        """Test that optimization actually improves performance"""
        def simple_chart_func(data, **kwargs):
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['date'], y=data['value']))
            return fig
        
        # Test with large dataset
        large_data = self.test_data.head(10000)
        
        # Time optimized version
        start_time = time.time()
        optimized_fig = self.optimizer.create_optimized_chart(
            simple_chart_func,
            large_data,
            "performance_test"
        )
        optimized_time = time.time() - start_time
        
        # Time unoptimized version
        start_time = time.time()
        unoptimized_fig = simple_chart_func(large_data)
        unoptimized_time = time.time() - start_time
        
        # Optimized should be faster or at least not significantly slower
        # (accounting for overhead of optimization)
        self.assertLessEqual(optimized_time, unoptimized_time * 1.5)
    
    def test_data_integrity(self):
        """Test that downsampling preserves data integrity"""
        # Test that downsampling preserves first and last points
        large_data = self.test_data.head(5000)
        
        for method in ['lttb', 'random', 'every_nth']:
            downsampled = DataDownsampler.downsample(
                large_data, 'date', 'value', 1000, method
            )
            
            # Check first and last points are preserved
            self.assertEqual(downsampled['date'].iloc[0], large_data['date'].iloc[0])
            self.assertEqual(downsampled['date'].iloc[-1], large_data['date'].iloc[-1])
            
            # Check data is sorted
            self.assertTrue(downsampled['date'].is_monotonic_increasing)

def run_performance_benchmark():
    """Run a performance benchmark"""
    print("🚀 Running Chart Optimization Performance Benchmark")
    print("=" * 60)
    
    # Create test data
    dates = pd.date_range('2020-01-01', periods=50000, freq='D')
    test_data = pd.DataFrame({
        'date': dates,
        'value': np.cumsum(np.random.randn(50000)) + 100,
        'trend': np.linspace(50, 150, 50000) + np.random.randn(50000) * 10
    })
    
    # Test different dataset sizes
    sizes = [1000, 5000, 10000, 25000, 50000]
    
    print(f"{'Size':<8} {'Original':<12} {'Optimized':<12} {'Improvement':<12}")
    print("-" * 60)
    
    for size in sizes:
        data = test_data.head(size)
        
        # Time original
        start_time = time.time()
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['date'], y=data['value']))
        original_time = time.time() - start_time
        
        # Time optimized
        config = ChartConfig(max_points=5000)
        optimizer = ChartOptimizer(config)
        charts = OptimizedCharts(optimizer)
        
        start_time = time.time()
        optimized_fig = charts.create_time_series(
            data, 'date', ['value'], "Test"
        )
        optimized_time = time.time() - start_time
        
        improvement = ((original_time - optimized_time) / original_time) * 100
        
        print(f"{size:<8} {original_time:<12.3f} {optimized_time:<12.3f} {improvement:<12.1f}%")
    
    print("=" * 60)
    print("✅ Performance benchmark completed!")

if __name__ == "__main__":
    # Run unit tests
    print("🧪 Running Chart Optimization Tests")
    print("=" * 50)
    
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    
    # Run performance benchmark
    run_performance_benchmark() 