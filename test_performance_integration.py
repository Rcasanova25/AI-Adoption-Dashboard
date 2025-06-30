#!/usr/bin/env python3
"""
Test Performance Integration System
Verify all components are working correctly
"""

import time
import pandas as pd
import numpy as np
from datetime import datetime

def test_performance_integration():
    """Test all performance integration components"""
    
    print("🚀 Testing Performance Integration System")
    print("=" * 50)
    
    # Test 1: Import all modules
    print("\n1. Testing Imports...")
    try:
        from performance.caching import AdvancedCache, smart_cache
        from performance.chart_optimization import ChartOptimizer, OptimizedCharts, ChartConfig
        from performance.memory_management import MemoryMonitor, DataFrameOptimizer
        from performance.integration import PerformanceIntegrator, PerformanceConfig
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Initialize components
    print("\n2. Testing Component Initialization...")
    try:
        cache = AdvancedCache()
        memory_monitor = MemoryMonitor()
        chart_optimizer = ChartOptimizer(ChartConfig())
        charts = OptimizedCharts(chart_optimizer)
        integrator = PerformanceIntegrator()
        print("✅ All components initialized successfully")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False
    
    # Test 3: Test caching
    print("\n3. Testing Caching System...")
    try:
        @smart_cache(ttl=60)
        def test_function(x):
            time.sleep(0.1)  # Simulate work
            return x * 2
        
        # First call (should be slow)
        start_time = time.time()
        result1 = test_function(5)
        first_call_time = time.time() - start_time
        
        # Second call (should be fast due to cache)
        start_time = time.time()
        result2 = test_function(5)
        second_call_time = time.time() - start_time
        
        if result1 == result2 == 10 and second_call_time < first_call_time:
            print(f"✅ Caching working: {first_call_time:.3f}s -> {second_call_time:.3f}s")
        else:
            print("❌ Caching not working correctly")
            return False
    except Exception as e:
        print(f"❌ Caching error: {e}")
        return False
    
    # Test 4: Test memory optimization
    print("\n4. Testing Memory Optimization...")
    try:
        # Create large DataFrame
        large_df = pd.DataFrame({
            'int_col': np.random.randint(0, 1000, 10000),
            'float_col': np.random.randn(10000),
            'string_col': np.random.choice(['A', 'B', 'C'], 10000),
            'bool_col': np.random.choice([True, False], 10000)
        })
        
        original_memory = large_df.memory_usage(deep=True).sum() / 1024 / 1024
        
        # Optimize DataFrame
        optimized_df, report = DataFrameOptimizer.optimize_dtypes(large_df)
        
        optimized_memory = optimized_df.memory_usage(deep=True).sum() / 1024 / 1024
        memory_saved = original_memory - optimized_memory
        
        if memory_saved > 0:
            print(f"✅ Memory optimization working: {original_memory:.2f}MB -> {optimized_memory:.2f}MB (saved {memory_saved:.2f}MB)")
        else:
            print("❌ Memory optimization not working")
            return False
    except Exception as e:
        print(f"❌ Memory optimization error: {e}")
        return False
    
    # Test 5: Test chart optimization
    print("\n5. Testing Chart Optimization...")
    try:
        # Create test data
        test_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=1000, freq='D'),
            'value': np.random.randn(1000).cumsum()
        })
        
        # Create optimized chart
        fig = charts.create_time_series(
            test_data, 'date', ['value'],
            title="Test Chart"
        )
        
        if fig is not None:
            print("✅ Chart optimization working")
        else:
            print("❌ Chart optimization failed")
            return False
    except Exception as e:
        print(f"❌ Chart optimization error: {e}")
        return False
    
    # Test 6: Test database optimization
    print("\n6. Testing Database Optimization...")
    try:
        # Create sample database
        integrator.db_optimizer.create_sample_database()
        
        # Execute test query
        query = "SELECT COUNT(*) as count FROM ai_adoption"
        result = integrator.db_optimizer.execute_optimized_query(query, query_name="test_query")
        
        if not result.empty and result['count'].iloc[0] > 0:
            print("✅ Database optimization working")
        else:
            print("❌ Database optimization failed")
            return False
    except Exception as e:
        print(f"❌ Database optimization error: {e}")
        return False
    
    # Test 7: Test performance monitoring
    print("\n7. Testing Performance Monitoring...")
    try:
        # Get memory report
        memory_report = memory_monitor.get_memory_report()
        
        # Get cache stats
        cache_stats = cache.get_stats()
        
        if memory_report and cache_stats:
            print("✅ Performance monitoring working")
            print(f"   - Memory: {memory_report['current_memory']['rss_mb']:.0f}MB")
            print(f"   - Cache entries: {cache_stats['entries']}")
        else:
            print("❌ Performance monitoring failed")
            return False
    except Exception as e:
        print(f"❌ Performance monitoring error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! Performance Integration System is working correctly.")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = test_performance_integration()
    if success:
        print("\n🚀 Ready to run performance integration demos!")
        print("   - Full demo: python -m streamlit run performance_integration_demo.py --server.port 8552")
        print("   - Simple demo: python -m streamlit run simple_integration_demo.py --server.port 8553")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 