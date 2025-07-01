"""
Enhanced data validation utilities for AI Adoption Dashboard
Provides comprehensive data checking, schema validation, and safe plotting helpers
"""

import pandas as pd
import streamlit as st
from typing import Dict, List, Optional, Tuple, Any, Callable
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class DataStatus(Enum):
    """Status of data validation"""
    VALID = "valid"
    EMPTY = "empty"
    MISSING_COLUMNS = "missing_columns"
    WRONG_TYPE = "wrong_type"
    INVALID = "invalid"


@dataclass
class ValidationResult:
    """Result of data validation"""
    status: DataStatus
    message: str
    missing_columns: List[str] = None
    data: pd.DataFrame = None
    
    @property
    def is_valid(self) -> bool:
        return self.status == DataStatus.VALID


class DataValidator:
    """Comprehensive data validation for dashboard"""
    
    @staticmethod
    def validate_dataframe(
        df: Any,
        name: str,
        required_columns: List[str] = None,
        column_types: Dict[str, type] = None,
        min_rows: int = 1,
        show_warning: bool = True
    ) -> ValidationResult:
        """
        Validate a dataframe with comprehensive checks
        
        Args:
            df: The dataframe to validate
            name: Name of the dataframe for error messages
            required_columns: List of required column names
            column_types: Dict mapping column names to expected types
            min_rows: Minimum number of rows required
            show_warning: Whether to show Streamlit warnings
            
        Returns:
            ValidationResult with status and messages
        """
        # Check if df is None
        if df is None:
            msg = f"❌ {name} is None"
            if show_warning:
                st.warning(msg)
            logger.error(msg)
            return ValidationResult(DataStatus.INVALID, msg)
        
        # Check if df is a DataFrame
        if not isinstance(df, pd.DataFrame):
            msg = f"❌ {name} is not a DataFrame (type: {type(df).__name__})"
            if show_warning:
                st.warning(msg)
            logger.error(msg)
            return ValidationResult(DataStatus.WRONG_TYPE, msg)
        
        # Check if empty
        if df.empty or len(df) < min_rows:
            msg = f"⚠️ {name} has insufficient data (rows: {len(df)}, required: {min_rows})"
            if show_warning:
                st.warning(msg)
            logger.warning(msg)
            return ValidationResult(DataStatus.EMPTY, msg, data=df)
        
        # Check required columns
        if required_columns:
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                msg = f"❌ {name} missing required columns: {missing}"
                if show_warning:
                    st.error(msg)
                logger.error(msg)
                return ValidationResult(DataStatus.MISSING_COLUMNS, msg, missing_columns=missing, data=df)
        
        # Check column types
        if column_types:
            for col, expected_type in column_types.items():
                if col in df.columns:
                    actual_type = df[col].dtype
                    # Basic type checking (can be enhanced)
                    if expected_type == float and actual_type not in ['float64', 'float32']:
                        try:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                        except Exception as e:
                            msg = f"⚠️ {name}.{col} type mismatch: expected {expected_type}, got {actual_type}"
                            logger.warning(msg)
        
        return ValidationResult(DataStatus.VALID, f"✅ {name} validated successfully", data=df)


def safe_plot_check(
    df: pd.DataFrame,
    name: str,
    required_columns: List[str] = None,
    min_rows: int = 1,
    plot_func: Callable = None,
    empty_message: str = None
) -> bool:
    """
    Safe plotting helper that validates data before plotting
    
    Args:
        df: DataFrame to validate
        name: Name for error messages
        required_columns: Required columns for the plot
        min_rows: Minimum rows needed
        plot_func: Function to call if data is valid
        empty_message: Custom message for empty data
        
    Returns:
        True if plot was successful, False otherwise
    """
    validator = DataValidator()
    result = validator.validate_dataframe(
        df, name, required_columns=required_columns, min_rows=min_rows
    )
    
    if result.is_valid:
        if plot_func:
            try:
                plot_func()
                return True
            except Exception as e:
                st.error(f"Error plotting {name}: {str(e)}")
                logger.error(f"Plot error for {name}: {e}", exc_info=True)
                return False
        return True
    else:
        # Show appropriate message based on status
        if result.status == DataStatus.EMPTY:
            msg = empty_message or f"No data available for {name}"
            st.info(msg)
        elif result.status == DataStatus.MISSING_COLUMNS:
            st.warning(f"Cannot display {name}: Missing columns {result.missing_columns}")
        else:
            st.error(result.message)
        return False


def validate_and_clean_data(
    df: pd.DataFrame,
    name: str,
    schema: Dict[str, Any]
) -> Tuple[bool, pd.DataFrame]:
    """
    Validate and clean dataframe according to schema
    
    Args:
        df: DataFrame to validate and clean
        name: Name for logging
        schema: Dict with column definitions
        
    Returns:
        Tuple of (is_valid, cleaned_dataframe)
    """
    if df is None or df.empty:
        return False, pd.DataFrame()
    
    cleaned_df = df.copy()
    
    # Add missing columns with defaults
    for col, config in schema.items():
        if col not in cleaned_df.columns:
            default_val = config.get('default', None)
            cleaned_df[col] = default_val
            logger.info(f"Added missing column {col} to {name} with default value")
    
    # Convert types
    for col, config in schema.items():
        if col in cleaned_df.columns and 'type' in config:
            try:
                if config['type'] == 'numeric':
                    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
                elif config['type'] == 'datetime':
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
                elif config['type'] == 'string':
                    cleaned_df[col] = cleaned_df[col].astype(str)
            except Exception as e:
                logger.warning(f"Failed to convert {name}.{col} to {config['type']}: {e}")
    
    # Remove rows with all NaN values
    cleaned_df = cleaned_df.dropna(how='all')
    
    return not cleaned_df.empty, cleaned_df


def create_retry_button(
    key: str,
    callback: Callable,
    message: str = "Failed to load data"
) -> None:
    """
    Create a retry button for failed operations
    
    Args:
        key: Unique key for the button
        callback: Function to call on retry
        message: Error message to display
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.error(message)
    with col2:
        if st.button("🔄 Retry", key=f"retry_{key}"):
            # Clear cache and retry
            st.cache_data.clear()
            callback()
            st.rerun()


def safe_download_button(
    df: pd.DataFrame,
    filename: str,
    button_text: str = "📥 Download Data",
    key: str = None,
    help_text: str = None
) -> None:
    """
    Show download button only if data exists
    
    Args:
        df: DataFrame to download
        filename: Name for the downloaded file
        button_text: Text for the button
        key: Unique key for the button
        help_text: Help tooltip
    """
    if df is not None and not df.empty:
        csv = df.to_csv(index=False)
        st.download_button(
            label=button_text,
            data=csv,
            file_name=filename,
            mime='text/csv',
            key=key,
            help=help_text
        )
    else:
        st.info("No data available for download")


# Schema definitions for common dataframes
SCHEMAS = {
    'historical_data': {
        'year': {'type': 'numeric', 'required': True},
        'ai_use': {'type': 'numeric', 'required': True},
        'genai_use': {'type': 'numeric', 'required': True, 'default': 0}
    },
    'sector_data': {
        'sector': {'type': 'string', 'required': True},
        'adoption_rate': {'type': 'numeric', 'required': True},
        'genai_adoption': {'type': 'numeric', 'default': 0},
        'avg_roi': {'type': 'numeric', 'default': 0}
    },
    'investment_data': {
        'year': {'type': 'numeric', 'required': True},
        'total_investment': {'type': 'numeric', 'required': True},
        'genai_investment': {'type': 'numeric', 'default': 0}
    },
    'financial_impact': {
        'function': {'type': 'string', 'required': True},
        'companies_reporting_revenue_gains': {'type': 'numeric', 'required': True},
        'companies_reporting_cost_savings': {'type': 'numeric', 'required': True}
    }
}