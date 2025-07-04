"""Optimized data manager with multi-layer caching and lazy loading."""

import asyncio
import concurrent.futures
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import pandas as pd
import logging
from datetime import datetime

from data.data_manager import DataManager
from data.models import DataSource
from performance.cache_manager import (
    MultiLayerCache, CacheKeyGenerator, cache_result, get_cache
)
from performance.monitor import (
    track_performance, PerformanceContext, get_metrics
)

logger = logging.getLogger(__name__)


class OptimizedDataManager(DataManager):
    """Enhanced data manager with performance optimizations."""
    
    def __init__(self, 
                 cache_memory_size: int = 200,
                 cache_memory_ttl: int = 600,
                 cache_disk_size: int = 2 * 1024**3,
                 max_workers: int = 4):
        """Initialize optimized data manager.
        
        Args:
            cache_memory_size: Max items in memory cache
            cache_memory_ttl: Default TTL for memory cache (seconds)
            cache_disk_size: Max disk cache size in bytes
            max_workers: Max concurrent workers for parallel loading
        """
        super().__init__()
        
        # Initialize enhanced cache
        self.cache = MultiLayerCache(
            memory_size=cache_memory_size,
            memory_ttl=cache_memory_ttl,
            disk_size=cache_disk_size
        )
        
        # Thread pool for parallel operations
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        
        # Lazy loading configuration
        self.lazy_load_enabled = True
        self._loaded_sources = set()
        
        # Progress tracking
        self._loading_progress = {}
    
    @track_performance('data_load', threshold=1.0)
    def get_data(self, source_name: str, 
                 force_refresh: bool = False) -> Dict[str, pd.DataFrame]:
        """Get data from a specific source with caching.
        
        Args:
            source_name: Name of the data source
            force_refresh: Force reload from source
            
        Returns:
            Dictionary of DataFrames
        """
        # Generate cache key
        cache_key = CacheKeyGenerator.generate_data_key(
            source=source_name,
            dataset='all',
            version=self._get_data_version()
        )
        
        # Check cache unless forced refresh
        if not force_refresh:
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                logger.debug(f"Cache hit for {source_name}")
                return cached_data
        
        # Load data with performance tracking
        with PerformanceContext(f'load_{source_name}'):
            if source_name not in self.loaders:
                logger.warning(f"Unknown data source: {source_name}")
                return {}
            
            try:
                # Load data
                loader = self.loaders[source_name]
                data = loader.load()
                
                # Cache the result
                self.cache.set(
                    cache_key, 
                    data,
                    memory_ttl=600,  # 10 minutes in memory
                    disk_ttl=3600    # 1 hour on disk
                )
                
                # Mark as loaded
                self._loaded_sources.add(source_name)
                
                return data
                
            except Exception as e:
                logger.error(f"Error loading data from {source_name}: {e}")
                return {}
    
    def get_all_data_async(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Load all data sources asynchronously."""
        return asyncio.run(self._load_all_async())
    
    async def _load_all_async(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Async implementation of parallel data loading."""
        tasks = []
        
        # Create async tasks for each loader
        async def load_source_async(source_name: str):
            """Load a single source asynchronously."""
            loop = asyncio.get_event_loop()
            return source_name, await loop.run_in_executor(
                self.executor, 
                self.get_data, 
                source_name
            )
        
        # Create tasks for all sources
        for source_name in self.loaders.keys():
            task = asyncio.create_task(load_source_async(source_name))
            tasks.append(task)
        
        # Track progress
        results = {}
        completed = 0
        total = len(tasks)
        
        # Process completed tasks as they finish
        for coro in asyncio.as_completed(tasks):
            source_name, data = await coro
            results[source_name] = data
            completed += 1
            
            # Update progress
            self._loading_progress['completed'] = completed
            self._loading_progress['total'] = total
            self._loading_progress['percent'] = (completed / total) * 100
            
            logger.info(f"Loaded {source_name} ({completed}/{total})")
        
        return results
    
    @track_performance('dataset_combine', threshold=0.5)
    def get_combined_dataset(self, dataset_name: str, 
                           sources: Optional[List[str]] = None) -> pd.DataFrame:
        """Get combined dataset from multiple sources with optimization.
        
        Args:
            dataset_name: Name of the dataset to retrieve
            sources: List of sources to combine (None for all)
            
        Returns:
            Combined DataFrame
        """
        # Generate cache key
        cache_key = CacheKeyGenerator.generate_data_key(
            source='combined',
            dataset=dataset_name,
            filters={'sources': sources}
        )
        
        # Check cache
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Determine sources
        if sources is None:
            sources = list(self.loaders.keys())
        
        # Load data in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(self._get_dataset_from_source, source, dataset_name): source
                for source in sources
            }
            
            # Combine results
            dataframes = []
            for future in concurrent.futures.as_completed(futures):
                source = futures[future]
                try:
                    df = future.result()
                    if df is not None and not df.empty:
                        df['source'] = source
                        dataframes.append(df)
                except Exception as e:
                    logger.error(f"Error loading {dataset_name} from {source}: {e}")
        
        # Combine DataFrames efficiently
        if dataframes:
            combined = self._efficient_concat(dataframes)
            
            # Cache result
            self.cache.set(cache_key, combined, memory_ttl=300)
            
            return combined
        
        return pd.DataFrame()
    
    def _get_dataset_from_source(self, source: str, dataset_name: str) -> Optional[pd.DataFrame]:
        """Get specific dataset from a source."""
        data = self.get_data(source)
        return data.get(dataset_name)
    
    @staticmethod
    def _efficient_concat(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        """Efficiently concatenate DataFrames."""
        if not dataframes:
            return pd.DataFrame()
        
        # Use concat with ignore_index for better performance
        combined = pd.concat(dataframes, ignore_index=True, sort=False)
        
        # Optimize memory usage
        for col in combined.columns:
            col_type = combined[col].dtype
            
            # Downcast numeric types
            if col_type != 'object':
                try:
                    if 'int' in str(col_type):
                        combined[col] = pd.to_numeric(combined[col], downcast='integer')
                    elif 'float' in str(col_type):
                        combined[col] = pd.to_numeric(combined[col], downcast='float')
                except:
                    pass
        
        return combined
    
    def preload_critical_data(self, sources: List[str]) -> None:
        """Preload critical data sources for better performance."""
        logger.info(f"Preloading {len(sources)} critical data sources")
        
        # Load in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.get_data, source)
                for source in sources
            ]
            
            # Wait for completion
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error preloading data: {e}")
    
    def get_loading_progress(self) -> Dict[str, Any]:
        """Get current loading progress."""
        return self._loading_progress.copy()
    
    def _get_data_version(self) -> str:
        """Get current data version for cache invalidation."""
        # In production, this could check file modification times
        # or data source versions
        return datetime.now().strftime("%Y%m%d")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = self.cache.get_stats()
        stats['loaded_sources'] = list(self._loaded_sources)
        return stats
    
    def optimize_memory(self) -> None:
        """Optimize memory usage by clearing old cached data."""
        # Clear memory cache of old items
        self.cache.memory_cache.clear()
        
        # Force garbage collection
        import gc
        gc.collect()
        
        logger.info("Memory optimization completed")
    
    def __del__(self):
        """Cleanup on deletion."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)


class LazyDataLoader:
    """Lazy loader for individual data sources."""
    
    def __init__(self, loader_class, source: DataSource):
        """Initialize lazy loader.
        
        Args:
            loader_class: Class of the loader
            source: Data source configuration
        """
        self.loader_class = loader_class
        self.source = source
        self._loader = None
        self._data = None
        self._loading = False
    
    @track_performance('lazy_load', threshold=2.0)
    def load(self) -> Dict[str, pd.DataFrame]:
        """Load data lazily."""
        if self._data is not None:
            return self._data
        
        if self._loading:
            # Wait for loading to complete
            import time
            while self._loading:
                time.sleep(0.1)
            return self._data or {}
        
        # Start loading
        self._loading = True
        try:
            # Initialize loader if needed
            if self._loader is None:
                self._loader = self.loader_class(self.source)
            
            # Load data
            self._data = self._loader.load()
            return self._data
            
        finally:
            self._loading = False
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata without loading full data."""
        if self._loader is None:
            self._loader = self.loader_class(self.source)
        
        # Return basic metadata
        return {
            'source': self.source.name,
            'type': self.source.type,
            'year': self.source.year,
            'loaded': self._data is not None
        }


def create_optimized_manager() -> OptimizedDataManager:
    """Factory function to create optimized data manager."""
    manager = OptimizedDataManager()
    
    # Preload critical sources for better initial performance
    critical_sources = ['ai_index', 'mckinsey', 'goldman_sachs']
    manager.preload_critical_data(critical_sources)
    
    return manager