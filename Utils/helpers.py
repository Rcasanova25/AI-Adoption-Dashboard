"""
Helper functions - Improve error handling in your app
Replace scattered try/catch blocks with these reusable functions
"""

import streamlit as st
import pandas as pd
import logging
from typing import Any, Callable, Optional
from functools import wraps

# Set up logging
logger = logging.getLogger(__name__)


class DashboardError(Exception):
    """Base exception for dashboard errors"""
    pass


def safe_execute(
    func: Callable,
    default_value: Any = None,
    error_message: str = "Operation failed",
    show_error: bool = True
) -> Any:
    """
    Safely execute a function with error handling
    
    Example usage:
    # Instead of:
    try:
        result = some_risky_function()
    except Exception as e:
        st.error(f"Error: {e}")
        result = None
    
    # Use:
    result = safe_execute(some_risky_function, default_value=None)
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        if show_error:
            st.error(f"{error_message}: {str(e)}")
        return default_value


def safe_data_check(
    data: Optional[pd.DataFrame], 
    data_name: str,
    show_ui_message: bool = True
) -> bool:
    """
    Safe data validation with user-friendly error messages
    
    Replace your scattered None checks with this
    """
    if data is None:
        if show_ui_message:
            st.error(f"❌ {data_name} is not available.")
            st.info("Please check data loading or contact support.")
        logger.error(f"{data_name} is None")
        return False
    
    if hasattr(data, 'empty') and data.empty:
        if show_ui_message:
            st.error(f"❌ {data_name} is empty.")
            st.info("Please check data sources or refresh the application.")
        logger.error(f"{data_name} is empty")
        return False
    
    return True


def clean_filename(text: str, max_length: int = 100) -> str:
    """
    Clean text for safe filename generation
    
    Replace your existing clean_filename function with this improved version
    """
    import re
    from pathlib import Path
    
    # Remove path traversal attempts
    text = Path(text).name
    
    # Remove emojis and special characters, replace spaces with underscores
    cleaned = re.sub(r'[^\w\s-]', '', text)
    cleaned = re.sub(r'\s+', '_', cleaned)
    
    # Collapse multiple consecutive underscores into a single underscore
    cleaned = re.sub(r'_+', '_', cleaned)
    
    cleaned = cleaned.lower().strip('_')
    
    # Limit length
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    # Ensure it's not empty
    if not cleaned:
        cleaned = "data"
    
    return cleaned


def validate_chart_data(data: Optional[pd.DataFrame], required_columns: list) -> tuple[bool, str]:
    """
    Validate data for chart rendering
    
    Args:
        data: DataFrame to validate
        required_columns: List of required column names
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Check for None data
    if data is None:
        return False, "Data is None"
    
    # Check for empty DataFrame
    if data.empty:
        return False, "Data is empty"
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return False, f"Missing columns: {', '.join(missing_columns)}"
    
    # Check for sufficient data (at least 1 row)
    if len(data) == 0:
        return False, "Data has no rows"
    
    return True, "Data is valid"


def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor function performance
    
    Usage:
    @monitor_performance
    def slow_function():
        # function code
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            if duration > 1.0:  # Log slow operations
                logger.warning(f"Slow operation: {func.__name__} took {duration:.2f}s")
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {e}")
            raise
    
    return wrapper