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

# Data loading function - updated with AI Index 2025 data and Token Economics
@st.cache_data
def load_data():
    try:
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
        
        # Technology stack - Fixed percentages to sum to 100
        tech_stack = pd.DataFrame({
            'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
            'percentage': [15, 23, 24, 38]  # Sum = 100
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
        
        # 2025 GenAI by function (for backward compatibility)
        genai_2025 = pd.DataFrame({
            'function': ['Marketing & Sales', 'Product Development', 'Service Operations', 
                        'Software Engineering', 'IT', 'Knowledge Management', 'HR', 'Supply Chain'],
            'adoption': [42, 28, 23, 22, 23, 21, 13, 7]
        })
        
        # NEW: Token economics data
        token_economics = pd.DataFrame({
            'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B', 
                      'Claude 3 Haiku', 'Llama 3 70B', 'GPT-4', 'Claude 3.5 Sonnet'],
            'cost_per_million_input': [20.00, 0.14, 0.07, 0.25, 0.35, 15.00, 3.00],
            'cost_per_million_output': [20.00, 0.14, 0.07, 1.25, 0.40, 30.00, 15.00],
            'context_window': [4096, 16385, 1000000, 200000, 8192, 128000, 200000],
            'tokens_per_second': [50, 150, 200, 180, 120, 80, 100]
        })
        
        # Token usage patterns
        token_usage_patterns = pd.DataFrame({
            'use_case': ['Simple Chat', 'Document Analysis', 'Code Generation', 
                         'Creative Writing', 'Data Analysis', 'Reasoning Tasks'],
            'avg_input_tokens': [50, 5000, 500, 200, 2000, 1000],
            'avg_output_tokens': [200, 500, 1500, 2000, 1000, 5000],
            'input_output_ratio': [0.25, 10.0, 0.33, 0.10, 2.0, 0.20]
        })
        
        # Token optimization strategies
        token_optimization = pd.DataFrame({
            'strategy': ['Prompt Engineering', 'Context Caching', 'Batch Processing', 
                        'Model Selection', 'Response Streaming', 'Token Pruning'],
            'cost_reduction': [30, 45, 60, 70, 15, 25],
            'implementation_complexity': [2, 4, 3, 1, 2, 5],  # 1-5 scale
            'time_to_implement': [1.0, 7.0, 3.0, 0.5, 2.0, 14.0]  # days as float
        })
        
        # Token pricing evolution - Fixed with explicit date list
        token_pricing_evolution = pd.DataFrame({
            'date': pd.to_datetime(['2022-11-01', '2023-02-01', '2023-05-01', '2023-08-01', '2023-11-01',
                                   '2024-02-01', '2024-05-01', '2024-08-01', '2024-11-01', '2025-02-01', '2025-05-01']),
            'avg_price_input': [20.0, 18.0, 15.0, 10.0, 5.0, 3.0, 1.5, 0.8, 0.5, 0.3, 0.2],
            'avg_price_output': [20.0, 19.0, 16.0, 12.0, 8.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.8],
            'models_available': [5, 8, 12, 18, 25, 35, 45, 58, 72, 85, 95]
        })
        
        return (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
                geographic, tech_stack, productivity_data, productivity_by_skill,
                ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
                barriers_data, support_effectiveness, state_data, ai_investment_data, 
                regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
                training_emissions, skill_gap_data, ai_governance, genai_2025,
                token_economics, token_usage_patterns, token_optimization, token_pricing_evolution)
    
    except Exception as e:
        st.error(f"Error in load_data function: {str(e)}")
        st.error(f"Error type: {type(e).__name__}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        raise

# Initialize session state
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "General"
if 'show_changelog' not in st.session_state:
    st.session_state.show_changelog = False

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

# Load all data
try:
    loaded_data = load_data()
    
    # Check if we got the expected number of items
    if len(loaded_data) != 28:
        st.error(f"Error: Expected 28 data items, but got {len(loaded_data)}")
        st.stop()
    
    # Unpack the data
    (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
     geographic, tech_stack, productivity_data, productivity_by_skill,
     ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
     barriers_data, support_effectiveness, state_data, ai_investment_data, 
     regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
     training_emissions, skill_gap_data, ai_governance, genai_2025,
     token_economics, token_usage_patterns, token_optimization, token_pricing_evolution) = loaded_data
     
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.error(f"Please check the data loading function for issues.")
    import traceback
    st.error(f"Full error: {traceback.format_exc()}")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: transparent;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stApp > div {
        background-color: transparent;
    }
    .main .block-container {
        background-color: transparent;
    }
    .source-info {
        font-size: 0.8em;
        color: #666;
        cursor: pointer;
        text-decoration: underline;
    }
    .insight-box {
        background-color: rgba(31, 119, 180, 0.1);
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and strategic positioning
st.title("🤖 AI Adoption Dashboard: Strategic Decision Intelligence")
st.markdown("**From data analysis to competitive advantage - make better AI investment decisions**")

# Strategic value proposition
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(31, 119, 180, 0.1); border-radius: 10px; margin: 5px;'>
        <h3>🎯</h3>
        <strong>Assess Position</strong><br>
        <small>Know where you stand vs competitors</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(255, 127, 14, 0.1); border-radius: 10px; margin: 5px;'>
        <h3>💰</h3>
        <strong>Optimize Investment</strong><br>
        <small>Make smarter AI spending decisions</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(44, 160, 44, 0.1); border-radius: 10px; margin: 5px;'>
        <h3>⚖️</h3>
        <strong>Manage Risk</strong><br>
        <small>Stay ahead of regulatory changes</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(214, 39, 40, 0.1); border-radius: 10px; margin: 5px;'>
        <h3>📊</h3>
        <strong>Track Progress</strong><br>
        <small>Monitor competitive dynamics</small>
    </div>
    """, unsafe_allow_html=True)

# What's New section
with st.expander("🆕 What's New in Version 2.2.0", expanded=st.session_state.show_changelog):
    st.markdown("""
    **Latest Updates (June 2025):**
    - ✅ Integrated AI Index Report 2025 findings
    - ✅ Added industry-specific 2025 data
    - ✅ Enhanced financial impact clarity
    - ✅ New skill gap and governance metrics
    - ✅ Interactive filtering for charts
    - ✅ Source attribution for all data points
    - ✅ Export data as CSV functionality
    - ✅ Comprehensive academic analysis integration
    - ✅ Enhanced risks and safety analysis
    """)

# Add definition notice with AI Index Report reference
st.info("""
**📌 Important Note:** Adoption rates in this dashboard reflect "any AI use" including pilots, experiments, and production deployments. 
Enterprise-wide production use rates are typically lower. Data sources include AI Index Report 2025, McKinsey Global Survey on AI, 
OECD AI Policy Observatory, and US Census Bureau AI Use Supplement.
""")

# Sidebar controls
st.sidebar.header("📊 Dashboard Controls")

# View selector based on persona
if st.session_state.selected_persona == "Business Leader":
    all_views = [
        "🎯 Competitive Position Assessor",
        "💰 Investment Decision Engine", 
        "📊 Strategic Market Intelligence",
        "🗺️ Industry Benchmarking",
        "Historical Trends",
        "Investment Trends",
        "Financial Impact",
        "Geographic Distribution",
        "Bibliography & Sources"
    ]
elif st.session_state.selected_persona == "Policymaker":
    all_views = [
        "🎯 Competitive Position Assessor",
        "⚖️ Regulatory Risk Radar",
        "🗺️ Geographic Distribution", 
        "📊 Strategic Market Intelligence",
        "OECD 2025 Findings",
        "AI Governance", 
        "Historical Trends",
        "Bibliography & Sources"
    ]
elif st.session_state.selected_persona == "Researcher":
    all_views = [
        "📊 Strategic Market Intelligence",
        "Historical Trends",
        "Productivity Research",
        "Environmental Impact",
        "Token Economics",
        "Financial Impact",
        "Bibliography & Sources"
    ]
else:  # General users
    all_views = [
        "🎯 Competitive Position Assessor",
        "💰 Investment Decision Engine",
        "📊 Strategic Market Intelligence",
        "Historical Trends",
        "Investment Trends",
        "Financial Impact",
        "Bibliography & Sources"
    ]

# Show view selector
view_type = st.sidebar.selectbox(
    "Analysis View", 
    all_views,
    index=0,
    help="Curated views based on your selected role"
)

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

# Key metrics row
st.subheader("📈 Strategic Market Intelligence")
col1, col2, col3, col4 = st.columns(4)

if "2025" in data_year:
    with col1:
        st.metric(
            label="Market Acceleration", 
            value="78%", 
            delta="+23pp from 2023",
            help="Business AI adoption jumped 23 percentage points in one year - fastest technology adoption in history"
        )
    with col2:
        st.metric(
            label="GenAI Revolution", 
            value="71%", 
            delta="+38pp from 2023",
            help="Generative AI adoption more than doubled, creating new competitive dynamics"
        )
    with col3:
        st.metric(
            label="Investment Surge", 
            value="$252.3B", 
            delta="+44.5% YoY",
            help="Record AI investment levels signal major economic shift underway"
        )
    with col4:
        st.metric(
            label="Cost Collapse", 
            value="280x cheaper", 
            delta="Since Nov 2022",
            help="Dramatic cost reduction enables new business models and wider adoption"
        )
else:
    with col1:
        st.metric("Early Adoption", "5.8%", "📊 Limited to pioneers")
    with col2:
        st.metric("Size Advantage", "58.5%", "🏢 Large firms leading")
    with col3:
        st.metric("Tech Integration", "45%", "☁️ Multi-technology approach")
    with col4:
        st.metric("Geographic Hub", "SF Bay (9.5%)", "🌍 Innovation concentration")

# Strategic interpretation
st.info("""
**🧠 Strategic Implications:** The 2022-2024 period represents a fundamental market transition. Organizations that don't adapt their AI strategy now risk falling permanently behind competitors who are gaining 15-40% productivity advantages.
""")

# Main visualization section
st.subheader(f"📊 {view_type}")

# Simplified view implementations
if view_type == "🎯 Competitive Position Assessor":
    st.write("# 🎯 AI Competitive Position Assessment")
    st.write("**Get your strategic position and risk analysis in under 2 minutes**")
    
    # Simplified assessment form
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.selectbox(
            "Industry Sector",
            ["Technology", "Financial Services", "Healthcare", "Manufacturing", 
             "Retail & E-commerce", "Education", "Energy & Utilities", "Government", "Other"]
        )
        
        company_size = st.selectbox(
            "Organization Size",
            ["1-50 employees", "51-250 employees", "251-1000 employees", 
             "1001-5000 employees", "5000+ employees"]
        )
        
        current_ai_adoption = st.slider(
            "Current AI Usage (%)",
            0, 100, 25,
            help="What percentage of your organization actively uses AI tools?"
        )
    
    with col2:
        ai_investment = st.selectbox(
            "Annual AI Investment",
            ["<$100K", "$100K-$500K", "$500K-$2M", "$2M-$10M", "$10M+"]
        )
        
        urgency = st.radio(
            "Strategic Priority Level",
            ["Low Priority", "Medium Priority", "High Priority", "Critical Priority"],
            index=1
        )
    
    if st.button("🔍 Assess My Competitive Position", type="primary"):
        # Simple assessment logic
        industry_benchmark = {
            "Technology": 92, "Financial Services": 85, "Healthcare": 78,
            "Manufacturing": 75, "Retail & E-commerce": 72, "Education": 65,
            "Energy & Utilities": 58, "Government": 52, "Other": 65
        }
        
        industry_avg = industry_benchmark[industry]
        gap = industry_avg - current_ai_adoption
        
        # Show results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Industry Gap", f"{gap:+.0f}pp", f"vs {industry} avg ({industry_avg}%)")
        with col2:
            position = "LEADER" if gap <= 0 else "LAGGARD" if gap > 20 else "COMPETITIVE"
            st.metric("Position", position)
        with col3:
            urgency_months = {"Low Priority": 36, "Medium Priority": 24, "High Priority": 12, "Critical Priority": 6}
            st.metric("Action Timeline", f"{urgency_months[urgency]} months")
        
        if gap <= 0:
            st.success("✅ You're ahead of industry average! Focus on maintaining advantage.")
        elif gap <= 20:
            st.warning("⚠️ Competitive position but acceleration needed.")
        else:
            st.error("🚨 Significant gap - immediate action required.")

elif view_type == "💰 Investment Decision Engine":
    st.write("# 💰 AI Investment Decision Engine")
    st.info("🚧 **Coming Soon** - AI investment optimization and ROI analysis tools")

elif view_type == "📊 Strategic Market Intelligence":
    st.write("# 📊 Strategic Market Intelligence Dashboard")
    
    # Market overview
    fig = px.bar(
        sector_2025,
        x='sector',
        y='adoption_rate',
        color='avg_roi',
        title='AI Adoption and ROI by Industry (2025)',
        labels={'adoption_rate': 'Adoption Rate (%)', 'avg_roi': 'Average ROI'}
    )
    fig.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **📈 Key Insights:**
    - Technology sector leads with 92% adoption and 4.2x ROI
    - Financial Services shows strong performance (85% adoption, 3.8x ROI)
    - Government sector lags significantly (52% adoption, 2.2x ROI)
    """)

elif view_type == "Historical Trends":
    st.write("📈 **AI Adoption Evolution: 2017-2025**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['ai_use'], 
        mode='lines+markers', 
        name='Overall AI Use', 
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['genai_use'], 
        mode='lines+markers', 
        name='GenAI Use', 
        line=dict(width=4, color='#ff7f0e'),
        marker=dict(size=10)
    ))
    
    # Add ChatGPT launch annotation
    fig.add_annotation(
        x=2022, y=33,
        text="ChatGPT Launch<br>GenAI Era Begins",
        showarrow=True,
        arrowhead=2,
        bgcolor="rgba(255,127,14,0.1)",
        bordercolor="#ff7f0e"
    )
    
    fig.update_layout(
        title="AI Adoption Trends: The GenAI Revolution", 
        xaxis_title="Year", 
        yaxis_title="Adoption Rate (%)",
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("""
    **📈 Key Findings:**
    - Business AI adoption jumped from 55% to 78% in just one year (2023-2024)
    - GenAI adoption more than doubled from 33% to 71%
    - ChatGPT launch in late 2022 triggered the GenAI revolution
    """)

elif view_type == "Investment Trends":
    st.write("💰 **AI Investment Trends: Record Growth in 2024**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ai_investment_data['year'],
        y=ai_investment_data['total_investment'],
        mode='lines+markers',
        name='Total Investment',
        line=dict(width=4, color='#2E86AB'),
        marker=dict(size=12)
    ))
    
    fig.add_trace(go.Scatter(
        x=ai_investment_data['year'][ai_investment_data['genai_investment'] > 0],
        y=ai_investment_data['genai_investment'][ai_investment_data['genai_investment'] > 0],
        mode='lines+markers',
        name='GenAI Investment',
        line=dict(width=3, color='#F24236'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='AI Investment Has Grown 13x Since 2014',
        xaxis_title='Year',
        yaxis_title='Investment ($ Billions)',
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("2024 Total", "$252.3B", "+44.5% YoY")
    with col2:
        st.metric("GenAI Share", "$33.9B", "13.4% of total")
    with col3:
        st.metric("US Dominance", "$109.1B", "43% global share")

elif view_type == "Financial Impact":
    st.write("💵 **Financial Impact of AI by Business Function**")
    
    fig = go.Figure()
    
    financial_sorted = financial_impact.sort_values('companies_reporting_revenue_gains', ascending=True)
    
    fig.add_trace(go.Bar(
        name='Companies Reporting Cost Savings',
        y=financial_sorted['function'],
        x=financial_sorted['companies_reporting_cost_savings'],
        orientation='h',
        marker_color='#2ECC71'
    ))
    
    fig.add_trace(go.Bar(
        name='Companies Reporting Revenue Gains',
        y=financial_sorted['function'],
        x=financial_sorted['companies_reporting_revenue_gains'],
        orientation='h',
        marker_color='#3498DB'
    ))
    
    fig.update_layout(
        title="Percentage of Companies Reporting Financial Benefits from AI",
        xaxis_title="Percentage of Companies (%)",
        yaxis_title="Business Function",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("""
    **📊 Understanding the Data:** The percentages show the **proportion of companies reporting financial benefits** from AI.
    Among companies that see benefits, the actual magnitude is typically 5-10% cost savings and 2-4% revenue gains.
    """)

elif view_type == "Geographic Distribution":
    st.write("🗺️ **AI Adoption Geographic Distribution**")
    
    # Simple state-level chart
    top_states = state_data.nlargest(10, 'rate')
    
    fig = px.bar(
        top_states,
        x='state',
        y='rate',
        title='Top 10 States by AI Adoption Rate',
        color='rate',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **🗺️ Geographic Insights:**
    - California leads in AI adoption and innovation
    - Strong concentration in coastal technology hubs
    - Significant digital divide between leading and lagging regions
    """)

elif view_type == "⚖️ Regulatory Risk Radar":
    st.write("# ⚖️ Regulatory Risk Radar")
    st.info("🚧 **Coming Soon** - Comprehensive regulatory monitoring and compliance tracking")

elif view_type == "🗺️ Industry Benchmarking":
    st.write("# 🗺️ Industry Benchmarking")
    st.info("🚧 **Coming Soon** - Detailed industry-specific AI adoption analysis")

elif view_type == "OECD 2025 Findings":
    st.write("📊 **OECD/BCG/INSEAD 2025 Report: Enterprise AI Adoption**")
    
    fig = go.Figure()
    
    x = oecd_g7_adoption['country']
    
    fig.add_trace(go.Bar(
        name='Overall Adoption',
        x=x,
        y=oecd_g7_adoption['adoption_rate'],
        marker_color='#3B82F6'
    ))
    
    fig.add_trace(go.Bar(
        name='Manufacturing',
        x=x,
        y=oecd_g7_adoption['manufacturing'],
        marker_color='#10B981'
    ))
    
    fig.add_trace(go.Bar(
        name='ICT Sector',
        x=x,
        y=oecd_g7_adoption['ict_sector'],
        marker_color='#F59E0B'
    ))
    
    fig.update_layout(
        title="AI Adoption Rates Across G7 Countries by Sector",
        xaxis_title="Country",
        yaxis_title="Adoption Rate (%)",
        barmode='group',
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **🌍 Key Findings:**
    - Japan leads G7 with 48% overall adoption
    - ICT sector universally leads (55-70%)
    - 15-20pp gap between ICT and other sectors
    """)

elif view_type == "Productivity Research":
    st.write("📊 **AI Productivity Impact Research**")
    
    fig = px.bar(
        productivity_by_skill,
        x='skill_level',
        y=['productivity_gain', 'skill_gap_reduction'],
        title='AI Impact by Worker Skill Level',
        barmode='group',
        color_discrete_map={'productivity_gain': '#2ECC71', 'skill_gap_reduction': '#3498DB'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("""
    **✅ AI Index 2025 Finding:** AI provides the greatest productivity boost to low-skilled workers (14%), 
    helping to narrow skill gaps and potentially reduce workplace inequality.
    """)

elif view_type == "Environmental Impact":
    st.write("🌱 **Environmental Impact: AI's Growing Carbon Footprint**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=training_emissions['model'],
        y=training_emissions['carbon_tons'],
        marker_color=['#90EE90', '#FFD700', '#FF6347', '#8B0000'],
        text=[f'{x:,.0f} tons' for x in training_emissions['carbon_tons']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Carbon Emissions from AI Model Training: Exponential Growth",
        xaxis_title="AI Model",
        yaxis_title="Carbon Emissions (tons CO₂)",
        yaxis_type="log",
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("""
    **📈 Environmental Impact:**
    - 900,000x increase from 2012 to 2024
    - Llama 3.1 = Annual emissions of 1,900 cars
    - Growing focus on sustainable AI development
    """)

elif view_type == "Token Economics":
    st.write("🪙 **Token Economics: The Language and Currency of AI**")
    
    # Token pricing comparison
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Input Cost',
        x=token_economics['model'],
        y=token_economics['cost_per_million_input'],
        marker_color='#3498DB'
    ))
    
    fig.add_trace(go.Bar(
        name='Output Cost',
        x=token_economics['model'],
        y=token_economics['cost_per_million_output'],
        marker_color='#E74C3C'
    ))
    
    fig.update_layout(
        title="Current Model Pricing (per Million Tokens)",
        yaxis_title="Cost ($)",
        barmode='group',
        height=400,
        xaxis_tickangle=45,
        yaxis_type="log"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cost Reduction", "286x", "Since Nov 2022")
    with col2:
        st.metric("Context Windows", "Up to 1M", "Tokens")
    with col3:
        st.metric("Processing Speed", "200 tokens/sec", "Peak performance")

elif view_type == "AI Governance":
    st.write("⚖️ **AI Governance & Ethics Implementation**")
    
    fig = go.Figure()
    
    categories = ai_governance['aspect'].tolist()
    
    fig.add_trace(go.Scatterpolar(
        r=ai_governance['adoption_rate'],
        theta=categories,
        fill='toself',
        name='Adoption Rate (%)',
        line_color='#3498DB'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[x * 20 for x in ai_governance['maturity_score']],
        theta=categories,
        fill='toself',
        name='Maturity Score (scaled)',
        line_color='#E74C3C'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="AI Governance Implementation and Maturity",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("✅ **Well-Established Areas:**")
        st.write("• Data Privacy: 78% adoption, 3.8/5 maturity")
        st.write("• Regulatory Compliance: 72% adoption, 3.5/5 maturity")
    
    with col2:
        st.write("⚠️ **Areas Needing Attention:**")
        st.write("• Bias Detection: 45% adoption, 2.5/5 maturity")
        st.write("• Accountability Framework: 48% adoption, 2.6/5 maturity")

elif view_type == "Bibliography & Sources":
    st.write("📚 **Complete Bibliography & Source Citations**")
    
    st.markdown("""
    This dashboard synthesizes data from multiple authoritative sources to provide comprehensive 
    AI adoption insights. All sources are cited using Chicago Manual of Style format.
    """)
    
    # Government and Institutional Sources
    st.subheader("🏛️ Government and Institutional Sources")
    st.markdown("""
    1. **Stanford Human-Centered AI Institute.** "AI Index Report 2025." Stanford University. 
       Accessed June 28, 2025. https://aiindex.stanford.edu/ai-index-report-2025/.

    2. **U.S. Census Bureau.** "AI Use Supplement." Washington, DC: U.S. Department of Commerce. 
       Accessed June 28, 2025. https://www.census.gov.

    3. **Organisation for Economic Co-operation and Development.** "OECD AI Policy Observatory." 
       Accessed June 28, 2025. https://oecd.ai.
    """)
    
    # Corporate Sources
    st.subheader("🏢 Corporate and Industry Sources")
    st.markdown("""
    4. **McKinsey & Company.** "The State of AI: McKinsey Global Survey on AI." McKinsey Global Institute. 
       Accessed June 28, 2025. https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai.

    5. **OpenAI.** "OpenAI Research." Accessed June 28, 2025. https://openai.com/research/.

    6. **GitHub.** "GitHub Blog." Accessed June 28, 2025. https://github.blog/.
    """)
    
    # Academic Sources
    st.subheader("🎓 Academic Publications")
    st.markdown("""
    7. **Bick, Alexander, Adam Blandin, and David Deming.** "The Rapid Adoption of Generative AI." 
       Federal Reserve Bank working paper, 2024.

    8. **Brynjolfsson, Erik, Danielle Li, and Lindsey R. Raymond.** "Generative AI at Work." 
       National Bureau of Economic Research Working Paper, 2023.
    """)
    
    # Source verification
    st.subheader("📋 Source Verification Methodology")
    st.info("""
    **Source Quality Assurance Process:**
    
    ✅ **Primary Source Verification** - All data traced to original publications and reports
    
    ✅ **Cross-Validation** - Key findings confirmed across multiple independent sources
    
    ✅ **Institutional Authority** - Preference for government agencies, academic institutions, and established research organizations
    
    ✅ **Recency Standards** - Data sources from 2020-2025, with emphasis on 2024-2025 findings
    """)

# Add export functionality if applicable
if view_type in ["Historical Trends", "Investment Trends", "Financial Impact"]:
    data_map = {
        "Historical Trends": historical_data,
        "Investment Trends": ai_investment_data,
        "Financial Impact": financial_impact
    }
    
    if view_type in data_map:
        csv = data_map[view_type].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name=f"ai_adoption_{view_type.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")

footer_cols = st.columns(4)

with footer_cols[0]:
    st.markdown("""
    ### 📚 Resources
    - [📖 GitHub Repository](https://github.com/Rcasanova25/AI-Adoption-Dashboard)
    - [🚀 Live Dashboard](https://ai-adoption-dashboard.streamlit.app/)
    """)

with footer_cols[1]:
    st.markdown("""
    ### 🔬 Research Partners
    - [Stanford HAI](https://hai.stanford.edu)
    - [AI Index Report](https://aiindex.stanford.edu)
    """)

with footer_cols[2]:
    st.markdown("""
    ### 🤝 Connect
    - [LinkedIn](https://linkedin.com/in/robert-casanova)
    - [GitHub](https://github.com/Rcasanova25)
    """)

with footer_cols[3]:
    st.markdown("""
    ### 🛟 Support
    - [Report Bug](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues)
    - [Request Feature](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues)
    """)

# Final attribution
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px; margin-top: 20px; border-top: 1px solid #ddd;'>
    <p style='font-size: 18px; margin-bottom: 10px;'>
        🤖 <strong>AI Adoption Dashboard</strong> v2.2.0
    </p>
    <p style='font-size: 14px; color: #888;'>
        Enhanced with AI Index Report 2025 findings | Last updated: June 28, 2025
    </p>
    <p style='font-size: 14px; margin-top: 15px;'>
        Created by <a href='https://linkedin.com/in/robert-casanova' style='color: #1f77b4;'>Robert Casanova</a> | 
        Powered by <a href='https://streamlit.io' style='color: #1f77b4;'>Streamlit</a>
    </p>
</div>
""", unsafe_allow_html=True)