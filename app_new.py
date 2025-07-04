"""
The Economics of AI Dashboard - Main Application
===============================================

This dashboard provides comprehensive insights into AI adoption trends and economic impact.
Integrates all Phase 1-5 components with backward compatibility.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio
import time
from typing import Dict, Any, Optional

# Import optimized components
from data.optimized_data_manager import create_optimized_manager
from components.competitive_assessor import CompetitivePositionAssessor
from components.accessibility import AccessibilityManager, create_accessible_dashboard_layout
from components.progressive_disclosure import ProgressiveDisclosure
from components.economic_insights import EconomicInsights
from components.persona_dashboards import PersonaDashboards
from components.guided_tour import GuidedTour
from components.key_takeaways import KeyTakeawaysGenerator
from components.mobile_responsive import MobileResponsive
from components.view_enhancements import ViewEnhancer
from components.lazy_loading import LazyLoadContainer, LazyChart, LazyDataFrame
from performance.monitor import track_performance, get_metrics, log_performance_report
from performance.cache_manager import get_cache

# Page configuration
st.set_page_config(
    page_title="The Economics of AI Dashboard | 2018-2025 Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        'About': "# The Economics of AI Dashboard\nVersion 3.0.0\n\nTrack AI adoption trends and economic impact across industries and geographies.\n\nCreated by Robert Casanova"
    }
)

# Initialize accessibility features
a11y_manager = create_accessible_dashboard_layout()

# Initialize session state
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "Executive"
if 'show_changelog' not in st.session_state:
    st.session_state.show_changelog = False
if 'year_filter' not in st.session_state:
    st.session_state.year_filter = None
if 'compare_years' not in st.session_state:
    st.session_state.compare_years = False
if 'disclosure_level' not in st.session_state:
    st.session_state.disclosure_level = 'standard'
if 'data_manager' not in st.session_state:
    with st.spinner("Initializing data systems..."):
        st.session_state.data_manager = create_optimized_manager()
if 'tour_completed' not in st.session_state:
    st.session_state.tour_completed = False

# Initialize components
data_manager = st.session_state.data_manager
assessor = CompetitivePositionAssessor()
disclosure = ProgressiveDisclosure()
insights = EconomicInsights()
personas = PersonaDashboards()
tour = GuidedTour()
takeaways = KeyTakeawaysGenerator()
mobile = MobileResponsive()
enhancer = ViewEnhancer()

@track_performance('page_load', threshold=3.0)
def main():
    """Main application entry point."""
    
    # Check if showing competitive assessment (new homepage)
    if st.session_state.first_visit and not st.session_state.tour_completed:
        show_competitive_assessment()
        return
    
    # Show guided tour for new users
    if not st.session_state.tour_completed:
        tour.start_tour()
        if st.button("Skip Tour", key="skip_tour"):
            st.session_state.tour_completed = True
            st.rerun()
        return
    
    # Main dashboard layout
    render_dashboard()

def show_competitive_assessment():
    """Show competitive position assessment as homepage."""
    st.title("🏆 The Economics of AI Dashboard")
    st.markdown("### Where does your organization stand in the AI revolution?")
    
    # Quick assessment
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Quick Assessment")
        
        industry = st.selectbox(
            "Your Industry",
            ["Technology", "Financial Services", "Healthcare", "Manufacturing", 
             "Retail & E-commerce", "Education", "Energy & Utilities", "Government"]
        )
        
        company_size = st.selectbox(
            "Company Size",
            ["< 50 employees", "50-249", "250-999", "1,000-4,999", "5,000+"]
        )
        
        ai_usage = st.select_slider(
            "Current AI Adoption Level",
            options=["None", "Exploring", "Piloting", "Limited Production", "Scaled Production"],
            value="Exploring"
        )
        
        if st.button("Get Your Position", type="primary", key="assess"):
            # Map inputs to assessment data
            assessment_data = {
                'company': {
                    'industry': industry,
                    'size': company_size,
                    'ai_maturity': ai_usage
                }
            }
            
            # Get all data for assessment
            all_data = data_manager.get_all_data()
            
            # Render full assessment
            assessor.render_full_assessment(all_data, assessment_data)
            
            # Option to continue to dashboard
            if st.button("Continue to Full Dashboard", type="primary"):
                st.session_state.first_visit = False
                st.session_state.tour_completed = True
                st.rerun()
    
    with col2:
        st.info("""
        **Why This Matters:**
        
        💰 **7% GDP Growth** potential by 2030
        
        📈 **280x Cost Reduction** in AI inference
        
        🏃 **$4.4 Trillion** annual productivity gains
        
        ⚡ **18 months** - Average time for competitors to match AI innovations
        """)
        
        st.warning("""
        **Cost of Inaction:**
        
        Companies delaying AI adoption risk:
        - 15-20% competitive disadvantage
        - $1M+ annual opportunity cost
        - Permanent market share loss
        """)

def render_dashboard():
    """Render main dashboard interface."""
    
    # Apply mobile responsive layout
    is_mobile = mobile.detect_device() == 'mobile'
    
    # Progressive disclosure level selector
    disclosure.render_level_selector()
    
    # Title and description
    st.title("💰 The Economics of AI Dashboard: 2018-2025")
    st.markdown("**Comprehensive analysis of AI's economic impact and adoption trends**")
    
    # What's New section
    with st.expander("🆕 What's New in Version 3.0.0", expanded=st.session_state.show_changelog):
        st.markdown("""
        **Major Updates:**
        - 🏆 New competitive position assessment
        - 📊 Modular data architecture with 12+ authoritative sources
        - 💡 Economic insights and cost of inaction calculator
        - 🎯 Persona-specific dashboards
        - ♿ WCAG 2.1 AA accessibility compliance
        - 🚀 Multi-layer caching for sub-3s load times
        - 📱 Mobile-responsive design
        """)
    
    # Load data with performance tracking
    with track_performance('data_load'):
        all_data = data_manager.get_all_data()
    
    # Sidebar controls
    setup_sidebar()
    
    # Get current view
    view_type = st.session_state.get('view_type', 'Executive Summary')
    
    # Render selected view
    if view_type == "Executive Summary":
        render_executive_summary(all_data)
    elif view_type == "Competitive Position":
        assessor.render_full_assessment(all_data)
    elif view_type in ["Historical Trends", "Industry Analysis", "Investment Trends"]:
        render_standard_view(view_type, all_data)
    else:
        # Persona-specific views
        if st.session_state.selected_persona == "Executive":
            personas.render_executive_dashboard(all_data)
        elif st.session_state.selected_persona == "Policymaker":
            personas.render_policymaker_dashboard(all_data)
        elif st.session_state.selected_persona == "Researcher":
            personas.render_researcher_dashboard(all_data)
        else:
            personas.render_general_dashboard(all_data)
    
    # Key takeaways
    if st.session_state.disclosure_level != 'executive':
        takeaways_data = takeaways.generate_takeaways(view_type, all_data)
        takeaways.render_takeaways(takeaways_data)
    
    # Performance monitoring
    if st.sidebar.button("📊 Performance Report"):
        log_performance_report()
        with st.expander("Performance Metrics", expanded=True):
            metrics = get_metrics()
            stats = metrics.get_summary()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Load Time", f"{stats.get('data_load', {}).get('mean', 0):.2f}s")
            with col2:
                st.metric("Cache Hit Rate", f"{get_cache().get_stats()['memory']['hit_rate']:.0%}")
            with col3:
                st.metric("Total Operations", stats.get('total_operations', 0))

def setup_sidebar():
    """Setup sidebar controls."""
    st.sidebar.header("📊 Dashboard Controls")
    
    # Persona selection
    persona = st.sidebar.selectbox(
        "Select Your Role",
        ["Executive", "Policymaker", "Researcher", "General"],
        index=["Executive", "Policymaker", "Researcher", "General"].index(st.session_state.selected_persona)
    )
    st.session_state.selected_persona = persona
    
    # View selection based on persona
    persona_views = {
        "Executive": ["Executive Summary", "Competitive Position", "Financial Impact", "ROI Analysis"],
        "Policymaker": ["Policy Overview", "Geographic Distribution", "Regional Growth", "AI Governance"],
        "Researcher": ["Research Insights", "Historical Trends", "Productivity Research", "Environmental Impact"],
        "General": ["Overview", "Adoption Rates", "Investment Trends", "Labor Impact"]
    }
    
    st.sidebar.info(f"💡 **Recommended for {persona}:**\n" + "\n".join([f"• {v}" for v in persona_views[persona][:3]]))
    
    # All available views
    all_views = ["Executive Summary", "Competitive Position", "Historical Trends", 
                 "Industry Analysis", "Investment Trends", "Regional Growth", 
                 "Financial Impact", "Labor Impact", "Firm Size Analysis", 
                 "Technology Stack", "AI Technology Maturity", "Productivity Research", 
                 "Environmental Impact", "Geographic Distribution", "AI Governance",
                 "Barriers & Support", "ROI Analysis", "Skill Gap Analysis"]
    
    view_type = st.sidebar.selectbox(
        "Analysis View", 
        all_views,
        index=0
    )
    st.session_state.view_type = view_type
    
    # Data controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Data Options")
    
    data_year = st.sidebar.selectbox(
        "Focus Period", 
        ["2025 (Current)", "2018-2025 (Full Range)", "2018 (Historical)"],
        index=0
    )
    st.session_state.data_year = data_year
    
    # Export options
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Options")
    
    if st.sidebar.button("📊 Export Current View"):
        # Implementation would export current view data
        st.sidebar.success("Export functionality coming soon!")
    
    # Help and feedback
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤝 Help & Feedback")
    
    if st.sidebar.button("📚 View Documentation"):
        st.sidebar.info("Documentation available at: https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki")
    
    if st.sidebar.button("💬 Send Feedback"):
        st.sidebar.info("Feedback form coming soon!")

def render_executive_summary(data: Dict[str, pd.DataFrame]):
    """Render executive summary view."""
    st.header("📊 Executive Summary")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Global AI Adoption",
            "78%",
            "+23% YoY",
            help="Percentage of companies using AI in production"
        )
    
    with col2:
        st.metric(
            "Economic Impact",
            "$4.4T",
            "Annual productivity gains",
            help="McKinsey estimate for global productivity impact"
        )
    
    with col3:
        st.metric(
            "Cost Reduction",
            "280x",
            "Since 2022",
            help="Reduction in AI inference costs"
        )
    
    with col4:
        st.metric(
            "Investment",
            "$252B",
            "+44% in 2024",
            help="Global AI investment in 2024"
        )
    
    # Economic insights
    st.markdown("### 💡 Key Economic Insights")
    
    insights_container = LazyLoadContainer(
        lambda: insights.render_executive_summary(data),
        placeholder_text="Loading economic insights..."
    )
    insights_container.render()
    
    # What-if scenarios
    if st.session_state.disclosure_level in ['standard', 'detailed']:
        st.markdown("### 🔮 What-If Scenarios")
        
        scenario_type = st.selectbox(
            "Select Scenario",
            ["Accelerated Adoption", "Delayed Adoption", "Selective Adoption"]
        )
        
        scenario_data = insights.generate_what_if_scenario(
            data,
            scenario_type,
            {'timeline': 3, 'adoption_rate': 0.8}
        )
        
        insights.render_what_if_scenario(scenario_data)

def render_standard_view(view_type: str, data: Dict[str, pd.DataFrame]):
    """Render standard analysis views with enhancements."""
    st.header(f"📈 {view_type}")
    
    # Add view enhancement
    enhancement = enhancer.enhance_view(view_type, data)
    
    if enhancement:
        st.info(enhancement['insight'])
        
        if 'executive_summary' in enhancement:
            with st.expander("Executive Summary", expanded=True):
                st.markdown(enhancement['executive_summary'])
    
    # Render view-specific content
    if view_type == "Historical Trends":
        render_historical_trends(data)
    elif view_type == "Industry Analysis":
        render_industry_analysis(data)
    elif view_type == "Investment Trends":
        render_investment_trends(data)
    # Add more view implementations as needed

def render_historical_trends(data: Dict[str, pd.DataFrame]):
    """Render historical trends view."""
    # Get historical data
    hist_data = data.get('historical_trends', pd.DataFrame())
    
    if hist_data.empty:
        st.warning("Historical data not available")
        return
    
    # Create trend chart
    fig = px.line(
        hist_data,
        x='year',
        y=['ai_use', 'genai_use'],
        title="AI Adoption Trends 2017-2025",
        labels={'value': 'Adoption Rate (%)', 'year': 'Year'},
        height=500
    )
    
    fig.update_layout(
        hovermode='x unified',
        legend=dict(title="Technology Type"),
        xaxis=dict(tickmode='linear', dtick=1)
    )
    
    # Use lazy loading for chart
    chart_container = LazyChart(lambda: fig)
    chart_container.render()
    
    # Additional insights
    if st.session_state.disclosure_level == 'detailed':
        st.markdown("### 📊 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Growth Metrics:**")
            cagr = ((hist_data['ai_use'].iloc[-1] / hist_data['ai_use'].iloc[0]) ** (1/8) - 1) * 100
            st.metric("AI Adoption CAGR", f"{cagr:.1f}%")
            
        with col2:
            st.markdown("**Acceleration Points:**")
            st.write("- 2023: GenAI breakthrough")
            st.write("- 2024: Enterprise adoption surge")

def render_industry_analysis(data: Dict[str, pd.DataFrame]):
    """Render industry analysis view."""
    industry_data = data.get('industry_analysis', pd.DataFrame())
    
    if industry_data.empty:
        st.warning("Industry data not available")
        return
    
    # Industry adoption chart
    fig = px.bar(
        industry_data.head(10),
        x='adoption_rate',
        y='sector',
        orientation='h',
        title="AI Adoption by Industry (2025)",
        labels={'adoption_rate': 'Adoption Rate (%)', 'sector': 'Industry'},
        color='adoption_rate',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=600, showlegend=False)
    
    # Lazy load chart
    LazyChart(lambda: fig).render()
    
    # ROI comparison
    if st.session_state.disclosure_level in ['standard', 'detailed']:
        st.markdown("### 💰 ROI by Industry")
        
        roi_fig = px.scatter(
            industry_data,
            x='adoption_rate',
            y='avg_roi',
            size='genai_adoption',
            color='sector',
            title="Adoption Rate vs ROI by Industry",
            labels={'avg_roi': 'Average ROI (x)', 'adoption_rate': 'Adoption Rate (%)'}
        )
        
        LazyChart(lambda: roi_fig).render()

def render_investment_trends(data: Dict[str, pd.DataFrame]):
    """Render investment trends view."""
    investment_data = data.get('investment_trends', pd.DataFrame())
    
    if investment_data.empty:
        st.warning("Investment data not available")
        return
    
    # Investment over time
    fig = px.area(
        investment_data,
        x='year',
        y=['total_investment', 'genai_investment'],
        title="Global AI Investment Trends",
        labels={'value': 'Investment ($B)', 'year': 'Year'},
        height=500
    )
    
    fig.update_layout(
        hovermode='x unified',
        legend=dict(title="Investment Type")
    )
    
    LazyChart(lambda: fig).render()
    
    # Regional breakdown
    if 'us_investment' in investment_data.columns:
        st.markdown("### 🌍 Regional Investment Distribution")
        
        regional_fig = px.bar(
            investment_data,
            x='year',
            y=['us_investment', 'china_investment', 'uk_investment'],
            title="AI Investment by Region",
            labels={'value': 'Investment ($B)', 'year': 'Year'},
            barmode='stack'
        )
        
        LazyChart(lambda: regional_fig).render()

# Run the application
if __name__ == "__main__":
    main()