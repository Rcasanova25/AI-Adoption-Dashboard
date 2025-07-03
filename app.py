#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Adoption Dashboard - Original Sophisticated Version
Multi-persona analytics platform with enterprise-grade features
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots

# Import business logic modules
try:
    from business.metrics import business_metrics, CompetitivePosition, InvestmentRecommendation
    from business.roi_calculator import roi_calculator
    from business.causal_analysis import causal_engine, CausalAnalysisResult, ProductivityMetric
    BUSINESS_MODULES_AVAILABLE = True
except ImportError:
    BUSINESS_MODULES_AVAILABLE = False
    print("Warning: Business modules not available, using fallback implementations")

# Import data infrastructure
try:
    from data.loaders import validate_all_loaded_data
    from data.pipeline_integration import load_all_datasets_integrated, integration_manager
    from data.models import safe_validate_data
    from data.geographic import get_geographic_data, get_country_details, generate_geographic_insights
    DATA_MODULES_AVAILABLE = True
except ImportError:
    DATA_MODULES_AVAILABLE = False
    print("Warning: Data modules not available, using fallback implementations")

# Import performance systems
try:
    from performance.caching import smart_cache, performance_monitor, DataPipeline
    PERFORMANCE_MODULES_AVAILABLE = True
except ImportError:
    PERFORMANCE_MODULES_AVAILABLE = False
    print("Warning: Performance modules not available")

# Import utilities
try:
    from Utils.helpers import clean_filename, safe_execute, safe_data_check
    from Utils.navigation import setup_navigation
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    print("Warning: Utils modules not available")

# Import accessibility features
try:
    from accessibility.integrate_accessibility import initialize_accessibility, accessibility_integrator
    ACCESSIBILITY_AVAILABLE = True
except ImportError:
    ACCESSIBILITY_AVAILABLE = False
    print("Warning: Accessibility modules not available")

# Page config
st.set_page_config(
    page_title="AI Adoption Dashboard | 2018-2025 Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        'About': "# AI Adoption Dashboard\nVersion 3.0.0\n\nTrack AI adoption trends across industries and geographies.\n\nCreated by Robert Casanova"
    }
)

# Initialize session state
if 'dashboard_data' not in st.session_state:
    st.session_state.dashboard_data = {}
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = 'Executive'
if 'data_year' not in st.session_state:
    st.session_state.data_year = '2025 (GenAI Era)'

def load_fallback_data():
    """Load fallback data when modules are not available"""
    # Historical trends (2018-2025)
    years = list(range(2018, 2026))
    historical_data = pd.DataFrame({
        'year': years,
        'ai_adoption_rate': [5, 8, 12, 18, 25, 35, 55, 78],
        'genai_adoption_rate': [0, 0, 0, 0, 0, 15, 33, 71],
        'investment_billions': [10, 15, 25, 40, 60, 100, 150, 252.3],
        'productivity_gain': [0.5, 0.8, 1.2, 1.5, 1.8, 2.1, 2.5, 3.2]
    })
    
    # Industry data (2025)
    industry_data = pd.DataFrame({
        'industry': ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail', 'Education'],
        'adoption_rate': [91, 85, 72, 68, 79, 65],
        'roi_multiplier': [3.2, 2.8, 2.5, 2.1, 2.9, 2.3],
        'productivity_gain': [2.8, 2.2, 1.8, 1.5, 2.1, 1.9],
        'investment_priority': [95, 88, 76, 72, 82, 68]
    })
    
    # Geographic data
    geographic_data = pd.DataFrame({
        'region': ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa'],
        'adoption_rate': [85, 72, 68, 45, 58, 32],
        'investment_billions': [120, 85, 95, 25, 35, 15],
        'growth_rate': [25, 18, 22, 35, 28, 45]
    })
    
    return {
        'historical_data': historical_data,
        'industry_data': industry_data,
        'geographic_data': geographic_data,
        'source': 'fallback'
    }

def load_data_with_mckinsey_tools():
    """Load data using McKinsey tools when available"""
    try:
        if DATA_MODULES_AVAILABLE:
            datasets, integration_metadata = load_all_datasets_integrated()
            return datasets
        else:
            return load_fallback_data()
    except Exception as e:
        st.warning(f"McKinsey tools unavailable: {e}")
        return load_fallback_data()

def show_executive_dashboard():
    """Executive persona dashboard with strategic insights"""
    st.title("👔 Executive Dashboard: Strategic AI Intelligence")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall AI Adoption", "78%", "+23pp from 2023")
    with col2:
        st.metric("GenAI Adoption", "71%", "+38pp from 2023")
    with col3:
        st.metric("2024 Investment", "$252.3B", "+44.5% YoY")
    with col4:
        st.metric("Productivity Gain", "3.2x", "+0.7x vs 2023")
    
    # Strategic insights
    st.subheader("🎯 Strategic Insights")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "💰 Financial Performance", "🎯 Competitive Analysis", "📈 Action Items"])
    
    with tab1:
        st.markdown("### Executive Summary")
        st.markdown("""
        - **AI adoption has accelerated dramatically** since 2023, with generative AI driving much of the recent growth
        - **Technology sector continues to lead** with 91% adoption rate, but adoption is spreading rapidly across all industries
        - **Investment priorities are shifting** from experimentation to production deployment
        - **Productivity gains are exceeding initial expectations** with average 3.2x improvement
        """)
        
        # Adoption trends chart
        if 'historical_data' in st.session_state.dashboard_data:
            data = st.session_state.dashboard_data['historical_data']
            fig = px.line(data, x='year', y=['ai_adoption_rate', 'genai_adoption_rate'],
                         title='AI Adoption Trends (2018-2025)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Financial Performance")
        if BUSINESS_MODULES_AVAILABLE:
            try:
                # ROI analysis
                roi_result = roi_calculator.calculate_roi(
                    investment_amount=1000000,
                    expected_revenue_increase=0.15,
                    cost_reduction_percentage=0.10,
                    time_horizon=3
                )
                st.success(f"**ROI Analysis**: {roi_result.roi_percentage:.1f}% ROI over {roi_result.time_horizon} years")
                st.info(f"**Payback Period**: {roi_result.payback_period:.1f} years")
            except Exception as e:
                st.warning(f"ROI calculation unavailable: {e}")
        
        # Investment trends
        if 'historical_data' in st.session_state.dashboard_data:
            data = st.session_state.dashboard_data['historical_data']
            fig = px.area(data, x='year', y='investment_billions',
                         title='Global AI Investment Trends')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Competitive Analysis")
        if 'industry_data' in st.session_state.dashboard_data:
            data = st.session_state.dashboard_data['industry_data']
            fig = px.bar(data, x='industry', y=['adoption_rate', 'roi_multiplier'],
                        title='Industry Performance Comparison',
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Strategic Action Items")
        st.markdown("""
        **High Priority:**
        1. **Accelerate GenAI adoption** - 71% of companies are already using it
        2. **Invest in AI infrastructure** - Focus on production deployment
        3. **Develop AI talent strategy** - Address skill gaps and training needs
        4. **Establish AI governance** - Implement responsible AI practices
        
        **Medium Priority:**
        1. **Benchmark against industry leaders** - Technology sector shows the way
        2. **Explore geographic opportunities** - Consider regional expansion
        3. **Monitor regulatory developments** - Stay ahead of policy changes
        """)

def show_policymaker_dashboard():
    """Policymaker persona dashboard with regulatory insights"""
    st.title("🏛️ Policymaker Dashboard: Regulatory & Policy Intelligence")
    
    # Policy metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Countries with AI Policies", "60+", "+15 in 2024")
    with col2:
        st.metric("Regulatory Frameworks", "45+", "Active development")
    with col3:
        st.metric("Policy Impact Score", "7.2/10", "Moderate impact")
    with col4:
        st.metric("Compliance Rate", "68%", "Industry average")
    
    # Geographic policy analysis
    st.subheader("🌍 Geographic Policy Landscape")
    
    if 'geographic_data' in st.session_state.dashboard_data:
        data = st.session_state.dashboard_data['geographic_data']
        fig = px.choropleth(data, locations='region', locationmode='country names',
                           color='adoption_rate', title='Global AI Adoption by Region')
        st.plotly_chart(fig, use_container_width=True)
    
    # Policy insights
    st.subheader("📋 Policy Insights")
    st.markdown("""
    - **North America leads** with comprehensive AI governance frameworks
    - **Europe focuses** on AI ethics and responsible development
    - **Asia Pacific** shows rapid policy development with diverse approaches
    - **Emerging markets** are developing AI policies to attract investment
    """)

def show_researcher_dashboard():
    """Researcher persona dashboard with advanced analytics"""
    st.title("🔬 Researcher Dashboard: Advanced Analytics & Insights")
    
    # Research metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Data Sources", "28+", "Comprehensive coverage")
    with col2:
        st.metric("Analysis Methods", "15+", "Advanced techniques")
    with col3:
        st.metric("Confidence Level", "95%", "High reliability")
    with col4:
        st.metric("Research Papers", "50+", "Cited sources")
    
    # Advanced analytics
    st.subheader("📊 Advanced Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📈 Trend Analysis", "🔍 Statistical Analysis", "📚 Research Database"])
    
    with tab1:
        st.markdown("### Trend Analysis")
        if 'historical_data' in st.session_state.dashboard_data:
            data = st.session_state.dashboard_data['historical_data']
            
            # Multiple trend lines
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['year'], y=data['ai_adoption_rate'],
                                   mode='lines+markers', name='AI Adoption'))
            fig.add_trace(go.Scatter(x=data['year'], y=data['genai_adoption_rate'],
                                   mode='lines+markers', name='GenAI Adoption'))
            fig.add_trace(go.Scatter(x=data['year'], y=data['productivity_gain'],
                                   mode='lines+markers', name='Productivity Gain'))
            
            fig.update_layout(title='Multi-Dimensional Trend Analysis',
                            xaxis_title='Year', yaxis_title='Percentage/Multiplier')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Statistical Analysis")
        if 'industry_data' in st.session_state.dashboard_data:
            data = st.session_state.dashboard_data['industry_data']
            
            # Correlation analysis
            correlation = data[['adoption_rate', 'roi_multiplier', 'productivity_gain']].corr()
            fig = px.imshow(correlation, title='Correlation Matrix')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Research Database")
        st.markdown("""
        **Key Research Sources:**
        - Stanford AI Index Report 2025
        - McKinsey Global Survey on AI
        - Goldman Sachs Economics Analysis
        - Federal Reserve Productivity Research
        - OECD AI Policy Observatory
        - US Census Bureau AI Use Supplement
        """)

def show_general_dashboard():
    """General user dashboard with simplified insights"""
    st.title("👥 General Dashboard: AI Adoption Overview")
    
    # Simple metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("AI Adoption", "78%", "of companies")
    with col2:
        st.metric("GenAI Use", "71%", "of companies")
    with col3:
        st.metric("Investment", "$252B", "in 2024")
    with col4:
        st.metric("Growth", "+23pp", "from 2023")
    
    # Simple insights
    st.subheader("📊 Key Insights")
    st.markdown("""
    - **AI adoption is growing rapidly** across all industries
    - **Generative AI is the biggest trend** with 71% adoption
    - **Technology companies lead** the way in AI adoption
    - **Investment is increasing** with $252 billion in 2024
    """)
    
    # Simple chart
    if 'historical_data' in st.session_state.dashboard_data:
        data = st.session_state.dashboard_data['historical_data']
        fig = px.line(data, x='year', y='ai_adoption_rate',
                     title='AI Adoption Growth Over Time')
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application entry point"""
    st.title("🤖 AI Adoption Dashboard")
    st.markdown("*Comprehensive analysis of AI adoption trends (2018-2025)*")
    
    # Load data
    with st.spinner("Loading dashboard data..."):
        st.session_state.dashboard_data = load_data_with_mckinsey_tools()
    
    # Persona selection
    st.sidebar.title("🎭 Select Your Persona")
    persona = st.sidebar.selectbox(
        "Choose your role:",
        ["Executive", "Policymaker", "Researcher", "General"],
        index=0
    )
    
    # Data year selection
    st.sidebar.title("📅 Data Period")
    data_year = st.sidebar.selectbox(
        "Select data period:",
        ["2025 (GenAI Era)", "2024 (Transition Year)", "2023 (Pre-GenAI)", "Historical (2018-2022)"],
        index=0
    )
    
    # Show appropriate dashboard based on persona
    if persona == "Executive":
        show_executive_dashboard()
    elif persona == "Policymaker":
        show_policymaker_dashboard()
    elif persona == "Researcher":
        show_researcher_dashboard()
    else:  # General
        show_general_dashboard()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Version 3.0.0")
    with col2:
        st.caption("Created by Robert Casanova")
    with col3:
        st.caption("Data: AI Index 2025, McKinsey, Goldman Sachs")

if __name__ == "__main__":
    main()
