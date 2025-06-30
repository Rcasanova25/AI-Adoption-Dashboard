# performance/caching.py - Advanced Caching System
import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import pickle
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import functools
import json
import os

@dataclass
class CacheConfig:
    """Configuration for caching behavior"""
    ttl_seconds: int = 3600  # 1 hour default
    max_entries: int = 1000
    persist_to_disk: bool = False
    disk_cache_dir: str = "./cache"
    compression: bool = True
    invalidate_on_data_change: bool = True

class AdvancedCache:
    """Advanced caching system with multiple layers and strategies"""
    
    def __init__(self, config: CacheConfig = None):
        self.config = config or CacheConfig()
        self.memory_cache = {}
        self.cache_metadata = {}
        self.lock = threading.Lock()
        
        # Create disk cache directory if needed
        if self.config.persist_to_disk:
            os.makedirs(self.config.disk_cache_dir, exist_ok=True)
    
    def _generate_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate unique cache key for function call"""
        # Create hashable representation
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': sorted(kwargs.items())
        }
        
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached item is still valid"""
        if cache_key not in self.cache_metadata:
            return False
        
        metadata = self.cache_metadata[cache_key]
        
        # Check TTL
        if datetime.now() > metadata['expires_at']:
            return False
        
        # Check data freshness if enabled
        if self.config.invalidate_on_data_change:
            if metadata.get('data_hash') != self._get_current_data_hash():
                return False
        
        return True
    
    def _get_current_data_hash(self) -> str:
        """Get hash of current data state for invalidation"""
        # This would be customized based on your data sources
        # For now, we'll use a simple timestamp-based approach
        if hasattr(st.session_state, 'data_last_modified'):
            return str(st.session_state.data_last_modified)
        return str(int(time.time() / 300))  # 5-minute buckets
    
    def _store_to_disk(self, cache_key: str, data: Any) -> None:
        """Store data to disk cache"""
        if not self.config.persist_to_disk:
            return
        
        try:
            file_path = os.path.join(self.config.disk_cache_dir, f"{cache_key}.pkl")
            
            if self.config.compression:
                import gzip
                with gzip.open(file_path, 'wb') as f:
                    pickle.dump(data, f)
            else:
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)
        except Exception as e:
            print(f"Warning: Failed to store to disk cache: {e}")
    
    def _load_from_disk(self, cache_key: str) -> Optional[Any]:
        """Load data from disk cache"""
        if not self.config.persist_to_disk:
            return None
        
        try:
            file_path = os.path.join(self.config.disk_cache_dir, f"{cache_key}.pkl")
            
            if not os.path.exists(file_path):
                return None
            
            if self.config.compression:
                import gzip
                with gzip.open(file_path, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            print(f"Warning: Failed to load from disk cache: {e}")
            return None
    
    def get(self, cache_key: str) -> Optional[Any]:
        """Get item from cache"""
        with self.lock:
            # Check memory cache first
            if cache_key in self.memory_cache and self._is_cache_valid(cache_key):
                return self.memory_cache[cache_key]
            
            # Check disk cache
            disk_data = self._load_from_disk(cache_key)
            if disk_data is not None and self._is_cache_valid(cache_key):
                # Restore to memory cache
                self.memory_cache[cache_key] = disk_data
                return disk_data
            
            return None
    
    def set(self, cache_key: str, data: Any) -> None:
        """Store item in cache"""
        with self.lock:
            # Clean up old entries if needed
            if len(self.memory_cache) >= self.config.max_entries:
                self._cleanup_old_entries()
            
            # Store in memory
            self.memory_cache[cache_key] = data
            
            # Store metadata
            self.cache_metadata[cache_key] = {
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=self.config.ttl_seconds),
                'data_hash': self._get_current_data_hash(),
                'size_bytes': len(pickle.dumps(data))
            }
            
            # Store to disk
            self._store_to_disk(cache_key, data)
    
    def _cleanup_old_entries(self) -> None:
        """Remove old entries from cache"""
        # Remove expired entries first
        expired_keys = [
            key for key in self.cache_metadata
            if not self._is_cache_valid(key)
        ]
        
        for key in expired_keys:
            self.memory_cache.pop(key, None)
            self.cache_metadata.pop(key, None)
        
        # If still too many, remove oldest
        if len(self.memory_cache) >= self.config.max_entries:
            sorted_keys = sorted(
                self.cache_metadata.keys(),
                key=lambda k: self.cache_metadata[k]['created_at']
            )
            
            keys_to_remove = sorted_keys[:len(self.memory_cache) - self.config.max_entries + 100]
            for key in keys_to_remove:
                self.memory_cache.pop(key, None)
                self.cache_metadata.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cached data"""
        with self.lock:
            self.memory_cache.clear()
            self.cache_metadata.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_size = sum(
                metadata['size_bytes']
                for metadata in self.cache_metadata.values()
            )
            
            return {
                'entries': len(self.memory_cache),
                'total_size_mb': total_size / 1024 / 1024,
                'hit_rate': getattr(self, '_hit_rate', 0),
                'miss_rate': getattr(self, '_miss_rate', 0),
                'oldest_entry': min(
                    (metadata['created_at'] for metadata in self.cache_metadata.values()),
                    default=None
                ),
                'config': self.config
            }

# Global cache instance
_global_cache = AdvancedCache()

def smart_cache(
    ttl: int = 3600,
    max_entries: int = 100,
    persist: bool = False,
    key_func: Optional[Callable] = None
):
    """Enhanced caching decorator with advanced features"""
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = _global_cache._generate_cache_key(func.__name__, args, kwargs)
            
            # Try to get from cache
            cached_result = _global_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Store in cache with metadata
            _global_cache.set(cache_key, result)
            
            # Log performance metrics
            if execution_time > 1.0:  # Log slow operations
                st.warning(f"⚠️ Slow operation detected: {func.__name__} took {execution_time:.2f}s")
            
            return result
        
        return wrapper
    return decorator

class DataPipeline:
    """High-performance data processing pipeline with caching"""
    
    def __init__(self):
        self.cache = AdvancedCache(CacheConfig(
            ttl_seconds=7200,  # 2 hours for data processing
            max_entries=50,
            persist_to_disk=True,
            compression=True
        ))
    
    @smart_cache(ttl=7200, persist=True)
    def load_and_process_data(self, data_source: str, filters: dict = None) -> pd.DataFrame:
        """Load and process data with intelligent caching"""
        print(f"Loading data from {data_source} with filters: {filters}")
        
        # Simulate data loading
        if data_source == "historical_ai_data":
            return self._load_historical_data(filters)
        elif data_source == "sector_analysis":
            return self._load_sector_data(filters)
        elif data_source == "investment_trends":
            return self._load_investment_data(filters)
        else:
            raise ValueError(f"Unknown data source: {data_source}")
    
    def _load_historical_data(self, filters: dict = None) -> pd.DataFrame:
        """Load historical AI adoption data"""
        # Simulate expensive data loading operation
        time.sleep(0.1)  # Simulate network/database latency
        
        # Generate sample data
        years = range(2017, 2026)
        data = []
        
        for year in years:
            adoption_rate = min(95, 5 + (year - 2017) * 8 + np.random.normal(0, 2))
            genai_rate = max(0, min(80, (year - 2021) * 20 + np.random.normal(0, 3)))
            
            data.append({
                'year': year,
                'ai_use': max(0, adoption_rate),
                'genai_use': max(0, genai_rate),
                'confidence_level': 0.85 + np.random.normal(0, 0.05)
            })
        
        df = pd.DataFrame(data)
        
        # Apply filters if provided
        if filters:
            if 'year_min' in filters:
                df = df[df['year'] >= filters['year_min']]
            if 'year_max' in filters:
                df = df[df['year'] <= filters['year_max']]
        
        return df
    
    def _load_sector_data(self, filters: dict = None) -> pd.DataFrame:
        """Load sector-specific adoption data"""
        time.sleep(0.15)  # Simulate processing time
        
        sectors = [
            'Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
            'Retail', 'Education', 'Energy', 'Government', 'Media', 'Transportation'
        ]
        
        data = []
        for sector in sectors:
            # Generate realistic sector data
            base_adoption = {
                'Technology': 92, 'Financial Services': 85, 'Healthcare': 78,
                'Manufacturing': 75, 'Retail': 72, 'Education': 65,
                'Energy': 58, 'Government': 52, 'Media': 68, 'Transportation': 62
            }
            
            adoption = base_adoption.get(sector, 60) + np.random.normal(0, 3)
            roi = 2.0 + (adoption - 50) * 0.04 + np.random.normal(0, 0.2)
            
            data.append({
                'sector': sector,
                'adoption_rate': max(0, min(100, adoption)),
                'avg_roi': max(1.0, roi),
                'genai_adoption': max(0, adoption - 10 + np.random.normal(0, 5)),
                'implementation_time': 6 + np.random.normal(0, 2)
            })
        
        df = pd.DataFrame(data)
        
        # Apply sector filters
        if filters and 'sectors' in filters:
            df = df[df['sector'].isin(filters['sectors'])]
        
        return df
    
    def _load_investment_data(self, filters: dict = None) -> pd.DataFrame:
        """Load AI investment trend data"""
        time.sleep(0.08)
        
        years = range(2020, 2026)
        data = []
        
        base_investment = 50
        for i, year in enumerate(years):
            total = base_investment * (1.4 ** i) + np.random.normal(0, 10)
            genai = max(0, total * 0.15 * (i - 1)) if i > 1 else 0
            
            data.append({
                'year': year,
                'total_investment': max(0, total),
                'genai_investment': genai,
                'private_investment': total * 0.8,
                'public_investment': total * 0.2
            })
        
        return pd.DataFrame(data)

class AsyncDataLoader:
    """Asynchronous data loading for improved performance"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def load_multiple_datasets(self, data_requests: List[Dict]) -> Dict[str, pd.DataFrame]:
        """Load multiple datasets asynchronously"""
        
        pipeline = DataPipeline()
        
        # Submit all requests
        futures = {}
        for request in data_requests:
            future = self.executor.submit(
                pipeline.load_and_process_data,
                request['source'],
                request.get('filters', {})
            )
            futures[request['name']] = future
        
        # Collect results
        results = {}
        for name, future in futures.items():
            try:
                results[name] = future.result(timeout=30)
            except Exception as e:
                st.error(f"Failed to load {name}: {str(e)}")
                results[name] = pd.DataFrame()  # Return empty DataFrame on error
        
        return results
    
    def load_data_with_progress(self, data_requests: List[Dict]) -> Dict[str, pd.DataFrame]:
        """Load data with progress indicator"""
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        pipeline = DataPipeline()
        results = {}
        
        for i, request in enumerate(data_requests):
            status_text.text(f"Loading {request['name']}...")
            
            try:
                results[request['name']] = pipeline.load_and_process_data(
                    request['source'],
                    request.get('filters', {})
                )
            except Exception as e:
                st.error(f"Failed to load {request['name']}: {str(e)}")
                results[request['name']] = pd.DataFrame()
            
            progress_bar.progress((i + 1) / len(data_requests))
        
        status_text.text("Data loading complete!")
        time.sleep(0.5)  # Brief pause to show completion
        status_text.empty()
        progress_bar.empty()
        
        return results

# Performance monitoring utilities
class PerformanceMonitor:
    """Monitor and report performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End timing and record metric"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.metrics[operation] = duration
            del self.start_times[operation]
            return duration
        return 0.0
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        cache_stats = _global_cache.get_stats()
        
        return {
            'operation_times': self.metrics,
            'cache_performance': cache_stats,
            'total_operations': len(self.metrics),
            'avg_operation_time': np.mean(list(self.metrics.values())) if self.metrics else 0,
            'slowest_operation': max(self.metrics.items(), key=lambda x: x[1]) if self.metrics else None
        }
    
    def render_performance_sidebar(self) -> None:
        """Render performance metrics in sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### ⚡ Performance")
            
            report = self.get_performance_report()
            
            # Cache statistics
            cache_stats = report['cache_performance']
            st.metric("Cache Entries", cache_stats['entries'])
            st.metric("Cache Size", f"{cache_stats['total_size_mb']:.1f} MB")
            
            # Operation performance
            if report['avg_operation_time'] > 0:
                st.metric("Avg Operation", f"{report['avg_operation_time']:.2f}s")
            
            # Performance alerts
            if report['avg_operation_time'] > 2.0:
                st.warning("⚠️ Some operations are slow")
            elif report['avg_operation_time'] > 0:
                st.success("✅ Good performance")

# Global performance monitor
performance_monitor = PerformanceMonitor()

# Usage examples and testing
def demo_advanced_caching():
    """Demonstrate advanced caching capabilities"""
    
    st.title("⚡ Advanced Caching & Performance Demo")
    
    # Performance monitor
    performance_monitor.render_performance_sidebar()
    
    st.markdown("### Data Loading Performance Test")
    
    # Test different caching scenarios
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Load Historical Data", type="primary"):
            performance_monitor.start_timer("historical_load")
            
            pipeline = DataPipeline()
            data = pipeline.load_and_process_data("historical_ai_data")
            
            duration = performance_monitor.end_timer("historical_load")
            
            st.success(f"✅ Loaded {len(data)} rows in {duration:.2f}s")
            st.dataframe(data.head())
    
    with col2:
        if st.button("Load Sector Data", type="secondary"):
            performance_monitor.start_timer("sector_load")
            
            pipeline = DataPipeline()
            data = pipeline.load_and_process_data("sector_analysis")
            
            duration = performance_monitor.end_timer("sector_load")
            
            st.success(f"✅ Loaded {len(data)} sectors in {duration:.2f}s")
            st.dataframe(data)
    
    # Async loading demo
    st.markdown("### Parallel Data Loading")
    
    if st.button("Load All Data Async", type="primary"):
        async_loader = AsyncDataLoader()
        
        data_requests = [
            {"name": "historical", "source": "historical_ai_data"},
            {"name": "sectors", "source": "sector_analysis"},
            {"name": "investments", "source": "investment_trends"}
        ]
        
        performance_monitor.start_timer("async_load_all")
        datasets = async_loader.load_data_with_progress(data_requests)
        duration = performance_monitor.end_timer("async_load_all")
        
        st.success(f"✅ Loaded all datasets in {duration:.2f}s")
        
        for name, data in datasets.items():
            st.write(f"**{name.title()}**: {len(data)} rows")
    
    # Cache statistics
    st.markdown("### Cache Performance")
    cache_stats = _global_cache.get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cache Entries", cache_stats['entries'])
    with col2:
        st.metric("Total Size", f"{cache_stats['total_size_mb']:.1f} MB")
    with col3:
        if st.button("Clear Cache"):
            _global_cache.clear()
            st.success("Cache cleared!")
    
    # Performance report
    st.markdown("### Performance Report")
    report = performance_monitor.get_performance_report()
    st.json(report)

if __name__ == "__main__":
    demo_advanced_caching() 