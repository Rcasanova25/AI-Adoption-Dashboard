"""
API monitoring and health check system with performance analytics
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
import time
import statistics
from dataclasses import dataclass, field
from enum import Enum

from .models import HealthStatus, DataSourceConfig, APIResponse
from .api_client import APIClient, APIConnectionPool

logger = logging.getLogger(__name__)

class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MetricType(str, Enum):
    """Types of metrics collected"""
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    AVAILABILITY = "availability"

@dataclass
class MetricValue:
    """A single metric measurement"""
    timestamp: datetime
    value: float
    metric_type: MetricType
    source_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Alert:
    """System alert"""
    alert_id: str
    source_id: str
    severity: AlertSeverity
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceThresholds:
    """Performance monitoring thresholds"""
    max_response_time: float = 30.0  # seconds
    min_success_rate: float = 95.0   # percentage
    max_error_rate: float = 5.0      # percentage
    min_availability: float = 99.0   # percentage
    alert_after_failures: int = 3    # consecutive failures before alert

class PerformanceMetrics:
    """Collects and analyzes performance metrics"""
    
    def __init__(self, retention_period: timedelta = timedelta(hours=24)):
        self.retention_period = retention_period
        self.metrics: Dict[str, List[MetricValue]] = {}
        self._lock = asyncio.Lock()
    
    async def record_metric(self, metric: MetricValue):
        """Record a performance metric"""
        async with self._lock:
            if metric.source_id not in self.metrics:
                self.metrics[metric.source_id] = []
            
            self.metrics[metric.source_id].append(metric)
            
            # Clean old metrics
            await self._cleanup_old_metrics(metric.source_id)
    
    async def _cleanup_old_metrics(self, source_id: str):
        """Remove old metrics beyond retention period"""
        cutoff_time = datetime.utcnow() - self.retention_period
        self.metrics[source_id] = [
            m for m in self.metrics[source_id] 
            if m.timestamp > cutoff_time
        ]
    
    async def get_metrics(
        self, 
        source_id: str, 
        metric_type: Optional[MetricType] = None,
        time_range: Optional[timedelta] = None
    ) -> List[MetricValue]:
        """Get metrics for a source"""
        async with self._lock:
            if source_id not in self.metrics:
                return []
            
            metrics = self.metrics[source_id]
            
            # Filter by metric type
            if metric_type:
                metrics = [m for m in metrics if m.metric_type == metric_type]
            
            # Filter by time range
            if time_range:
                cutoff_time = datetime.utcnow() - time_range
                metrics = [m for m in metrics if m.timestamp > cutoff_time]
            
            return sorted(metrics, key=lambda m: m.timestamp)
    
    async def calculate_statistics(
        self, 
        source_id: str, 
        metric_type: MetricType,
        time_range: timedelta = timedelta(hours=1)
    ) -> Dict[str, float]:
        """Calculate statistical measures for metrics"""
        metrics = await self.get_metrics(source_id, metric_type, time_range)
        
        if not metrics:
            return {}
        
        values = [m.value for m in metrics]
        
        stats = {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values)
        }
        
        if len(values) > 1:
            stats['stdev'] = statistics.stdev(values)
            stats['p95'] = self._percentile(values, 95)
            stats['p99'] = self._percentile(values, 99)
        
        return stats
    
    def _percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile value"""
        sorted_values = sorted(values)
        index = (percentile / 100) * (len(sorted_values) - 1)
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(sorted_values) - 1)
        
        if lower_index == upper_index:
            return sorted_values[lower_index]
        
        # Interpolate between values
        weight = index - lower_index
        return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight

class AlertManager:
    """Manages system alerts and notifications"""
    
    def __init__(self):
        self.alerts: Dict[str, Alert] = {}
        self.alert_handlers: List[Callable[[Alert], Any]] = []
        self._alert_counter = 0
        self._lock = asyncio.Lock()
    
    def add_alert_handler(self, handler: Callable[[Alert], Any]):
        """Add an alert notification handler"""
        self.alert_handlers.append(handler)
    
    def remove_alert_handler(self, handler: Callable[[Alert], Any]):
        """Remove an alert notification handler"""
        if handler in self.alert_handlers:
            self.alert_handlers.remove(handler)
    
    async def create_alert(
        self, 
        source_id: str, 
        severity: AlertSeverity,
        message: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Alert:
        """Create a new alert"""
        async with self._lock:
            self._alert_counter += 1
            alert_id = f"alert_{self._alert_counter}_{int(time.time())}"
            
            alert = Alert(
                alert_id=alert_id,
                source_id=source_id,
                severity=severity,
                message=message,
                metadata=metadata or {}
            )
            
            self.alerts[alert_id] = alert
            
            # Notify handlers
            await self._notify_handlers(alert)
            
            return alert
    
    async def _notify_handlers(self, alert: Alert):
        """Notify all alert handlers"""
        tasks = []
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(handler(alert))
                else:
                    loop = asyncio.get_event_loop()
                    tasks.append(loop.run_in_executor(None, handler, alert))
            except Exception as e:
                logger.error(f"Error creating task for alert handler: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        async with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].acknowledged = True
                return True
            return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        async with self._lock:
            if alert_id in self.alerts:
                self.alerts[alert_id].resolved = True
                return True
            return False
    
    async def get_active_alerts(self, source_id: Optional[str] = None) -> List[Alert]:
        """Get active (unresolved) alerts"""
        async with self._lock:
            alerts = [a for a in self.alerts.values() if not a.resolved]
            
            if source_id:
                alerts = [a for a in alerts if a.source_id == source_id]
            
            return sorted(alerts, key=lambda a: a.timestamp, reverse=True)
    
    async def cleanup_old_alerts(self, max_age: timedelta = timedelta(days=7)):
        """Remove old resolved alerts"""
        cutoff_time = datetime.utcnow() - max_age
        
        async with self._lock:
            to_remove = [
                alert_id for alert_id, alert in self.alerts.items()
                if alert.resolved and alert.timestamp < cutoff_time
            ]
            
            for alert_id in to_remove:
                del self.alerts[alert_id]

class HealthChecker:
    """Performs health checks on data sources"""
    
    def __init__(self, pool: APIConnectionPool):
        self.pool = pool
        self.health_states: Dict[str, HealthStatus] = {}
        self.thresholds: Dict[str, PerformanceThresholds] = {}
        self._lock = asyncio.Lock()
    
    def set_thresholds(self, source_id: str, thresholds: PerformanceThresholds):
        """Set performance thresholds for a source"""
        self.thresholds[source_id] = thresholds
    
    async def check_health(self, config: DataSourceConfig) -> HealthStatus:
        """Perform health check for a data source"""
        start_time = time.time()
        
        try:
            client = await self.pool.get_client(config)
            is_healthy = await client.health_check()
            response_time = time.time() - start_time
            
            async with self._lock:
                current_status = self.health_states.get(
                    config.source_id, 
                    HealthStatus(source_id=config.source_id)
                )
                
                # Update health status
                current_status.is_healthy = is_healthy
                current_status.response_time = response_time
                current_status.last_check = datetime.utcnow()
                
                if is_healthy:
                    current_status.consecutive_failures = 0
                else:
                    current_status.consecutive_failures += 1
                    current_status.issues.append(f"Health check failed at {current_status.last_check}")
                
                # Calculate uptime percentage (simplified)
                # In a real implementation, this would track uptime over time
                if current_status.consecutive_failures > 0:
                    current_status.uptime_percentage = max(0, 100 - (current_status.consecutive_failures * 10))
                else:
                    current_status.uptime_percentage = 100.0
                
                self.health_states[config.source_id] = current_status
                
                return current_status
        
        except Exception as e:
            logger.error(f"Health check error for {config.source_id}: {e}")
            
            async with self._lock:
                error_status = self.health_states.get(
                    config.source_id,
                    HealthStatus(source_id=config.source_id)
                )
                
                error_status.is_healthy = False
                error_status.last_check = datetime.utcnow()
                error_status.consecutive_failures += 1
                error_status.issues.append(f"Exception: {str(e)}")
                error_status.uptime_percentage = max(0, 100 - (error_status.consecutive_failures * 10))
                
                self.health_states[config.source_id] = error_status
                
                return error_status
    
    async def get_health_status(self, source_id: str) -> Optional[HealthStatus]:
        """Get current health status for a source"""
        async with self._lock:
            return self.health_states.get(source_id)
    
    async def get_all_health_statuses(self) -> Dict[str, HealthStatus]:
        """Get health statuses for all sources"""
        async with self._lock:
            return self.health_states.copy()

class APIMonitor:
    """Main API monitoring coordinator"""
    
    def __init__(self, pool: APIConnectionPool):
        self.pool = pool
        self.metrics = PerformanceMetrics()
        self.alerts = AlertManager()
        self.health_checker = HealthChecker(pool)
        self._monitoring_tasks: Dict[str, asyncio.Task] = {}
        self._monitoring_configs: Dict[str, DataSourceConfig] = {}
        self._stop_event = asyncio.Event()
        
    async def start_monitoring(self, config: DataSourceConfig):
        """Start monitoring a data source"""
        if config.source_id in self._monitoring_tasks:
            logger.warning(f"Already monitoring {config.source_id}")
            return
        
        self._monitoring_configs[config.source_id] = config
        
        # Set default thresholds
        thresholds = PerformanceThresholds()
        self.health_checker.set_thresholds(config.source_id, thresholds)
        
        # Start monitoring task
        task = asyncio.create_task(self._monitoring_loop(config))
        self._monitoring_tasks[config.source_id] = task
        
        logger.info(f"Started monitoring for {config.source_id}")
    
    async def stop_monitoring(self, source_id: str):
        """Stop monitoring a data source"""
        if source_id in self._monitoring_tasks:
            task = self._monitoring_tasks[source_id]
            task.cancel()
            
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            del self._monitoring_tasks[source_id]
            del self._monitoring_configs[source_id]
            
            logger.info(f"Stopped monitoring for {source_id}")
    
    async def stop_all_monitoring(self):
        """Stop all monitoring tasks"""
        self._stop_event.set()
        
        tasks = list(self._monitoring_tasks.values())
        if tasks:
            for task in tasks:
                task.cancel()
            
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self._monitoring_tasks.clear()
        self._monitoring_configs.clear()
    
    async def _monitoring_loop(self, config: DataSourceConfig):
        """Main monitoring loop for a data source"""
        while not self._stop_event.is_set():
            try:
                # Perform health check
                health_status = await self.health_checker.check_health(config)
                
                # Record metrics
                await self._record_health_metrics(config.source_id, health_status)
                
                # Check for alerts
                await self._check_alerts(config.source_id, health_status)
                
                # Wait for next check
                await asyncio.sleep(config.health_check_interval.total_seconds())
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop for {config.source_id}: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _record_health_metrics(self, source_id: str, health_status: HealthStatus):
        """Record health metrics"""
        timestamp = datetime.utcnow()
        
        # Response time metric
        if health_status.response_time is not None:
            await self.metrics.record_metric(MetricValue(
                timestamp=timestamp,
                value=health_status.response_time,
                metric_type=MetricType.RESPONSE_TIME,
                source_id=source_id
            ))
        
        # Availability metric
        await self.metrics.record_metric(MetricValue(
            timestamp=timestamp,
            value=1.0 if health_status.is_healthy else 0.0,
            metric_type=MetricType.AVAILABILITY,
            source_id=source_id
        ))
        
        # Success rate (based on uptime percentage)
        await self.metrics.record_metric(MetricValue(
            timestamp=timestamp,
            value=health_status.uptime_percentage,
            metric_type=MetricType.SUCCESS_RATE,
            source_id=source_id
        ))
    
    async def _check_alerts(self, source_id: str, health_status: HealthStatus):
        """Check if alerts should be triggered"""
        thresholds = self.health_checker.thresholds.get(source_id)
        if not thresholds:
            return
        
        # Check consecutive failures
        if health_status.consecutive_failures >= thresholds.alert_after_failures:
            await self.alerts.create_alert(
                source_id=source_id,
                severity=AlertSeverity.ERROR,
                message=f"Source {source_id} has failed {health_status.consecutive_failures} consecutive health checks",
                metadata={'consecutive_failures': health_status.consecutive_failures}
            )
        
        # Check response time
        if (health_status.response_time is not None and 
            health_status.response_time > thresholds.max_response_time):
            await self.alerts.create_alert(
                source_id=source_id,
                severity=AlertSeverity.WARNING,
                message=f"High response time: {health_status.response_time:.2f}s (threshold: {thresholds.max_response_time}s)",
                metadata={'response_time': health_status.response_time}
            )
        
        # Check uptime percentage
        if health_status.uptime_percentage < thresholds.min_availability:
            await self.alerts.create_alert(
                source_id=source_id,
                severity=AlertSeverity.CRITICAL,
                message=f"Low availability: {health_status.uptime_percentage:.1f}% (threshold: {thresholds.min_availability}%)",
                metadata={'uptime_percentage': health_status.uptime_percentage}
            )
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive monitoring data for dashboard"""
        health_statuses = await self.health_checker.get_all_health_statuses()
        active_alerts = await self.alerts.get_active_alerts()
        
        # Calculate summary statistics
        total_sources = len(health_statuses)
        healthy_sources = sum(1 for h in health_statuses.values() if h.is_healthy)
        
        dashboard_data = {
            'summary': {
                'total_sources': total_sources,
                'healthy_sources': healthy_sources,
                'unhealthy_sources': total_sources - healthy_sources,
                'total_alerts': len(active_alerts),
                'critical_alerts': len([a for a in active_alerts if a.severity == AlertSeverity.CRITICAL])
            },
            'health_statuses': {sid: {
                'is_healthy': status.is_healthy,
                'response_time': status.response_time,
                'uptime_percentage': status.uptime_percentage,
                'consecutive_failures': status.consecutive_failures,
                'last_check': status.last_check.isoformat() if status.last_check else None
            } for sid, status in health_statuses.items()},
            'recent_alerts': [{
                'alert_id': alert.alert_id,
                'source_id': alert.source_id,
                'severity': alert.severity.value,
                'message': alert.message,
                'timestamp': alert.timestamp.isoformat(),
                'acknowledged': alert.acknowledged
            } for alert in active_alerts[:10]]  # Last 10 alerts
        }
        
        return dashboard_data

# Global monitor instance
_global_monitor: Optional[APIMonitor] = None

async def get_global_monitor(pool: Optional[APIConnectionPool] = None) -> APIMonitor:
    """Get the global API monitor instance"""
    global _global_monitor
    if _global_monitor is None:
        if pool is None:
            from .api_client import get_global_pool
            pool = await get_global_pool()
        _global_monitor = APIMonitor(pool)
    return _global_monitor

async def cleanup_global_monitor():
    """Cleanup the global API monitor"""
    global _global_monitor
    if _global_monitor:
        await _global_monitor.stop_all_monitoring()
        _global_monitor = None