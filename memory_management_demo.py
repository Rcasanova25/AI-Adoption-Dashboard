# memory_management_demo.py - Memory Management System Demo
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

from performance.memory_management import (
    MemoryConfig,
    MemoryMonitor,
    DataFrameOptimizer,
    SessionStateManager,
    memory_profiler,
    memory_efficient_operation,
    demo_memory_management
)

def main():
    """Main demo function"""
    st.set_page_config(
        page_title="Memory Management Demo",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 AI Dashboard Memory Management System")
    st.markdown("Advanced memory monitoring, optimization, and resource management")
    
    # Navigation
    demo_type = st.sidebar.selectbox(
        "Demo Type",
        ["Full Demo", "Memory Monitor", "DataFrame Optimization", "Session State Management", "Performance Profiling"]
    )
    
    if demo_type == "Full Demo":
        demo_memory_management()
    elif demo_type == "Memory Monitor":
        demo_memory_monitor()
    elif demo_type == "DataFrame Optimization":
        demo_dataframe_optimization()
    elif demo_type == "Session State Management":
        demo_session_state_management()
    elif demo_type == "Performance Profiling":
        demo_performance_profiling()

def demo_memory_monitor():
    """Demo the memory monitoring capabilities"""
    st.header("📊 Memory Monitor Demo")
    
    # Initialize memory monitor
    if 'memory_monitor' not in st.session_state:
        st.session_state.memory_monitor = MemoryMonitor()
    
    monitor = st.session_state.memory_monitor
    
    # Configuration
    st.subheader("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_memory = st.slider("Max Memory (MB)", 512, 4096, 2048)
        cleanup_threshold = st.slider("Cleanup Threshold", 0.5, 0.95, 0.8)
    
    with col2:
        gc_frequency = st.slider("GC Frequency", 5, 50, 10)
        enable_warnings = st.checkbox("Enable Warnings", True)
    
    # Update config
    monitor.config.max_memory_mb = max_memory
    monitor.config.cleanup_threshold = cleanup_threshold
    monitor.config.gc_frequency = gc_frequency
    monitor.config.enable_warnings = enable_warnings
    
    # Memory dashboard
    st.subheader("📈 Memory Dashboard")
    monitor.render_memory_dashboard()
    
    # Memory operations
    st.subheader("🔧 Memory Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Get Memory Report"):
            report = monitor.get_memory_report()
            st.json(report)
    
    with col2:
        if st.button("🧹 Force Cleanup"):
            results = monitor.trigger_cleanup(force=True)
            st.json(results)
    
    with col3:
        if st.button("📈 Memory History"):
            if monitor.memory_history:
                history_df = pd.DataFrame(monitor.memory_history)
                st.dataframe(history_df)
            else:
                st.info("No memory history available")

def demo_dataframe_optimization():
    """Demo DataFrame optimization features"""
    st.header("📊 DataFrame Optimization Demo")
    
    # Create test DataFrame
    st.subheader("🔄 Create Test DataFrame")
    
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.selectbox("DataFrame Size", [1000, 10000, 50000, 100000], key="opt_size")
        include_strings = st.checkbox("Include String Columns", True)
        include_datetime = st.checkbox("Include DateTime Columns", True)
    
    with col2:
        if st.button("🔄 Generate DataFrame"):
            # Create DataFrame with various data types
            data = {
                'id': range(size),
                'value1': np.random.randn(size),
                'value2': np.random.randint(0, 1000, size),
                'value3': np.random.choice([True, False], size),
                'float_col': np.random.uniform(0, 100, size)
            }
            
            if include_strings:
                data['category'] = np.random.choice(['A', 'B', 'C', 'D', 'E'], size)
                data['text'] = [f"Text_{i}" for i in range(size)]
            
            if include_datetime:
                data['timestamp'] = pd.date_range('2020-01-01', periods=size, freq='H')
            
            df = pd.DataFrame(data)
            
            # Store in session state
            SessionStateManager.set_with_timestamp('test_df', df, 1800)
            st.success(f"Created DataFrame with {len(df):,} rows")
    
    # Optimization demo
    st.subheader("⚡ Optimization Demo")
    
    df = SessionStateManager.get_with_expiry('test_df')
    
    if df is not None:
        # Show original memory usage
        original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("Original Memory Usage", f"{original_memory:.2f} MB")
        
        # Show data types
        st.write("**Original Data Types:**")
        st.dataframe(df.dtypes.to_frame('dtype'))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚡ Optimize DataTypes"):
                with memory_profiler("dataframe_optimization"):
                    optimized_df, stats = DataFrameOptimizer.optimize_dtypes(df)
                    
                    st.success("✅ Optimization Complete!")
                    st.json(stats)
                    
                    # Show optimized data types
                    st.write("**Optimized Data Types:**")
                    st.dataframe(optimized_df.dtypes.to_frame('dtype'))
                    
                    # Store optimized version
                    SessionStateManager.set_with_timestamp('optimized_df', optimized_df, 1800)
        
        with col2:
            if st.button("📦 Create Chunks"):
                chunk_size = st.selectbox("Chunk Size", [1000, 5000, 10000], key="chunk_size")
                chunks = DataFrameOptimizer.chunk_dataframe(df, chunk_size)
                
                st.success(f"Created {len(chunks)} chunks")
                
                # Show chunk info
                chunk_info = []
                for i, chunk in enumerate(chunks[:5]):  # Show first 5
                    memory = chunk.memory_usage(deep=True).sum() / 1024 / 1024
                    chunk_info.append({
                        'Chunk': i + 1,
                        'Rows': len(chunk),
                        'Memory (MB)': f"{memory:.2f}"
                    })
                
                st.dataframe(pd.DataFrame(chunk_info))

def demo_session_state_management():
    """Demo session state management features"""
    st.header("🗂️ Session State Management Demo")
    
    st.subheader("📝 Store Data with TTL")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Store different types of data
        data_type = st.selectbox("Data Type", ["Small Array", "Large Array", "DataFrame", "Dictionary"])
        ttl_seconds = st.slider("TTL (seconds)", 60, 3600, 300)
        
        if st.button("💾 Store Data"):
            if data_type == "Small Array":
                data = np.random.randn(1000)
            elif data_type == "Large Array":
                data = np.random.randn(100000)
            elif data_type == "DataFrame":
                data = pd.DataFrame({
                    'id': range(10000),
                    'value': np.random.randn(10000),
                    'category': np.random.choice(['A', 'B', 'C'], 10000)
                })
            else:  # Dictionary
                data = {
                    'timestamp': datetime.now(),
                    'values': np.random.randn(5000).tolist(),
                    'metadata': {'source': 'demo', 'version': '1.0'}
                }
            
            SessionStateManager.set_with_timestamp(f'test_{data_type.lower()}', data, ttl_seconds)
            st.success(f"Stored {data_type} with {ttl_seconds}s TTL")
    
    with col2:
        # Retrieve data
        if st.button("📖 Retrieve Data"):
            keys = [key for key in st.session_state.keys() if key.startswith('test_') and not key.endswith(('_timestamp', '_ttl'))]
            
            if keys:
                st.write("**Available Keys:**")
                for key in keys:
                    data = SessionStateManager.get_with_expiry(key)
                    if data is not None:
                        if isinstance(data, np.ndarray):
                            st.write(f"✅ {key}: {data.shape} array")
                        elif isinstance(data, pd.DataFrame):
                            st.write(f"✅ {key}: {data.shape} DataFrame")
                        else:
                            st.write(f"✅ {key}: {type(data).__name__}")
                    else:
                        st.write(f"❌ {key}: Expired")
            else:
                st.info("No test data available")
    
    # Cleanup demo
    st.subheader("🧹 Cleanup Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧹 Cleanup Expired"):
            cleaned_count = SessionStateManager.cleanup_expired()
            st.success(f"Cleaned up {cleaned_count} expired items")
    
    with col2:
        if st.button("📊 Session State Info"):
            total_items = len(st.session_state)
            ttl_items = len([k for k in st.session_state.keys() if k.endswith('_ttl')])
            
            st.metric("Total Items", total_items)
            st.metric("TTL Items", ttl_items)
            
            # Show session state keys
            st.write("**Session State Keys:**")
            for key in list(st.session_state.keys())[:20]:  # Show first 20
                st.write(f"• {key}")

def demo_performance_profiling():
    """Demo performance profiling features"""
    st.header("⚡ Performance Profiling Demo")
    
    # Initialize memory monitor
    if 'memory_monitor' not in st.session_state:
        st.session_state.memory_monitor = MemoryMonitor()
    
    monitor = st.session_state.memory_monitor
    
    st.subheader("🔧 Memory-Intensive Operations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Large DataFrame Creation"):
            with memory_profiler("large_df_creation", monitor):
                size = 50000
                df = pd.DataFrame({
                    'id': range(size),
                    'value1': np.random.randn(size),
                    'value2': np.random.randn(size),
                    'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], size),
                    'timestamp': pd.date_range('2020-01-01', periods=size, freq='H')
                })
                st.success(f"Created DataFrame with {len(df):,} rows")
    
    with col2:
        if st.button("🔄 DataFrame Operations"):
            df = SessionStateManager.get_with_expiry('large_df')
            if df is not None:
                with memory_profiler("df_operations", monitor):
                    # Perform various operations
                    result1 = df.groupby('category').agg({'value1': ['mean', 'std']})
                    result2 = df.rolling(window=100).mean()
                    result3 = df.corr()
                    st.success("Completed DataFrame operations")
            else:
                st.warning("No large DataFrame available. Create one first.")
    
    with col3:
        if st.button("🧮 Complex Calculations"):
            with memory_profiler("complex_calculations", monitor):
                # Simulate complex calculations
                large_array = np.random.randn(100000, 100)
                result = np.linalg.svd(large_array)
                st.success("Completed complex calculations")
    
    # Performance statistics
    st.subheader("📈 Performance Statistics")
    
    if hasattr(st.session_state, 'memory_operations'):
        operations_df = pd.DataFrame(st.session_state.memory_operations)
        
        if not operations_df.empty:
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_ops = len(operations_df)
                st.metric("Total Operations", total_ops)
            
            with col2:
                avg_memory = operations_df['memory_delta_mb'].mean()
                st.metric("Avg Memory Delta", f"{avg_memory:.1f} MB")
            
            with col3:
                max_memory = operations_df['memory_delta_mb'].max()
                st.metric("Max Memory Delta", f"{max_memory:.1f} MB")
            
            with col4:
                total_time = operations_df['execution_time_s'].sum()
                st.metric("Total Time", f"{total_time:.2f} s")
            
            # Recent operations table
            st.write("**Recent Operations:**")
            recent_ops = operations_df.tail(10)[['operation', 'memory_delta_mb', 'execution_time_s', 'timestamp']]
            st.dataframe(recent_ops)
            
            # Memory usage chart
            if len(operations_df) > 1:
                st.write("**Memory Usage Over Time:**")
                
                import plotly.express as px
                fig = px.line(operations_df, 
                            x='timestamp', 
                            y='memory_delta_mb',
                            title='Memory Usage by Operation',
                            labels={'memory_delta_mb': 'Memory Delta (MB)', 'timestamp': 'Time'})
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No performance data available. Run some operations first.")
    else:
        st.info("No performance data available. Run some operations first.")

if __name__ == "__main__":
    main() 