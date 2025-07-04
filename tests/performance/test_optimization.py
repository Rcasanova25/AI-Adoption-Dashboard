"""Performance tests for optimization features."""

import pytest
import time
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import threading
import concurrent.futures

from performance.cache_manager import MultiLayerCache, TTLCache, DiskCache, CacheKeyGenerator
from performance.monitor import PerformanceMetrics, track_performance, PerformanceContext
from data.optimized_data_manager import OptimizedDataManager, LazyDataLoader
from tests.fixtures.mock_data import generate_adoption_data, generate_industry_data
from tests.utils.test_helpers import PerformanceTimer


class TestCachePerformance:
    """Test cache system performance."""
    
    @pytest.fixture
    def cache(self, tmp_path):
        """Create test cache instance."""
        return MultiLayerCache(
            memory_size=100,
            memory_ttl=60,
            disk_dir=str(tmp_path / "cache"),
            disk_size=10 * 1024 * 1024  # 10MB
        )
    
    def test_memory_cache_performance(self):
        """Test TTL cache performance."""
        cache = TTLCache(maxsize=1000, ttl=300)
        
        # Test write performance
        with PerformanceTimer("1000 cache writes") as timer:
            for i in range(1000):
                cache.set(f"key_{i}", f"value_{i}")
        
        timer.assert_faster_than(0.1)  # Should be very fast
        
        # Test read performance
        with PerformanceTimer("1000 cache reads") as timer:
            for i in range(1000):
                value = cache.get(f"key_{i}")
                assert value == f"value_{i}"
        
        timer.assert_faster_than(0.05)  # Reads should be faster
        
        # Test cache hit rate
        stats = cache.get_stats()
        assert stats['hit_rate'] == 1.0  # All hits
        assert stats['size'] == 1000
    
    def test_disk_cache_performance(self, tmp_path):
        """Test disk cache performance."""
        cache = DiskCache(cache_dir=str(tmp_path / "disk_cache"), size_limit=50 * 1024 * 1024)
        
        # Create test data
        large_data = pd.DataFrame({
            'col1': np.random.rand(10000),
            'col2': np.random.rand(10000),
            'col3': ['value'] * 10000
        })
        
        # Test write performance
        with PerformanceTimer("Large data disk write") as timer:
            cache.set("large_data", large_data, ttl=3600)
        
        timer.assert_faster_than(0.5)  # Reasonable for disk I/O
        
        # Test read performance
        with PerformanceTimer("Large data disk read") as timer:
            loaded_data = cache.get("large_data")
        
        timer.assert_faster_than(0.3)  # Should be faster than write
        
        # Verify data integrity
        pd.testing.assert_frame_equal(loaded_data, large_data)
    
    def test_multi_layer_cache_promotion(self, cache):
        """Test data promotion between cache layers."""
        test_data = {"key": "value", "data": list(range(1000))}
        
        # Write to disk only
        cache.set("test_key", test_data, disk_only=True)
        
        # First read (from disk)
        with PerformanceTimer("First read (disk)") as timer1:
            data1 = cache.get("test_key")
        
        # Second read (from memory - promoted)
        with PerformanceTimer("Second read (memory)") as timer2:
            data2 = cache.get("test_key")
        
        # Memory read should be much faster
        assert timer2.duration < timer1.duration / 10
        assert data1 == data2 == test_data
    
    def test_concurrent_cache_access(self, cache):
        """Test cache performance under concurrent access."""
        num_threads = 10
        operations_per_thread = 100
        
        def cache_operations(thread_id):
            """Perform cache operations."""
            for i in range(operations_per_thread):
                key = f"thread_{thread_id}_key_{i}"
                value = f"value_{i}"
                
                # Write
                cache.set(key, value)
                
                # Read
                retrieved = cache.get(key)
                assert retrieved == value
        
        # Run concurrent operations
        with PerformanceTimer(f"{num_threads} concurrent threads") as timer:
            threads = []
            for i in range(num_threads):
                thread = threading.Thread(target=cache_operations, args=(i,))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
        
        # Should handle concurrent access efficiently
        timer.assert_faster_than(2.0)
        
        # Verify cache stats
        stats = cache.get_stats()
        assert stats['memory']['size'] > 0


class TestOptimizedDataManager:
    """Test optimized data manager performance."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create test data manager."""
        return OptimizedDataManager(
            cache_memory_size=50,
            cache_memory_ttl=60,
            cache_disk_size=100 * 1024 * 1024
        )
    
    @patch('data.loaders.ai_index.PDFExtractor')
    def test_parallel_data_loading(self, mock_extractor, manager):
        """Test parallel loading performance."""
        # Setup mock loaders
        for i in range(5):
            mock_loader = Mock()
            mock_loader.load.return_value = {
                'data': generate_adoption_data(100)
            }
            # Simulate loading time
            mock_loader.load.side_effect = lambda: (
                time.sleep(0.1),  # Simulate I/O
                {'data': generate_adoption_data(100)}
            )[1]
            
            manager.loaders[f'source_{i}'] = mock_loader
        
        # Sequential loading baseline
        start = time.time()
        for source in manager.loaders:
            manager.get_data(source)
        sequential_time = time.time() - start
        
        # Clear cache
        manager.cache.clear()
        
        # Parallel loading
        with PerformanceTimer("Parallel data loading") as timer:
            results = manager.get_all_data_async()
        
        # Parallel should be significantly faster
        assert timer.duration < sequential_time / 2
        assert len(results) == 5
    
    def test_lazy_loading_performance(self):
        """Test lazy data loader performance."""
        # Mock loader class
        mock_loader_class = Mock()
        mock_instance = Mock()
        mock_instance.load.return_value = {'data': generate_adoption_data(1000)}
        mock_loader_class.return_value = mock_instance
        
        # Create lazy loader
        source = Mock(name="Test Source", type="csv", year=2024)
        lazy_loader = LazyDataLoader(mock_loader_class, source)
        
        # First access should load data
        with PerformanceTimer("First lazy load") as timer1:
            data1 = lazy_loader.load()
        
        # Verify loader was called
        assert mock_instance.load.called
        
        # Second access should be instant (cached)
        with PerformanceTimer("Second lazy load") as timer2:
            data2 = lazy_loader.load()
        
        # Should be much faster
        assert timer2.duration < timer1.duration / 100
        assert data1 == data2
    
    def test_memory_optimization(self, manager):
        """Test memory optimization features."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Load large datasets
        for i in range(10):
            large_df = pd.DataFrame({
                f'col_{j}': np.random.rand(100000)
                for j in range(10)
            })
            manager.cache.set(f"large_{i}", large_df)
        
        # Check memory usage
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        # Run optimization
        manager.optimize_memory()
        
        # Check memory after optimization
        optimized_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Should free some memory
        assert optimized_memory < peak_memory
        print(f"Memory freed: {peak_memory - optimized_memory:.1f} MB")


class TestPerformanceMonitoring:
    """Test performance monitoring system."""
    
    def test_performance_tracking_decorator(self):
        """Test performance tracking decorator."""
        metrics = PerformanceMetrics()
        
        @track_performance('test_operation', threshold=0.1)
        def slow_operation():
            time.sleep(0.15)
            return "result"
        
        # Monkey patch to use test metrics
        import performance.monitor
        original_get_metrics = performance.monitor.get_metrics
        performance.monitor.get_metrics = lambda: metrics
        
        try:
            # Run operation
            result = slow_operation()
            
            # Check metrics recorded
            stats = metrics.get_stats('test_operation')
            assert stats['count'] == 1
            assert stats['min'] >= 0.15
            assert stats['threshold'] == 0.1
            
            # Check slow operations detected
            slow_ops = metrics.get_slow_operations()
            assert len(slow_ops) == 1
            assert slow_ops[0]['operation'] == 'test_operation'
            
        finally:
            # Restore original
            performance.monitor.get_metrics = original_get_metrics
    
    def test_performance_context_manager(self):
        """Test performance context manager."""
        metrics = PerformanceMetrics()
        
        # Test successful operation
        with PerformanceContext('test_context', {'meta': 'data'}):
            time.sleep(0.05)
        
        # Manually record to test metrics
        metrics.record('test_context', 0.05, {'meta': 'data'})
        
        stats = metrics.get_stats('test_context')
        assert stats['count'] == 1
        assert stats['errors'] == 0
        
        # Test failed operation
        try:
            with PerformanceContext('test_error'):
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Record error
        metrics.record_error('test_error', "Test error")
        error_stats = metrics.get_stats('test_error')
        assert error_stats['errors'] == 1
    
    def test_metrics_aggregation(self):
        """Test metrics aggregation and percentiles."""
        metrics = PerformanceMetrics()
        
        # Record multiple measurements
        durations = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
        for duration in durations:
            metrics.record('test_op', duration)
        
        stats = metrics.get_stats('test_op')
        
        # Check aggregations
        assert stats['count'] == 10
        assert stats['min'] == 0.01
        assert stats['max'] == 0.10
        assert abs(stats['mean'] - 0.055) < 0.001
        assert stats['median'] == 0.055
        assert stats['p95'] >= 0.09
        assert stats['p99'] >= 0.10


class TestCacheKeyGeneration:
    """Test cache key generation."""
    
    def test_consistent_key_generation(self):
        """Test that keys are consistent for same params."""
        params1 = {'a': 1, 'b': 2, 'c': [1, 2, 3]}
        params2 = {'b': 2, 'a': 1, 'c': [1, 2, 3]}  # Different order
        
        key1 = CacheKeyGenerator.generate('test', params1)
        key2 = CacheKeyGenerator.generate('test', params2)
        
        # Should be same despite order
        assert key1 == key2
    
    def test_data_key_generation(self):
        """Test data-specific key generation."""
        key1 = CacheKeyGenerator.generate_data_key(
            source='ai_index',
            dataset='adoption_rates',
            filters={'year': 2024},
            version='v1'
        )
        
        key2 = CacheKeyGenerator.generate_data_key(
            source='ai_index',
            dataset='adoption_rates',
            filters={'year': 2025},  # Different filter
            version='v1'
        )
        
        # Should be different
        assert key1 != key2
        
        # Should have correct prefix
        assert key1.startswith('data:')
        assert key2.startswith('data:')


class TestRealWorldScenarios:
    """Test real-world performance scenarios."""
    
    def test_dashboard_cold_start_optimized(self, tmp_path):
        """Test optimized dashboard initialization."""
        # Create manager with cache
        manager = OptimizedDataManager(
            cache_memory_size=100,
            cache_disk_size=100 * 1024 * 1024
        )
        
        # Mock 10 data sources
        for i in range(10):
            mock_loader = Mock()
            mock_loader.load.return_value = {
                'adoption': generate_adoption_data(50),
                'industry': generate_industry_data()
            }
            manager.loaders[f'source_{i}'] = mock_loader
        
        # Cold start
        with PerformanceTimer("Optimized cold start") as timer:
            # Preload critical sources
            manager.preload_critical_data(['source_0', 'source_1', 'source_2'])
        
        # Should meet performance target
        timer.assert_faster_than(3.0)  # Dashboard init threshold
        
        # Verify data loaded
        assert 'source_0' in manager._loaded_sources
        assert 'source_1' in manager._loaded_sources
        assert 'source_2' in manager._loaded_sources
    
    @pytest.mark.parametrize("num_users", [1, 5, 10, 20])
    def test_concurrent_user_scalability(self, num_users, tmp_path):
        """Test system scalability with concurrent users."""
        manager = OptimizedDataManager()
        
        # Mock data source
        mock_loader = Mock()
        mock_loader.load.return_value = {'data': generate_adoption_data(100)}
        manager.loaders['test_source'] = mock_loader
        
        def simulate_user():
            """Simulate user accessing data."""
            # Each user makes 5 requests
            for _ in range(5):
                data = manager.get_data('test_source')
                assert 'data' in data
                time.sleep(0.01)  # Simulate think time
        
        # Run concurrent users
        with PerformanceTimer(f"{num_users} concurrent users") as timer:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
                futures = [executor.submit(simulate_user) for _ in range(num_users)]
                concurrent.futures.wait(futures)
        
        # Performance should scale reasonably
        # Allow 0.5s per user for linear scaling
        timer.assert_faster_than(num_users * 0.5)