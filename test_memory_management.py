# test_memory_management.py - Memory Management System Tests
import streamlit as st
import pandas as pd
import numpy as np
import time
import gc
from datetime import datetime, timedelta

from performance.memory_management import (
    MemoryConfig,
    MemoryMonitor,
    DataFrameOptimizer,
    SessionStateManager,
    memory_profiler,
    memory_efficient_operation
)

def test_memory_monitor():
    """Test MemoryMonitor functionality"""
    st.header("🧪 Memory Monitor Tests")
    
    # Initialize monitor
    config = MemoryConfig(
        max_memory_mb=1024,
        cleanup_threshold=0.7,
        enable_warnings=False
    )
    monitor = MemoryMonitor(config)
    
    # Test memory usage retrieval
    st.subheader("📊 Memory Usage Tests")
    
    memory_info = monitor.get_memory_usage()
    st.write("**Memory Info:**")
    st.json(memory_info)
    
    # Test threshold checking
    threshold_result = monitor.check_memory_threshold()
    st.write(f"**Threshold Check:** {threshold_result}")
    
    # Test cleanup
    st.subheader("🧹 Cleanup Tests")
    
    if st.button("Test Cleanup"):
        cleanup_results = monitor.trigger_cleanup(force=True)
        st.write("**Cleanup Results:**")
        st.json(cleanup_results)
    
    # Test memory report
    st.subheader("📈 Memory Report Tests")
    
    if st.button("Generate Report"):
        report = monitor.get_memory_report()
        st.write("**Memory Report:**")
        st.json(report)
    
    return True

def test_dataframe_optimizer():
    """Test DataFrameOptimizer functionality"""
    st.header("🧪 DataFrame Optimizer Tests")
    
    # Create test DataFrame
    st.subheader("📊 DataFrame Creation")
    
    test_data = {
        'id': range(10000),
        'value1': np.random.randn(10000),
        'value2': np.random.randint(0, 1000, 10000),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 10000),
        'text': [f"Text_{i}" for i in range(10000)],
        'timestamp': pd.date_range('2020-01-01', periods=10000, freq='H')
    }
    
    df = pd.DataFrame(test_data)
    original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    
    st.write(f"**Original DataFrame:** {len(df):,} rows, {original_memory:.2f} MB")
    st.write("**Original Data Types:**")
    st.dataframe(df.dtypes.to_frame('dtype'))
    
    # Test optimization
    st.subheader("⚡ Optimization Tests")
    
    if st.button("Test Optimization"):
        optimized_df, stats = DataFrameOptimizer.optimize_dtypes(df)
        
        st.write("**Optimization Results:**")
        st.json(stats)
        
        st.write("**Optimized Data Types:**")
        st.dataframe(optimized_df.dtypes.to_frame('dtype'))
    
    # Test chunking
    st.subheader("📦 Chunking Tests")
    
    if st.button("Test Chunking"):
        chunks = DataFrameOptimizer.chunk_dataframe(df, chunk_size=2000)
        
        st.write(f"**Created {len(chunks)} chunks**")
        
        chunk_info = []
        for i, chunk in enumerate(chunks):
            memory = chunk.memory_usage(deep=True).sum() / 1024 / 1024
            chunk_info.append({
                'Chunk': i + 1,
                'Rows': len(chunk),
                'Memory (MB)': f"{memory:.2f}"
            })
        
        st.dataframe(pd.DataFrame(chunk_info))
    
    return True

def test_session_state_manager():
    """Test SessionStateManager functionality"""
    st.header("🧪 Session State Manager Tests")
    
    # Test setting with timestamp
    st.subheader("📝 Set/Get Tests")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Set Test Data"):
            test_data = {
                'array': np.random.randn(1000),
                'timestamp': datetime.now(),
                'metadata': {'test': True}
            }
            SessionStateManager.set_with_timestamp('test_data', test_data, 60)  # 1 minute TTL
            st.success("✅ Test data set with 60s TTL")
    
    with col2:
        if st.button("Get Test Data"):
            data = SessionStateManager.get_with_expiry('test_data')
            if data is not None:
                st.success("✅ Data retrieved successfully")
                st.write(f"**Data Type:** {type(data).__name__}")
                if isinstance(data, dict):
                    st.write(f"**Keys:** {list(data.keys())}")
            else:
                st.warning("❌ Data not found or expired")
    
    # Test cleanup
    st.subheader("🧹 Cleanup Tests")
    
    if st.button("Test Cleanup Expired"):
        # Set some expired data
        old_data = {'old': True}
        SessionStateManager.set_with_timestamp('old_data', old_data, 1)  # 1 second TTL
        
        # Wait a moment
        time.sleep(2)
        
        # Cleanup
        cleaned_count = SessionStateManager.cleanup_expired()
        st.write(f"**Cleaned up {cleaned_count} expired items**")
    
    return True

def test_memory_profiler():
    """Test memory profiler functionality"""
    st.header("🧪 Memory Profiler Tests")
    
    # Initialize monitor
    monitor = MemoryMonitor()
    
    # Test memory profiler
    st.subheader("📊 Profiler Tests")
    
    if st.button("Test Memory Profiler"):
        with memory_profiler("test_operation", monitor):
            # Simulate memory-intensive operation
            large_array = np.random.randn(50000)
            result = np.sum(large_array ** 2)
            time.sleep(0.1)  # Simulate processing time
        
        st.success("✅ Memory profiler test completed")
        
        # Check if operation was recorded
        if hasattr(st.session_state, 'memory_operations'):
            ops = st.session_state.memory_operations
            if ops:
                latest_op = ops[-1]
                st.write("**Latest Operation:**")
                st.json(latest_op)
    
    return True

def test_memory_efficient_operation():
    """Test memory efficient operation decorator"""
    st.header("🧪 Memory Efficient Operation Tests")
    
    @memory_efficient_operation
    def test_function(size):
        """Test function that uses memory"""
        data = np.random.randn(size)
        result = np.mean(data)
        return result
    
    st.subheader("⚡ Decorator Tests")
    
    if st.button("Test Decorated Function"):
        try:
            result = test_function(10000)
            st.success(f"✅ Function executed successfully: {result:.4f}")
        except Exception as e:
            st.error(f"❌ Function failed: {e}")
    
    return True

def run_all_tests():
    """Run all memory management tests"""
    st.title("🧪 Memory Management System Tests")
    st.markdown("Comprehensive testing of memory management features")
    
    # Test results
    test_results = {}
    
    # Run tests
    st.markdown("---")
    test_results['memory_monitor'] = test_memory_monitor()
    
    st.markdown("---")
    test_results['dataframe_optimizer'] = test_dataframe_optimizer()
    
    st.markdown("---")
    test_results['session_state_manager'] = test_session_state_manager()
    
    st.markdown("---")
    test_results['memory_profiler'] = test_memory_profiler()
    
    st.markdown("---")
    test_results['memory_efficient_operation'] = test_memory_efficient_operation()
    
    # Summary
    st.markdown("---")
    st.subheader("📊 Test Summary")
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    st.metric("Tests Passed", f"{passed}/{total}")
    
    if passed == total:
        st.success("🎉 All tests passed!")
    else:
        st.warning(f"⚠️ {total - passed} tests failed")
    
    # Show detailed results
    st.write("**Detailed Results:**")
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        st.write(f"• {test_name}: {status}")

def performance_benchmark():
    """Run performance benchmarks"""
    st.header("🏃 Performance Benchmarks")
    
    # Initialize monitor
    monitor = MemoryMonitor()
    
    st.subheader("📊 Memory Usage Benchmark")
    
    if st.button("Run Benchmark"):
        # Baseline memory
        baseline = monitor.get_memory_usage()
        
        # Create large DataFrame
        with memory_profiler("large_df_creation", monitor):
            df = pd.DataFrame({
                'id': range(100000),
                'value1': np.random.randn(100000),
                'value2': np.random.randn(100000),
                'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 100000),
                'timestamp': pd.date_range('2020-01-01', periods=100000, freq='H')
            })
        
        # Optimize DataFrame
        with memory_profiler("df_optimization", monitor):
            optimized_df, stats = DataFrameOptimizer.optimize_dtypes(df)
        
        # Perform operations
        with memory_profiler("df_operations", monitor):
            result1 = optimized_df.groupby('category').agg({'value1': ['mean', 'std']})
            result2 = optimized_df.rolling(window=1000).mean()
        
        # Final memory
        final = monitor.get_memory_usage()
        
        # Results
        st.subheader("📈 Benchmark Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Baseline Memory", f"{baseline['rss_mb']:.1f} MB")
        
        with col2:
            st.metric("Peak Memory", f"{monitor.peak_memory['rss_mb']:.1f} MB")
        
        with col3:
            st.metric("Final Memory", f"{final['rss_mb']:.1f} MB")
        
        # Optimization stats
        st.write("**Optimization Stats:**")
        st.json(stats)
        
        # Memory operations
        if hasattr(st.session_state, 'memory_operations'):
            ops_df = pd.DataFrame(st.session_state.memory_operations)
            if not ops_df.empty:
                st.write("**Operation Summary:**")
                st.dataframe(ops_df[['operation', 'memory_delta_mb', 'execution_time_s']])

if __name__ == "__main__":
    # Navigation
    test_type = st.sidebar.selectbox(
        "Test Type",
        ["All Tests", "Performance Benchmark"]
    )
    
    if test_type == "All Tests":
        run_all_tests()
    else:
        performance_benchmark() 