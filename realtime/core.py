"""
Core real-time data integration components
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable, Set
from datetime import datetime, timedelta
import json
import weakref
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from .models import (
    DataSourceConfig, DataRecord, DataStreamState, DataStatus,
    APIResponse, DataChangeEvent, validate_data_against_rules
)
from .api_client import APIClient, APIConnectionPool, get_global_pool

logger = logging.getLogger(__name__)

@dataclass
class DataStreamMetrics:
    """Metrics for a data stream"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_records: int = 0
    avg_response_time: float = 0.0
    last_update: Optional[datetime] = None
    uptime_percentage: float = 100.0

class DataStream:
    """Represents a real-time data stream from a source"""
    
    def __init__(self, config: DataSourceConfig, pool: Optional[APIConnectionPool] = None):
        self.config = config
        self.pool = pool
        self.state = DataStreamState(source_id=config.source_id)
        self.metrics = DataStreamMetrics()
        self._client: Optional[APIClient] = None
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._data_cache: Dict[str, DataRecord] = {}
        self._subscribers: Set[Callable] = set()
        self._lock = asyncio.Lock()
        
    async def start(self):
        """Start the data stream"""
        if self._task is not None:
            logger.warning(f"Data stream {self.config.source_id} is already running")
            return
        
        logger.info(f"Starting data stream for {self.config.source_id}")
        self.state.status = DataStatus.LOADING
        self._stop_event.clear()
        
        # Get connection pool
        if self.pool is None:
            self.pool = await get_global_pool()
        
        # Get API client
        self._client = await self.pool.get_client(self.config)
        
        # Start the streaming task
        self._task = asyncio.create_task(self._stream_loop())
        
    async def stop(self):
        """Stop the data stream"""
        if self._task is None:
            return
        
        logger.info(f"Stopping data stream for {self.config.source_id}")
        self._stop_event.set()
        
        try:
            await asyncio.wait_for(self._task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning(f"Force cancelling data stream for {self.config.source_id}")
            self._task.cancel()
        
        self._task = None
        self.state.status = DataStatus.PENDING
    
    async def _stream_loop(self):
        """Main streaming loop"""
        while not self._stop_event.is_set():
            try:
                await self._fetch_data()
                
                # Wait for next update
                if self.config.real_time:
                    await asyncio.sleep(1.0)  # Real-time mode: check every second
                else:
                    # Wait for the configured interval
                    await asyncio.sleep(self.config.update_interval.total_seconds())
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in stream loop for {self.config.source_id}: {e}")
                self.state.status = DataStatus.ERROR
                self.state.error_message = str(e)
                self.state.error_count += 1
                await asyncio.sleep(min(30, 5 * self.state.error_count))  # Backoff
    
    async def _fetch_data(self):
        """Fetch data from the source"""
        if not self._client:
            return
        
        start_time = datetime.utcnow()
        
        try:
            # Make API request
            response = await self._client.get()
            
            # Update metrics
            self.metrics.total_requests += 1
            response_time = (datetime.utcnow() - start_time).total_seconds()
            
            if response.is_success:
                self.metrics.successful_requests += 1
                await self._process_successful_response(response)
            else:
                self.metrics.failed_requests += 1
                await self._process_failed_response(response)
            
            # Update average response time
            self.metrics.avg_response_time = (
                (self.metrics.avg_response_time * (self.metrics.total_requests - 1) + response_time) /
                self.metrics.total_requests
            )
            
        except Exception as e:
            logger.error(f"Error fetching data for {self.config.source_id}: {e}")
            self.metrics.failed_requests += 1
            self.state.status = DataStatus.ERROR
            self.state.error_message = str(e)
            self.state.error_count += 1
    
    async def _process_successful_response(self, response: APIResponse):
        """Process a successful API response"""
        if not response.data:
            return
        
        try:
            # Validate data
            if self.config.validation_rules:
                errors = validate_data_against_rules(response.data, self.config.validation_rules)
                if errors:
                    logger.warning(f"Data validation errors for {self.config.source_id}: {errors}")
                    self.state.status = DataStatus.ERROR
                    self.state.error_message = f"Validation errors: {', '.join(errors)}"
                    return
            
            # Apply data mapping if configured
            processed_data = self._apply_data_mapping(response.data)
            
            # Create data record
            record = DataRecord(
                source_id=self.config.source_id,
                data=processed_data,
                metadata={
                    'response_time': response.response_time,
                    'status_code': response.status_code,
                    'headers': response.headers
                }
            )
            
            # Check for changes
            old_record = self._data_cache.get(self.config.source_id)
            if old_record and old_record.data != record.data:
                # Data changed - notify subscribers
                change_event = DataChangeEvent(
                    source_id=self.config.source_id,
                    change_type="update",
                    old_data=old_record.data,
                    new_data=record.data,
                    changed_fields=self._find_changed_fields(old_record.data, record.data)
                )
                await self._notify_subscribers(change_event)
            
            # Update cache
            async with self._lock:
                self._data_cache[self.config.source_id] = record
            
            # Update state
            self.state.status = DataStatus.SUCCESS
            self.state.last_update = datetime.utcnow()
            self.state.last_success = self.state.last_update
            self.state.total_records += 1
            self.state.error_count = 0  # Reset error count on success
            self.state.error_message = None
            
            self.metrics.total_records += 1
            self.metrics.last_update = self.state.last_update
            
        except Exception as e:
            logger.error(f"Error processing response for {self.config.source_id}: {e}")
            self.state.status = DataStatus.ERROR
            self.state.error_message = str(e)
    
    async def _process_failed_response(self, response: APIResponse):
        """Process a failed API response"""
        self.state.status = DataStatus.ERROR
        self.state.last_error = datetime.utcnow()
        self.state.error_message = response.error or f"HTTP {response.status_code}"
        self.state.error_count += 1
        
        logger.warning(f"API request failed for {self.config.source_id}: {self.state.error_message}")
    
    def _apply_data_mapping(self, data: Any) -> Dict[str, Any]:
        """Apply data mapping configuration"""
        if not self.config.data_mapping or not isinstance(data, dict):
            return data if isinstance(data, dict) else {"raw_data": data}
        
        mapped_data = {}
        for target_field, source_path in self.config.data_mapping.items():
            try:
                # Simple dot notation support
                value = data
                for key in source_path.split('.'):
                    if isinstance(value, dict):
                        value = value.get(key)
                    elif isinstance(value, list) and key.isdigit():
                        idx = int(key)
                        value = value[idx] if 0 <= idx < len(value) else None
                    else:
                        value = None
                        break
                
                if value is not None:
                    mapped_data[target_field] = value
                    
            except Exception as e:
                logger.warning(f"Error mapping field {target_field} from {source_path}: {e}")
        
        return mapped_data
    
    def _find_changed_fields(self, old_data: Dict[str, Any], new_data: Dict[str, Any]) -> List[str]:
        """Find fields that changed between old and new data"""
        changed_fields = []
        
        all_keys = set(old_data.keys()) | set(new_data.keys())
        for key in all_keys:
            old_value = old_data.get(key)
            new_value = new_data.get(key)
            if old_value != new_value:
                changed_fields.append(key)
        
        return changed_fields
    
    async def _notify_subscribers(self, event: DataChangeEvent):
        """Notify all subscribers of a data change"""
        if not self._subscribers:
            return
        
        # Create tasks for all subscribers
        tasks = []
        for subscriber in self._subscribers.copy():  # Copy to avoid modification during iteration
            try:
                if asyncio.iscoroutinefunction(subscriber):
                    tasks.append(subscriber(event))
                else:
                    # Run sync function in thread pool
                    loop = asyncio.get_event_loop()
                    tasks.append(loop.run_in_executor(None, subscriber, event))
            except Exception as e:
                logger.error(f"Error creating task for subscriber: {e}")
        
        # Execute all notifications concurrently
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logger.error(f"Error notifying subscribers: {e}")
    
    def subscribe(self, callback: Callable[[DataChangeEvent], Any]):
        """Subscribe to data change events"""
        self._subscribers.add(callback)
    
    def unsubscribe(self, callback: Callable[[DataChangeEvent], Any]):
        """Unsubscribe from data change events"""
        self._subscribers.discard(callback)
    
    async def get_latest_data(self) -> Optional[DataRecord]:
        """Get the latest data record"""
        async with self._lock:
            return self._data_cache.get(self.config.source_id)
    
    def get_state(self) -> DataStreamState:
        """Get current stream state"""
        return self.state
    
    def get_metrics(self) -> DataStreamMetrics:
        """Get stream metrics"""
        return self.metrics

class RealtimeDataManager:
    """Manages multiple real-time data streams"""
    
    def __init__(self, pool: Optional[APIConnectionPool] = None):
        self.pool = pool
        self.streams: Dict[str, DataStream] = {}
        self._global_subscribers: Set[Callable] = set()
        self._lock = asyncio.Lock()
        
    async def start(self):
        """Start the data manager"""
        if self.pool is None:
            self.pool = await get_global_pool()
    
    async def stop(self):
        """Stop all data streams"""
        tasks = []
        async with self._lock:
            for stream in self.streams.values():
                tasks.append(stream.stop())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self.streams.clear()
    
    async def add_data_source(self, config: DataSourceConfig, auto_start: bool = True) -> DataStream:
        """Add a new data source"""
        async with self._lock:
            if config.source_id in self.streams:
                logger.warning(f"Data source {config.source_id} already exists")
                return self.streams[config.source_id]
            
            # Create new stream
            stream = DataStream(config, self.pool)
            
            # Subscribe to stream changes for global notifications
            stream.subscribe(self._handle_global_change)
            
            self.streams[config.source_id] = stream
            
            if auto_start and config.enabled:
                await stream.start()
            
            return stream
    
    async def remove_data_source(self, source_id: str):
        """Remove a data source"""
        async with self._lock:
            if source_id in self.streams:
                stream = self.streams[source_id]
                await stream.stop()
                del self.streams[source_id]
    
    async def _handle_global_change(self, event: DataChangeEvent):
        """Handle global change notifications"""
        if not self._global_subscribers:
            return
        
        tasks = []
        for subscriber in self._global_subscribers.copy():
            try:
                if asyncio.iscoroutinefunction(subscriber):
                    tasks.append(subscriber(event))
                else:
                    loop = asyncio.get_event_loop()
                    tasks.append(loop.run_in_executor(None, subscriber, event))
            except Exception as e:
                logger.error(f"Error creating task for global subscriber: {e}")
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    def subscribe_global(self, callback: Callable[[DataChangeEvent], Any]):
        """Subscribe to all data change events"""
        self._global_subscribers.add(callback)
    
    def unsubscribe_global(self, callback: Callable[[DataChangeEvent], Any]):
        """Unsubscribe from global data change events"""
        self._global_subscribers.discard(callback)
    
    async def get_stream(self, source_id: str) -> Optional[DataStream]:
        """Get a data stream by ID"""
        return self.streams.get(source_id)
    
    async def get_all_states(self) -> Dict[str, DataStreamState]:
        """Get states of all streams"""
        return {source_id: stream.get_state() for source_id, stream in self.streams.items()}
    
    async def get_all_data(self) -> Dict[str, Optional[DataRecord]]:
        """Get latest data from all streams"""
        results = {}
        tasks = []
        
        for source_id, stream in self.streams.items():
            tasks.append(self._get_stream_data(source_id, stream))
        
        if tasks:
            data_results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, source_id in enumerate(self.streams.keys()):
                result = data_results[i]
                results[source_id] = result if not isinstance(result, Exception) else None
        
        return results
    
    async def _get_stream_data(self, source_id: str, stream: DataStream) -> Optional[DataRecord]:
        """Get data from a single stream"""
        try:
            return await stream.get_latest_data()
        except Exception as e:
            logger.error(f"Error getting data from stream {source_id}: {e}")
            return None
    
    async def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all streams"""
        if self.pool:
            return await self.pool.health_check_all()
        return {}

# Global manager instance
_global_manager: Optional[RealtimeDataManager] = None

async def get_global_manager() -> RealtimeDataManager:
    """Get the global data manager instance"""
    global _global_manager
    if _global_manager is None:
        _global_manager = RealtimeDataManager()
        await _global_manager.start()
    return _global_manager

async def cleanup_global_manager():
    """Cleanup the global data manager"""
    global _global_manager
    if _global_manager:
        await _global_manager.stop()
        _global_manager = None