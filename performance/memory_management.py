# performance/memory_management.py - Memory Management and Resource Optimization
import streamlit as st
import pandas as pd
import numpy as np
import gc
import psutil
import threading
import weakref
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import time
import sys
import os
from contextlib import contextmanager
import warnings
from functools import wraps

@dataclass
class MemoryConfig:
    """Configuration for memory management"""
    max_memory_mb: int = 2048  # Maximum memory usage in MB
    cleanup_threshold: float = 0.8  # Cleanup when memory usage exceeds this ratio
    gc_frequency: int = 10  # Run garbage collection every N operations
    session_state_limit: int = 100  # Maximum items in session state
    dataframe_chunk_size: int = 10000  # Chunk size for large DataFrames
    cache_cleanup_interval: int = 300  # Cleanup interval in seconds
    enable_warnings: bool = True  # Show memory warnings
    auto_optimize: bool = True  # Automatically optimize memory usage

class MemoryMonitor:
    """Real-time memory monitoring and management"""
    
    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self.process = psutil.Process()
        self.baseline_memory = self.get_memory_usage()
        self.peak_memory = self.baseline_memory
        self.operation_count = 0
        self.memory_history = []
        self.weak_references = weakref.WeakSet()
        self.cleanup_callbacks = []
        
        # Start background cleanup thread
        self.cleanup_thread = threading.Thread(target=self._background_cleanup, daemon=True)
        self.cleanup_thread.start()
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage statistics"""
        memory_info = self.process.memory_info()
        memory_percent = self.process.memory_percent()
        
        # System memory info
        system_memory = psutil.virtual_memory()
        
        return {
            'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
            'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
            'percent': memory_percent,
            'available_mb': system_memory.available / 1024 / 1024,
            'system_percent': system_memory.percent
        }
    
    def check_memory_threshold(self) -> bool:
        """Check if memory usage exceeds threshold"""
        current_memory = self.get_memory_usage()
        
        # Update peak memory
        if current_memory['rss_mb'] > self.peak_memory['rss_mb']:
            self.peak_memory = current_memory
        
        # Check thresholds
        memory_ratio = current_memory['rss_mb'] / self.config.max_memory_mb
        
        if memory_ratio > self.config.cleanup_threshold:
            if self.config.enable_warnings:
                st.warning(f"⚠️ High memory usage detected: {current_memory['rss_mb']:.1f}MB ({memory_ratio:.1%})")
            return True
        
        return False
    
    def trigger_cleanup(self, force: bool = False) -> Dict[str, Any]:
        """Trigger memory cleanup operations"""
        start_time = time.time()
        before_memory = self.get_memory_usage()
        
        cleanup_results = {
            'gc_collected': 0,
            'session_state_cleaned': 0,
            'cache_cleared': False,
            'callbacks_executed': 0
        }
        
        # Force garbage collection
        cleanup_results['gc_collected'] = gc.collect()
        
        # Clean session state
        if hasattr(st, 'session_state'):
            cleanup_results['session_state_cleaned'] = self._cleanup_session_state()
        
        # Execute cleanup callbacks
        for callback in self.cleanup_callbacks:
            try:
                callback()
                cleanup_results['callbacks_executed'] += 1
            except Exception as e:
                if self.config.enable_warnings:
                    st.warning(f"Cleanup callback failed: {e}")
        
        # Clear caches if memory is still high
        after_gc_memory = self.get_memory_usage()
        if force or after_gc_memory['rss_mb'] > self.config.max_memory_mb * 0.7:
            self._clear_streamlit_caches()
            cleanup_results['cache_cleared'] = True
        
        after_memory = self.get_memory_usage()
        cleanup_time = time.time() - start_time
        
        memory_freed = before_memory['rss_mb'] - after_memory['rss_mb']
        
        cleanup_results.update({
            'before_memory_mb': before_memory['rss_mb'],
            'after_memory_mb': after_memory['rss_mb'],
            'memory_freed_mb': memory_freed,
            'cleanup_time_ms': cleanup_time * 1000
        })
        
        if self.config.enable_warnings and memory_freed > 50:
            st.success(f"✅ Memory cleanup freed {memory_freed:.1f}MB in {cleanup_time:.2f}s")
        
        return cleanup_results
    
    def _cleanup_session_state(self) -> int:
        """Clean up old session state items"""
        if not hasattr(st, 'session_state'):
            return 0
        
        initial_count = len(st.session_state)
        
        # Remove old temporary items
        keys_to_remove = []
        current_time = time.time()
        
        for key in st.session_state.keys():
            # Remove temporary keys older than 1 hour
            if key.startswith('temp_') and hasattr(st.session_state[key], '__timestamp__'):
                if current_time - getattr(st.session_state[key], '__timestamp__', 0) > 3600:
                    keys_to_remove.append(key)
            
            # Limit total session state size
            elif len(st.session_state) > self.config.session_state_limit:
                # Remove oldest non-essential items
                if not key.startswith(('user_', 'config_', 'auth_')):
                    keys_to_remove.append(key)
        
        for key in keys_to_remove[:50]:  # Limit removal batch size
            try:
                del st.session_state[key]
            except KeyError:
                pass
        
        return initial_count - len(st.session_state)
    
    def _clear_streamlit_caches(self):
        """Clear Streamlit caches"""
        try:
            st.cache_data.clear()
            st.cache_resource.clear()
        except Exception as e:
            if self.config.enable_warnings:
                st.warning(f"Cache clearing failed: {e}")
    
    def _background_cleanup(self):
        """Background thread for periodic cleanup"""
        while True:
            time.sleep(self.config.cache_cleanup_interval)
            
            if self.check_memory_threshold():
                self.trigger_cleanup()
    
    def register_cleanup_callback(self, callback: Callable):
        """Register a callback for memory cleanup"""
        self.cleanup_callbacks.append(callback)
    
    def track_object(self, obj: Any, name: str = None):
        """Track an object for memory monitoring"""
        self.weak_references.add(obj)
        
        if name and hasattr(obj, '__sizeof__'):
            size_mb = sys.getsizeof(obj) / 1024 / 1024
            if size_mb > 10:  # Track objects larger than 10MB
                self.memory_history.append({
                    'timestamp': datetime.now(),
                    'object_name': name,
                    'size_mb': size_mb,
                    'type': type(obj).__name__
                })
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Generate comprehensive memory usage report"""
        current_memory = self.get_memory_usage()
        
        return {
            'current_memory': current_memory,
            'baseline_memory': self.baseline_memory,
            'peak_memory': self.peak_memory,
            'memory_growth_mb': current_memory['rss_mb'] - self.baseline_memory['rss_mb'],
            'tracked_objects': len(self.weak_references),
            'large_objects_history': self.memory_history[-10:],  # Last 10 large objects
            'config': self.config,
            'gc_stats': {
                'generation_0': gc.get_count()[0],
                'generation_1': gc.get_count()[1], 
                'generation_2': gc.get_count()[2],
                'total_collections': sum(gc.get_stats()[i]['collections'] for i in range(3))
            }
        }
    
    def render_memory_dashboard(self):
        """Render memory monitoring dashboard in sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🧠 Memory Monitor")
            
            current_memory = self.get_memory_usage()
            
            # Memory usage metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Memory Usage", 
                    f"{current_memory['rss_mb']:.0f}MB",
                    f"{current_memory['percent']:.1f}%"
                )
            
            with col2:
                growth = current_memory['rss_mb'] - self.baseline_memory['rss_mb']
                st.metric(
                    "Growth", 
                    f"{growth:+.0f}MB",
                    f"Peak: {self.peak_memory['rss_mb']:.0f}MB"
                )
            
            # Memory status indicator
            memory_ratio = current_memory['rss_mb'] / self.config.max_memory_mb
            
            if memory_ratio > 0.9:
                st.error("🔴 Critical memory usage")
            elif memory_ratio > 0.7:
                st.warning("🟡 High memory usage")
            else:
                st.success("🟢 Normal memory usage")
            
            # Manual cleanup button
            if st.button("🧹 Clean Memory", help="Force memory cleanup", key=f"clean_memory_btn_{id(self)}"):
                cleanup_results = self.trigger_cleanup(force=True)
                st.json(cleanup_results)

class DataFrameOptimizer:
    """Optimize pandas DataFrames for memory efficiency"""
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame, aggressive: bool = False) -> pd.DataFrame:
        """Optimize DataFrame dtypes to reduce memory usage"""
        original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        
        df_optimized = df.copy()
        
        for col in df_optimized.columns:
            col_type = df_optimized[col].dtype
            
            # Optimize numeric columns
            if pd.api.types.is_numeric_dtype(df_optimized[col]):
                if pd.api.types.is_integer_dtype(df_optimized[col]):
                    # Downcast integers
                    df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
                else:
                    # Downcast floats
                    df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
            
            # Optimize string columns
            elif pd.api.types.is_object_dtype(df_optimized[col]):
                # Try to convert to category if beneficial
                unique_ratio = df_optimized[col].nunique() / len(df_optimized[col])
                
                if unique_ratio < 0.5 or (aggressive and unique_ratio < 0.8):
                    try:
                        df_optimized[col] = df_optimized[col].astype('category')
                    except:
                        pass
            
            # Optimize datetime columns
            elif pd.api.types.is_datetime64_any_dtype(df_optimized[col]):
                # Use appropriate datetime resolution
                if aggressive:
                    df_optimized[col] = df_optimized[col].dt.floor('s')  # Second precision
        
        optimized_memory = df_optimized.memory_usage(deep=True).sum() / 1024 / 1024
        reduction = (original_memory - optimized_memory) / original_memory * 100
        
        return df_optimized, {
            'original_memory_mb': original_memory,
            'optimized_memory_mb': optimized_memory,
            'reduction_percent': reduction
        }
    
    @staticmethod
    def chunk_dataframe(df: pd.DataFrame, chunk_size: int = 10000) -> List[pd.DataFrame]:
        """Split large DataFrame into memory-efficient chunks"""
        chunks = []
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size].copy()
            chunks.append(chunk)
        
        return chunks
    
    @staticmethod
    def lazy_load_dataframe(file_path: str, 
                           chunk_size: int = 10000,
                           optimize: bool = True) -> pd.DataFrame:
        """Lazy load large DataFrames with optimization"""
        
        # Read in chunks to avoid memory spikes
        chunks = []
        total_rows = 0
        
        try:
            # Get total rows for progress tracking
            with pd.read_csv(file_path, chunksize=chunk_size) as reader:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, chunk in enumerate(reader):
                    if optimize:
                        chunk, _ = DataFrameOptimizer.optimize_dtypes(chunk)
                    
                    chunks.append(chunk)
                    total_rows += len(chunk)
                    
                    # Update progress
                    status_text.text(f"Loading chunk {i+1}, total rows: {total_rows:,}")
                    
                    # Memory check
                    current_memory = psutil.Process().memory_info().rss / 1024 / 1024
                    if current_memory > 1500:  # 1.5GB threshold
                        st.warning("⚠️ High memory usage during loading")
                        break
                
                progress_bar.progress(1.0)
                status_text.text(f"Loaded {total_rows:,} rows successfully")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
        
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
        
        # Concatenate chunks
        if chunks:
            return pd.concat(chunks, ignore_index=True)
        else:
            return pd.DataFrame()

@contextmanager
def memory_profiler(operation_name: str, monitor: MemoryMonitor = None):
    """Context manager for profiling memory usage of operations"""
    if monitor is None:
        monitor = MemoryMonitor()
    
    start_memory = monitor.get_memory_usage()
    start_time = time.time()
    
    try:
        yield monitor
    finally:
        end_memory = monitor.get_memory_usage()
        end_time = time.time()
        
        memory_delta = end_memory['rss_mb'] - start_memory['rss_mb']
        time_delta = end_time - start_time
        
        # Store operation stats
        if not hasattr(st.session_state, 'memory_operations'):
            st.session_state.memory_operations = []
        
        st.session_state.memory_operations.append({
            'operation': operation_name,
            'memory_delta_mb': memory_delta,
            'execution_time_s': time_delta,
            'timestamp': datetime.now()
        })
        
        # Show warning for memory-intensive operations
        if memory_delta > 100:  # More than 100MB
            st.warning(f"⚠️ Operation '{operation_name}' used {memory_delta:.1f}MB memory")

def memory_efficient_operation(func):
    """Decorator for memory-efficient operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        monitor = MemoryMonitor()
        
        # Check memory before operation
        if monitor.check_memory_threshold():
            monitor.trigger_cleanup()
        
        # Execute operation with monitoring
        with memory_profiler(func.__name__, monitor):
            result = func(*args, **kwargs)
        
        # Increment operation count for GC scheduling
        monitor.operation_count += 1
        
        # Trigger GC if needed
        if monitor.operation_count % monitor.config.gc_frequency == 0:
            gc.collect()
        
        return result
    
    return wrapper

class SessionStateManager:
    """Manage Streamlit session state for memory efficiency"""
    
    @staticmethod
    def set_with_timestamp(key: str, value: Any, ttl_seconds: int = 3600):
        """Set session state value with automatic expiration"""
        st.session_state[key] = value
        st.session_state[f"{key}_timestamp"] = time.time()
        st.session_state[f"{key}_ttl"] = ttl_seconds
    
    @staticmethod
    def get_with_expiry(key: str, default: Any = None) -> Any:
        """Get session state value, checking for expiration"""
        if key not in st.session_state:
            return default
        
        timestamp_key = f"{key}_timestamp"
        ttl_key = f"{key}_ttl"
        
        if timestamp_key in st.session_state and ttl_key in st.session_state:
            age = time.time() - st.session_state[timestamp_key]
            ttl = st.session_state[ttl_key]
            
            if age > ttl:
                # Expired, clean up
                del st.session_state[key]
                if timestamp_key in st.session_state:
                    del st.session_state[timestamp_key]
                if ttl_key in st.session_state:
                    del st.session_state[ttl_key]
                return default
        
        return st.session_state[key]
    
    @staticmethod
    def cleanup_expired():
        """Clean up all expired session state items"""
        current_time = time.time()
        keys_to_remove = []
        
        for key in list(st.session_state.keys()):
            if key.endswith('_timestamp'):
                base_key = key[:-10]  # Remove '_timestamp'
                ttl_key = f"{base_key}_ttl"
                
                if ttl_key in st.session_state:
                    age = current_time - st.session_state[key]
                    ttl = st.session_state[ttl_key]
                    
                    if age > ttl:
                        keys_to_remove.extend([base_key, key, ttl_key])
        
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        
        return len(keys_to_remove) // 3  # Return number of expired items

# Demo function
def demo_memory_management():
    """Demonstrate memory management features"""
    
    st.title("🧠 Memory Management & Optimization Demo")
    
    # Initialize memory monitor
    if 'memory_monitor' not in st.session_state:
        st.session_state.memory_monitor = MemoryMonitor()
    
    monitor = st.session_state.memory_monitor
    
    # Render memory dashboard
    monitor.render_memory_dashboard()
    
    # Memory test controls
    st.markdown("### Memory Operations Testing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Create Large DataFrame"):
            with memory_profiler("large_dataframe_creation", monitor):
                # Create large DataFrame
                size = st.selectbox("DataFrame Size", [10000, 50000, 100000], key="df_size")
                
                large_df = pd.DataFrame({
                    'id': range(size),
                    'value1': np.random.randn(size),
                    'value2': np.random.randn(size),
                    'category': np.random.choice(['A', 'B', 'C', 'D'], size),
                    'timestamp': pd.date_range('2020-01-01', periods=size, freq='H')
                })
                
                # Optimize DataFrame
                optimized_df, optimization_stats = DataFrameOptimizer.optimize_dtypes(large_df)
                
                st.success(f"Created DataFrame with {len(large_df):,} rows")
                st.json(optimization_stats)
                
                # Store in session state
                SessionStateManager.set_with_timestamp('large_df', optimized_df, 1800)  # 30 min TTL
    
    with col2:
        if st.button("🧹 Force Memory Cleanup"):
            cleanup_results = monitor.trigger_cleanup(force=True)
            st.json(cleanup_results)
    
    with col3:
        if st.button("📊 Memory Report"):
            report = monitor.get_memory_report()
            st.json(report)
    
    # DataFrame optimization demo
    st.markdown("### DataFrame Optimization Demo")
    
    # Check if we have a stored DataFrame
    stored_df = SessionStateManager.get_with_expiry('large_df')
    
    if stored_df is not None:
        st.write(f"Stored DataFrame: {len(stored_df):,} rows")
        
        # Show memory usage
        memory_usage = stored_df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric("DataFrame Memory Usage", f"{memory_usage:.2f} MB")
        
        # Chunking demo
        if st.button("📦 Create Chunks"):
            chunks = DataFrameOptimizer.chunk_dataframe(stored_df, chunk_size=10000)
            st.success(f"Created {len(chunks)} chunks")
            
            # Show chunk sizes
            for i, chunk in enumerate(chunks[:5]):  # Show first 5 chunks
                chunk_memory = chunk.memory_usage(deep=True).sum() / 1024 / 1024
                st.write(f"Chunk {i+1}: {len(chunk):,} rows, {chunk_memory:.2f} MB")
    
    # Session state management demo
    st.markdown("### Session State Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Set temporary data
        if st.button("🔄 Store Temporary Data"):
            temp_data = {
                'large_array': np.random.randn(10000),
                'timestamp': datetime.now()
            }
            SessionStateManager.set_with_timestamp('temp_data', temp_data, 300)  # 5 min TTL
            st.success("Stored temporary data with 5-minute expiration")
    
    with col2:
        # Cleanup expired items
        if st.button("🧹 Cleanup Expired"):
            cleaned_count = SessionStateManager.cleanup_expired()
            st.success(f"Cleaned up {cleaned_count} expired items")
    
    # Performance statistics
    st.markdown("### Performance Statistics")
    
    if hasattr(st.session_state, 'memory_operations'):
        operations_df = pd.DataFrame(st.session_state.memory_operations)
        
        if not operations_df.empty:
            # Recent operations
            st.subheader("Recent Memory Operations")
            recent_ops = operations_df.tail(10)
            st.dataframe(recent_ops)
            
            # Memory usage chart
            if len(operations_df) > 1:
                st.subheader("Memory Usage Over Time")
                
                import plotly.express as px
                fig = px.line(operations_df, 
                            x='timestamp', 
                            y='memory_delta_mb',
                            title='Memory Usage by Operation')
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    demo_memory_management() 