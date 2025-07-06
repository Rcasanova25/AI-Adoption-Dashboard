"""Cache management for expensive calculations.

This module provides caching functionality to improve performance
of repeated calculations, especially for Monte Carlo simulations
and complex financial computations.
"""

import hashlib
import json
import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple
import pickle
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching of calculation results."""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """Initialize cache manager.
        
        Args:
            max_size: Maximum number of items to cache
            ttl_seconds: Time to live for cache entries in seconds
        """
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._access_times: Dict[str, float] = {}
        self._hit_count = 0
        self._miss_count = 0
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a unique cache key for function call.
        
        Args:
            func_name: Name of the function
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Unique cache key
        """
        # Create a hashable representation
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        
        # Convert to JSON string for consistent hashing
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        
        # Generate hash
        return hashlib.md5(key_string.encode()).hexdigest()
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if exists and not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self._miss_count += 1
            return None
            
        value, timestamp = self._cache[key]
        
        # Check if expired
        if time.time() - timestamp > self.ttl_seconds:
            del self._cache[key]
            del self._access_times[key]
            self._miss_count += 1
            return None
            
        # Update access time
        self._access_times[key] = time.time()
        self._hit_count += 1
        
        logger.debug(f"Cache hit for key: {key[:8]}...")
        return value
        
    def set(self, key: str, value: Any) -> None:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        # Check if we need to evict items
        if len(self._cache) >= self.max_size:
            self._evict_lru()
            
        self._cache[key] = (value, time.time())
        self._access_times[key] = time.time()
        
        logger.debug(f"Cached result for key: {key[:8]}...")
        
    def _evict_lru(self) -> None:
        """Evict least recently used item from cache."""
        if not self._access_times:
            return
            
        # Find LRU item
        lru_key = min(self._access_times.items(), key=lambda x: x[1])[0]
        
        # Remove it
        del self._cache[lru_key]
        del self._access_times[lru_key]
        
        logger.debug(f"Evicted LRU item: {lru_key[:8]}...")
        
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._access_times.clear()
        self._hit_count = 0
        self._miss_count = 0
        logger.info("Cache cleared")
        
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self._hit_count + self._miss_count
        hit_rate = self._hit_count / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self._cache),
            'max_size': self.max_size,
            'hit_count': self._hit_count,
            'miss_count': self._miss_count,
            'hit_rate': hit_rate,
            'ttl_seconds': self.ttl_seconds
        }


# Global cache instance
_global_cache = CacheManager()


def cached(ttl_seconds: Optional[int] = None, 
          key_prefix: Optional[str] = None) -> Callable:
    """Decorator to cache function results.
    
    Args:
        ttl_seconds: Override default TTL for this function
        key_prefix: Optional prefix for cache keys
        
    Returns:
        Decorated function with caching
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _global_cache._generate_key(
                f"{key_prefix or ''}{func.__name__}", 
                args, 
                kwargs
            )
            
            # Try to get from cache
            cached_result = _global_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
                
            # Calculate result
            result = func(*args, **kwargs)
            
            # Cache it
            _global_cache.set(cache_key, result)
            
            return result
            
        # Add cache management methods
        wrapper.clear_cache = _global_cache.clear
        wrapper.get_cache_stats = _global_cache.get_stats
        
        return wrapper
    return decorator


class CalculationCache:
    """Specialized cache for financial calculations."""
    
    def __init__(self):
        """Initialize calculation cache."""
        self._npv_cache = CacheManager(max_size=500, ttl_seconds=1800)
        self._irr_cache = CacheManager(max_size=500, ttl_seconds=1800)
        self._monte_carlo_cache = CacheManager(max_size=100, ttl_seconds=3600)
        self._sensitivity_cache = CacheManager(max_size=200, ttl_seconds=3600)
        
    def cache_npv(self, cash_flows: list, discount_rate: float, 
                  initial_investment: float, result: float) -> None:
        """Cache NPV calculation result.
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate used
            initial_investment: Initial investment amount
            result: Calculated NPV
        """
        key = self._generate_npv_key(cash_flows, discount_rate, initial_investment)
        self._npv_cache.set(key, result)
        
    def get_npv(self, cash_flows: list, discount_rate: float, 
                initial_investment: float) -> Optional[float]:
        """Get cached NPV result if available.
        
        Args:
            cash_flows: List of cash flows
            discount_rate: Discount rate
            initial_investment: Initial investment amount
            
        Returns:
            Cached NPV or None
        """
        key = self._generate_npv_key(cash_flows, discount_rate, initial_investment)
        return self._npv_cache.get(key)
        
    def _generate_npv_key(self, cash_flows: list, discount_rate: float, 
                         initial_investment: float) -> str:
        """Generate cache key for NPV calculation."""
        return self._npv_cache._generate_key(
            'npv',
            (tuple(cash_flows), discount_rate, initial_investment),
            {}
        )
        
    def cache_monte_carlo(self, base_case: dict, variables: list, 
                         iterations: int, result: dict) -> None:
        """Cache Monte Carlo simulation result.
        
        Args:
            base_case: Base case parameters
            variables: List of scenario variables
            iterations: Number of iterations
            result: Simulation results
        """
        # Create hashable representation of variables
        var_repr = [(v.name, v.base_value, v.min_value, v.max_value, 
                    v.distribution) for v in variables]
        
        key = self._monte_carlo_cache._generate_key(
            'monte_carlo',
            (json.dumps(base_case, sort_keys=True), 
             json.dumps(var_repr, sort_keys=True),
             iterations),
            {}
        )
        self._monte_carlo_cache.set(key, result)
        
    def get_monte_carlo(self, base_case: dict, variables: list, 
                       iterations: int) -> Optional[dict]:
        """Get cached Monte Carlo result if available.
        
        Args:
            base_case: Base case parameters
            variables: List of scenario variables
            iterations: Number of iterations
            
        Returns:
            Cached results or None
        """
        # Create hashable representation of variables
        var_repr = [(v.name, v.base_value, v.min_value, v.max_value, 
                    v.distribution) for v in variables]
        
        key = self._monte_carlo_cache._generate_key(
            'monte_carlo',
            (json.dumps(base_case, sort_keys=True), 
             json.dumps(var_repr, sort_keys=True),
             iterations),
            {}
        )
        return self._monte_carlo_cache.get(key)
        
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all caches.
        
        Returns:
            Dictionary with stats for each cache type
        """
        return {
            'npv': self._npv_cache.get_stats(),
            'irr': self._irr_cache.get_stats(),
            'monte_carlo': self._monte_carlo_cache.get_stats(),
            'sensitivity': self._sensitivity_cache.get_stats()
        }
        
    def clear_all(self) -> None:
        """Clear all calculation caches."""
        self._npv_cache.clear()
        self._irr_cache.clear()
        self._monte_carlo_cache.clear()
        self._sensitivity_cache.clear()
        logger.info("All calculation caches cleared")


# Global calculation cache instance
calculation_cache = CalculationCache()


# Specialized decorators for common calculations
def cache_financial_calculation(func: Callable) -> Callable:
    """Decorator specifically for financial calculations."""
    return cached(ttl_seconds=1800, key_prefix='fin_')(func)


def cache_monte_carlo(func: Callable) -> Callable:
    """Decorator specifically for Monte Carlo simulations."""
    return cached(ttl_seconds=3600, key_prefix='mc_')(func)


def cache_sensitivity_analysis(func: Callable) -> Callable:
    """Decorator specifically for sensitivity analysis."""
    return cached(ttl_seconds=3600, key_prefix='sa_')(func)