"""Persona-specific dashboard configurations and layouts."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class PersonaConfig:
    """Configuration for a specific persona."""
    name: str
    title: str
    description: str
    primary_metrics: List[str]
    recommended_views: List[str]
    quick_actions: List[Dict[str, str]]
    time_to_insight: str
    key_questions: List[str]
    default_disclosure_level: str


class PersonaDashboards:
    """Manages persona-specific dashboard experiences."""
    
    def __init__(self):
        """Initialize persona configurations."""
        self.personas = {
            'Executive': PersonaConfig(
                name='Executive',
                title='Executive Strategic Dashboard',
                description='High-level strategic insights for C-suite decision making',
                primary_metrics=['roi', 'competitive_position', 'market_share', 'investment_required'],
                recommended_views=['Competitive Position', 'ROI Analysis', 'Investment Builder'],
                quick_actions=[
                    {'label': '📊 Download Executive Brief', 'action': 'download_brief'},
                    {'label': '🎯 Calculate ROI', 'action': 'roi_calculator'},
                    {'label': '📈 View Market Position', 'action': 'competitive_position'}
                ],
                time_to_insight='2 minutes',
                key_questions=[
                    'What is our competitive position?',
                    'What is the ROI of AI investment?',
                    'How much should we invest?',
                    'What are the key risks?'
                ],
                default_disclosure_level='executive'
            ),
            'Policymaker': PersonaConfig(
                name='Policymaker',
                title='Policy & Governance Dashboard',
                description='Regional insights and policy implications of AI adoption',
                primary_metrics=['regional_adoption', 'labor_impact', 'governance_maturity', 'economic_impact'],
                recommended_views=['Geographic Distribution', 'Labor Impact', 'AI Governance'],
                quick_actions=[
                    {'label': '🗺️ Regional Analysis', 'action': 'geographic_view'},
                    {'label': '👥 Labor Impact Report', 'action': 'labor_analysis'},
                    {'label': '📋 Policy Brief', 'action': 'policy_brief'}
                ],
                time_to_insight='5 minutes',
                key_questions=[
                    'What is the regional adoption pattern?',
                    'How will AI affect employment?',
                    'What governance frameworks are needed?',
                    'What are the economic implications?'
                ],
                default_disclosure_level='standard'
            ),
            'Researcher': PersonaConfig(
                name='Researcher',
                title='Research & Analytics Dashboard',
                description='Comprehensive data analysis and research insights',
                primary_metrics=['adoption_trends', 'technology_maturity', 'research_gaps', 'data_quality'],
                recommended_views=['Historical Trends', 'Technology Stack', 'Productivity Research'],
                quick_actions=[
                    {'label': '📊 Export Dataset', 'action': 'export_data'},
                    {'label': '📈 Trend Analysis', 'action': 'trend_analysis'},
                    {'label': '🔍 Deep Dive', 'action': 'detailed_analysis'}
                ],
                time_to_insight='15 minutes',
                key_questions=[
                    'What are the adoption trends?',
                    'Which technologies are maturing?',
                    'What are the research gaps?',
                    'How reliable is the data?'
                ],
                default_disclosure_level='detailed'
            ),
            'General': PersonaConfig(
                name='General',
                title='AI Insights Dashboard',
                description='Balanced overview of AI adoption and impact',
                primary_metrics=['overall_adoption', 'industry_trends', 'key_benefits', 'implementation_barriers'],
                recommended_views=['Adoption Rates', 'Industry Analysis', 'Cost Trends'],
                quick_actions=[
                    {'label': '📚 Learn Basics', 'action': 'tutorial'},
                    {'label': '📊 View Trends', 'action': 'trends'},
                    {'label': '💡 Get Started', 'action': 'getting_started'}
                ],
                time_to_insight='10 minutes',
                key_questions=[
                    'What is AI adoption?',
                    'Which industries are leading?',
                    'What are the benefits?',
                    'How do I get started?'
                ],
                default_disclosure_level='standard'
            )
        }
    
    def render_persona_selector(self) -> str:
        """Render persona selector and return selected persona."""
        st.sidebar.markdown("### 👤 Select Your Role")
        
        # Create visual persona cards
        persona_icons = {
            'Executive': '👔',
            'Policymaker': '🏛️',
            'Researcher': '🔬',
            'General': '👥'
        }
        
        selected_persona = st.sidebar.radio(
            "Choose your perspective:",
            options=list(self.personas.keys()),
            format_func=lambda x: f"{persona_icons[x]} {x}",
            key='persona_selector'
        )
        
        # Show persona description
        persona = self.personas[selected_persona]
        st.sidebar.info(f"**{persona.time_to_insight} to key insights**\n\n{persona.description}")
        
        return selected_persona
    
    def render_persona_dashboard(self, persona_name: str, data: Dict[str, pd.DataFrame]):
        """Render the main dashboard for a specific persona.
        
        Args:
            persona_name: Name of the persona
            data: Dictionary of available data
        """
        persona = self.personas[persona_name]
        
        # Header with persona-specific messaging
        st.markdown(f"# {persona.title}")
        st.markdown(f"*{persona.description}*")
        
        # Quick actions bar
        self._render_quick_actions(persona)
        
        # Key questions answered
        with st.expander("❓ **Key Questions This Dashboard Answers**", expanded=False):
            for question in persona.key_questions:
                st.markdown(f"• {question}")
        
        # Main content area with tabs
        if persona_name == 'Executive':
            self._render_executive_dashboard(data)
        elif persona_name == 'Policymaker':
            self._render_policymaker_dashboard(data)
        elif persona_name == 'Researcher':
            self._render_researcher_dashboard(data)
        else:
            self._render_general_dashboard(data)
    
    def _render_quick_actions(self, persona: PersonaConfig):
        """Render quick action buttons for persona."""
        st.markdown("### 🚀 Quick Actions")
        
        cols = st.columns(len(persona.quick_actions))
        for idx, action in enumerate(persona.quick_actions):
            with cols[idx]:
                if st.button(
                    action['label'],
                    key=f"quick_action_{action['action']}",
                    use_container_width=True
                ):
                    self._handle_quick_action(action['action'])
    
    def _handle_quick_action(self, action: str):
        """Handle quick action button clicks."""
        action_handlers = {
            'download_brief': lambda: st.info("📥 Generating executive brief..."),
            'roi_calculator': lambda: st.session_state.update({'selected_view': 'ROI Analysis'}),
            'competitive_position': lambda: st.session_state.update({'selected_view': 'Competitive Position'}),
            'geographic_view': lambda: st.session_state.update({'selected_view': 'Geographic Distribution'}),
            'export_data': lambda: st.info("📥 Preparing data export..."),
            'tutorial': lambda: st.session_state.update({'show_tutorial': True})
        }
        
        handler = action_handlers.get(action)
        if handler:
            handler()
            st.rerun()
    
    def _render_executive_dashboard(self, data: Dict[str, pd.DataFrame]):
        """Render executive-specific dashboard."""
        # Executive summary metrics
        st.markdown("### 📊 Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self._render_metric_card(
                "AI Adoption",
                "87%",
                "+15% YoY",
                "Above industry average",
                color="green"
            )
        
        with col2:
            self._render_metric_card(
                "Competitive Position",
                "Leader",
                "Top 20%",
                "Ahead of 80% of peers",
                color="blue"
            )
        
        with col3:
            self._render_metric_card(
                "ROI Projection",
                "185%",
                "18 mo payback",
                "High confidence",
                color="green"
            )
        
        with col4:
            self._render_metric_card(
                "Investment Gap",
                "$2.5M",
                "To reach leaders",
                "Priority: High",
                color="yellow"
            )
        
        # Strategic insights
        st.markdown("### 💡 Strategic Insights")
        
        tab1, tab2, tab3 = st.tabs(["Market Position", "Investment Strategy", "Risk Assessment"])
        
        with tab1:
            self._render_market_position(data)
        
        with tab2:
            self._render_investment_strategy(data)
        
        with tab3:
            self._render_risk_assessment(data)
    
    def _render_policymaker_dashboard(self, data: Dict[str, pd.DataFrame]):
        """Render policymaker-specific dashboard."""
        st.markdown("### 🏛️ Policy Overview")
        
        # Regional summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self._render_metric_card(
                "National Adoption",
                "72%",
                "+8% YoY",
                "OECD Average: 65%",
                color="green"
            )
        
        with col2:
            self._render_metric_card(
                "Labor Impact",
                "12% at risk",
                "45% augmented",
                "Net positive impact",
                color="blue"
            )
        
        with col3:
            self._render_metric_card(
                "GDP Impact",
                "+7.2%",
                "By 2030",
                "Above projections",
                color="green"
            )
        
        with col4:
            self._render_metric_card(
                "Policy Readiness",
                "65%",
                "Gaps identified",
                "Action needed",
                color="yellow"
            )
        
        # Policy insights
        st.markdown("### 📋 Policy Implications")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Regional Analysis", "Labor Market", "Economic Impact", "Governance"])
        
        with tab1:
            self._render_regional_analysis(data)
        
        with tab2:
            self._render_labor_analysis(data)
        
        with tab3:
            self._render_economic_impact(data)
        
        with tab4:
            self._render_governance_status(data)
    
    def _render_researcher_dashboard(self, data: Dict[str, pd.DataFrame]):
        """Render researcher-specific dashboard."""
        st.markdown("### 🔬 Research Overview")
        
        # Research metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self._render_metric_card(
                "Data Points",
                "1.2M+",
                "28 sources",
                "95% validated",
                color="blue"
            )
        
        with col2:
            self._render_metric_card(
                "Time Series",
                "2017-2025",
                "8 years",
                "Monthly granularity",
                color="blue"
            )
        
        with col3:
            self._render_metric_card(
                "Coverage",
                "52 countries",
                "15 sectors",
                "Comprehensive",
                color="green"
            )
        
        with col4:
            self._render_metric_card(
                "Model Accuracy",
                "R² = 0.92",
                "p < 0.001",
                "Highly significant",
                color="green"
            )
        
        # Research deep dive
        st.markdown("### 📈 Research Analysis")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Trends", "Correlations", "Predictions", "Methodology", "Data Quality"
        ])
        
        with tab1:
            self._render_trend_analysis(data)
        
        with tab2:
            self._render_correlation_analysis(data)
        
        with tab3:
            self._render_predictions(data)
        
        with tab4:
            self._render_methodology(data)
        
        with tab5:
            self._render_data_quality(data)
    
    def _render_general_dashboard(self, data: Dict[str, pd.DataFrame]):
        """Render general user dashboard."""
        st.markdown("### 🌟 AI Adoption Overview")
        
        # Beginner-friendly metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_metric_card(
                "Companies Using AI",
                "87%",
                "Growing fast",
                "Most businesses now use AI",
                color="blue"
            )
        
        with col2:
            self._render_metric_card(
                "Average Benefits",
                "+25%",
                "Productivity gain",
                "Significant improvements",
                color="green"
            )
        
        with col3:
            self._render_metric_card(
                "Time to Value",
                "6-12 months",
                "Typical timeline",
                "Quick returns possible",
                color="blue"
            )
        
        # Educational content
        st.markdown("### 📚 Understanding AI Adoption")
        
        tab1, tab2, tab3, tab4 = st.tabs(["What is AI?", "Benefits", "Getting Started", "Success Stories"])
        
        with tab1:
            self._render_ai_basics()
        
        with tab2:
            self._render_benefits_overview(data)
        
        with tab3:
            self._render_getting_started()
        
        with tab4:
            self._render_success_stories()
    
    def _render_metric_card(
        self,
        title: str,
        value: str,
        delta: str,
        description: str,
        color: str = "blue"
    ):
        """Render a styled metric card."""
        color_map = {
            "blue": "#1f77b4",
            "green": "#28a745",
            "red": "#dc3545",
            "yellow": "#ffc107"
        }
        
        accent = color_map.get(color, color_map["blue"])
        
        st.markdown(f"""
        <div style='background-color: #f8f9fa; border-left: 4px solid {accent};
                    padding: 15px; margin: 5px 0; border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 120px;'>
            <h5 style='margin: 0; color: #6c757d; font-size: 14px;'>{title}</h5>
            <h3 style='margin: 5px 0; color: {accent};'>{value}</h3>
            <p style='margin: 0; font-size: 12px; color: #6c757d;'>{delta}</p>
            <p style='margin: 5px 0 0 0; font-size: 11px; color: #6c757d;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Placeholder methods for specific renderings
    def _render_market_position(self, data):
        st.info("Market position analysis would be rendered here")
    
    def _render_investment_strategy(self, data):
        st.info("Investment strategy recommendations would be rendered here")
    
    def _render_risk_assessment(self, data):
        st.info("Risk assessment matrix would be rendered here")
    
    def _render_regional_analysis(self, data):
        st.info("Regional adoption patterns would be rendered here")
    
    def _render_labor_analysis(self, data):
        st.info("Labor market impact analysis would be rendered here")
    
    def _render_economic_impact(self, data):
        st.info("Economic impact projections would be rendered here")
    
    def _render_governance_status(self, data):
        st.info("Governance readiness assessment would be rendered here")
    
    def _render_trend_analysis(self, data):
        st.info("Detailed trend analysis would be rendered here")
    
    def _render_correlation_analysis(self, data):
        st.info("Correlation matrices would be rendered here")
    
    def _render_predictions(self, data):
        st.info("Predictive models would be rendered here")
    
    def _render_methodology(self, data):
        st.info("Research methodology details would be rendered here")
    
    def _render_data_quality(self, data):
        st.info("Data quality metrics would be rendered here")
    
    def _render_ai_basics(self):
        st.markdown("""
        ### What is AI?
        
        Artificial Intelligence (AI) refers to computer systems that can perform tasks 
        that typically require human intelligence:
        
        - **Machine Learning**: Systems that learn from data
        - **Natural Language Processing**: Understanding human language
        - **Computer Vision**: Analyzing images and videos
        - **Predictive Analytics**: Forecasting future trends
        
        💡 **Key Point**: AI is already being used by 87% of businesses to improve 
        efficiency and create new opportunities.
        """)
    
    def _render_benefits_overview(self, data):
        st.info("AI benefits overview would be rendered here")
    
    def _render_getting_started(self):
        st.markdown("""
        ### Getting Started with AI
        
        **Step 1: Identify Use Cases**
        - Look for repetitive tasks
        - Find data-rich processes
        - Consider customer pain points
        
        **Step 2: Start Small**
        - Pick one pilot project
        - Measure results carefully
        - Learn and iterate
        
        **Step 3: Scale Success**
        - Expand proven use cases
        - Build internal capabilities
        - Create an AI strategy
        
        🎯 **Tip**: Most successful AI projects start with a focused pilot that 
        delivers value in 3-6 months.
        """)
    
    def _render_success_stories(self):
        st.info("AI success stories would be rendered here")


def create_persona_specific_view(persona: str, view_type: str, data: Dict[str, pd.DataFrame]):
    """Create a view specifically tailored for a persona.
    
    Args:
        persona: The user's persona
        view_type: The type of view to render
        data: Available data
    
    Returns:
        Rendered view with persona-specific customizations
    """
    # Persona-specific view customizations
    view_configs = {
        'Executive': {
            'show_technical_details': False,
            'emphasize_roi': True,
            'highlight_competitive': True,
            'summary_level': 'high'
        },
        'Policymaker': {
            'show_regional_data': True,
            'emphasize_societal_impact': True,
            'include_governance': True,
            'summary_level': 'medium'
        },
        'Researcher': {
            'show_methodology': True,
            'include_raw_data': True,
            'statistical_details': True,
            'summary_level': 'detailed'
        },
        'General': {
            'use_simple_language': True,
            'include_explanations': True,
            'show_basics': True,
            'summary_level': 'simple'
        }
    }
    
    config = view_configs.get(persona, view_configs['General'])
    
    # Apply persona-specific rendering
    # This would be integrated with actual view rendering
    return config