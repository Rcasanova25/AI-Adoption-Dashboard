"""Multi-layer caching system for performance optimization."""

import os
import json
import time
import hashlib
import pickle
import threading
from pathlib import Path
from typing import Any, Dict, Optional, Callable, Tuple
from datetime import datetime, timedelta
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class TTLCache:
    """Time-based cache with TTL (Time To Live) support."""
    
    def __init__(self, maxsize: int = 128, ttl: int = 300):
        """Initialize TTL cache.
        
        Args:
            maxsize: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache = OrderedDict()
        self._lock = threading.RLock()
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get item from cache."""
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if time.time() < expiry:
                    # Move to end (LRU behavior)
                    self._cache.move_to_end(key)
                    self._stats['hits'] += 1
                    return value
                else:
                    # Expired
                    del self._cache[key]
            
            self._stats['misses'] += 1
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set item in cache."""
        with self._lock:
            # Use provided TTL or default
            item_ttl = ttl if ttl is not None else self.ttl
            expiry = time.time() + item_ttl
            
            # Check size limit
            if key not in self._cache and len(self._cache) >= self.maxsize:
                # Evict oldest item
                self._cache.popitem(last=False)
                self._stats['evictions'] += 1
            
            self._cache[key] = (value, expiry)
            self._cache.move_to_end(key)
    
    def delete(self, key: str) -> bool:
        """Delete item from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all items from cache."""
        with self._lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._lock:
            total = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total if total > 0 else 0
            return {
                **self._stats,
                'size': len(self._cache),
                'hit_rate': hit_rate
            }


class DiskCache:
    """Disk-based cache for large datasets."""
    
    def __init__(self, cache_dir: str = './cache', size_limit: int = 1024**3):
        """Initialize disk cache.
        
        Args:
            cache_dir: Directory for cache files
            size_limit: Maximum cache size in bytes (default 1GB)
        """
        self.cache_dir = Path(cache_dir)
        self.size_limit = size_limit
        self.cache_dir.mkdir(exist_ok=True)
        self._index = self._load_index()
        self._lock = threading.RLock()
    
    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """Load cache index from disk."""
        index_file = self.cache_dir / '.cache_index.json'
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_index(self) -> None:
        """Save cache index to disk."""
        index_file = self.cache_dir / '.cache_index.json'
        with open(index_file, 'w') as f:
            json.dump(self._index, f)
    
    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Hash key to avoid filesystem issues
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.pkl"
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get item from disk cache."""
        with self._lock:
            if key in self._index:
                info = self._index[key]
                
                # Check expiry
                if 'expiry' in info and time.time() > info['expiry']:
                    self.delete(key)
                    return default
                
                # Load from disk
                cache_path = self._get_cache_path(key)
                if cache_path.exists():
                    try:
                        with open(cache_path, 'rb') as f:
                            return pickle.load(f)
                    except Exception as e:
                        logger.error(f"Error loading cache file {cache_path}: {e}")
                        self.delete(key)
            
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set item in disk cache."""
        with self._lock:
            cache_path = self._get_cache_path(key)
            
            # Serialize to disk
            try:
                with open(cache_path, 'wb') as f:
                    pickle.dump(value, f)
                
                # Update index
                self._index[key] = {
                    'size': cache_path.stat().st_size,
                    'created': time.time(),
                    'expiry': time.time() + ttl if ttl else None
                }
                
                # Check size limit
                self._enforce_size_limit()
                
                # Save index
                self._save_index()
                
            except Exception as e:
                logger.error(f"Error saving to disk cache: {e}")
                if cache_path.exists():
                    cache_path.unlink()
    
    def delete(self, key: str) -> bool:
        """Delete item from disk cache."""
        with self._lock:
            if key in self._index:
                cache_path = self._get_cache_path(key)
                if cache_path.exists():
                    cache_path.unlink()
                del self._index[key]
                self._save_index()
                return True
            return False
    
    def _enforce_size_limit(self) -> None:
        """Remove old items if size limit exceeded."""
        total_size = sum(info['size'] for info in self._index.values())
        
        if total_size > self.size_limit:
            # Sort by creation time (oldest first)
            items = sorted(
                self._index.items(),
                key=lambda x: x[1]['created']
            )
            
            # Remove oldest items until under limit
            for key, info in items:
                if total_size <= self.size_limit:
                    break
                self.delete(key)
                total_size -= info['size']
    
    def clear(self) -> None:
        """Clear all items from disk cache."""
        with self._lock:
            for key in list(self._index.keys()):
                self.delete(key)
            self._index.clear()
            self._save_index()


class MultiLayerCache:
    """Multi-layer caching system with memory and disk tiers."""
    
    def __init__(self, 
                 memory_size: int = 100,
                 memory_ttl: int = 300,
                 disk_dir: str = './cache',
                 disk_size: int = 1024**3):
        """Initialize multi-layer cache.
        
        Args:
            memory_size: Max items in memory cache
            memory_ttl: Default TTL for memory cache (seconds)
            disk_dir: Directory for disk cache
            disk_size: Max disk cache size in bytes
        """
        self.memory_cache = TTLCache(maxsize=memory_size, ttl=memory_ttl)
        self.disk_cache = DiskCache(cache_dir=disk_dir, size_limit=disk_size)
        self._lock = threading.RLock()
    
    def get(self, key: str, loader: Optional[Callable] = None) -> Any:
        """Get item from cache with automatic loading.
        
        Args:
            key: Cache key
            loader: Optional function to load data if not cached
            
        Returns:
            Cached value or loaded value
        """
        # Check memory cache first
        value = self.memory_cache.get(key)
        if value is not None:
            return value
        
        # Check disk cache
        value = self.disk_cache.get(key)
        if value is not None:
            # Promote to memory cache
            self.memory_cache.set(key, value)
            return value
        
        # Load if loader provided
        if loader:
            value = loader()
            if value is not None:
                self.set(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: Any, 
            memory_ttl: Optional[int] = None,
            disk_ttl: Optional[int] = None,
            disk_only: bool = False) -> None:
        """Set item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            memory_ttl: TTL for memory cache
            disk_ttl: TTL for disk cache
            disk_only: Skip memory cache
        """
        with self._lock:
            # Store in memory cache unless disk_only
            if not disk_only:
                self.memory_cache.set(key, value, ttl=memory_ttl)
            
            # Store large objects in disk cache
            # Estimate size (simplified)
            try:
                import sys
                size = sys.getsizeof(value)
                if size > 1024 * 1024:  # > 1MB
                    self.disk_cache.set(key, value, ttl=disk_ttl)
            except:
                # If size check fails, store anyway
                self.disk_cache.set(key, value, ttl=disk_ttl)
    
    def delete(self, key: str) -> bool:
        """Delete from all cache layers."""
        with self._lock:
            memory_deleted = self.memory_cache.delete(key)
            disk_deleted = self.disk_cache.delete(key)
            return memory_deleted or disk_deleted
    
    def clear(self) -> None:
        """Clear all cache layers."""
        with self._lock:
            self.memory_cache.clear()
            self.disk_cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics from all cache layers."""
        return {
            'memory': self.memory_cache.get_stats(),
            'disk': {
                'items': len(self.disk_cache._index),
                'size': sum(info['size'] for info in self.disk_cache._index.values())
            }
        }


class CacheKeyGenerator:
    """Generate intelligent cache keys based on context."""
    
    @staticmethod
    def generate(prefix: str, 
                 params: Dict[str, Any],
                 context: Optional[Dict[str, Any]] = None) -> str:
        """Generate cache key from parameters.
        
        Args:
            prefix: Key prefix (e.g., 'data', 'chart')
            params: Parameters that affect the cached value
            context: Additional context (e.g., user persona)
            
        Returns:
            Cache key string
        """
        # Sort params for consistent keys
        sorted_params = sorted(params.items())
        
        # Add context if provided
        if context:
            sorted_params.extend(sorted(context.items()))
        
        # Create hash of parameters
        param_str = json.dumps(sorted_params, sort_keys=True, default=str)
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        
        return f"{prefix}:{param_hash}"
    
    @staticmethod
    def generate_data_key(source: str, dataset: str, 
                         filters: Optional[Dict] = None,
                         version: Optional[str] = None) -> str:
        """Generate cache key for data requests."""
        params = {
            'source': source,
            'dataset': dataset,
            'filters': filters or {},
            'version': version or 'latest'
        }
        return CacheKeyGenerator.generate('data', params)
    
    @staticmethod
    def generate_chart_key(chart_type: str, data_key: str,
                          options: Optional[Dict] = None) -> str:
        """Generate cache key for charts."""
        params = {
            'type': chart_type,
            'data': data_key,
            'options': options or {}
        }
        return CacheKeyGenerator.generate('chart', params)


# Global cache instance
_cache_instance = None


def get_cache() -> MultiLayerCache:
    """Get global cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = MultiLayerCache()
    return _cache_instance


def cache_result(prefix: str = 'result', 
                ttl: int = 300,
                key_params: Optional[List[str]] = None):
    """Decorator to cache function results.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
        key_params: Parameter names to include in cache key
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_params:
                params = {k: kwargs.get(k) for k in key_params if k in kwargs}
            else:
                # Use all kwargs
                params = kwargs
            
            cache_key = CacheKeyGenerator.generate(
                f"{prefix}:{func.__name__}",
                params
            )
            
            # Get from cache
            cache = get_cache()
            result = cache.get(cache_key)
            
            if result is None:
                # Execute function
                result = func(*args, **kwargs)
                # Cache result
                cache.set(cache_key, result, memory_ttl=ttl)
            
            return result
        
        return wrapper
    return decorator