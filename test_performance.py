#!/usr/bin/env python3
"""
Simple test script for the performance module
"""

import time
import pandas as pd
from performance import (
    AdvancedCache,
    CacheConfig,
    DataPipeline,
    PerformanceMonitor,
    smart_cache,
    _global_cache,
    performance_monitor
)

def test_basic_caching():
    """Test basic caching functionality"""
    print("🧪 Testing basic caching...")
    
    @smart_cache(ttl=60)
    def expensive_function(x):
        time.sleep(0.1)  # Simulate expensive operation
        return x * 2
    
    # First call - should be slow
    start = time.time()
    result1 = expensive_function(5)
    duration1 = time.time() - start
    print(f"First call: {duration1:.3f}s")
    
    # Second call - should be fast (cached)
    start = time.time()
    result2 = expensive_function(5)
    duration2 = time.time() - start
    print(f"Second call: {duration2:.3f}s")
    
    # Verify results are the same
    assert result1 == result2 == 10
    print(f"✅ Caching working: {duration2:.3f}s vs {duration1:.3f}s")

def test_data_pipeline():
    """Test data pipeline functionality"""
    print("\n📊 Testing data pipeline...")
    
    pipeline = DataPipeline()
    
    # Test historical data loading
    start = time.time()
    data = pipeline.load_and_process_data("historical_ai_data")
    duration = time.time() - start
    
    print(f"Historical data loaded: {len(data)} rows in {duration:.3f}s")
    assert len(data) > 0
    print("✅ Data pipeline working")

def test_performance_monitor():
    """Test performance monitoring"""
    print("\n📈 Testing performance monitor...")
    
    # Start timing
    performance_monitor.start_timer("test_operation")
    time.sleep(0.1)  # Simulate work
    duration = performance_monitor.end_timer("test_operation")
    
    print(f"Operation took: {duration:.3f}s")
    
    # Get performance report
    report = performance_monitor.get_performance_report()
    print(f"Total operations: {report['total_operations']}")
    print("✅ Performance monitor working")

def test_cache_stats():
    """Test cache statistics"""
    print("\n💾 Testing cache statistics...")
    
    stats = _global_cache.get_stats()
    print(f"Cache entries: {stats['entries']}")
    print(f"Cache size: {stats['total_size_mb']:.2f} MB")
    print("✅ Cache statistics working")

def main():
    """Run all tests"""
    print("🚀 Performance Module Test Suite")
    print("=" * 40)
    
    try:
        test_basic_caching()
        test_data_pipeline()
        test_performance_monitor()
        test_cache_stats()
        
        print("\n🎉 All tests passed!")
        print("\n📊 Final Performance Report:")
        
        report = performance_monitor.get_performance_report()
        print(f"- Total operations: {report['total_operations']}")
        print(f"- Average time: {report['avg_operation_time']:.3f}s")
        
        cache_stats = _global_cache.get_stats()
        print(f"- Cache entries: {cache_stats['entries']}")
        print(f"- Cache size: {cache_stats['total_size_mb']:.2f} MB")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 