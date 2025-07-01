#!/usr/bin/env python3
"""
AI Adoption Dashboard - Minimal Test Version for Option C
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="AI Adoption Dashboard",
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "General"
if 'strategic_view_selection' not in st.session_state:
    st.session_state.strategic_view_selection = None

# Sample data for testing
def load_sample_data():
    """Load sample data for testing"""
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [5, 8, 12, 18, 25, 33, 45, 58, 72],
        'genai_use': [0, 0, 1, 2, 5, 15, 35, 52, 68]
    })
    
    industry_data = pd.DataFrame({
        'industry': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing'],
        'adoption_rate': [85, 72, 65, 58],
        'investment': [2500, 1800, 1200, 900]
    })
    
    return historical_data, industry_data

historical_data, industry_data = load_sample_data()

# Basic persona landing page (Option C: Only Executive + General)
if st.session_state.first_visit:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #1f77b4; font-size: 3rem; margin-bottom: 0.5rem;">🤖 AI Strategic Intelligence Center</h1>
        <p style="font-size: 1.3rem; color: #666; margin-bottom: 2rem;">Transform AI data into competitive advantage</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0; color: white; text-align: center;">
        <h2 style="margin-bottom: 1rem; color: white;">Choose Your Strategic Dashboard</h2>
        <p style="opacity: 0.9; font-size: 1.1rem;">Get personalized insights tailored to your role and decision-making needs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Available personas for MVP testing (Option C)
    col1, col2 = st.columns(2)
    
    with col1:
        # Executive Card - FULLY IMPLEMENTED
        if st.button("📊 Executive Dashboard", key="exec_card", help="Strategic insights for C-level decision makers", use_container_width=True):
            st.session_state.selected_persona = "Executive"
            st.session_state.first_visit = False
            st.rerun()
        
        st.markdown("""
        <div style="border: 2px solid #1f77b4; border-radius: 15px; padding: 1.5rem; margin: 0.5rem 0; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                <h4 style="color: #1f77b4; margin-bottom: 0.5rem;">Executive Dashboard</h4>
                <p style="color: #555; margin-bottom: 0.5rem; font-size: 0.9rem;">Strategic insights for C-level decision makers</p>
                <div style="text-align: left; background: rgba(255,255,255,0.7); padding: 0.8rem; border-radius: 8px; font-size: 0.85rem;">
                    <strong>Your Strategic Views:</strong><br>
                    • Competitive Position Analysis<br>
                    • Investment Decision Engine<br>
                    • Market Intelligence Center<br>
                    • Strategic Action Planning<br>
                    • ROI & Financial Impact
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # General User Card - FULLY IMPLEMENTED
        if st.button("👤 General Explorer", key="general_card", help="Comprehensive access to all analytics and insights", use_container_width=True):
            st.session_state.selected_persona = "General"
            st.session_state.first_visit = False
            st.rerun()
            
        st.markdown("""
        <div style="border: 2px solid #9467bd; border-radius: 15px; padding: 1.5rem; margin: 0.5rem 0; 
                    background: linear-gradient(135deg, #e6e6fa 0%, #d8bfd8 100%);">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👤</div>
                <h4 style="color: #6b46a3; margin-bottom: 0.5rem;">General Explorer</h4>
                <p style="color: #555; margin-bottom: 0.5rem; font-size: 0.9rem;">Comprehensive access to all analytics and insights</p>
                <div style="text-align: left; background: rgba(255,255,255,0.7); padding: 0.8rem; border-radius: 8px; font-size: 0.85rem;">
                    <strong>Full Access Includes:</strong><br>
                    • All strategic dashboards<br>
                    • Complete analysis library<br>
                    • Advanced filtering options<br>
                    • Export capabilities<br>
                    • Custom view creation
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Coming Soon section
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: rgba(255,193,7,0.1); border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: #856404; margin-bottom: 1rem;">🚧 Additional Personas Coming Soon</h4>
        <div style="display: flex; justify-content: center; gap: 2rem;">
            <div style="opacity: 0.7;">
                <div style="font-size: 2rem;">🏛️</div>
                <p style="margin: 0.5rem 0 0 0; color: #856404;"><strong>Policymaker</strong><br><small>Command Center</small></p>
            </div>
            <div style="opacity: 0.7;">
                <div style="font-size: 2rem;">🔬</div>
                <p style="margin: 0.5rem 0 0 0; color: #856404;"><strong>Researcher</strong><br><small>Analytics Hub</small></p>
            </div>
        </div>
        <p style="color: #856404; margin-top: 1rem; font-size: 0.9rem;">These personas will be available after comprehensive testing is complete</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0; padding: 1rem; 
                background: rgba(31, 119, 180, 0.1); border-radius: 10px;">
        <p style="color: #1f77b4; font-weight: bold;">💡 Click any button above to access your personalized dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Only stop if user hasn't made a selection
    if not st.session_state.get('selected_persona'):
        st.stop()

# Main Dashboard
st.title("🤖 AI Adoption Dashboard: Strategic Decision Intelligence")
st.markdown("**From data analysis to competitive advantage - make better AI investment decisions**")

# Current persona display
current_persona = st.session_state.get('selected_persona', 'General')
st.sidebar.markdown(f"## Current Role: {current_persona}")

# Basic navigation
if current_persona == "Executive":
    # Executive Strategic Command Center
    view_options = ["🎯 Strategic Command Center", "📊 Market Intelligence", "💰 Investment Analysis", "⚖️ Competitive Position"]
else:
    # General Explorer
    view_options = ["Historical Trends", "Industry Analysis", "Geographic Distribution", "ROI Analysis"]

current_view = st.sidebar.selectbox("Select Analysis View", view_options)

# Display current view
st.subheader(f"📊 {current_view}")

if current_view == "🎯 Strategic Command Center":
    # Executive Command Center
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0; color: white;">
        <h1 style="margin: 0; color: white; text-align: center;">💼 Executive Strategic Command Center</h1>
        <p style="margin: 0.5rem 0 0 0; text-align: center; opacity: 0.9;">Strategic insights for C-level decision making</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Market Position", "Top 25%", "+5% vs competition")
    with col2:
        st.metric("💰 ROI Potential", "4.2x", "+15% vs baseline")
    with col3:
        st.metric("⚡ Implementation Speed", "8.5/10", "Fast Track")
    with col4:
        st.metric("🎯 Competitive Advantage", "High", "Strategic Priority")

elif current_view == "Historical Trends" or current_view == "📊 Market Intelligence":
    # Historical trends chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['ai_use'], 
        mode='lines+markers',
        name='Overall AI Use',
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['genai_use'], 
        mode='lines+markers',
        name='GenAI Use',
        line=dict(width=4, color='#ff7f0e'),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="AI Adoption Trends: 2017-2025",
        xaxis_title="Year",
        yaxis_title="Adoption Rate (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

elif current_view == "Industry Analysis":
    # Industry analysis chart
    fig = px.bar(
        industry_data, 
        x='industry', 
        y='adoption_rate',
        title="AI Adoption by Industry",
        color='adoption_rate',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

else:
    # Default view
    st.info(f"📊 {current_view} view is available. Sample data and visualizations are displayed.")
    st.dataframe(historical_data, use_container_width=True)

# Test status
st.sidebar.markdown("---")
st.sidebar.success("✅ Option C Implementation Active")
st.sidebar.info("🚧 Full dashboard testing in progress")

# Export functionality
if current_view:
    csv = historical_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Sample Data",
        data=csv,
        file_name=f"{current_view.replace(' ', '_')}.csv",
        mime="text/csv"
    )