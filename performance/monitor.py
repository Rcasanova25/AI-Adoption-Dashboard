"""Performance monitoring and metrics collection system."""

import functools
import json
import logging
import statistics
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Collect and analyze performance metrics."""

    def __init__(self, window_size: int = 1000):
        """Initialize metrics collector.

        Args:
            window_size: Number of recent measurements to keep
        """
        self.window_size = window_size
        self._metrics = defaultdict(lambda: deque(maxlen=window_size))
        self._errors = defaultdict(int)
        self._lock = threading.RLock()
        self._thresholds = {
            "data_load": 1.0,
            "view_render": 0.5,
            "chart_render": 0.3,
            "cache_get": 0.01,
            "cache_set": 0.05,
            "pdf_extract": 2.0,
            "api_call": 1.0,
        }

    def record(self, operation: str, duration: float, metadata: Optional[Dict] = None) -> None:
        """Record a performance measurement.

        Args:
            operation: Name of the operation
            duration: Duration in seconds
            metadata: Additional metadata
        """
        with self._lock:
            measurement = {
                "duration": duration,
                "timestamp": time.time(),
                "metadata": metadata or {},
            }
            self._metrics[operation].append(measurement)

            # Check threshold
            threshold = self._thresholds.get(operation, 1.0)
            if duration > threshold:
                logger.warning(
                    f"Slow operation detected: {operation} took {duration:.3f}s "
                    f"(threshold: {threshold}s)"
                )

    def record_error(self, operation: str, error: str) -> None:
        """Record an error for an operation."""
        with self._lock:
            self._errors[operation] += 1
            logger.error(f"Error in {operation}: {error}")

    def get_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for an operation.

        Returns:
            Dict with min, max, mean, median, p95, p99
        """
        with self._lock:
            measurements = self._metrics.get(operation, [])
            if not measurements:
                return {}

            durations = [m["duration"] for m in measurements]

            return {
                "count": len(durations),
                "min": min(durations),
                "max": max(durations),
                "mean": statistics.mean(durations),
                "median": statistics.median(durations),
                "p95": self._percentile(durations, 95),
                "p99": self._percentile(durations, 99),
                "errors": self._errors.get(operation, 0),
                "threshold": self._thresholds.get(operation, 1.0),
            }

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all operations."""
        with self._lock:
            return {op: self.get_stats(op) for op in self._metrics.keys()}

    def get_slow_operations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slowest recent operations."""
        with self._lock:
            all_ops = []

            for operation, measurements in self._metrics.items():
                threshold = self._thresholds.get(operation, 1.0)
                for m in measurements:
                    if m["duration"] > threshold:
                        all_ops.append(
                            {
                                "operation": operation,
                                "duration": m["duration"],
                                "timestamp": m["timestamp"],
                                "threshold": threshold,
                                "excess": m["duration"] - threshold,
                            }
                        )

            # Sort by excess time over threshold
            all_ops.sort(key=lambda x: x["excess"], reverse=True)
            return all_ops[:limit]

    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data."""
        if not data:
            return 0

        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

    def set_threshold(self, operation: str, threshold: float) -> None:
        """Set performance threshold for an operation."""
        self._thresholds[operation] = threshold

    def export_metrics(self) -> str:
        """Export metrics as JSON."""
        with self._lock:
            data = {
                "timestamp": datetime.now().isoformat(),
                "stats": self.get_all_stats(),
                "slow_operations": self.get_slow_operations(),
                "thresholds": self._thresholds,
            }
            return json.dumps(data, indent=2)


# Global metrics instance
_metrics_instance = None


def get_metrics() -> PerformanceMetrics:
    """Get global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = PerformanceMetrics()
    return _metrics_instance


def track_performance(
    operation: str = None,
    threshold: Optional[float] = None,
    metadata_func: Optional[Callable] = None,
):
    """Decorator to track function performance.

    Args:
        operation: Operation name (defaults to function name)
        threshold: Custom threshold for this operation
        metadata_func: Function to generate metadata from args/kwargs
    """

    def decorator(func):
        op_name = operation or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            metrics = get_metrics()

            # Set custom threshold if provided
            if threshold is not None:
                metrics.set_threshold(op_name, threshold)

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # Generate metadata if function provided
                metadata = None
                if metadata_func:
                    try:
                        metadata = metadata_func(*args, **kwargs)
                    except:
                        pass

                # Record success
                metrics.record(op_name, duration, metadata)

                return result

            except Exception as e:
                duration = time.time() - start_time

                # Record error
                metrics.record_error(op_name, str(e))

                # Still record duration for failed operations
                metrics.record(op_name, duration, {"error": True})

                raise

        return wrapper

    return decorator


class PerformanceContext:
    """Context manager for tracking performance of code blocks."""

    def __init__(self, operation: str, metadata: Optional[Dict] = None):
        """Initialize performance context.

        Args:
            operation: Name of the operation
            metadata: Additional metadata
        """
        self.operation = operation
        self.metadata = metadata or {}
        self.start_time = None

    def __enter__(self):
        """Enter context and start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and record metrics."""
        duration = time.time() - self.start_time
        metrics = get_metrics()

        if exc_type:
            # Error occurred
            metrics.record_error(self.operation, str(exc_val))
            self.metadata["error"] = True

        metrics.record(self.operation, duration, self.metadata)


class ResourceMonitor:
    """Monitor system resource usage."""

    def __init__(self):
        """Initialize resource monitor."""
        self._measurements = deque(maxlen=100)
        self._lock = threading.RLock()

        # Try to import resource monitoring libraries
        try:
            import psutil

            self.psutil = psutil
        except ImportError:
            logger.warning("psutil not available, resource monitoring limited")
            self.psutil = None

    def measure(self) -> Dict[str, Any]:
        """Measure current resource usage."""
        measurement = {
            "timestamp": time.time(),
            "memory": self._get_memory_usage(),
            "cpu": self._get_cpu_usage(),
        }

        with self._lock:
            self._measurements.append(measurement)

        return measurement

    def _get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage statistics."""
        if self.psutil:
            process = self.psutil.Process()
            memory_info = process.memory_info()
            return {"rss_mb": memory_info.rss / 1024 / 1024, "percent": process.memory_percent()}
        else:
            # Fallback to basic memory check
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            return {"rss_mb": usage.ru_maxrss / 1024, "percent": 0}  # May need adjustment per OS

    def _get_cpu_usage(self) -> Dict[str, float]:
        """Get CPU usage statistics."""
        if self.psutil:
            process = self.psutil.Process()
            return {"percent": process.cpu_percent(interval=0.1), "threads": process.num_threads()}
        else:
            return {"percent": 0, "threads": 1}

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of resource usage."""
        with self._lock:
            if not self._measurements:
                return {}

            memory_values = [m["memory"]["rss_mb"] for m in self._measurements]
            cpu_values = [m["cpu"]["percent"] for m in self._measurements]

            return {
                "memory": {
                    "current_mb": memory_values[-1] if memory_values else 0,
                    "peak_mb": max(memory_values) if memory_values else 0,
                    "avg_mb": statistics.mean(memory_values) if memory_values else 0,
                },
                "cpu": {
                    "current_percent": cpu_values[-1] if cpu_values else 0,
                    "peak_percent": max(cpu_values) if cpu_values else 0,
                    "avg_percent": statistics.mean(cpu_values) if cpu_values else 0,
                },
            }


def log_performance_report():
    """Log a performance report."""
    metrics = get_metrics()
    stats = metrics.get_all_stats()

    logger.info("=" * 60)
    logger.info("Performance Report")
    logger.info("=" * 60)

    for operation, op_stats in stats.items():
        if op_stats:
            logger.info(
                f"{operation}: "
                f"mean={op_stats['mean']:.3f}s, "
                f"p95={op_stats['p95']:.3f}s, "
                f"count={op_stats['count']}, "
                f"errors={op_stats['errors']}"
            )

    # Log slow operations
    slow_ops = metrics.get_slow_operations(5)
    if slow_ops:
        logger.info("\nSlowest Operations:")
        for op in slow_ops:
            logger.info(
                f"  {op['operation']}: {op['duration']:.3f}s " f"(threshold: {op['threshold']}s)"
            )


# Utility functions for common monitoring patterns


def monitor_data_load(source: str):
    """Create metadata function for data loading operations."""

    def metadata_func(*args, **kwargs):
        return {"source": source, "timestamp": time.time()}

    return metadata_func


def monitor_cache_operation(cache_type: str, operation: str):
    """Create metadata function for cache operations."""

    def metadata_func(*args, **kwargs):
        return {
            "cache_type": cache_type,
            "operation": operation,
            "key": args[0] if args else kwargs.get("key", "unknown"),
        }

    return metadata_func
