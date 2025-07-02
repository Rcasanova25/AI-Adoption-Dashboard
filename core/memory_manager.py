"""
Memory Management and Monitoring for AI Adoption Dashboard
Implements memory optimization, leak prevention, and monitoring utilities
"""

import gc
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from contextlib import contextmanager
from functools import wraps
import logging
import time
import warnings

logger = logging.getLogger(__name__)

# Try to import psutil for detailed memory monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil not available. Memory monitoring will be limited.")


class MemoryManager:
    """
    Comprehensive memory management and monitoring utilities
    """
    
    # Memory thresholds (in MB)
    WARNING_THRESHOLD = 512  # 512 MB
    CRITICAL_THRESHOLD = 1024  # 1 GB
    
    @staticmethod
    def get_memory_info() -> Dict[str, float]:
        """
        Get current memory usage information
        
        Returns:
            Dictionary with memory information in MB
        """
        info = {
            'process_memory': 0,
            'available_memory': 0,
            'memory_percent': 0,
            'python_objects': 0
        }
        
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process()
                memory_info = process.memory_info()
                virtual_memory = psutil.virtual_memory()
                
                info.update({
                    'process_memory': memory_info.rss / 1024 / 1024,  # MB
                    'available_memory': virtual_memory.available / 1024 / 1024,  # MB
                    'memory_percent': process.memory_percent(),
                    'python_objects': len(gc.get_objects())
                })
            except Exception as e:
                logger.error(f"Error getting memory info: {e}")
        
        return info
    
    @staticmethod
    def check_memory_usage(operation_name: str = "") -> bool:
        """
        Check current memory usage and warn if high
        
        Args:
            operation_name: Name of the operation being checked
            
        Returns:
            True if memory usage is acceptable, False if critical
        """
        memory_info = MemoryManager.get_memory_info()
        process_memory = memory_info['process_memory']
        
        if process_memory > MemoryManager.CRITICAL_THRESHOLD:
            logger.critical(f"Critical memory usage: {process_memory:.1f}MB {operation_name}")
            st.error(f"Critical memory usage detected: {process_memory:.1f}MB")
            return False
        elif process_memory > MemoryManager.WARNING_THRESHOLD:
            logger.warning(f"High memory usage: {process_memory:.1f}MB {operation_name}")
            st.warning(f"High memory usage: {process_memory:.1f}MB")
            return True
        
        return True
    
    @staticmethod
    def force_garbage_collection() -> Dict[str, int]:
        """
        Force garbage collection and return statistics
        
        Returns:
            Dictionary with garbage collection statistics
        """
        # Get object count before
        objects_before = len(gc.get_objects())
        
        # Force garbage collection
        collected = {
            'generation_0': gc.collect(0),
            'generation_1': gc.collect(1), 
            'generation_2': gc.collect(2)
        }
        
        # Get object count after
        objects_after = len(gc.get_objects())
        
        stats = {
            'objects_before': objects_before,
            'objects_after': objects_after,
            'objects_freed': objects_before - objects_after,
            'total_collected': sum(collected.values())
        }
        
        logger.info(f"Garbage collection: freed {stats['objects_freed']} objects")
        return stats
    
    @staticmethod
    def optimize_dataframe_memory_usage(df: pd.DataFrame, aggressive: bool = False) -> pd.DataFrame:
        """
        Optimize DataFrame memory usage with detailed reporting
        
        Args:
            df: DataFrame to optimize
            aggressive: Whether to apply aggressive optimization
            
        Returns:
            Memory-optimized DataFrame
        """
        if df.empty:
            return df
        
        original_memory = df.memory_usage(deep=True).sum()
        df_optimized = df.copy()
        
        try:
            # Convert object columns to categories for repeated values
            for col in df_optimized.select_dtypes(include=['object']).columns:
                unique_ratio = df_optimized[col].nunique() / len(df_optimized)
                if unique_ratio < 0.5:  # Less than 50% unique values
                    df_optimized[col] = df_optimized[col].astype('category')
            
            # Optimize integer columns
            for col in df_optimized.select_dtypes(include=['int64']).columns:
                col_min = df_optimized[col].min()
                col_max = df_optimized[col].max()
                
                if pd.isna(col_min) or pd.isna(col_max):
                    continue
                
                # Use smallest possible integer type
                if col_min >= 0:  # Unsigned integers
                    if col_max <= 255:
                        df_optimized[col] = df_optimized[col].astype('uint8')
                    elif col_max <= 65535:
                        df_optimized[col] = df_optimized[col].astype('uint16')
                    elif col_max <= 4294967295:
                        df_optimized[col] = df_optimized[col].astype('uint32')
                else:  # Signed integers
                    if col_min >= -128 and col_max <= 127:
                        df_optimized[col] = df_optimized[col].astype('int8')
                    elif col_min >= -32768 and col_max <= 32767:
                        df_optimized[col] = df_optimized[col].astype('int16')
                    elif col_min >= -2147483648 and col_max <= 2147483647:
                        df_optimized[col] = df_optimized[col].astype('int32')
            
            # Optimize float columns
            for col in df_optimized.select_dtypes(include=['float64']).columns:
                if aggressive:
                    # Check if values can fit in float32 without precision loss
                    df_temp = df_optimized[col].astype('float32')
                    if np.allclose(df_optimized[col].dropna(), df_temp.dropna(), equal_nan=True):
                        df_optimized[col] = df_temp
                else:
                    # Use pandas downcast
                    df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
            
            # Report memory savings
            optimized_memory = df_optimized.memory_usage(deep=True).sum()
            memory_reduction = original_memory - optimized_memory
            reduction_pct = (memory_reduction / original_memory) * 100 if original_memory > 0 else 0
            
            logger.info(f"Memory optimization: {original_memory/1024/1024:.2f}MB → "
                       f"{optimized_memory/1024/1024:.2f}MB ({reduction_pct:.1f}% reduction)")
            
        except Exception as e:
            logger.error(f"Error optimizing DataFrame memory: {e}")
            return df  # Return original if optimization fails
        
        return df_optimized
    
    @staticmethod
    def clear_session_memory(keep_essential: bool = True) -> int:
        """
        Clear memory used by session state with option to keep essential data
        
        Args:
            keep_essential: Whether to preserve essential session data
            
        Returns:
            Number of items cleared from session state
        """
        essential_keys = ['view_type', 'data_year', 'user_preferences'] if keep_essential else []
        
        cleared_count = 0
        keys_to_remove = []
        
        for key in st.session_state.keys():
            if key not in essential_keys:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            try:
                del st.session_state[key]
                cleared_count += 1
            except KeyError:
                pass  # Key was already removed
        
        # Force garbage collection after clearing
        MemoryManager.force_garbage_collection()
        
        logger.info(f"Cleared {cleared_count} items from session state")
        return cleared_count


@contextmanager
def memory_monitor(operation_name: str, auto_cleanup: bool = True):
    """
    Monitor memory usage during operations with automatic cleanup
    
    Args:
        operation_name: Name of the operation being monitored
        auto_cleanup: Whether to automatically run garbage collection if needed
        
    Yields:
        Memory monitoring context
    """
    # Get initial memory state
    start_memory = MemoryManager.get_memory_info()
    start_time = time.time()
    
    logger.info(f"Starting {operation_name} - Memory: {start_memory['process_memory']:.1f}MB")
    
    try:
        yield
    finally:
        # Get final memory state
        end_memory = MemoryManager.get_memory_info()
        end_time = time.time()
        
        duration = end_time - start_time
        memory_diff = end_memory['process_memory'] - start_memory['process_memory']
        
        # Log results
        if memory_diff > 100:  # More than 100MB increase
            logger.warning(f"High memory usage in {operation_name}: "
                          f"+{memory_diff:.1f}MB (duration: {duration:.2f}s)")
            
            if auto_cleanup:
                logger.info("Performing automatic memory cleanup")
                MemoryManager.force_garbage_collection()
                
                # Check if cleanup helped
                cleanup_memory = MemoryManager.get_memory_info()
                cleanup_reduction = end_memory['process_memory'] - cleanup_memory['process_memory']
                if cleanup_reduction > 0:
                    logger.info(f"Cleanup freed {cleanup_reduction:.1f}MB")
        else:
            logger.info(f"Completed {operation_name}: "
                       f"{memory_diff:+.1f}MB (duration: {duration:.2f}s)")


def memory_optimized(auto_cleanup: bool = True):
    """
    Decorator for memory optimization of functions
    
    Args:
        auto_cleanup: Whether to run garbage collection after function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with memory_monitor(func.__name__, auto_cleanup=auto_cleanup):
                result = func(*args, **kwargs)
                
                # Optimize DataFrame results
                if isinstance(result, pd.DataFrame):
                    result = MemoryManager.optimize_dataframe_memory_usage(result)
                elif isinstance(result, dict):
                    # Optimize DataFrames in dictionary results
                    for key, value in result.items():
                        if isinstance(value, pd.DataFrame):
                            result[key] = MemoryManager.optimize_dataframe_memory_usage(value)
                
                return result
        return wrapper
    return decorator


class LowMemoryDataProcessor:
    """
    Process large datasets in chunks to minimize memory usage
    """
    
    @staticmethod
    def process_in_chunks(
        df: pd.DataFrame,
        chunk_size: int = 10000,
        process_func: Callable = None
    ) -> pd.DataFrame:
        """
        Process large DataFrame in chunks to reduce memory usage
        
        Args:
            df: Large DataFrame to process
            chunk_size: Size of chunks to process
            process_func: Function to apply to each chunk
            
        Returns:
            Processed DataFrame
        """
        if len(df) <= chunk_size:
            return process_func(df) if process_func else df
        
        processed_chunks = []
        total_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size else 0)
        
        logger.info(f"Processing {len(df)} rows in {total_chunks} chunks of {chunk_size}")
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i + chunk_size].copy()
            
            if process_func:
                chunk = process_func(chunk)
            
            processed_chunks.append(chunk)
            
            # Log progress and check memory
            chunk_num = i // chunk_size + 1
            if chunk_num % 10 == 0 or chunk_num == total_chunks:
                memory_info = MemoryManager.get_memory_info()
                logger.info(f"Processed chunk {chunk_num}/{total_chunks} "
                           f"(Memory: {memory_info['process_memory']:.1f}MB)")
                
                # Force garbage collection every 10 chunks
                if chunk_num % 10 == 0:
                    MemoryManager.force_garbage_collection()
        
        # Combine results
        logger.info("Combining processed chunks")
        result = pd.concat(processed_chunks, ignore_index=True)
        
        # Clean up intermediate results
        del processed_chunks
        MemoryManager.force_garbage_collection()
        
        return result


def setup_memory_warnings():
    """Setup memory-related warnings and monitoring"""
    
    # Configure pandas to be more memory efficient
    pd.options.mode.copy_on_write = True
    
    # Filter out specific pandas warnings that can clutter logs
    warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)
    
    # Set up memory monitoring for large operations
    if PSUTIL_AVAILABLE:
        memory_info = MemoryManager.get_memory_info()
        logger.info(f"Memory monitoring initialized - Current usage: {memory_info['process_memory']:.1f}MB")
    else:
        logger.warning("Advanced memory monitoring unavailable (psutil not installed)")


# Initialize memory management when module is imported
setup_memory_warnings()