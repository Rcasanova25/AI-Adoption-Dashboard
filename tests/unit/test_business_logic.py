import pytest
import pandas as pd
from unittest.mock import Mock, patch
from hypothesis import given, strategies as st

# Import your business logic modules
from business.metrics import BusinessMetrics, CompetitivePosition, InvestmentRecommendation

class TestCompetitivePositionAssessment:
    """Test competitive position assessment functionality"""
    
    def test_leader_position_assessment(self, sample_sector_data):
        """Test assessment for market leaders"""
        assessment = BusinessMetrics.assess_competitive_position(
            industry="Technology (92% adoption)",
            company_size="5000+ employees (58% adoption)",
            maturity="Leading (80%+)",
            urgency=5
        )
        
        # Assertions for leader position
        assert assessment.position == CompetitivePosition.LEADER
        assert assessment.score >= 80
        assert assessment.industry_benchmark == 92
        assert assessment.size_benchmark == 58
        assert len(assessment.recommendations) > 0
        assert "maintain" in assessment.gap_analysis.lower()
        
    def test_laggard_position_assessment(self):
        """Test assessment for lagging organizations"""
        assessment = BusinessMetrics.assess_competitive_position(
            industry="Government (52% adoption)",
            company_size="1-50 employees (3% adoption)",
            maturity="Exploring (0-10%)",
            urgency=9
        )
        
        # Assertions for laggard position
        assert assessment.position == CompetitivePosition.LAGGARD
        assert assessment.score < 30
        assert assessment.urgency_level == 9
        assert any("urgent" in rec.lower() for rec in assessment.recommendations)
        assert len(assessment.risk_factors) > 0
        
    def test_competitive_position_assessment(self):
        """Test assessment for competitive organizations"""
        assessment = BusinessMetrics.assess_competitive_position(
            industry="Healthcare (78% adoption)",
            company_size="1000-5000 employees (42% adoption)",
            maturity="Implementing (30-60%)",
            urgency=6
        )
        
        assert assessment.position == CompetitivePosition.COMPETITIVE
        assert 30 <= assessment.score < 70
        assert assessment.industry_benchmark == 78
        assert assessment.size_benchmark == 42
        
    @given(st.integers(min_value=1, max_value=10))
    def test_urgency_levels(self, urgency_level):
        """Property-based test for urgency levels"""
        assessment = BusinessMetrics.assess_competitive_position(
            industry="Technology (92% adoption)",
            company_size="251-1000 employees (25% adoption)",
            maturity="Piloting (10-30%)",
            urgency=urgency_level
        )
        
        assert assessment.urgency_level == urgency_level
        assert 0 <= assessment.score <= 100
        assert assessment.position in [CompetitivePosition.LEADER, 
                                     CompetitivePosition.COMPETITIVE, 
                                     CompetitivePosition.LAGGARD]
    
    def test_invalid_inputs(self):
        """Test error handling for invalid inputs"""
        with pytest.raises(ValueError):
            BusinessMetrics.assess_competitive_position(
                industry="Invalid Industry",
                company_size="Invalid Size",
                maturity="Invalid Maturity",
                urgency=11  # Invalid urgency > 10
            )

class TestInvestmentCaseCalculation:
    """Test investment case calculation functionality"""
    
    def test_basic_investment_calculation(self):
        """Test basic investment case calculation"""
        case = BusinessMetrics.calculate_investment_case(
            investment_amount=500000,
            timeline_months=12,
            industry="Technology",
            goal="Operational Efficiency",
            risk_tolerance="Medium"
        )
        
        # Basic financial validation
        assert case.investment_amount == 500000
        assert case.timeline_months == 12
        assert case.expected_roi > 0
        assert case.total_return > case.investment_amount
        assert case.net_benefit == case.total_return - case.investment_amount
        assert case.payback_months > 0
        assert case.monthly_benefit > 0
        
    def test_high_roi_industry_calculation(self):
        """Test calculation for high-ROI industries"""
        case = BusinessMetrics.calculate_investment_case(
            investment_amount=1000000,
            timeline_months=18,
            industry="Technology",
            goal="Revenue Growth",
            risk_tolerance="High"
        )
        
        # Technology should have higher ROI
        assert case.expected_roi >= 3.5
        assert case.recommendation in [InvestmentRecommendation.APPROVE, 
                                     InvestmentRecommendation.CONDITIONAL]
        assert case.confidence_level in ["Medium", "High"]
        
    def test_low_roi_scenario(self):
        """Test calculation for challenging scenarios"""
        case = BusinessMetrics.calculate_investment_case(
            investment_amount=5000000,
            timeline_months=6,  # Very short timeline
            industry="Government",
            goal="Innovation & New Products",
            risk_tolerance="Low"
        )
        
        # Should be more conservative
        assert case.expected_roi <= 3.0
        assert case.recommendation in [InvestmentRecommendation.CONDITIONAL, 
                                     InvestmentRecommendation.REJECT]
        
    @pytest.mark.parametrize("amount,timeline,expected_payback", [
        (100000, 12, lambda x: x <= 12),
        (500000, 18, lambda x: x <= 24),
        (1000000, 24, lambda x: x <= 36),
    ])
    def test_payback_period_calculations(self, amount, timeline, expected_payback):
        """Test payback period calculations"""
        case = BusinessMetrics.calculate_investment_case(
            investment_amount=amount,
            timeline_months=timeline,
            industry="Technology",
            goal="Cost Reduction",
            risk_tolerance="Medium"
        )
        
        assert expected_payback(case.payback_months)
        
    def test_roi_consistency_across_goals(self):
        """Test ROI consistency across different goals"""
        goals = ["Operational Efficiency", "Revenue Growth", "Cost Reduction", 
                "Innovation & New Products", "Risk Management", "Customer Experience"]
        
        roi_results = []
        for goal in goals:
            case = BusinessMetrics.calculate_investment_case(
                investment_amount=500000,
                timeline_months=12,
                industry="Financial Services",
                goal=goal,
                risk_tolerance="Medium"
            )
            roi_results.append(case.expected_roi)
        
        # ROI should be within reasonable range for all goals
        assert all(1.5 <= roi <= 5.0 for roi in roi_results)
        
        # Revenue Growth should generally have higher ROI than Cost Reduction
        revenue_roi = roi_results[goals.index("Revenue Growth")]
        cost_roi = roi_results[goals.index("Cost Reduction")]
        assert revenue_roi >= cost_roi * 0.9  # Allow some variance

class TestDataValidationUtilities:
    """Test data validation utility functions"""
    
    def test_safe_data_check_valid_data(self, sample_historical_data):
        """Test safe data check with valid data"""
        from Utils.helpers import safe_data_check
        
        result = safe_data_check(sample_historical_data, "test_data")
        assert result == True
        
    def test_safe_data_check_empty_data(self, empty_dataframe):
        """Test safe data check with empty data"""
        from Utils.helpers import safe_data_check
        
        with patch('streamlit.error') as mock_error:
            result = safe_data_check(empty_dataframe, "test_data")
            assert result == False
            mock_error.assert_called()
            
    def test_safe_data_check_none_data(self):
        """Test safe data check with None data"""
        from Utils.helpers import safe_data_check
        
        with patch('streamlit.error') as mock_error:
            result = safe_data_check(None, "test_data")
            assert result == False
            mock_error.assert_called()

class TestMetricsCalculation:
    """Test dynamic metrics calculation"""
    
    def test_get_dynamic_metrics_complete_data(self, sample_historical_data, 
                                             sample_investment_data, sample_sector_data):
        """Test metrics calculation with complete data"""
        from app import get_dynamic_metrics
        
        # Mock cost reduction data
        cost_data = pd.DataFrame({
            'cost_per_million_tokens': [20.0, 0.07],
            'year': [2022, 2024]
        })
        
        metrics = get_dynamic_metrics(
            sample_historical_data, 
            cost_data, 
            sample_investment_data, 
            sample_sector_data
        )
        
        # Validate all required metrics are present
        required_metrics = ['market_adoption', 'market_delta', 'genai_adoption', 
                          'genai_delta', 'cost_reduction', 'cost_period',
                          'investment_value', 'investment_delta', 'avg_roi', 'roi_desc']
        
        for metric in required_metrics:
            assert metric in metrics
            assert metrics[metric] is not None
            
        # Validate specific calculations
        assert metrics['market_adoption'] == "82.1%"  # Latest year from sample data
        assert "pp" in metrics['market_delta']  # Should contain percentage points
        
    def test_get_dynamic_metrics_missing_data(self):
        """Test metrics calculation with missing data (fallback)"""
        from app import get_dynamic_metrics
        
        metrics = get_dynamic_metrics(None, None, None, None)
        
        # Should return fallback values, not crash
        assert 'market_adoption' in metrics
        assert 'cost_reduction' in metrics
        assert metrics['market_adoption'] == "78%"  # Fallback value
        assert metrics['cost_reduction'] == "280x cheaper"  # Fallback value
        
    def test_metrics_calculation_edge_cases(self):
        """Test metrics calculation with edge case data"""
        from app import get_dynamic_metrics
        
        # Single row data
        minimal_historical = pd.DataFrame({
            'year': [2024],
            'ai_use': [50],
            'genai_use': [40]
        })
        
        metrics = get_dynamic_metrics(minimal_historical, None, None, None)
        
        # Should handle gracefully
        assert 'market_adoption' in metrics
        assert metrics['market_adoption'] == "50%"

class TestHelperFunctions:
    """Test utility helper functions"""
    
    @pytest.mark.parametrize("input_text,expected_output", [
        ("🎯 Competitive Position Assessor", "competitive_position_assessor"),
        ("💰 Investment Decision Engine", "investment_decision_engine"),
        ("Simple Name", "simple_name"),
        ("Name with Spaces & Special!@#", "name_with_spaces_special"),
        ("Multiple___Underscores", "multiple_underscores"),
        ("", ""),
        ("123 Numbers", "123_numbers"),
    ])
    def test_clean_filename(self, input_text, expected_output):
        """Test filename cleaning function"""
        from Utils.helpers import clean_filename
        
        result = clean_filename(input_text)
        assert result == expected_output
        
        # Ensure result is safe for all operating systems
        unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        assert not any(char in result for char in unsafe_chars)
        
    def test_safe_execute_success(self):
        """Test safe execution with successful function"""
        from Utils.helpers import safe_execute
        
        def successful_function():
            return "success"
        
        result = safe_execute(successful_function, "default", "error message")
        assert result == "success"
        
    def test_safe_execute_failure(self):
        """Test safe execution with failing function"""
        from Utils.helpers import safe_execute
        
        def failing_function():
            raise ValueError("Test error")
        
        with patch('streamlit.error') as mock_error:
            result = safe_execute(failing_function, "default", "error message")
            assert result == "default"
            mock_error.assert_called()
            
    @patch('time.time')
    def test_monitor_performance(self, mock_time):
        """Test performance monitoring decorator"""
        from Utils.helpers import monitor_performance
        
        # Mock time to return specific values
        mock_time.side_effect = [0, 1.5]  # 1.5 second execution time
        
        @monitor_performance
        def test_function():
            return "result"
        
        result = test_function()
        assert result == "result"
        
        # Verify time.time() was called twice (start and end)
        assert mock_time.call_count == 2

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_fallback_data_creation(self):
        """Test fallback data creation doesn't crash"""
        from app import _create_fallback_data
        
        # Should not raise any exceptions
        try:
            _create_fallback_data()
        except Exception as e:
            pytest.fail(f"Fallback data creation failed: {e}")
            
    def test_validation_with_corrupted_data(self, invalid_dataframe):
        """Test validation with corrupted/invalid data"""
        from data.models import safe_validate_data
        
        result = safe_validate_data(invalid_dataframe, "test_data")
        
        # Should handle gracefully
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')
        
        if not result.is_valid:
            assert len(result.errors) > 0
            
    def test_chart_validation_edge_cases(self):
        """Test chart data validation with edge cases"""
        from app import validate_chart_data
        
        # Test with None data
        is_valid, message = validate_chart_data(None, ['col1', 'col2'])
        assert not is_valid
        assert "None" in message
        
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        is_valid, message = validate_chart_data(empty_df, ['col1', 'col2'])
        assert not is_valid
        assert "empty" in message.lower()
        
        # Test with missing columns
        df_missing_cols = pd.DataFrame({'col1': [1, 2, 3]})
        is_valid, message = validate_chart_data(df_missing_cols, ['col1', 'col2'])
        assert not is_valid
        assert "Missing columns" in message

# Run specific unit tests
if __name__ == "__main__":
    pytest.main(["-v", "tests/unit/test_business_logic.py"]) 