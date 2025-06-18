[⚠️ Suspicious Content] import streamlit as st
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
    """
    Loads all necessary dataframes for the AI Adoption Dashboard.
    Data includes historical trends, sector-specific adoption, firm size,
    AI maturity, geographic distribution, technology stack, productivity,
    environmental impact, financial impact, labor impact, skill gaps,
    AI governance, and new token economics data.
    """
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
    
    # Technology stack - FIXED percentages to sum to 100
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
    
    # Token pricing evolution - Fixed date range issue
    dates = pd.date_range('2022-11-01', '2025-06-01', freq='Q').tolist()
    token_pricing_evolution = pd.DataFrame({
        'date': dates,
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
        },
        'nvidia': { # Added this source to the second code where it was missing
            'title': 'AI Tokens Explained',
            'org': 'NVIDIA Blog',
            'url': 'https://blogs.nvidia.com/blog/ai-tokens-explained/',
            'methodology': 'Insights on AI tokens and their processing'
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
    
    # Unpack the data - ENSURING ALL DATA IS UNPACKED
    (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
     geographic, tech_stack, productivity_data, productivity_by_skill,
     ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
     barriers_data, support_effectiveness, state_data, ai_investment_data, 
     regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
     training_emissions, skill_gap_data, ai_governance, genai_2025,
     token_economics, token_usage_patterns, token_optimization, token_pricing_evolution) = loaded_data
     
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
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

# Title and description
st.title("🤖 AI Adoption Dashboard: 2018-2025")
st.markdown("**Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)**")

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
    - ✅ **New: AI Token Cost Trends analysis view**
    - ✅ **New: Token Economics analysis view**
    """)

# Add definition notice with AI Index Report reference
st.info("""
**📌 Important Note:** Adoption rates in this dashboard reflect "any AI use" including pilots, experiments, and production deployments. 
Enterprise-wide production use rates are typically lower. Data sources include AI Index Report 2025, McKinsey Global Survey on AI, 
OECD AI Policy Observatory, US Census Bureau AI Use Supplement, and NVIDIA.
""")

# Sidebar controls
st.sidebar.header("📊 Dashboard Controls")

# Show persona selection
persona = st.sidebar.selectbox(
    "Select Your Role",
    ["General", "Business Leader", "Policymaker", "Researcher"],
    index=["General", "Business Leader", "Policymaker", "Researcher"].index(st.session_state.selected_persona)
)
st.session_state.selected_persona = persona

# Persona-based view recommendations and filtering
persona_views = {
    "Business Leader": ["Industry Analysis", "Financial Impact", "Investment Trends", "ROI Analysis", "AI Token Cost Trends", "Token Economics"],
    "Policymaker": ["Geographic Distribution", "OECD 2025 Findings", "Regional Growth", "AI Governance"],
    "Researcher": ["Historical Trends", "Productivity Research", "Environmental Impact", "Skill Gap Analysis", "AI Token Cost Trends", "Token Economics"],
    "General": ["Adoption Rates", "Historical Trends", "Investment Trends", "Labor Impact", "AI Token Cost Trends", "Token Economics"]
}

# Filter views based on persona
all_views = ["Adoption Rates", "Historical Trends", "Industry Analysis", "Investment Trends", 
             "Regional Growth", "AI Cost Trends", "Token Economics", "Financial Impact", "Labor Impact", 
             "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
             "Productivity Research", "Environmental Impact", "Geographic Distribution", 
             "OECD 2025 Findings", "Barriers & Support", "ROI Analysis", "Skill Gap Analysis", 
             "AI Governance", "AI Token Cost Trends"] # Ensure all views are present and in desired order

if persona != "General":
    st.sidebar.info(f"💡 **Recommended views for {persona}:**\n" + "\n".join([f"• {v}" for v in persona_views[persona]]))

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

# Fix: Ensure the selected view is correctly initialized based on persona and exists in all_views
view_type = st.sidebar.selectbox(
    "Analysis View", 
    all_views,
    index=all_views.index(persona_views[persona][0]) if persona_views[persona][0] in all_views else 0
)

# Advanced filters
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Advanced Options")

# Year filter for historical data
if view_type == "Historical Trends":
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=2017,
        max_value=2025,
        value=(2017, 2025),
        step=1
    )
    
    compare_mode = st.sidebar.checkbox("Compare specific years", value=False)
    if compare_mode:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            year1 = st.selectbox("Year 1", range(2017, 2026), index=1)
        with col2:
            year2 = st.selectbox("Year 2", range(2017, 2026), index=7)

# Export functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")

export_format = st.sidebar.selectbox(
    "Export Format",
    ["PNG Image", "CSV Data", "PDF Report (Beta)"]
)

if st.sidebar.button("📥 Export Current View", help="Download the current visualization"):
    if export_format == "CSV Data":
        # Export current data based on view
        if view_type == "Historical Trends":
            csv = historical_data.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_adoption_{view_type.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
        elif view_type == "AI Token Cost Trends":
            csv = ai_cost_reduction.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_token_cost_trends.csv",
                mime="text/csv"
            )
        elif view_type == "Token Economics":
            csv = token_economics.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_token_economics.csv",
                mime="text/csv"
            )
        elif view_type == "Financial Impact":
            csv = financial_impact.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_financial_impact.csv",
                mime="text/csv"
            )
        elif view_type == "Industry Analysis":
            csv = sector_2025.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_adoption_by_industry_2025.csv",
                mime="text/csv"
            )
        elif view_type == "Investment Trends":
            csv = ai_investment_data.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_investment_trends.csv",
                mime="text/csv"
            )
        elif view_type == "Regional Growth":
            csv = regional_growth.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_regional_growth.csv",
                mime="text/csv"
            )
        elif view_type == "Labor Impact":
            csv = ai_perception.to_csv(index=False) # Or productivity_by_skill
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_labor_impact.csv",
                mime="text/csv"
            )
        elif view_type == "Firm Size Analysis":
            csv = firm_size.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_firm_size_analysis.csv",
                mime="text/csv"
            )
        elif view_type == "Technology Stack":
            csv = tech_stack.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_technology_stack.csv",
                mime="text/csv"
            )
        elif view_type == "AI Technology Maturity":
            csv = ai_maturity.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_technology_maturity.csv",
                mime="text/csv"
            )
        elif view_type == "Productivity Research":
            csv = productivity_data.to_csv(index=False) # Or other productivity DFs
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_productivity_research.csv",
                mime="text/csv"
            )
        elif view_type == "Environmental Impact":
            csv = training_emissions.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_environmental_impact.csv",
                mime="text/csv"
            )
        elif view_type == "Geographic Distribution":
            csv = geographic.to_csv(index=False) # Or state_data
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_geographic_distribution.csv",
                mime="text/csv"
            )
        elif view_type == "OECD 2025 Findings":
            csv = oecd_g7_adoption.to_csv(index=False) # Or oecd_applications
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_oecd_findings.csv",
                mime="text/csv"
            )
        elif view_type == "Barriers & Support":
            csv = barriers_data.to_csv(index=False) # Or support_effectiveness
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_barriers_support.csv",
                mime="text/csv"
            )
        elif view_type == "ROI Analysis":
            csv = sector_2025[['sector', 'avg_roi']].to_csv(index=False) # Simplified for ROI
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_roi_analysis.csv",
                mime="text/csv"
            )
        elif view_type == "Skill Gap Analysis":
            csv = skill_gap_data.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_skill_gap_analysis.csv",
                mime="text/csv"
            )
        elif view_type == "AI Governance":
            csv = ai_governance.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_governance.csv",
                mime="text/csv"
            )
        else:
            st.sidebar.warning("No specific data export defined for this view.")

        st.sidebar.success("✅ Data export initiated!")
    else:
        st.sidebar.warning("Export to PNG/PDF is not yet fully implemented. Please select CSV.")

# Feedback widget
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Feedback")
feedback = st.sidebar.text_area("Share your thoughts or request features:", height=100)
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

# Help section
with st.sidebar.expander("❓ Need Help?"):
    st.markdown("""
    **Navigation Tips:**
    - Use the Analysis View dropdown to explore different perspectives
    - Click 📊 icons for data source information
    - Hover over chart elements for details
    
    **Keyboard Shortcuts:**
    - `Ctrl + K`: Quick search
    - `F`: Toggle fullscreen
    - `?`: Show help
    """)

# Key metrics row - UPDATED with AI Index 2025 data
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

if "2025" in data_year:
    with col1:
        st.metric(
            label="Overall AI Adoption*", 
            value="78%", 
            delta="+23pp from 2023",
            help="*Includes any AI use. Jumped from 55% in 2023 (AI Index 2025)"
        )
    with col2:
        st.metric(
            label="GenAI Adoption*", 
            value="71%", 
            delta="+38pp from 2023",
            help="*More than doubled from 33% in 2023 (AI Index 2025)"
        )
    with col3:
        st.metric(
            label="2024 AI Investment", 
            value="$252.3B", 
            delta="+44.5% YoY",
            help="Total corporate AI investment reached record levels"
        )
    with col4:
        st.metric(
            label="Cost Reduction", 
            value="280x cheaper", 
            delta="Since Nov 2022",
            help="AI inference cost dropped from $20 to $0.07 per million tokens"
        )
else:
    with col1:
        st.metric("Overall AI Adoption", "5.8%", "📊 Firm-weighted")
    with col2:
        st.metric("Large Firms (5000+)", "58.5%", "🏢 High adoption")
    with col3:
        st.metric("AI + Cloud", "45%", "☁️ Technology stack")
    with col4:
        st.metric("Top City", "SF Bay (9.5%)", "🌍 Geographic leader")

# Main visualization section
st.subheader(f"📊 {view_type}")

# View implementations
if view_type == "Adoption Rates":
    st.write("📈 **Overall AI & GenAI Adoption Rates (2017-2025)**")
    
    fig = go.Figure()
    
    # Overall AI Use
    fig.add_trace(go.Bar(
        x=historical_data['year'],
        y=historical_data['ai_use'],
        name='Overall AI Use',
        marker_color='#1f77b4',
        text=[f'{x}%' for x in historical_data['ai_use']],
        textposition='outside'
    ))
    
    # GenAI Use
    fig.add_trace(go.Bar(
        x=historical_data['year'],
        y=historical_data['genai_use'],
        name='GenAI Use',
        marker_color='#ff7f0e',
        text=[f'{x}%' for x in historical_data['genai_use']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Evolution of AI and GenAI Adoption (2017-2025)",
        xaxis_title="Year",
        yaxis_title="Adoption Rate (%)",
        barmode='group',
        height=500,
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.7)', bordercolor='rgba(0,0,0,0.5)')
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="adoption_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🚀 **Adoption Insights:**")
    st.write("• A dramatic acceleration in **Overall AI Use** is observed, particularly between 2023 and 2024, jumping from 55% to 78%.")
    st.write("• **GenAI Use** shows explosive growth from 2022 onwards, indicating the rapid integration of generative AI technologies into businesses.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = historical_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Adoption Rates Data (CSV)",
        data=csv,
        file_name="ai_adoption_rates.csv",
        mime="text/csv"
    )

elif view_type == "Historical Trends":
    # Apply year filter if set
    filtered_data = historical_data[
        (historical_data['year'] >= year_range[0]) & 
        (historical_data['year'] <= year_range[1])
    ]
    
    fig = go.Figure()
    
    # Add overall AI use line
    fig.add_trace(go.Scatter(
        x=filtered_data['year'], 
        y=filtered_data['ai_use'], 
        mode='lines+markers', 
        name='Overall AI Use', 
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Adoption: %{y}%<br>Source: AI Index & McKinsey<extra></extra>'
    ))
    
    # Add GenAI use line
    fig.add_trace(go.Scatter(
        x=filtered_data['year'], 
        y=filtered_data['genai_use'], 
        mode='lines+markers', 
        name='GenAI Use', 
        line=dict(width=4, color='#ff7f0e'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Adoption: %{y}%<br>Source: AI Index 2025<extra></extra>'
    ))
    
    # Add annotations
    fig.add_annotation(
        x=2022, y=33,
        text="<b>ChatGPT Launch</b><br>GenAI Era Begins",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#ff7f0e",
        ax=-50,
        ay=-40,
        bgcolor="rgba(255,127,14,0.1)",
        bordercolor="#ff7f0e",
        borderwidth=2,
        font=dict(color="#ff7f0e", size=12, family="Arial")
    )
    
    fig.add_annotation(
        x=2024, y=78,
        text="<b>2024 Acceleration</b><br>AI Index Report findings",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#1f77b4",
        ax=50,
        ay=-30,
        bgcolor="rgba(31,119,180,0.1)",
        bordercolor="#1f77b4",
        borderwidth=2,
        font=dict(color="#1f77b4", size=12, family="Arial")
    )
    
    fig.update_layout(
        title="AI Adoption Trends: The GenAI Revolution", 
        xaxis_title="Year", 
        yaxis_title="Adoption Rate (%)",
        height=500,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    # Display chart with source info
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="hist_source", help="View data source"):
            st.info(show_source_info('ai_index'))
    
    # Enhanced insights
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("📊 **Key Growth Insights (AI Index 2025):**")
        st.write("• Business adoption jumped from **55% to 78%** in just one year")
        st.write("• GenAI adoption more than **doubled** from 33% to 71%")
        st.write("• AI moved to **central role** in driving business value")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.write("🎯 **Industry Context:**")
        st.write("• Fastest enterprise technology adoption in history")
        st.write("• **280x cost reduction** in AI inference since 2022")
        st.write("• Growing research confirms AI **boosts productivity**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export data option
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Historical Data (CSV)",
        data=csv,
        file_name="ai_adoption_historical_trends.csv",
        mime="text/csv"
    )

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
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="industry_source", help="View data source"):
            st.info(show_source_info('mckinsey'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📈 **Industry Insights:**")
    st.write("• **Technology** and **Financial Services** sectors lead in both overall AI and GenAI adoption, reflecting their digital maturity and potential for automation.")
    st.write("• Industries like **Healthcare** and **Manufacturing** show solid AI adoption, with substantial GenAI integration as well, indicating a broad impact across diverse sectors.")
    st.write("• The **Average ROI** from AI is highest in Technology and Financial Services, reinforcing the correlation between high adoption and tangible business benefits.")
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    **📊 Understanding the Data:** - The percentages below show the **proportion of companies reporting financial benefits** from AI
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
        title="Financial Impact of AI by Business Function (2025)",
        xaxis_title="% of Companies Reporting Benefits",
        yaxis_title="Business Function",
        barmode='group',
        height=600,
        hovermode='y unified'
    )
    
    # Display chart with source info
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button(" ", key="financial_source", help="View data source"):
            st.info(show_source_info('ai_index'))
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📈 **Key Financial Impact Insights:**")
    st.write("• **Marketing & Sales** leads in revenue gains, with **71%** of companies reporting increases.")
    st.write("• **Service Operations** shows high cost savings, with **49%** of companies seeing reductions.")
    st.write("• While many companies report benefits, the **magnitude of gains (cost reduction <10%, revenue increase <5%)** suggests incremental improvements rather than radical transformation for most functions currently.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export option
    csv = financial_impact.to_csv(index=False)
    st.download_button(
        label="📥 Download Financial Impact Data (CSV)",
        data=csv,
        file_name="ai_financial_impact.csv",
        mime="text/csv"
    )

elif view_type == "Investment Trends":
    st.write("💰 **AI Investment Trends (2014-2024)**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=ai_investment_data['year'],
        y=ai_investment_data['total_investment'],
        mode='lines+markers',
        name='Total Investment',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Total Investment: $%{y:.1f}B<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=ai_investment_data['year'],
        y=ai_investment_data['genai_investment'],
        mode='lines+markers',
        name='GenAI Investment',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>GenAI Investment: $%{y:.1f}B<extra></extra>'
    ))
    
    fig.update_layout(
        title="Global AI Investment Trends (2014-2024)",
        xaxis_title="Year",
        yaxis_title="Investment (Billion USD)",
        hovermode="x unified",
        height=500
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="invest_source", help="View data source"):
            st.info(show_source_info('ai_index'))
    
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🌟 **Investment Highlights:**")
    st.write(f"• Total corporate AI investment soared to **${ai_investment_data['total_investment'].iloc[-1]:.1f}B** in 2024.")
    st.write(f"• GenAI investment alone reached **${ai_investment_data['genai_investment'].iloc[-1]:.1f}B** in 2024, showing explosive growth since 2022.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Regional Investment
    st.subheader("🌐 Regional AI Investment Growth (2024)")
    fig_regional_invest = px.bar(
        regional_growth.sort_values('investment_growth'),
        x='investment_growth',
        y='region',
        orientation='h',
        title='Year-over-Year AI Investment Growth by Region (2024)',
        labels={'investment_growth': 'Investment Growth (%)', 'region': 'Region'},
        text='investment_growth',
        color='investment_growth',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_regional_invest.update_layout(height=400, showlegend=False)
    fig_regional_invest.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_regional_invest, use_container_width=True)
    with col2:
        if st.button("📊", key="regional_invest_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🌎 **Regional Investment Dynamics:**")
    st.write(f"• **North America** leads with **{regional_growth[regional_growth['region'] == 'North America']['investment_growth'].iloc[0]}%** year-over-year investment growth.")
    st.write("• This sustained investment highlights the global race for AI leadership and development.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = ai_investment_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Investment Data (CSV)",
        data=csv,
        file_name="ai_investment_trends.csv",
        mime="text/csv"
    )

elif view_type == "Regional Growth":
    st.write("🌍 **Regional AI Adoption & Investment Growth (2024)**")
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('AI Adoption Rate by Region', 'YoY AI Investment Growth by Region'))
    
    # Adoption Rate
    fig.add_trace(
        go.Bar(
            x=regional_growth['region'],
            y=regional_growth['adoption_rate'],
            name='Adoption Rate',
            marker_color='#6A5ACD',
            text=[f'{x}%' for x in regional_growth['adoption_rate']],
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Investment Growth
    fig.add_trace(
        go.Bar(
            x=regional_growth['region'],
            y=regional_growth['investment_growth'],
            name='Investment Growth',
            marker_color='#FFA07A',
            text=[f'{x}%' for x in regional_growth['investment_growth']],
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Global Regional AI Trends (2024)",
        height=500,
        showlegend=False,
        hovermode="x unified"
    )
    fig.update_yaxes(title_text="Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Growth (%)", row=1, col=2)
    fig.update_xaxes(title_text="Region", row=1, col=1, tickangle=45)
    fig.update_xaxes(title_text="Region", row=1, col=2, tickangle=45)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="regional_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📊 **Key Regional Highlights:**")
    st.write(f"• **North America** leads in AI adoption at **{regional_growth[regional_growth['region'] == 'North America']['adoption_rate'].iloc[0]}%**.")
    st.write(f"• **Greater China** shows significant year-over-year growth in both adoption and investment.")
    st.write("• These regional disparities highlight varying stages of AI maturity and strategic focus globally.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = regional_growth.to_csv(index=False)
    st.download_button(
        label="📥 Download Regional Growth Data (CSV)",
        data=csv,
        file_name="ai_regional_growth.csv",
        mime="text/csv"
    )

elif view_type == "AI Cost Trends":
    st.write("💸 **AI Inference Cost Trends (Cost per Million Tokens)**")
    
    fig = px.bar(
        ai_cost_reduction,
        x='model',
        y='cost_per_million_tokens',
        color='model',
        title='Dramatic Drop in AI Inference Cost Over Time',
        labels={'cost_per_million_tokens': 'Cost per Million Tokens (USD)', 'model': 'AI Model'},
        text='cost_per_million_tokens'
    )
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis={'categoryorder':'array', 'categoryarray':['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B']},
        yaxis_type="log", # Use a log scale due to the large difference
        yaxis_title="Cost per Million Tokens (USD, Log Scale)"
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="ai_cost_source", help="View data source"):
            st.info(show_source_info('ai_index') + "\n\n" + show_source_info('nvidia')) # Refer to AI Index and NVIDIA

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📉 **Key AI Token Cost Insights:**")
    st.write(f"• The cost of AI inference has plummeted dramatically, making advanced AI more accessible.")
    st.write(f"• GPT-3.5 inference cost dropped from **$20.00 to $0.14 per million tokens** (a 142x reduction) between Nov 2022 and Oct 2024.")
    st.write(f"• New models like Gemini-1.5-Flash-8B further reduce costs to **$0.07 per million tokens**, representing a **280x reduction** since Nov 2022.")
    st.write("• This cost efficiency is crucial for scaling AI applications across industries.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = ai_cost_reduction.to_csv(index=False)
    st.download_button(
        label="📥 Download AI Token Cost Data (CSV)",
        data=csv,
        file_name="ai_token_cost_trends.csv",
        mime="text/csv"
    )

elif view_type == "Token Economics":
    st.write("💲 **AI Token Economics & Optimization**")

    st.subheader("Cost per Million Tokens by Model")
    fig_token_cost = px.bar(
        token_economics.sort_values('cost_per_million_input', ascending=True),
        x='model',
        y=['cost_per_million_input', 'cost_per_million_output'],
        barmode='group',
        title='AI Model Token Costs (Input vs. Output)',
        labels={'value': 'Cost per Million Tokens (USD)', 'variable': 'Token Type', 'model': 'AI Model'},
        text_auto=True,
        height=500,
        color_discrete_map={'cost_per_million_input': '#1f77b4', 'cost_per_million_output': '#ff7f0e'}
    )
    fig_token_cost.update_traces(texttemplate='$%{y:.2f}', textposition='outside')
    fig_token_cost.update_layout(hovermode='x unified')

    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_token_cost, use_container_width=True)
    with col2:
        if st.button("📊", key="token_cost_source", help="View data source"):
            st.info(show_source_info('ai_index') + "\n\n" + show_source_info('nvidia'))

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("💸 **Model Cost Insights:**")
    st.write("• Newer, more efficient models like **Gemini-1.5-Flash-8B** offer significantly lower costs per million tokens for both input and output.")
    st.write("• There's a clear trend towards more cost-effective AI inference, making advanced models more accessible.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Token Usage Patterns by Use Case")
    fig_usage_patterns = px.bar(
        token_usage_patterns.melt(id_vars='use_case', value_vars=['avg_input_tokens', 'avg_output_tokens']),
        x='use_case',
        y='value',
        color='variable',
        barmode='group',
        title='Average Token Usage by Use Case',
        labels={'value': 'Average Tokens', 'variable': 'Token Type', 'use_case': 'Use Case'},
        text_auto=True,
        height=500
    )
    fig_usage_patterns.update_layout(hovermode='x unified')
    fig_usage_patterns.update_traces(texttemplate='%{y}', textposition='outside')

    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_usage_patterns, use_container_width=True)
    with col2:
        if st.button("📊", key="usage_source", help="View data source"):
            st.info("Data based on industry benchmarks and typical LLM usage scenarios.")

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📈 **Usage Pattern Insights:**")
    st.write("• **Document Analysis** requires the highest average input tokens, while **Reasoning Tasks** demand substantial output tokens.")
    st.write("• Understanding these patterns helps in optimizing prompt design and model selection for specific applications.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Token Optimization Strategies")
    fig_optimization = px.bar(
        token_optimization.sort_values('cost_reduction', ascending=True),
        x='cost_reduction',
        y='strategy',
        orientation='h',
        title='Cost Reduction Potential of Token Optimization Strategies',
        labels={'cost_reduction': 'Potential Cost Reduction (%)', 'strategy': 'Strategy'},
        text='cost_reduction',
        height=500
    )
    fig_optimization.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig_optimization.update_layout(hovermode='y unified')

    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_optimization, use_container_width=True)
    with col2:
        if st.button("📊", key="optimization_source", help="View data source"):
            st.info("Data based on industry best practices and internal studies.")

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🛠️ **Optimization Insights:**")
    st.write("• **Model Selection** (70% cost reduction) and **Batch Processing** (60% cost reduction) offer the highest potential for cost savings.")
    st.write("• **Prompt Engineering** is a fundamental and highly effective strategy for immediate gains.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Token Pricing Evolution")
    fig_pricing_evolution = px.line(
        token_pricing_evolution,
        x='date',
        y=['avg_price_input', 'avg_price_output'],
        title='Average Token Pricing Evolution Over Time',
        labels={'value': 'Average Price (USD)', 'variable': 'Price Type', 'date': 'Date'},
        height=500
    )
    fig_pricing_evolution.update_layout(hovermode='x unified')

    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_pricing_evolution, use_container_width=True)
    with col2:
        if st.button("📊", key="pricing_source", help="View data source"):
            st.info("Data based on historical pricing trends of major LLM providers.")

    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📉 **Pricing Evolution Insights:**")
    st.write("• Both input and output token prices have seen a significant downward trend since late 2022, making LLMs increasingly affordable.")
    st.write("• This trend is driven by continuous innovation, increased competition, and economies of scale in AI infrastructure.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Download buttons for all token economics dataframes
    st.download_button(
        label="📥 Download Token Economics (Models) Data (CSV)",
        data=token_economics.to_csv(index=False),
        file_name="token_economics_models.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 Download Token Usage Patterns Data (CSV)",
        data=token_usage_patterns.to_csv(index=False),
        file_name="token_usage_patterns.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 Download Token Optimization Strategies Data (CSV)",
        data=token_optimization.to_csv(index=False),
        file_name="token_optimization_strategies.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 Download Token Pricing Evolution Data (CSV)",
        data=token_pricing_evolution.to_csv(index=False),
        file_name="token_pricing_evolution.csv",
        mime="text/csv"
    )

elif view_type == "Labor Impact":
    st.write("👩‍💼 **AI and the Future of Work (2025)**")
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Generational Job Impact Perception", "Productivity Gain by Skill Level"))
    
    # Generational Perception
    fig.add_trace(go.Bar(
        x=ai_perception['generation'],
        y=ai_perception['expect_job_change'],
        name='Expect Job Change',
        marker_color='#82E0AA',
        text=[f'{x}%' for x in ai_perception['expect_job_change']],
        textposition='outside'
    ), row=1, col=1)
    
    fig.add_trace(go.Bar(
        x=ai_perception['generation'],
        y=ai_perception['expect_job_replacement'],
        name='Expect Job Replacement',
        marker_color='#EC7063',
        text=[f'{x}%' for x in ai_perception['expect_job_replacement']],
        textposition='outside'
    ), row=1, col=1)
    
    # Productivity Gain by Skill Level
    fig.add_trace(go.Bar(
        x=productivity_by_skill['skill_level'],
        y=productivity_by_skill['productivity_gain'],
        name='Productivity Gain (%)',
        marker_color='#AF7AC5',
        text=[f'{x}%' for x in productivity_by_skill['productivity_gain']],
        textposition='outside'
    ), row=1, col=2)
    
    fig.update_layout(
        title_text='AI\'s Impact on Labor: Perception and Productivity',
        height=500,
        barmode='group',
        showlegend=True,
        legend=dict(x=0.01, y=1.15, orientation="h", bgcolor='rgba(255,255,255,0.7)', bordercolor='rgba(0,0,0,0.5)')
    )
    fig.update_yaxes(title_text="Percentage (%)", row=1, col=1)
    fig.update_yaxes(title_text="Productivity Gain (%)", row=1, col=2)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="labor_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            st.info("Productivity data adapted from various academic sources (Acemoglu, Brynjolfsson)")
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("💼 **Labor Market Insights (AI Index 2025 & Academic):**")
    st.write("• Younger generations (Gen Z, Millennials) are significantly more likely to anticipate AI changing or replacing their jobs compared to older generations.")
    st.write("• AI disproportionately boosts the productivity of **low-skilled workers**, potentially reducing skill gaps and fostering more equitable growth.")
    st.write("• This suggests AI could lead to a 'flattening' of the labor market, increasing the relative value of less skilled tasks.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_perception = ai_perception.to_csv(index=False)
    csv_productivity = productivity_by_skill.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Generational Perception Data (CSV)",
        data=csv_perception,
        file_name="ai_generational_perception.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 Download Productivity by Skill Data (CSV)",
        data=csv_productivity,
        file_name="ai_productivity_by_skill.csv",
        mime="text/csv"
    )

elif view_type == "Firm Size Analysis":
    st.write("🏢 **AI Adoption by Firm Size (2018)**")
    
    fig = px.bar(
        firm_size,
        x='size',
        y='adoption',
        title='AI Adoption Rate by Firm Size',
        labels={'size': 'Firm Size (Number of Employees)', 'adoption': 'Adoption Rate (%)'},
        color_discrete_sequence=px.colors.sequential.Tealgrn,
        text='adoption'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="firm_source", help="View data source"):
            st.info(show_source_info('census'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📏 **Firm Size Insights (US Census Bureau 2018):**")
    st.write("• AI adoption rates show a strong positive correlation with firm size, with **large firms (5000+ employees)** demonstrating significantly higher adoption (58.5%).")
    st.write("• This trend highlights the resource intensity of early AI adoption and the advantages larger organizations have in implementing these technologies.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = firm_size.to_csv(index=False)
    st.download_button(
        label="📥 Download Firm Size Data (CSV)",
        data=csv,
        file_name="ai_adoption_by_firm_size.csv",
        mime="text/csv"
    )

elif view_type == "Technology Stack":
    st.write("☁️ **AI Integration in Technology Stacks**")
    
    fig = px.pie(
        tech_stack,
        values='percentage',
        names='technology',
        title='AI Integration with Cloud and Digitization',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textinfo='percent+label', pull=[0.1 if t == 'AI + Cloud + Digitization' else 0 for t in tech_stack['technology']])
    fig.update_layout(height=500)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="tech_source", help="View data source"):
            st.info(show_source_info('mckinsey'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("⚙️ **Technology Stack Insights (McKinsey 2024):**")
    st.write("• A significant majority of AI adoption occurs in conjunction with **Cloud (45%)** and **Digitization (38%)**, indicating AI is rarely a standalone implementation.")
    st.write("• The highest percentage (**62%**) of firms integrate AI with both Cloud and Digitization, highlighting the synergistic relationship between these technologies for maximum impact.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = tech_stack.to_csv(index=False)
    st.download_button(
        label="📥 Download Technology Stack Data (CSV)",
        data=csv,
        file_name="ai_tech_stack_integration.csv",
        mime="text/csv"
    )

elif view_type == "AI Technology Maturity":
    st.write("⏳ **AI Technology Maturity & Adoption (2025)**")
    
    fig = px.scatter(
        ai_maturity,
        x='adoption_rate',
        y='risk_score',
        color='maturity',
        size='time_to_value',
        hover_name='technology',
        title='AI Technologies: Adoption vs. Risk by Maturity Stage',
        labels={
            'adoption_rate': 'Adoption Rate (%)',
            'risk_score': 'Risk Score (0-100)',
            'maturity': 'Maturity Stage',
            'time_to_value': 'Time to Value (Years)'
        },
        color_discrete_map={
            'Peak of Expectations': '#E74C3C',
            'Trough of Disillusionment': '#F1C40F',
            'Slope of Enlightenment': '#2ECC71'
        },
        size_max=40
    )
    fig.update_layout(height=600)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="maturity_source", help="View data source"):
            st.info("Data adapted from Gartner Hype Cycle for AI & AI Index Report 2025.")
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🧠 **AI Maturity Insights (Gartner Hype Cycle & AI Index 2025):**")
    st.write("• **Generative AI** is at the 'Peak of Expectations' with high adoption but also a high perceived risk, reflecting its novelty and rapid evolution.")
    st.write("• Technologies like **Cloud AI Services** are on the 'Slope of Enlightenment', indicating widespread adoption and proven value with lower associated risks.")
    st.write("• **AI Agents** and **Composite AI** are emerging technologies with high risk and high potential but currently lower adoption, signifying they are still in early development phases.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = ai_maturity.to_csv(index=False)
    st.download_button(
        label="📥 Download AI Maturity Data (CSV)",
        data=csv,
        file_name="ai_technology_maturity.csv",
        mime="text/csv"
    )

elif view_type == "Productivity Research":
    st.write("📈 **AI's Impact on Productivity Growth**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=productivity_data['year'],
        y=productivity_data['productivity_growth'],
        mode='lines+markers',
        name='Productivity Growth (Annual %)',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=productivity_data['year'],
        y=productivity_data['young_workers_share'],
        mode='lines+markers',
        name='Young Workers Share (%)',
        yaxis='y2',
        line=dict(color='#ff7f0e', dash='dot', width=2),
        marker=dict(size=6)
    ))
    
    # Add AI impact markers
    for index, row in ai_productivity_estimates.iterrows():
        if row['source'] == 'Acemoglu (2024)':
            fig.add_annotation(
                x=2025, y=row['annual_impact'] + 0.1,
                text=f"Acemoglu (2024): +{row['annual_impact']}%",
                showarrow=True, arrowhead=1, ax=50, ay=0
            )
        else:
            fig.add_annotation(
                x=2025, y=row['annual_impact'],
                text=f"{row['source']}: +{row['annual_impact']}%",
                showarrow=True, arrowhead=1, ax=50, ay= (index * 20)
            )
            
    fig.update_layout(
        title="Long-Term Productivity Trends and AI Estimates",
        xaxis_title="Year",
        yaxis=dict(title="Annual Productivity Growth (%)", side="left", range=[0, 3]),
        yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y", range=[20, 50]),
        height=600,
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.7)', bordercolor='rgba(0,0,0,0.5)')
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="prod_source", help="View data source"):
            st.info("Productivity data from US Bureau of Labor Statistics. AI estimates from cited academic and industry reports.")
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🔬 **Productivity Research Insights (Various Sources):**")
    st.write("• Recent research by **Brynjolfsson et al. (2023)** suggests AI could contribute an annual productivity growth of **1.5%**.")
    st.write("• Broader estimates from **McKinsey** and **Goldman Sachs** project even higher potential impacts, up to **2.5%** annually, underscoring AI's transformative economic potential.")
    st.write("• The impact of AI on productivity growth is a rapidly evolving field of study, with early evidence pointing to significant positive effects.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_productivity_data = productivity_data.to_csv(index=False)
    csv_productivity_estimates = ai_productivity_estimates.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Productivity Growth Data (CSV)",
        data=csv_productivity_data,
        file_name="ai_productivity_growth.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 Download AI Productivity Estimates (CSV)",
        data=csv_productivity_estimates,
        file_name="ai_productivity_estimates.csv",
        mime="text/csv"
    )

elif view_type == "Environmental Impact":
    st.write("🌳 **Environmental Cost of AI Training (2012-2024)**")
    
    fig = px.bar(
        training_emissions,
        x='model',
        y='carbon_tons',
        color='year',
        text='carbon_tons',
        title='Estimated Carbon Emissions from Training Large AI Models',
        labels={'carbon_tons': 'Carbon Emissions (Tons CO2e)', 'model': 'AI Model'},
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_traces(texttemplate='%{text:.0f} tons', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="emissions_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🌿 **Environmental Insights (AI Index 2025):**")
    st.write("• The carbon emissions associated with training large AI models have seen a massive increase, from **0.01 tons for AlexNet (2012)** to **8930 tons for Llama 3.1 (2024)**.")
    st.write("• This highlights the growing environmental footprint of advanced AI development and the need for more sustainable AI practices.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv = training_emissions.to_csv(index=False)
    st.download_button(
        label="📥 Download Training Emissions Data (CSV)",
        data=csv,
        file_name="ai_training_emissions.csv",
        mime="text/csv"
    )

elif view_type == "Geographic Distribution":
    st.write("🗺️ **AI Adoption Across US Cities & States (2018)**")
    
    # City-level map
    fig_city = px.scatter_mapbox(
        geographic,
        lat="lat",
        lon="lon",
        color="rate",
        size="rate",
        hover_name="city",
        hover_data={"state": True, "rate": ":.1f%", "population_millions": ":.1fM", "gdp_billions": ":$.1fB"},
        color_continuous_scale=px.colors.sequential.Viridis,
        zoom=3,
        height=600,
        title="AI Adoption Rate by US City (2018)"
    )
    fig_city.update_layout(mapbox_style="carto-positron")
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_city, use_container_width=True)
    with col2:
        if st.button("📊", key="geo_city_source", help="View data source"):
            st.info(show_source_info('census'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📍 **Geographic Insights (US Census Bureau 2018):**")
    st.write("• **San Francisco Bay Area** leads in AI adoption, consistent with its status as a tech hub.")
    st.write("• Cities with strong innovation ecosystems like **Boston** and **Seattle** also show high adoption rates.")
    st.write("• The data suggests that AI adoption is concentrated in economic centers with significant tech industries and higher GDP.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_geographic = geographic.to_csv(index=False)
    st.download_button(
        label="📥 Download Geographic Data (Cities) (CSV)",
        data=csv_geographic,
        file_name="ai_geographic_city_data.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.write("🗺️ **AI Adoption Across US States (2018 - Average City Rate)**")
    
    fig_state = px.choropleth(
        state_data,
        locations='state_code',
        locationmode="USA-states",
        color="rate",
        scope="usa",
        color_continuous_scale="Plasma",
        title="Average AI Adoption Rate by US State (Based on Sampled Cities)",
        hover_name="state",
        hover_data={"rate": ":.1f%"}
    )
    fig_state.update_layout(height=600)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_state, use_container_width=True)
    with col2:
        if st.button("📊", key="geo_state_source", help="View data source"):
            st.info(show_source_info('census'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📊 **State-level Insights (US Census Bureau 2018):**")
    st.write("• States with major tech hubs like **California**, **Massachusetts**, and **Washington** exhibit higher average AI adoption rates.")
    st.write("• This aggregated view highlights regional disparities in AI readiness and adoption across the United States.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_state_data = state_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Geographic Data (States) (CSV)",
        data=csv_state_data,
        file_name="ai_geographic_state_data.csv",
        mime="text/csv"
    )

elif view_type == "OECD 2025 Findings":
    st.write("🌐 **OECD Countries AI Adoption & Applications (2025)**")
    
    st.markdown("#### G7 AI Adoption Rates by Country and Sector")
    fig_g7 = go.Figure()
    fig_g7.add_trace(go.Bar(
        x=oecd_g7_adoption['country'],
        y=oecd_g7_adoption['adoption_rate'],
        name='Overall Adoption Rate',
        marker_color='#3498DB',
        text=[f'{x}%' for x in oecd_g7_adoption['adoption_rate']],
        textposition='outside'
    ))
    fig_g7.add_trace(go.Bar(
        x=oecd_g7_adoption['country'],
        y=oecd_g7_adoption['manufacturing'],
        name='Manufacturing Sector',
        marker_color='#2ECC71',
        text=[f'{x}%' for x in oecd_g7_adoption['manufacturing']],
        textposition='outside'
    ))
    fig_g7.add_trace(go.Bar(
        x=oecd_g7_adoption['country'],
        y=oecd_g7_adoption['ict_sector'],
        name='ICT Sector',
        marker_color='#E74C3C',
        text=[f'{x}%' for x in oecd_g7_adoption['ict_sector']],
        textposition='outside'
    ))
    fig_g7.update_layout(
        title="AI Adoption Across G7 Countries by Sector",
        xaxis_title="Country",
        yaxis_title="Adoption Rate (%)",
        barmode='group',
        height=600,
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.7)', bordercolor='rgba(0,0,0,0.5)')
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_g7, use_container_width=True)
    with col2:
        if st.button("📊", key="oecd_g7_source", help="View data source"):
            st.info(show_source_info('oecd'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🌐 **G7 Adoption Insights (OECD 2025):**")
    st.write("• **Japan** and the **United States** show strong overall AI adoption, with Japan leading across sectors including Manufacturing.")
    st.write("• The **ICT sector** consistently demonstrates higher AI adoption rates compared to overall adoption and manufacturing in most G7 countries, reflecting its inherent digital nature.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_oecd_g7 = oecd_g7_adoption.to_csv(index=False)
    st.download_button(
        label="📥 Download G7 Adoption Data (CSV)",
        data=csv_oecd_g7,
        file_name="oecd_g7_ai_adoption.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("#### AI Application Usage Rates (2025)")
    
    fig_applications = px.bar(
        oecd_applications.sort_values('usage_rate', ascending=False),
        x='usage_rate',
        y='application',
        color='category',
        orientation='h',
        title='Usage Rates of AI Applications (GenAI vs. Traditional AI)',
        labels={'usage_rate': 'Usage Rate (%)', 'application': 'AI Application'},
        color_discrete_map={'GenAI': '#8e44ad', 'Traditional AI': '#1abc9c'},
        text='usage_rate'
    )
    fig_applications.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig_applications.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=600, yaxis={'categoryorder':'total ascending'})
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_applications, use_container_width=True)
    with col2:
        if st.button("📊", key="oecd_app_source", help="View data source"):
            st.info(show_source_info('oecd'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("💡 **Application Usage Insights (OECD 2025):**")
    st.write("• **Content Generation** and **Code Generation** lead in usage rates, underscoring the immediate and tangible benefits of GenAI in creative and development tasks.")
    st.write("• Traditional AI applications like **Predictive Maintenance** and **Process Automation** remain highly relevant, indicating a diversified use of AI technologies across various business functions.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_oecd_applications = oecd_applications.to_csv(index=False)
    st.download_button(
        label="📥 Download AI Applications Data (CSV)",
        data=csv_oecd_applications,
        file_name="oecd_ai_applications.csv",
        mime="text/csv"
    )

elif view_type == "Barriers & Support":
    st.write("🚧 **Barriers to AI Adoption & Support Effectiveness (2025)**")
    
    fig_barriers = px.bar(
        barriers_data.sort_values('percentage', ascending=False),
        x='percentage',
        y='barrier',
        orientation='h',
        title='Top Barriers to AI Adoption',
        labels={'percentage': 'Percentage of Firms Reporting Barrier (%)', 'barrier': 'Barrier'},
        color_discrete_sequence=px.colors.sequential.OrRd,
        text='percentage'
    )
    fig_barriers.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig_barriers.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500, yaxis={'categoryorder':'total ascending'})
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_barriers, use_container_width=True)
    with col2:
        if st.button("📊", key="barriers_source", help="View data source"):
            st.info(show_source_info('mckinsey'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🛑 **Barrier Insights (McKinsey 2024):**")
    st.write("• The primary impediment to AI adoption is the **lack of skilled personnel (68%)**, underscoring a critical talent gap in the AI ecosystem.")
    st.write("• **Data availability/quality** and **integration with legacy systems** are also significant challenges, indicating the need for robust data strategies and modern infrastructure.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_barriers = barriers_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Barriers Data (CSV)",
        data=csv_barriers,
        file_name="ai_adoption_barriers.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.markdown("#### Effectiveness of Support Measures")
    
    fig_support = px.bar(
        support_effectiveness.sort_values('effectiveness_score', ascending=False),
        x='effectiveness_score',
        y='support_type',
        orientation='h',
        title='Perceived Effectiveness of AI Adoption Support Measures',
        labels={'effectiveness_score': 'Effectiveness Score (0-100)', 'support_type': 'Support Type'},
        color_discrete_sequence=px.colors.sequential.Greens,
        text='effectiveness_score'
    )
    fig_support.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig_support.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500, yaxis={'categoryorder':'total ascending'})
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_support, use_container_width=True)
    with col2:
        if st.button("📊", key="support_source", help="View data source"):
            st.info(show_source_info('oecd'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("✅ **Support Insights (OECD 2025):**")
    st.write("• **Government investment in education** and **university partnerships** are considered the most effective support measures, directly addressing the skill gap.")
    st.write("• **Public-private collaboration** and **regulatory clarity** are also highly valued, emphasizing the importance of a supportive ecosystem for AI development and deployment.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_support = support_effectiveness.to_csv(index=False)
    st.download_button(
        label="📥 Download Support Effectiveness Data (CSV)",
        data=csv_support,
        file_name="ai_support_effectiveness.csv",
        mime="text/csv"
    )

elif view_type == "ROI Analysis":
    st.write("💰 **Return on Investment from AI Initiatives (2025)**")
    
    # Data for a simple ROI chart, reusing sector_2025 avg_roi
    fig_roi = px.bar(
        sector_2025.sort_values('avg_roi', ascending=False),
        x='sector',
        y='avg_roi',
        title='Average ROI from AI by Industry Sector',
        labels={'avg_roi': 'Average ROI (x)', 'sector': 'Industry'},
        color_discrete_sequence=px.colors.sequential.Plotly3,
        text='avg_roi'
    )
    fig_roi.update_traces(texttemplate='%{text:.1f}x', textposition='outside')
    fig_roi.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500, xaxis_tickangle=-45)
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_roi, use_container_width=True)
    with col2:
        if st.button("📊", key="roi_source", help="View data source"):
            st.info(show_source_info('mckinsey')) # Adjust source if needed
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("📈 **ROI Insights (McKinsey 2025):**")
    st.write("• Industries with higher digital maturity and AI adoption, such as **Technology (4.2x)** and **Financial Services (3.8x)**, report the highest average ROI from their AI investments.")
    st.write("• This reinforces the idea that strategic and well-integrated AI initiatives yield significant financial returns.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Also include the financial impact data as it relates to ROI
    st.subheader("Reported Financial Benefits by Function")
    fig_financial_benefits = go.Figure()
    
    financial_sorted_rev = financial_impact.sort_values('companies_reporting_revenue_gains', ascending=True)
    fig_financial_benefits.add_trace(go.Bar(
        name='Companies Reporting Revenue Gains',
        y=financial_sorted_rev['function'],
        x=financial_sorted_rev['companies_reporting_revenue_gains'],
        orientation='h',
        marker_color='#3498DB',
        hovertemplate='Function: %{y}<br>Companies reporting gains: %{x}%<extra></extra>'
    ))
    
    financial_sorted_cost = financial_impact.sort_values('companies_reporting_cost_savings', ascending=True)
    fig_financial_benefits.add_trace(go.Bar(
        name='Companies Reporting Cost Savings',
        y=financial_sorted_cost['function'],
        x=financial_sorted_cost['companies_reporting_cost_savings'],
        orientation='h',
        marker_color='#2ECC71',
        hovertemplate='Function: %{y}<br>Companies reporting savings: %{x}%<extra></extra>'
    ))
    
    fig_financial_benefits.update_layout(
        title="Percentage of Companies Reporting Financial Benefits from AI (Cost Savings vs. Revenue Gains)",
        xaxis_title="% of Companies",
        yaxis_title="Business Function",
        barmode='group',
        height=600
    )
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_financial_benefits, use_container_width=True)
    with col2:
        if st.button("📊", key="financial_benefits_source", help="View data source"):
            st.info(show_source_info('ai_index'))
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("💰 **Additional Financial Impact Insights:**")
    st.write("• While ROI can be substantial in certain sectors, the proportion of companies reporting significant revenue gains or cost savings varies by business function.")
    st.write("• This indicates that AI's financial impact is not uniform and depends on the specific application and functional area.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv1 = sector_2025.to_csv(index=False)
    csv2 = financial_impact.to_csv(index=False)
    st.download_button(label="📥 Download ROI by Industry Data (CSV)", data=csv1, file_name="ai_roi_by_industry.csv", mime="text/csv")
    st.download_button(label="📥 Download Financial Benefits Data (CSV)", data=csv2, file_name="ai_financial_benefits.csv", mime="text/csv")

elif view_type == "Skill Gap Analysis":
    st.write("🧑‍💻 **AI Skill Gaps and Training Initiatives (2025)**")
    
    fig_skills = make_subplots(rows=1, cols=2, subplot_titles=("Skill Gap Severity", "Training Initiatives"))
    
    # Skill Gap Severity
    fig_skills.add_trace(go.Bar(
        x=skill_gap_data['gap_severity'],
        y=skill_gap_data['skill'],
        name='Gap Severity (0-100)',
        orientation='h',
        marker_color='#E74C3C',
        text=[f'{x}' for x in skill_gap_data['gap_severity']],
        textposition='outside'
    ), row=1, col=1)
    
    # Training Initiatives
    fig_skills.add_trace(go.Bar(
        x=skill_gap_data['training_initiatives'],
        y=skill_gap_data['skill'],
        name='Training Initiatives (0-100)',
        orientation='h',
        marker_color='#2ECC71',
        text=[f'{x}' for x in skill_gap_data['training_initiatives']],
        textposition='outside'
    ), row=1, col=2)
    
    fig_skills.update_layout(
        title_text='AI Skill Gaps and Corresponding Training Efforts',
        height=600,
        showlegend=False
    )
    fig_skills.update_xaxes(title_text="Severity Score", row=1, col=1)
    fig_skills.update_xaxes(title_text="Initiative Score", row=1, col=2)
    fig_skills.update_yaxes(autorange="reversed") # To keep skills in the same order
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_skills, use_container_width=True)
    with col2:
        if st.button("📊", key="skills_source", help="View data source"):
            st.info("Data based on industry reports and expert surveys (e.g., McKinsey, Deloitte).")
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("💡 **Skill Gap Insights (Industry Reports):**")
    st.write("• **AI/ML Engineering** and **Data Science** represent the most severe skill gaps, indicating a high demand for core technical AI competencies.")
    st.write("• There's a notable disparity between skill gap severity and training initiatives for areas like **AI Ethics** and **AI Security**, suggesting these critical areas might be underserved in current training efforts.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_skills = skill_gap_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Skill Gap Data (CSV)",
        data=csv_skills,
        file_name="ai_skill_gap_analysis.csv",
        mime="text/csv"
    )

elif view_type == "AI Governance":
    st.write("⚖️ **AI Governance Adoption & Maturity (2025)**")
    
    fig_gov = make_subplots(rows=1, cols=2, subplot_titles=("Governance Aspect Adoption Rate", "Maturity Score"))
    
    # Adoption Rate
    fig_gov.add_trace(go.Bar(
        x=ai_governance['adoption_rate'],
        y=ai_governance['aspect'],
        name='Adoption Rate (%)',
        orientation='h',
        marker_color='#9B59B6',
        text=[f'{x}%' for x in ai_governance['adoption_rate']],
        textposition='outside'
    ), row=1, col=1)
    
    # Maturity Score
    fig_gov.add_trace(go.Bar(
        x=ai_governance['maturity_score'],
        y=ai_governance['aspect'],
        name='Maturity Score (out of 5)',
        orientation='h',
        marker_color='#34495E',
        text=[f'{x:.1f}' for x in ai_governance['maturity_score']],
        textposition='outside'
    ), row=1, col=2)
    
    fig_gov.update_layout(
        title_text='AI Governance: Adoption and Maturity by Aspect',
        height=600,
        showlegend=False
    )
    fig_gov.update_xaxes(title_text="Adoption Rate (%)", row=1, col=1)
    fig_gov.update_xaxes(title_text="Maturity Score", row=1, col=2)
    fig_gov.update_yaxes(autorange="reversed") # Keep order consistent
    
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig_gov, use_container_width=True)
    with col2:
        if st.button("📊", key="gov_source", help="View data source"):
            st.info("Data based on global AI governance surveys and frameworks (e.g., OECD, NIST).")
            
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.write("🏛️ **Governance Insights (Global Surveys):**")
    st.write("• **Data Privacy (78%)** and **Regulatory Compliance (72%)** show the highest adoption rates, indicating organizations prioritize adherence to existing legal frameworks.")
    st.write("• Aspects like **Bias Detection (45%)** and **Accountability Frameworks (48%)** have lower adoption and maturity scores, highlighting areas where AI governance practices need significant development.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    csv_governance = ai_governance.to_csv(index=False)
    st.download_button(
        label="📥 Download AI Governance Data (CSV)",
        data=csv_governance,
        file_name="ai_governance_data.csv",
        mime="text/csv"
    )

else:
    st.info("Select an analysis view from the sidebar to get started!")

st.markdown("---")
st.markdown("Created by Robert Casanova | [GitHub](https://github.com/Rcasanova25/AI-Adoption-Dashboard)")
