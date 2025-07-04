"""Performance tests for dashboard load times."""

import pytest
import time
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import memory_profiler

from data.data_manager import DataManager
from data.loaders.ai_index import AIIndexLoader
from components.economic_insights import EconomicInsights
from components.key_takeaways import KeyTakeawaysGenerator
from tests.fixtures.mock_data import generate_adoption_data, generate_industry_data
from tests.utils.test_helpers import PerformanceTimer


class TestLoadTimePerformance:
    """Test suite for load time performance benchmarks."""
    
    @pytest.fixture
    def performance_thresholds(self):
        """Performance thresholds based on APPDEV.md requirements."""
        return {
            'data_load_time': 1.0,      # 1 second max for data loading
            'view_render_time': 0.5,    # 0.5 seconds max for view rendering  
            'dashboard_init_time': 3.0,  # 3 seconds max for dashboard initialization
            'component_init_time': 0.1,  # 0.1 seconds max per component
            'chart_render_time': 0.3,    # 0.3 seconds max for chart rendering
        }
    
    @pytest.fixture
    def large_dataset(self):
        """Generate large dataset for performance testing."""
        # Generate 3 years of daily data
        dates = pd.date_range(start='2022-01-01', end='2024-12-31', freq='D')
        return pd.DataFrame({
            'date': dates,
            'adoption_rate': np.random.uniform(50, 95, len(dates)),
            'investment': np.random.uniform(100000, 1000000, len(dates)),
            'productivity_gain': np.random.uniform(5, 30, len(dates)),
            'employee_count': np.random.randint(100, 10000, len(dates)),
            'revenue': np.random.uniform(1000000, 10000000, len(dates))
        })
    
    def test_data_manager_initialization_time(self, performance_thresholds):
        """Test DataManager initialization performance."""
        with PerformanceTimer("DataManager initialization") as timer:
            manager = DataManager()
        
        timer.assert_faster_than(performance_thresholds['component_init_time'])
    
    @patch('data.loaders.ai_index.PDFExtractor')
    def test_single_loader_performance(self, mock_extractor, performance_thresholds):
        """Test single data loader performance."""
        # Setup mock
        mock_extractor.return_value.extract_text.return_value = "Test data"
        mock_extractor.return_value.extract_tables.return_value = [
            generate_adoption_data(100)  # 100 months of data
        ]
        
        # Test load time
        with PerformanceTimer("Single loader") as timer:
            loader = AIIndexLoader(Mock())
            data = loader.load()
        
        timer.assert_faster_than(performance_thresholds['data_load_time'])
        assert 'adoption_rates' in data
    
    def test_multiple_loader_performance(self, performance_thresholds):
        """Test loading data from multiple sources concurrently."""
        manager = DataManager()
        
        # Mock multiple loaders
        for i in range(5):
            mock_loader = Mock()
            mock_loader.load.return_value = {
                'data': generate_adoption_data(50)
            }
            manager.loaders[f'source_{i}'] = mock_loader
        
        # Test concurrent loading
        with PerformanceTimer("Multiple loaders") as timer:
            all_data = manager.get_all_data()
        
        # Should complete within reasonable time even with 5 sources
        timer.assert_faster_than(performance_thresholds['data_load_time'] * 2)
        assert len(all_data) == 5
    
    def test_cache_performance(self, performance_thresholds):
        """Test cache hit performance."""
        manager = DataManager()
        
        # Setup mock loader
        mock_loader = Mock()
        mock_loader.load.return_value = {'data': generate_adoption_data(100)}
        manager.loaders['test'] = mock_loader
        
        # First load (cache miss)
        with PerformanceTimer("First load (cache miss)") as timer1:
            data1 = manager.get_data('test')
        
        # Second load (cache hit)
        with PerformanceTimer("Second load (cache hit)") as timer2:
            data2 = manager.get_data('test')
        
        # Cache hit should be at least 10x faster
        assert timer2.duration < timer1.duration / 10
        assert timer2.duration < 0.01  # Should be near instant
    
    def test_large_dataframe_processing(self, large_dataset, performance_thresholds):
        """Test processing performance with large datasets."""
        # Test filtering
        with PerformanceTimer("Large dataset filtering") as timer:
            filtered = large_dataset[large_dataset['adoption_rate'] > 80]
        
        timer.assert_faster_than(0.1)
        
        # Test aggregation
        with PerformanceTimer("Large dataset aggregation") as timer:
            monthly_avg = large_dataset.resample('M', on='date').mean()
        
        timer.assert_faster_than(0.2)
    
    def test_takeaway_generation_performance(self, performance_thresholds):
        """Test key takeaway generation performance."""
        generator = KeyTakeawaysGenerator()
        
        # Generate takeaways for large dataset
        test_data = {
            'current_adoption': 87.3,
            'yoy_growth': 15.2,
            'industry_average': 72.5,
            'competitors': list(range(100)),  # 100 competitors
            'metrics': {f'metric_{i}': np.random.rand() for i in range(50)}
        }
        
        with PerformanceTimer("Takeaway generation") as timer:
            takeaways = generator.generate_takeaways('adoption_rates', test_data)
        
        timer.assert_faster_than(performance_thresholds['view_render_time'])
        assert len(takeaways) <= 3  # Should return top 3
    
    @patch('streamlit.plotly_chart')
    def test_chart_rendering_performance(self, mock_chart, large_dataset, performance_thresholds):
        """Test chart rendering performance."""
        import plotly.graph_objects as go
        
        # Create complex chart with large dataset
        with PerformanceTimer("Chart creation") as timer:
            fig = go.Figure()
            
            # Add multiple traces
            for col in ['adoption_rate', 'productivity_gain']:
                fig.add_trace(go.Scatter(
                    x=large_dataset['date'],
                    y=large_dataset[col],
                    mode='lines',
                    name=col
                ))
            
            # Add layout
            fig.update_layout(
                title="Performance Test Chart",
                xaxis_title="Date",
                yaxis_title="Value",
                height=600
            )
        
        timer.assert_faster_than(performance_thresholds['chart_render_time'])
    
    def test_concurrent_user_simulation(self, performance_thresholds):
        """Simulate multiple concurrent users accessing data."""
        import threading
        import queue
        
        manager = DataManager()
        results = queue.Queue()
        
        # Mock loader
        mock_loader = Mock()
        mock_loader.load.return_value = {'data': generate_adoption_data(50)}
        manager.loaders['test'] = mock_loader
        
        def user_request():
            start = time.time()
            data = manager.get_data('test')
            duration = time.time() - start
            results.put(duration)
        
        # Simulate 10 concurrent users
        threads = []
        with PerformanceTimer("10 concurrent users") as timer:
            for _ in range(10):
                t = threading.Thread(target=user_request)
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
        
        # Check individual request times
        max_request_time = 0
        while not results.empty():
            request_time = results.get()
            max_request_time = max(max_request_time, request_time)
        
        # Even under load, requests should complete quickly
        assert max_request_time < performance_thresholds['data_load_time']
    
    @pytest.mark.benchmark
    def test_memory_usage_data_loading(self, large_dataset):
        """Test memory usage during data loading."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Load large dataset multiple times
        datasets = []
        for _ in range(5):
            datasets.append(large_dataset.copy())
        
        # Check memory after loading
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - baseline_memory
        
        # Should not exceed 500MB increase (from performance_threshold fixture)
        assert memory_increase < 500, f"Memory increased by {memory_increase}MB"
        
        # Cleanup
        datasets.clear()
    
    def test_dashboard_cold_start(self, performance_thresholds):
        """Test complete dashboard initialization time."""
        with PerformanceTimer("Dashboard cold start") as timer:
            # Simulate dashboard initialization
            manager = DataManager()
            
            # Initialize components
            insights = EconomicInsights()
            generator = KeyTakeawaysGenerator()
            
            # Load initial data
            manager._initialize_loaders()
        
        timer.assert_faster_than(performance_thresholds['dashboard_init_time'])
    
    @pytest.mark.parametrize("num_metrics", [10, 50, 100, 500])
    def test_metric_display_scaling(self, num_metrics, performance_thresholds):
        """Test performance with varying numbers of metrics."""
        # Generate metrics
        metrics = {
            f'metric_{i}': {
                'value': np.random.rand() * 100,
                'delta': np.random.rand() * 10 - 5,
                'label': f'Test Metric {i}'
            }
            for i in range(num_metrics)
        }
        
        with PerformanceTimer(f"Display {num_metrics} metrics") as timer:
            # Simulate metric rendering
            for metric_id, metric_data in metrics.items():
                # Simulate streamlit metric call
                rendered = f"{metric_data['label']}: {metric_data['value']:.2f}"
        
        # Should scale linearly or better
        max_time = performance_thresholds['component_init_time'] * (num_metrics / 10)
        timer.assert_faster_than(max_time)