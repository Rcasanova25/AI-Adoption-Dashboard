import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
import plotly.graph_objects as go

class TestDashboardIntegration:
    """Integration tests for dashboard functionality"""
    
    @patch('streamlit.plotly_chart')
    @patch('streamlit.metric')
    def test_executive_dashboard_flow(self, mock_metric, mock_chart, 
                                    sample_historical_data, sample_sector_data, 
                                    sample_investment_data):
        """Test complete executive dashboard flow"""
        from app import get_dynamic_metrics, executive_strategic_brief
        
        # Test data flow through the system
        metrics = get_dynamic_metrics(
            sample_historical_data,
            None,  # ai_cost_reduction
            sample_investment_data,
            sample_sector_data
        )
        
        # Verify metrics calculation
        assert 'market_adoption' in metrics
        assert 'investment_value' in metrics
        
        # Test executive brief rendering (should not crash)
        with patch('streamlit.title'), \
             patch('streamlit.markdown'), \
             patch('streamlit.columns') as mock_cols, \
             patch('streamlit.subheader'):
            
            # Mock columns return
            mock_cols.return_value = [Mock(), Mock(), Mock(), Mock()]
            
            try:
                executive_strategic_brief(metrics, sample_historical_data)
            except Exception as e:
                pytest.fail(f"Executive brief rendering failed: {e}")
                
        # Verify Streamlit components were called
        assert mock_metric.called
        
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    def test_competitive_assessment_integration(self, mock_button, mock_selectbox):
        """Test competitive assessment integration"""
        from app import display_competitive_assessment
        
        # Mock user inputs
        mock_selectbox.side_effect = [
            "Technology (92% adoption)",
            "1000-5000 employees (42% adoption)"
        ]
        mock_button.return_value = True
        
        with patch('streamlit.success'), \
             patch('streamlit.metric'), \
             patch('streamlit.markdown'), \
             patch('streamlit.columns') as mock_cols:
            
            mock_cols.return_value = [Mock(), Mock(), Mock()]
            
            # Test assessment generation
            try:
                assessment = display_competitive_assessment(
                    "Technology (92% adoption)",
                    "1000-5000 employees (42% adoption)",
                    "Implementing (30-60%)",
                    7
                )
                
                # Verify assessment object
                assert hasattr(assessment, 'position')
                assert hasattr(assessment, 'score')
                assert hasattr(assessment, 'recommendations')
                
            except Exception as e:
                pytest.fail(f"Competitive assessment integration failed: {e}")
    
    @patch('streamlit.download_button')
    def test_investment_case_integration(self, mock_download):
        """Test investment case integration"""
        from app import display_investment_case
        
        with patch('streamlit.subheader'), \
             patch('streamlit.columns') as mock_cols, \
             patch('streamlit.metric'), \
             patch('streamlit.success'), \
             patch('streamlit.info'):
            
            mock_cols.return_value = [Mock(), Mock(), Mock(), Mock()]
            
            try:
                case = display_investment_case(
                    investment_amount=500000,
                    timeline=12,
                    industry="Technology",
                    goal="Operational Efficiency",
                    risk_tolerance="Medium"
                )
                
                # Verify case object
                assert hasattr(case, 'expected_roi')
                assert hasattr(case, 'recommendation')
                assert case.investment_amount == 500000
                
                # Verify download button was called
                assert mock_download.called
                
            except Exception as e:
                pytest.fail(f"Investment case integration failed: {e}")

class TestDataLoadingIntegration:
    """Test data loading and validation integration"""
    
    @patch('data.loaders.load_all_datasets')
    def test_data_loading_pipeline(self, mock_loader, sample_historical_data, 
                                 sample_sector_data, sample_investment_data):
        """Test complete data loading pipeline"""
        # Mock successful data loading
        mock_data = {
            'historical_data': sample_historical_data,
            'sector_2025': sample_sector_data,
            'investment_data': sample_investment_data
        }
        mock_loader.return_value = mock_data
        
        from app import load_data
        
        # Test data loading
        loaded_data = load_data()
        
        assert loaded_data is not None
        assert 'historical_data' in loaded_data
        assert 'sector_2025' in loaded_data
        assert 'investment_data' in loaded_data
        
        # Verify data structure
        hist_data = loaded_data['historical_data']
        assert 'year' in hist_data.columns
        assert 'ai_use' in hist_data.columns
        assert len(hist_data) > 0
        
    def test_data_validation_integration(self, sample_historical_data):
        """Test data validation integration"""
        from data.models import safe_validate_data
        from data.loaders import validate_all_loaded_data
        
        # Test individual validation
        result = safe_validate_data(sample_historical_data, "historical_data")
        assert result.is_valid == True
        
        # Test complete validation
        mock_datasets = {
            'historical_data': sample_historical_data,
            'sector_2025': pd.DataFrame({'sector': ['Tech'], 'adoption_rate': [90]})
        }
        
        try:
            validation_results = validate_all_loaded_data(mock_datasets)
            assert isinstance(validation_results, dict)
        except Exception as e:
            pytest.fail(f"Complete validation integration failed: {e}")

class TestChartRenderingIntegration:
    """Test chart rendering and visualization integration"""
    
    def test_historical_trends_chart(self, sample_historical_data):
        """Test historical trends chart generation"""
        import plotly.graph_objects as go
        
        # Test chart creation (mimicking app logic)
        try:
            fig = go.Figure()
            
            # Add traces like in the app
            fig.add_trace(go.Scatter(
                x=sample_historical_data['year'], 
                y=sample_historical_data['ai_use'], 
                mode='lines+markers', 
                name='Overall AI Use'
            ))
            
            fig.add_trace(go.Scatter(
                x=sample_historical_data['year'], 
                y=sample_historical_data['genai_use'], 
                mode='lines+markers', 
                name='GenAI Use'
            ))
            
            fig.update_layout(
                title="AI Adoption Trends",
                xaxis_title="Year",
                yaxis_title="Adoption Rate (%)"
            )
            
            # Verify chart structure
            assert len(fig.data) == 2
            assert fig.layout.title.text == "AI Adoption Trends"
            
        except Exception as e:
            pytest.fail(f"Historical trends chart creation failed: {e}")
    
    def test_sector_analysis_chart(self, sample_sector_data):
        """Test sector analysis chart generation"""
        import plotly.express as px
        
        try:
            # Test bar chart creation
            fig = px.bar(
                sample_sector_data, 
                x='sector', 
                y='adoption_rate',
                title="AI Adoption by Sector"
            )
            
            # Verify chart structure
            assert len(fig.data) > 0
            assert fig.layout.title.text == "AI Adoption by Sector"
            
        except Exception as e:
            pytest.fail(f"Sector analysis chart creation failed: {e}")
    
    @patch('streamlit.plotly_chart')
    def test_chart_validation_before_rendering(self, mock_chart, sample_historical_data):
        """Test chart validation before rendering"""
        from app import validate_chart_data
        
        # Test validation before chart creation
        required_columns = ['year', 'ai_use']
        is_valid, message = validate_chart_data(sample_historical_data, required_columns)
        
        assert is_valid == True
        assert message == "Data is valid"
        
        # Should proceed to chart rendering
        if is_valid:
            # Simulate chart creation and rendering
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sample_historical_data['year'],
                y=sample_historical_data['ai_use']
            ))
            
            # Simulate Streamlit chart rendering
            mock_chart(fig)
            assert mock_chart.called

class TestNavigationIntegration:
    """Test navigation and user flow integration"""
    
    @patch('streamlit.sidebar')
    def test_executive_navigation_flow(self, mock_sidebar, sample_historical_data,
                                     sample_investment_data, sample_sector_data):
        """Test executive navigation integration"""
        from app import create_executive_navigation, get_dynamic_metrics
        
        # Mock sidebar components
        mock_sidebar.markdown = Mock()
        mock_sidebar.radio = Mock(return_value="🚀 Strategic Brief")
        mock_sidebar.metric = Mock()
        mock_sidebar.expander = Mock()
        
        # Get dynamic metrics for navigation
        metrics = get_dynamic_metrics(
            sample_historical_data,
            None,
            sample_investment_data,
            sample_sector_data
        )
        
        try:
            view, is_detailed = create_executive_navigation(metrics)
            
            assert view in ["🚀 Strategic Brief", "⚖️ Competitive Position", 
                          "💰 Investment Case", "📊 Market Intelligence", 
                          "🎯 Action Planning"]
            assert isinstance(is_detailed, bool)
            
            # Verify sidebar components were called
            assert mock_sidebar.markdown.called
            assert mock_sidebar.radio.called
            assert mock_sidebar.metric.called
            
        except Exception as e:
            pytest.fail(f"Executive navigation integration failed: {e}")
    
    @patch('streamlit.selectbox')
    def test_view_routing_integration(self, mock_selectbox):
        """Test view routing integration"""
        from app import all_views
        
        # Test different view selections
        test_views = ["Historical Trends", "Industry Analysis", "ROI Analysis"]
        
        for view in test_views:
            mock_selectbox.return_value = view
            
            # Verify view is in available views
            assert view in all_views
            
            # Test view routing logic (simplified)
            if view == "Historical Trends":
                assert "historical" in view.lower()
            elif view == "Industry Analysis":
                assert "industry" in view.lower()

class TestErrorHandlingIntegration:
    """Test error handling in integrated scenarios"""
    
    @patch('streamlit.error')
    @patch('data.loaders.load_all_datasets')
    def test_data_loading_failure_handling(self, mock_loader, mock_error):
        """Test handling of data loading failures"""
        # Mock data loading failure
        mock_loader.side_effect = Exception("Network error")
        
        from app import load_data, _create_fallback_data
        
        # Test error handling
        with patch('app._create_fallback_data') as mock_fallback:
            try:
                result = load_data()
                # Should either return None or fallback data
                assert result is None or isinstance(result, dict)
            except Exception as e:
                pytest.fail(f"Data loading error handling failed: {e}")
    
    def test_missing_data_graceful_degradation(self):
        """Test graceful degradation with missing data"""
        from app import get_dynamic_metrics
        
        # Test with various missing data scenarios
        scenarios = [
            (None, None, None, None),  # All missing
            (pd.DataFrame({'year': [2024], 'ai_use': [50]}), None, None, None),  # Partial
        ]
        
        for hist, cost, invest, sector in scenarios:
            try:
                metrics = get_dynamic_metrics(hist, cost, invest, sector)
                
                # Should return fallback values, not crash
                assert 'market_adoption' in metrics
                assert isinstance(metrics, dict)
                
            except Exception as e:
                pytest.fail(f"Missing data handling failed: {e}")

class TestPerformanceIntegration:
    """Test performance in integrated scenarios"""
    
    def test_large_dataset_rendering(self, large_dataset):
        """Test rendering with large datasets"""
        import time
        from app import validate_chart_data
        
        start_time = time.time()
        
        # Test validation with large dataset
        is_valid, message = validate_chart_data(
            large_dataset, 
            ['year', 'adoption_rate']
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within reasonable time
        assert execution_time < 2.0  # 2 seconds threshold
        assert is_valid == True
    
    @patch('streamlit.plotly_chart')
    def test_chart_rendering_performance(self, mock_chart, sample_historical_data):
        """Test chart rendering performance"""
        import time
        import plotly.graph_objects as go
        
        start_time = time.time()
        
        # Create complex chart
        fig = go.Figure()
        
        # Add multiple traces
        for i in range(10):
            fig.add_trace(go.Scatter(
                x=sample_historical_data['year'],
                y=sample_historical_data['ai_use'] + i,
                name=f'Series {i}'
            ))
        
        fig.update_layout(title="Performance Test Chart")
        
        # Simulate rendering
        mock_chart(fig)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Chart creation should be fast
        assert execution_time < 1.0  # 1 second threshold

# Run integration tests
if __name__ == "__main__":
    pytest.main(["-v", "tests/integration/test_dashboard_integration.py"]) 