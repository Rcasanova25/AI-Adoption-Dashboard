import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="AI Adoption Dashboard | 2018-2025 Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        'About': "# AI Adoption Dashboard\nVersion 2.2.0\n\nTrack AI adoption trends across industries and geographies.\n\nCreated by Robert Casanova"
    }
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Data loading function - updated with AI Index 2025 data
@st.cache_data
def load_data():
    # Historical trends data - UPDATED with AI Index 2025 findings
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],  # Updated: 78% in 2024
        'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]  # Updated: 71% in 2024
    })
    
    # 2018 Sector data
    sector_2018 = pd.DataFrame({
        'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                  'Finance & Insurance', 'Retail Trade', 'Construction'],
        'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
        'employment_weighted': [18, 22, 15, 14, 12, 8, 6]
    })
    
    # 2025 Sector data - NEW for industry-specific insights
    sector_2025 = pd.DataFrame({
        'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                  'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
        'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
    })
    
    # Firm size data
    firm_size = pd.DataFrame({
        'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                '500-999', '1000-2499', '2500-4999', '5000+'],
        'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5]
    })
    
    # AI Maturity data
    ai_maturity = pd.DataFrame({
        'technology': ['Generative AI', 'AI Agents', 'Foundation Models', 'ModelOps', 
                      'AI Engineering', 'Cloud AI Services', 'Knowledge Graphs', 'Composite AI'],
        'adoption_rate': [71, 15, 45, 25, 30, 78, 35, 12],
        'maturity': ['Peak of Expectations', 'Peak of Expectations', 'Trough of Disillusionment',
                    'Trough of Disillusionment', 'Peak of Expectations', 'Slope of Enlightenment',
                    'Slope of Enlightenment', 'Peak of Expectations'],
        'risk_score': [85, 90, 60, 55, 80, 25, 40, 95],
        'time_to_value': [3, 3, 3, 3, 3, 1, 3, 7]
    })
    
    # Geographic data - enhanced with population and GDP
    geographic = pd.DataFrame({
        'city': ['San Francisco Bay Area', 'Nashville', 'San Antonio', 'Las Vegas', 
                'New Orleans', 'San Diego', 'Seattle', 'Boston', 'Los Angeles',
                'Phoenix', 'Denver', 'Austin', 'Portland', 'Miami', 'Atlanta',
                'Chicago', 'New York', 'Philadelphia', 'Dallas', 'Houston'],
        'state': ['California', 'Tennessee', 'Texas', 'Nevada', 
                 'Louisiana', 'California', 'Washington', 'Massachusetts', 'California',
                 'Arizona', 'Colorado', 'Texas', 'Oregon', 'Florida', 'Georgia',
                 'Illinois', 'New York', 'Pennsylvania', 'Texas', 'Texas'],
        'lat': [37.7749, 36.1627, 29.4241, 36.1699, 
               29.9511, 32.7157, 47.6062, 42.3601, 34.0522,
               33.4484, 39.7392, 30.2672, 45.5152, 25.7617, 33.7490,
               41.8781, 40.7128, 39.9526, 32.7767, 29.7604],
        'lon': [-122.4194, -86.7816, -98.4936, -115.1398, 
               -90.0715, -117.1611, -122.3321, -71.0589, -118.2437,
               -112.0740, -104.9903, -97.7431, -122.6784, -80.1918, -84.3880,
               -87.6298, -74.0060, -75.1652, -96.7970, -95.3698],
        'rate': [9.5, 8.3, 8.3, 7.7, 
                7.4, 7.4, 6.8, 6.7, 7.2,
                6.5, 6.3, 7.8, 6.2, 6.9, 7.1,
                7.0, 8.0, 6.6, 7.5, 7.3],
        'state_code': ['CA', 'TN', 'TX', 'NV', 
                      'LA', 'CA', 'WA', 'MA', 'CA',
                      'AZ', 'CO', 'TX', 'OR', 'FL', 'GA',
                      'IL', 'NY', 'PA', 'TX', 'TX'],
        'population_millions': [7.7, 0.7, 1.5, 0.6, 
                               0.4, 1.4, 0.8, 0.7, 4.0,
                               1.7, 0.7, 1.0, 0.7, 0.5, 0.5,
                               2.7, 8.3, 1.6, 1.3, 2.3],
        'gdp_billions': [535, 48, 98, 68, 
                        25, 253, 392, 463, 860,
                        162, 201, 148, 121, 345, 396,
                        610, 1487, 388, 368, 356]
    })
    
    # State-level aggregation
    state_data = geographic.groupby(['state', 'state_code']).agg({
        'rate': 'mean'
    }).reset_index()
    
    # Add more states
    additional_states = pd.DataFrame({
        'state': ['Michigan', 'Ohio', 'North Carolina', 'Virginia', 'Maryland',
                 'Connecticut', 'New Jersey', 'Indiana', 'Missouri', 'Wisconsin'],
        'state_code': ['MI', 'OH', 'NC', 'VA', 'MD', 'CT', 'NJ', 'IN', 'MO', 'WI'],
        'rate': [5.5, 5.8, 6.0, 6.2, 6.4, 6.8, 6.9, 5.2, 5.4, 5.3]
    })
    state_data = pd.concat([state_data, additional_states], ignore_index=True)
    
    # Technology stack
    tech_stack = pd.DataFrame({
        'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
        'percentage': [15, 45, 38, 62]
    })
    
    # Productivity data with skill levels - ENHANCED
    productivity_data = pd.DataFrame({
        'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
        'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
    })
    
    # AI productivity by skill level - NEW
    productivity_by_skill = pd.DataFrame({
        'skill_level': ['Low-skilled', 'Medium-skilled', 'High-skilled'],
        'productivity_gain': [14, 9, 5],
        'skill_gap_reduction': [28, 18, 8]
    })
    
    # AI productivity estimates
    ai_productivity_estimates = pd.DataFrame({
        'source': ['Acemoglu (2024)', 'Brynjolfsson et al. (2023)', 'McKinsey (potential)', 'Goldman Sachs (potential)', 'Richmond Fed'],
        'annual_impact': [0.07, 1.5, 2.0, 2.5, 0.1]
    })
    
    # OECD 2025 Report data
    oecd_g7_adoption = pd.DataFrame({
        'country': ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Japan'],
        'adoption_rate': [45, 38, 42, 40, 35, 32, 48],
        'manufacturing': [52, 45, 48, 55, 42, 40, 58],
        'ict_sector': [68, 62, 65, 63, 58, 55, 70]
    })
    
    # OECD AI Applications - ENHANCED with GenAI use cases
    oecd_applications = pd.DataFrame({
        'application': ['Content Generation', 'Code Generation', 'Customer Service Chatbots',
                       'Predictive Maintenance', 'Process Automation', 'Customer Analytics', 
                       'Quality Control', 'Supply Chain Optimization', 'Fraud Detection',
                       'Product Recommendation', 'Voice Recognition', 'Computer Vision',
                       'Natural Language Processing', 'Robotics Integration', 'Personalized Learning'],
        'usage_rate': [65, 58, 52, 45, 42, 38, 35, 32, 30, 28, 25, 23, 22, 18, 15],
        'category': ['GenAI', 'GenAI', 'GenAI', 'Traditional AI', 'Traditional AI', 
                    'Traditional AI', 'Traditional AI', 'Traditional AI', 'Traditional AI',
                    'Traditional AI', 'Traditional AI', 'Traditional AI', 'Traditional AI', 
                    'Traditional AI', 'GenAI']
    })
    
    # Barriers to AI Adoption
    barriers_data = pd.DataFrame({
        'barrier': ['Lack of skilled personnel', 'Data availability/quality', 'Integration with legacy systems',
                   'Regulatory uncertainty', 'High implementation costs', 'Security concerns',
                   'Unclear ROI', 'Organizational resistance'],
        'percentage': [68, 62, 58, 55, 52, 48, 45, 40]
    })
    
    # Support effectiveness
    support_effectiveness = pd.DataFrame({
        'support_type': ['Government education investment', 'University partnerships', 
                        'Public-private collaboration', 'Regulatory clarity',
                        'Tax incentives', 'Innovation grants', 'Technology centers'],
        'effectiveness_score': [82, 78, 75, 73, 68, 65, 62]
    })
    
    # NEW: AI Investment data from AI Index 2025
    ai_investment_data = pd.DataFrame({
        'year': [2014, 2020, 2021, 2022, 2023, 2024],
        'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
        'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
        'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
        'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
        'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
    })
    
    # NEW: Regional AI adoption growth from AI Index 2025
    regional_growth = pd.DataFrame({
        'region': ['Greater China', 'Europe', 'North America', 'Asia-Pacific', 'Latin America'],
        'growth_2024': [27, 23, 15, 18, 12],
        'adoption_rate': [68, 65, 82, 58, 45],
        'investment_growth': [32, 28, 44, 25, 18]
    })
    
    # NEW: AI cost reduction data from AI Index 2025
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
        'cost_per_million_tokens': [20.00, 0.14, 0.07],
        'year': [2022, 2024, 2024]
    })
    
    # CORRECTED: Financial impact by function from AI Index 2025
    # These percentages represent the % of companies reporting ANY financial benefit
    # The actual magnitude is typically <10% cost savings and <5% revenue gains
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],  # % of companies
        'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],  # % of companies
        'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],  # Actual % reduction for those who see benefits
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]  # Actual % increase for those who see benefits
    })
    
    # NEW: Generational AI perception data from AI Index 2025
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
        'expect_job_change': [67, 65, 58, 49],
        'expect_job_replacement': [42, 40, 34, 28]
    })
    
    # NEW: Training emissions data from AI Index 2025
    training_emissions = pd.DataFrame({
        'model': ['AlexNet (2012)', 'GPT-3 (2020)', 'GPT-4 (2023)', 'Llama 3.1 405B (2024)'],
        'carbon_tons': [0.01, 588, 5184, 8930]
    })
    
    # NEW: Skill gap data
    skill_gap_data = pd.DataFrame({
        'skill': ['AI/ML Engineering', 'Data Science', 'AI Ethics', 'Prompt Engineering',
                 'AI Product Management', 'MLOps', 'AI Security', 'Change Management'],
        'gap_severity': [85, 78, 72, 68, 65, 62, 58, 55],
        'training_initiatives': [45, 52, 28, 38, 32, 35, 22, 48]
    })
    
    # NEW: AI governance data
    ai_governance = pd.DataFrame({
        'aspect': ['Ethics Guidelines', 'Data Privacy', 'Bias Detection', 'Transparency',
                  'Accountability Framework', 'Risk Assessment', 'Regulatory Compliance'],
        'adoption_rate': [62, 78, 45, 52, 48, 55, 72],
        'maturity_score': [3.2, 3.8, 2.5, 2.8, 2.6, 3.0, 3.5]  # Out of 5
    })
    
    return (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
            geographic, tech_stack, productivity_data, productivity_by_skill,
            ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
            barriers_data, support_effectiveness, state_data, ai_investment_data, 
            regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
            training_emissions, skill_gap_data, ai_governance)

# Initialize session state
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "General"
if 'show_changelog' not in st.session_state:
    st.session_state.show_changelog = False
if 'year_filter' not in st.session_state:
    st.session_state.year_filter = None
if 'compare_years' not in st.session_state:
    st.session_state.compare_years = False

# Helper function for source info
def show_source_info(source_key):
    sources = {
        'ai_index': {
            'title': 'AI Index Report 2025',
            'org': 'Stanford HAI',
            'url': 'https://aiindex.stanford.edu',
            'methodology': 'Comprehensive analysis of AI metrics globally'
        },
        'mckinsey': {
            'title': 'McKinsey Global Survey on AI',
            'org': 'McKinsey & Company',
            'url': 'https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai',
            'methodology': '1,491 participants across 101 nations, July 2024'
        },
        'oecd': {
            'title': 'OECD/BCG/INSEAD Report 2025',
            'org': 'OECD AI Policy Observatory',
            'url': 'https://oecd.ai',
            'methodology': '840 enterprises across G7 countries + Brazil'
        },
        'census': {
            'title': 'US Census Bureau AI Use Supplement',
            'org': 'US Census Bureau',
            'url': 'https://www.census.gov',
            'methodology': '850,000 U.S. firms surveyed'
        }
    }
    
    if source_key in sources:
        source = sources[source_key]
        return f"""
        **Source:** {source['title']}  
        **Organization:** {source['org']}  
        **Methodology:** {source['methodology']}  
        [View Report]({source['url']})
        """
    return ""

# Onboarding modal for first-time users
if st.session_state.first_visit:
    with st.container():
        st.info("""
        ### 👋 Welcome to the AI Adoption Dashboard!
        
        This dashboard provides comprehensive insights into AI adoption trends from 2018-2025, 
        including the latest findings from the AI Index Report 2025.
        
        **Quick Start:**
        - Use the sidebar to select different analysis views
        - Click on charts to see detailed information
        - Export any visualization using the download buttons
        
        **For best experience, select your role:**
        """)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Business Leader"):
                st.session_state.selected_persona = "Business Leader"
                st.session_state.first_visit = False
                st.rerun()
        with col2:
            if st.button("🏛️ Policymaker"):
                st.session_state.selected_persona = "Policymaker"
                st.session_state.first_visit = False
                st.rerun()
        with col3:
            if st.button("🔬 Researcher"):
                st.session_state.selected_persona = "Researcher"
                st.session_state.first_visit = False
                st.rerun()
        with col4:
            if st.button("👤 General User"):
                st.session_state.selected_persona = "General"
                st.session_state.first_visit = False
                st.rerun()
        
        if st.button("Got it! Let's explore", type="primary"):
            st.session_state.first_visit = False
            st.rerun()
    st.stop()

# Load data
(historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
 geographic, tech_stack, productivity_data, productivity_by_skill,
 ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
 barriers_data, support_effectiveness, state_data, ai_investment_data, 
 regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
 training_emissions, skill_gap_data, ai_governance) = load_data()

# Header
st.title("🤖 AI Adoption Dashboard: 2018-2025 Analysis")
st.markdown("*Comprehensive insights from AI Index Report 2025, McKinsey, OECD, and more*")

# Quick stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("2024 AI Adoption", "78%", "+23pp YoY")
with col2:
    st.metric("GenAI Adoption", "71%", "+38pp YoY")
with col3:
    st.metric("2024 Investment", "$252.3B", "+44.5%")
with col4:
    st.metric("Cost Reduction", "286x", "Since 2022")

# Sidebar
with st.sidebar:
    st.header("🔧 Dashboard Controls")
    
    # View selector
    view_type = st.selectbox(
        "Select Analysis View",
        ["Historical Trends", "Industry Analysis", "Financial Impact", 
         "Skill Gap Analysis", "AI Governance", "Productivity Research",
         "Investment Trends", "Regional Growth", "AI Cost Trends",
         "Labor Impact", "Environmental Impact", "Adoption Rates",
         "Firm Size Analysis", "Technology Stack", "AI Technology Maturity",
         "Geographic Distribution", "OECD 2025 Findings", "Barriers & Support",
         "ROI Analysis"]
    )
    
    # Year selector for relevant views
    if view_type in ["Historical Trends", "Adoption Rates", "Industry Analysis"]:
        data_year = st.radio(
            "Data Period",
            ["2018 Data", "2025 Data", "Compare Both"],
            help="Select data period for analysis"
        )
    else:
        data_year = "2025 Data"
    
    # Export options
    st.markdown("---")
    st.subheader("📥 Export Options")
    export_format = st.selectbox(
        "Export Format",
        ["CSV", "Excel", "JSON", "PDF Report"]
    )
    
    if st.button("Export Data", type="secondary"):
        st.success("Export functionality would be implemented here")
    
    # Info section
    st.markdown("---")
    st.info("""
    **About This Dashboard**
    
    Version 2.2.0
    Last Updated: June 17, 2025
    
    Data Sources:
    - AI Index Report 2025
    - McKinsey Global Survey
    - OECD AI Observatory
    - US Census Bureau
    """)

# Main content area
if view_type == "Historical Trends":
    st.write("📈 **AI Adoption Historical Trends (2017-2025)**")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overall Trends", "🚀 GenAI Revolution", "📈 Growth Analysis", "🔮 Projections"])
    
    with tab1:
        # Enhanced historical trends visualization
        fig = go.Figure()
        
        # Overall AI adoption
        fig.add_trace(go.Scatter(
            x=historical_data['year'], 
            y=historical_data['ai_use'],
            mode='lines+markers',
            name='Overall AI Adoption',
            line=dict(width=4, color='#1f77b4'),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.1)'
        ))
        
        # GenAI adoption
        fig.add_trace(go.Scatter(
            x=historical_data['year'][historical_data['genai_use'] > 0], 
            y=historical_data['genai_use'][historical_data['genai_use'] > 0],
            mode='lines+markers',
            name='GenAI Adoption',
            line=dict(width=4, color='#ff7f0e', dash='dash'),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(255, 127, 14, 0.1)'
        ))
        
        # Add annotations for key events
        annotations = [
            dict(x=2022, y=33, text="<b>ChatGPT Launch</b>", showarrow=True, arrowhead=2, ax=0, ay=-40),
            dict(x=2024, y=78, text="<b>Record Growth</b><br>+23pp in one year", showarrow=True, arrowhead=2, ax=40, ay=-30)
        ]
        
        fig.update_layout(
            title='AI Adoption Trajectory: The 2024 Acceleration',
            xaxis_title='Year',
            yaxis_title='Adoption Rate (%)',
            height=500,
            hovermode='x unified',
            annotations=annotations,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("2024 Overall AI", "78%", "+23pp from 2023")
        with col2:
            st.metric("2024 GenAI", "71%", "+38pp from 2023")
        with col3:
            st.metric("Growth Rate", "41.8%", "Fastest ever recorded")
    
    with tab2:
        # GenAI deep dive
        st.write("**The GenAI Revolution: From 0% to 71% in 3 Years**")
        
        # Create focused GenAI visualization
        genai_data = historical_data[historical_data['genai_use'] > 0].copy()
        
        fig = go.Figure()
        
        # Add bar chart
        fig.add_trace(go.Bar(
            x=genai_data['year'],
            y=genai_data['genai_use'],
            text=[f'{x}%' for x in genai_data['genai_use']],
            textposition='outside',
            marker_color=['#FFB6C1', '#FF69B4', '#FF1493', '#FF1493'],
            name='GenAI Adoption'
        ))
        
        # Add growth rate line
        growth_rates = [0, 0, 115.2, 0]  # Growth rates
        fig.add_trace(go.Scatter(
            x=genai_data['year'],
            y=growth_rates[:len(genai_data)],
            mode='lines+markers+text',
            name='YoY Growth Rate',
            yaxis='y2',
            line=dict(width=3, color='#2C3E50'),
            text=['', '', '+115%', 'Sustained'],
            textposition='top center'
        ))
        
        fig.update_layout(
            title='GenAI: The Fastest Technology Adoption in History',
            xaxis_title='Year',
            yaxis=dict(title='Adoption Rate (%)', side='left'),
            yaxis2=dict(title='YoY Growth (%)', side='right', overlaying='y', showgrid=False),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Key Insight:** GenAI achieved in 2 years what took traditional AI over a decade")
    
    with tab3:
        # Growth analysis
        st.write("**Adoption Growth Patterns**")
        
        # Calculate year-over-year growth
        historical_data['yoy_growth'] = historical_data['ai_use'].pct_change() * 100
        historical_data['genai_yoy_growth'] = historical_data['genai_use'].pct_change() * 100
        
        # Filter for display
        growth_data = historical_data[historical_data['year'] >= 2018].copy()
        
        fig = go.Figure()
        
        # Growth rate bars
        fig.add_trace(go.Bar(
            x=growth_data['year'],
            y=growth_data['yoy_growth'],
            name='AI YoY Growth',
            marker_color='#3498DB',
            text=[f'{x:.1f}%' if pd.notna(x) else '' for x in growth_data['yoy_growth']],
            textposition='outside'
        ))
        
        # Add average growth line
        avg_growth = growth_data['yoy_growth'].mean()
        fig.add_hline(y=avg_growth, line_dash="dash", line_color="red",
                      annotation_text=f"Average: {avg_growth:.1f}%", annotation_position="right")
        
        fig.update_layout(
            title='Year-over-Year AI Adoption Growth Rate',
            xaxis_title='Year',
            yaxis_title='YoY Growth Rate (%)',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Interactive ROI Calculator
        st.write("**🧮 AI Investment ROI Calculator**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            investment_amount = st.number_input(
                "Initial Investment ($)",
                min_value=10000,
                max_value=10000000,
                value=250000,
                step=10000,
                help="Total AI project investment"
            )
            
            project_type = st.selectbox(
                "Project Type",
                ["Process Automation", "Predictive Analytics", "Customer Service", 
                 "Product Development", "Marketing Optimization"]
            )
            
            company_size = st.select_slider(
                "Company Size",
                options=["Small (<50)", "Medium (50-250)", "Large (250-1000)", "Enterprise (1000+)"],
                value="Medium (50-250)"
            )
        
        with col2:
            implementation_quality = st.slider(
                "Implementation Quality",
                min_value=1,
                max_value=5,
                value=3,
                help="1=Poor, 5=Excellent"
            )
            
            data_readiness = st.slider(
                "Data Readiness",
                min_value=1,
                max_value=5,
                value=3,
                help="1=Poor quality, 5=Excellent quality"
            )
            
            timeline = st.selectbox(
                "Implementation Timeline",
                ["3 months", "6 months", "12 months", "18 months", "24 months"],
                index=2
            )
        
        # Calculate ROI based on inputs
        base_roi = {
            "Process Automation": 3.2,
            "Predictive Analytics": 2.8,
            "Customer Service": 2.5,
            "Product Development": 3.5,
            "Marketing Optimization": 3.0
        }[project_type]
        
        size_multiplier = {
            "Small (<50)": 0.8,
            "Medium (50-250)": 1.0,
            "Large (250-1000)": 1.2,
            "Enterprise (1000+)": 1.4
        }[company_size]
        
        quality_multiplier = 0.6 + (implementation_quality * 0.2)
        data_multiplier = 0.7 + (data_readiness * 0.15)
        
        final_roi = base_roi * size_multiplier * quality_multiplier * data_multiplier
        expected_return = investment_amount * final_roi
        net_benefit = expected_return - investment_amount
        payback_months = int(investment_amount / (net_benefit / int(timeline.split()[0])))
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Projected Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Expected ROI", f"{final_roi:.1f}x", help="Return on investment multiplier")
        with col2:
            st.metric("Total Return", f"${expected_return:,.0f}", help="Total expected value")
        with col3:
            st.metric("Net Benefit", f"${net_benefit:,.0f}", delta=f"{(net_benefit/investment_amount)*100:.0f}%")
        with col4:
            st.metric("Payback Period", f"{payback_months} months", help="Time to recover investment")
        
        # Risk assessment
        risk_score = 5 - ((implementation_quality + data_readiness) / 2)
        risk_level = ["Very Low", "Low", "Medium", "High", "Very High"][int(risk_score)-1]
        
        st.warning(f"""
        **Risk Assessment:** {risk_level}
        - Implementation Quality: {'⭐' * implementation_quality}
        - Data Readiness: {'⭐' * data_readiness}
        - Recommendation: {"Proceed with confidence" if risk_score <= 2 else "Address gaps before proceeding"}
        """)
        
        # Export calculation
        if st.button("📥 Export ROI Analysis"):
            analysis_text = f"""AI ROI Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Investment Details:
- Amount: ${investment_amount:,}
- Project Type: {project_type}
- Company Size: {company_size}
- Timeline: {timeline}

Quality Metrics:
- Implementation Quality: {implementation_quality}/5
- Data Readiness: {data_readiness}/5

Projected Results:
- Expected ROI: {final_roi:.1f}x
- Total Return: ${expected_return:,.0f}
- Net Benefit: ${net_benefit:,.0f}
- Payback Period: {payback_months} months
- Risk Level: {risk_level}
"""
            
            st.download_button(
                label="Download Analysis",
                data=analysis_text,
                file_name=f"ai_roi_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# Complete implementation of all view types for the AI Adoption Dashboard
# This code should be inserted after the "Historical Trends" view implementation

elif view_type == "Industry Analysis":
    st.write("🏭 **AI Adoption by Industry (2025)**")
    
    # Industry comparison
    fig = go.Figure()
    
    # Create grouped bar chart
    fig.add_trace(go.Bar(
        name='Overall AI Adoption',
        x=sector_2025['sector'],
        y=sector_2025['adoption_rate'],
        marker_color='#3498DB',
        text=[f'{x}%' for x in sector_2025['adoption_rate']],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='GenAI Adoption',
        x=sector_2025['sector'],
        y=sector_2025['genai_adoption'],
        marker_color='#E74C3C',
        text=[f'{x}%' for x in sector_2025['genai_adoption']],
        textposition='outside'
    ))
    
    # Add ROI as line chart
    fig.add_trace(go.Scatter(
        name='Average ROI',
        x=sector_2025['sector'],
        y=sector_2025['avg_roi'],
        mode='lines+markers',
        line=dict(width=3, color='#2ECC71'),
        marker=dict(size=10),
        yaxis='y2',
        text=[f'{x}x' for x in sector_2025['avg_roi']],
        textposition='top center'
    ))
    
    fig.update_layout(
        title="AI Adoption and ROI by Industry Sector",
        xaxis_title="Industry",
        yaxis=dict(title="Adoption Rate (%)", side="left"),
        yaxis2=dict(title="Average ROI (x)", side="right", overlaying="y"),
        barmode='group',
        height=500,
        hovermode='x unified',
        xaxis_tickangle=45
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Industry insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Top Adopter", "Technology (92%)", delta="+7% vs Finance")
    with col2:
        st.metric("Highest ROI", "Technology (4.2x)", delta="Best returns")
    with col3:
        st.metric("Fastest Growing", "Healthcare", delta="+15pp YoY")
    
    # Export option
    csv = sector_2025.to_csv(index=False)
    st.download_button(
        label="📥 Download Industry Data (CSV)",
        data=csv,
        file_name="ai_adoption_by_industry_2025.csv",
        mime="text/csv"
    )

elif view_type == "Financial Impact":
    st.write("💵 **Financial Impact of AI by Business Function (AI Index Report 2025)**")
    
    # CORRECTED interpretation box
    st.warning("""
    **📊 Understanding the Data:** 
    - The percentages below show the **proportion of companies reporting financial benefits** from AI
    - Among companies that see benefits, the **actual magnitude** is typically:
      - Cost savings: **Less than 10%** (average 5-10%)
      - Revenue gains: **Less than 5%** (average 2-4%)
    - Example: 71% of companies using AI in Marketing report revenue gains, but these gains average only 4%
    """)
    
    # Create visualization with clearer labels
    fig = go.Figure()
    
    # Sort by revenue gains
    financial_sorted = financial_impact.sort_values('companies_reporting_revenue_gains', ascending=True)
    
    # Add bars showing % of companies reporting benefits
    fig.add_trace(go.Bar(
        name='Companies Reporting Cost Savings',
        y=financial_sorted['function'],
        x=financial_sorted['companies_reporting_cost_savings'],
        orientation='h',
        marker_color='#2ECC71',
        text=[f'{x}%' for x in financial_sorted['companies_reporting_cost_savings']],
        textposition='auto',
        hovertemplate='Function: %{y}<br>Companies reporting savings: %{x}%<br>Avg magnitude: %{customdata}%<extra></extra>',
        customdata=financial_sorted['avg_cost_reduction']
    ))
    
    fig.add_trace(go.Bar(
        name='Companies Reporting Revenue Gains',
        y=financial_sorted['function'],
        x=financial_sorted['companies_reporting_revenue_gains'],
        orientation='h',
        marker_color='#3498DB',
        text=[f'{x}%' for x in financial_sorted['companies_reporting_revenue_gains']],
        textposition='auto',
        hovertemplate='Function: %{y}<br>Companies reporting gains: %{x}%<br>Avg magnitude: %{customdata}%<extra></extra>',
        customdata=financial_sorted['avg_revenue_increase']
    ))
    
    fig.update_layout(
        title="Percentage of Companies Reporting Financial Benefits from AI",
        xaxis_title="Percentage of Companies (%)",
        yaxis_title="Business Function",
        barmode='group',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Function-specific insights with magnitude clarification
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("💰 **Top Functions by Adoption Success:**")
        st.write("• **Service Operations:** 49% report cost savings (avg 8% reduction)")
        st.write("• **Marketing & Sales:** 71% report revenue gains (avg 4% increase)")
        st.write("• **Supply Chain:** 43% report cost savings (avg 9% reduction)")
    
    with col2:
        st.write("📈 **Reality Check:**")
        st.write("• Most benefits are **incremental**, not transformative")
        st.write("• Success varies significantly by implementation quality")
        st.write("• ROI typically takes **12-18 months** to materialize")
    
    # Add source info
    with st.expander("📊 Data Source & Methodology"):
        st.info(show_source_info('ai_index'))

elif view_type == "Skill Gap Analysis":
    st.write("🎓 **AI Skills Gap Analysis**")
    
    # Skills gap visualization
    fig = go.Figure()
    
    # Sort by gap severity
    skill_sorted = skill_gap_data.sort_values('gap_severity', ascending=True)
    
    # Create diverging bar chart
    fig.add_trace(go.Bar(
        name='Gap Severity',
        y=skill_sorted['skill'],
        x=skill_sorted['gap_severity'],
        orientation='h',
        marker_color='#E74C3C',
        text=[f'{x}%' for x in skill_sorted['gap_severity']],
        textposition='outside'
    ))
    
    fig.add_trace(go.Bar(
        name='Training Initiatives',
        y=skill_sorted['skill'],
        x=skill_sorted['training_initiatives'],
        orientation='h',
        marker_color='#2ECC71',
        text=[f'{x}%' for x in skill_sorted['training_initiatives']],
        textposition='outside',
        xaxis='x2'
    ))
    
    fig.update_layout(
        title="AI Skills Gap vs Training Initiatives",
        xaxis=dict(title="Gap Severity (%)", side="bottom"),
        xaxis2=dict(title="Companies with Training (%)", overlaying="x", side="top"),
        yaxis_title="Skill Area",
        height=500,
        barmode='overlay'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.info("""
    **🔍 Key Findings:**
    - **AI/ML Engineering** shows the highest gap severity (85%) with only 45% of companies having training programs
    - **Change Management** has a lower gap (55%) but higher training coverage (48%), showing organizational awareness
    - The gap between severity and training initiatives indicates significant opportunity for workforce development
    """)

elif view_type == "AI Governance":
    st.write("⚖️ **AI Governance & Ethics Implementation**")
    
    # Governance maturity visualization
    fig = go.Figure()
    
    # Create radar chart for maturity
    categories = ai_governance['aspect'].tolist()
    
    fig.add_trace(go.Scatterpolar(
        r=ai_governance['adoption_rate'],
        theta=categories,
        fill='toself',
        name='Adoption Rate (%)',
        line_color='#3498DB'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[x * 20 for x in ai_governance['maturity_score']],  # Scale to 100
        theta=categories,
        fill='toself',
        name='Maturity Score (scaled)',
        line_color='#E74C3C'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="AI Governance Implementation and Maturity",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Governance insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("✅ **Well-Established Areas:**")
        st.write("• **Data Privacy:** 78% adoption, 3.8/5 maturity")
        st.write("• **Regulatory Compliance:** 72% adoption, 3.5/5 maturity")
        st.write("• **Ethics Guidelines:** 62% adoption, 3.2/5 maturity")
    
    with col2:
        st.write("⚠️ **Areas Needing Attention:**")
        st.write("• **Bias Detection:** Only 45% adoption, 2.5/5 maturity")
        st.write("• **Accountability Framework:** 48% adoption, 2.6/5 maturity")
        st.write("• **Transparency:** 52% adoption, 2.8/5 maturity")

elif view_type == "Productivity Research":
    st.write("📊 **AI Productivity Impact Research**")
    
    # Create tabs for different productivity views
    tab1, tab2, tab3 = st.tabs(["Historical Context", "Skill-Level Impact", "Economic Estimates"])
    
    with tab1:
        # Historical productivity paradox
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=productivity_data['year'], 
            y=productivity_data['productivity_growth'],
            mode='lines+markers',
            name='Productivity Growth (%)',
            line=dict(width=3, color='#3B82F6'),
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            x=productivity_data['year'], 
            y=productivity_data['young_workers_share'],
            mode='lines+markers',
            name='Young Workers Share (25-34)',
            line=dict(width=3, color='#EF4444'),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="The Productivity Paradox: Demographics vs Technology",
            xaxis_title="Year",
            yaxis=dict(title="Productivity Growth (%)", side="left"),
            yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        # AI productivity by skill level
        fig = px.bar(
            productivity_by_skill,
            x='skill_level',
            y=['productivity_gain', 'skill_gap_reduction'],
            title='AI Impact by Worker Skill Level',
            labels={'value': 'Percentage (%)', 'variable': 'Impact Type'},
            barmode='group',
            color_discrete_map={'productivity_gain': '#2ECC71', 'skill_gap_reduction': '#3498DB'}
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **✅ AI Index 2025 Finding:** AI provides the greatest productivity boost to low-skilled workers (14%), 
        helping to narrow skill gaps and potentially reduce workplace inequality.
        """)
        
    with tab3:
        # Economic impact estimates
        fig = px.bar(
            ai_productivity_estimates,
            x='source',
            y='annual_impact',
            title='AI Productivity Impact Estimates: Academic vs Industry',
            color='annual_impact',
            color_continuous_scale='RdYlBu_r',
            text='annual_impact'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **📊 Note on Estimates:** 
        - Conservative estimates (0.07-0.1%) focus on task-level automation
        - Optimistic estimates (1.5-2.5%) assume economy-wide transformation
        - Actual impact depends on implementation quality and complementary investments
        """)

elif view_type == "Investment Trends":
    st.write("💰 **AI Investment Trends: Record Growth in 2024 (AI Index Report 2025)**")
    
    # Investment overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="2024 Total Investment", 
            value="$252.3B", 
            delta="+44.5% YoY",
            help="Total corporate AI investment in 2024"
        )
    
    with col2:
        st.metric(
            label="GenAI Investment", 
            value="$33.9B", 
            delta="+18.7% from 2023",
            help="8.5x higher than 2022 levels"
        )
    
    with col3:
        st.metric(
            label="US Investment Lead", 
            value="12x China", 
            delta="$109.1B vs $9.3B",
            help="US leads global AI investment"
        )
    
    with col4:
        st.metric(
            label="Growth Since 2014", 
            value="13x", 
            delta="From $19.4B to $252.3B",
            help="Investment has grown thirteenfold"
        )
    
    # Create tabs for different investment views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overall Trends", "🌍 Geographic Distribution", "🚀 GenAI Focus", "📊 Comparative Analysis"])
    
    with tab1:
        # Total investment trend chart with interactivity
        fig = go.Figure()
        
        # Total investment line
        fig.add_trace(go.Scatter(
            x=ai_investment_data['year'],
            y=ai_investment_data['total_investment'],
            mode='lines+markers',
            name='Total AI Investment',
            line=dict(width=4, color='#2E86AB'),
            marker=dict(size=10),
            text=[f'${x:.1f}B' for x in ai_investment_data['total_investment']],
            textposition='top center',
            hovertemplate='Year: %{x}<br>Total Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>'
        ))
        
        # GenAI investment line
        fig.add_trace(go.Scatter(
            x=ai_investment_data['year'][ai_investment_data['genai_investment'] > 0],
            y=ai_investment_data['genai_investment'][ai_investment_data['genai_investment'] > 0],
            mode='lines+markers',
            name='GenAI Investment',
            line=dict(width=3, color='#F24236'),
            marker=dict(size=8),
            text=[f'${x:.1f}B' for x in ai_investment_data['genai_investment'][ai_investment_data['genai_investment'] > 0]],
            textposition='bottom center',
            hovertemplate='Year: %{x}<br>GenAI Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>'
        ))
        
        # Add annotation for GenAI emergence
        fig.add_annotation(
            x=2022,
            y=3.95,
            text="<b>GenAI Era Begins</b><br>Now 20% of all AI investment",
            showarrow=True,
            arrowhead=2,
            bgcolor="white",
            bordercolor="#F24236",
            borderwidth=2,
            font=dict(size=11, color="#F24236")
        )
        
        fig.update_layout(
            title="AI Investment Has Grown 13x Since 2014",
            xaxis_title="Year",
            yaxis_title="Investment ($ Billions)",
            height=450,
            hovermode='x unified'
        )
        
        col1, col2 = st.columns([10, 1])
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if st.button("📊", key="inv_source", help="View data source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('ai_index'))
        
        st.info("**Key Insight:** Private investment in generative AI now represents over 20% of all AI-related private investment")
        
        # Export option
        csv = ai_investment_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Investment Data (CSV)",
            data=csv,
            file_name="ai_investment_trends_2014_2024.csv",
            mime="text/csv"
        )
    
    with tab2:
        # Country comparison with more context
        countries_extended = pd.DataFrame({
            'country': ['United States', 'China', 'United Kingdom', 'Germany', 'France', 
                       'Canada', 'Israel', 'Japan', 'South Korea', 'India'],
            'investment': [109.1, 9.3, 4.5, 3.2, 2.8, 2.5, 2.2, 2.0, 1.8, 1.5],
            'per_capita': [324.8, 6.6, 66.2, 38.1, 41.2, 65.8, 231.6, 16.0, 34.6, 1.1],
            'pct_of_gdp': [0.43, 0.05, 0.14, 0.08, 0.09, 0.13, 0.48, 0.05, 0.10, 0.04]
        })
        
        # Create subplot with multiple metrics
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Total Investment ($B)', 'Per Capita Investment ($)', '% of GDP'),
            horizontal_spacing=0.12
        )
        
        # Total investment
        fig.add_trace(
            go.Bar(x=countries_extended['country'][:5], y=countries_extended['investment'][:5],
                   marker_color='#3498DB', showlegend=False,
                   text=[f'${x:.1f}B' for x in countries_extended['investment'][:5]],
                   textposition='outside'),
            row=1, col=1
        )
        
        # Per capita
        fig.add_trace(
            go.Bar(x=countries_extended['country'][:5], y=countries_extended['per_capita'][:5],
                   marker_color='#E74C3C', showlegend=False,
                   text=[f'${x:.0f}' for x in countries_extended['per_capita'][:5]],
                   textposition='outside'),
            row=1, col=2
        )
        
        # % of GDP
        fig.add_trace(
            go.Bar(x=countries_extended['country'][:5], y=countries_extended['pct_of_gdp'][:5],
                   marker_color='#2ECC71', showlegend=False,
                   text=[f'{x:.2f}%' for x in countries_extended['pct_of_gdp'][:5]],
                   textposition='outside'),
            row=1, col=3
        )
        
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400, title_text="AI Investment by Country - Multiple Perspectives (2024)")
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🌍 Investment Leadership:**")
            st.write("• **US dominance:** $109.1B (43% of global)")
            st.write("• **Per capita leader:** Israel at $232 per person")
            st.write("• **As % of GDP:** Israel (0.48%) and US (0.43%) lead")
        
        with col2:
            st.write("**📈 Regional Dynamics:**")
            st.write("• **Asia rising:** Combined $16.4B across major economies")
            st.write("• **Europe steady:** $10.5B across top 3 countries")
            st.write("• **Concentration:** Top 5 countries = 82% of investment")
    
    with tab3:
        # GenAI growth visualization with context
        genai_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            'investment': [3.95, 28.5, 33.9],
            'growth': ['Baseline', '+621%', '+18.7%'],
            'pct_of_total': [2.7, 16.3, 13.4]  # % of total AI investment
        })
        
        # Create dual-axis chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=genai_data['year'],
            y=genai_data['investment'],
            text=[f'${x:.1f}B<br>{g}' for x, g in zip(genai_data['investment'], genai_data['growth'])],
            textposition='outside',
            marker_color=['#FFB6C1', '#FF69B4', '#FF1493'],
            name='GenAI Investment',
            yaxis='y'
        ))
        
        fig.add_trace(go.Scatter(
            x=genai_data['year'],
            y=genai_data['pct_of_total'],
            mode='lines+markers',
            name='% of Total AI Investment',
            line=dict(width=3, color='#2C3E50'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="GenAI Investment: From $3.95B to $33.9B in Two Years",
            xaxis_title="Year",
            yaxis=dict(title="Investment ($ Billions)", side="left"),
            yaxis2=dict(title="% of Total AI Investment", side="right", overlaying="y"),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**🚀 GenAI represents over 20% of all AI-related private investment, up from near zero in 2021**")
    
    with tab4:
        # Comparative analysis
        st.write("**Investment Growth Comparison**")
        
        # Calculate YoY growth rates
        growth_data = pd.DataFrame({
            'metric': ['Total AI', 'GenAI', 'US Investment', 'China Investment', 'UK Investment'],
            'growth_2024': [44.5, 18.7, 44.3, 10.7, 18.4],
            'cagr_5yr': [28.3, 156.8, 31.2, 15.4, 22.7]  # 5-year CAGR
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='2024 Growth (%)',
            x=growth_data['metric'],
            y=growth_data['growth_2024'],
            marker_color='#3498DB',
            text=[f'{x:.1f}%' for x in growth_data['growth_2024']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='5-Year CAGR (%)',
            x=growth_data['metric'],
            y=growth_data['cagr_5yr'],
            marker_color='#E74C3C',
            text=[f'{x:.1f}%' for x in growth_data['cagr_5yr']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="AI Investment Growth Rates",
            xaxis_title="Investment Category",
            yaxis_title="Growth Rate (%)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Note:** GenAI shows exceptional 5-year CAGR due to starting from near-zero base in 2019")

elif view_type == "Regional Growth":
    st.write("🌍 **Regional AI Adoption Growth (AI Index Report 2025)**")
    
    # Enhanced regional visualization with investment data
    fig = go.Figure()
    
    # Create subplot figure
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Adoption Growth in 2024', 'Investment Growth vs Adoption Rate'),
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.15
    )
    
    # Bar chart for adoption growth
    fig.add_trace(
        go.Bar(
            x=regional_growth['region'],
            y=regional_growth['growth_2024'],
            text=[f'+{x}pp' for x in regional_growth['growth_2024']],
            textposition='outside',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
            name='2024 Growth',
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Scatter plot for investment vs adoption
    fig.add_trace(
        go.Scatter(
            x=regional_growth['adoption_rate'],
            y=regional_growth['investment_growth'],
            mode='markers+text',
            marker=dict(
                size=regional_growth['growth_2024'],
                color=regional_growth['growth_2024'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="2024 Growth (pp)")
            ),
            text=regional_growth['region'],
            textposition='top center',
            showlegend=False
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text="Region", row=1, col=1)
    fig.update_yaxes(title_text="Growth (percentage points)", row=1, col=1)
    fig.update_xaxes(title_text="Current Adoption Rate (%)", row=1, col=2)
    fig.update_yaxes(title_text="Investment Growth (%)", row=1, col=2)
    
    fig.update_layout(height=450, title_text="Regional AI Adoption and Investment Dynamics")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional insights with metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fastest Growing", "Greater China", "+27pp adoption")
        st.write("**Also leads in:**")
        st.write("• Investment growth: +32%")
        st.write("• New AI startups: +45%")
    
    with col2:
        st.metric("Highest Adoption", "North America", "82% rate")
        st.write("**Characteristics:**")
        st.write("• Mature market")
        st.write("• Slower growth: +15pp")
    
    with col3:
        st.metric("Emerging Leader", "Europe", "+23pp growth")
        st.write("**Key drivers:**")
        st.write("• Regulatory clarity")
        st.write("• Public investment")
    
    # Competitive dynamics analysis
    st.subheader("🏁 Competitive Dynamics")
    
    # Create competitive positioning matrix
    fig2 = px.scatter(
        regional_growth,
        x='adoption_rate',
        y='growth_2024',
        size='investment_growth',
        color='region',
        title='Regional AI Competitive Positioning Matrix',
        labels={
            'adoption_rate': 'Current Adoption Rate (%)',
            'growth_2024': 'Adoption Growth Rate (pp)',
            'investment_growth': 'Investment Growth (%)'
        },
        height=400
    )
    
    # Add quadrant lines
    fig2.add_hline(y=regional_growth['growth_2024'].mean(), line_dash="dash", line_color="gray")
    fig2.add_vline(x=regional_growth['adoption_rate'].mean(), line_dash="dash", line_color="gray")
    
    # Add quadrant labels
    fig2.add_annotation(x=50, y=25, text="High Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=75, y=25, text="High Growth<br>High Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=50, y=13, text="Low Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=75, y=13, text="Low Growth<br>High Base", showarrow=False, font=dict(color="gray"))
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("""
    **Strategic Insights:**
    - **Greater China & Europe:** Aggressive catch-up strategy with high growth rates
    - **North America:** Market leader maintaining position with steady growth
    - **Competition intensifying:** Regional gaps narrowing as adoption accelerates globally
    """)

elif view_type == "AI Cost Trends":
    st.write("💰 **AI Cost Reduction: Dramatic Improvements (AI Index Report 2025)**")
    
    # Cost reduction visualization with context
    tab1, tab2, tab3 = st.tabs(["Inference Costs", "Hardware Improvements", "Cost Projections"])
    
    with tab1:
        # Enhanced cost reduction chart
        fig = go.Figure()
        
        # Add cost trajectory
        fig.add_trace(go.Scatter(
            x=['Nov 2022', 'Jan 2023', 'Jul 2023', 'Jan 2024', 'Oct 2024', 'Oct 2024\n(Gemini)'],
            y=[20.00, 10.00, 2.00, 0.50, 0.14, 0.07],
            mode='lines+markers',
            marker=dict(
                size=[15, 10, 10, 10, 15, 20],
                color=['red', 'orange', 'yellow', 'lightgreen', 'green', 'darkgreen']
            ),
            line=dict(width=3, color='gray', dash='dash'),
            text=['$20.00', '$10.00', '$2.00', '$0.50', '$0.14', '$0.07'],
            textposition='top center',
            name='Cost per Million Tokens',
            hovertemplate='Date: %{x}<br>Cost: %{text}<br>Reduction: %{customdata}<extra></extra>',
            customdata=['Baseline', '2x cheaper', '10x cheaper', '40x cheaper', '143x cheaper', '286x cheaper']
        ))
        
        # Add annotations for key milestones
        fig.add_annotation(
            x='Nov 2022', y=20,
            text="<b>GPT-3.5 Launch</b><br>$20/M tokens",
            showarrow=True,
            arrowhead=2,
            ax=0, ay=-40
        )
        
        fig.add_annotation(
            x='Oct 2024\n(Gemini)', y=0.07,
            text="<b>286x Cost Reduction</b><br>$0.07/M tokens",
            showarrow=True,
            arrowhead=2,
            ax=0, ay=40
        )
        
        fig.update_layout(
            title="AI Inference Cost Collapse: 286x Reduction in 2 Years",
            xaxis_title="Time Period",
            yaxis_title="Cost per Million Tokens ($)",
            yaxis_type="log",
            height=450,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost impact analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**💡 What This Means:**")
            st.write("• Processing 1B tokens now costs $70 (was $20,000)")
            st.write("• Enables mass deployment of AI applications")
            st.write("• Makes AI accessible to smaller organizations")
            
        with col2:
            st.write("**📈 Rate of Improvement:**")
            st.write("• Prices falling 9-900x per year by task")
            st.write("• Outpacing Moore's Law significantly")
            st.write("• Driven by competition and efficiency gains")
    
    with tab2:
        # Hardware improvements
        hardware_metrics = pd.DataFrame({
            'metric': ['Performance Growth', 'Price/Performance', 'Energy Efficiency'],
            'annual_rate': [43, -30, 40],
            'cumulative_5yr': [680, -83, 538]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Annual Rate (%)',
            x=hardware_metrics['metric'],
            y=hardware_metrics['annual_rate'],
            marker_color=['#2ECC71' if x > 0 else '#E74C3C' for x in hardware_metrics['annual_rate']],
            text=[f'{x:+d}%' for x in hardware_metrics['annual_rate']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="ML Hardware Annual Improvement Rates",
            xaxis_title="Metric",
            yaxis_title="Annual Change (%)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **🚀 Hardware Revolution:**
        - Performance improving **43% annually** (16-bit operations)
        - Cost dropping **30% per year** for same performance
        - Energy efficiency gaining **40% annually**
        - Enabling larger models at lower costs
        """)
    
    with tab3:
        # Cost projections
        st.write("**Future Cost Projections**")
        
        # Create projection data
        years = list(range(2024, 2028))
        conservative = [0.07, 0.035, 0.018, 0.009]
        aggressive = [0.07, 0.014, 0.003, 0.0006]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=conservative,
            mode='lines+markers',
            name='Conservative (50% annual reduction)',
            line=dict(width=3, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=aggressive,
            mode='lines+markers',
            name='Aggressive (80% annual reduction)',
            line=dict(width=3),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)'
        ))
        
        fig.update_layout(
            title="AI Cost Projections: 2024-2027",
            xaxis_title="Year",
            yaxis_title="Cost per Million Tokens ($)",
            yaxis_type="log",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **📊 Projection Assumptions:**
        - **Conservative:** Based on historical semiconductor improvements
        - **Aggressive:** Based on current AI-specific optimization rates
        - By 2027, costs could be 1000-10,000x lower than 2022
        """)

elif view_type == "Labor Impact":
    st.write("👥 **AI's Impact on Jobs and Workers (AI Index Report 2025)**")
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Expect Job Changes", 
            value="60%", 
            delta="Within 5 years",
            help="Global respondents believing AI will change their jobs"
        )
    
    with col2:
        st.metric(
            label="Expect Job Replacement", 
            value="36%", 
            delta="Within 5 years",
            help="Believe AI will replace their current jobs"
        )
    
    with col3:
        st.metric(
            label="Skill Gap Narrowing", 
            value="Confirmed", 
            delta="Low-skilled benefit most",
            help="AI helps reduce inequality"
        )
    
    with col4:
        st.metric(
            label="Productivity Boost", 
            value="14%", 
            delta="For low-skilled workers",
            help="Highest gains for entry-level"
        )
    
    # Create comprehensive labor impact visualization
    tab1, tab2, tab3, tab4 = st.tabs(["Generational Views", "Skill Impact", "Job Transformation", "Policy Implications"])
    
    with tab1:
        # Enhanced generational visualization
        fig = go.Figure()
        
        # Job change expectations
        fig.add_trace(go.Bar(
            name='Expect Job Changes',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_change'],
            marker_color='#4ECDC4',
            text=[f'{x}%' for x in ai_perception['expect_job_change']],
            textposition='outside'
        ))
        
        # Job replacement expectations
        fig.add_trace(go.Bar(
            name='Expect Job Replacement',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_replacement'],
            marker_color='#F38630',
            text=[f'{x}%' for x in ai_perception['expect_job_replacement']],
            textposition='outside'
        ))
        
        # Add average lines
        avg_change = ai_perception['expect_job_change'].mean()
        avg_replace = ai_perception['expect_job_replacement'].mean()
        
        fig.add_hline(y=avg_change, line_dash="dash", line_color="rgba(78, 205, 196, 0.5)",
                      annotation_text=f"Avg: {avg_change:.0f}%", annotation_position="right")
        fig.add_hline(y=avg_replace, line_dash="dash", line_color="rgba(243, 134, 48, 0.5)",
                      annotation_text=f"Avg: {avg_replace:.0f}%", annotation_position="right")
        
        fig.update_layout(
            title="AI Job Impact Expectations by Generation",
            xaxis_title="Generation",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Generation insights
        st.info("""
        **Key Insights:**
        - **18pp gap** between Gen Z and Baby Boomers on job change expectations
        - Younger workers more aware of AI's transformative potential
        - All generations show concern but vary in urgency perception
        """)
    
    with tab2:
        # Skill impact analysis
        skill_impact = pd.DataFrame({
            'job_category': ['Entry-Level/Low-Skill', 'Mid-Level/Medium-Skill', 'Senior/High-Skill', 'Creative/Specialized'],
            'productivity_gain': [14, 9, 5, 7],
            'job_risk': [45, 38, 22, 15],
            'reskilling_need': [85, 72, 58, 65]
        })
        
        fig = go.Figure()
        
        # Create grouped bar chart
        categories = ['Productivity Gain (%)', 'Job Risk (%)', 'Reskilling Need (%)']
        
        for i, category in enumerate(skill_impact['job_category']):
            values = [
                skill_impact.loc[i, 'productivity_gain'],
                skill_impact.loc[i, 'job_risk'],
                skill_impact.loc[i, 'reskilling_need']
            ]
            
            fig.add_trace(go.Bar(
                name=category,
                x=categories,
                y=values,
                text=[f'{v}%' for v in values],
                textposition='outside'
            ))
        
        fig.update_layout(
            title="AI Impact by Job Category",
            xaxis_title="Impact Metric",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **Positive Finding:** AI provides greatest productivity boosts to entry-level workers, 
        potentially reducing workplace inequality and accelerating skill development.
        """)
    
    with tab3:
        # Job transformation timeline
        transformation_data = pd.DataFrame({
            'timeframe': ['0-2 years', '2-5 years', '5-10 years', '10+ years'],
            'jobs_affected': [15, 35, 60, 80],
            'new_jobs_created': [10, 25, 45, 65],
            'net_impact': [5, 10, 15, 15]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=transformation_data['timeframe'],
            y=transformation_data['jobs_affected'],
            mode='lines+markers',
            name='Jobs Affected',
            line=dict(width=3, color='#E74C3C'),
            marker=dict(size=10),
            fill='tonexty'
        ))
        
        fig.add_trace(go.Scatter(
            x=transformation_data['timeframe'],
            y=transformation_data['new_jobs_created'],
            mode='lines+markers',
            name='New Jobs Created',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title="Projected Job Market Transformation Timeline",
            xaxis_title="Timeframe",
            yaxis_title="Percentage of Workforce (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Transformation Patterns:**
        - Initial displacement in routine tasks
        - New roles emerge in AI management, ethics, and human-AI collaboration
        - Net positive effect expected long-term with proper reskilling
        """)
    
    with tab4:
        # Policy recommendations
        st.write("**Policy Recommendations for Workforce Transition**")
        
        policy_areas = pd.DataFrame({
            'area': ['Education Reform', 'Reskilling Programs', 'Safety Nets', 
                    'Innovation Support', 'Regulation', 'Public-Private Partnership'],
            'priority': [95, 92, 85, 78, 72, 88],
            'current_investment': [45, 38, 52, 65, 58, 42]
        })
        
        fig = px.scatter(
            policy_areas,
            x='current_investment',
            y='priority',
            size='priority',
            text='area',
            title='Policy Priority vs Current Investment',
            labels={'current_investment': 'Current Investment Level (%)', 
                   'priority': 'Priority Score (%)'},
            height=400
        )
        
        # Add quadrant dividers
        fig.add_hline(y=85, line_dash="dash", line_color="gray")
        fig.add_vline(x=50, line_dash="dash", line_color="gray")
        
        # Quadrant labels
        fig.add_annotation(x=30, y=90, text="High Priority<br>Low Investment", 
                          showarrow=False, font=dict(color="red"))
        fig.add_annotation(x=70, y=90, text="High Priority<br>High Investment", 
                          showarrow=False, font=dict(color="green"))
        
        fig.update_traces(textposition='top center')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning("""
        **Critical Gaps:**
        - **Education Reform** and **Reskilling Programs** are high priority but underfunded
        - Need 2-3x increase in workforce development investment
        - Public-private partnerships essential for scale
        """)

elif view_type == "Environmental Impact":
    st.write("🌱 **Environmental Impact: AI's Growing Carbon Footprint (AI Index Report 2025)**")
    
    # Create comprehensive environmental dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["Training Emissions", "Energy Trends", "Mitigation Strategies", "Sustainability Metrics"])
    
    with tab1:
        # Enhanced emissions visualization
        fig = go.Figure()
        
        # Add bars for emissions
        fig.add_trace(go.Bar(
            x=training_emissions['model'],
            y=training_emissions['carbon_tons'],
            marker_color=['#90EE90', '#FFD700', '#FF6347', '#8B0000'],
            text=[f'{x:,.0f} tons' for x in training_emissions['carbon_tons']],
            textposition='outside',
            hovertemplate='Model: %{x}<br>Emissions: %{text}<br>Equivalent: %{customdata}<extra></extra>',
            customdata=['Negligible', '~125 cars/year', '~1,100 cars/year', '~1,900 cars/year']
        ))
        
        # Add trend line
        fig.add_trace(go.Scatter(
            x=training_emissions['model'],
            y=training_emissions['carbon_tons'],
            mode='lines',
            line=dict(width=3, color='red', dash='dash'),
            name='Exponential Growth Trend',
            showlegend=True
        ))
        
        fig.update_layout(
            title="Carbon Emissions from AI Model Training: Exponential Growth",
            xaxis_title="AI Model",
            yaxis_title="Carbon Emissions (tons CO₂)",
            yaxis_type="log",
            height=450,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Emissions context
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📈 Growth Rate:**")
            st.write("• 900,000x increase from 2012 to 2024")
            st.write("• Doubling approximately every 2 years")
            st.write("• Driven by model size and compute needs")
        
        with col2:
            st.write("**🌍 Context:**")
            st.write("• Llama 3.1 = Annual emissions of 1,900 cars")
            st.write("• One training run = 8,930 tons CO₂")
            st.write("• Excludes inference and retraining")
    
    with tab2:
        # Energy trends and nuclear pivot
        st.write("**⚡ Energy Consumption and Nuclear Renaissance**")
        
        energy_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024, 2025],
            'ai_energy_twh': [2.1, 3.5, 5.8, 9.6, 16.2, 27.3],
            'nuclear_deals': [0, 0, 1, 3, 8, 15]
        })
        
        fig = go.Figure()
        
        # Energy consumption
        fig.add_trace(go.Bar(
            x=energy_data['year'],
            y=energy_data['ai_energy_twh'],
            name='AI Energy Use (TWh)',
            marker_color='#3498DB',
            yaxis='y',
            text=[f'{x:.1f} TWh' for x in energy_data['ai_energy_twh']],
            textposition='outside'
        ))
        
        # Nuclear deals
        fig.add_trace(go.Scatter(
            x=energy_data['year'],
            y=energy_data['nuclear_deals'],
            name='Nuclear Energy Deals',
            mode='lines+markers',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="AI Energy Consumption Driving Nuclear Energy Revival",
            xaxis_title="Year",
            yaxis=dict(title="Energy Consumption (TWh)", side="left"),
            yaxis2=dict(title="Nuclear Deals (#)", side="right", overlaying="y"),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **🔋 Major Nuclear Agreements (2024-2025):**
        - Microsoft: Three Mile Island restart
        - Google: Kairos Power SMR partnership
        - Amazon: X-energy SMR development
        - Meta: Nuclear power exploration
        """)
    
    with tab3:
        # Mitigation strategies
        mitigation = pd.DataFrame({
            'strategy': ['Efficient Architectures', 'Renewable Energy', 'Model Reuse', 
                        'Edge Computing', 'Quantum Computing', 'Carbon Offsets'],
            'potential_reduction': [40, 85, 95, 60, 90, 100],
            'adoption_rate': [65, 45, 35, 25, 5, 30],
            'timeframe': [1, 3, 1, 2, 7, 1]
        })
        
        fig = px.scatter(
            mitigation,
            x='adoption_rate',
            y='potential_reduction',
            size='timeframe',
            color='strategy',
            title='AI Sustainability Strategies: Impact vs Adoption',
            labels={
                'adoption_rate': 'Current Adoption Rate (%)',
                'potential_reduction': 'Potential Emission Reduction (%)',
                'timeframe': 'Implementation Time (years)'
            },
            height=400
        )
        
        # Add target zone
        fig.add_shape(
            type="rect",
            x0=70, x1=100,
            y0=70, y1=100,
            fillcolor="lightgreen",
            opacity=0.2,
            line_width=0
        )
        
        fig.add_annotation(
            x=85, y=85,
            text="Target Zone",
            showarrow=False,
            font=dict(color="green")
        )
        
        fig.update_traces(textposition='top center')
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("""
        **Most Promising Strategies:**
        - **Model Reuse:** 95% reduction potential, needs ecosystem development
        - **Renewable Energy:** 85% reduction, requires infrastructure investment
        - **Efficient Architectures:** Quick wins with 40% reduction potential
        """)
    
    with tab4:
        # Sustainability metrics dashboard
        st.write("**Sustainability Performance Metrics**")
        
        # Create sustainability scorecard
        metrics = pd.DataFrame({
            'company': ['OpenAI', 'Google', 'Microsoft', 'Meta', 'Amazon'],
            'renewable_pct': [45, 78, 65, 52, 40],
            'efficiency_score': [7.2, 8.5, 7.8, 6.9, 7.5],
            'transparency_score': [6.5, 8.2, 7.9, 6.2, 7.0],
            'carbon_neutral_target': [2030, 2028, 2029, 2030, 2032]
        })
        
        fig = go.Figure()
        
        # Create radar chart
        categories = ['Renewable %', 'Efficiency', 'Transparency']
        
        for _, company in metrics.iterrows():
            values = [
                company['renewable_pct'] / 10,  # Scale to 10
                company['efficiency_score'],
                company['transparency_score']
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=company['company']
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="AI Company Sustainability Scores",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Industry Trends:**
        - Increasing pressure for carbon neutrality
        - Hardware efficiency improving 40% annually
        - Growing focus on lifecycle emissions
        """)

elif view_type == "Adoption Rates":
    if "2025" in data_year:
        st.write("📊 **GenAI Adoption by Business Function (2025)**")
        
        # Enhanced function data with financial impact
        function_data = financial_impact.copy()
        function_data['adoption'] = [42, 23, 7, 22, 28, 23, 13, 15]  # GenAI adoption rates
        
        # Create comprehensive visualization
        fig = go.Figure()
        
        # Adoption rate bars
        fig.add_trace(go.Bar(
            x=function_data['function'],
            y=function_data['adoption'],
            name='GenAI Adoption Rate',
            marker_color='#3498DB',
            yaxis='y',
            text=[f'{x}%' for x in function_data['adoption']],
            textposition='outside'
        ))
        
        # Revenue impact line
        fig.add_trace(go.Scatter(
            x=function_data['function'],
            y=function_data['companies_reporting_revenue_gains'],
            mode='lines+markers',
            name='% Reporting Revenue Gains',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='GenAI Adoption and Business Impact by Function',
            xaxis_tickangle=45,
            yaxis=dict(title="GenAI Adoption Rate (%)", side="left"),
            yaxis2=dict(title="% Reporting Revenue Gains", side="right", overlaying="y"),
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Function insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("🎯 **Top Functions:**")
            st.write("• **Marketing & Sales:** 42% adoption, 71% see revenue gains")
            st.write("• **Product Development:** 28% adoption, 52% see revenue gains")
            st.write("• **Service Operations:** 23% adoption, 49% see cost savings")
        
        with col2:
            if st.button("📊 View Data Source", key="adoption_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('mckinsey'))
        
        # Note about adoption definition
        st.info("**Note:** Adoption rates include any GenAI use (pilots, experiments, production) among firms using AI")
        
    else:
        # 2018 view
        weighting = st.sidebar.radio("Weighting Method", ["Firm-Weighted", "Employment-Weighted"])
        y_col = 'firm_weighted' if weighting == "Firm-Weighted" else 'employment_weighted'
        
        fig = px.bar(
            sector_2018, 
            x='sector', 
            y=y_col, 
            title=f'AI Adoption by Sector (2018) - {weighting}',
            color=y_col, 
            color_continuous_scale='blues',
            text=y_col
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(xaxis_tickangle=45, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("🏭 **Key Insight**: Manufacturing and Information sectors led early AI adoption at 12% each")

elif view_type == "Firm Size Analysis":
    st.write("🏢 **AI Adoption by Firm Size**")
    
    # Enhanced visualization with annotations
    fig = go.Figure()
    
    # Main bar chart
    fig.add_trace(go.Bar(
        x=firm_size['size'], 
        y=firm_size['adoption'],
        marker_color=firm_size['adoption'],
        marker_colorscale='Greens',
        text=[f'{x}%' for x in firm_size['adoption']],
        textposition='outside',
        hovertemplate='Size: %{x}<br>Adoption: %{y}%<br>Employees: %{customdata}<extra></extra>',
        customdata=firm_size['size']
    ))
    
    # Add trend line
    x_numeric = list(range(len(firm_size)))
    z = np.polyfit(x_numeric, firm_size['adoption'], 2)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=firm_size['size'],
        y=p(x_numeric),
        mode='lines',
        line=dict(width=3, color='red', dash='dash'),
        name='Trend',
        showlegend=True
    ))
    
    # Add annotations for key thresholds
    fig.add_annotation(
        x='100-249', y=12.5,
        text="<b>SME Threshold</b><br>12.5% adoption",
        showarrow=True,
        arrowhead=2,
        ax=0, ay=-40
    )
    
    fig.add_annotation(
        x='5000+', y=58.5,
        text="<b>Enterprise Leaders</b><br>58.5% adoption",
        showarrow=True,
        arrowhead=2,
        ax=0, ay=-40
    )
    
    fig.update_layout(
        title='AI Adoption Shows Strong Correlation with Firm Size',
        xaxis_title='Number of Employees',
        yaxis_title='AI Adoption Rate (%)',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Size insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Size Gap", "18x", "5000+ vs 1-4 employees")
    with col2:
        st.metric("SME Adoption", "<20%", "For firms <250 employees")
    with col3:
        st.metric("Enterprise Adoption", ">40%", "For firms >2500 employees")
    
    st.info("""
    **📈 Key Insights:**
    - Strong exponential relationship between size and adoption
    - Resource constraints limit small firm adoption
    - Enterprises benefit from economies of scale in AI deployment
    """)

elif view_type == "Technology Stack":
    st.write("🔧 **AI Technology Stack Analysis**")
    
    # Enhanced pie chart with additional context
    fig = go.Figure()
    
    # Calculate actual percentages
    stack_data = pd.DataFrame({
        'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
        'percentage': [15, 23, 24, 38],  # Adjusted to sum to 100%
        'roi_multiplier': [1.5, 2.8, 2.5, 3.5]
    })
    
    # Create donut chart
    fig.add_trace(go.Pie(
        labels=stack_data['technology'],
        values=stack_data['percentage'],
        hole=0.4,
        marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Adoption: %{value}%<br>ROI: %{customdata}x<extra></extra>',
        customdata=stack_data['roi_multiplier']
    ))
    
    fig.update_layout(
        title='Technology Stack Combinations and Their Prevalence',
        height=450,
        annotations=[dict(text='Tech<br>Stack', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Stack insights with ROI
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🔗 Technology Synergies:**")
        st.write("• **38%** use full stack (AI + Cloud + Digitization)")
        st.write("• **62%** combine AI with at least one other technology")
        st.write("• Only **15%** use AI in isolation")
    
    with col2:
        st.write("**💰 ROI by Stack:**")
        st.write("• Full stack: **3.5x** ROI")
        st.write("• AI + Cloud: **2.8x** ROI")
        st.write("• AI only: **1.5x** ROI")
    
    st.success("**Key Finding:** Technology complementarity is crucial - combined deployments show significantly higher returns")

elif view_type == "AI Technology Maturity":
    st.write("🎯 **AI Technology Maturity & Adoption (Gartner 2025)**")
    
    # Enhanced maturity visualization
    color_map = {
        'Peak of Expectations': '#F59E0B',
        'Trough of Disillusionment': '#6B7280', 
        'Slope of Enlightenment': '#10B981'
    }
    
    fig = go.Figure()
    
    # Group by maturity stage
    for stage in ai_maturity['maturity'].unique():
        stage_data = ai_maturity[ai_maturity['maturity'] == stage]
        
        fig.add_trace(go.Scatter(
            x=stage_data['adoption_rate'],
            y=stage_data['risk_score'],
            mode='markers+text',
            name=stage,
            marker=dict(
                size=stage_data['time_to_value'] * 10,
                color=color_map[stage],
                line=dict(width=2, color='white')
            ),
            text=stage_data['technology'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Adoption: %{x}%<br>Risk: %{y}/100<br>Time to Value: %{customdata} years<extra></extra>',
            customdata=stage_data['time_to_value']
        ))
    
    # Add quadrant lines
    fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Quadrant labels
    fig.add_annotation(x=25, y=75, text="High Risk<br>Low Adoption", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(x=75, y=75, text="High Risk<br>High Adoption", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(x=25, y=25, text="Low Risk<br>Low Adoption", showarrow=False, font=dict(color="gray"))
    fig.add_annotation(x=75, y=25, text="Low Risk<br>High Adoption", showarrow=False, font=dict(color="gray"))
    
    fig.update_layout(
        title="AI Technology Risk-Adoption Matrix",
        xaxis_title="Adoption Rate (%)",
        yaxis_title="Risk Score (0-100)",
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Maturity insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Strategic Recommendations:**")
        st.write("• **Invest in:** Cloud AI Services (low risk, high adoption)")
        st.write("• **Watch:** AI Agents (high potential, high risk)")
        st.write("• **Mature:** Foundation Models moving past hype")
    
    with col2:
        st.write("**⏱️ Time to Value:**")
        st.write("• **Fastest:** Cloud AI Services (1 year)")
        st.write("• **Medium:** Most technologies (3 years)")
        st.write("• **Longest:** Composite AI (7 years)")

elif view_type == "Geographic Distribution":
    st.write("🗺️ **AI Adoption Geographic Distribution**")
    
    # Enhanced geographic visualization
    fig = go.Figure()
    
    # State choropleth
    fig.add_trace(go.Choropleth(
        locations=state_data['state_code'],
        z=state_data['rate'],
        locationmode='USA-states',
        colorscale='YlGnBu',
        colorbar=dict(
            title="State Average<br>AI Adoption (%)",
            x=0.02,
            len=0.4,
            y=0.5
        ),
        marker_line_color='black',
        marker_line_width=2,
        hovertemplate='<b>%{text}</b><br>State Average: %{z:.1f}%<extra></extra>',
        text=state_data['state']
    ))
    
    # City scatter with GDP context
    fig.add_trace(go.Scattergeo(
        lon=geographic['lon'],
        lat=geographic['lat'],
        text=geographic['city'],
        customdata=geographic[['rate', 'state', 'population_millions', 'gdp_billions']],
        mode='markers',
        marker=dict(
            size=geographic['rate'] ** 1.8,
            color=geographic['rate'],
            colorscale='Hot_r',
            showscale=True,
            colorbar=dict(
                title="City AI<br>Adoption (%)",
                x=0.98,
                len=0.4,
                y=0.5
            ),
            line=dict(width=3, color='white'),
            sizemode='diameter',
            sizemin=10,
            opacity=0.85
        ),
        showlegend=False,
        hovertemplate='<b>%{text}</b><br>State: %{customdata[1]}<br>AI Adoption: %{customdata[0]:.1f}%<br>Population: %{customdata[2]:.1f}M<br>GDP: $%{customdata[3]:.0f}B<extra></extra>'
    ))
    
    # Add top 3 city annotations
    top_cities = geographic.nlargest(3, 'rate')
    for _, city in top_cities.iterrows():
        fig.add_annotation(
            x=city['lon'],
            y=city['lat'],
            text=f"<b>{city['city'].split()[0]}</b><br>{city['rate']:.1f}%",
            showarrow=True,
            arrowhead=2,
            ax=-50 if city['lon'] < -100 else 50,
            ay=-30,
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='white',
            borderwidth=2,
            font=dict(size=11, color='white')
        )
    
    fig.update_layout(
        title='AI Adoption Landscape: State Foundations & City Innovation Hubs',
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='rgb(235, 235, 235)',
            coastlinecolor='rgb(50, 50, 50)',
            coastlinewidth=2
        ),
        height=700
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Geographic insights with economic context
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Top Metro", "SF Bay Area", "9.5% adoption")
        st.write("**Economic Context:**")
        st.write("• GDP: $535B")
        st.write("• Pop: 7.7M")
        st.write("• AI per capita: High")
    
    with col2:
        st.metric("Emerging Hub", "Nashville", "8.3% adoption")
        st.write("**Growth Factors:**")
        st.write("• Tech migration")
        st.write("• Lower costs")
        st.write("• Policy support")
    
    with col3:
        st.metric("Geographic Gap", "3.5pp", "Highest vs lowest state")
        st.write("**Regional Patterns:**")
        st.write("• Coastal concentration")
        st.write("• Midwest lagging")
        st.write("• South emerging")

elif view_type == "OECD 2025 Findings":
    st.write("📊 **OECD/BCG/INSEAD 2025 Report: Enterprise AI Adoption**")
    
    # Enhanced OECD visualization
    tab1, tab2, tab3 = st.tabs(["Country Analysis", "Application Trends", "Success Factors"])
    
    with tab1:
        # G7 comparison with context
        fig = go.Figure()
        
        # Create grouped bars
        x = oecd_g7_adoption['country']
        
        fig.add_trace(go.Bar(
            name='Overall Adoption',
            x=x,
            y=oecd_g7_adoption['adoption_rate'],
            marker_color='#3B82F6',
            text=[f'{x}%' for x in oecd_g7_adoption['adoption_rate']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Manufacturing',
            x=x,
            y=oecd_g7_adoption['manufacturing'],
            marker_color='#10B981',
            text=[f'{x}%' for x in oecd_g7_adoption['manufacturing']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='ICT Sector',
            x=x,
            y=oecd_g7_adoption['ict_sector'],
            marker_color='#F59E0B',
            text=[f'{x}%' for x in oecd_g7_adoption['ict_sector']],
            textposition='outside'
        ))
        
        # Add G7 average line
        g7_avg = oecd_g7_adoption['adoption_rate'].mean()
        fig.add_hline(y=g7_avg, line_dash="dash", line_color="red",
                      annotation_text=f"G7 Average: {g7_avg:.0f}%", annotation_position="right")
        
        fig.update_layout(
            title="AI Adoption Rates Across G7 Countries by Sector",
            xaxis_title="Country",
            yaxis_title="Adoption Rate (%)",
            barmode='group',
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Country insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🌍 Key Findings:**")
            st.write("• **Japan** leads G7 with 48% overall adoption")
            st.write("• **ICT sector** universally leads (55-70%)")
            st.write("• **15-20pp** gap between ICT and other sectors")
        
        with col2:
            if st.button("📊 View OECD Methodology", key="oecd_method"):
                with st.expander("Methodology", expanded=True):
                    st.info(show_source_info('oecd'))
    
    with tab2:
        # Enhanced applications view
        genai_apps = oecd_applications[oecd_applications['category'] == 'GenAI']
        traditional_apps = oecd_applications[oecd_applications['category'] == 'Traditional AI']
        
        fig = go.Figure()
        
        # GenAI applications
        fig.add_trace(go.Bar(
            name='GenAI Applications',
            y=genai_apps.sort_values('usage_rate')['application'],
            x=genai_apps.sort_values('usage_rate')['usage_rate'],
            orientation='h',
            marker_color='#E74C3C',
            text=[f'{x}%' for x in genai_apps.sort_values('usage_rate')['usage_rate']],
            textposition='outside'
        ))
        
        # Traditional AI applications
        fig.add_trace(go.Bar(
            name='Traditional AI',
            y=traditional_apps.sort_values('usage_rate')['application'],
            x=traditional_apps.sort_values('usage_rate')['usage_rate'],
            orientation='h',
            marker_color='#3498DB',
            text=[f'{x}%' for x in traditional_apps.sort_values('usage_rate')['usage_rate']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='AI Application Usage: GenAI vs Traditional AI',
            xaxis_title='Usage Rate (% of AI-adopting firms)',
            height=600,
            showlegend=True,
            barmode='overlay'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**Key Trend:** GenAI applications (content generation, code generation, chatbots) now lead adoption rates")
    
    with tab3:
        # Success factors analysis
        success_factors = pd.DataFrame({
            'factor': ['Leadership Commitment', 'Data Infrastructure', 'Talent Availability',
                      'Change Management', 'Partnership Ecosystem', 'Regulatory Clarity'],
            'importance': [92, 88, 85, 78, 72, 68],
            'readiness': [65, 72, 45, 52, 58, 48]
        })
        
        fig = go.Figure()
        
        # Create gap analysis
        fig.add_trace(go.Bar(
            name='Importance',
            x=success_factors['factor'],
            y=success_factors['importance'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in success_factors['importance']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='Current Readiness',
            x=success_factors['factor'],
            y=success_factors['readiness'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in success_factors['readiness']],
            textposition='outside'
        ))
        
        # Calculate and display gaps
        gaps = success_factors['importance'] - success_factors['readiness']
        fig.add_trace(go.Scatter(
            name='Gap',
            x=success_factors['factor'],
            y=gaps,
            mode='markers+text',
            marker=dict(size=15, color='orange'),
            text=[f'-{x}pp' for x in gaps],
            textposition='top center',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='AI Success Factors: Importance vs Readiness Gap',
            xaxis_title='Success Factor',
            yaxis=dict(title='Score (%)', side='left'),
            yaxis2=dict(title='Gap (pp)', side='right', overlaying='y', range=[0, 50]),
            height=450,
            barmode='group',
            xaxis_tickangle=45
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning("**Critical Gap:** Talent availability shows the largest readiness gap (40pp), highlighting the global AI skills shortage")

elif view_type == "Barriers & Support":
    st.write("🚧 **AI Adoption Barriers & Support Effectiveness**")
    
    # Enhanced barriers visualization
    fig = go.Figure()
    
    # Sort barriers by severity
    barriers_sorted = barriers_data.sort_values('percentage', ascending=True)
    
    # Create horizontal bar chart with categories
    barrier_categories = {
        'Lack of skilled personnel': 'Talent',
        'Data availability/quality': 'Data',
        'Integration with legacy systems': 'Technical',
        'Regulatory uncertainty': 'Regulatory',
        'High implementation costs': 'Financial',
        'Security concerns': 'Risk',
        'Unclear ROI': 'Financial',
        'Organizational resistance': 'Cultural'
    }
    
    colors = {
        'Talent': '#E74C3C',
        'Data': '#3498DB',
        'Technical': '#9B59B6',
        'Regulatory': '#F39C12',
        'Financial': '#2ECC71',
        'Risk': '#1ABC9C',
        'Cultural': '#34495E'
    }
    
    barriers_sorted['category'] = barriers_sorted['barrier'].map(barrier_categories)
    barriers_sorted['color'] = barriers_sorted['category'].map(colors)
    
    fig.add_trace(go.Bar(
        y=barriers_sorted['barrier'],
        x=barriers_sorted['percentage'],
        orientation='h',
        marker_color=barriers_sorted['color'],
        text=[f'{x}%' for x in barriers_sorted['percentage']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Severity: %{x}%<br>Category: %{customdata}<extra></extra>',
        customdata=barriers_sorted['category']
    ))
    
    fig.update_layout(
        title='Main Barriers to AI Adoption by Category',
        xaxis_title='Companies Reporting Barrier (%)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Support effectiveness with implementation roadmap
    st.subheader("🎯 Support Measures & Implementation Roadmap")
    
    # Create implementation timeline
    support_timeline = pd.DataFrame({
        'measure': ['Regulatory clarity', 'Government education investment', 'Tax incentives',
                   'University partnerships', 'Innovation grants', 'Technology centers',
                   'Public-private collaboration'],
        'effectiveness': [73, 82, 68, 78, 65, 62, 75],
        'implementation_time': [6, 24, 12, 18, 9, 36, 15],  # months
        'cost': [1, 5, 4, 3, 4, 5, 3]  # 1-5 scale
    })
    
    fig2 = px.scatter(
        support_timeline,
        x='implementation_time',
        y='effectiveness',
        size='cost',
        color='measure',
        title='Support Measures: Effectiveness vs Implementation Time',
        labels={
            'implementation_time': 'Implementation Time (months)',
            'effectiveness': 'Effectiveness Score (%)',
            'cost': 'Relative Cost'
        },
        height=400
    )
    
    # Add quadrant dividers
    fig2.add_hline(y=70, line_dash="dash", line_color="gray")
    fig2.add_vline(x=18, line_dash="dash", line_color="gray")
    
    # Quadrant labels
    fig2.add_annotation(x=9, y=75, text="Quick Wins", showarrow=False, font=dict(color="green", size=14))
    fig2.add_annotation(x=30, y=75, text="Long-term Strategic", showarrow=False, font=dict(color="blue", size=14))
    
    fig2.update_traces(textposition='top center')
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Policy recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🚀 Quick Wins (< 1 year):**")
        st.write("• **Regulatory clarity:** High impact, low cost")
        st.write("• **Innovation grants:** Fast deployment")
        st.write("• **Tax incentives:** Immediate effect")
    
    with col2:
        st.write("**🎯 Strategic Investments:**")
        st.write("• **Education investment:** Highest effectiveness (82%)")
        st.write("• **University partnerships:** Strong talent pipeline")
        st.write("• **Technology centers:** Infrastructure development")
    
    st.success("""
    **Recommended Approach:** 
    Start with regulatory clarity and tax incentives for immediate impact while building 
    long-term capacity through education and partnerships.
    """)

elif view_type == "ROI Analysis":
    st.write("💰 **ROI Analysis: Comprehensive Economic Impact**")
    
    # Create detailed ROI dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["Investment Returns", "Payback Analysis", "Sector ROI", "ROI Calculator"])
    
    with tab1:
        # Investment returns visualization
        roi_data = pd.DataFrame({
            'investment_level': ['Pilot (<$100K)', 'Small ($100K-$500K)', 'Medium ($500K-$2M)', 
                               'Large ($2M-$10M)', 'Enterprise ($10M+)'],
            'avg_roi': [1.8, 2.5, 3.2, 3.8, 4.5],
            'time_to_roi': [6, 9, 12, 18, 24],  # months
            'success_rate': [45, 58, 72, 81, 87]  # % of projects achieving positive ROI
        })
        
        fig = go.Figure()
        
        # ROI bars
        fig.add_trace(go.Bar(
            name='Average ROI',
            x=roi_data['investment_level'],
            y=roi_data['avg_roi'],
            yaxis='y',
            marker_color='#2ECC71',
            text=[f'{x}x' for x in roi_data['avg_roi']],
            textposition='outside'
        ))
        
        # Success rate line
        fig.add_trace(go.Scatter(
            name='Success Rate',
            x=roi_data['investment_level'],
            y=roi_data['success_rate'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(width=3, color='#3498DB'),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='AI ROI by Investment Level',
            xaxis_title='Investment Level',
            yaxis=dict(title='Average ROI (x)', side='left'),
            yaxis2=dict(title='Success Rate (%)', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Key Insights:**
        - Larger investments show higher ROI and success rates
        - Enterprise projects (87% success) benefit from better resources and planning
        - Even small pilots can achieve 1.8x ROI with 45% success rate
        """)
    
    with tab2:
        # Payback period analysis
        payback_data = pd.DataFrame({
            'scenario': ['Best Case', 'Typical', 'Conservative'],
            'months': [8, 15, 24],
            'probability': [20, 60, 20]
        })
        
        fig = go.Figure()
        
        # Create funnel chart for payback scenarios
        fig.add_trace(go.Funnel(
            y=payback_data['scenario'],
            x=payback_data['months'],
            textinfo="value+percent",
            marker=dict(color=['#2ECC71', '#F39C12', '#E74C3C'])
        ))
        
        fig.update_layout(
            title='AI Investment Payback Period Distribution',
            xaxis_title='Months to Payback',
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Factors affecting payback
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🚀 Accelerators:**")
            st.write("• Clear use case definition")
            st.write("• Strong change management")
            st.write("• Existing data infrastructure")
            st.write("• Skilled team in place")
        
        with col2:
            st.write("**🐌 Delays:**")
            st.write("• Poor data quality")
            st.write("• Integration challenges")
            st.write("• Organizational resistance")
            st.write("• Scope creep")
    
    with tab3:
        # Sector-specific ROI
        fig = go.Figure()
        
        # Use sector_2025 data for ROI
        fig.add_trace(go.Bar(
            x=sector_2025.sort_values('avg_roi')['sector'],
            y=sector_2025.sort_values('avg_roi')['avg_roi'],
            marker_color=sector_2025.sort_values('avg_roi')['avg_roi'],
            marker_colorscale='Viridis',
            text=[f'{x}x' for x in sector_2025.sort_values('avg_roi')['avg_roi']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>ROI: %{y}x<br>Adoption: %{customdata}%<extra></extra>',
            customdata=sector_2025.sort_values('avg_roi')['adoption_rate']
        ))
        
        fig.update_layout(
            title='Average AI ROI by Industry Sector',
            xaxis_title='Industry',
            yaxis_title='Average ROI (x)',
            height=400,
            xaxis_tickangle=45,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top performers analysis
        top_sectors = sector_2025.nlargest(3, 'avg_roi')
        
        st.write("**🏆 Top ROI Performers:**")
        for _, sector in top_sectors.iterrows():
            st.write(f"• **{sector['sector']}:** {sector['avg_roi']}x ROI, {sector['adoption_rate']}% adoption")
    
    with tab4:
        # Interactive ROI Calculator
        st.write("**🧮 AI ROI Calculator**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calc_investment = st.number_input(
                "Initial Investment ($)",
                min_value=10000,
                max_value=10000000,
                value=500000,
                step=10000
            )
            
            calc_industry = st.selectbox(
                "Industry",
                sector_2025['sector'].tolist()
            )
            
            calc_timeline = st.slider(
                "Implementation Timeline (months)",
                min_value=3,
                max_value=36,
                value=12
            )
        
        with col2:
            calc_quality = st.slider(
                "Implementation Quality (1-10)",
                min_value=1,
                max_value=10,
                value=7
            )
            
            calc_scale = st.selectbox(
                "Deployment Scale",
                ["Pilot", "Department", "Division", "Enterprise-wide"]
            )
            
            calc_tech_stack = st.multiselect(
                "Technology Stack",
                ["AI Only", "Cloud", "Advanced Analytics", "Automation"],
                default=["AI Only", "Cloud"]
            )
        
        # Calculate ROI
        base_roi = sector_2025[sector_2025['sector'] == calc_industry]['avg_roi'].values[0]
        
        # Quality multiplier
        quality_mult = 0.5 + (calc_quality / 10)
        
        # Scale multiplier
        scale_mult = {"Pilot": 0.7, "Department": 0.9, "Division": 1.1, "Enterprise-wide": 1.3}[calc_scale]
        
        # Tech stack multiplier
        tech_mult = 1 + (len(calc_tech_stack) - 1) * 0.2
        
        # Final calculation
        final_calc_roi = base_roi * quality_mult * scale_mult * tech_mult
        expected_value = calc_investment * final_calc_roi
        net_gain = expected_value - calc_investment
        monthly_gain = net_gain / calc_timeline
        
        # Display results
        st.markdown("---")
        
        result_col1, result_col2, result_col3, result_col4 = st.columns(4)
        
        with result_col1:
            st.metric("Expected ROI", f"{final_calc_roi:.2f}x")
        with result_col2:
            st.metric("Total Value", f"${expected_value:,.0f}")
        with result_col3:
            st.metric("Net Gain", f"${net_gain:,.0f}")
        with result_col4:
            st.metric("Monthly Value", f"${monthly_gain:,.0f}")
        
        # Visualization of ROI timeline
        months = list(range(0, calc_timeline + 1))
        values = [-calc_investment + (monthly_gain * m) for m in months]
        
        fig_calc = go.Figure()
        
        fig_calc.add_trace(go.Scatter(
            x=months,
            y=values,
            mode='lines+markers',
            name='Cumulative Value',
            fill='tozeroy',
            fillcolor='rgba(46, 204, 113, 0.1)',
            line=dict(width=3, color='#2ECC71')
        ))
        
        # Add break-even line
        fig_calc.add_hline(y=0, line_dash="dash", line_color="gray",
                          annotation_text="Break-even", annotation_position="right")
        
        # Find break-even point
        breakeven_month = calc_investment / monthly_gain
        fig_calc.add_vline(x=breakeven_month, line_dash="dash", line_color="red",
                          annotation_text=f"Break-even: {breakeven_month:.1f} months")
        
        fig_calc.update_layout(
            title='ROI Timeline Projection',
            xaxis_title='Months',
            yaxis_title='Cumulative Value ($)',
            height=300
        )
        
        st.plotly_chart(fig_calc, use_container_width=True)

# Contextual insights section - Enhanced with all new findings
st.subheader("💡 Key Research Findings")

if "2025" in data_year:
    st.write("🚀 **2024-2025 AI Acceleration (AI Index Report 2025)**")
    
    # Create insight tabs for better organization
    insight_tabs = st.tabs(["📊 Adoption", "💰 Investment", "🏭 Industry", "👥 Labor", "🌍 Global"])
    
    with insight_tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**📈 Adoption Explosion:**")
            st.write("• Overall AI: **55% → 78%** in one year")
            st.write("• GenAI: **33% → 71%** (more than doubled)")
            st.write("• AI now in **central role** for business value")
            st.write("• **Fastest** tech adoption in history")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**🎯 Function Leadership:**")
            st.write("• **Marketing & Sales:** 42% GenAI adoption")
            st.write("• **71%** report revenue gains")
            st.write("• **Service Operations:** 49% report cost savings")
            st.write("• Benefits typically **<10%** savings, **<5%** revenue")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with insight_tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**💵 Investment Records:**")
            st.write("• Total: **$252.3B** (+44.5% YoY)")
            st.write("• GenAI: **$33.9B** (20% of all AI)")
            st.write("• **13x growth** since 2014")
            st.write("• US leads: **$109.1B** (12x China)")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**💸 Cost Revolution:**")
            st.write("• **280x cheaper** inference since 2022")
            st.write("• $20 → $0.07 per million tokens")
            st.write("• Hardware: **43%** annual performance gain")
            st.write("• Energy efficiency: **+40%** annually")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with insight_tabs[2]:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**🏢 Industry Dynamics:**")
        st.write("• **Technology sector:** 92% adoption, 4.2x ROI")
        st.write("• **Financial services:** 85% adoption, 3.8x ROI")
        st.write("• **GenAI apps** now lead: content generation (65%), code generation (58%)")
        st.write("• **Full tech stack** (AI+Cloud+Digital) shows 3.5x ROI vs 1.5x for AI alone")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with insight_tabs[3]:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**👷 Workforce Impact:**")
        st.write("• **60%** expect job changes within 5 years")
        st.write("• **36%** believe AI will replace their jobs")
        st.write("• **Gen Z** (67%) vs **Boomers** (49%) on job impact")
        st.write("• AI helps **low-skilled workers most** (14% productivity gain)")
        st.write("• **Skill gaps narrowing** - potential for reduced inequality")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with insight_tabs[4]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**🌏 Regional Competition:**")
            st.write("• **Greater China:** +27pp growth")
            st.write("• **Europe:** +23pp growth")
            st.write("• **North America:** 82% adoption (highest)")
            st.write("• Competition **intensifying** globally")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("**🌱 Environmental Impact:**")
            st.write("• Training emissions **increasing exponentially**")
            st.write("• Llama 3.1: **8,930 tons** CO₂")
            st.write("• Driving **nuclear energy** deals")
            st.write("• Major tech securing clean energy")
            st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.write("📊 **2018 Early AI Adoption Era**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**🏭 Industry Leadership:**")
        st.write("• **Manufacturing & Information** sectors led at ~12%")
        st.write("• Strong **correlation with firm size**")
        st.write("• **Technology complementarity** crucial")
        st.write("• Cloud + AI shows higher returns")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("**📍 Geographic Patterns:**")
        st.write("• **SF Bay Area** leads at 9.5%")
        st.write("• **Emerging hubs:** Nashville, San Antonio")
        st.write("• Strong **urban concentration**")
        st.write("• Midwest and rural areas lagging")
        st.markdown('</div>', unsafe_allow_html=True)

# Data sources and methodology - Enhanced
with st.expander("📚 Data Sources & Methodology"):
    source_tabs = st.tabs(["Primary Sources", "Methodology", "Data Quality", "Updates"])
    
    with source_tabs[0]:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **AI Index Report 2025**  
            Stanford HAI  
            - Global AI metrics  
            - Investment & adoption data  
            - Productivity research  
            - Environmental impact  
            [View Report](https://aiindex.stanford.edu)
            """)
            
        with col2:
            st.markdown("""
            **McKinsey Global Survey**  
            July 2024 Survey  
            - 1,491 participants  
            - 101 nations covered  
            - All organization levels  
            - Function-specific data  
            [View Report](https://www.mckinsey.com)
            """)
            
        with col3:
            st.markdown("""
            **OECD AI Observatory**  
            OECD/BCG/INSEAD 2025  
            - 840 enterprises  
            - G7 + Brazil  
            - Policy focus  
            - Success factors  
            [View Report](https://oecd.ai)
            """)
    
    with source_tabs[1]:
        st.write("**Research Methodology:**")
        st.write("• **Survey Methods:** Large-scale enterprise surveys with statistical weighting")
        st.write("• **Data Collection:** Q3 2024 - Q1 2025 for most recent data")
        st.write("• **Adoption Definition:** Includes any AI use (pilots, experiments, production)")
        st.write("• **Geographic Coverage:** Global with focus on developed economies")
        st.write("• **Sector Classification:** Standard industry codes (NAICS/ISIC)")
    
    with source_tabs[2]:
        quality_metrics = pd.DataFrame({
            'Source': ['AI Index 2025', 'McKinsey Survey', 'OECD Report', 'Census Data'],
            'Sample Size': ['Global aggregate', '1,491 firms', '840 firms', '850,000 firms'],
            'Confidence Level': ['95%', '95%', '95%', '99%'],
            'Margin of Error': ['±2%', '±3%', '±3.5%', '±0.5%']
        })
        st.dataframe(quality_metrics, hide_index=True)
    
    with source_tabs[3]:
        st.write("**Latest Updates:**")
        st.write("• **June 2025:** Integrated AI Index Report 2025 findings")
        st.write("• **May 2025:** Added industry-specific 2025 data")
        st.write("• **April 2025:** Enhanced financial impact analysis")
        st.write("• **March 2025:** Added skill gap and governance metrics")

# Footer - Enhanced with trust indicators
st.markdown("---")

# Trust and quality indicators
trust_cols = st.columns(5)

with trust_cols[0]:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>📊 Data Quality</h4>
        <div style='background-color: #28a745; color: white; padding: 8px; border-radius: 20px; display: inline-block;'>
            ✓ Verified Sources
        </div>
    </div>
    """, unsafe_allow_html=True)

with trust_cols[1]:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>🔄 Update Status</h4>
        <div style='color: #28a745;'>
            ✅ June 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

with trust_cols[2]:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>📈 Coverage</h4>
        <div>
            Global Scope<br>
            <small>101+ countries</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with trust_cols[3]:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>🔍 Transparency</h4>
        <div>
            Open Source<br>
            <small>MIT License</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with trust_cols[4]:
    st.markdown("""
    <div style='text-align: center;'>
        <h4>🔒 Privacy</h4>
        <div style='color: #28a745;'>
            GDPR Compliant<br>
            <small>No tracking</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Enhanced footer with resources
footer_cols = st.columns(4)

with footer_cols[0]:
    st.markdown("""
    ### 📚 Resources
    - [📖 GitHub Repository](https://github.com/Rcasanova25/AI-Adoption-Dashboard)
    - [🚀 Live Dashboard](https://ai-adoption-dashboard.streamlit.app/)
    - [📊 View Source Code](https://github.com/Rcasanova25/AI-Adoption-Dashboard/blob/main/app.py)
    - [🐛 Report Issues](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues)
    - [📄 Documentation](https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki)
    """)

with footer_cols[1]:
    st.markdown("""
    ### Research Partners
    - [Stanford HAI](https://hai.stanford.edu)
    - [AI Index Report](https://aiindex.stanford.edu)
    - [McKinsey AI](https://www.mckinsey.com/capabilities/quantumblack)
    - [OECD.AI](https://oecd.ai)
    - [MIT CSAIL](https://www.csail.mit.edu)
    """)

with footer_cols[2]:
    st.markdown("""
    ### Connect
    - [LinkedIn - Robert Casanova](https://linkedin.com/in/robert-casanova)
    - [GitHub - @Rcasanova25](https://github.com/Rcasanova25)
    - [Email](mailto:Robert.casanova82@gmail.com)
    - [Twitter/X](https://twitter.com)
    - [Star on GitHub](https://github.com/Rcasanova25/AI-Adoption-Dashboard)
    """)

with footer_cols[3]:
    st.markdown("""
    ### Support
    - [User Guide](https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki/User-Guide)
    - [FAQ](https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki/FAQ)
    - [Report Bug](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=bug)
    - [Request Feature](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=enhancement)
    - [Discussions](https://github.com/Rcasanova25/AI-Adoption-Dashboard/discussions)
    """)

# Final attribution
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px 20px 20px 20px; margin-top: 40px; border-top: 1px solid #ddd;'>
    <p style='font-size: 20px; margin-bottom: 10px;'>
        🤖 <strong>AI Adoption Dashboard</strong> v2.2.0
    </p>
    <p style='margin-bottom: 5px; font-size: 16px;'>
        Comprehensive AI adoption insights from 2018 to 2025
    </p>
    <p style='font-size: 14px; color: #888; margin-top: 15px;'>
        Enhanced with AI Index Report 2025 findings | Last updated: June 17, 2025
    </p>
    <p style='font-size: 14px; margin-top: 20px;'>
        Created by <a href='https://linkedin.com/in/robert-casanova' style='color: #1f77b4;'>Robert Casanova</a> | 
        Powered by <a href='https://streamlit.io' style='color: #1f77b4;'>Streamlit</a> & 
        <a href='https://plotly.com' style='color: #1f77b4;'>Plotly</a> | 
        <a href='https://github.com/Rcasanova25/AI-Adoption-Dashboard/blob/main/LICENSE' style='color: #1f77b4;'>MIT License</a>
    </p>
    <p style='font-size: 12px; margin-top: 15px; color: #999;'>
        <i>Data sources: AI Index Report 2025 (Stanford HAI), McKinsey Global Survey on AI, OECD AI Policy Observatory</i>
    </p>
</div>
""", unsafe_allow_html=True)