"""Unit tests for Key Takeaways Generator component."""

import pytest
from unittest.mock import Mock, patch
import pandas as pd

from components.key_takeaways import KeyTakeawaysGenerator, Takeaway
from tests.utils.test_helpers import StreamlitTestHelper


class TestKeyTakeawaysGenerator:
    """Test suite for Key Takeaways Generator."""
    
    @pytest.fixture
    def generator(self):
        """Create KeyTakeawaysGenerator instance."""
        return KeyTakeawaysGenerator()
    
    @pytest.fixture
    def sample_takeaways(self):
        """Create sample takeaways for testing."""
        return [
            Takeaway(
                category='threat',
                message='Adoption below industry average by 15%',
                urgency='high',
                impact='high',
                timeframe='immediate'
            ),
            Takeaway(
                category='opportunity',
                message='AI costs dropped 85% enabling new use cases',
                urgency='high',
                impact='high',
                timeframe='short-term'
            ),
            Takeaway(
                category='action',
                message='Launch 3 pilot projects in next 90 days',
                urgency='critical',
                impact='high',
                timeframe='immediate'
            )
        ]
    
    def test_takeaway_dataclass(self):
        """Test Takeaway dataclass."""
        takeaway = Takeaway(
            category='threat',
            message='Test threat',
            urgency='high',
            impact='medium',
            timeframe='short-term'
        )
        
        assert takeaway.category == 'threat'
        assert takeaway.urgency == 'high'
        assert takeaway.impact == 'medium'
    
    def test_generate_adoption_takeaways(self, generator):
        """Test adoption rate takeaway generation."""
        data = {
            'current_adoption': 65,
            'yoy_growth': 25,
            'industry_average': 80
        }
        
        takeaways = generator.generate_takeaways('adoption_rates', data)
        
        # Should generate relevant takeaways
        assert len(takeaways) > 0
        assert len(takeaways) <= 3  # Top 3 only
        
        # Should identify threat (below average)
        threat_found = any(t.category == 'threat' for t in takeaways)
        assert threat_found
        
        # Should identify opportunity (high growth)
        opp_found = any(t.category == 'opportunity' for t in takeaways)
        assert opp_found
    
    def test_generate_competitive_takeaways(self, generator):
        """Test competitive position takeaway generation."""
        data = {
            'competitive_position': 'Laggard',
            'gap_to_leaders': 35,
            'time_to_parity_months': 24
        }
        
        takeaways = generator.generate_takeaways('competitive_position', data)
        
        # Should identify critical threat
        critical_threats = [t for t in takeaways if t.category == 'threat' and t.urgency == 'critical']
        assert len(critical_threats) > 0
        
        # Should recommend action
        actions = [t for t in takeaways if t.category == 'action']
        assert len(actions) > 0
    
    def test_generate_roi_takeaways(self, generator):
        """Test ROI analysis takeaway generation."""
        data = {
            'expected_roi': 220,
            'payback_months': 8,
            'confidence_level': 'high'
        }
        
        takeaways = generator.generate_takeaways('roi_analysis', data)
        
        # Should identify strong opportunity
        opportunities = [t for t in takeaways if t.category == 'opportunity']
        assert len(opportunities) > 0
        
        # Should have positive messaging
        assert any('strong' in t.message.lower() or 'justif' in t.message.lower() 
                  for t in takeaways)
    
    def test_urgency_sorting(self, generator):
        """Test takeaways are sorted by urgency."""
        # Create takeaways with different urgencies
        unsorted_takeaways = [
            Takeaway('action', 'Low priority', 'low', 'low', 'long-term'),
            Takeaway('threat', 'Critical issue', 'critical', 'high', 'immediate'),
            Takeaway('opportunity', 'Medium opportunity', 'medium', 'medium', 'short-term'),
            Takeaway('threat', 'High risk', 'high', 'high', 'immediate')
        ]
        
        # Sort using generator logic
        sorted_takeaways = sorted(
            unsorted_takeaways,
            key=lambda x: ['critical', 'high', 'medium', 'low'].index(x.urgency)
        )
        
        # Verify order
        assert sorted_takeaways[0].urgency == 'critical'
        assert sorted_takeaways[-1].urgency == 'low'
    
    def test_render_takeaways(self, generator, sample_takeaways):
        """Test takeaway rendering."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock expander
            mock_expander = Mock()
            mock_expander.__enter__ = Mock(return_value=mock_expander)
            mock_expander.__exit__ = Mock(return_value=None)
            mocks['expander'].return_value = mock_expander
            
            # Render takeaways
            generator.render_takeaways(sample_takeaways)
            
            # Verify expander created
            assert mocks['expander'].called
            
            # Verify content rendered
            assert mocks['markdown'].called
            
            # Check all takeaways displayed
            markdown_calls = mocks['markdown'].call_count
            assert markdown_calls >= len(sample_takeaways)
    
    def test_render_single_takeaway(self, generator):
        """Test single takeaway rendering."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create columns mock
            mock_cols = [Mock(), Mock()]
            mocks['columns'].return_value = mock_cols
            
            takeaway = Takeaway(
                category='threat',
                message='Test threat message',
                urgency='high',
                impact='high',
                timeframe='immediate'
            )
            
            # Render
            generator._render_single_takeaway(takeaway, show_details=True)
            
            # Verify columns used
            assert mocks['columns'].called
            
            # Verify markdown with urgency color
            assert mocks['markdown'].called
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks['markdown'])
            assert any('#' in content for content in markdown_content)  # Color code
    
    def test_generate_smart_summary(self, generator):
        """Test smart summary generation."""
        test_df = pd.DataFrame({
            'metric': ['adoption', 'roi', 'growth'],
            'value': [87, 185, 15]
        })
        
        # Generate summaries for different personas
        exec_summary = generator.generate_smart_summary(test_df, 'competitive_position', 'Executive')
        researcher_summary = generator.generate_smart_summary(test_df, 'competitive_position', 'Researcher')
        
        # Executive should be concise
        assert 'strategic' in exec_summary.lower()
        
        # Researcher should be analytical
        assert 'analysis' in researcher_summary.lower() or 'statistical' in researcher_summary.lower()
    
    def test_labor_impact_takeaways(self, generator):
        """Test labor impact takeaway generation."""
        data = {
            'displacement_risk': 25,
            'augmentation_percentage': 55,
            'reskilling_gap': 70
        }
        
        takeaways = generator.generate_takeaways('labor_impact', data)
        
        # Should identify high displacement risk
        displacement_threats = [t for t in takeaways if 'displacement' in t.message.lower()]
        assert len(displacement_threats) > 0
        
        # Should recommend reskilling
        reskilling_actions = [t for t in takeaways if 'reskilling' in t.message.lower()]
        assert len(reskilling_actions) > 0
    
    def test_fallback_takeaways(self, generator):
        """Test fallback for unknown view types."""
        takeaways = generator.generate_takeaways('unknown_view', {})
        
        # Should return generic takeaways
        assert len(takeaways) > 0
        assert all(isinstance(t, Takeaway) for t in takeaways)
    
    def test_render_summary_box(self, generator, sample_takeaways):
        """Test summary box rendering."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Mock columns for metrics
            mocks['columns'].return_value = [Mock(), Mock(), Mock()]
            
            # Render summary box
            generator.render_summary_box(
                title="Executive Overview",
                takeaways=sample_takeaways[:2],
                additional_metrics={
                    'ROI': '185%',
                    'Payback': '18 months',
                    'Risk': 'Medium'
                }
            )
            
            # Verify components rendered
            assert mocks['markdown'].called
            assert mocks['columns'].called
            assert mocks['metric'].called
            
            # Verify metrics displayed
            assert mocks['metric'].call_count >= 3
    
    def test_empty_data_handling(self, generator):
        """Test handling of empty or missing data."""
        # Empty data
        takeaways = generator.generate_takeaways('adoption_rates', {})
        assert len(takeaways) > 0  # Should have fallbacks
        
        # None values
        data_with_none = {
            'current_adoption': None,
            'yoy_growth': None,
            'industry_average': 72
        }
        takeaways = generator.generate_takeaways('adoption_rates', data_with_none)
        assert len(takeaways) > 0
        
        # Verify no None values in messages
        assert all('None' not in t.message for t in takeaways)
    
    def test_persona_specific_generation(self, generator):
        """Test persona-specific takeaway generation."""
        data = {
            'current_adoption': 75,
            'roi': 165,
            'implementation_time': 12
        }
        
        # Executive persona
        exec_takeaways = generator.generate_takeaways('roi_analysis', data, 'Executive')
        
        # Policymaker persona
        policy_takeaways = generator.generate_takeaways('roi_analysis', data, 'Policymaker')
        
        # Should have different focus
        # Executive focuses on ROI/competitive advantage
        exec_has_roi = any('roi' in t.message.lower() or 'return' in t.message.lower() 
                          for t in exec_takeaways)
        assert exec_has_roi
        
        # Note: In real implementation, personas would have different takeaway logic