"""
Cross-Persona Navigation Interface for AI Adoption Dashboard

This module provides navigation components for the cross-persona comparison
functionality, including persona selection, view switching, and comparison
mode controls.
"""

import streamlit as st
from typing import List, Dict, Optional, Tuple
from enum import Enum
import pandas as pd

# Import persona types from comparison module
from .persona_comparison import PersonaType, PERSONA_CONFIGS

class NavigationMode(Enum):
    """Navigation modes for the dashboard"""
    SINGLE_PERSONA = "single_persona"
    COMPARISON_MODE = "comparison_mode"
    ANALYSIS_MODE = "analysis_mode"

class PersonaNavigationInterface:
    """Main navigation interface for cross-persona functionality"""
    
    def __init__(self):
        self.persona_configs = PERSONA_CONFIGS
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables for navigation"""
        if 'navigation_mode' not in st.session_state:
            st.session_state.navigation_mode = NavigationMode.SINGLE_PERSONA
        
        if 'selected_personas' not in st.session_state:
            st.session_state.selected_personas = [PersonaType.GENERAL]
        
        if 'comparison_metrics' not in st.session_state:
            st.session_state.comparison_metrics = []
        
        if 'show_persona_insights' not in st.session_state:
            st.session_state.show_persona_insights = True
        
        if 'selected_persona' not in st.session_state:
            st.session_state.selected_persona = "General"
    
    def render_navigation_sidebar(self) -> Dict[str, any]:
        """
        Render the main navigation sidebar with persona selection and comparison controls
        
        Returns:
            Dict containing current navigation state
        """
        st.sidebar.header("🎭 Persona Navigation")
        
        # Navigation mode selection
        mode_options = {
            "👤 Single Persona View": NavigationMode.SINGLE_PERSONA,
            "⚖️ Compare Personas": NavigationMode.COMPARISON_MODE,
            "🔍 Analysis Mode": NavigationMode.ANALYSIS_MODE
        }
        
        selected_mode_text = st.sidebar.radio(
            "Navigation Mode",
            list(mode_options.keys()),
            key="nav_mode_radio"
        )
        
        st.session_state.navigation_mode = mode_options[selected_mode_text]
        
        # Render controls based on selected mode
        if st.session_state.navigation_mode == NavigationMode.SINGLE_PERSONA:
            return self._render_single_persona_controls()
        elif st.session_state.navigation_mode == NavigationMode.COMPARISON_MODE:
            return self._render_comparison_controls()
        else:  # ANALYSIS_MODE
            return self._render_analysis_controls()
    
    def _render_single_persona_controls(self) -> Dict[str, any]:
        """Render controls for single persona view"""
        st.sidebar.subheader("👤 Single Persona View")
        
        # Persona selection
        persona_options = {
            "General User": PersonaType.GENERAL,
            "Business Leader": PersonaType.BUSINESS_LEADER,
            "Policymaker": PersonaType.POLICYMAKER,
            "Researcher": PersonaType.RESEARCHER
        }
        
        selected_persona_text = st.sidebar.selectbox(
            "Select Your Role",
            list(persona_options.keys()),
            key="single_persona_select"
        )
        
        selected_persona = persona_options[selected_persona_text]
        st.session_state.selected_personas = [selected_persona]
        
        # Update legacy session state for compatibility
        st.session_state.selected_persona = selected_persona.value
        
        # Show persona-specific insights
        self._show_persona_info(selected_persona)
        
        # Advanced options
        with st.sidebar.expander("🔧 Advanced Options", expanded=False):
            show_insights = st.checkbox("Show Persona Insights", value=True)
            st.session_state.show_persona_insights = show_insights
            
            enable_recommendations = st.checkbox("Enable Smart Recommendations", value=True)
            
            if enable_recommendations:
                st.caption("💡 Personalized recommendations based on your role")
        
        return {
            "mode": NavigationMode.SINGLE_PERSONA,
            "personas": [selected_persona],
            "show_insights": st.session_state.show_persona_insights,
            "enable_recommendations": enable_recommendations if 'enable_recommendations' in locals() else True
        }
    
    def _render_comparison_controls(self) -> Dict[str, any]:
        """Render controls for comparison mode"""
        st.sidebar.subheader("⚖️ Compare Personas")
        
        # Multi-persona selection
        persona_options = {
            "General User": PersonaType.GENERAL,
            "Business Leader": PersonaType.BUSINESS_LEADER,
            "Policymaker": PersonaType.POLICYMAKER,
            "Researcher": PersonaType.RESEARCHER
        }
        
        st.sidebar.write("Select personas to compare:")
        selected_personas = []
        
        for name, persona_type in persona_options.items():
            if st.sidebar.checkbox(name, value=persona_type == PersonaType.GENERAL, key=f"compare_{name}"):
                selected_personas.append(persona_type)
        
        if not selected_personas:
            st.sidebar.warning("Please select at least one persona.")
            selected_personas = [PersonaType.GENERAL]
        
        st.session_state.selected_personas = selected_personas
        
        # Comparison type selection
        comparison_types = [
            "Side-by-Side Metrics",
            "ROI Comparison Matrix", 
            "Perspective Radar",
            "Investment Analysis",
            "Risk Assessment"
        ]
        
        selected_comparison = st.sidebar.selectbox(
            "Comparison Type",
            comparison_types,
            key="comparison_type_select"
        )
        
        # Metric selection for comparison
        available_metrics = [
            "adoption_rate",
            "roi_multiplier", 
            "investment_required",
            "risk_score",
            "time_to_value",
            "implementation_complexity"
        ]
        
        selected_metrics = st.sidebar.multiselect(
            "Metrics to Compare",
            available_metrics,
            default=available_metrics[:3],
            key="comparison_metrics_select"
        )
        
        st.session_state.comparison_metrics = selected_metrics
        
        # Advanced comparison options
        with st.sidebar.expander("🔧 Comparison Options", expanded=False):
            show_insights = st.checkbox("Show Cross-Persona Insights", value=True)
            highlight_differences = st.checkbox("Highlight Key Differences", value=True)
            enable_export = st.checkbox("Enable Export to PDF", value=False)
            
            if enable_export:
                st.caption("📄 Export comparison results to PDF report")
        
        # Show selected personas summary
        if len(selected_personas) > 1:
            st.sidebar.success(f"Comparing {len(selected_personas)} personas")
            for persona in selected_personas:
                st.sidebar.write(f"• {persona.value}")
        
        return {
            "mode": NavigationMode.COMPARISON_MODE,
            "personas": selected_personas,
            "comparison_type": selected_comparison,
            "metrics": selected_metrics,
            "show_insights": show_insights if 'show_insights' in locals() else True,
            "highlight_differences": highlight_differences if 'highlight_differences' in locals() else True,
            "enable_export": enable_export if 'enable_export' in locals() else False
        }
    
    def _render_analysis_controls(self) -> Dict[str, any]:
        """Render controls for analysis mode"""
        st.sidebar.subheader("🔍 Analysis Mode")
        
        # Analysis type selection
        analysis_types = [
            "Convergence Analysis",
            "Strategic Alignment",
            "Decision Matrix",
            "Stakeholder Impact",
            "Implementation Roadmap"
        ]
        
        selected_analysis = st.sidebar.selectbox(
            "Analysis Type",
            analysis_types,
            key="analysis_type_select"
        )
        
        # Scenario selection
        scenarios = [
            "Current State",
            "6-Month Horizon",
            "1-Year Projection",
            "Conservative Estimate",
            "Optimistic Scenario"
        ]
        
        selected_scenario = st.sidebar.selectbox(
            "Scenario",
            scenarios,
            key="scenario_select"
        )
        
        # Industry/sector focus
        industries = [
            "Technology",
            "Financial Services", 
            "Healthcare",
            "Manufacturing",
            "Retail & E-commerce",
            "Education",
            "Government",
            "All Industries"
        ]
        
        selected_industry = st.sidebar.selectbox(
            "Industry Focus",
            industries,
            index=len(industries)-1,  # Default to "All Industries"
            key="industry_focus_select"
        )
        
        # Advanced analysis options
        with st.sidebar.expander("🔧 Analysis Options", expanded=False):
            confidence_level = st.slider("Confidence Level", 80, 99, 95, key="confidence_slider")
            include_uncertainty = st.checkbox("Include Uncertainty Analysis", value=True)
            generate_recommendations = st.checkbox("Generate Actionable Recommendations", value=True)
        
        return {
            "mode": NavigationMode.ANALYSIS_MODE,
            "analysis_type": selected_analysis,
            "scenario": selected_scenario,
            "industry": selected_industry,
            "confidence_level": confidence_level if 'confidence_level' in locals() else 95,
            "include_uncertainty": include_uncertainty if 'include_uncertainty' in locals() else True,
            "generate_recommendations": generate_recommendations if 'generate_recommendations' in locals() else True
        }
    
    def _show_persona_info(self, persona: PersonaType):
        """Show information about the selected persona"""
        config = self.persona_configs[persona]
        
        with st.sidebar.expander(f"ℹ️ About {persona.value}", expanded=False):
            st.write(f"**Focus Areas:**")
            for metric in config.primary_metrics[:3]:  # Show top 3
                st.write(f"• {metric.replace('_', ' ').title()}")
            
            st.write(f"**ROI Focus:** {config.roi_focus}")
            st.write(f"**Time Horizon:** {config.time_horizon}")
            st.write(f"**Risk Tolerance:** {config.risk_tolerance}")
            
            if config.key_insights:
                st.write("**Key Insights:**")
                for insight in config.key_insights[:2]:  # Show top 2
                    st.write(f"• {insight}")
    
    def render_breadcrumb_navigation(self, current_view: str) -> None:
        """Render breadcrumb navigation for current view"""
        mode = st.session_state.navigation_mode
        personas = st.session_state.selected_personas
        
        # Build breadcrumb path
        breadcrumbs = ["🏠 Dashboard"]
        
        if mode == NavigationMode.SINGLE_PERSONA:
            breadcrumbs.append(f"👤 {personas[0].value}")
        elif mode == NavigationMode.COMPARISON_MODE:
            breadcrumbs.append(f"⚖️ Compare ({len(personas)} personas)")
        else:
            breadcrumbs.append("🔍 Analysis")
        
        breadcrumbs.append(current_view)
        
        # Render breadcrumbs
        breadcrumb_html = " > ".join([f"<span style='color: #2E86AB;'>{crumb}</span>" for crumb in breadcrumbs])
        st.markdown(f"<div style='margin-bottom: 1rem; font-size: 0.9rem;'>{breadcrumb_html}</div>", 
                   unsafe_allow_html=True)
    
    def get_persona_specific_views(self, persona: PersonaType) -> List[str]:
        """Get views available for a specific persona"""
        # This maps to the original persona_views structure
        view_mapping = {
            PersonaType.GENERAL: ["🎯 Competitive Position Assessor", "Historical Trends"],
            PersonaType.BUSINESS_LEADER: [
                "🎯 Competitive Position Assessor", 
                "💰 Investment Decision Engine", 
                "Financial Impact", 
                "ROI Analysis",
                "🏭 Firm Size Analysis",
                "🎓 Skill Gap Analysis"
            ],
            PersonaType.POLICYMAKER: [
                "⚖️ Regulatory Risk Radar", 
                "Labor Impact", 
                "Geographic Distribution", 
                "🚧 Barriers & Support", 
                "🌍 OECD 2025 Findings"
            ],
            PersonaType.RESEARCHER: [
                "Historical Trends", 
                "Productivity Research", 
                "🤖 AI Technology Maturity", 
                "🌍 OECD 2025 Findings", 
                "Bibliography & Sources"
            ]
        }
        
        return view_mapping.get(persona, [])
    
    def render_view_selector(self, persona: PersonaType) -> Optional[str]:
        """Render view selector for a specific persona"""
        available_views = self.get_persona_specific_views(persona)
        
        if not available_views:
            return None
        
        # Add comparison view as an option
        all_views = ["🔄 Cross-Persona Comparison"] + available_views
        
        selected_view = st.sidebar.selectbox(
            f"📊 {persona.value} Views",
            all_views,
            key=f"view_select_{persona.value}"
        )
        
        return selected_view
    
    def render_quick_actions(self) -> Dict[str, bool]:
        """Render quick action buttons in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚡ Quick Actions")
        
        actions = {}
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            actions["export_data"] = st.button("📊 Export Data", key="export_data_btn")
            actions["save_config"] = st.button("💾 Save Config", key="save_config_btn")
        
        with col2:
            actions["reset_view"] = st.button("🔄 Reset View", key="reset_view_btn")
            actions["help"] = st.button("❓ Help", key="help_btn")
        
        return actions

class PersonaComparisonNavigation:
    """Specialized navigation for comparison mode"""
    
    def __init__(self):
        self.nav_interface = PersonaNavigationInterface()
    
    def render_comparison_header(self, personas: List[PersonaType]) -> None:
        """Render header for comparison mode"""
        if len(personas) < 2:
            st.warning("⚠️ Please select at least 2 personas for meaningful comparison.")
            return
        
        # Create comparison header
        persona_names = [p.value for p in personas]
        comparison_text = " vs ".join(persona_names)
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <h2 style="margin: 0; font-size: 1.8rem;">⚖️ Persona Comparison</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                {comparison_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_comparison_summary(self, personas: List[PersonaType], metrics: List[str]) -> None:
        """Render summary of comparison settings"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Personas Compared",
                value=len(personas),
                delta=f"{len(personas) - 1} comparisons" if len(personas) > 1 else None
            )
        
        with col2:
            st.metric(
                label="Metrics Analyzed",
                value=len(metrics),
                delta=f"{len(metrics)} dimensions"
            )
        
        with col3:
            # Calculate complexity score
            complexity = len(personas) * len(metrics)
            complexity_level = "Low" if complexity < 6 else "Medium" if complexity < 12 else "High"
            
            st.metric(
                label="Analysis Complexity",
                value=complexity_level,
                delta=f"{complexity} data points"
            )

# Usage example
def demo_navigation():
    """Demo function for navigation components"""
    st.title("🎭 Persona Navigation Demo")
    
    # Initialize navigation
    nav = PersonaNavigationInterface()
    
    # Render sidebar navigation
    nav_state = nav.render_navigation_sidebar()
    
    # Render main content based on navigation state
    if nav_state["mode"] == NavigationMode.SINGLE_PERSONA:
        st.header(f"👤 {nav_state['personas'][0].value} Dashboard")
        st.write("This is the single persona view.")
        
        # Render view selector
        selected_view = nav.render_view_selector(nav_state['personas'][0])
        if selected_view:
            st.subheader(f"Current View: {selected_view}")
    
    elif nav_state["mode"] == NavigationMode.COMPARISON_MODE:
        comparison_nav = PersonaComparisonNavigation()
        comparison_nav.render_comparison_header(nav_state["personas"])
        comparison_nav.render_comparison_summary(nav_state["personas"], nav_state["metrics"])
        
        st.write(f"Comparison Type: {nav_state['comparison_type']}")
        st.write(f"Selected Metrics: {nav_state['metrics']}")
    
    else:  # Analysis mode
        st.header("🔍 Analysis Mode")
        st.write(f"Analysis Type: {nav_state['analysis_type']}")
        st.write(f"Scenario: {nav_state['scenario']}")
        st.write(f"Industry Focus: {nav_state['industry']}")
    
    # Render breadcrumbs
    nav.render_breadcrumb_navigation("Demo View")
    
    # Render quick actions
    actions = nav.render_quick_actions()
    if any(actions.values()):
        st.write("Quick action performed:", [k for k, v in actions.items() if v])

if __name__ == "__main__":
    demo_navigation()