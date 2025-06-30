# performance/__init__.py
"""
Advanced Performance and Caching System for AI Adoption Dashboard

This module provides high-performance caching, data processing, monitoring,
and chart optimization capabilities to optimize dashboard performance and user experience.

Key Components:
- AdvancedCache: Multi-layer caching system (memory + disk)
- DataPipeline: High-performance data processing with caching
- AsyncDataLoader: Parallel data loading capabilities
- PerformanceMonitor: Real-time performance monitoring
- smart_cache: Decorator for automatic function caching
- ChartOptimizer: Advanced chart rendering optimization
- DataDownsampler: Intelligent data downsampling algorithms
- OptimizedCharts: Pre-optimized chart creation functions
- LazyChartLoader: Lazy loading system for charts
"""

from .caching import (
    AdvancedCache,
    CacheConfig,
    DataPipeline,
    AsyncDataLoader,
    PerformanceMonitor,
    smart_cache,
    _global_cache,
    performance_monitor,
    demo_advanced_caching
)

from .chart_optimization import (
    ChartConfig,
    DataDownsampler,
    ChartOptimizer,
    LazyChartLoader,
    OptimizedCharts,
    demo_chart_optimization
)

from .memory_management import (
    MemoryConfig,
    MemoryMonitor,
    DataFrameOptimizer,
    SessionStateManager,
    memory_profiler,
    memory_efficient_operation,
    demo_memory_management
)

__all__ = [
    'AdvancedCache',
    'CacheConfig', 
    'DataPipeline',
    'AsyncDataLoader',
    'PerformanceMonitor',
    'smart_cache',
    '_global_cache',
    'performance_monitor',
    'demo_advanced_caching',
    'ChartConfig',
    'DataDownsampler',
    'ChartOptimizer',
    'LazyChartLoader',
    'OptimizedCharts',
    'demo_chart_optimization',
    'MemoryConfig',
    'MemoryMonitor',
    'DataFrameOptimizer',
    'SessionStateManager',
    'memory_profiler',
    'memory_efficient_operation',
    'demo_memory_management'
]

__version__ = "1.1.0"
__author__ = "AI Adoption Dashboard Team" 