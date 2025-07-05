"""Error handling utilities for the AI Adoption Dashboard."""

import functools
import logging
import sys
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar, Union

import streamlit as st

# Type variable for decorators
T = TypeVar("T")


class ErrorSeverity(Enum):
    """Error severity levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    
    DATA_LOADING = "data_loading"
    VISUALIZATION = "visualization"
    CACHE = "cache"
    NETWORK = "network"
    FILE_IO = "file_io"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class ErrorHandler:
    """Centralized error handling for the dashboard."""
    
    def __init__(self, log_file: Optional[Path] = None):
        """Initialize error handler with optional log file path."""
        self.log_file = log_file or Path("dashboard_errors.log")
        self.logger = logging.getLogger(__name__)
        self._error_counts: Dict[ErrorCategory, int] = {cat: 0 for cat in ErrorCategory}
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: Optional[ErrorCategory] = None,
    ) -> None:
        """Log an error with context and severity."""
        if category is None:
            category = self._categorize_error(error)
        
        self._error_counts[category] += 1
        
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "severity": severity.value,
            "category": category.value,
            "context": context or {},
            "traceback": traceback.format_exc(),
        }
        
        # Log to file
        self.logger.error(f"Error occurred: {error_info}")
        
        # Also log to console in debug mode
        if self.logger.level <= logging.DEBUG:
            print(f"ERROR: {error_info}", file=sys.stderr)
    
    def display_error(
        self,
        title: str,
        message: str,
        error: Optional[Exception] = None,
        recovery_action: Optional[str] = None,
        show_details: bool = False,
    ) -> None:
        """Display an error message in the Streamlit interface."""
        with st.container():
            st.error(f"**{title}**")
            st.write(message)
            
            if recovery_action:
                self._show_recovery_action(recovery_action)
            
            if show_details and error:
                with st.expander("Error Details"):
                    st.code(str(error))
                    if self.logger.level <= logging.DEBUG:
                        st.code(traceback.format_exc())
            
            # Show error statistics in debug mode
            if self.logger.level <= logging.DEBUG:
                with st.expander("Error Statistics"):
                    for category, count in self._error_counts.items():
                        if count > 0:
                            st.write(f"{category.value}: {count} errors")
    
    def _categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize an error based on its type and message."""
        error_msg = str(error).lower()
        error_type = type(error).__name__
        
        if "file" in error_msg or "path" in error_msg or isinstance(error, (FileNotFoundError, IOError)):
            return ErrorCategory.FILE_IO
        elif "connection" in error_msg or "network" in error_msg or "timeout" in error_msg:
            return ErrorCategory.NETWORK
        elif "cache" in error_msg:
            return ErrorCategory.CACHE
        elif "data" in error_msg or "load" in error_msg or "parse" in error_msg:
            return ErrorCategory.DATA_LOADING
        elif "plot" in error_msg or "chart" in error_msg or "visual" in error_msg:
            return ErrorCategory.VISUALIZATION
        elif "valid" in error_msg or isinstance(error, (ValueError, TypeError)):
            return ErrorCategory.VALIDATION
        else:
            return ErrorCategory.UNKNOWN
    
    def _show_recovery_action(self, action: str) -> None:
        """Show recovery action based on the action type."""
        actions = {
            "reload": ("🔄 Reload Page", "Refresh the page to try again"),
            "change_view": ("📊 Try Another View", "Select a different analysis view from the sidebar"),
            "check_data": ("📁 Check Data Sources", "Ensure all data files are available"),
            "clear_cache": ("🗑️ Clear Cache", "Clear cached data and reload"),
        }
        
        if action in actions:
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(actions[action][0]):
                    if action == "reload":
                        st.rerun()
                    elif action == "clear_cache":
                        st.cache_data.clear()
                        st.rerun()
            with col2:
                st.info(actions[action][1])
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of errors by category."""
        return {
            "total_errors": sum(self._error_counts.values()),
            "by_category": dict(self._error_counts),
            "timestamp": datetime.now().isoformat(),
        }


def handle_errors(
    fallback_return: Any = None,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    category: Optional[ErrorCategory] = None,
    log_only: bool = False,
) -> Callable:
    """Decorator for handling errors in functions.
    
    CLAUDE.md COMPLIANCE: fallback_return must only be None. Returning sample, hardcoded, or placeholder data is strictly prohibited.
    
    Args:
        fallback_return: Value to return if an error occurs (must be None for CLAUDE.md compliance)
        severity: Error severity level
        category: Error category for classification
        log_only: If True, only log the error without displaying to user
    """
    if fallback_return is not None:
        raise ValueError("CLAUDE.md compliance: fallback_return must be None. Returning sample/hardcoded data is not allowed.")
    def decorator(func: Callable[..., T]) -> Callable[..., Union[T, Any]]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[T, Any]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler = ErrorHandler()
                # Log the error
                error_handler.log_error(
                    e,
                    context={
                        "function": func.__name__,
                        "args": str(args)[:100],  # Truncate for security
                        "kwargs": str(kwargs)[:100],
                    },
                    severity=severity,
                    category=category,
                )
                # Display error if not log_only
                if not log_only:
                    error_handler.display_error(
                        f"Error in {func.__name__}",
                        "An error occurred while processing your request.",
                        error=e,
                        recovery_action="reload",
                    )
                return None
        return wrapper
    return decorator


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None,
) -> None:
    """Setup logging configuration for the application."""
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers,
    )
    
    # Set specific loggers to appropriate levels
    logging.getLogger("streamlit").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)


# Specific error handlers for common scenarios
@handle_errors(fallback_return=None, category=ErrorCategory.DATA_LOADING)
def safe_data_load(loader_func: Callable[..., T], *args, **kwargs) -> Optional[T]:
    """Safely load data with error handling."""
    return loader_func(*args, **kwargs)


@handle_errors(fallback_return=None, category=ErrorCategory.VISUALIZATION, log_only=True)
def safe_visualization(plot_func: Callable[..., T], *args, **kwargs) -> Optional[T]:
    """Safely create visualizations with error handling."""
    return plot_func(*args, **kwargs)


# Error recovery utilities
class ErrorRecovery:
    """Utilities for error recovery strategies."""
    
    @staticmethod
    def with_retry(
        func: Callable[..., T],
        max_attempts: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
    ) -> Callable[..., Optional[T]]:
        """Retry a function with exponential backoff."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Optional[T]:
            import time
            
            last_error = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        error_handler = ErrorHandler()
                        error_handler.log_error(
                            e,
                            context={
                                "function": func.__name__,
                                "attempts": max_attempts,
                            },
                            severity=ErrorSeverity.HIGH,
                        )
            
            return None
        
        return wrapper
    
    @staticmethod
    def with_fallback(primary: Callable[..., T], fallback: Callable[..., T]) -> Callable[..., T]:
        """Try primary function, fall back to secondary on error.
        
        CLAUDE.md COMPLIANCE: The fallback function must NOT return sample, hardcoded, or placeholder data. It may only return None or raise/log errors. This is enforced by project policy and must be documented in all usages.
        """
        def wrapper(*args, **kwargs) -> T:
            try:
                return primary(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.warning(f"Primary function failed, using fallback: {e}")
                result = fallback(*args, **kwargs)
                if result not in (None,):
                    raise ValueError("CLAUDE.md compliance: fallback must not return sample/hardcoded data. Only None is allowed.")
                return result
        return wrapper