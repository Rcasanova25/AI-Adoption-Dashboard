#!/usr/bin/env python3
"""
Simple Performance Integration Demo
Test the basic performance optimization system
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Import performance modules
from performance.caching import AdvancedCache, smart_cache
from performance.chart_optimization import ChartOptimizer, OptimizedCharts, ChartConfig
from performance.memory_management import MemoryMonitor, DataFrameOptimizer

def simple_performance_demo():
    """Simple performance integration demo"""
    
    st.title("🚀 Performance Integration System Demo")
    st.markdown("Testing the integrated performance optimization system")
    
    # Initialize components
    if 'cache' not in st.session_state:
        st.session_state.cache = AdvancedCache()
    
    if 'memory_monitor' not in st.session_state:
        st.session_state.memory_monitor = MemoryMonitor()
    
    if 'chart_optimizer' not in st.session_state:
        st.session_state.chart_optimizer = ChartOptimizer(ChartConfig())
    
    if 'charts' not in st.session_state:
        st.session_state.charts = OptimizedCharts(st.session_state.chart_optimizer)
    
    # Sidebar controls
    st.sidebar.markdown("### ⚡ Performance Controls")
    
    # Memory monitoring
    st.session_state.memory_monitor.render_memory_dashboard()
    
    # Cache stats
    with st.sidebar.expander("💾 Cache Statistics"):
        cache_stats = st.session_state.cache.get_stats()
        st.metric("Cache Entries", cache_stats['entries'])
        st.metric("Cache Size", f"{cache_stats['total_size_mb']:.1f} MB")
        
        if st.button("Clear Cache"):
            st.session_state.cache.clear()
            st.success("Cache cleared!")
    
    # Main content
    st.markdown("### 📊 Performance Test Dashboard")
    
    # Generate test data
    @smart_cache(ttl=300)  # 5-minute cache
    def generate_test_data(size=10000):
        """Generate test data with caching"""
        np.random.seed(42)
        dates = pd.date_range('2020-01-01', periods=size, freq='D')
        
        data = pd.DataFrame({
            'date': dates,
            'value1': np.random.randn(size).cumsum(),
            'value2': np.random.randn(size).cumsum() * 0.5,
            'category': np.random.choice(['A', 'B', 'C'], size)
        })
        
        return data
    
    # Load data with optimization
    with st.spinner("Loading optimized data..."):
        start_time = time.time()
        test_data = generate_test_data(5000)
        load_time = time.time() - start_time
    
    st.metric("Data Load Time", f"{load_time:.3f}s")
    st.metric("Data Points", f"{len(test_data):,}")
    
    # Create optimized chart
    st.markdown("### 📈 Optimized Chart Rendering")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Create Optimized Chart"):
            start_time = time.time()
            
            # Create optimized time series
            fig = st.session_state.charts.create_time_series(
                test_data, 'date', ['value1'],
                title="Optimized Performance Chart"
            )
            
            render_time = time.time() - start_time
            st.metric("Chart Render Time", f"{render_time:.3f}s")
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if st.button("Create Standard Chart"):
            start_time = time.time()
            
            # Create standard chart for comparison
            import plotly.express as px
            fig = px.line(test_data, x='date', y='value1', title="Standard Chart")
            
            render_time = time.time() - start_time
            st.metric("Standard Render Time", f"{render_time:.3f}s")
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Performance comparison
    st.markdown("### 🏁 Performance Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Caching Benefits**")
        st.write("• Reduced data loading time")
        st.write("• Persistent across sessions")
        st.write("• Smart cache invalidation")
    
    with col2:
        st.info("**Chart Optimization**")
        st.write("• WebGL rendering")
        st.write("• Data downsampling")
        st.write("• Lazy loading")
    
    with col3:
        st.info("**Memory Management**")
        st.write("• Real-time monitoring")
        st.write("• Automatic cleanup")
        st.write("• DataFrame optimization")
    
    # Data optimization demo
    st.markdown("### 🔧 Data Optimization Demo")
    
    if st.button("Optimize DataFrame"):
        start_time = time.time()
        
        # Create large DataFrame
        large_df = pd.DataFrame({
            'int_col': np.random.randint(0, 1000, 100000),
            'float_col': np.random.randn(100000),
            'string_col': np.random.choice(['A', 'B', 'C', 'D'], 100000),
            'bool_col': np.random.choice([True, False], 100000)
        })
        
        original_memory = large_df.memory_usage(deep=True).sum() / 1024 / 1024
        
        # Optimize DataFrame
        optimized_df, optimization_report = DataFrameOptimizer.optimize_dtypes(large_df)
        
        optimized_memory = optimized_df.memory_usage(deep=True).sum() / 1024 / 1024
        optimization_time = time.time() - start_time
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Original Memory", f"{original_memory:.1f} MB")
        with col2:
            st.metric("Optimized Memory", f"{optimized_memory:.1f} MB")
        with col3:
            st.metric("Memory Saved", f"{original_memory - optimized_memory:.1f} MB")
        
        st.metric("Optimization Time", f"{optimization_time:.3f}s")
        
        # Show optimization details
        with st.expander("📋 Optimization Details"):
            st.json(optimization_report)

if __name__ == "__main__":
    simple_performance_demo() 