"""Data services for connecting views to data sources."""

from .data_service import DataService, get_data_service, show_data_error

__all__ = ["DataService", "get_data_service", "show_data_error"]