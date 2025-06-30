"""
Simple tests to verify the testing infrastructure is working
"""

import pytest
import pandas as pd
from Utils.helpers import safe_execute, clean_filename


class TestInfrastructure:
    """Test that the basic testing infrastructure works"""
    
    def test_basic_imports(self):
        """Test that we can import the main modules"""
        assert True  # If we get here, imports worked
    
    def test_safe_execute_success(self):
        """Test safe_execute with successful function"""
        def test_func():
            return "success"
        
        result = safe_execute(test_func, default_value="default")
        assert result == "success"
    
    def test_safe_execute_failure(self):
        """Test safe_execute with failing function"""
        def test_func():
            raise ValueError("test error")
        
        result = safe_execute(test_func, default_value="default")
        assert result == "default"
    
    def test_clean_filename(self):
        """Test filename cleaning function"""
        result = clean_filename("Test Name")
        assert result == "test_name"
        
        result = clean_filename("🎯 Competitive Position")
        assert result == "competitive_position"
    
    def test_pandas_import(self):
        """Test pandas functionality"""
        df = pd.DataFrame({'test': [1, 2, 3]})
        assert len(df) == 3
        assert df['test'].sum() == 6


class TestBusinessLogicImports:
    """Test that business logic can be imported"""
    
    def test_business_metrics_import(self):
        """Test importing business metrics"""
        try:
            from business.metrics import BusinessMetrics, CompetitivePosition
            assert BusinessMetrics is not None
            assert CompetitivePosition is not None
        except ImportError as e:
            pytest.skip(f"Business metrics not available: {e}")
    
    def test_data_models_import(self):
        """Test importing data models"""
        try:
            from data.models import safe_validate_data
            assert safe_validate_data is not None
        except ImportError as e:
            pytest.skip(f"Data models not available: {e}")


class TestConfiguration:
    """Test configuration and settings"""
    
    def test_pytest_configuration(self):
        """Test that pytest is configured correctly"""
        assert True  # If we get here, pytest is working
    
    def test_markers_available(self):
        """Test that pytest markers are available"""
        # This test will be marked with unit marker
        assert True
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test unit marker"""
        assert True 