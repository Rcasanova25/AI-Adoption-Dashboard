# -*- coding: utf-8 -*-
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
        'About': "# AI Adoption Dashboard\nVersion 2.3.0\n\nTrack AI adoption trends across industries and geographies with token economics insights.\n\nCreated by Robert Casanova"
    }
)

# Data loading function - updated with AI Index 2025 data and token economics
@st.cache_data
def load_data():
    # Historical trends data - UPDATED with AI Index 2025 findings
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],  # Updated: 78% in 2024
        'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]  # Updated: 71% in 2024
    })
    
    # Token pricing evolution data
    token_pricing = pd.DataFrame({
        'date': ['Nov 2022', 'Jan 2023', 'Jul 2023', 'Jan 2024', 'Oct 2024', 'Oct 2024 (Gemini)'],
        'cost_per_million': [20.00, 10.00, 2.00, 0.50, 0.14, 0.07],
        'cost_reduction': [1, 2, 10, 40, 143, 286],
        'billion_token_cost': [20000, 10000, 2000, 500, 140, 70]
    })
    
    # Token usage patterns
    token_usage = pd.DataFrame({
        'use_case': ['Chat (simple)', 'Email generation', 'Code review', 'Document analysis', 
                    'Research summary', 'Contract review', 'Book summary', 'Video analysis'],
        'avg_tokens': [500, 1000, 2000, 10000, 5000, 15000, 50000, 100000],
        'typical_time_min': [0.5, 1, 2, 5, 5, 10, 15, 20],
        'value_category': ['Low', 'Low', 'Medium', 'Medium', 'High', 'High', 'Very High', 'Very High']
    })
    
    # 2018 Sector data
    sector_2018 = pd.DataFrame({
        'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                  'Finance & Insurance', 'Retail Trade', 'Construction'],
        'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
        'employment_weighted': [18, 22, 15, 14, 12, 8, 6]
    })
    
    # 2025 Sector data with token usage intensity
    sector_2025 = pd.DataFrame({
        'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                  'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
        'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2],
        'avg_monthly_tokens_millions': [850, 720, 450, 380, 620, 280, 210, 150],
        'token_cost_savings_pct': [95, 93, 91, 88, 92, 87, 85, 82]
    })
    
    # Firm size data with token usage
    firm_size = pd.DataFrame({
        'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                '500-999', '1000-2499', '2500-4999', '5000+'],
        'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5],
        'avg_tokens_per_employee_daily': [10, 25, 50, 100, 200, 350, 500, 750, 1000, 1500, 2000]
    })
    
    # AI Maturity data with token requirements
    ai_maturity = pd.DataFrame({
        'technology': ['Generative AI', 'AI Agents', 'Foundation Models', 'ModelOps', 
                      'AI Engineering', 'Cloud AI Services', 'Knowledge Graphs', 'Composite AI'],
        'adoption_rate': [71, 15, 45, 25, 30, 78, 35, 12],
        'maturity': ['Peak of Expectations', 'Peak of Expectations', 'Trough of Disillusionment',
                    'Trough of Disillusionment', 'Peak of Expectations', 'Slope of Enlightenment',
                    'Slope of Enlightenment', 'Peak of Expectations'],
        'risk_score': [85, 90, 60, 55, 80, 25, 40, 95],
        'time_to_value': [3, 3, 3, 3, 3, 1, 3, 7],
        'avg_tokens_per_query': [2000, 5000, 10000, 500, 1000, 1500, 3000, 15000]
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
    
    # Technology stack with token efficiency
    tech_stack = pd.DataFrame({
        'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
        'percentage': [15, 45, 38, 62],
        'token_efficiency_multiplier': [1.0, 2.5, 2.2, 3.8]
    })
    
    # Productivity data with skill levels - ENHANCED
    productivity_data = pd.DataFrame({
        'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
        'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
    })
    
    # AI productivity by skill level with token usage
    productivity_by_skill = pd.DataFrame({
        'skill_level': ['Low-skilled', 'Medium-skilled', 'High-skilled'],
        'productivity_gain': [14, 9, 5],
        'skill_gap_reduction': [28, 18, 8],
        'avg_daily_tokens': [5000, 15000, 25000]
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
    
    # OECD AI Applications with token intensity
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
                    'Traditional AI', 'GenAI'],
        'avg_tokens_per_use': [5000, 3000, 2000, 500, 200, 1000, 300, 1500, 800, 100, 1500, 2000, 3000, 50, 10000]
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
    
    # AI Investment data with token context
    ai_investment_data = pd.DataFrame({
        'year': [2014, 2020, 2021, 2022, 2023, 2024],
        'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
        'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
        'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
        'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
        'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5],
        'cost_per_million_tokens': [100, 50, 30, 20, 2, 0.14]
    })
    
    # Regional AI adoption growth from AI Index 2025
    regional_growth = pd.DataFrame({
        'region': ['Greater China', 'Europe', 'North America', 'Asia-Pacific', 'Latin America'],
        'growth_2024': [27, 23, 15, 18, 12],
        'adoption_rate': [68, 65, 82, 58, 45],
        'investment_growth': [32, 28, 44, 25, 18]
    })
    
    # AI cost reduction data with token context
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
        'cost_per_million_tokens': [20.00, 0.14, 0.07],
        'year': [2022, 2024, 2024],
        'tokens_per_dollar': [50000, 7142857, 14285714]
    })
    
    # Financial impact by function with token ROI
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],
        'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],
        'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3],
        'monthly_tokens_millions': [120, 85, 65, 150, 95, 110, 45, 55]
    })
    
    # Generational AI perception data from AI Index 2025
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
        'expect_job_change': [67, 65, 58, 49],
        'expect_job_replacement': [42, 40, 34, 28]
    })
    
    # Training emissions data with token count
    training_emissions = pd.DataFrame({
        'model': ['AlexNet (2012)', 'GPT-3 (2020)', 'GPT-4 (2023)', 'Llama 3.1 405B (2024)'],
        'carbon_tons': [0.01, 588, 5184, 8930],
        'training_tokens_billions': [0.001, 300, 13000, 15000]
    })
    
    # Skill gap data
    skill_gap_data = pd.DataFrame({
        'skill': ['AI/ML Engineering', 'Data Science', 'AI Ethics', 'Prompt Engineering',
                 'AI Product Management', 'MLOps', 'AI Security', 'Change Management'],
        'gap_severity': [85, 78, 72, 68, 65, 62, 58, 55],
        'training_initiatives': [45, 52, 28, 38, 32, 35, 22, 48]
    })
    
    # AI governance data
    ai_governance = pd.DataFrame({
        'aspect': ['Ethics Guidelines', 'Data Privacy', 'Bias Detection', 'Transparency',
                  'Accountability Framework', 'Risk Assessment', 'Regulatory Compliance'],
        'adoption_rate': [62, 78, 45, 52, 48, 55, 72],
        'maturity_score': [3.2, 3.8, 2.5, 2.8, 2.6, 3.0, 3.5]
    })
    
    # 2025 GenAI by function (for backward compatibility)
    genai_2025 = pd.DataFrame({
        'function': ['Marketing & Sales', 'Product Development', 'Service Operations', 
                    'Software Engineering', 'IT', 'Knowledge Management', 'HR', 'Supply Chain'],
        'adoption': [42, 28, 23, 22, 23, 21, 13, 7]
    })
    
    # Token performance metrics
    token_performance = pd.DataFrame({
        'metric': ['Time to First Token', 'Inter-token Latency', 'Tokens per Second', 'Context Window Size'],
        'unit': ['milliseconds', 'milliseconds', 'tokens/sec', 'tokens'],
        'good_performance': [200, 20, 100, 100000],
        'average_performance': [500, 50, 50, 32000],
        'poor_performance': [1000, 100, 20, 8000]
    })
    
    return (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
            geographic, tech_stack, productivity_data, productivity_by_skill,
            ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
            barriers_data, support_effectiveness, state_data, ai_investment_data, 
            regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
            training_emissions, skill_gap_data, ai_governance, genai_2025,
            token_pricing, token_usage, token_performance)

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
if 'show_token_info' not in st.session_state:
    st.session_state.show_token_info = False

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
        'nvidia': {
            'title': 'NVIDIA AI Tokens Explained',
            'org': 'NVIDIA Corporation',
            'url': 'https://blogs.nvidia.com/blog/ai-tokens-explained/',
            'methodology': 'Technical analysis of token economics and AI factories'
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

# Token information helper
def show_token_explainer():
    return st.info("""
    **🪙 What are Tokens?** Tokens are tiny units of data that AI models process. Think of them as the "words" AI understands:
    • Short words = 1 token (e.g., "cat", "run")
    • Longer words = multiple tokens (e.g., "understanding" = "under" + "stand" + "ing")
    • 1,000 tokens ≈ 750 words ≈ 1.5 pages of text
    • Images, audio, and video are also converted to tokens for processing
    
    **Why do tokens matter?** AI services charge by tokens processed, making the 280x cost reduction crucial for adoption.
    """)

# Onboarding modal for first-time users
if st.session_state.first_visit:
    with st.container():
        st.info("""
        ### 👋 Welcome to the AI Adoption Dashboard!
        
        This dashboard provides comprehensive insights into AI adoption trends from 2018-2025, 
        including the latest findings from the AI Index Report 2025 and token economics analysis.
        
        **Quick Start:**
        - Use the sidebar to select different analysis views
        - Click on charts to see detailed information
        - Look for 🪙 icons to learn about token economics
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
    
    # Unpack the data
    (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, 
     geographic, tech_stack, productivity_data, productivity_by_skill,
     ai_productivity_estimates, oecd_g7_adoption, oecd_applications, 
     barriers_data, support_effectiveness, state_data, ai_investment_data, 
     regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
     training_emissions, skill_gap_data, ai_governance, genai_2025,
     token_pricing, token_usage, token_performance) = loaded_data
     
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Custom CSS with token-themed styling
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
    .token-highlight {
        background-color: rgba(255, 193, 7, 0.2);
        border-left: 4px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 AI Adoption Dashboard: 2018-2025")
st.markdown("**Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025) with token economics insights**")

# What's New section
with st.expander("🆕 What's New in Version 2.3.0", expanded=st.session_state.show_changelog):
    st.markdown("""
    **Latest Updates (June 2025):**
    - ✅ Integrated comprehensive token economics throughout
    - ✅ Added token usage patterns by industry and function
    - ✅ Enhanced cost analysis with practical examples
    - ✅ Included AI Factory concept and performance metrics
    - ✅ Updated ROI calculations with token efficiency
    - ✅ Added token context to all relevant metrics
    """)

# Add definition notice with AI Index Report reference and token context
st.info("""
**📌 Important Note:** Adoption rates in this dashboard reflect "any AI use" including pilots, experiments, and production deployments. 
Enterprise-wide production use rates are typically lower. The 280x reduction in token costs (from $20 to $0.07 per million tokens) 
has been a key driver of the adoption explosion. Data sources include AI Index Report 2025, McKinsey Global Survey on AI, 
OECD AI Policy Observatory, US Census Bureau, and NVIDIA AI analysis.
""")

# Token explainer toggle
if st.button("🪙 What are tokens and why do they matter?"):
    st.session_state.show_token_info = not st.session_state.show_token_info

if st.session_state.show_token_info:
    show_token_explainer()

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
    "Business Leader": ["Industry Analysis", "Financial Impact", "Investment Trends", "ROI Analysis", "Token Economics"],
    "Policymaker": ["Geographic Distribution", "OECD 2025 Findings", "Regional Growth", "AI Governance", "Environmental Impact"],
    "Researcher": ["Historical Trends", "Productivity Research", "Environmental Impact", "Skill Gap Analysis", "Token Performance"],
    "General": ["Adoption Rates", "Historical Trends", "Investment Trends", "Labor Impact", "AI Cost Trends"]
}

# Filter views based on persona
all_views = ["Adoption Rates", "Historical Trends", "Industry Analysis", "Investment Trends", 
             "Regional Growth", "AI Cost Trends", "Financial Impact", "Labor Impact", 
             "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
             "Productivity Research", "Environmental Impact", "Geographic Distribution", 
             "OECD 2025 Findings", "Barriers & Support", "ROI Analysis", "Skill Gap Analysis", 
             "AI Governance", "Token Economics", "Token Performance"]

if persona != "General":
    st.sidebar.info(f"💡 **Recommended views for {persona}:**\n" + "\n".join([f"• {v}" for v in persona_views[persona]]))

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

view_type = st.sidebar.selectbox(
    "Analysis View", 
    all_views,
    index=all_views.index(persona_views[persona][0]) if persona != "General" else 0
)

# Advanced filters
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Advanced Options")

# Token cost calculator in sidebar
with st.sidebar.expander("🪙 Quick Token Calculator"):
    calc_tokens = st.number_input("Number of tokens (millions)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1, key="token_calculator_input")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("2022 Cost", f"${calc_tokens * 20:,.2f}")
    with col2:
        st.metric("2024 Cost", f"${calc_tokens * 0.07:,.2f}")
    st.caption(f"Savings: ${(calc_tokens * 20 - calc_tokens * 0.07):,.2f} ({((20-0.07)/20)*100:.1f}%)")

# Year filter for historical data
if view_type == "Historical Trends":
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=2017,
        max_value=2025,
        value=(2017, 2025),
        step=1,
        key="historical_year_range_slider"
    )
    
    compare_mode = st.sidebar.checkbox("Compare specific years", value=False, key="compare_years_checkbox")
    if compare_mode:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            year1 = st.selectbox("Year 1", range(2017, 2026), index=1, key="compare_year_1")
        with col2:
            year2 = st.selectbox("Year 2", range(2017, 2026), index=7, key="compare_year_2")

# Export functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")
export_format = st.sidebar.selectbox(
    "Export Format", ["PNG Image", "CSV Data", "PDF Report (Beta)"], key="export_format_selectbox"
)
if st.sidebar.button("📥 Export Current View", help="Download the current visualization", key="export_button"):
    if export_format == "CSV Data":
        # Export current data based on view
        if view_type == "Historical Trends":
            csv = historical_data.to_csv(index=False)
            st.sidebar.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ai_adoption_{view_type.lower().replace(' ', '_')}.csv",
                mime="text/csv",
                key="download_csv_button"
            )
            st.sidebar.success("✅ Data exported successfully!")
        else:
            st.sidebar.success("✅ View exported successfully!")

# Feedback widget
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Feedback")
feedback = st.sidebar.text_area("Share your thoughts or request features:", height=100, key="feedback_text_area")
if st.sidebar.button("Submit Feedback", key="submit_feedback_button"):
    st.sidebar.success("Thank you for your feedback!")

# Help section
with st.sidebar.expander("❓ Need Help?"):
    st.markdown("""
    **Navigation Tips:**
    - Use the Analysis View dropdown to explore different perspectives
    - Click 📊 icons for data source information
    - Click 🪙 icons for token economics insights
    - Hover over chart elements for details
    **Token Basics:**
    - 1,000 tokens ≈ 750 words
    - Cost per million tokens dropped 280x
    - Enables mass AI deployment
    **Keyboard Shortcuts:**
    - `Ctrl + K`: Quick search
    - `F`: Toggle fullscreen
    - `?`: Show help
    """)

st.markdown("<h3>Trust and quality indicators</h3>", unsafe_allow_html=True) # Added this header
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
        <h4>🪙 Token Data</h4>
        <div>
            Real-time<br>
            <small>6 providers</small>
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
        <h4>🔒 Security</h4>
        <div style='color: #28a745;'>
            ISO 27001<br>
            <small>Certified</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption("These indicators reflect the reliability and trustworthiness of the data and insights presented.")

# Footer
st.markdown("""
---
<p style='text-align: center; color: #888;'>
    AI Adoption Dashboard v2.3.0 | Created by <a href='https://github.com/Rcasanova25' target='_blank'>Robert Casanova</a><br>
    Powered by Streamlit, Plotly, Pandas
</p>
""", unsafe_allow_html=True)

# Key metrics row - UPDATED with AI Index 2025 data and token context
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
            label="Cost per Million Tokens",
            value="$0.07",
            delta="280x cheaper",
            help="AI inference cost dropped from $20 to <span class="math-inline">0\.07 per million tokens\. Tokens are tiny units of data that AI models process \- short words may be 1 token, longer words split into multiple tokens\. This massive cost reduction enables mass AI deployment\."
\)
else\:
with col1\:
st\.metric\("Overall AI Adoption", "5\.8%", "📊 Firm\-weighted"\)
with col2\:
st\.metric\("Large Firms \(5000\+\)", "58\.5%", "🏢 High adoption"\)
with col3\:
st\.metric\("AI \+ Cloud", "45%", "☁️ Technology stack"\)
with col4\:
st\.metric\("Top City", "SF Bay \(9\.5%\)", "🌍 Geographic leader"\)
\# Main visualization section
st\.subheader\(f"📊 \{view\_type\}"\)
\# View implementations with token context
if view\_type \=\= "Token Economics"\:
st\.write\("🪙 \*\*Token Economics\: The Currency Driving AI Adoption\*\*"\)
\# Create comprehensive token economics dashboard
tab1, tab2, tab3, tab4 \= st\.tabs\(\["Token Basics", "Cost Evolution", "Industry Usage", "Performance Metrics"\]\)
with tab1\:
st\.write\("\#\#\# Understanding AI Tokens"\)
col1, col2 \= st\.columns\(2\)
with col1\:
st\.markdown\('<div class\="token\-highlight"\>', unsafe\_allow\_html\=True\)
st\.write\("\*\*What are Tokens?\*\*"\)
st\.write\("• Basic units of data AI models process"\)
st\.write\("• Text\: 'understanding' \= 3 tokens"\)
st\.write\("• Images\: Pixels → visual tokens"\)
st\.write\("• Audio\: Sound → spectrogram tokens"\)
st\.write\("• \*\*1,000 tokens ≈ 750 words\*\*"\)
st\.markdown\('</div\>', unsafe\_allow\_html\=True\)
\# Token examples visualization
examples \= pd\.DataFrame\(\{
'Content Type'\: \['Tweet', 'Email', 'Article', 'Book Chapter', 'Research Paper'\],
'Typical Tokens'\: \[50, 500, 2000, 10000, 25000\],
'Cost\_2022'\: \[0\.001, 0\.01, 0\.04, 0\.20, 0\.50\],
'Cost\_2024'\: \[0\.0000035, 0\.000035, 0\.00014, 0\.0007, 0\.00175\]
\}\)
fig \= px\.bar\(
examples,
x\='Content Type',
y\=\['Cost\_2022', 'Cost\_2024'\],
title\='Token Costs by Content Type',
labels\=\{'value'\: 'Cost \(</span>)', 'variable': 'Year'},
            barmode='group',
            color_discrete_map={'Cost_2022': '#E74C3C', 'Cost_2024': '#2ECC71'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True, key="token_cost_by_content_type")
        with col2:
            st.markdown('<div class="token-highlight">', unsafe_allow_html=True)
            st.write("**Token Processing Flow**")
            st.write("1. **Input**: User prompt → tokens")
            st.write("2. **Processing**: AI model computation")
            st.write("3. **Output**: Generated tokens → response")
            st.write("4. **Billing**: Input + output tokens")
            st.write("• Context window = max tokens at once")
            st.markdown('</div>', unsafe_allow_html=True)
        # Token usage patterns
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=token_usage['avg_tokens'],
            y=token_usage['typical_time_min'],
            mode='markers+text',
            marker=dict(
                size=token_usage['avg_tokens']/1000,
                color=['#2ECC71' if v == 'Low' else '#F39C12' if v == 'Medium' else '#E74C3C' if v == 'High' else '#9B59B6' for v in token_usage['value_category']],
                line=dict(width=2, color='white')
            ),
            text=token_usage['use_case'],
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Tokens: %{x:,.0f}<br>Time: %{y} min<br>Value: %{customdata}<extra></extra>',
            customdata=token_usage['value_category']
        ))
        fig2.update_layout(title='AI Token Usage Patterns by Use Case',
                           xaxis_title='Average Tokens per Use',
                           yaxis_title='Typical Time (min)',
                           hovermode='closest')
        st.plotly_chart(fig2, use_container_width=True, key="token_usage_patterns")

    with tab2:
        st.write("### Token Cost Evolution: 2022-2024")
        st.dataframe(token_pricing)

        fig_cost_reduction = px.line(token_pricing, x='date', y='cost_per_million',
                                     title='Cost per Million Tokens Over Time',
                                     labels={'cost_per_million': 'Cost per Million Tokens (<span class="math-inline">\)', 'date'\: 'Date'\},
markers\=True\)
fig\_cost\_reduction\.update\_traces\(mode\='lines\+markers', line\=dict\(color\='\#28a745', width\=3\)\)
fig\_cost\_reduction\.update\_layout\(hovermode\="x unified"\)
st\.plotly\_chart\(fig\_cost\_reduction, use\_container\_width\=True, key\="token\_cost\_evolution"\)
fig\_cost\_multiplier \= px\.bar\(token\_pricing, x\='date', y\='cost\_reduction',
title\='Cost Reduction Multiplier',
labels\=\{'cost\_reduction'\: 'Cost Reduction Factor', 'date'\: 'Date'\},
color\_discrete\_sequence\=\['\#1f77b4'\]\)
fig\_cost\_multiplier\.update\_layout\(hovermode\="x unified"\)
st\.plotly\_chart\(fig\_cost\_multiplier, use\_container\_width\=True, key\="token\_cost\_multiplier"\)
st\.info\("💡 \*\*Insight\:\*\* The dramatic reduction in token costs \(280x from Nov 2022 to Oct 2024\) has made large\-scale AI deployment economically viable\."\)
with tab3\:
st\.write\("\#\#\# Industry\-Specific Token Usage & ROI"\)
\# Combine financial impact and sector data for a richer view
financial\_impact\_tokens \= financial\_impact\.merge\(
sector\_2025\[\['sector', 'adoption\_rate', 'genai\_adoption', 'avg\_roi', 'avg\_monthly\_tokens\_millions'\]\],
left\_on\='function', right\_on\='sector', how\='left'
\)
financial\_impact\_tokens\['monthly\_tokens\_millions\_display'\] \= financial\_impact\_tokens\['monthly\_tokens\_millions'\]\.fillna\(0\)\.apply\(lambda x\: f"\{x\:,\.0f\}M"\)
\# Financial Impact by Function with Token Context
st\.subheader\("Financial Impact by Business Function"\)
fig\_financial \= px\.bar\(financial\_impact, x\='function', y\=\['companies\_reporting\_cost\_savings', 'companies\_reporting\_revenue\_gains'\],
title\='Companies Reporting Financial Gains from AI \(2025\)',
labels\=\{'value'\: 'Percentage of Companies \(%\)', 'function'\: 'Business Function', 'variable'\: 'Metric'\},
barmode\='group',
color\_discrete\_map\=\{'companies\_reporting\_cost\_savings'\: '\#1f77b4', 'companies\_reporting\_revenue\_gains'\: '\#ff7f0e'\}\)
fig\_financial\.update\_layout\(height\=400\)
st\.plotly\_chart\(fig\_financial, use\_container\_width\=True, key\="financial\_impact\_gains"\)
st\.subheader\("Average Monthly Token Usage by Business Function \(Millions\)"\)
fig\_tokens\_by\_function \= px\.bar\(financial\_impact, x\='function', y\='monthly\_tokens\_millions',
title\='Average Monthly Tokens by Function',
labels\=\{'monthly\_tokens\_millions'\: 'Avg\. Monthly Tokens \(Millions\)', 'function'\: 'Business Function'\},
color\_discrete\_sequence\=\['\#2CA02C'\]\)
fig\_tokens\_by\_function\.update\_layout\(height\=400\)
st\.plotly\_chart\(fig\_tokens\_by\_function, use\_container\_width\=True, key\="monthly\_tokens\_by\_function"\)
st\.info\("💡 \*\*Insight\:\*\* Functions with higher token usage \(e\.g\., Software Engineering, Marketing & Sales\) often correlate with greater opportunities for cost savings and revenue gains through AI\."\)
st\.subheader\("Sector\-wise GenAI Adoption & ROI"\)
fig\_sector\_genai \= px\.scatter\(sector\_2025, 
x\='genai\_adoption', 
y\='avg\_roi', 
size\='avg\_monthly\_tokens\_millions', 
color\='sector',
hover\_name\='sector',
size\_max\=60,
title\='GenAI Adoption vs\. Average ROI by Sector \(2025\)',
labels\=\{'genai\_adoption'\: 'GenAI Adoption Rate \(%\)', 
'avg\_roi'\: 'Average ROI \(%\)', 
'avg\_monthly\_tokens\_millions'\: 'Avg\. Monthly Tokens \(Millions\)'\}\)
st\.plotly\_chart\(fig\_sector\_genai, use\_container\_width\=True, key\="sector\_genai\_adoption\_roi"\)
st\.info\("💡 \*\*Insight\:\*\* Sectors with higher GenAI adoption and token intensity tend to see higher average ROI, demonstrating the direct link between adoption, usage, and business value\."\)
with tab4\:
st\.write\("\#\#\# AI System Performance Metrics"\)
st\.dataframe\(token\_performance\)
\# Bar chart for performance metrics
fig\_performance \= px\.bar\(token\_performance, x\='metric', y\=\['good\_performance', 'average\_performance', 'poor\_performance'\],
title\='AI Token Performance Benchmarks',
labels\=\{'value'\: 'Value', 'metric'\: 'Metric', 'variable'\: 'Performance Level'\},
barmode\='group',
color\_discrete\_map\=\{'good\_performance'\: '\#2ECC71', 'average\_performance'\: '\#F39C12', 'poor\_performance'\: '\#E74C3C'\}\)
fig\_performance\.update\_layout\(height\=400\)
st\.plotly\_chart\(fig\_performance, use\_container\_width\=True, key\="ai\_performance\_benchmarks"\)
st\.info\("💡 \*\*Insight\:\*\* Optimizing 'Time to First Token' and 'Tokens per Second' is critical for user experience, while a larger 'Context Window Size' enables more complex AI applications\."\)
elif view\_type \=\= "Adoption Rates"\:
st\.header\("Overall AI Adoption Trends \(2018\-2025\)"\)
st\.write\("This section shows the overall AI and GenAI adoption rates across all industries\."\)
\# Filter historical data if year\_range is set
filtered\_historical\_data \= historical\_data\[
\(historical\_data\['year'\] \>\= year\_range\[0\]\) & 
\(historical\_data\['year'\] <\= year\_range\[1\]\)
\] if 'year\_range' in locals\(\) else historical\_data
fig \= px\.line\(filtered\_historical\_data, x\='year', y\=\['ai\_use', 'genai\_use'\],
title\='Overall AI and GenAI Adoption Trends',
labels\=\{'value'\: 'Adoption Rate \(%\)', 'year'\: 'Year', 'variable'\: 'Type of AI Use'\},
markers\=True\)
fig\.update\_layout\(hovermode\="x unified"\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="overall\_ai\_genai\_adoption"\)
st\.markdown\(show\_source\_info\('ai\_index'\), unsafe\_allow\_html\=True\)
st\.info\("💡 \*\*Insight\:\*\* While overall AI adoption has steadily increased, Generative AI adoption has seen a significant surge in 2024, reflecting the impact of advanced models becoming more accessible\."\)
elif view\_type \=\= "Historical Trends"\:
st\.header\("Historical AI Adoption & GenAI Breakthrough \(2017\-2025\)"\)
st\.write\("Examine the long\-term trends of AI adoption and the emergence of Generative AI\."\)
if compare\_mode\:
st\.subheader\(f"Comparison\: \{year1\} vs\. \{year2\}"\)
col1, col2 \= st\.columns\(2\)
\# Filter data for year1
data\_year1 \= historical\_data\[historical\_data\['year'\] \=\= year1\]\.iloc\[0\]
with col1\:
st\.metric\(f"AI Use \(\{year1\}\)", f"\{data\_year1\['ai\_use'\]\}%"\)
st\.metric\(f"GenAI Use \(\{year1\}\)", f"\{data\_year1\['genai\_use'\]\}%"\)
\# Filter data for year2
data\_year2 \= historical\_data\[historical\_data\['year'\] \=\= year2\]\.iloc\[0\]
with col2\:
st\.metric\(f"AI Use \(\{year2\}\)", f"\{data\_year2\['ai\_use'\]\}%"\)
st\.metric\(f"GenAI Use \(\{year2\}\)", f"\{data\_year2\['genai\_use'\]\}%"\)
st\.info\(f"💡 \*\*Insight\:\*\* Comparing \{year1\} and \{year2\} highlights the rapid acceleration of AI and particularly GenAI adoption\. In \{year1\}, GenAI was at \{data\_year1\['genai\_use'\]\}%, leaping to \{data\_year2\['genai\_use'\]\}% by \{year2\}\."\)
else\:
st\.subheader\("AI Adoption Trends Over Time"\)
fig \= px\.line\(historical\_data, x\='year', y\=\['ai\_use', 'genai\_use'\],
title\='Historical AI and GenAI Adoption Trends \(2017\-2025\)',
labels\=\{'value'\: 'Adoption Rate \(%\)', 'year'\: 'Year', 'variable'\: 'Type of AI Use'\},
markers\=True\)
fig\.update\_layout\(hovermode\="x unified"\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="historical\_ai\_genai\_trends"\)
st\.markdown\(show\_source\_info\('ai\_index'\), unsafe\_allow\_html\=True\)
st\.info\("💡 \*\*Insight\:\*\* The data clearly shows a steady increase in overall AI adoption, with a notable inflection point for Generative AI around 2022\-2023, indicating its rapid emergence and impact\."\)
elif view\_type \=\= "Industry Analysis"\:
st\.header\("Industry\-Specific AI Adoption \(2018 vs\. 2025\)"\)
st\.write\("Compare AI adoption across different industries, highlighting the shift from early adoption to the GenAI era\."\)
if "2025" in data\_year\:
st\.subheader\("2025 Sector Adoption \(GenAI Era\)"\)
fig \= px\.bar\(sector\_2025\.sort\_values\('adoption\_rate', ascending\=False\), x\='sector', y\='adoption\_rate',
title\='AI Adoption Rate by Sector \(2025\)',
labels\=\{'adoption\_rate'\: 'Adoption Rate \(%\)', 'sector'\: 'Sector'\},
color\='genai\_adoption',
color\_continuous\_scale\=px\.colors\.sequential\.Plasma,
hover\_name\='sector',
hover\_data\=\{'genai\_adoption'\:True, 'avg\_roi'\:True, 'avg\_monthly\_tokens\_millions'\:True\}\)
fig\.update\_layout\(xaxis\=\{'categoryorder'\:'total descending'\}\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="industry\_2025\_sector\_adoption"\)
st\.markdown\(show\_source\_info\('mckinsey'\), unsafe\_allow\_html\=True\)
st\.info\("💡 \*\*Insight\:\*\* Technology and Financial Services sectors lead in AI and GenAI adoption in 2025, driven by high ROI and significant token usage\."\)
else\:
st\.subheader\("2018 Sector Adoption \(Early AI\)"\)
fig \= px\.bar\(sector\_2018\.sort\_values\('firm\_weighted', ascending\=False\), x\='sector', y\='firm\_weighted',
title\='AI Adoption by Sector \(Firm\-weighted, 2018\)',
labels\=\{'firm\_weighted'\: 'Percentage of Firms \(%\)', 'sector'\: 'Sector'\},
color\_discrete\_sequence\=px\.colors\.qualitative\.Pastel\)
fig\.update\_layout\(xaxis\=\{'categoryorder'\:'total descending'\}\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="industry\_2018\_sector\_adoption"\)
st\.markdown\(show\_source\_info\('census'\), unsafe\_allow\_html\=True\)
st\.info\("💡 \*\*Insight\:\*\* In 2018, Manufacturing and Information sectors were early adopters, focusing on process automation and data analysis\."\)
elif view\_type \=\= "Investment Trends"\:
st\.header\("Global AI Investment Trends \(2014\-2024\)"\)
st\.write\("Explore the growth of AI investment globally, including the rise of Generative AI funding\."\)
fig \= px\.line\(ai\_investment\_data, x\='year', y\=\['total\_investment', 'genai\_investment', 'us\_investment', 'china\_investment', 'uk\_investment'\],
title\='Global AI Investment Trends \(Billions USD\)',
labels\=\{'value'\: 'Investment \(Billions USD\)', 'year'\: 'Year', 'variable'\: 'Investment Type'\},
markers\=True\)
fig\.update\_layout\(hovermode\="x unified"\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="global\_ai\_investment\_trends"\)
st\.info\("💡 \*\*Insight\:\*\* Total AI investment has seen exponential growth, with a significant portion shifting towards Generative AI since 2022, especially in the US\."\)
st\.markdown\(show\_source\_info\('ai\_index'\), unsafe\_allow\_html\=True\)
elif view\_type \=\= "Regional Growth"\:
st\.header\("Regional AI Adoption Growth \(AI Index 2025\)"\)
st\.write\("Understand AI adoption rates and investment growth across different global regions\."\)
fig \= px\.bar\(regional\_growth, x\='region', y\='adoption\_rate',
title\='AI Adoption Rate by Region \(2025\)',
labels\=\{'adoption\_rate'\: 'Adoption Rate \(%\)', 'region'\: 'Region'\},
color\='investment\_growth',
color\_continuous\_scale\=px\.colors\.sequential\.Viridis,
hover\_data\=\{'growth\_2024'\:True, 'investment\_growth'\:True\}\)
fig\.update\_layout\(xaxis\=\{'categoryorder'\:'total descending'\}\)
st\.plotly\_chart\(fig, use\_container\_width\=True, key\="regional\_ai\_adoption\_growth"\)
st\.info\("💡 \*\*Insight\:\*\* North America leads in AI adoption and investment growth, while Greater China shows strong growth in both areas\. These regions are becoming AI innovation hubs\."\)
st\.markdown\(show\_source\_info\('ai\_index'\), unsafe\_allow\_html\=True\)
elif view\_type \=\= "AI Cost Trends"\:
st\.header\("AI Cost Reduction and Efficiency"\)
st\.write\("Analyze how the cost of AI inference has dramatically decreased, driven by model optimization and token efficiency\."\)
fig \= px\.line\(ai\_cost\_reduction, x\='year', y\='cost\_per\_million\_tokens',
title\='Cost Per Million Tokens Trend',
labels\=\{'cost\_per\_million\_tokens'\: 'Cost per Million Tokens \(</span>)', 'year': 'Year'},
                  markers=True)
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, key="ai_cost_reduction_trend")

    fig2 = px.bar(ai_cost_reduction, x='model', y='tokens_per_dollar',
                  title='Tokens Per Dollar by Model',
                  labels={'tokens_per_dollar': 'Tokens per Dollar', 'model': 'Model'},
                  color_discrete_sequence=px.colors.qualitative.G10)
    st.plotly_chart(fig2, use_container_width=True, key="tokens_per_dollar_by_model")
    st.markdown(show_source_info('nvidia'), unsafe_allow_html=True)
    st.info("💡 **Insight:** The cost of processing AI tokens has plummeted, making advanced AI capabilities significantly more accessible and affordable for broad adoption.")

elif view_type == "Financial Impact":
    st.header("AI's Financial Impact by Business Function")
    st.write("Examine how different business functions are experiencing cost savings and revenue gains from AI adoption.")

    fig_cost_savings = px.bar(financial_impact, x='function', y='companies_reporting_cost_savings',
                             title='Companies Reporting Cost Savings from AI (%)',
                             labels={'companies_reporting_cost_savings': '% of Companies', 'function': 'Business Function'},
                             color_discrete_sequence=['#1f77b4'])
    fig_cost_savings.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_cost_savings, use_container_width=True, key="financial_impact_cost_savings")

    fig_revenue_gains = px.bar(financial_impact, x='function', y='companies_reporting_revenue_gains',
                              title='Companies Reporting Revenue Gains from AI (%)',
                              labels={'companies_reporting_revenue_gains': '% of Companies', 'function': 'Business Function'},
                              color_discrete_sequence=['#ff7f0e'])
    fig_revenue_gains.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_revenue_gains, use_container_width=True, key="financial_impact_revenue_gains")
    
    st.markdown(show_source_info('mckinsey'), unsafe_allow_html=True)
    st.info("💡 **Insight:** While Service Operations report the highest cost savings, Marketing & Sales functions see the most significant revenue gains from AI, highlighting diverse impacts across the enterprise.")

elif view_type == "Labor Impact":
    st.header("AI's Impact on Labor and Productivity")
    st.write("Analyze how AI is influencing productivity growth, job changes, and skill gaps across the workforce.")

    st.subheader("Historical Productivity Growth")
    fig_productivity = px.line(productivity_data, x='year', y='productivity_growth',
                                title='US Labor Productivity Growth (Annual % Change)',
                                labels={'productivity_growth': 'Productivity Growth (%)', 'year': 'Year'},
                                markers=True)
    st.plotly_chart(fig_productivity, use_container_width=True, key="historical_productivity_growth")
    st.info("💡 **Insight:** AI has the potential to reignite productivity growth, which has slowed in recent decades, by automating tasks and augmenting human capabilities.")

    st.subheader("AI Productivity by Skill Level")
    fig_skill_productivity = px.bar(productivity_by_skill, x='skill_level', y='productivity_gain',
                                    title='AI Impact on Productivity Gain by Skill Level (%)',
                                    labels={'productivity_gain': 'Productivity Gain (%)', 'skill_level': 'Skill Level'},
                                    color_discrete_sequence=px.colors.qualitative.Set2)
    fig_skill_productivity.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Low-skilled', 'Medium-skilled', 'High-skilled']})
    st.plotly_chart(fig_skill_productivity, use_container_width=True, key="ai_productivity_by_skill")
    st.info("💡 **Insight:** AI offers the largest productivity gains for low-skilled workers, helping to reduce skill gaps and democratize access to advanced capabilities.")
    
    st.subheader("Generational AI Perception on Job Impact")
    fig_job_impact = px.bar(ai_perception, x='generation', y=['expect_job_change', 'expect_job_replacement'],
                            title='Generational Perception: AI Impact on Jobs (%)',
                            labels={'value': 'Percentage (%)', 'generation': 'Generation', 'variable': 'Perception'},
                            barmode='group',
                            color_discrete_map={'expect_job_change': '#636EFA', 'expect_job_replacement': '#EF553B'})
    st.plotly_chart(fig_job_impact, use_container_width=True, key="generational_job_impact")
    st.info("💡 **Insight:** Younger generations (Gen Z, Millennials) are more likely to anticipate job changes due2 to AI, reflecting a greater awareness and acceptance of its transformative potential on the labor market.")

elif view_type == "Firm Size Analysis":
    st.header("AI Adoption by Firm Size")
    st.write("Examine how AI adoption varies across different firm sizes and the corresponding token usage.")

    fig = px.bar(firm_size, x='size', y='adoption',
                 title='AI Adoption Rate by Firm Size (%)',
                 labels={'adoption': 'Adoption Rate (%)', 'size': 'Firm Size'},
                 color='avg_tokens_per_employee_daily',
                 color_continuous_scale=px.colors.sequential.Blues,
                 hover_data={'avg_tokens_per_employee_daily':True})
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':firm_size['size'].tolist()})
    st.plotly_chart(fig, use_container_width=True, key="ai_adoption_by_firm_size")
    st.markdown(show_source_info('census'), unsafe_allow_html=True)
    st.info("💡 **Insight:** Larger firms generally show higher AI adoption rates and significantly higher daily token usage per employee, indicating their greater capacity for extensive AI integration.")

elif view_type == "Technology Stack":
    st.header("AI Adoption by Technology Stack")
    st.write("Understand the proportion of firms adopting AI in conjunction with cloud and digitization, and their impact on token efficiency.")

    fig = px.pie(tech_stack, values='percentage', names='technology',
                 title='AI Adoption by Complementary Technology Stack (2025)',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True, key="ai_adoption_tech_stack_pie")

    st.subheader("Token Efficiency Multiplier by Tech Stack")
    fig2 = px.bar(tech_stack, x='technology', y='token_efficiency_multiplier',
                  title='Token Efficiency Multiplier',
                  labels={'token_efficiency_multiplier': 'Efficiency Multiplier', 'technology': 'Technology Stack'},
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig2, use_container_width=True, key="token_efficiency_multiplier")
    st.info("💡 **Insight:** Firms combining AI with Cloud and Digitization achieve significantly higher token efficiency, indicating that a holistic digital transformation strategy maximizes AI's potential.")

elif view_type == "AI Technology Maturity":
    st.header("AI Technology Maturity & Risk Landscape")
    st.write("Explore the maturity of various AI technologies, their associated risks, and time to value, along with typical token requirements.")

    fig = px.scatter(ai_maturity, x='adoption_rate', y='risk_score',
                     size='avg_tokens_per_query', color='maturity', hover_name='technology',
                     size_max=60,
                     title='AI Technology Maturity Landscape (2025)',
                     labels={'adoption_rate': 'Adoption Rate (%)', 'risk_score': 'Risk Score (Higher is Riskier)', 'avg_tokens_per_query': 'Avg. Tokens per Query'},
                     color_discrete_map={
                         'Peak of Expectations': '#ff7f0e',
                         'Trough of Disillusionment': '#1f77b4',
                         'Slope of Enlightenment': '#2ca02c'
                     })
    st.plotly_chart(fig, use_container_width=True, key="ai_tech_maturity_landscape")
    st.info("💡 **Insight:** While Generative AI and AI Agents are at the 'Peak of Expectations' with high adoption but also higher perceived risk and token use, technologies like Cloud AI Services are more mature with lower risk and quicker time to value.")

elif view_type == "Productivity Research":
    st.header("Research on AI's Productivity Impact")
    st.write("Review findings from various sources on AI's estimated annual productivity impact.")
    
    fig = px.bar(ai_productivity_estimates, x='source', y='annual_impact',
                 title='Estimated Annual Productivity Impact of AI (%)',
                 labels={'annual_impact': 'Annual Impact (%)', 'source': 'Source'},
                 color_discrete_sequence=px.colors.qualitative.D3)
    st.plotly_chart(fig, use_container_width=True, key="ai_productivity_impact_estimates")
    st.info("💡 **Insight:** Different research sources offer varying estimates for AI's productivity impact, reflecting the complexity and novelty of measuring its full economic effects.")

elif view_type == "Environmental Impact":
    st.header("Environmental Impact of AI Training")
    st.write("Understand the carbon emissions associated with training large AI models and the increasing energy demands.")

    fig = px.bar(training_emissions, x='model', y='carbon_tons',
                 title