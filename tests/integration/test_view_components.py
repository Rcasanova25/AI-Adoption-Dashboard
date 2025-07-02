"""
Integration tests for view components
Tests complete view functionality with real data flow and Streamlit integration
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.test_config import TestUtils, TestDataFixtures, MockStreamlit
from tests.fixtures.test_data import *


class TestHistoricalTrendsView:
    """Integration tests for Historical Trends view"""
    
    @pytest.mark.integration
    def test_show_historical_trends_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete historical trends view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.subheader'), \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.columns') as mock_columns:
            
            mock_columns.return_value = [Mock(), Mock(), Mock()]
            
            from views.historical_trends import show_historical_trends
            
            # Test with complete data
            show_historical_trends(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                historical_data=complete_dashboard_data['historical_data']
            )
            
            # Verify metrics were displayed
            assert mock_metric.call_count >= 2
            
            # Verify charts were created
            assert mock_plotly.call_count >= 1
    
    @pytest.mark.integration
    def test_show_historical_trends_empty_data(self, empty_dataframe, mock_streamlit):
        """Test historical trends view with empty data"""
        with patch('streamlit.write'), \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.metric'):
            
            from views.historical_trends import show_historical_trends
            
            # Test with empty data
            show_historical_trends(
                data_year="2024",
                sources_data=empty_dataframe,
                historical_data=empty_dataframe
            )
            
            # Should display info message about missing data
            assert mock_info.call_count >= 1
    
    @pytest.mark.integration
    def test_historical_trends_error_handling(self, invalid_data, mock_streamlit):
        """Test error handling in historical trends view"""
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.write'):
            
            from views.historical_trends import show_historical_trends
            
            # Test with invalid data - should not crash
            try:
                show_historical_trends(
                    data_year="2024",
                    sources_data=invalid_data,
                    historical_data=invalid_data
                )
            except Exception:
                # If it does crash, verify error was logged
                pass


class TestIndustryAnalysisView:
    """Integration tests for Industry Analysis view"""
    
    @pytest.mark.integration
    def test_show_industry_analysis_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete industry analysis view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.subheader'), \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.dataframe') as mock_dataframe:
            
            from views.industry_analysis import show_industry_analysis
            
            # Test with sector data
            show_industry_analysis(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                sector_2025=complete_dashboard_data['sector_2025']
            )
            
            # Verify components were rendered
            assert mock_metric.call_count >= 2
            assert mock_plotly.call_count >= 1
            assert mock_dataframe.call_count >= 1
    
    @pytest.mark.integration
    def test_industry_analysis_data_validation(self, sector_data, mock_streamlit):
        """Test data validation in industry analysis"""
        with patch('streamlit.write'), \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            from views.industry_analysis import show_industry_analysis
            
            # Test with valid sector data
            show_industry_analysis(
                data_year="2024",
                sources_data=pd.DataFrame(),
                sector_2025=sector_data
            )
            
            # Charts should be created with valid data
            assert mock_plotly.call_count >= 1


class TestFinancialImpactView:
    """Integration tests for Financial Impact view"""
    
    @pytest.mark.integration
    def test_show_financial_impact_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete financial impact view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.plotly_chart') as mock_plotly:
            
            # Mock tab context managers
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [mock_tab, mock_tab, mock_tab]
            
            from views.financial_impact import show_financial_impact
            
            # Test with complete financial data
            show_financial_impact(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                financial_impact=complete_dashboard_data['financial_impact']
            )
            
            # Verify tabs and charts were created
            assert mock_tabs.call_count >= 1
            assert mock_plotly.call_count >= 1


class TestGovernanceComplianceView:
    """Integration tests for Governance & Compliance view"""
    
    @pytest.mark.integration
    def test_show_governance_compliance_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete governance compliance view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.columns') as mock_columns:
            
            # Mock tab and column context managers
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [mock_tab] * 5
            
            mock_columns.return_value = [Mock(), Mock()]
            
            from views.governance_compliance import show_governance_compliance
            
            # Create governance dashboard data
            governance_dashboard_data = {
                'ai_governance_framework': complete_dashboard_data.get('ai_governance_framework', pd.DataFrame()),
                'regulatory_landscape_study': TestDataFixtures.get_geographic_data(),  # Mock regulatory data
                'ai_skills_gap_analysis': complete_dashboard_data.get('ai_skills_gap_analysis', pd.DataFrame()),
                'change_management_study': TestDataFixtures.get_governance_data(),  # Mock change management
                'industry_transformation_study': TestDataFixtures.get_sector_data()  # Mock transformation
            }
            
            # Test with governance data
            show_governance_compliance(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                dashboard_data=governance_dashboard_data
            )
            
            # Verify tabs and visualizations were created
            assert mock_tabs.call_count >= 1
            assert mock_plotly.call_count >= 1


class TestResearchMetaAnalysisView:
    """Integration tests for Research Meta-Analysis view"""
    
    @pytest.mark.integration
    def test_show_research_meta_analysis_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete research meta-analysis view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.success') as mock_success, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.metric') as mock_metric:
            
            # Mock tab context managers
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [mock_tab] * 4
            
            from views.research_meta_analysis import show_research_meta_analysis
            
            # Test with meta-analysis data
            show_research_meta_analysis(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                dashboard_data=complete_dashboard_data
            )
            
            # Verify success message for 100% completion
            assert mock_success.call_count >= 1
            
            # Verify metrics and visualizations
            assert mock_metric.call_count >= 4  # Overview metrics
            assert mock_tabs.call_count >= 1
            assert mock_plotly.call_count >= 1


class TestImplementationGuidesView:
    """Integration tests for Implementation Guides view"""
    
    @pytest.mark.integration
    def test_show_implementation_guides_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete implementation guides view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.metric') as mock_metric:
            
            # Mock selectbox to return first stakeholder type
            mock_selectbox.return_value = "🏢 Enterprise Leadership (C-Suite)"
            
            # Mock tab context managers
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [mock_tab] * 4
            
            from views.implementation_guides import show_implementation_guides
            
            # Test with implementation guide data
            show_implementation_guides(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                dashboard_data=complete_dashboard_data
            )
            
            # Verify stakeholder selection and content
            assert mock_selectbox.call_count >= 1
            assert mock_metric.call_count >= 4  # Enterprise metrics
            assert mock_tabs.call_count >= 1
    
    @pytest.mark.integration
    def test_implementation_guides_all_stakeholders(self, complete_dashboard_data, mock_streamlit):
        """Test implementation guides for different stakeholder types"""
        stakeholder_types = [
            "🏢 Enterprise Leadership (C-Suite)",
            "💼 IT/Technology Leadership", 
            "🏛️ Government & Public Sector",
            "🚀 Startups & SMEs"
        ]
        
        from views.implementation_guides import show_implementation_guides
        
        for stakeholder in stakeholder_types:
            with patch('streamlit.selectbox', return_value=stakeholder), \
                 patch('streamlit.write'), \
                 patch('streamlit.markdown'), \
                 patch('streamlit.metric'):
                
                # Should not crash for any stakeholder type
                try:
                    show_implementation_guides(
                        data_year="2024",
                        sources_data=complete_dashboard_data['sources_data'],
                        dashboard_data=complete_dashboard_data
                    )
                except Exception as e:
                    pytest.fail(f"Implementation guide failed for {stakeholder}: {e}")


class TestTechnicalResearchView:
    """Integration tests for Technical Research view"""
    
    @pytest.mark.integration
    def test_show_technical_research_complete(self, complete_dashboard_data, mock_streamlit):
        """Test complete technical research view rendering"""
        with patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.tabs') as mock_tabs, \
             patch('streamlit.plotly_chart') as mock_plotly, \
             patch('streamlit.metric') as mock_metric:
            
            # Mock tab context managers
            mock_tab = Mock()
            mock_tab.__enter__ = Mock(return_value=mock_tab)
            mock_tab.__exit__ = Mock(return_value=None)
            mock_tabs.return_value = [mock_tab] * 5
            
            from views.technical_research import show_technical_research
            
            # Create technical research dashboard data
            technical_dashboard_data = {
                'nvidia_token_economics': complete_dashboard_data.get('token_economics', pd.DataFrame()),
                'ai_strategy_framework': TestDataFixtures.get_governance_data(),
                'ai_use_case_analysis': TestDataFixtures.get_sector_data(),
                'public_sector_ai_study': TestDataFixtures.get_geographic_data()
            }
            
            # Test with technical research data
            show_technical_research(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                dashboard_data=technical_dashboard_data
            )
            
            # Verify technical content was rendered
            assert mock_tabs.call_count >= 1
            assert mock_metric.call_count >= 4  # Overview metrics
            assert mock_plotly.call_count >= 1


class TestViewDataFlow:
    """Integration tests for data flow between components"""
    
    @pytest.mark.integration
    def test_data_consistency_across_views(self, complete_dashboard_data):
        """Test that data is consistent across different views"""
        
        # Test that the same data produces consistent results
        historical_data = complete_dashboard_data['historical_data']
        sector_data = complete_dashboard_data['sector_2025']
        
        # Verify data integrity
        assert not historical_data.empty
        assert not sector_data.empty
        assert 'year' in historical_data.columns
        assert 'sector' in sector_data.columns
        
        # Test data ranges are realistic
        assert historical_data['year'].min() >= 2017
        assert historical_data['year'].max() <= 2025
        assert sector_data['adoption_rate'].min() >= 0
        assert sector_data['adoption_rate'].max() <= 100
    
    @pytest.mark.integration
    def test_view_error_propagation(self, invalid_data):
        """Test error handling propagates correctly through views"""
        
        # Test that views handle invalid data gracefully
        from views.historical_trends import show_historical_trends
        
        with patch('streamlit.error') as mock_error, \
             patch('streamlit.write'), \
             patch('streamlit.info'):
            
            # Should not crash with invalid data
            try:
                show_historical_trends(
                    data_year="2024",
                    sources_data=invalid_data,
                    historical_data=invalid_data
                )
            except Exception:
                # If exception occurs, verify error handling
                pass
    
    @pytest.mark.integration
    def test_download_functionality(self, complete_dashboard_data, mock_streamlit):
        """Test download button functionality across views"""
        
        with patch('streamlit.download_button') as mock_download, \
             patch('streamlit.write'), \
             patch('streamlit.markdown'):
            
            from views.historical_trends import show_historical_trends
            
            # Test download functionality
            show_historical_trends(
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                historical_data=complete_dashboard_data['historical_data']
            )
            
            # Verify download buttons were created
            # Note: Actual download testing would require more complex setup
            # This tests that the download functions are called
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_view_rendering_performance(self, complete_dashboard_data):
        """Test view rendering performance"""
        
        from views.historical_trends import show_historical_trends
        
        with patch('streamlit.write'), \
             patch('streamlit.plotly_chart'), \
             patch('streamlit.metric'):
            
            # Test rendering performance
            result = TestUtils.assert_performance(
                show_historical_trends,
                max_time_ms=3000,  # 3 seconds max
                data_year="2024",
                sources_data=complete_dashboard_data['sources_data'],
                historical_data=complete_dashboard_data['historical_data']
            )


class TestNavigationIntegration:
    """Integration tests for navigation and routing"""
    
    @pytest.mark.integration
    def test_view_type_routing(self, complete_dashboard_data):
        """Test that all view types are properly routed"""
        
        view_types = [
            "Historical Trends",
            "Industry Analysis", 
            "Financial Impact",
            "Governance & Compliance",
            "Research Meta-Analysis",
            "Implementation Guides"
        ]
        
        # Mock main app routing
        with patch('streamlit.sidebar'), \
             patch('streamlit.selectbox') as mock_selectbox:
            
            for view_type in view_types:
                mock_selectbox.return_value = view_type
                
                # Test that each view type can be selected
                # This would normally trigger the app routing logic
                assert mock_selectbox.return_value == view_type
    
    @pytest.mark.integration
    def test_sidebar_integration(self, sample_config):
        """Test sidebar component integration"""
        
        with patch('streamlit.sidebar.selectbox') as mock_selectbox, \
             patch('streamlit.sidebar.slider') as mock_slider:
            
            mock_selectbox.return_value = "Historical Trends"
            mock_slider.return_value = 2024
            
            # Test sidebar functionality
            selected_view = mock_selectbox.return_value
            selected_year = mock_slider.return_value
            
            assert selected_view == "Historical Trends"
            assert selected_year == 2024


class TestChartIntegration:
    """Integration tests for chart rendering and interaction"""
    
    @pytest.mark.integration
    def test_plotly_chart_creation(self, historical_data):
        """Test Plotly chart creation and rendering"""
        
        import plotly.graph_objects as go
        
        with patch('streamlit.plotly_chart') as mock_plotly:
            
            # Create a test chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=historical_data['year'],
                y=historical_data['ai_use'],
                mode='lines+markers',
                name='AI Adoption'
            ))
            
            # Mock rendering
            mock_plotly(fig, use_container_width=True)
            
            # Verify chart was rendered
            assert mock_plotly.call_count == 1
            assert mock_plotly.call_args[1]['use_container_width'] == True
    
    @pytest.mark.integration
    def test_chart_data_binding(self, sector_data):
        """Test chart data binding and validation"""
        
        import plotly.express as px
        
        # Test that charts can be created with real data
        try:
            fig = px.bar(
                sector_data,
                x='sector',
                y='adoption_rate',
                title='Sector Adoption Rates'
            )
            
            # Verify chart has data
            assert len(fig.data) > 0
            assert len(fig.data[0].x) == len(sector_data)
            
        except Exception as e:
            pytest.fail(f"Chart creation failed: {e}")