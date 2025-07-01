"""
Real-time update notifications and user interface integration
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import time
import weakref

from .models import DataChangeEvent, NotificationEvent, DataStatus

logger = logging.getLogger(__name__)

class NotificationType(str, Enum):
    """Types of notifications"""
    DATA_UPDATE = "data_update"
    DATA_ERROR = "data_error"
    SOURCE_ONLINE = "source_online"
    SOURCE_OFFLINE = "source_offline"
    CONFIG_CHANGE = "config_change"
    SYSTEM_ALERT = "system_alert"

class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class UINotification:
    """User interface notification"""
    id: str
    title: str
    message: str
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.NORMAL
    source_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    read: bool = False
    actions: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if notification is expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def age_seconds(self) -> float:
        """Get notification age in seconds"""
        return (datetime.utcnow() - self.timestamp).total_seconds()

class NotificationSubscriber:
    """Subscriber for notifications"""
    
    def __init__(
        self,
        callback: Callable[[UINotification], Any],
        filters: Optional[Dict[str, Any]] = None,
        subscriber_id: Optional[str] = None
    ):
        self.callback = callback
        self.filters = filters or {}
        self.subscriber_id = subscriber_id or f"subscriber_{id(self)}"
        self.active = True
        self.last_notification = None
        self.notification_count = 0
    
    def matches_filters(self, notification: UINotification) -> bool:
        """Check if notification matches subscriber filters"""
        if not self.filters:
            return True
        
        # Check notification type filter
        if 'types' in self.filters:
            if notification.notification_type not in self.filters['types']:
                return False
        
        # Check source filter
        if 'sources' in self.filters:
            if notification.source_id not in self.filters['sources']:
                return False
        
        # Check priority filter
        if 'min_priority' in self.filters:
            priority_order = [p.value for p in NotificationPriority]
            min_priority_idx = priority_order.index(self.filters['min_priority'])
            notification_priority_idx = priority_order.index(notification.priority.value)
            if notification_priority_idx < min_priority_idx:
                return False
        
        return True

class NotificationManager:
    """Manages real-time notifications"""
    
    def __init__(self, max_notifications: int = 1000):
        self.max_notifications = max_notifications
        self.notifications: Dict[str, UINotification] = {}
        self.subscribers: Dict[str, NotificationSubscriber] = {}
        self._notification_counter = 0
        self._lock = asyncio.Lock()
        
        # Cleanup task
        self._cleanup_task = None
        self._stop_cleanup = asyncio.Event()
    
    async def start(self):
        """Start the notification manager"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def stop(self):
        """Stop the notification manager"""
        if self._cleanup_task:
            self._stop_cleanup.set()
            try:
                await asyncio.wait_for(self._cleanup_task, timeout=5.0)
            except asyncio.TimeoutError:
                self._cleanup_task.cancel()
            self._cleanup_task = None
    
    async def create_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        source_id: Optional[str] = None,
        expires_in: Optional[timedelta] = None,
        actions: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UINotification:
        """Create a new notification"""
        async with self._lock:
            self._notification_counter += 1
            notification_id = f"notification_{self._notification_counter}_{int(time.time())}"
            
            expires_at = None
            if expires_in:
                expires_at = datetime.utcnow() + expires_in
            
            notification = UINotification(
                id=notification_id,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                source_id=source_id,
                expires_at=expires_at,
                actions=actions or [],
                metadata=metadata or {}
            )
            
            self.notifications[notification_id] = notification
            
            # Ensure we don't exceed max notifications
            await self._enforce_limits()
            
            # Notify subscribers
            await self._notify_subscribers(notification)
            
            return notification
    
    async def _notify_subscribers(self, notification: UINotification):
        """Notify all matching subscribers"""
        tasks = []
        
        async with self._lock:
            for subscriber in self.subscribers.values():
                if not subscriber.active:
                    continue
                
                if not subscriber.matches_filters(notification):
                    continue
                
                subscriber.last_notification = datetime.utcnow()
                subscriber.notification_count += 1
                
                try:
                    if asyncio.iscoroutinefunction(subscriber.callback):
                        tasks.append(subscriber.callback(notification))
                    else:
                        loop = asyncio.get_event_loop()
                        tasks.append(loop.run_in_executor(None, subscriber.callback, notification))
                except Exception as e:
                    logger.error(f"Error creating task for subscriber {subscriber.subscriber_id}: {e}")
        
        # Execute all notifications concurrently
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logger.error(f"Error notifying subscribers: {e}")
    
    async def mark_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        async with self._lock:
            if notification_id in self.notifications:
                self.notifications[notification_id].read = True
                return True
            return False
    
    async def dismiss_notification(self, notification_id: str) -> bool:
        """Dismiss (delete) a notification"""
        async with self._lock:
            if notification_id in self.notifications:
                del self.notifications[notification_id]
                return True
            return False
    
    async def get_notifications(
        self,
        unread_only: bool = False,
        source_id: Optional[str] = None,
        notification_type: Optional[NotificationType] = None,
        limit: int = 50
    ) -> List[UINotification]:
        """Get notifications with filtering"""
        async with self._lock:
            notifications = list(self.notifications.values())
            
            # Apply filters
            if unread_only:
                notifications = [n for n in notifications if not n.read]
            
            if source_id:
                notifications = [n for n in notifications if n.source_id == source_id]
            
            if notification_type:
                notifications = [n for n in notifications if n.notification_type == notification_type]
            
            # Remove expired notifications
            notifications = [n for n in notifications if not n.is_expired]
            
            # Sort by timestamp (newest first)
            notifications.sort(key=lambda n: n.timestamp, reverse=True)
            
            return notifications[:limit]
    
    async def get_unread_count(self, source_id: Optional[str] = None) -> int:
        """Get count of unread notifications"""
        notifications = await self.get_notifications(unread_only=True, source_id=source_id)
        return len(notifications)
    
    def subscribe(
        self,
        callback: Callable[[UINotification], Any],
        filters: Optional[Dict[str, Any]] = None,
        subscriber_id: Optional[str] = None
    ) -> str:
        """Subscribe to notifications"""
        subscriber = NotificationSubscriber(callback, filters, subscriber_id)
        self.subscribers[subscriber.subscriber_id] = subscriber
        return subscriber.subscriber_id
    
    def unsubscribe(self, subscriber_id: str) -> bool:
        """Unsubscribe from notifications"""
        if subscriber_id in self.subscribers:
            self.subscribers[subscriber_id].active = False
            del self.subscribers[subscriber_id]
            return True
        return False
    
    async def _enforce_limits(self):
        """Enforce notification limits"""
        if len(self.notifications) <= self.max_notifications:
            return
        
        # Sort by timestamp and remove oldest
        notifications_by_age = sorted(
            self.notifications.items(),
            key=lambda item: item[1].timestamp
        )
        
        to_remove = len(self.notifications) - self.max_notifications
        for i in range(to_remove):
            notification_id = notifications_by_age[i][0]
            del self.notifications[notification_id]
    
    async def _cleanup_loop(self):
        """Periodic cleanup of expired notifications"""
        while not self._stop_cleanup.is_set():
            try:
                await self._cleanup_expired()
                await asyncio.sleep(60)  # Cleanup every minute
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_expired(self):
        """Remove expired notifications"""
        async with self._lock:
            expired_ids = [
                notification_id
                for notification_id, notification in self.notifications.items()
                if notification.is_expired
            ]
            
            for notification_id in expired_ids:
                del self.notifications[notification_id]
            
            if expired_ids:
                logger.debug(f"Cleaned up {len(expired_ids)} expired notifications")
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get notification statistics"""
        async with self._lock:
            total_notifications = len(self.notifications)
            unread_notifications = sum(1 for n in self.notifications.values() if not n.read)
            
            # Count by type
            by_type = {}
            for notification in self.notifications.values():
                notification_type = notification.notification_type.value
                by_type[notification_type] = by_type.get(notification_type, 0) + 1
            
            return {
                'total_notifications': total_notifications,
                'unread_notifications': unread_notifications,
                'active_subscribers': len([s for s in self.subscribers.values() if s.active]),
                'notifications_by_type': by_type,
                'max_notifications': self.max_notifications
            }

class UpdateNotifier:
    """Specialized notifier for data updates"""
    
    def __init__(self, notification_manager: NotificationManager):
        self.notification_manager = notification_manager
        self._last_update_times: Dict[str, datetime] = {}
        self._update_counts: Dict[str, int] = {}
    
    async def notify_data_update(
        self,
        source_id: str,
        change_event: DataChangeEvent,
        suppress_duplicates: bool = True,
        min_interval: timedelta = timedelta(seconds=30)
    ):
        """Notify about data updates"""
        now = datetime.utcnow()
        
        # Check if we should suppress this notification
        if suppress_duplicates:
            last_update = self._last_update_times.get(source_id)
            if last_update and (now - last_update) < min_interval:
                return
        
        # Update tracking
        self._last_update_times[source_id] = now
        self._update_counts[source_id] = self._update_counts.get(source_id, 0) + 1
        
        # Determine priority based on change type
        priority = NotificationPriority.NORMAL
        if change_event.change_type == "insert":
            priority = NotificationPriority.HIGH
        
        # Create notification
        await self.notification_manager.create_notification(
            title=f"Data Updated: {source_id}",
            message=f"Data source {source_id} has been updated ({change_event.change_type})",
            notification_type=NotificationType.DATA_UPDATE,
            priority=priority,
            source_id=source_id,
            expires_in=timedelta(minutes=5),
            metadata={
                'change_type': change_event.change_type,
                'changed_fields': change_event.changed_fields,
                'update_count': self._update_counts[source_id]
            }
        )
    
    async def notify_data_error(
        self,
        source_id: str,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None
    ):
        """Notify about data errors"""
        await self.notification_manager.create_notification(
            title=f"Data Error: {source_id}",
            message=f"Error loading data from {source_id}: {error_message}",
            notification_type=NotificationType.DATA_ERROR,
            priority=NotificationPriority.HIGH,
            source_id=source_id,
            expires_in=timedelta(hours=1),
            actions=[
                {"label": "Retry", "action": "retry_source", "source_id": source_id},
                {"label": "View Details", "action": "view_error_details"}
            ],
            metadata=error_details or {}
        )
    
    async def notify_source_status(
        self,
        source_id: str,
        is_online: bool,
        status_details: Optional[str] = None
    ):
        """Notify about source status changes"""
        if is_online:
            notification_type = NotificationType.SOURCE_ONLINE
            title = f"Source Online: {source_id}"
            message = f"Data source {source_id} is now online and available"
            priority = NotificationPriority.NORMAL
        else:
            notification_type = NotificationType.SOURCE_OFFLINE
            title = f"Source Offline: {source_id}"
            message = f"Data source {source_id} is currently offline or unavailable"
            priority = NotificationPriority.HIGH
        
        if status_details:
            message += f". {status_details}"
        
        await self.notification_manager.create_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            source_id=source_id,
            expires_in=timedelta(minutes=10)
        )

class StreamlitNotificationHandler:
    """Handler for Streamlit-specific notifications"""
    
    def __init__(self):
        self.session_notifications: Dict[str, List[UINotification]] = {}
        self._lock = asyncio.Lock()
    
    async def handle_notification(self, notification: UINotification):
        """Handle notification for Streamlit session"""
        # In a real implementation, this would integrate with Streamlit's session state
        # For now, we'll store notifications per session
        
        session_id = "default"  # Would get actual session ID from Streamlit
        
        async with self._lock:
            if session_id not in self.session_notifications:
                self.session_notifications[session_id] = []
            
            self.session_notifications[session_id].append(notification)
            
            # Keep only recent notifications
            max_per_session = 20
            if len(self.session_notifications[session_id]) > max_per_session:
                self.session_notifications[session_id] = self.session_notifications[session_id][-max_per_session:]
    
    async def get_session_notifications(self, session_id: str = "default") -> List[UINotification]:
        """Get notifications for a Streamlit session"""
        async with self._lock:
            return self.session_notifications.get(session_id, [])
    
    async def clear_session_notifications(self, session_id: str = "default"):
        """Clear notifications for a session"""
        async with self._lock:
            if session_id in self.session_notifications:
                self.session_notifications[session_id] = []

# Global notification manager instance
_global_notification_manager: Optional[NotificationManager] = None
_global_update_notifier: Optional[UpdateNotifier] = None

async def get_global_notification_manager() -> NotificationManager:
    """Get the global notification manager instance"""
    global _global_notification_manager
    if _global_notification_manager is None:
        _global_notification_manager = NotificationManager()
        await _global_notification_manager.start()
    return _global_notification_manager

async def get_global_update_notifier() -> UpdateNotifier:
    """Get the global update notifier instance"""
    global _global_update_notifier
    if _global_update_notifier is None:
        notification_manager = await get_global_notification_manager()
        _global_update_notifier = UpdateNotifier(notification_manager)
    return _global_update_notifier

async def cleanup_global_notifications():
    """Cleanup global notification instances"""
    global _global_notification_manager, _global_update_notifier
    
    if _global_notification_manager:
        await _global_notification_manager.stop()
        _global_notification_manager = None
    
    _global_update_notifier = None