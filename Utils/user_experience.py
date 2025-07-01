"""
User Experience Enhancement Module for AI Adoption Dashboard
Provides user-centric design patterns and persona-driven experiences
"""

import streamlit as st
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class UserPersona(Enum):
    EXECUTIVE = "Executive"
    POLICYMAKER = "Policymaker"
    RESEARCHER = "Researcher"
    GENERAL = "General"

class ViewType(Enum):
    DASHBOARD = "Dashboard"
    ANALYSIS = "Analysis"
    REPORT = "Report"
    INTERACTIVE = "Interactive"

@dataclass
class PersonaPreferences:
    """User persona preferences and customizations"""
    persona: UserPersona
    preferred_views: List[str]
    key_metrics: List[str]
    chart_preferences: Dict[str, str]
    detail_level: str  # "Summary", "Detailed", "Expert"
    update_frequency: str
    export_formats: List[str]

@dataclass
class UserSession:
    """User session management"""
    session_id: str
    persona: UserPersona
    preferences: PersonaPreferences
    visited_views: List[str]
    bookmarks: List[str]
    custom_filters: Dict[str, Any]

class UserExperienceManager:
    """Manages user-centric design and persona-driven experiences"""
    
    def __init__(self):
        self.persona_configs = self._load_persona_configurations()
        self.user_sessions = {}
    
    def initialize_user_session(self, persona: UserPersona) -> UserSession:
        """Initialize user session with persona-specific preferences"""
        
        session_id = st.session_state.get('session_id', 'default')
        preferences = self.get_persona_preferences(persona)
        
        session = UserSession(
            session_id=session_id,
            persona=persona,
            preferences=preferences,
            visited_views=[],
            bookmarks=[],
            custom_filters={}
        )
        
        self.user_sessions[session_id] = session
        return session
    
    def get_persona_preferences(self, persona: UserPersona) -> PersonaPreferences:
        """Get default preferences for a persona"""
        
        persona_configs = {
            UserPersona.EXECUTIVE: PersonaPreferences(
                persona=persona,
                preferred_views=[
                    "Strategic Overview",
                    "Competitive Position", 
                    "Investment Decision",
                    "ROI Analysis",
                    "Market Intelligence"
                ],
                key_metrics=[
                    "Market Adoption Rate",
                    "Expected ROI",
                    "Competitive Position",
                    "Investment Required",
                    "Implementation Timeline"
                ],
                chart_preferences={
                    "style": "executive",
                    "complexity": "simplified",
                    "color_scheme": "professional",
                    "annotations": "key_insights_only"
                },
                detail_level="Summary",
                update_frequency="Weekly",
                export_formats=["PDF", "PowerPoint", "Executive Summary"]
            ),
            
            UserPersona.POLICYMAKER: PersonaPreferences(
                persona=persona,
                preferred_views=[
                    "Geographic Distribution",
                    "Regulatory Impact",
                    "Sector Analysis",
                    "Public vs Private Adoption",
                    "Policy Recommendations"
                ],
                key_metrics=[
                    "Geographic Coverage",
                    "Sector Penetration",
                    "Regulatory Compliance",
                    "Public Sector Adoption",
                    "Economic Impact"
                ],
                chart_preferences={
                    "style": "analytical",
                    "complexity": "detailed",
                    "color_scheme": "governmental",
                    "annotations": "comprehensive"
                },
                detail_level="Detailed",
                update_frequency="Monthly",
                export_formats=["PDF", "Excel", "Policy Brief"]
            ),
            
            UserPersona.RESEARCHER: PersonaPreferences(
                persona=persona,
                preferred_views=[
                    "Data Deep Dive",
                    "Statistical Analysis",
                    "Trend Forecasting",
                    "Methodology Details",
                    "Data Sources"
                ],
                key_metrics=[
                    "Statistical Significance",
                    "Data Quality Score",
                    "Confidence Intervals",
                    "Sample Sizes",
                    "Methodology Validation"
                ],
                chart_preferences={
                    "style": "scientific",
                    "complexity": "expert",
                    "color_scheme": "academic",
                    "annotations": "statistical_notes"
                },
                detail_level="Expert",
                update_frequency="Real-time",
                export_formats=["CSV", "JSON", "Research Paper", "Jupyter Notebook"]
            ),
            
            UserPersona.GENERAL: PersonaPreferences(
                persona=persona,
                preferred_views=[
                    "AI Basics",
                    "Industry Overview",
                    "Getting Started",
                    "Success Stories",
                    "Educational Resources"
                ],
                key_metrics=[
                    "Adoption Trends",
                    "Industry Examples",
                    "Implementation Steps",
                    "Success Rate",
                    "Learning Resources"
                ],
                chart_preferences={
                    "style": "accessible",
                    "complexity": "basic",
                    "color_scheme": "friendly",
                    "annotations": "explanatory"
                },
                detail_level="Summary",
                update_frequency="Monthly",
                export_formats=["PDF", "Infographic", "Guide"]
            )
        }
        
        return persona_configs.get(persona, persona_configs[UserPersona.GENERAL])
    
    def create_persona_landing_page(self, persona: UserPersona) -> None:
        """Create persona-specific landing page"""
        
        preferences = self.get_persona_preferences(persona)
        
        # Header with persona context
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%); 
                    padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>
                🎯 {persona.value} Dashboard
            </h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
                {self._get_persona_description(persona)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick metrics overview
        self._render_persona_metrics(preferences)
        
        # Recommended views
        self._render_recommended_views(preferences)
        
        # Personalized insights
        self._render_personalized_insights(persona)
    
    def render_adaptive_sidebar(self, persona: UserPersona) -> None:
        """Render persona-adaptive sidebar"""
        
        preferences = self.get_persona_preferences(persona)
        
        with st.sidebar:
            st.markdown(f"### 👤 {persona.value} View")
            
            # Quick actions for persona
            st.markdown("#### Quick Actions")
            for view in preferences.preferred_views[:3]:
                if st.button(f"📊 {view}", key=f"quick_{view}"):
                    st.session_state.selected_view = view
            
            # Personalized filters
            st.markdown("#### Personalized Filters")
            self._render_persona_filters(persona)
            
            # Export options
            st.markdown("#### Export Options")
            export_format = st.selectbox(
                "Format", 
                preferences.export_formats,
                key=f"export_{persona.value}"
            )
            
            if st.button("📥 Export"):
                self._handle_export(persona, export_format)
    
    def create_contextual_help(self, view_name: str, persona: UserPersona) -> None:
        """Create contextual help based on view and persona"""
        
        help_content = self._get_contextual_help_content(view_name, persona)
        
        if help_content:
            with st.expander("❓ Help & Context", expanded=False):
                st.markdown(help_content)
    
    def render_progress_indicator(self, persona: UserPersona) -> None:
        """Render progress indicator for user journey"""
        
        preferences = self.get_persona_preferences(persona)
        session = self.user_sessions.get(st.session_state.get('session_id', 'default'))
        
        if session:
            visited_views = session.visited_views
            total_views = len(preferences.preferred_views)
            progress = len(visited_views) / total_views if total_views > 0 else 0
            
            st.markdown("#### 📈 Your Progress")
            st.progress(progress)
            st.caption(f"Explored {len(visited_views)} of {total_views} recommended views")
    
    def create_personalized_recommendations(self, persona: UserPersona) -> List[str]:
        """Generate personalized recommendations"""
        
        session = self.user_sessions.get(st.session_state.get('session_id', 'default'))
        preferences = self.get_persona_preferences(persona)
        
        recommendations = []
        
        if session:
            unvisited_views = [v for v in preferences.preferred_views if v not in session.visited_views]
            
            if unvisited_views:
                recommendations.append(f"Explore {unvisited_views[0]} for comprehensive insights")
            
            # Persona-specific recommendations
            if persona == UserPersona.EXECUTIVE:
                recommendations.extend([
                    "Review competitive position for strategic planning",
                    "Analyze ROI projections for budget allocation",
                    "Monitor market trends for timing decisions"
                ])
            elif persona == UserPersona.POLICYMAKER:
                recommendations.extend([
                    "Examine geographic disparities for policy targeting",
                    "Review sector-specific adoption for regulation planning",
                    "Analyze public vs private sector gaps"
                ])
            elif persona == UserPersona.RESEARCHER:
                recommendations.extend([
                    "Validate statistical models and assumptions",
                    "Explore data quality and methodology details",
                    "Review confidence intervals and significance tests"
                ])
            else:  # GENERAL
                recommendations.extend([
                    "Start with industry overview for context",
                    "Review success stories for inspiration",
                    "Explore educational resources for learning"
                ])
        
        return recommendations[:5]  # Limit to top 5
    
    def track_user_interaction(self, interaction_type: str, details: Dict[str, Any]) -> None:
        """Track user interactions for experience optimization"""
        
        session_id = st.session_state.get('session_id', 'default')
        session = self.user_sessions.get(session_id)
        
        if session:
            # Update visited views
            if interaction_type == "view_visited":
                view_name = details.get('view_name')
                if view_name and view_name not in session.visited_views:
                    session.visited_views.append(view_name)
            
            # Update bookmarks
            elif interaction_type == "bookmark_added":
                bookmark = details.get('bookmark')
                if bookmark and bookmark not in session.bookmarks:
                    session.bookmarks.append(bookmark)
            
            # Update filters
            elif interaction_type == "filter_applied":
                session.custom_filters.update(details.get('filters', {}))
    
    def _render_persona_metrics(self, preferences: PersonaPreferences) -> None:
        """Render persona-specific key metrics"""
        
        cols = st.columns(len(preferences.key_metrics[:4]))
        
        # Sample metrics (would be populated with real data)
        sample_metrics = {
            "Market Adoption Rate": ("78%", "+5pp", "success"),
            "Expected ROI": ("3.2x", "+0.4x", "success"),
            "Competitive Position": ("Strong", "Improving", "info"),
            "Investment Required": ("$500K", "Within budget", "info"),
            "Geographic Coverage": ("85%", "Expanding", "success"),
            "Statistical Significance": ("p<0.01", "High confidence", "success")
        }
        
        for i, metric in enumerate(preferences.key_metrics[:4]):
            with cols[i]:
                value, delta, color = sample_metrics.get(metric, ("N/A", "", "info"))
                st.metric(
                    label=metric,
                    value=value,
                    delta=delta
                )
    
    def _render_recommended_views(self, preferences: PersonaPreferences) -> None:
        """Render recommended views for persona"""
        
        st.markdown("### 🎯 Recommended for You")
        
        cols = st.columns(3)
        
        for i, view in enumerate(preferences.preferred_views[:6]):
            with cols[i % 3]:
                if st.button(
                    f"📊 {view}",
                    key=f"rec_view_{view}",
                    help=f"Explore {view} tailored for {preferences.persona.value}"
                ):
                    st.session_state.selected_view = view
                    self.track_user_interaction("view_visited", {"view_name": view})
    
    def _render_personalized_insights(self, persona: UserPersona) -> None:
        """Render personalized insights"""
        
        insights = {
            UserPersona.EXECUTIVE: [
                "🎯 Technology sector shows 92% adoption rate - consider industry partnerships",
                "💰 Average ROI of 4.2x justifies increased AI investment budget",
                "⚡ GenAI adoption at 71% - opportunity for competitive advantage"
            ],
            UserPersona.POLICYMAKER: [
                "🌍 Geographic disparities show rural areas lagging by 25%",
                "🏛️ Government adoption at 52% - policy interventions needed",
                "📊 Public-private gap of 15% requires targeted initiatives"
            ],
            UserPersona.RESEARCHER: [
                "📈 95% confidence intervals show robust trend predictions",
                "🔬 Statistical significance (p<0.01) validates adoption patterns",
                "📊 Sample sizes exceed requirements for reliable inference"
            ],
            UserPersona.GENERAL: [
                "🚀 AI adoption has grown 78% in 2024 - mainstream technology",
                "💡 Most organizations start with operational efficiency use cases",
                "📚 Training and skills development are key success factors"
            ]
        }
        
        st.markdown("### 💡 Insights for You")
        for insight in insights.get(persona, [])[:3]:
            st.info(insight)
    
    def _render_persona_filters(self, persona: UserPersona) -> None:
        """Render persona-specific filters"""
        
        if persona == UserPersona.EXECUTIVE:
            st.selectbox("Industry Focus", ["All", "Technology", "Financial Services", "Healthcare"])
            st.selectbox("Time Horizon", ["Current", "1 Year", "3 Years", "5 Years"])
            
        elif persona == UserPersona.POLICYMAKER:
            st.selectbox("Geographic Scope", ["Global", "National", "Regional", "Local"])
            st.selectbox("Sector Type", ["All", "Public", "Private", "Non-Profit"])
            
        elif persona == UserPersona.RESEARCHER:
            st.selectbox("Data Quality", ["All", "High Quality Only", "Validated Only"])
            st.selectbox("Methodology", ["All", "Survey", "Administrative", "Mixed"])
            
        else:  # GENERAL
            st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
            st.selectbox("Industry Interest", ["All", "My Industry", "Similar Industries"])
    
    def _get_persona_description(self, persona: UserPersona) -> str:
        """Get description for persona"""
        
        descriptions = {
            UserPersona.EXECUTIVE: "Strategic insights and ROI analysis for C-level decision making",
            UserPersona.POLICYMAKER: "Geographic and sector analysis for policy development and regulation",
            UserPersona.RESEARCHER: "Detailed data analysis and statistical validation for research purposes",
            UserPersona.GENERAL: "Accessible AI adoption insights and educational resources"
        }
        
        return descriptions.get(persona, "AI adoption insights tailored to your needs")
    
    def _get_contextual_help_content(self, view_name: str, persona: UserPersona) -> str:
        """Get contextual help content"""
        
        base_help = {
            "Competitive Position": "This analysis compares your organization's AI maturity against industry benchmarks...",
            "Investment Decision": "Evaluate AI investment opportunities with comprehensive ROI analysis...",
            "Market Intelligence": "Track market trends and competitive landscape developments...",
            "Geographic Distribution": "Analyze AI adoption patterns across different regions and countries..."
        }
        
        persona_context = {
            UserPersona.EXECUTIVE: " Focus on strategic implications and business impact.",
            UserPersona.POLICYMAKER: " Consider regulatory and policy development opportunities.",
            UserPersona.RESEARCHER: " Review methodology and statistical validation details.",
            UserPersona.GENERAL: " This provides an accessible overview of key concepts."
        }
        
        base = base_help.get(view_name, "This view provides AI adoption insights.")
        context = persona_context.get(persona, "")
        
        return base + context
    
    def _handle_export(self, persona: UserPersona, format: str) -> None:
        """Handle export functionality"""
        
        st.success(f"Export prepared in {format} format for {persona.value} users")
        # In a real implementation, this would generate the actual export
    
    def _load_persona_configurations(self) -> Dict:
        """Load persona-specific configurations"""
        
        return {
            "executive": {"theme": "corporate", "detail_level": "summary"},
            "policymaker": {"theme": "governmental", "detail_level": "detailed"},
            "researcher": {"theme": "academic", "detail_level": "expert"},
            "general": {"theme": "accessible", "detail_level": "basic"}
        }

# Global user experience manager instance
ux_manager = UserExperienceManager()

# Export functions
__all__ = [
    'UserPersona',
    'ViewType',
    'PersonaPreferences',
    'UserSession',
    'UserExperienceManager',
    'ux_manager'
]