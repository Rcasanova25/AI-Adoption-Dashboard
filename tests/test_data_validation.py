"""
Unit tests for data validation utilities
Tests the DataValidator class and related functions
"""

import pytest
import pandas as pd
import numpy as np
from utils.data_validation import DataValidator, DataStatus, ValidationResult, safe_plot_check


class TestDataValidator:
    """Test cases for DataValidator class"""
    
    def test_validate_none_dataframe(self):
        """Test validation of None input"""
        validator = DataValidator()
        result = validator.validate_dataframe(None, "test_data", show_warning=False)
        
        assert result.status == DataStatus.INVALID
        assert "is None" in result.message
        assert not result.is_valid
    
    def test_validate_wrong_type(self):
        """Test validation of non-DataFrame input"""
        validator = DataValidator()
        result = validator.validate_dataframe("not_a_dataframe", "test_data", show_warning=False)
        
        assert result.status == DataStatus.WRONG_TYPE
        assert "not a DataFrame" in result.message
        assert not result.is_valid
    
    def test_validate_empty_dataframe(self):
        """Test validation of empty DataFrame"""
        validator = DataValidator()
        empty_df = pd.DataFrame()
        result = validator.validate_dataframe(empty_df, "test_data", show_warning=False)
        
        assert result.status == DataStatus.EMPTY
        assert "insufficient data" in result.message
        assert not result.is_valid
    
    def test_validate_missing_columns(self):
        """Test validation with missing required columns"""
        validator = DataValidator()
        df = pd.DataFrame({'col1': [1, 2, 3]})
        result = validator.validate_dataframe(
            df, "test_data", 
            required_columns=['col1', 'col2'], 
            show_warning=False
        )
        
        assert result.status == DataStatus.MISSING_COLUMNS
        assert 'col2' in result.missing_columns
        assert not result.is_valid
    
    def test_validate_successful(self):
        """Test successful validation"""
        validator = DataValidator()
        df = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'value': [10.5, 20.3, 30.1]
        })
        result = validator.validate_dataframe(
            df, "test_data",
            required_columns=['year', 'value'],
            show_warning=False
        )
        
        assert result.status == DataStatus.VALID
        assert result.is_valid
        assert "successfully" in result.message
    
    def test_validate_min_rows(self):
        """Test minimum rows requirement"""
        validator = DataValidator()
        df = pd.DataFrame({'col1': [1, 2]})  # Only 2 rows
        result = validator.validate_dataframe(
            df, "test_data",
            min_rows=5,  # Require 5 rows
            show_warning=False
        )
        
        assert result.status == DataStatus.EMPTY
        assert not result.is_valid
    
    def test_validate_column_types(self):
        """Test column type validation"""
        validator = DataValidator()
        df = pd.DataFrame({
            'year': ['2020', '2021', '2022'],  # String instead of int
            'value': [10.5, 20.3, 30.1]
        })
        result = validator.validate_dataframe(
            df, "test_data",
            required_columns=['year', 'value'],
            column_types={'year': int, 'value': float},
            show_warning=False
        )
        
        # Should still be valid after type conversion attempt
        assert result.is_valid


class TestSafePlotCheck:
    """Test cases for safe_plot_check function"""
    
    def test_safe_plot_valid_data(self):
        """Test safe plotting with valid data"""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 30, 40, 50]
        })
        
        plot_called = False
        def mock_plot():
            nonlocal plot_called
            plot_called = True
        
        result = safe_plot_check(
            df, "test_plot",
            required_columns=['x', 'y'],
            plot_func=mock_plot
        )
        
        assert result is True
        assert plot_called is True
    
    def test_safe_plot_invalid_data(self):
        """Test safe plotting with invalid data"""
        df = pd.DataFrame()  # Empty dataframe
        
        plot_called = False
        def mock_plot():
            nonlocal plot_called
            plot_called = True
        
        result = safe_plot_check(
            df, "test_plot",
            required_columns=['x', 'y'],
            plot_func=mock_plot
        )
        
        assert result is False
        assert plot_called is False
    
    def test_safe_plot_missing_columns(self):
        """Test safe plotting with missing columns"""
        df = pd.DataFrame({'x': [1, 2, 3]})  # Missing 'y' column
        
        plot_called = False
        def mock_plot():
            nonlocal plot_called
            plot_called = True
        
        result = safe_plot_check(
            df, "test_plot",
            required_columns=['x', 'y'],
            plot_func=mock_plot
        )
        
        assert result is False
        assert plot_called is False


class TestValidationResult:
    """Test cases for ValidationResult class"""
    
    def test_validation_result_valid(self):
        """Test ValidationResult for valid status"""
        result = ValidationResult(DataStatus.VALID, "Test message")
        assert result.is_valid is True
    
    def test_validation_result_invalid(self):
        """Test ValidationResult for invalid status"""
        result = ValidationResult(DataStatus.INVALID, "Test message")
        assert result.is_valid is False
    
    def test_validation_result_with_data(self):
        """Test ValidationResult with data"""
        df = pd.DataFrame({'col': [1, 2, 3]})
        result = ValidationResult(DataStatus.VALID, "Test message", data=df)
        assert result.data is not None
        assert len(result.data) == 3


# Sample data for integration tests
@pytest.fixture
def sample_historical_data():
    """Sample historical data fixture"""
    return pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'ai_use': [45, 50, 55, 65, 78],
        'genai_use': [0, 0, 33, 55, 71]
    })


@pytest.fixture
def sample_sector_data():
    """Sample sector data fixture"""
    return pd.DataFrame({
        'sector': ['Technology', 'Finance', 'Healthcare'],
        'adoption_rate': [85, 75, 65],
        'genai_adoption': [80, 70, 60]
    })


class TestIntegration:
    """Integration tests using sample data"""
    
    def test_historical_data_validation(self, sample_historical_data):
        """Test validation of historical data structure"""
        validator = DataValidator()
        result = validator.validate_dataframe(
            sample_historical_data,
            "historical_data",
            required_columns=['year', 'ai_use'],
            show_warning=False
        )
        
        assert result.is_valid
        assert result.status == DataStatus.VALID
    
    def test_sector_data_validation(self, sample_sector_data):
        """Test validation of sector data structure"""
        validator = DataValidator()
        result = validator.validate_dataframe(
            sample_sector_data,
            "sector_data",
            required_columns=['sector', 'adoption_rate'],
            show_warning=False
        )
        
        assert result.is_valid
        assert result.status == DataStatus.VALID


if __name__ == "__main__":
    pytest.main([__file__])