"""
Simple data validation without Pydantic dependency
Provides type safety and validation using standard Python
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ValidationResult:
    """Simple validation result class"""
    def __init__(self, is_valid: bool, error_message: str = None, 
                 warning_messages: List[str] = None, validated_rows: int = 0, total_rows: int = 0):
        self.is_valid = is_valid
        self.error_message = error_message
        self.warning_messages = warning_messages or []
        self.validated_rows = validated_rows
        self.total_rows = total_rows


def validate_historical_data(df: pd.DataFrame) -> ValidationResult:
    """Validate historical AI adoption data"""
    if df is None or df.empty:
        return ValidationResult(False, "DataFrame is None or empty", total_rows=0)
    
    required_columns = ['year', 'ai_use', 'genai_use']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return ValidationResult(False, f"Missing columns: {missing_columns}", total_rows=len(df))
    
    errors = []
    warnings = []
    validated_rows = 0
    
    for idx, row in df.iterrows():
        try:
            # Validate year
            year = row['year']
            if not isinstance(year, (int, float)) or year < 2017 or year > 2025:
                errors.append(f"Row {idx}: Invalid year {year} (must be 2017-2025)")
                continue
            
            # Validate percentages
            ai_use = row['ai_use']
            genai_use = row['genai_use']
            
            if not (0 <= ai_use <= 100):
                errors.append(f"Row {idx}: AI use {ai_use}% must be 0-100%")
                continue
                
            if not (0 <= genai_use <= 100):
                errors.append(f"Row {idx}: GenAI use {genai_use}% must be 0-100%")
                continue
            
            # Business rule: GenAI cannot exceed AI use
            if genai_use > ai_use:
                errors.append(f"Row {idx}: GenAI use ({genai_use}%) cannot exceed AI use ({ai_use}%)")
                continue
            
            validated_rows += 1
            
        except Exception as e:
            errors.append(f"Row {idx}: Validation error - {e}")
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors[:5]) if errors else None  # Limit to first 5 errors
    
    return ValidationResult(is_valid, error_message, warnings, validated_rows, len(df))


def validate_sector_data(df: pd.DataFrame) -> ValidationResult:
    """Validate sector AI adoption data"""
    if df is None or df.empty:
        return ValidationResult(False, "DataFrame is None or empty", total_rows=0)
    
    required_columns = ['sector', 'adoption_rate', 'avg_roi']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return ValidationResult(False, f"Missing columns: {missing_columns}", total_rows=len(df))
    
    valid_sectors = {
        'Technology', 'Financial Services', 'Healthcare', 'Manufacturing',
        'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government',
        'Information', 'Professional Services', 'Finance & Insurance', 'Retail Trade', 'Construction'
    }
    
    errors = []
    warnings = []
    validated_rows = 0
    
    for idx, row in df.iterrows():
        try:
            # Validate sector name
            sector = row['sector']
            if sector not in valid_sectors:
                warnings.append(f"Row {idx}: Sector '{sector}' not in standard list")
            
            # Validate adoption rate
            adoption_rate = row['adoption_rate']
            if not (0 <= adoption_rate <= 100):
                errors.append(f"Row {idx}: Adoption rate {adoption_rate}% must be 0-100%")
                continue
            
            # Validate ROI
            avg_roi = row['avg_roi']
            if avg_roi <= 0:
                errors.append(f"Row {idx}: ROI {avg_roi} must be positive")
                continue
            
            if avg_roi > 10:
                warnings.append(f"Row {idx}: ROI {avg_roi}x is unusually high")
            
            # Validate GenAI adoption if present
            if 'genai_adoption' in df.columns and pd.notna(row['genai_adoption']):
                genai_adoption = row['genai_adoption']
                if genai_adoption > adoption_rate:
                    errors.append(f"Row {idx}: GenAI adoption ({genai_adoption}%) cannot exceed overall adoption ({adoption_rate}%)")
                    continue
            
            validated_rows += 1
            
        except Exception as e:
            errors.append(f"Row {idx}: Validation error - {e}")
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors[:5]) if errors else None
    
    return ValidationResult(is_valid, error_message, warnings, validated_rows, len(df))


def validate_investment_data(df: pd.DataFrame) -> ValidationResult:
    """Validate AI investment data"""
    if df is None or df.empty:
        return ValidationResult(False, "DataFrame is None or empty", total_rows=0)
    
    required_columns = ['year', 'total_investment']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return ValidationResult(False, f"Missing columns: {missing_columns}", total_rows=len(df))
    
    errors = []
    warnings = []
    validated_rows = 0
    
    for idx, row in df.iterrows():
        try:
            # Validate year
            year = row['year']
            if not isinstance(year, (int, float)) or year < 2014 or year > 2030:
                errors.append(f"Row {idx}: Invalid year {year} (must be 2014-2030)")
                continue
            
            # Validate investment amounts
            total_investment = row['total_investment']
            if total_investment < 0:
                errors.append(f"Row {idx}: Total investment {total_investment} cannot be negative")
                continue
            
            # Check GenAI investment vs total
            if 'genai_investment' in df.columns and pd.notna(row['genai_investment']):
                genai_investment = row['genai_investment']
                if genai_investment > total_investment:
                    errors.append(f"Row {idx}: GenAI investment ({genai_investment}B) cannot exceed total ({total_investment}B)")
                    continue
            
            # Warn about low investment for recent years
            if year >= 2020 and total_investment < 50:
                warnings.append(f"Row {idx}: Investment {total_investment}B seems low for year {year}")
            
            validated_rows += 1
            
        except Exception as e:
            errors.append(f"Row {idx}: Validation error - {e}")
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors[:5]) if errors else None
    
    return ValidationResult(is_valid, error_message, warnings, validated_rows, len(df))


def validate_financial_impact_data(df: pd.DataFrame) -> ValidationResult:
    """Validate financial impact data"""
    if df is None or df.empty:
        return ValidationResult(False, "DataFrame is None or empty", total_rows=0)
    
    required_columns = ['function', 'companies_reporting_cost_savings', 'companies_reporting_revenue_gains']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return ValidationResult(False, f"Missing columns: {missing_columns}", total_rows=len(df))
    
    valid_functions = {
        'Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering',
        'Product Development', 'IT', 'HR', 'Finance', 'Operations', 'Customer Service'
    }
    
    errors = []
    warnings = []
    validated_rows = 0
    
    for idx, row in df.iterrows():
        try:
            # Validate function name
            function = row['function']
            if function not in valid_functions:
                warnings.append(f"Row {idx}: Function '{function}' not in standard list")
            
            # Validate percentages
            cost_savings = row['companies_reporting_cost_savings']
            revenue_gains = row['companies_reporting_revenue_gains']
            
            if not (0 <= cost_savings <= 100):
                errors.append(f"Row {idx}: Cost savings percentage {cost_savings}% must be 0-100%")
                continue
                
            if not (0 <= revenue_gains <= 100):
                errors.append(f"Row {idx}: Revenue gains percentage {revenue_gains}% must be 0-100%")
                continue
            
            validated_rows += 1
            
        except Exception as e:
            errors.append(f"Row {idx}: Validation error - {e}")
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors[:5]) if errors else None
    
    return ValidationResult(is_valid, error_message, warnings, validated_rows, len(df))


# Validation registry mapping dataset names to validation functions
VALIDATION_REGISTRY = {
    "historical_data": validate_historical_data,
    "sector_data": validate_sector_data,
    "investment_data": validate_investment_data,
    "financial_impact": validate_financial_impact_data,
}


def validate_dataset(df: pd.DataFrame, dataset_name: str) -> ValidationResult:
    """
    Validate a dataset using its registered validation function
    
    Args:
        df: DataFrame to validate
        dataset_name: Name of the dataset
    
    Returns:
        ValidationResult with validation status
    """
    validator_func = VALIDATION_REGISTRY.get(dataset_name)
    if validator_func is None:
        return ValidationResult(
            False, 
            f"No validation function found for dataset: {dataset_name}",
            total_rows=len(df) if df is not None else 0
        )
    
    try:
        return validator_func(df)
    except Exception as e:
        return ValidationResult(
            False,
            f"Validation function failed: {e}",
            total_rows=len(df) if df is not None else 0
        )


def safe_validate_data(df: pd.DataFrame, dataset_name: str, show_warnings: bool = True) -> bool:
    """
    Safely validate data with user-friendly output
    
    Args:
        df: DataFrame to validate
        dataset_name: Name of the dataset
        show_warnings: Whether to display warnings in UI
    
    Returns:
        True if validation passes, False otherwise
    """
    try:
        result = validate_dataset(df, dataset_name)
        
        if result.is_valid:
            logger.info(f"✅ {dataset_name} validation passed ({result.validated_rows}/{result.total_rows} rows)")
            
            # Log warnings
            for warning in result.warning_messages:
                logger.warning(f"⚠️ {dataset_name}: {warning}")
            
            return True
        else:
            logger.error(f"❌ {dataset_name} validation failed: {result.error_message}")
            if show_warnings:
                try:
                    import streamlit as st
                    st.warning(f"Data validation issues for {dataset_name}: {result.error_message}")
                except:
                    pass  # Streamlit not available
            return False
            
    except Exception as e:
        logger.error(f"Validation error for {dataset_name}: {e}")
        return False


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> ValidationResult:
    """
    Validate that DataFrame has required columns
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
    
    Returns:
        ValidationResult with validation status
    """
    if df is None:
        return ValidationResult(False, "DataFrame is None", total_rows=0)
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    extra_columns = [col for col in df.columns if col not in required_columns]
    
    warnings = []
    if extra_columns:
        warnings.append(f"Extra columns found: {extra_columns}")
    
    if missing_columns:
        return ValidationResult(
            False,
            f"Missing required columns: {missing_columns}",
            warnings,
            total_rows=len(df)
        )
    
    return ValidationResult(True, None, warnings, len(df), len(df))