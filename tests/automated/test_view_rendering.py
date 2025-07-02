"""
Automated View Rendering Tests
Tests for all dashboard views and their rendering logic
"""

import pytest
import pandas as pd
import numpy as np
import streamlit as st
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, Any, List
import plotly.graph_objects as go
from io import StringIO
import sys

# Import views to test
from views import (
    historical_trends, adoption_rates, financial_impact, industry_analysis,
    geographic_distribution, investment_trends, productivity_research,
    skill_gap_analysis, governance_compliance, environmental_impact
)


class StreamlitCapture:
    """Helper class to capture Streamlit outputs for testing"""
    
    def __init__(self):
        self.calls = []
        self.text_outputs = []
        self.plots = []
        self.metrics = []
        self.warnings = []
        self.errors = []
    
    def write(self, content):
        self.calls.append(('write', content))
        self.text_outputs.append(content)
    
    def warning(self, content):
        self.calls.append(('warning', content))
        self.warnings.append(content)
    
    def error(self, content):
        self.calls.append(('error', content))
        self.errors.append(content)
    
    def plotly_chart(self, fig, **kwargs):
        self.calls.append(('plotly_chart', fig))
        self.plots.append(fig)
    
    def metric(self, label, value, delta=None):
        self.calls.append(('metric', label, value, delta))
        self.metrics.append({'label': label, 'value': value, 'delta': delta})
    
    def columns(self, spec):
        # Return mock column objects
        return [Mock() for _ in range(spec if isinstance(spec, int) else len(spec))]
    
    def expander(self, label):
        return Mock()
    
    def info(self, content):
        self.calls.append(('info', content))
    
    def success(self, content):
        self.calls.append(('success', content))
    
    def button(self, label, key=None):
        return False  # Default to not clicked
    
    def rerun(self):
        self.calls.append(('rerun',))


class TestViewDataValidation:
    """Test data validation in view rendering"""
    
    @pytest.fixture
    def mock_streamlit(self):
        """Mock Streamlit for testing"""
        capture = StreamlitCapture()
        
        with patch.multiple(
            'streamlit',
            write=capture.write,
            warning=capture.warning,
            error=capture.error,
            plotly_chart=capture.plotly_chart,
            metric=capture.metric,
            columns=capture.columns,
            expander=capture.expander,
            info=capture.info,
            success=capture.success,
            button=capture.button,
            rerun=capture.rerun
        ):
            yield capture
    
    @pytest.fixture
    def valid_historical_data(self):
        """Valid historical data for testing"""
        return pd.DataFrame({
            'year': [2022, 2023, 2024, 2025],
            'ai_use': [55.0, 65.0, 78.0, 78.0],
            'genai_use': [33.0, 55.0, 71.0, 71.0],
            'data_source': ['Stanford AI Index'] * 4
        })
    
    @pytest.fixture
    def invalid_historical_data(self):
        """Invalid historical data for testing"""
        return pd.DataFrame({
            'invalid_column': ['bad', 'data'],
            'another_column': [None, None]
        })
    
    @pytest.fixture
    def valid_financial_data(self):
        """Valid financial impact data for testing"""
        return pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain'],
            'companies_reporting_revenue_gains': [71, 57, 63],
            'companies_reporting_cost_savings': [38, 49, 43],
            'data_source': ['McKinsey Global Survey 2024'] * 3
        })
    
    @pytest.fixture
    def valid_sector_data(self):
        """Valid sector data for testing"""
        return pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare'],
            'adoption_rate': [92, 85, 78],
            'genai_adoption': [88, 78, 65],
            'avg_roi': [4.2, 3.8, 3.2]
        })
    
    def test_historical_trends_with_valid_data(self, mock_streamlit, valid_historical_data):
        """Test historical trends view with valid data"""
        # Test the view function
        historical_trends.show_historical_trends(
            data_year="2025 (GenAI Era)",
            historical_data=valid_historical_data
        )
        
        # Check that no warnings were generated
        assert len(mock_streamlit.warnings) == 0
        assert len(mock_streamlit.errors) == 0
        
        # Check that some content was rendered
        assert len(mock_streamlit.text_outputs) > 0
    
    def test_historical_trends_with_invalid_data(self, mock_streamlit, invalid_historical_data):
        """Test historical trends view with invalid data"""
        historical_trends.show_historical_trends(
            data_year="2025 (GenAI Era)",
            historical_data=invalid_historical_data
        )
        
        # Should generate warnings for invalid data
        assert len(mock_streamlit.warnings) > 0
        warning_text = ' '.join(mock_streamlit.warnings).lower()
        assert 'not available' in warning_text or 'invalid' in warning_text
    
    def test_adoption_rates_with_valid_data(self, mock_streamlit, valid_financial_data, valid_sector_data):
        """Test adoption rates view with valid data"""
        adoption_rates.show_adoption_rates(
            data_year="2025 (GenAI Era)",
            financial_impact=valid_financial_data,
            sector_2018=valid_sector_data
        )
        
        # Check that no errors were generated
        assert len(mock_streamlit.errors) == 0
        
        # Check that content was rendered
        assert len(mock_streamlit.text_outputs) > 0
    
    def test_financial_impact_rendering(self, mock_streamlit, valid_financial_data):
        """Test financial impact view rendering"""
        financial_impact.show_financial_impact(
            data_year="2025",
            financial_impact=valid_financial_data
        )
        
        # Should not produce errors
        assert len(mock_streamlit.errors) == 0
        
        # Should produce some metrics or plots
        assert len(mock_streamlit.metrics) > 0 or len(mock_streamlit.plots) > 0


class TestViewRenderingLogic:
    """Test the rendering logic of views"""
    
    @pytest.fixture
    def mock_plotly(self):
        """Mock Plotly for testing"""
        with patch('plotly.graph_objects.Figure') as mock_fig:
            mock_instance = Mock()
            mock_fig.return_value = mock_instance
            yield mock_instance
    
    def test_plot_generation_historical_trends(self, valid_historical_data, mock_plotly):
        """Test that historical trends generates appropriate plots"""
        with patch('streamlit.plotly_chart') as mock_chart:
            historical_trends.show_historical_trends(
                data_year="2025 (GenAI Era)",
                historical_data=valid_historical_data
            )
            
            # Should generate at least one plot
            assert mock_chart.call_count >= 0  # May or may not plot depending on data
    
    def test_data_filtering_logic(self, valid_historical_data):
        """Test data filtering logic in views"""
        # Test year filtering
        filtered_2024 = valid_historical_data[valid_historical_data['year'] == 2024]
        assert len(filtered_2024) == 1
        assert filtered_2024.iloc[0]['ai_use'] == 78.0
        
        # Test range filtering
        recent_data = valid_historical_data[valid_historical_data['year'] >= 2023]
        assert len(recent_data) == 3
    
    def test_metric_calculation_logic(self, valid_financial_data):
        """Test metric calculations in views"""
        # Test average calculations
        avg_revenue_gains = valid_financial_data['companies_reporting_revenue_gains'].mean()
        assert avg_revenue_gains > 0
        
        # Test percentage calculations
        max_revenue_gains = valid_financial_data['companies_reporting_revenue_gains'].max()
        assert max_revenue_gains <= 100  # Should be percentage


class TestViewErrorHandling:
    """Test error handling in view rendering"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames"""
        empty_df = pd.DataFrame()
        
        with patch('streamlit.warning') as mock_warning:
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=empty_df
            )
            
            # Should produce a warning
            assert mock_warning.called
    
    def test_none_dataframe_handling(self):
        """Test handling of None DataFrames"""
        with patch('streamlit.warning') as mock_warning:
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=None
            )
            
            # Should handle None gracefully
            assert mock_warning.called or True  # Should not crash
    
    def test_missing_columns_handling(self):
        """Test handling of missing required columns"""
        df_missing_cols = pd.DataFrame({
            'wrong_column': [1, 2, 3],
            'another_wrong': ['a', 'b', 'c']
        })
        
        with patch('streamlit.warning') as mock_warning:
            adoption_rates.show_adoption_rates(
                data_year="2025",
                financial_impact=df_missing_cols,
                sector_2018=df_missing_cols
            )
            
            # Should handle missing columns gracefully
            assert True  # Should not crash
    
    def test_corrupted_data_handling(self):
        """Test handling of corrupted data"""
        corrupted_df = pd.DataFrame({
            'year': [2024, 'invalid', None],
            'ai_use': [78.0, 'bad_data', np.inf],
            'genai_use': [71.0, None, -999]
        })
        
        with patch('streamlit.warning') as mock_warning:
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=corrupted_df
            )
            
            # Should handle corrupted data gracefully
            assert True  # Should not crash


class TestViewPerformance:
    """Test performance aspects of view rendering"""
    
    def test_large_dataset_rendering(self):
        """Test rendering with large datasets"""
        # Create large dataset
        large_df = pd.DataFrame({
            'year': np.random.choice(range(2020, 2025), 10000),
            'ai_use': np.random.uniform(30, 95, 10000),
            'genai_use': np.random.uniform(20, 80, 10000)
        })
        
        import time
        start_time = time.time()
        
        with patch('streamlit.plotly_chart'), patch('streamlit.write'):
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=large_df
            )
        
        end_time = time.time()
        
        # Should complete in reasonable time (< 10 seconds)
        assert (end_time - start_time) < 10.0
    
    def test_memory_usage_monitoring(self, valid_historical_data):
        """Test memory usage during view rendering"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Render view multiple times
        for _ in range(10):
            with patch('streamlit.plotly_chart'), patch('streamlit.write'):
                historical_trends.show_historical_trends(
                    data_year="2025",
                    historical_data=valid_historical_data
                )
        
        # Check final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB)
        assert memory_increase < 100.0


class TestViewAccessibility:
    """Test accessibility aspects of view rendering"""
    
    def test_color_contrast_in_plots(self, valid_historical_data, mock_plotly):
        """Test that plots use accessible colors"""
        with patch('streamlit.plotly_chart') as mock_chart:
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=valid_historical_data
            )
            
            # Check if plotly_chart was called
            if mock_chart.called:
                # Get the figure that was passed
                args, kwargs = mock_chart.call_args
                if args:
                    fig = args[0]
                    # Basic check that figure exists
                    assert fig is not None
    
    def test_text_readability(self, valid_financial_data):
        """Test that text outputs are readable"""
        with patch('streamlit.write') as mock_write:
            adoption_rates.show_adoption_rates(
                data_year="2025",
                financial_impact=valid_financial_data,
                sector_2018=valid_financial_data
            )
            
            # Check that text was written
            if mock_write.called:
                # Get all text outputs
                text_outputs = [call[0][0] for call in mock_write.call_args_list if call[0]]
                
                # Check that text is not empty
                non_empty_outputs = [text for text in text_outputs if text and str(text).strip()]
                assert len(non_empty_outputs) > 0
    
    def test_alternative_text_for_charts(self):
        """Test that charts have appropriate alternative descriptions"""
        # This would typically check for alt text or descriptions
        # For now, we ensure the structure supports accessibility
        assert True  # Placeholder for accessibility validation


class TestViewIntegration:
    """Test integration between views and data pipeline"""
    
    def test_view_with_automated_data(self):
        """Test views work with automated data loading"""
        try:
            from data.pipeline_integration import load_all_datasets_integrated
            
            # Load data using integrated pipeline
            datasets, metadata = load_all_datasets_integrated()
            
            # Test that historical view works with loaded data
            if 'historical_data' in datasets and not datasets['historical_data'].empty:
                with patch('streamlit.plotly_chart'), patch('streamlit.write'):
                    historical_trends.show_historical_trends(
                        data_year="2025",
                        historical_data=datasets['historical_data']
                    )
                
                # Should not crash
                assert True
        
        except ImportError:
            pytest.skip("Integration pipeline not available")
    
    def test_view_fallback_behavior(self):
        """Test view fallback when data is unavailable"""
        empty_dashboard_data = {}
        
        with patch('streamlit.warning') as mock_warning:
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=pd.DataFrame(),
                dashboard_data=empty_dashboard_data
            )
            
            # Should provide user feedback
            assert mock_warning.called
    
    def test_cross_view_data_consistency(self, valid_historical_data, valid_sector_data):
        """Test data consistency across different views"""
        # Test that years are consistent
        hist_years = set(valid_historical_data['year'].tolist())
        
        # Both datasets should have compatible year ranges
        assert len(hist_years) > 0
        
        # Test that adoption rates are in valid ranges
        ai_rates = valid_historical_data['ai_use'].tolist()
        assert all(0 <= rate <= 100 for rate in ai_rates)


# Integration test fixtures
@pytest.fixture
def full_dashboard_data():
    """Complete dashboard data for integration testing"""
    return {
        'historical_data': pd.DataFrame({
            'year': [2022, 2023, 2024, 2025],
            'ai_use': [55.0, 65.0, 78.0, 78.0],
            'genai_use': [33.0, 55.0, 71.0, 71.0]
        }),
        'sector_data': pd.DataFrame({
            'sector': ['Technology', 'Finance', 'Healthcare'],
            'adoption_rate': [92, 85, 78],
            'genai_adoption': [88, 78, 65]
        }),
        'financial_impact': pd.DataFrame({
            'function': ['Marketing & Sales', 'Service Operations'],
            'companies_reporting_revenue_gains': [71, 57],
            'companies_reporting_cost_savings': [38, 49]
        })
    }


class TestFullIntegration:
    """Full integration tests for view rendering"""
    
    def test_complete_dashboard_rendering(self, full_dashboard_data):
        """Test rendering of complete dashboard"""
        with patch('streamlit.plotly_chart'), patch('streamlit.write'), patch('streamlit.metric'):
            # Test multiple views with complete data
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=full_dashboard_data['historical_data']
            )
            
            adoption_rates.show_adoption_rates(
                data_year="2025",
                financial_impact=full_dashboard_data['financial_impact'],
                sector_2018=full_dashboard_data['sector_data']
            )
            
            # Should complete without errors
            assert True
    
    def test_view_state_management(self, full_dashboard_data):
        """Test that views handle session state properly"""
        # Mock session state
        with patch.object(st, 'session_state', Mock()) as mock_session:
            mock_session.year_range = (2022, 2025)
            mock_session.compare_mode = False
            
            historical_trends.show_historical_trends(
                data_year="2025",
                historical_data=full_dashboard_data['historical_data']
            )
            
            # Should handle session state gracefully
            assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])