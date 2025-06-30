# test_suite.py - Comprehensive Testing Suite for AI Adoption Dashboard

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
from datetime import datetime
import tempfile
import os

# Import your modules (adjust paths as needed)
from business.metrics import BusinessMetrics, CompetitivePosition, InvestmentRecommendation
from data.loaders import load_all_datasets, validate_all_loaded_data
from data.models import safe_validate_data, ValidationResult
from Utils.helpers import safe_execute, safe_data_check, clean_filename, monitor_performance

class TestBusinessLogic:
    """Test suite for core business logic modules"""
    
    def test_competitive_position_assessment(self):
        """Test competitive position assessment logic"""
        # Test leader position
        assessment = BusinessMetrics.assess_competitive_position(
            industry="Technology (92% adoption)",
            company_size="5000+ employees (58% adoption)",
            maturity="Leading (80%+)",
            urgency=5
        )
        
        assert assessment.position == CompetitivePosition.LEADER
        assert assessment.score >= 80
        assert len(assessment.recommendations) > 0
        
        # Test laggard position
        assessment_laggard = BusinessMetrics.assess_competitive_position(
            industry="Government (52% adoption)",
            company_size="1-50 employees (3% adoption)",
            maturity="Exploring (0-10%)",
            urgency=8
        )
        
        assert assessment_laggard.position == CompetitivePosition.LAGGARD
        assert assessment_laggard.score < 30
        assert "URGENT" in str(assessment_laggard.recommendations)
    
    def test_investment_case_calculation(self):
        """Test investment case calculations"""
        case = BusinessMetrics.calculate_investment_case(
            investment_amount=500000,
            timeline_months=12,
            industry="Technology",
            goal="Operational Efficiency",
            risk_tolerance="Medium"
        )
        
        # Validate financial calculations
        assert case.expected_roi > 0
        assert case.total_return > case.investment_amount
        assert case.net_benefit == case.total_return - case.investment_amount
        assert case.payback_months > 0
        assert case.payback_months <= case.timeline_months * 2  # Reasonable payback
        
        # Test edge cases
        case_high_risk = BusinessMetrics.calculate_investment_case(
            investment_amount=10000000,
            timeline_months=6,
            industry="Government",
            goal="Innovation & New Products",
            risk_tolerance="Low"
        )
        
        assert case_high_risk.recommendation in [
            InvestmentRecommendation.CONDITIONAL,
            InvestmentRecommendation.REJECT
        ]
    
    def test_roi_consistency(self):
        """Test ROI calculations for consistency"""
        test_cases = [
            (100000, 12, "Technology", "Cost Reduction"),
            (1000000, 24, "Healthcare", "Revenue Growth"),
            (50000, 6, "Manufacturing", "Operational Efficiency")
        ]
        
        for amount, timeline, industry, goal in test_cases:
            case = BusinessMetrics.calculate_investment_case(
                amount, timeline, industry, goal, "Medium"
            )
            
            # ROI should be reasonable (0.5x to 10x)
            assert 0.5 <= case.expected_roi <= 10.0
            
            # Monthly benefit should be positive
            assert case.monthly_benefit > 0
            
            # Confidence level should be valid
            assert case.confidence_level in ["Low", "Medium", "High"]

class TestDataValidation:
    """Test suite for data validation and loading"""
    
    def create_sample_data(self):
        """Create sample datasets for testing"""
        return {
            'historical_data': pd.DataFrame({
                'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                'ai_use': [5.8, 12.1, 18.5, 27.3, 37.2, 55.0, 78.0, 82.1],
                'genai_use': [0, 0, 0, 2.1, 33.0, 71.0, 75.3, 78.2]
            }),
            'sector_2025': pd.DataFrame({
                'sector': ['Technology', 'Finance', 'Healthcare'],
                'adoption_rate': [92, 85, 78],
                'avg_roi': [4.2, 3.8, 3.1],
                'genai_adoption': [89, 76, 68]
            }),
            'investment_data': pd.DataFrame({
                'year': [2022, 2023, 2024],
                'total_investment': [174.5, 207.8, 252.3],
                'genai_investment': [5.2, 18.7, 33.9]
            })
        }
    
    def test_data_loading(self):
        """Test data loading functionality"""
        # Test with valid data
        sample_data = self.create_sample_data()
        
        with patch('data.loaders.load_all_datasets', return_value=sample_data):
            loaded_data = load_all_datasets()
            
            assert loaded_data is not None
            assert 'historical_data' in loaded_data
            assert 'sector_2025' in loaded_data
            assert 'investment_data' in loaded_data
    
    def test_data_validation(self):
        """Test data validation functions"""
        sample_data = self.create_sample_data()
        
        # Test valid data
        result = safe_validate_data(sample_data['historical_data'], "historical_data")
        assert result.is_valid == True
        assert len(result.errors) == 0
        
        # Test invalid data (missing columns)
        invalid_data = pd.DataFrame({'wrong_column': [1, 2, 3]})
        result_invalid = safe_validate_data(invalid_data, "historical_data")
        assert result_invalid.is_valid == False
        assert len(result_invalid.errors) > 0
    
    def test_safe_data_check(self):
        """Test safe data checking utility"""
        valid_data = pd.DataFrame({'col1': [1, 2, 3]})
        empty_data = pd.DataFrame()
        none_data = None
        
        # Test valid data
        assert safe_data_check(valid_data, "test_data") == True
        
        # Test empty data
        assert safe_data_check(empty_data, "test_data") == False
        
        # Test None data
        assert safe_data_check(none_data, "test_data") == False

class TestUtilityFunctions:
    """Test suite for utility functions"""
    
    def test_clean_filename(self):
        """Test filename cleaning function"""
        test_cases = [
            ("🎯 Competitive Position Assessor", "competitive_position_assessor"),
            ("💰 Investment Decision Engine", "investment_decision_engine"),
            ("Simple Name", "simple_name"),
            ("Name with Spaces & Special!@#", "name_with_spaces_special"),
            ("Multiple___Underscores", "multiple_underscores"),
            ("CamelCase Name", "camelcase_name")
        ]
        
        for input_name, expected in test_cases:
            result = clean_filename(input_name)
            assert result == expected
            # Ensure result is safe for all OS
            assert not any(char in result for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*'])
    
    def test_safe_execute(self):
        """Test safe execution wrapper"""
        # Test successful execution
        def successful_func():
            return "success"
        
        result = safe_execute(successful_func, "default", "error")
        assert result == "success"
        
        # Test exception handling
        def failing_func():
            raise ValueError("Test error")
        
        result = safe_execute(failing_func, "default", "error")
        assert result == "default"
    
    @patch('time.time')
    def test_monitor_performance(self, mock_time):
        """Test performance monitoring decorator"""
        mock_time.side_effect = [0, 1]  # 1 second execution
        
        @monitor_performance
        def test_function():
            return "result"
        
        result = test_function()
        assert result == "result"

class TestChartValidation:
    """Test suite for chart data validation"""
    
    def test_validate_chart_data(self):
        """Test chart data validation"""
        # Test valid data
        valid_data = pd.DataFrame({
            'year': [2023, 2024, 2025],
            'value': [10, 20, 30]
        })
        
        is_valid, message = validate_chart_data(valid_data, ['year', 'value'])
        assert is_valid == True
        assert message == "Data is valid"
        
        # Test missing columns
        invalid_data = pd.DataFrame({
            'year': [2023, 2024, 2025]
        })
        
        is_valid, message = validate_chart_data(invalid_data, ['year', 'value'])
        assert is_valid == False
        assert "Missing columns" in message
        
        # Test None data
        is_valid, message = validate_chart_data(None, ['year', 'value'])
        assert is_valid == False
        assert message == "Data is None"
        
        # Test empty data
        empty_data = pd.DataFrame()
        is_valid, message = validate_chart_data(empty_data, ['year', 'value'])
        assert is_valid == False
        assert message == "Data is empty"

class TestIntegration:
    """Integration tests for end-to-end functionality"""
    
    @patch('streamlit.metric')
    @patch('streamlit.plotly_chart')
    def test_executive_dashboard_flow(self, mock_chart, mock_metric):
        """Test executive dashboard integration"""
        sample_data = {
            'historical_data': pd.DataFrame({
                'year': [2023, 2024, 2025],
                'ai_use': [55, 78, 82],
                'genai_use': [33, 71, 75]
            }),
            'sector_2025': pd.DataFrame({
                'sector': ['Technology'],
                'adoption_rate': [92],
                'avg_roi': [4.2]
            }),
            'investment_data': pd.DataFrame({
                'year': [2024],
                'total_investment': [252.3]
            })
        }
        
        # Test dynamic metrics calculation
        from app import get_dynamic_metrics
        metrics = get_dynamic_metrics(
            sample_data['historical_data'],
            None,  # ai_cost_reduction
            sample_data['investment_data'],
            sample_data['sector_2025']
        )
        
        assert 'market_adoption' in metrics
        assert 'investment_value' in metrics
        assert 'avg_roi' in metrics
        
        # Verify metrics are not hardcoded
        assert metrics['market_adoption'] == "82%"
        assert metrics['investment_value'] == "$252.3B"

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_fallback_data_creation(self):
        """Test fallback data creation when loading fails"""
        from app import _create_fallback_data
        
        # This should not raise any exceptions
        try:
            _create_fallback_data()
            assert True
        except Exception as e:
            pytest.fail(f"Fallback data creation failed: {e}")
    
    def test_missing_data_scenarios(self):
        """Test behavior with missing or corrupted data"""
        # Test with completely missing datasets
        empty_datasets = {}
        
        # Test dynamic metrics with empty data
        from app import get_dynamic_metrics
        metrics = get_dynamic_metrics(None, None, None, None)
        
        # Should return fallback values, not crash
        assert 'market_adoption' in metrics
        assert 'cost_reduction' in metrics
        
        # Test with partial data
        partial_data = pd.DataFrame({'year': [2024], 'ai_use': [50]})
        metrics_partial = get_dynamic_metrics(partial_data, None, None, None)
        assert metrics_partial['market_adoption'] == "50%"

# Performance and Load Testing
class TestPerformance:
    """Performance and load testing"""
    
    def test_large_dataset_handling(self):
        """Test performance with large datasets"""
        # Create large dataset
        large_data = pd.DataFrame({
            'year': np.repeat(range(2000, 2026), 1000),
            'ai_use': np.random.randint(0, 100, 26000),
            'genai_use': np.random.randint(0, 100, 26000)
        })
        
        start_time = datetime.now()
        
        # Test data validation performance
        result = safe_validate_data(large_data, "historical_data")
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Should complete within reasonable time (5 seconds)
        assert execution_time < 5.0
        assert result.is_valid == True
    
    def test_memory_usage(self):
        """Test memory efficiency"""
        import psutil
        import gc
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple large datasets
        datasets = []
        for i in range(10):
            data = pd.DataFrame({
                'col1': np.random.rand(10000),
                'col2': np.random.rand(10000)
            })
            datasets.append(data)
        
        # Clean up
        del datasets
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100

# Configuration for pytest
def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )

# Fixtures for common test data
@pytest.fixture
def sample_historical_data():
    """Fixture providing sample historical data"""
    return pd.DataFrame({
        'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [5.8, 12.1, 18.5, 27.3, 37.2, 55.0, 78.0, 82.1],
        'genai_use': [0, 0, 0, 2.1, 33.0, 71.0, 75.3, 78.2]
    })

@pytest.fixture
def sample_sector_data():
    """Fixture providing sample sector data"""
    return pd.DataFrame({
        'sector': ['Technology', 'Finance', 'Healthcare', 'Manufacturing'],
        'adoption_rate': [92, 85, 78, 75],
        'avg_roi': [4.2, 3.8, 3.1, 2.9],
        'genai_adoption': [89, 76, 68, 65]
    })

# Test runner script
if __name__ == "__main__":
    # Run all tests with coverage
    pytest.main([
        "-v",                    # Verbose output
        "--cov=.",              # Coverage for all modules
        "--cov-report=html",    # HTML coverage report
        "--cov-report=term",    # Terminal coverage report
        "--tb=short",           # Short traceback format
        "test_suite.py"         # This file
    ])

"""
TESTING STRATEGY IMPLEMENTATION GUIDE:

1. UNIT TESTS (70% of effort):
   - Test each business logic function in isolation
   - Validate all calculation methods
   - Test edge cases and error conditions

2. INTEGRATION TESTS (20% of effort):
   - Test data flow between modules
   - Validate dashboard rendering pipeline
   - Test user interaction scenarios

3. PERFORMANCE TESTS (10% of effort):
   - Load testing with large datasets
   - Memory usage validation
   - Response time benchmarks

RUNNING THE TESTS:

1. Install test dependencies:
   pip install pytest pytest-cov pytest-mock

2. Run basic tests:
   python test_suite.py

3. Run with coverage:
   pytest --cov=. --cov-report=html

4. Run specific test categories:
   pytest -k "TestBusinessLogic"  # Only business logic tests
   pytest -m "not slow"           # Skip slow tests

5. Continuous integration setup:
   - Add to GitHub Actions
   - Run on every commit
   - Require tests to pass before merge
"""