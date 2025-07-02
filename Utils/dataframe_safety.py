"""
DataFrame Safety Utilities

This module provides safe DataFrame operations and type checking utilities
to prevent common errors and ensure data consistency.
"""

import pandas as pd
import numpy as np
from typing import Any, Union, Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

def ensure_dataframe(data: Any) -> pd.DataFrame:
    """
    Ensure data is a pandas DataFrame with proper error handling.
    
    Args:
        data: Input data that should be converted to DataFrame
        
    Returns:
        pandas.DataFrame: Safe DataFrame object
        
    Examples:
        >>> ensure_dataframe([{'a': 1, 'b': 2}])
        DataFrame with columns 'a' and 'b'
        
        >>> ensure_dataframe(None)
        Empty DataFrame
    """
    try:
        if isinstance(data, pd.DataFrame):
            return data.copy()
        elif isinstance(data, (list, dict)):
            return pd.DataFrame(data)
        elif isinstance(data, np.ndarray):
            return pd.DataFrame(data)
        elif data is None:
            return pd.DataFrame()
        else:
            logger.warning(f"Unexpected data type: {type(data)}")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error converting to DataFrame: {e}")
        return pd.DataFrame()

def safe_dataframe_operation(df: pd.DataFrame, operation: str, **kwargs) -> pd.DataFrame:
    """
    Perform safe DataFrame operations with proper error handling.
    
    Args:
        df: Input DataFrame
        operation: Operation to perform ('sort_values', 'iloc', 'groupby', etc.)
        **kwargs: Operation-specific arguments
        
    Returns:
        pandas.DataFrame: Result of the operation or original DataFrame on error
    """
    if not isinstance(df, pd.DataFrame):
        logger.warning(f"Expected DataFrame, got {type(df)}")
        return pd.DataFrame()
    
    try:
        if operation == "sort_values" and "by" in kwargs:
            column = kwargs["by"]
            if column in df.columns:
                return df.sort_values(**kwargs)
            else:
                logger.warning(f"Column '{column}' not found in DataFrame")
                return df.copy()
        
        elif operation == "iloc":
            index = kwargs.get("index", 0)
            if isinstance(index, int) and 0 <= index < len(df):
                return df.iloc[index:index+1]  # Return as DataFrame, not Series
            else:
                logger.warning(f"Invalid index {index} for DataFrame of length {len(df)}")
                return df.copy()
        
        elif operation == "groupby":
            by = kwargs.get("by")
            if by and by in df.columns:
                return df.groupby(**kwargs)
            else:
                logger.warning(f"Groupby column '{by}' not found")
                return df.copy()
        
        else:
            logger.warning(f"Unknown operation: {operation}")
            return df.copy()
            
    except Exception as e:
        logger.error(f"DataFrame operation '{operation}' failed: {e}")
        return df.copy()

def safe_column_access(df: pd.DataFrame, column: str, default_value: Any = None) -> Any:
    """
    Safely access DataFrame column with fallback value.
    
    Args:
        df: Input DataFrame
        column: Column name to access
        default_value: Value to return if column doesn't exist
        
    Returns:
        Column data or default value
    """
    if not isinstance(df, pd.DataFrame):
        return default_value
    
    if column in df.columns:
        return df[column]
    else:
        logger.warning(f"Column '{column}' not found in DataFrame")
        return default_value

def safe_numeric_conversion(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float with error handling.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted value or default
    """
    try:
        if pd.isna(value) or value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        logger.warning(f"Could not convert {value} to float, using default {default}")
        return default

def safe_dataframe_filter(df: pd.DataFrame, condition: str, **kwargs) -> pd.DataFrame:
    """
    Safely filter DataFrame with error handling.
    
    Args:
        df: Input DataFrame
        condition: Filter condition (e.g., 'state == "California"')
        **kwargs: Additional filter parameters
        
    Returns:
        pandas.DataFrame: Filtered DataFrame or empty DataFrame on error
    """
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()
    
    try:
        # Parse condition safely
        if '==' in condition:
            column, value = condition.split('==')
            column = column.strip()
            value = value.strip().strip('"\'')
            
            if column in df.columns:
                return df[df[column] == value]
            else:
                logger.warning(f"Column '{column}' not found for filtering")
                return pd.DataFrame()
        else:
            logger.warning(f"Unsupported filter condition: {condition}")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"DataFrame filtering failed: {e}")
        return pd.DataFrame()

def validate_dataframe_structure(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that DataFrame has required columns.
    
    Args:
        df: Input DataFrame
        required_columns: List of required column names
        
    Returns:
        bool: True if all required columns are present
    """
    if not isinstance(df, pd.DataFrame):
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.warning(f"Missing required columns: {missing_columns}")
        return False
    
    return True

def safe_aggregation(df: pd.DataFrame, group_by: str, agg_column: str, agg_func: str = 'sum') -> pd.DataFrame:
    """
    Safely perform DataFrame aggregation with error handling.
    
    Args:
        df: Input DataFrame
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_func: Aggregation function ('sum', 'mean', 'count', etc.)
        
    Returns:
        pandas.DataFrame: Aggregated result or empty DataFrame on error
    """
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()
    
    try:
        if group_by not in df.columns:
            logger.warning(f"Group by column '{group_by}' not found")
            return pd.DataFrame()
        
        if agg_column not in df.columns:
            logger.warning(f"Aggregation column '{agg_column}' not found")
            return pd.DataFrame()
        
        if agg_func == 'sum':
            result = df.groupby(group_by)[agg_column].sum().reset_index()
        elif agg_func == 'mean':
            result = df.groupby(group_by)[agg_column].mean().reset_index()
        elif agg_func == 'count':
            result = df.groupby(group_by)[agg_column].count().reset_index()
        else:
            logger.warning(f"Unsupported aggregation function: {agg_func}")
            return pd.DataFrame()
        
        return result
        
    except Exception as e:
        logger.error(f"Aggregation failed: {e}")
        return pd.DataFrame()

def safe_dataframe_concat(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Safely concatenate multiple DataFrames with error handling.
    
    Args:
        dataframes: List of DataFrames to concatenate
        
    Returns:
        pandas.DataFrame: Concatenated result or empty DataFrame on error
    """
    try:
        # Filter out None and non-DataFrame objects
        valid_dfs = [df for df in dataframes if isinstance(df, pd.DataFrame) and not df.empty]
        
        if not valid_dfs:
            logger.warning("No valid DataFrames to concatenate")
            return pd.DataFrame()
        
        if len(valid_dfs) == 1:
            return valid_dfs[0].copy()
        
        return pd.concat(valid_dfs, ignore_index=True)
        
    except Exception as e:
        logger.error(f"DataFrame concatenation failed: {e}")
        return pd.DataFrame()

# Convenience functions for common operations
def safe_sort_values(df: pd.DataFrame, by: str, ascending: bool = True, **kwargs) -> pd.DataFrame:
    """Safe sort_values operation"""
    return safe_dataframe_operation(df, "sort_values", by=by, ascending=ascending, **kwargs)

def safe_iloc(df: pd.DataFrame, index: int) -> pd.DataFrame:
    """Safe iloc operation that returns DataFrame, not Series"""
    return safe_dataframe_operation(df, "iloc", index=index)

def safe_groupby(df: pd.DataFrame, by: str, **kwargs) -> pd.DataFrame:
    """Safe groupby operation"""
    return safe_dataframe_operation(df, "groupby", by=by, **kwargs) 