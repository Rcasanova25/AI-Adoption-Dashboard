"""
Enhanced Dashboard Integration Module
====================================

Drop-in replacement for load_data() function with all new features.
Maintains 100% backward compatibility while adding new capabilities.
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, Optional
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import new components, fallback gracefully
try:
    from data.optimized_data_manager import create_optimized_manager
    USE_OPTIMIZED_MANAGER = True
except ImportError:
    USE_OPTIMIZED_MANAGER = False
    print("Warning: Optimized data manager not available, using legacy loader")

try:
    from components.competitive_assessor import CompetitivePositionAssessor
    HAS_COMPETITIVE_ASSESSOR = True
except ImportError:
    HAS_COMPETITIVE_ASSESSOR = False

try:
    from components.accessibility import AccessibilityManager
    HAS_ACCESSIBILITY = True
except ImportError:
    HAS_ACCESSIBILITY = False

try:
    from components.economic_insights import EconomicInsights
    HAS_ECONOMIC_INSIGHTS = True
except ImportError:
    HAS_ECONOMIC_INSIGHTS = False

try:
    from components.progressive_disclosure import ProgressiveDisclosure
    HAS_PROGRESSIVE_DISCLOSURE = True
except ImportError:
    HAS_PROGRESSIVE_DISCLOSURE = False

# Import the original load_data function as fallback
from dashboard_integration import load_data_enhanced as legacy_load_data

@st.cache_data(ttl=3600)
def load_data_enhanced() -> Tuple:
    """
    Enhanced data loading function with new features.
    Maintains backward compatibility with original load_data().
    
    Returns:
        Tuple of all data DataFrames in exact same order as original
    """
    
    # Check if we should use the optimized manager
    if USE_OPTIMIZED_MANAGER and st.session_state.get('use_optimized_loader', True):
        try:
            # Initialize optimized manager
            if 'data_manager' not in st.session_state:
                with st.spinner("Initializing optimized data systems..."):
                    st.session_state.data_manager = create_optimized_manager()
            
            manager = st.session_state.data_manager
            
            # Get all data
            all_data = manager.get_all_data()
            
            # Map to legacy format for backward compatibility
            # This ensures the exact same return signature
            historical_data = all_data.get('historical_trends', pd.DataFrame({
                'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
                'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
            }))
            
            sector_2018 = all_data.get('sector_2018', pd.DataFrame({
                'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                          'Finance & Insurance', 'Retail Trade', 'Construction'],
                'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
                'employment_weighted': [18, 22, 15, 14, 12, 8, 6]
            }))
            
            sector_2025 = all_data.get('industry_analysis', pd.DataFrame({
                'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                          'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
                'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
                'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
                'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
            }))
            
            # Continue mapping all other data...
            # (Using get() with defaults ensures backward compatibility)
            
            firm_size = all_data.get('firm_size_analysis', legacy_load_data()[3])
            ai_maturity = all_data.get('technology_maturity', legacy_load_data()[4])
            geographic = all_data.get('geographic_distribution', legacy_load_data()[5])
            tech_stack = all_data.get('technology_stack', legacy_load_data()[6])
            productivity_data = all_data.get('productivity_trends', legacy_load_data()[7])
            productivity_by_skill = all_data.get('skill_productivity', legacy_load_data()[8])
            ai_productivity_estimates = all_data.get('productivity_estimates', legacy_load_data()[9])
            oecd_g7_adoption = all_data.get('oecd_adoption', legacy_load_data()[10])
            oecd_applications = all_data.get('oecd_applications', legacy_load_data()[11])
            barriers_data = all_data.get('adoption_barriers', legacy_load_data()[12])
            support_effectiveness = all_data.get('support_effectiveness', legacy_load_data()[13])
            state_data = all_data.get('state_data', legacy_load_data()[14])
            ai_investment_data = all_data.get('investment_trends', legacy_load_data()[15])
            regional_growth = all_data.get('regional_growth', legacy_load_data()[16])
            ai_cost_reduction = all_data.get('cost_trends', legacy_load_data()[17])
            financial_impact = all_data.get('financial_impact', legacy_load_data()[18])
            ai_perception = all_data.get('perception_data', legacy_load_data()[19])
            training_emissions = all_data.get('environmental_impact', legacy_load_data()[20])
            skill_gap_data = all_data.get('skill_gaps', legacy_load_data()[21])
            ai_governance = all_data.get('governance_metrics', legacy_load_data()[22])
            genai_2025 = all_data.get('genai_adoption', legacy_load_data()[23])
            token_economics = all_data.get('token_economics', legacy_load_data()[24])
            token_usage_patterns = all_data.get('token_usage', legacy_load_data()[25])
            token_optimization = all_data.get('token_optimization', legacy_load_data()[26])
            token_pricing_evolution = all_data.get('token_pricing', legacy_load_data()[27])
            
            # Store enhanced data in session state for new components
            st.session_state.enhanced_data = all_data
            
            return (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
                    geographic, tech_stack, productivity_data, productivity_by_skill,
                    ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
                    barriers_data, support_effectiveness, state_data, ai_investment_data, 
                    regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
                    training_emissions, skill_gap_data, ai_governance, genai_2025,
                    token_economics, token_usage_patterns, token_optimization, token_pricing_evolution)
                    
        except Exception as e:
            st.warning(f"Optimized loader failed, using legacy: {str(e)}")
            # Fall back to legacy loader
            return legacy_load_data()
    else:
        # Use legacy loader
        return legacy_load_data()

def inject_new_features():
    """
    Inject new features into existing dashboard.
    Call this after st.set_page_config() in app.py.
    """
    
    # Inject accessibility features
    if HAS_ACCESSIBILITY:
        try:
            manager = AccessibilityManager()
            manager.inject_accessibility_features()
            st.session_state.accessibility_enabled = True
        except Exception as e:
            st.session_state.accessibility_enabled = False
            if st.session_state.get('debug_mode', False):
                st.sidebar.error(f"Accessibility injection failed: {e}")
    
    # Add competitive assessor button to sidebar
    if HAS_COMPETITIVE_ASSESSOR and st.sidebar.button("🏆 Competitive Assessment", key="comp_assess_btn"):
        show_competitive_assessment_modal()
    
    # Add progressive disclosure control
    if HAS_PROGRESSIVE_DISCLOSURE:
        disclosure = ProgressiveDisclosure()
        with st.sidebar:
            st.markdown("---")
            disclosure.render_level_selector()
    
    # Add economic insights button
    if HAS_ECONOMIC_INSIGHTS and st.sidebar.button("💡 Economic Insights", key="econ_insights_btn"):
        show_economic_insights_modal()

def show_competitive_assessment_modal():
    """Show competitive assessment in a modal-like container."""
    with st.container():
        assessor = CompetitivePositionAssessor()
        
        # Get data from session state
        if 'enhanced_data' in st.session_state:
            data = st.session_state.enhanced_data
        else:
            # Load data if not available
            load_data_enhanced()
            data = st.session_state.get('enhanced_data', {})
        
        # Quick assessment form
        st.markdown("### 🏆 Quick Competitive Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Your Industry",
                ["Technology", "Financial Services", "Healthcare", "Manufacturing", 
                 "Retail & E-commerce", "Education", "Energy & Utilities", "Government"],
                key="modal_industry"
            )
            
            company_size = st.selectbox(
                "Company Size",
                ["< 50 employees", "50-249", "250-999", "1,000-4,999", "5,000+"],
                key="modal_size"
            )
        
        with col2:
            ai_usage = st.select_slider(
                "Current AI Adoption Level",
                options=["None", "Exploring", "Piloting", "Limited Production", "Scaled Production"],
                value="Exploring",
                key="modal_ai_level"
            )
            
            if st.button("Get Assessment", type="primary", key="modal_assess"):
                assessment_data = {
                    'company': {
                        'industry': industry,
                        'size': company_size,
                        'ai_maturity': ai_usage
                    }
                }
                
                # Show assessment results
                position = assessor.calculate_position(data, assessment_data['company'])
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Your Position", f"{position['percentile']:.0f}th percentile")
                with col2:
                    st.metric("vs Industry Avg", f"{position['vs_industry']:+.0f}%")
                with col3:
                    st.metric("Gap to Leaders", f"{position['gap_to_leaders']:.0f}%")
                
                # Show recommendations
                st.markdown("### 📋 Recommended Actions")
                recommendations = assessor.generate_recommendations(position, assessment_data['company'])
                for i, rec in enumerate(recommendations[:3], 1):
                    st.write(f"{i}. {rec}")

def show_economic_insights_modal():
    """Show economic insights in a modal-like container."""
    with st.container():
        insights = EconomicInsights()
        
        # Get data
        if 'enhanced_data' in st.session_state:
            data = st.session_state.enhanced_data
        else:
            load_data_enhanced()
            data = st.session_state.get('enhanced_data', {})
        
        st.markdown("### 💡 Economic Insights")
        
        # Cost of inaction calculator
        col1, col2 = st.columns(2)
        
        with col1:
            current_position = st.slider(
                "Current AI Maturity (0-100)",
                0, 100, 30,
                key="modal_maturity"
            )
            
            market_size = st.number_input(
                "Your Market Size ($M)",
                min_value=10.0,
                max_value=10000.0,
                value=100.0,
                step=10.0,
                key="modal_market"
            )
        
        with col2:
            industry_avg = st.slider(
                "Industry Average Maturity",
                0, 100, 50,
                key="modal_ind_avg"
            )
            
            years = st.slider(
                "Time Horizon (years)",
                1, 10, 5,
                key="modal_years"
            )
        
        if st.button("Calculate Cost of Inaction", key="modal_calc"):
            cost = insights.calculate_cost_of_inaction(
                current_position,
                industry_avg,
                market_size,
                years
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Lost Market Share",
                    f"{cost['market_share_loss']:.1f}%",
                    help="Projected market share loss"
                )
            
            with col2:
                st.metric(
                    "Revenue Impact",
                    f"${cost['revenue_impact']:.1f}M",
                    delta=f"-${cost['revenue_impact']/years:.1f}M/year"
                )
            
            with col3:
                st.metric(
                    "Competitive Gap",
                    f"{cost['competitive_gap']:.0f}%",
                    help="Gap vs competitors after time horizon"
                )

def add_view_enhancements(view_type: str, data: Dict[str, Any]):
    """
    Add economic insights to existing views.
    Call this within each view rendering function.
    """
    if not HAS_ECONOMIC_INSIGHTS:
        return
    
    try:
        from components.view_enhancements import ViewEnhancer
        enhancer = ViewEnhancer()
        
        enhancement = enhancer.enhance_view(view_type, data)
        
        if enhancement:
            # Add "What This Means" section
            with st.expander("💡 What This Means", expanded=True):
                st.info(enhancement['insight'])
                
                if 'metrics' in enhancement:
                    cols = st.columns(len(enhancement['metrics']))
                    for col, metric in zip(cols, enhancement['metrics']):
                        with col:
                            st.metric(
                                metric['label'],
                                metric['value'],
                                delta=metric.get('delta')
                            )
                
                if 'recommendations' in enhancement:
                    st.markdown("**Key Actions:**")
                    for rec in enhancement['recommendations']:
                        st.write(f"• {rec}")
    
    except Exception as e:
        if st.session_state.get('debug_mode', False):
            st.error(f"View enhancement failed: {e}")

# Convenience function for easy integration
def upgrade_dashboard():
    """
    One-line upgrade for existing dashboards.
    Add this after st.set_page_config() in app.py:
    
    from dashboard_integration_enhanced import upgrade_dashboard
    upgrade_dashboard()
    """
    
    # Inject new features
    inject_new_features()
    
    # Override load_data in the global namespace
    import sys
    if 'app' in sys.modules:
        sys.modules['app'].load_data = load_data_enhanced
    
    # Set feature flags
    st.session_state.enhanced_features = {
        'competitive_assessor': HAS_COMPETITIVE_ASSESSOR,
        'accessibility': HAS_ACCESSIBILITY,
        'economic_insights': HAS_ECONOMIC_INSIGHTS,
        'progressive_disclosure': HAS_PROGRESSIVE_DISCLOSURE,
        'optimized_loader': USE_OPTIMIZED_MANAGER
    }
    
    # Show features status in sidebar
    with st.sidebar:
        if st.checkbox("Show Enhancement Status", value=False):
            st.markdown("### 🚀 Enhanced Features")
            for feature, enabled in st.session_state.enhanced_features.items():
                if enabled:
                    st.success(f"✅ {feature.replace('_', ' ').title()}")
                else:
                    st.info(f"⚪ {feature.replace('_', ' ').title()}")

# Export key functions for direct use
__all__ = [
    'load_data_enhanced',
    'inject_new_features', 
    'show_competitive_assessment_modal',
    'show_economic_insights_modal',
    'add_view_enhancements',
    'upgrade_dashboard'
]