"""API module for AI Adoption Dashboard.

This module provides RESTful API endpoints and WebSocket support
for accessing financial calculations and analysis capabilities.
"""

from .endpoints import (
    financial_api,
    scenario_api,
    industry_api,
    export_api,
    report_api
)

from .websocket_server import (
    connection_manager,
    market_simulator,
    calculation_service,
    notification_service,
    websocket_endpoint,
    start_background_tasks,
    stop_background_tasks
)

__all__ = [
    'financial_api',
    'scenario_api', 
    'industry_api',
    'export_api',
    'report_api',
    'connection_manager',
    'market_simulator',
    'calculation_service',
    'notification_service',
    'websocket_endpoint',
    'start_background_tasks',
    'stop_background_tasks'
]