"""Cache management utilities for the AI Adoption Dashboard.

This module provides caching decorators and cache management functionality
to improve performance for expensive calculations.
"""

import functools
import hashlib
import json
import time
from typing import Any, Callable, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Simple in-memory cache manager with TTL support."""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """Initialize cache manager.
        
        Args:
            max_size: Maximum number of items to store in cache
            default_ttl: Default time-to-live in seconds
        """
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        
    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create a cache key from function name and arguments."""
        # Convert args and kwargs to a string representation
        key_data = {
            'func': func_name,
            'args': str(args),
            'kwargs': str(sorted(kwargs.items()))
        }
        key_str = json.dumps(key_data, sort_keys=True)
        # Create a hash for the key
        return hashlib.sha256(key_str.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and is not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.default_ttl:
                self.hits += 1
                return value
            else:
                # Expired, remove from cache
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache with current timestamp."""
        # Check cache size and evict oldest if necessary
        if len(self.cache) >= self.max_size:
            # Simple eviction: remove oldest entry
            oldest_key = min(self.cache.keys(), 
                           key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache),
            'max_size': self.max_size
        }


# Global cache instances
calculation_cache = CacheManager(max_size=500, default_ttl=1800)  # 30 minutes
monte_carlo_cache = CacheManager(max_size=100, default_ttl=3600)  # 1 hour


def cache_financial_calculation(ttl: Optional[int] = None):
    """Decorator to cache financial calculation results.
    
    Args:
        ttl: Time-to-live in seconds (uses default if not specified)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = calculation_cache._make_key(func.__name__, args, kwargs)
            
            # Check cache
            cached_result = calculation_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Calculate result
            logger.debug(f"Cache miss for {func.__name__}, calculating...")
            result = func(*args, **kwargs)
            
            # Store in cache
            calculation_cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


def cache_monte_carlo(ttl: Optional[int] = None):
    """Decorator specifically for Monte Carlo simulations with longer TTL.
    
    Args:
        ttl: Time-to-live in seconds (uses default if not specified)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = monte_carlo_cache._make_key(func.__name__, args, kwargs)
            
            # Check cache
            cached_result = monte_carlo_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Monte Carlo cache hit for {func.__name__}")
                return cached_result
            
            # Run simulation
            logger.debug(f"Monte Carlo cache miss for {func.__name__}, running simulation...")
            result = func(*args, **kwargs)
            
            # Store in cache
            monte_carlo_cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


def clear_all_caches():
    """Clear all cache instances."""
    calculation_cache.clear()
    monte_carlo_cache.clear()
    logger.info("All caches cleared")


def get_cache_statistics() -> Dict[str, Dict[str, Any]]:
    """Get statistics for all cache instances."""
    return {
        'calculation_cache': calculation_cache.get_stats(),
        'monte_carlo_cache': monte_carlo_cache.get_stats()
    }