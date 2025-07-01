"""
Real-time Data Integration Module

This module provides comprehensive real-time data integration capabilities for the AI Dashboard,
including API connections, data synchronization, and live updates.
"""

from .core import RealtimeDataManager, DataStream
from .api_client import APIClient, APIConnectionPool
from .data_sync import DataSynchronizer, ChangeDetector
from .monitoring import APIMonitor, HealthChecker
from .config import DataSourceConfig, APIConfig
from .notifications import NotificationManager, UpdateNotifier

__all__ = [
    'RealtimeDataManager',
    'DataStream', 
    'APIClient',
    'APIConnectionPool',
    'DataSynchronizer',
    'ChangeDetector',
    'APIMonitor',
    'HealthChecker',
    'DataSourceConfig',
    'APIConfig',
    'NotificationManager',
    'UpdateNotifier'
]

__version__ = "1.0.0"