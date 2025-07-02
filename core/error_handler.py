"""
Comprehensive Error Handling and Fallback System
Implements robust error handling with graceful fallbacks and user-friendly messaging
"""

import streamlit as st
import pandas as pd
import traceback
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from functools import wraps
from datetime import datetime
import sys
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for better classification"""
    DATA_LOADING = "data_loading"
    DATA_VALIDATION = "data_validation"
    VISUALIZATION = "visualization"
    CALCULATION = "calculation"
    USER_INPUT = "user_input"
    SYSTEM = "system"
    EXTERNAL_API = "external_api"


class DashboardError(Exception):
    """Custom exception for dashboard-specific errors"""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        user_message: str = None,
        original_error: Exception = None
    ):
        super().__init__(message)
        self.category = category
        self.severity = severity
        self.user_message = user_message or message
        self.original_error = original_error
        self.timestamp = datetime.now()


class ErrorHandler:
    """
    Comprehensive error handling system with fallbacks and user messaging
    """
    
    @staticmethod
    def safe_execute_with_fallback(
        primary_func: Callable,
        fallback_func: Callable = None,
        error_message: str = "Operation failed",
        category: ErrorCategory = ErrorCategory.SYSTEM,
        show_error: bool = True
    ) -> Any:
        """
        Execute function with fallback on error
        
        Args:
            primary_func: Primary function to execute
            fallback_func: Fallback function if primary fails
            error_message: User-friendly error message
            category: Error category for logging
            show_error: Whether to show error to user
            
        Returns:
            Result from primary or fallback function
        """
        try:
            logger.debug(f"Executing primary function: {primary_func.__name__}")
            return primary_func()
            
        except Exception as e:
            # Log the error with full details
            logger.error(f"{error_message} in {primary_func.__name__}: {str(e)}", exc_info=True)
            
            # Show user-friendly error if requested
            if show_error:
                ErrorHandler._display_user_error(error_message, str(e), category)
            
            # Try fallback if available
            if fallback_func:
                try:
                    logger.info(f"Attempting fallback function: {fallback_func.__name__}")
                    st.info("Loading fallback data due to primary source failure...")
                    result = fallback_func()
                    st.warning("Using fallback data. Some features may be limited.")
                    return result
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {str(fallback_error)}", exc_info=True)
                    if show_error:
                        st.error("Both primary and fallback operations failed. Please try again later.")
            
            # Return None if all attempts failed
            return None
    
    @staticmethod
    def _display_user_error(
        error_message: str,
        technical_details: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM
    ) -> None:
        """
        Display user-friendly error messages based on category and severity
        
        Args:
            error_message: User-friendly error message
            technical_details: Technical error details
            category: Error category
            severity: Error severity
        """
        # Choose appropriate Streamlit display method based on severity
        if severity == ErrorSeverity.CRITICAL:
            display_func = st.error
            icon = "🚨"
        elif severity == ErrorSeverity.HIGH:
            display_func = st.error
            icon = "❌"
        elif severity == ErrorSeverity.MEDIUM:
            display_func = st.warning
            icon = "⚠️"
        else:
            display_func = st.info
            icon = "ℹ️"
        
        # Display main error message
        display_func(f"{icon} {error_message}")
        
        # Provide category-specific guidance
        guidance = ErrorHandler._get_error_guidance(category)
        if guidance:
            st.info(f"💡 **Suggestion**: {guidance}")
        
        # Show technical details in expandable section
        with st.expander("🔧 Technical Details", expanded=False):
            st.code(technical_details, language="text")
            
            # Add helpful actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔄 Retry", key=f"retry_{hash(technical_details)}"):
                    st.rerun()
            with col2:
                if st.button("🗑️ Clear Cache", key=f"clear_{hash(technical_details)}"):
                    st.cache_data.clear()
                    st.rerun()
            with col3:
                if st.button("📝 Report Issue", key=f"report_{hash(technical_details)}"):
                    ErrorHandler._show_issue_reporting(error_message, technical_details, category)
    
    @staticmethod
    def _get_error_guidance(category: ErrorCategory) -> str:
        """
        Get user guidance based on error category
        
        Args:
            category: Error category
            
        Returns:
            User-friendly guidance message
        """
        guidance_map = {
            ErrorCategory.DATA_LOADING: "Check your internet connection and ensure data sources are accessible. Try refreshing the page.",
            ErrorCategory.DATA_VALIDATION: "Verify that your data format matches the expected structure. Check for missing required columns.",
            ErrorCategory.VISUALIZATION: "This might be due to incompatible data. Try selecting a different view or time period.",
            ErrorCategory.CALCULATION: "Check if the required data is available and in the correct format. Some calculations require minimum data points.",
            ErrorCategory.USER_INPUT: "Please verify your input values are within the expected range and format.",
            ErrorCategory.SYSTEM: "This appears to be a system issue. Try refreshing the page or clearing the cache.",
            ErrorCategory.EXTERNAL_API: "External service may be temporarily unavailable. The system will use cached data if available."
        }
        return guidance_map.get(category, "Try refreshing the page or contact support if the issue persists.")
    
    @staticmethod
    def _show_issue_reporting(error_message: str, technical_details: str, category: ErrorCategory) -> None:
        """
        Show issue reporting interface
        
        Args:
            error_message: User-friendly error message
            technical_details: Technical error details
            category: Error category
        """
        st.markdown("### 📝 Report This Issue")
        st.markdown("Help us improve the dashboard by reporting this error:")
        
        # Pre-filled issue template
        issue_template = f"""
**Error Category**: {category.value}
**Error Message**: {error_message}
**Technical Details**: 
```
{technical_details}
```
**Steps to Reproduce**:
1. [Please describe what you were doing when this error occurred]

**Additional Context**:
[Any additional information that might help us understand the issue]
        """
        
        st.text_area("Issue Details", value=issue_template.strip(), height=200)
        st.markdown("📧 Please copy the above details and send them to: support@ai-dashboard.com")


def safe_operation(
    category: ErrorCategory = ErrorCategory.SYSTEM,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    fallback_result: Any = None,
    show_error: bool = True
):
    """
    Decorator for safe operation execution with automatic error handling
    
    Args:
        category: Error category for logging and guidance
        severity: Error severity level
        fallback_result: Result to return if operation fails
        show_error: Whether to show error to user
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"Error in {func.__name__}"
                
                # Log error with context
                logger.error(f"{error_msg}: {str(e)}", exc_info=True)
                
                # Display user error if requested
                if show_error:
                    ErrorHandler._display_user_error(error_msg, str(e), category, severity)
                
                return fallback_result
        return wrapper
    return decorator


class DataSourceValidator:
    """
    Validate data sources and provide fallbacks
    """
    
    @staticmethod
    def validate_data_sources() -> Dict[str, bool]:
        """
        Validate all data sources are accessible
        
        Returns:
            Dictionary mapping source names to availability status
        """
        import os
        from pathlib import Path
        
        sources = {
            'stanford_ai_index': 'data/stanford_ai_index_2025.csv',
            'mckinsey_survey': 'data/mckinsey_ai_survey.csv',
            'oecd_data': 'data/oecd_ai_policy.csv',
            'financial_impact': 'data/financial_impact.csv',
            'investment_trends': 'data/investment_trends.csv'
        }
        
        results = {}
        missing_sources = []
        
        for name, path in sources.items():
            file_path = Path(path)
            is_available = file_path.exists() and file_path.is_file()
            results[name] = is_available
            
            if not is_available:
                missing_sources.append(name)
        
        # Report missing sources
        if missing_sources:
            logger.warning(f"Missing data sources: {missing_sources}")
            st.warning(f"⚠️ Some data sources are not available: {', '.join(missing_sources)}")
            st.info("📁 The dashboard will use fallback data for missing sources.")
        else:
            logger.info("All data sources validated successfully")
        
        return results
    
    @staticmethod
    def validate_data_freshness(data_dict: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
        """
        Validate freshness of loaded data
        
        Args:
            data_dict: Dictionary of DataFrames to validate
            
        Returns:
            Dictionary with freshness information for each dataset
        """
        freshness_info = {}
        current_year = datetime.now().year
        
        for name, df in data_dict.items():
            info = {
                'is_fresh': True,
                'age_years': 0,
                'last_year': None,
                'warnings': []
            }
            
            if df is not None and not df.empty and 'year' in df.columns:
                try:
                    last_year = df['year'].max()
                    age_years = current_year - last_year
                    
                    info.update({
                        'last_year': last_year,
                        'age_years': age_years,
                        'is_fresh': age_years <= 2  # Fresh if within 2 years
                    })
                    
                    if age_years > 2:
                        info['warnings'].append(f"Data is {age_years} years old")
                    
                except Exception as e:
                    info['warnings'].append(f"Could not determine data age: {str(e)}")
            else:
                info['warnings'].append("No year column found or empty dataset")
            
            freshness_info[name] = info
        
        return freshness_info


class FileUploadValidator:
    """
    Validate uploaded files for security and format compliance
    """
    
    ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.json']
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @staticmethod
    def validate_uploaded_file(uploaded_file) -> Tuple[bool, List[str]]:
        """
        Validate uploaded files for security and format
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        if uploaded_file is None:
            return False, ["No file uploaded"]
        
        # Check file size
        if uploaded_file.size > FileUploadValidator.MAX_FILE_SIZE:
            file_size_mb = uploaded_file.size / 1024 / 1024
            errors.append(f"File too large: {file_size_mb:.1f}MB (max {FileUploadValidator.MAX_FILE_SIZE // 1024 // 1024}MB)")
        
        # Check file extension
        import os
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in FileUploadValidator.ALLOWED_EXTENSIONS:
            errors.append(f"File type not allowed: {file_extension}. Supported types: {FileUploadValidator.ALLOWED_EXTENSIONS}")
        
        # Check filename for security
        if any(char in uploaded_file.name for char in ['..', '/', '\\']):
            errors.append("Filename contains invalid characters")
        
        # Validate file content
        try:
            if file_extension == '.csv':
                df = pd.read_csv(uploaded_file, nrows=5)  # Read first 5 rows to validate
                if df.empty:
                    errors.append("CSV file is empty")
            elif file_extension == '.xlsx':
                df = pd.read_excel(uploaded_file, nrows=5)
                if df.empty:
                    errors.append("Excel file is empty")
            elif file_extension == '.json':
                import json
                content = uploaded_file.getvalue().decode('utf-8')
                json.loads(content)  # Validate JSON format
                
        except Exception as e:
            errors.append(f"File format validation failed: {str(e)}")
        
        is_valid = len(errors) == 0
        return is_valid, errors


# Global error handler for uncaught exceptions
def setup_global_error_handler():
    """Setup global error handler for uncaught exceptions"""
    
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = f"Uncaught exception: {exc_type.__name__}: {str(exc_value)}"
        logger.critical(error_msg, exc_info=(exc_type, exc_value, exc_traceback))
        
        # Show user error if in Streamlit context
        try:
            st.error("🚨 An unexpected error occurred. Please refresh the page.")
            with st.expander("Error Details"):
                st.code(error_msg)
        except:
            pass  # Not in Streamlit context
    
    sys.excepthook = handle_exception


# Initialize global error handling
setup_global_error_handler()