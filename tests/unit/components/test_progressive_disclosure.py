"""Unit tests for Progressive Disclosure component."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

from components.progressive_disclosure import ProgressiveDisclosure, DisclosureLevel
from tests.utils.test_helpers import StreamlitTestHelper, MockSessionState


class TestProgressiveDisclosure:
    """Test suite for Progressive Disclosure functionality."""
    
    @pytest.fixture
    def disclosure(self):
        """Create ProgressiveDisclosure instance."""
        return ProgressiveDisclosure()
    
    @pytest.fixture
    def sample_content(self):
        """Create sample content for testing."""
        return {
            'executive': {
                'summary': 'High-level overview',
                'metrics': ['ROI: 185%', 'Adoption: 87%'],
                'action': 'Invest in AI'
            },
            'standard': {
                'summary': 'Detailed analysis with key insights',
                'metrics': ['ROI: 185%', 'Adoption: 87%', 'Growth: 15%'],
                'charts': ['trend_chart', 'comparison_chart'],
                'insights': ['Insight 1', 'Insight 2']
            },
            'detailed': {
                'summary': 'Comprehensive analysis with full data',
                'metrics': ['ROI: 185%', 'Adoption: 87%', 'Growth: 15%', 'More metrics...'],
                'charts': ['trend_chart', 'comparison_chart', 'detailed_chart'],
                'raw_data': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}),
                'methodology': 'Detailed methodology explanation'
            }
        }
    
    def test_disclosure_levels(self):
        """Test disclosure level enum."""
        assert DisclosureLevel.EXECUTIVE.value == 'executive'
        assert DisclosureLevel.STANDARD.value == 'standard'
        assert DisclosureLevel.DETAILED.value == 'detailed'
    
    def test_render_with_disclosure_executive(self, disclosure, sample_content):
        """Test rendering with executive disclosure level."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Set session state
            st = MockSessionState()
            st._state['disclosure_level'] = DisclosureLevel.EXECUTIVE
            
            with patch('streamlit.session_state', st):
                # Render content
                disclosure.render_with_disclosure(
                    title="Test View",
                    content=sample_content,
                    current_level=DisclosureLevel.EXECUTIVE
                )
            
            # Verify executive content displayed
            assert mocks['markdown'].called
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks['markdown'])
            
            # Should show executive summary
            assert any('High-level overview' in content for content in markdown_content)
            
            # Should not show detailed data
            assert not mocks['dataframe'].called
    
    def test_render_with_disclosure_standard(self, disclosure, sample_content):
        """Test rendering with standard disclosure level."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock columns for metrics
            mock_cols = [Mock(), Mock(), Mock()]
            mocks['columns'].return_value = mock_cols
            
            # Render content
            disclosure.render_with_disclosure(
                title="Test View",
                content=sample_content,
                current_level=DisclosureLevel.STANDARD
            )
            
            # Should show more content than executive
            assert mocks['markdown'].called
            assert mocks['columns'].called
            
            # Should show charts
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks['markdown'])
            assert any('chart' in str(content).lower() for content in markdown_content)
    
    def test_render_with_disclosure_detailed(self, disclosure, sample_content):
        """Test rendering with detailed disclosure level."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Render content
            disclosure.render_with_disclosure(
                title="Test View",
                content=sample_content,
                current_level=DisclosureLevel.DETAILED
            )
            
            # Should show all content including raw data
            assert mocks['markdown'].called
            assert mocks['dataframe'].called
            
            # Verify DataFrame displayed
            df_call = mocks['dataframe'].call_args[0][0]
            assert isinstance(df_call, pd.DataFrame)
    
    def test_disclosure_level_selector(self, disclosure):
        """Test disclosure level selector UI."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock radio button selection
            mocks['radio'] = Mock(return_value='Standard')
            
            with patch('streamlit.radio', mocks['radio']):
                # Render selector
                selected = disclosure.render_disclosure_selector()
            
            # Verify selector created
            assert mocks['radio'].called
            
            # Verify options
            call_args = mocks['radio'].call_args
            options = call_args[1]['options']
            assert 'Executive Summary' in options
            assert 'Standard View' in options
            assert 'Detailed Analysis' in options
            
            # Verify return value
            assert selected == DisclosureLevel.STANDARD
    
    def test_collapsible_section(self, disclosure):
        """Test collapsible section functionality."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock expander
            mock_expander = MagicMock()
            mock_expander.__enter__ = Mock(return_value=mock_expander)
            mock_expander.__exit__ = Mock(return_value=None)
            mocks['expander'].return_value = mock_expander
            
            # Create collapsible section
            with disclosure.collapsible_section("Test Section", expanded=True):
                mocks['write']("Test content")
            
            # Verify expander created
            assert mocks['expander'].called
            assert mocks['expander'].call_args[0][0] == "Test Section"
            assert mocks['expander'].call_args[1]['expanded'] == True
    
    def test_auto_disclosure_based_on_persona(self, disclosure):
        """Test automatic disclosure level based on persona."""
        persona_levels = {
            'Executive': DisclosureLevel.EXECUTIVE,
            'Researcher': DisclosureLevel.DETAILED,
            'General': DisclosureLevel.STANDARD
        }
        
        for persona, expected_level in persona_levels.items():
            level = disclosure.get_default_level_for_persona(persona)
            assert level == expected_level
    
    def test_progressive_loading(self, disclosure):
        """Test progressive content loading."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock button for "Show more"
            mocks['button'].side_effect = [True, False]  # First click returns True
            
            # Test progressive loading
            content_shown = disclosure.render_progressive_content(
                sections=['Section 1', 'Section 2', 'Section 3', 'Section 4'],
                initial_count=2
            )
            
            # Verify initial sections shown
            assert mocks['write'].call_count >= 2
            
            # Verify "Show more" button
            assert mocks['button'].called
            button_calls = [call for call in mocks['button'].call_args_list 
                          if 'Show more' in str(call)]
            assert len(button_calls) > 0
    
    def test_information_density_control(self, disclosure):
        """Test information density control."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock slider for density control
            mocks['slider'].return_value = 50  # Medium density
            
            # Render density control
            density = disclosure.render_density_control()
            
            # Verify slider created
            assert mocks['slider'].called
            assert density == 50
            
            # Verify help text
            slider_call = mocks['slider'].call_args
            assert 'help' in slider_call[1]
    
    def test_content_filtering(self, disclosure):
        """Test content filtering based on disclosure level."""
        # Full content
        full_content = {
            'basic_info': 'Available to all',
            'detailed_analysis': 'Standard and above',
            'raw_data': 'Detailed only',
            'technical_details': 'Detailed only'
        }
        
        # Test executive filtering
        exec_content = disclosure.filter_content(
            full_content, 
            DisclosureLevel.EXECUTIVE
        )
        assert 'basic_info' in exec_content
        assert 'raw_data' not in exec_content
        
        # Test standard filtering
        std_content = disclosure.filter_content(
            full_content,
            DisclosureLevel.STANDARD
        )
        assert 'basic_info' in std_content
        assert 'detailed_analysis' in std_content
        assert 'raw_data' not in std_content
        
        # Test detailed filtering
        detailed_content = disclosure.filter_content(
            full_content,
            DisclosureLevel.DETAILED
        )
        assert len(detailed_content) == len(full_content)
    
    def test_smart_summarization(self, disclosure):
        """Test smart content summarization."""
        # Long detailed text
        detailed_text = " ".join([f"Sentence {i}." for i in range(20)])
        
        # Summarize for different levels
        exec_summary = disclosure.summarize_for_level(
            detailed_text,
            DisclosureLevel.EXECUTIVE,
            max_sentences=3
        )
        
        std_summary = disclosure.summarize_for_level(
            detailed_text,
            DisclosureLevel.STANDARD,
            max_sentences=10
        )
        
        # Executive should be shorter
        assert len(exec_summary.split('.')) <= 4  # 3 sentences + empty
        assert len(std_summary.split('.')) <= 11  # 10 sentences + empty
        assert len(exec_summary) < len(std_summary)
    
    def test_visual_complexity_adjustment(self, disclosure):
        """Test visual complexity adjustment for charts."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            import plotly.graph_objects as go
            
            # Create complex chart
            fig = go.Figure()
            for i in range(10):
                fig.add_trace(go.Scatter(
                    x=list(range(100)),
                    y=[j + i for j in range(100)],
                    name=f'Series {i}'
                ))
            
            # Simplify for executive
            exec_fig = disclosure.adjust_chart_complexity(
                fig,
                DisclosureLevel.EXECUTIVE
            )
            
            # Should have fewer traces
            assert len(exec_fig.data) < len(fig.data)
            
            # Detailed should keep all
            detailed_fig = disclosure.adjust_chart_complexity(
                fig,
                DisclosureLevel.DETAILED
            )
            assert len(detailed_fig.data) == len(fig.data)
    
    def test_tooltip_verbosity(self, disclosure):
        """Test tooltip verbosity based on disclosure level."""
        tooltips = disclosure.get_tooltips_for_level(DisclosureLevel.EXECUTIVE)
        assert 'roi' in tooltips
        assert len(tooltips['roi']) < 100  # Short explanation
        
        detailed_tooltips = disclosure.get_tooltips_for_level(DisclosureLevel.DETAILED)
        assert 'roi' in detailed_tooltips
        assert len(detailed_tooltips['roi']) > len(tooltips['roi'])  # More detailed
    
    def test_state_persistence(self, disclosure):
        """Test disclosure level state persistence."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create session state
            st = MockSessionState()
            
            with patch('streamlit.session_state', st):
                # Set level
                disclosure.set_disclosure_level(DisclosureLevel.DETAILED)
                
                # Verify saved
                assert st.get('disclosure_level') == DisclosureLevel.DETAILED
                
                # Get level
                retrieved = disclosure.get_current_level()
                assert retrieved == DisclosureLevel.DETAILED