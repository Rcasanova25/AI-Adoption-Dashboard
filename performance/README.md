# Performance Module - Advanced Caching & Optimization

This module provides high-performance caching, data processing, and monitoring capabilities for the AI Adoption Dashboard.

## 🚀 Features

### Advanced Caching System
- **Multi-layer caching**: Memory + disk storage
- **Smart invalidation**: Automatic cache invalidation on data changes
- **Configurable TTL**: Time-to-live settings for cache entries
- **Compression**: Optional gzip compression for disk storage
- **Thread-safe**: Concurrent access support

### Data Pipeline
- **High-performance processing**: Optimized data loading and processing
- **Caching integration**: Automatic caching of expensive operations
- **Filter support**: Flexible data filtering capabilities
- **Error handling**: Robust error recovery

### Async Loading
- **Parallel processing**: Load multiple datasets simultaneously
- **Progress tracking**: Real-time progress indicators
- **Resource management**: Configurable worker pools
- **Timeout handling**: Automatic timeout and retry logic

### Performance Monitoring
- **Real-time metrics**: Operation timing and cache statistics
- **Performance alerts**: Automatic detection of slow operations
- **Optimization recommendations**: Data-driven performance tips
- **Sidebar integration**: Built-in Streamlit sidebar widgets

## 📦 Installation

The performance module is included with the main dashboard. No additional installation required.

## 🔧 Usage

### Basic Caching

```python
from performance import smart_cache

@smart_cache(ttl=3600, persist=True)
def expensive_operation(data):
    # This function will be cached for 1 hour
    return process_data(data)
```

### Advanced Cache Configuration

```python
from performance import AdvancedCache, CacheConfig

config = CacheConfig(
    ttl_seconds=7200,        # 2 hours
    max_entries=1000,        # Max cache entries
    persist_to_disk=True,    # Enable disk storage
    compression=True,        # Enable compression
    invalidate_on_data_change=True
)

cache = AdvancedCache(config)
```

### Data Pipeline

```python
from performance import DataPipeline

pipeline = DataPipeline()

# Load data with caching
data = pipeline.load_and_process_data("historical_ai_data", filters={
    'year_min': 2020,
    'year_max': 2025
})
```

### Async Loading

```python
from performance import AsyncDataLoader

loader = AsyncDataLoader(max_workers=4)

data_requests = [
    {"name": "historical", "source": "historical_ai_data"},
    {"name": "sectors", "source": "sector_analysis"},
    {"name": "investments", "source": "investment_trends"}
]

# Load all datasets in parallel
datasets = loader.load_data_with_progress(data_requests)
```

### Performance Monitoring

```python
from performance import performance_monitor

# Start timing an operation
performance_monitor.start_timer("my_operation")

# ... perform operation ...

# End timing and get duration
duration = performance_monitor.end_timer("my_operation")

# Get performance report
report = performance_monitor.get_performance_report()

# Display in sidebar
performance_monitor.render_performance_sidebar()
```

## 🎯 Integration with Main Dashboard

The performance module is automatically integrated into the main dashboard:

1. **Automatic caching** of data loading operations
2. **Performance monitoring** in the sidebar
3. **Async data loading** for improved responsiveness
4. **Cache statistics** and management tools

## 📊 Performance Benefits

- **10-50x faster** data loading with caching
- **Parallel processing** for multiple datasets
- **Memory optimization** with disk persistence
- **Real-time monitoring** of performance metrics
- **Automatic optimization** recommendations

## 🔍 Monitoring & Debugging

### Cache Statistics
```python
from performance import _global_cache

stats = _global_cache.get_stats()
print(f"Cache entries: {stats['entries']}")
print(f"Cache size: {stats['total_size_mb']:.1f} MB")
```

### Performance Reports
```python
from performance import performance_monitor

report = performance_monitor.get_performance_report()
print(f"Average operation time: {report['avg_operation_time']:.2f}s")
print(f"Slowest operation: {report['slowest_operation']}")
```

### Cache Management
```python
# Clear all cached data
_global_cache.clear()

# Check cache validity
is_valid = _global_cache._is_cache_valid(cache_key)
```

## 🧪 Testing

Run the performance demo:

```bash
streamlit run performance_demo.py
```

Or test individual components:

```python
from performance import demo_advanced_caching

# Run full demo
demo_advanced_caching()
```

## 📈 Configuration Options

### CacheConfig Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ttl_seconds` | 3600 | Cache entry time-to-live in seconds |
| `max_entries` | 1000 | Maximum number of cache entries |
| `persist_to_disk` | False | Enable disk persistence |
| `disk_cache_dir` | "./cache" | Directory for disk cache |
| `compression` | True | Enable gzip compression |
| `invalidate_on_data_change` | True | Auto-invalidate on data changes |

### Smart Cache Decorator

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ttl` | 3600 | Cache TTL in seconds |
| `max_entries` | 100 | Max entries for this function |
| `persist` | False | Enable disk persistence |
| `key_func` | None | Custom cache key function |

## 🚨 Performance Alerts

The system automatically detects and alerts on:

- **Slow operations** (>1 second execution time)
- **High memory usage** (>100MB cache size)
- **Low cache hit rates** (<50%)
- **Failed operations** with error recovery

## 🔧 Advanced Usage

### Custom Cache Keys
```python
def custom_key_func(*args, **kwargs):
    # Create custom cache key based on specific parameters
    return f"custom_{hash(str(args))}_{hash(str(kwargs))}"

@smart_cache(key_func=custom_key_func)
def my_function(data, options=None):
    return process_data(data, options)
```

### Cache Invalidation
```python
# Manual cache invalidation
_global_cache.clear()

# Update data modification timestamp
st.session_state.data_last_modified = time.time()
```

### Performance Optimization
```python
# Use filters to reduce data size
data = pipeline.load_and_process_data("historical_ai_data", {
    'year_min': 2023,
    'sectors': ['Technology', 'Finance']
})

# Parallel loading for multiple sources
loader = AsyncDataLoader(max_workers=8)
datasets = loader.load_multiple_datasets(data_requests)
```

## 📚 API Reference

### Classes

- `AdvancedCache`: Multi-layer caching system
- `CacheConfig`: Cache configuration dataclass
- `DataPipeline`: High-performance data processing
- `AsyncDataLoader`: Parallel data loading
- `PerformanceMonitor`: Performance monitoring and reporting

### Functions

- `smart_cache()`: Decorator for function caching
- `demo_advanced_caching()`: Demo application

### Global Instances

- `_global_cache`: Global cache instance
- `performance_monitor`: Global performance monitor

## 🤝 Contributing

When contributing to the performance module:

1. **Test performance impact** of changes
2. **Update cache keys** when data structures change
3. **Monitor memory usage** in long-running applications
4. **Document new features** with examples
5. **Add performance tests** for new functionality

## 📄 License

This module is part of the AI Adoption Dashboard project. 