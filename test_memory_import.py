#!/usr/bin/env python3
"""Simple test script to verify memory management system imports"""

def test_imports():
    """Test that all memory management components can be imported"""
    try:
        from performance.memory_management import (
            MemoryConfig,
            MemoryMonitor,
            DataFrameOptimizer,
            SessionStateManager,
            memory_profiler,
            memory_efficient_operation,
            demo_memory_management
        )
        print("✅ All memory management imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic memory management functionality"""
    try:
        from performance.memory_management import MemoryMonitor, DataFrameOptimizer
        import pandas as pd
        import numpy as np
        
        # Test MemoryMonitor
        monitor = MemoryMonitor()
        memory_info = monitor.get_memory_usage()
        print(f"✅ MemoryMonitor working: {memory_info['rss_mb']:.1f}MB")
        
        # Test DataFrameOptimizer
        df = pd.DataFrame({
            'id': range(1000),
            'value': np.random.randn(1000),
            'category': ['A', 'B', 'C'] * 333 + ['A']
        })
        
        optimized_df, stats = DataFrameOptimizer.optimize_dtypes(df)
        print(f"✅ DataFrameOptimizer working: {stats['reduction_percent']:.1f}% reduction")
        
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Testing Memory Management System")
    print("=" * 50)
    
    import_success = test_imports()
    if import_success:
        func_success = test_basic_functionality()
        
        if func_success:
            print("\n🎉 Memory management system is working correctly!")
        else:
            print("\n⚠️ Memory management system has functionality issues")
    else:
        print("\n❌ Memory management system has import issues")
    
    print("=" * 50) 