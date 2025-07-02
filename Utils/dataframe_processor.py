"""
DataFrame Processing and Optimization Utilities
Implements comprehensive DataFrame validation, type standardization, and memory optimization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from pathlib import Path

from data.models import CompanySize, DataQuality, DataSource

logger = logging.getLogger(__name__)


class DataFrameProcessor:
    """
    Comprehensive DataFrame processing and optimization utilities
    """
    
    @staticmethod
    def validate_dataframe(
        df: pd.DataFrame, 
        required_columns: List[str],
        optional_columns: List[str] = None,
        min_rows: int = 1
    ) -> Tuple[bool, List[str], pd.DataFrame]:
        """
        Validate DataFrame structure and content with comprehensive checks
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            optional_columns: List of optional column names
            min_rows: Minimum number of rows required
            
        Returns:
            Tuple of (is_valid, error_messages, cleaned_dataframe)
        """
        errors = []
        
        # Check if DataFrame exists and is not None
        if df is None:
            return False, ["DataFrame is None"], pd.DataFrame()
        
        # Check if DataFrame is empty
        if df.empty:
            return False, ["DataFrame is empty"], df
        
        # Check minimum rows
        if len(df) < min_rows:
            errors.append(f"DataFrame has {len(df)} rows, minimum {min_rows} required")
        
        # Check for required columns
        missing_required = set(required_columns) - set(df.columns)
        if missing_required:
            errors.append(f"Missing required columns: {list(missing_required)}")
        
        # Check for duplicate columns
        if df.columns.duplicated().any():
            duplicate_cols = df.columns[df.columns.duplicated()].tolist()
            errors.append(f"Duplicate columns found: {duplicate_cols}")
            
        # Check for completely empty columns
        empty_cols = df.columns[df.isnull().all()].tolist()
        if empty_cols:
            logger.warning(f"Found completely empty columns: {empty_cols}")
            df = df.drop(columns=empty_cols)
        
        # Return validation results
        is_valid = len(errors) == 0
        return is_valid, errors, df
    
    @staticmethod
    def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize data types across datasets
        
        Args:
            df: DataFrame to standardize
            
        Returns:
            DataFrame with standardized types
        """
        df = df.copy()
        
        try:
            # Convert percentage columns
            percentage_cols = [
                'adoption_rate', 'genai_adoption', 'growth_rate', 
                'roi_percentage', 'avg_roi', 'firm_weighted', 'employment_weighted'
            ]
            for col in percentage_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # Clip values to valid percentage range
                    df[col] = df[col].clip(0, 100)
            
            # Standardize company size categories
            if 'company_size' in df.columns:
                size_mapping = {
                    'SMB': CompanySize.SMALL,
                    'Small': CompanySize.SMALL,
                    'small': CompanySize.SMALL,
                    'Medium': CompanySize.MEDIUM,
                    'medium': CompanySize.MEDIUM,
                    'Mid-Market': CompanySize.MEDIUM,
                    'Large': CompanySize.LARGE,
                    'large': CompanySize.LARGE,
                    'Enterprise': CompanySize.ENTERPRISE,
                    'enterprise': CompanySize.ENTERPRISE
                }
                df['company_size'] = df['company_size'].map(size_mapping).fillna(df['company_size'])
            
            # Standardize sector names
            if 'sector' in df.columns:
                df['sector'] = df['sector'].str.title().str.strip()
                
                # Apply sector name mapping
                sector_mapping = {
                    'Tech': 'Technology',
                    'Finance': 'Financial Services',
                    'Fintech': 'Financial Services',
                    'Healthcare': 'Healthcare',
                    'Manufacturing': 'Manufacturing',
                    'Retail': 'Retail & E-commerce',
                    'Education': 'Education',
                    'Energy': 'Energy & Utilities',
                    'Government': 'Government'
                }
                df['sector'] = df['sector'].replace(sector_mapping)
            
            # Convert years to integers
            if 'year' in df.columns:
                df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
                # Validate year range
                df = df[(df['year'] >= 2017) & (df['year'] <= 2025)]
            
            # Standardize boolean columns
            bool_cols = ['has_ai_strategy', 'reports_roi', 'uses_genai']
            for col in bool_cols:
                if col in df.columns:
                    df[col] = df[col].astype('boolean')
            
            # Standardize string columns
            string_cols = ['sector', 'company_name', 'function']
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].astype('string')
            
            logger.info("Data types standardized successfully")
            
        except Exception as e:
            logger.error(f"Error standardizing data types: {str(e)}")
        
        return df
    
    @staticmethod
    def optimize_dataframe_memory(df: pd.DataFrame, aggressive: bool = False) -> pd.DataFrame:
        """
        Optimize DataFrame memory usage
        
        Args:
            df: DataFrame to optimize
            aggressive: Whether to apply aggressive optimization
            
        Returns:
            Memory-optimized DataFrame
        """
        df = df.copy()
        original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        
        try:
            # Convert object columns to categories for repeated values
            for col in df.select_dtypes(include=['object']).columns:
                unique_ratio = df[col].nunique() / len(df)
                if unique_ratio < 0.5:  # Less than 50% unique values
                    df[col] = df[col].astype('category')
            
            # Optimize integer types
            for col in df.select_dtypes(include=['int64']).columns:
                col_min = df[col].min()
                col_max = df[col].max()
                
                if col_min >= 0:  # Unsigned integers
                    if col_max <= 255:
                        df[col] = df[col].astype('uint8')
                    elif col_max <= 65535:
                        df[col] = df[col].astype('uint16')
                    elif col_max <= 4294967295:
                        df[col] = df[col].astype('uint32')
                else:  # Signed integers
                    if col_min >= -128 and col_max <= 127:
                        df[col] = df[col].astype('int8')
                    elif col_min >= -32768 and col_max <= 32767:
                        df[col] = df[col].astype('int16')
                    elif col_min >= -2147483648 and col_max <= 2147483647:
                        df[col] = df[col].astype('int32')
            
            # Optimize float types
            for col in df.select_dtypes(include=['float64']).columns:
                if aggressive:
                    # Check if values can fit in float32
                    df_temp = df[col].astype('float32')
                    if np.allclose(df[col], df_temp, equal_nan=True):
                        df[col] = df_temp
                else:
                    # Use pandas downcast
                    df[col] = pd.to_numeric(df[col], downcast='float')
            
            optimized_memory = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
            reduction = ((original_memory - optimized_memory) / original_memory) * 100
            
            logger.info(f"Memory optimization: {original_memory:.2f}MB → {optimized_memory:.2f}MB ({reduction:.1f}% reduction)")
            
        except Exception as e:
            logger.error(f"Error optimizing DataFrame memory: {str(e)}")
        
        return df
    
    @staticmethod
    def handle_missing_data(
        df: pd.DataFrame,
        strategy: str = 'drop',
        threshold: float = 0.5
    ) -> pd.DataFrame:
        """
        Handle missing data with various strategies
        
        Args:
            df: DataFrame with missing data
            strategy: Strategy to handle missing data ('drop', 'fill', 'interpolate')
            threshold: Threshold for dropping columns/rows (0.0 to 1.0)
            
        Returns:
            DataFrame with missing data handled
        """
        df = df.copy()
        
        try:
            # Drop columns with too many missing values
            missing_ratio = df.isnull().sum() / len(df)
            cols_to_drop = missing_ratio[missing_ratio > threshold].index.tolist()
            if cols_to_drop:
                logger.warning(f"Dropping columns with >{threshold*100}% missing: {cols_to_drop}")
                df = df.drop(columns=cols_to_drop)
            
            if strategy == 'drop':
                # Drop rows with any missing values in key columns
                key_columns = ['year', 'sector'] if 'year' in df.columns else []
                if key_columns:
                    df = df.dropna(subset=key_columns)
                
            elif strategy == 'fill':
                # Fill missing values with appropriate defaults
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns
                
                # Fill numeric with median
                for col in numeric_cols:
                    df[col] = df[col].fillna(df[col].median())
                
                # Fill categorical with mode or 'Unknown'
                for col in categorical_cols:
                    mode_value = df[col].mode()
                    fill_value = mode_value[0] if len(mode_value) > 0 else 'Unknown'
                    df[col] = df[col].fillna(fill_value)
                    
            elif strategy == 'interpolate':
                # Interpolate numeric columns
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                for col in numeric_cols:
                    df[col] = df[col].interpolate(method='linear')
            
            logger.info(f"Missing data handled using strategy: {strategy}")
            
        except Exception as e:
            logger.error(f"Error handling missing data: {str(e)}")
        
        return df
    
    @staticmethod
    def detect_outliers(
        df: pd.DataFrame,
        columns: List[str] = None,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> Dict[str, List[int]]:
        """
        Detect outliers in DataFrame columns
        
        Args:
            df: DataFrame to analyze
            columns: Columns to check for outliers (None for all numeric)
            method: Method to use ('iqr', 'zscore', 'isolation')
            threshold: Threshold for outlier detection
            
        Returns:
            Dictionary mapping column names to lists of outlier indices
        """
        outliers = {}
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        try:
            for col in columns:
                if col not in df.columns:
                    continue
                    
                col_outliers = []
                
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    col_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                
                elif method == 'zscore':
                    from scipy import stats
                    z_scores = np.abs(stats.zscore(df[col].dropna()))
                    col_outliers = df[df[col].notna()].iloc[z_scores > threshold].index.tolist()
                
                elif method == 'isolation':
                    from sklearn.ensemble import IsolationForest
                    isolation_forest = IsolationForest(contamination=0.1, random_state=42)
                    outlier_labels = isolation_forest.fit_predict(df[[col]].dropna())
                    col_outliers = df[df[col].notna()].iloc[outlier_labels == -1].index.tolist()
                
                if col_outliers:
                    outliers[col] = col_outliers
                    logger.info(f"Found {len(col_outliers)} outliers in column '{col}'")
        
        except Exception as e:
            logger.error(f"Error detecting outliers: {str(e)}")
        
        return outliers
    
    @staticmethod
    def add_data_quality_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add data quality indicators to DataFrame
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            DataFrame with quality indicators added
        """
        df = df.copy()
        
        try:
            # Calculate completeness score (0-100)
            completeness = ((df.notna().sum(axis=1) / len(df.columns)) * 100).round(1)
            df['data_completeness'] = completeness
            
            # Assign quality categories
            df['data_quality'] = pd.cut(
                completeness,
                bins=[0, 50, 75, 90, 100],
                labels=[DataQuality.POOR, DataQuality.FAIR, DataQuality.GOOD, DataQuality.EXCELLENT],
                include_lowest=True
            )
            
            # Add freshness indicator (if year column exists)
            if 'year' in df.columns:
                current_year = 2025  # Dashboard context
                df['data_age'] = current_year - df['year']
                df['is_recent'] = df['data_age'] <= 2  # Recent if within 2 years
            
            logger.info("Data quality indicators added successfully")
            
        except Exception as e:
            logger.error(f"Error adding data quality indicators: {str(e)}")
        
        return df


# Convenience functions for common operations
def quick_validate(df: pd.DataFrame, required_cols: List[str]) -> bool:
    """Quick validation check for DataFrames"""
    is_valid, errors, _ = DataFrameProcessor.validate_dataframe(df, required_cols)
    if not is_valid:
        logger.warning(f"DataFrame validation failed: {errors}")
    return is_valid


def prepare_for_visualization(df: pd.DataFrame, optimize_memory: bool = True) -> pd.DataFrame:
    """Prepare DataFrame for visualization with all optimizations"""
    processor = DataFrameProcessor()
    
    # Apply all optimizations
    df = processor.standardize_data_types(df)
    df = processor.handle_missing_data(df, strategy='fill')
    df = processor.add_data_quality_indicators(df)
    
    if optimize_memory:
        df = processor.optimize_dataframe_memory(df)
    
    return df


def validate_upload_data(df: pd.DataFrame, expected_schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate uploaded data against expected schema"""
    errors = []
    
    # Check required columns
    required_columns = expected_schema.get('required_columns', [])
    is_valid, validation_errors, _ = DataFrameProcessor.validate_dataframe(df, required_columns)
    errors.extend(validation_errors)
    
    # Check data types
    if 'column_types' in expected_schema:
        for col, expected_type in expected_schema['column_types'].items():
            if col in df.columns:
                if not df[col].dtype == expected_type:
                    errors.append(f"Column '{col}' has type {df[col].dtype}, expected {expected_type}")
    
    # Check value ranges
    if 'value_ranges' in expected_schema:
        for col, (min_val, max_val) in expected_schema['value_ranges'].items():
            if col in df.columns:
                out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
                if not out_of_range.empty:
                    errors.append(f"Column '{col}' has {len(out_of_range)} values outside range [{min_val}, {max_val}]")
    
    return len(errors) == 0, errors