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


# Initialize session state for navigation if not already present
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = None
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

# Load data once
(historical_data, sector_2018, sector_2025, firm_size, ai_maturity,
 geographic, tech_stack, productivity_data, productivity_by_skill,
 ai_productivity_estimates, oecd_g7_adoption, oecd_applications,
 barriers_data, support_effectiveness, state_data, ai_investment_data,
 regional_growth, ai_cost_reduction, financial_impact, ai_perception,
 training_emissions, skill_gap_data, ai_governance, genai_2025,
 token_economics, token_usage_patterns, token_optimization, token_pricing_evolution) = load_data()


# Persona-based welcome and navigation
if st.session_state.first_visit:
    with st.container():
        st.info("""
        ### 👋 Welcome to the AI Adoption Dashboard!
        This dashboard provides comprehensive insights into AI adoption trends from 2018-2025, including the latest findings from the AI Index Report 2025.

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
            if st.button("💡 Enthusiast"):
                st.session_state.selected_persona = "Enthusiast"
                st.session_state.first_visit = False
                st.rerun()

    st.markdown("---")
    st.write("Or, continue to explore all features:")
    if st.button("🚀 Explore All Features"):
        st.session_state.selected_persona = "All"
        st.session_state.first_visit = False
        st.rerun()

else:
    # Sidebar navigation
    st.sidebar.title("AI Adoption Dashboard")
    st.sidebar.header("Navigation")

    # Define menu items based on persona
    menu_items = {
        "Business Leader": {
            "Overview": "📊 Overall Trends",
            "Sector Analysis": "🏢 Sector & Firm Size Adoption",
            "Investment Trends": "💰 Investment & ROI",
            "Productivity Impact": "📈 Productivity & Workforce",
            "Barriers & Solutions": "🚧 Overcoming Challenges",
            "Token Economics": "💸 Token Economics"
        },
        "Policymaker": {
            "Overview": "📊 Overall Trends",
            "Geographic Insights": "🌍 Regional Adoption",
            "Regulatory & Governance": "⚖️ Governance & Ethics",
            "Investment Trends": "💰 Investment & ROI",
            "Workforce & Skills": "🧑‍💼 Workforce & Skills",
            "Barriers & Solutions": "🚧 Overcoming Challenges",
            "Environmental Impact": "🌱 Environmental Impact"
        },
        "Researcher": {
            "Overview": "📊 Overall Trends",
            "AI Maturity & Tech Stack": "🔬 AI Maturity & Tech Stack",
            "Productivity Impact": "📈 Productivity & Workforce",
            "AI Applications": "🛠️ AI Applications",
            "Investment Trends": "💰 Investment & ROI",
            "Geographic Insights": "🌍 Regional Adoption",
            "Generational Perception": "🧑‍🤝‍🧑 Generational Perception",
            "Environmental Impact": "🌱 Environmental Impact",
            "Token Economics": "💸 Token Economics"
        },
        "Enthusiast": {
            "Overview": "📊 Overall Trends",
            "AI Applications": "🛠️ AI Applications",
            "AI Cost Trends": "📉 AI Cost Trends",
            "Generational Perception": "🧑‍🤝‍🧑 Generational Perception",
            "Environmental Impact": "🌱 Environmental Impact",
            "Token Economics": "💸 Token Economics"
        },
        "All": {
            "Overview": "📊 Overall Trends",
            "Sector Analysis": "🏢 Sector & Firm Size Adoption",
            "AI Maturity & Tech Stack": "🔬 AI Maturity & Tech Stack",
            "Geographic Insights": "🌍 Regional Adoption",
            "Productivity Impact": "📈 Productivity & Workforce",
            "AI Applications": "🛠️ AI Applications",
            "Barriers & Solutions": "🚧 Overcoming Challenges",
            "Investment Trends": "💰 Investment & ROI",
            "Workforce & Skills": "🧑‍💼 Workforce & Skills",
            "Regulatory & Governance": "⚖️ Governance & Ethics",
            "Generational Perception": "🧑‍🤝‍🧑 Generational Perception",
            "Environmental Impact": "🌱 Environmental Impact",
            "AI Cost Trends": "📉 AI Cost Trends",
            "Token Economics": "💸 Token Economics"
        }
    }

    persona_selection_key = f"persona_select_{st.session_state.selected_persona}"
    selected_view = st.sidebar.radio(
        "Choose a view:",
        list(menu_items[st.session_state.selected_persona].values()),
        key=persona_selection_key
    )

    # Allow changing persona
    st.sidebar.markdown("---")
    st.sidebar.subheader("Change Persona")
    current_persona_index = ["Business Leader", "Policymaker", "Researcher", "Enthusiast", "All"].index(st.session_state.selected_persona)
    new_persona = st.sidebar.selectbox("Select your role:", ["Business Leader", "Policymaker", "Researcher", "Enthusiast", "All"], index=current_persona_index)
    if new_persona != st.session_state.selected_persona:
        st.session_state.selected_persona = new_persona
        st.session_state.first_visit = False # Ensure welcome screen doesn't reappear unnecessarily
        st.rerun()

    # Main content area
    st.title("AI Adoption Dashboard")
    st.subheader(f"Current View: {selected_view}")

    if selected_view == "📊 Overall Trends":
        st.header("Overall AI Adoption Trends (2018-2025)")
        st.write("This section provides a high-level overview of AI and Generative AI adoption rates over time.")

        # Historical Adoption Trends
        st.markdown("### Historical AI Adoption Rates")
        fig_historical = px.line(historical_data, x='year', y=['ai_use', 'genai_use'],
                                 markers=True,
                                 labels={'value':'Adoption Rate (%)', 'year':'Year', 'variable':'AI Type'},
                                 title='Overall AI and Generative AI Adoption Rates (2017-2025)')
        fig_historical.update_traces(hovertemplate='Year: %{x}<br>Adoption Rate: %{y}%')
        fig_historical.update_layout(hovermode="x unified")
        st.plotly_chart(fig_historical, use_container_width=True)
        st.info("The significant jump in 2024 for both AI and GenAI reflects the rapid advancements and increased awareness of Generative AI capabilities.")

        # Investment Trends Overview
        st.markdown("### AI Investment Overview")
        fig_investment = px.bar(ai_investment_data, x='year', y='total_investment',
                                title='Global Total AI Investment (Billions USD)',
                                labels={'total_investment': 'Investment (Billions USD)', 'year': 'Year'},
                                hover_data={'genai_investment': ':.1f', 'us_investment': ':.1f',
                                            'china_investment': ':.1f', 'uk_investment': ':.1f'})
        st.plotly_chart(fig_investment, use_container_width=True)
        st.write("Total AI investment has seen a steady increase, with a notable acceleration in recent years.")

        # Regional Growth
        st.markdown("### Regional AI Adoption Growth")
        fig_regional = px.bar(regional_growth.sort_values('adoption_rate', ascending=False),
                              x='region', y='adoption_rate',
                              color='region',
                              title='AI Adoption Rate by Region (2024)',
                              labels={'adoption_rate': 'Adoption Rate (%)'},
                              hover_data={'growth_2024': True, 'investment_growth': True})
        st.plotly_chart(fig_regional, use_container_width=True)
        st.info("North America currently leads in AI adoption, but Greater China shows the highest growth rate in 2024.")

    elif selected_view == "🏢 Sector & Firm Size Adoption":
        st.header("AI Adoption by Sector and Firm Size")
        st.write("This section analyzes how AI adoption varies across different industries and company sizes.")

        # Sectoral Adoption (2025)
        st.markdown("### AI and GenAI Adoption by Sector (2025)")
        fig_sector_2025 = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]],
                                        subplot_titles=['Overall AI Adoption by Sector', 'Generative AI Adoption by Sector'])

        fig_sector_2025.add_trace(go.Pie(labels=sector_2025['sector'], values=sector_2025['adoption_rate'], name="AI Adoption"),
                                  1, 1)
        fig_sector_2025.add_trace(go.Pie(labels=sector_2025['sector'], values=sector_2025['genai_adoption'], name="GenAI Adoption"),
                                  1, 2)

        fig_sector_2025.update_layout(title_text='AI and Generative AI Adoption Rates by Sector (2025)', height=500)
        st.plotly_chart(fig_sector_2025, use_container_width=True)
        st.info("Technology and Financial Services sectors demonstrate the highest AI and GenAI adoption rates in 2025.")

        # Sectoral Adoption (2018) for comparison
        st.markdown("### AI Adoption by Sector (2018 - Firm Weighted)")
        fig_sector_2018 = px.bar(sector_2018.sort_values('firm_weighted', ascending=True),
                                x='firm_weighted', y='sector', orientation='h',
                                title='AI Adoption Across Sectors (2018, Firm Weighted)',
                                labels={'firm_weighted': 'Percentage of Firms Weighted (%)', 'sector': 'Sector'})
        st.plotly_chart(fig_sector_2018, use_container_width=True)
        st.write("In 2018, Manufacturing and Information sectors led in AI adoption.")

        # Firm Size Adoption
        st.markdown("### AI Adoption by Firm Size")
        fig_firm_size = px.bar(firm_size, x='size', y='adoption',
                               title='AI Adoption Rate by Firm Size',
                               labels={'adoption': 'Adoption Rate (%)', 'size': 'Firm Size (Number of Employees)'},
                               category_orders={"size": ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499',
                                                        '500-999', '1000-2499', '2500-4999', '5000+']})
        st.plotly_chart(fig_firm_size, use_container_width=True)
        st.success("Larger firms consistently show higher AI adoption rates, indicating better resource availability for implementation.")

    elif selected_view == "🔬 AI Maturity & Tech Stack":
        st.header("AI Maturity and Technology Stack Analysis")
        st.write("Explore the maturity levels of various AI technologies and the composition of current AI tech stacks.")

        # AI Maturity Landscape
        st.markdown("### AI Technology Maturity Landscape")
        fig_maturity = px.scatter(ai_maturity, x='time_to_value', y='adoption_rate',
                                  size='risk_score', color='maturity',
                                  hover_name='technology',
                                  log_x=False, size_max=60,
                                  title='AI Technology Maturity: Adoption vs. Time to Value',
                                  labels={'time_to_value': 'Time to Value (Years)',
                                          'adoption_rate': 'Adoption Rate (%)',
                                          'risk_score': 'Risk Score (Higher is Riskier)'})
        st.plotly_chart(fig_maturity, use_container_width=True)
        st.info("Generative AI is at the 'Peak of Expectations' with high adoption but also a high risk score, while Cloud AI Services are more mature.")

        # Technology Stack Composition
        st.markdown("### AI Technology Stack Composition")
        fig_tech_stack = px.pie(tech_stack, values='percentage', names='technology',
                               title='Current AI Technology Stack Composition',
                               hole=0.4)
        fig_tech_stack.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_tech_stack, use_container_width=True)
        st.write("A significant portion of companies integrate AI with both cloud and digitization initiatives.")

    elif selected_view == "🌍 Regional Adoption":
        st.header("Geographic AI Adoption Insights")
        st.write("This section visualizes AI adoption rates across different U.S. cities and states, along with global regional growth.")

        # AI Adoption by City (Map)
        st.markdown("### AI Adoption Rate by U.S. City")
        fig_geo = px.scatter_mapbox(geographic, lat="lat", lon="lon", color="rate", size="population_millions",
                                    hover_name="city", hover_data={"state": True, "gdp_billions": ':.2f', "rate": ':.2f'},
                                    color_continuous_scale=px.colors.sequential.Plasma, zoom=3,
                                    title='AI Adoption Rate by U.S. City (Bubble size indicates Population in Millions)')
        fig_geo.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig_geo, use_container_width=True)
        st.info("Major tech hubs like San Francisco Bay Area and New York show high AI adoption rates.")

        # AI Adoption by State (Bar chart)
        st.markdown("### AI Adoption Rate by U.S. State (Average)")
        fig_state = px.bar(state_data.sort_values('rate', ascending=False),
                           x='state_code', y='rate',
                           title='Average AI Adoption Rate by U.S. State',
                           labels={'state_code': 'State', 'rate': 'Average Adoption Rate (%)'})
        st.plotly_chart(fig_state, use_container_width=True)
        st.write("California, New York, and Washington states exhibit higher average AI adoption rates.")

        # Regional AI Adoption Growth
        st.markdown("### Global Regional AI Adoption Growth (2024)")
        fig_regional_growth = px.bar(regional_growth.sort_values('growth_2024', ascending=False),
                                     x='region', y='growth_2024',
                                     color='region',
                                     title='AI Adoption Growth Rate by Region (2024)',
                                     labels={'growth_2024': 'Growth Rate (%)'})
        st.plotly_chart(fig_regional_growth, use_container_width=True)
        st.success("Greater China leads in AI adoption growth rate in 2024, followed by Europe.")

    elif selected_view == "📈 Productivity & Workforce":
        st.header("AI Impact on Productivity and Workforce")
        st.write("This section examines the relationship between AI adoption and productivity growth, along with its impact on different skill levels and worker demographics.")

        # Productivity Growth over time
        st.markdown("### U.S. Productivity Growth vs. Young Workers Share")
        fig_prod = make_subplots(specs=[[{"secondary_y": True}]])

        fig_prod.add_trace(go.Scatter(x=productivity_data['year'], y=productivity_data['productivity_growth'],
                                       mode='lines+markers', name='Productivity Growth (%)', line=dict(color='blue')),
                           secondary_y=False)

        fig_prod.add_trace(go.Scatter(x=productivity_data['year'], y=productivity_data['young_workers_share'],
                                       mode='lines+markers', name='Young Workers Share (%)', line=dict(color='red')),
                           secondary_y=True)

        fig_prod.update_layout(title_text='U.S. Productivity Growth and Young Workers Share (1980-2025)',
                               hovermode="x unified")
        fig_prod.update_xaxes(title_text="Year")
        fig_prod.update_yaxes(title_text="Productivity Growth (%)", secondary_y=False)
        fig_prod.update_yaxes(title_text="Young Workers Share (%)", secondary_y=True)
        st.plotly_chart(fig_prod, use_container_width=True)
        st.info("While overall productivity growth has fluctuated, AI is expected to contribute positively in the coming years.")

        # AI Productivity by Skill Level
        st.markdown("### AI Productivity Gain and Skill Gap Reduction by Skill Level")
        fig_skill_prod = make_subplots(rows=1, cols=2, subplot_titles=('Productivity Gain from AI', 'Skill Gap Reduction from AI'))

        fig_skill_prod.add_trace(go.Bar(x=productivity_by_skill['skill_level'], y=productivity_by_skill['productivity_gain'],
                                        name='Productivity Gain (%)', marker_color='teal'), 1, 1)
        fig_skill_prod.add_trace(go.Bar(x=productivity_by_skill['skill_level'], y=productivity_by_skill['skill_gap_reduction'],
                                        name='Skill Gap Reduction (%)', marker_color='lightcoral'), 1, 2)

        fig_skill_prod.update_layout(title_text='AI Impact on Productivity and Skill Gaps by Skill Level', height=450)
        fig_skill_prod.update_yaxes(title_text='Percentage (%)')
        st.plotly_chart(fig_skill_prod, use_container_width=True)
        st.write("AI tends to offer higher productivity gains and skill gap reduction for low-skilled workers.")

        # AI Productivity Estimates
        st.markdown("### Annual AI Productivity Impact Estimates")
        fig_ai_prod_est = px.bar(ai_productivity_estimates.sort_values('annual_impact', ascending=False),
                                 x='source', y='annual_impact',
                                 title='Annual AI Productivity Impact Estimates by Source',
                                 labels={'annual_impact': 'Annual Impact on Productivity (%)', 'source': 'Source'})
        st.plotly_chart(fig_ai_prod_est, use_container_width=True)
        st.success("Various research institutions project a significant annual impact of AI on productivity, ranging from 0.07% to 2.5%.")

    elif selected_view == "🛠️ AI Applications":
        st.header("AI Application Usage Trends")
        st.write("Discover the most adopted AI applications, differentiating between Generative AI and traditional AI uses.")

        # Split into GenAI and Traditional AI
        genai_apps = oecd_applications[oecd_applications['category'] == 'GenAI']
        traditional_apps = oecd_applications[oecd_applications['category'] == 'Traditional AI']

        # AI Applications Usage
        st.markdown("### AI Application Usage Rates (GenAI vs. Traditional AI)")
        fig_apps = go.Figure()

        # GenAI applications
        fig_apps.add_trace(go.Bar(
            name='Generative AI',
            y=genai_apps.sort_values('usage_rate')['application'],
            x=genai_apps.sort_values('usage_rate')['usage_rate'],
            orientation='h',
            marker_color='#FF7F0E', # Orange for GenAI
            text=[f'{x}%' for x in genai_apps.sort_values('usage_rate')['usage_rate']],
            textposition='outside'
        ))

        # Traditional AI applications
        fig_apps.add_trace(go.Bar(
            name='Traditional AI',
            y=traditional_apps.sort_values('usage_rate')['application'],
            x=traditional_apps.sort_values('usage_rate')['usage_rate'],
            orientation='h',
            marker_color='#3498DB', # Blue for Traditional AI
            text=[f'{x}%' for x in traditional_apps.sort_values('usage_rate')['usage_rate']],
            textposition='outside'
        ))

        fig_apps.update_layout(
            title='AI Application Usage: GenAI vs Traditional AI',
            xaxis_title='Usage Rate (% of AI-adopting firms)',
            height=600,
            showlegend=True,
            barmode='overlay' # Overlay bars for comparison
        )
        st.plotly_chart(fig_apps, use_container_width=True)
        st.success("**Key Trend:** GenAI applications (content generation, code generation, chatbots) now lead adoption rates.")

        # GenAI by Business Function (2025)
        st.markdown("### Generative AI Adoption by Business Function (2025)")
        fig_genai_func = px.bar(genai_2025.sort_values('adoption', ascending=False),
                                x='adoption', y='function', orientation='h',
                                title='Generative AI Adoption Rate by Business Function (2025)',
                                labels={'adoption': 'Adoption Rate (%)', 'function': 'Business Function'})
        st.plotly_chart(fig_genai_func, use_container_width=True)
        st.write("Marketing & Sales, along with Product Development, show the highest GenAI adoption among business functions.")

    elif selected_view == "🚧 Overcoming Challenges":
        st.header("Barriers to AI Adoption and Support Effectiveness")
        st.write("Understand the key challenges organizations face in adopting AI and evaluate the effectiveness of various support mechanisms.")

        # Barriers to AI Adoption
        st.markdown("### Top Barriers to AI Adoption")
        fig_barriers = px.bar(barriers_data.sort_values('percentage'),
                              x='percentage', y='barrier', orientation='h',
                              title='Key Barriers to AI Adoption',
                              labels={'percentage': 'Percentage of Firms Reporting Barrier (%)', 'barrier': 'Barrier'})
        st.plotly_chart(fig_barriers, use_container_width=True)
        st.info("Lack of skilled personnel and data availability/quality are identified as the most significant barriers.")

        # Support Effectiveness
        st.markdown("### Effectiveness of AI Adoption Support Initiatives")
        fig_support = px.bar(support_effectiveness.sort_values('effectiveness_score', ascending=False),
                             x='support_type', y='effectiveness_score',
                             title='Effectiveness of Support Initiatives for AI Adoption',
                             labels={'effectiveness_score': 'Effectiveness Score (1-100)', 'support_type': 'Support Type'})
        st.plotly_chart(fig_support, use_container_width=True)
        st.success("Government education investment and university partnerships are perceived as the most effective support types.")

    elif selected_view == "💰 Investment & ROI":
        st.header("AI Investment Trends and Financial Impact")
        st.write("Analyze global AI investment flows and the reported cost savings and revenue gains from AI implementation across different business functions.")

        # AI Investment Trends
        st.markdown("### Global AI Investment Trends (Billions USD)")
        fig_ai_investment = px.line(ai_investment_data, x='year',
                                     y=['total_investment', 'genai_investment', 'us_investment', 'china_investment', 'uk_investment'],
                                     markers=True,
                                     title='Global AI Investment Trends',
                                     labels={'value':'Investment (Billions USD)', 'year':'Year', 'variable':'Investment Type'},
                                     hover_data={'total_investment': ':.1f', 'genai_investment': ':.1f',
                                                 'us_investment': ':.1f', 'china_investment': ':.1f',
                                                 'uk_investment': ':.1f'})
        fig_ai_investment.update_layout(hovermode="x unified")
        st.plotly_chart(fig_ai_investment, use_container_width=True)
        st.info("Total AI investment has consistently grown, with a sharp increase in Generative AI investments recently.")

        # Financial Impact by Function
        st.markdown("### Financial Impact of AI by Business Function")
        fig_financial_impact = make_subplots(rows=1, cols=2,
                                             subplot_titles=('Companies Reporting Cost Savings (%)', 'Companies Reporting Revenue Gains (%)'))

        fig_financial_impact.add_trace(go.Bar(x=financial_impact['function'], y=financial_impact['companies_reporting_cost_savings'],
                                              name='Cost Savings', marker_color='#2ecc71'), 1, 1) # Green for savings
        fig_financial_impact.add_trace(go.Bar(x=financial_impact['function'], y=financial_impact['companies_reporting_revenue_gains'],
                                              name='Revenue Gains', marker_color='#e67e22'), 1, 2) # Orange for gains

        fig_financial_impact.update_yaxes(title_text="Percentage of Companies (%)", col=1)
        fig_financial_impact.update_yaxes(title_text="Percentage of Companies (%)", col=2)
        fig_financial_impact.update_layout(title_text='Percentage of Companies Reporting Financial Benefits from AI by Function', height=500)
        st.plotly_chart(fig_financial_impact, use_container_width=True)

        st.markdown("### Average Financial Impact for Benefiting Companies")
        fig_avg_impact = make_subplots(rows=1, cols=2,
                                       subplot_titles=('Average Cost Reduction (%)', 'Average Revenue Increase (%)'))

        fig_avg_impact.add_trace(go.Bar(x=financial_impact['function'], y=financial_impact['avg_cost_reduction'],
                                         name='Avg Cost Reduction', marker_color='#27ae60'), 1, 1) # Darker green
        fig_avg_impact.add_trace(go.Bar(x=financial_impact['function'], y=financial_impact['avg_revenue_increase'],
                                         name='Avg Revenue Increase', marker_color='#d35400'), 1, 2) # Darker orange

        fig_avg_impact.update_yaxes(title_text="Average Percentage (%)", col=1)
        fig_avg_impact.update_yaxes(title_text="Average Percentage (%)", col=2)
        fig_avg_impact.update_layout(title_text='Average Cost Reduction and Revenue Increase for Companies Reporting Benefits', height=500)
        st.plotly_chart(fig_avg_impact, use_container_width=True)

        st.success("Marketing & Sales functions show the highest revenue gains, while Service Operations lead in reported cost savings from AI.")

    elif selected_view == "🧑‍💼 Workforce & Skills":
        st.header("AI Impact on Workforce and Skill Development")
        st.write("Examine the perception of AI's impact on jobs across generations and identify critical skill gaps and training initiatives.")

        # Generational AI Perception
        st.markdown("### Generational Perception of AI's Impact on Jobs")
        fig_perception = px.bar(ai_perception, x='generation', y=['expect_job_change', 'expect_job_replacement'],
                                barmode='group',
                                title='Generational Views on AI Impact on Jobs',
                                labels={'value': 'Percentage (%)', 'generation': 'Generation', 'variable': 'Perception'})
        st.plotly_chart(fig_perception, use_container_width=True)
        st.info("Younger generations (Gen Z, Millennials) are more likely to expect their jobs to change or be replaced by AI.")

        # Skill Gap Data
        st.markdown("### AI Skill Gap Severity and Training Initiatives")
        fig_skill_gap = make_subplots(rows=1, cols=2, subplot_titles=('Skill Gap Severity', 'Training Initiatives'))

        fig_skill_gap.add_trace(go.Bar(x=skill_gap_data['skill'], y=skill_gap_data['gap_severity'],
                                       name='Gap Severity', marker_color='darkblue'), 1, 1)
        fig_skill_gap.add_trace(go.Bar(x=skill_gap_data['skill'], y=skill_gap_data['training_initiatives'],
                                       name='Training Initiatives', marker_color='darkgreen'), 1, 2)

        fig_skill_gap.update_yaxes(title_text="Score (%)")
        fig_skill_gap.update_layout(title_text='AI Skill Gaps and Training Efforts', height=500)
        st.plotly_chart(fig_skill_gap, use_container_width=True)
        st.write("AI/ML Engineering and Data Science show the highest skill gap severity, with varying levels of training initiatives to address them.")

    elif selected_view == "⚖️ Governance & Ethics":
        st.header("AI Governance and Ethics in Practice")
        st.write("Explore the adoption rates and maturity scores of different AI governance aspects within organizations.")

        # AI Governance Adoption and Maturity
        st.markdown("### AI Governance Adoption and Maturity")
        fig_governance = make_subplots(rows=1, cols=2, subplot_titles=('Adoption Rate (%)', 'Maturity Score (Out of 5)'))

        fig_governance.add_trace(go.Bar(x=ai_governance['aspect'], y=ai_governance['adoption_rate'],
                                        name='Adoption Rate', marker_color='purple'), 1, 1)
        fig_governance.add_trace(go.Bar(x=ai_governance['aspect'], y=ai_governance['maturity_score'],
                                        name='Maturity Score', marker_color='orange'), 1, 2)

        fig_governance.update_yaxes(title_text="Percentage / Score")
        fig_governance.update_layout(title_text='AI Governance: Adoption and Maturity Across Key Aspects', height=500)
        st.plotly_chart(fig_governance, use_container_width=True)
        st.info("Data Privacy and Regulatory Compliance have high adoption rates, while Bias Detection and Accountability Frameworks have lower maturity scores.")

    elif selected_view == "🌱 Environmental Impact":
        st.header("Environmental Impact of AI Training")
        st.write("This section visualizes the carbon emissions associated with training different AI models.")

        # Training Emissions
        st.markdown("### Carbon Emissions from Training AI Models (Tons of CO2e)")
        fig_emissions = px.bar(training_emissions.sort_values('carbon_tons', ascending=False),
                               x='model', y='carbon_tons',
                               title='Estimated Carbon Emissions from Training Select AI Models',
                               labels={'carbon_tons': 'Carbon Emissions (Tons of CO2e)', 'model': 'AI Model'})
        st.plotly_chart(fig_emissions, use_container_width=True)
        st.warning("Training large-scale AI models like Llama 3.1 and GPT-4 involves significant carbon emissions, highlighting the need for more energy-efficient AI.")

    elif selected_view == "📉 AI Cost Trends":
        st.header("AI Cost Trends")
        st.write("Examine the evolution of AI model costs, showcasing the significant reduction in token pricing over time.")

        # AI Cost Reduction
        st.markdown("### AI Model Cost Reduction")
        fig_cost_reduction = px.bar(ai_cost_reduction.sort_values('cost_per_million_tokens', ascending=True),
                                    x='model', y='cost_per_million_tokens',
                                    title='Cost per Million Tokens for Select AI Models',
                                    labels={'cost_per_million_tokens': 'Cost per Million Tokens (USD)', 'model': 'AI Model'},
                                    text_auto='.2s')
        st.plotly_chart(fig_cost_reduction, use_container_width=True)
        st.info("There has been a dramatic reduction in the cost per million tokens for AI models like GPT-3.5 over a short period.")

    elif selected_view == "💸 Token Economics":
        st.header("Token Economics and Optimization")
        st.write("Dive into the economics of AI tokens, including pricing, usage patterns, and optimization strategies.")

        tab1, tab2, tab3, tab4 = st.tabs(["Token Pricing", "Token Cost Reduction", "Usage Patterns", "Optimization Strategies"])

        with tab1:
            st.subheader("AI Model Token Pricing")
            st.write("The table below shows the cost per million input and output tokens, context window size, and tokens per second for various AI models.")
            st.dataframe(token_economics)

            st.write("#### Key Takeaways:")
            st.write("• **Gemini-1.5-Flash-8B** and **GPT-3.5 (Oct 2024)** offer highly competitive pricing at $0.07-0.14/M tokens.")
            st.write("• **GPT-4** remains a premium option at $15-30/M tokens.")
            st.write("• There's a **286x reduction** in GPT-3.5 pricing in just 2 years.")
            st.info("""
            **Token Pricing Models:**
            - **Pay-per-use**: Charge by tokens consumed
            - **Token bundles**: Pre-purchase token packages
            - **Rate limits**: Max tokens/minute per user
            - **Tiered pricing**: Volume discounts
            """)

        with tab2:
            st.subheader("Token Cost Reduction Over Time")
            st.write("This chart illustrates the dramatic decrease in average token pricing for both input and output tokens over time.")
            fig_token_price_evolution = px.line(token_pricing_evolution, x='date', y=['avg_price_input', 'avg_price_output'],
                                                markers=True,
                                                title='Average Token Pricing Evolution (USD per Million Tokens)',
                                                labels={'value': 'Price (USD/Million Tokens)', 'date': 'Date', 'variable': 'Token Type'})
            fig_token_price_evolution.update_layout(hovermode="x unified")
            st.plotly_chart(fig_token_price_evolution, use_container_width=True)
            st.success("The cost of AI tokens has decreased significantly from November 2022 to May 2025, making AI more accessible.")

        with tab3:
            st.subheader("Token Usage Patterns by Use Case")
            fig = px.scatter(
                token_usage_patterns,
                x='avg_input_tokens',
                y='avg_output_tokens',
                size='input_output_ratio',
                color='use_case',
                title='Token Usage Patterns: Input vs Output by Use Case',
                labels={
                    'avg_input_tokens': 'Average Input Tokens',
                    'avg_output_tokens': 'Average Output Tokens',
                    'input_output_ratio': 'Input/Output Ratio'
                },
                height=450,
                size_max=50
            )
            # Add diagonal line for equal input/output
            fig.add_shape(
                type="line",
                x0=0, y0=0, x1=5000, y1=5000, # Assuming max tokens for axis
                line=dict(color="Red", width=2, dash="dash"),
            )
            fig.add_annotation(
                x=4500, y=4700,
                text="Equal Input/Output",
                showarrow=False,
                textangle=-15
            )
            st.plotly_chart(fig, use_container_width=True)
            st.info("Document analysis and data analysis tend to have higher input token usage, while creative writing and reasoning tasks require more output tokens.")

        with tab4:
            st.subheader("Token Optimization Strategies")
            fig_optimization = px.bar(token_optimization.sort_values('cost_reduction', ascending=False),
                                      x='strategy', y='cost_reduction',
                                      color='implementation_complexity',
                                      title='Token Optimization Strategies by Cost Reduction and Complexity',
                                      labels={'cost_reduction': 'Potential Cost Reduction (%)', 'strategy': 'Strategy',
                                              'implementation_complexity': 'Implementation Complexity (1-5)'},
                                      hover_data={'time_to_implement': ':.1f'})
            st.plotly_chart(fig_optimization, use_container_width=True)
            st.success("Model selection and batch processing offer high cost reduction with varying levels of implementation complexity.")


    # Information about sources and methodology
    st.markdown("---")
    st.header("Data Sources & Methodology")
    source_tabs = st.tabs(["Key Reports", "Methodology"])

    with source_tabs[0]:
        st.subheader("Key Reports for AI Adoption Insights")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **📈 Stanford AI Index Report 2025**
            - Latest comprehensive metrics
            - Investment & adoption data
            - Productivity research
            - Environmental impact
            [View Report](https://aiindex.stanford.edu)
            """)
        with col2:
            st.markdown("""
            **📊 McKinsey Global Survey**
            - July 2024 Survey
            - 👥 1,491 participants
            - 🌍 101 nations covered
            - 🏢 All organization levels
            - 💼 Function-specific data
            [View Report](https://www.mckinsey.com)
            """)
        with col3:
            st.markdown("""
            **🏛️ OECD AI Observatory**
            - OECD/BCG/INSEAD 2025
            - 🏢 840 enterprises
            - 🌍 G7 + Brazil
            - 📋 Policy focus
            - 🎯 Success factors
            [View Report](https://oecd.ai)
            """)

        st.markdown("---")
        st.markdown("### 📚 Comprehensive Analysis Sources")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            **🎓 Federal Reserve Research**
            - Bick, Blandin, Deming
            - 📈 Productivity impact studies
            - 👥 Worker survey analysis
            - 💼 Labor market effects
            [St. Louis Fed](https://www.stlouisfed.org)
            """)
        with col2:
            st.markdown("""
            **🏫 MIT Research**
            - Daron Acemoglu
            - 🔬 Macroeconomic analysis
            - 📊 Task-level impact
            - 💡 AI automation vs augmentation
            [MIT Economics](https://economics.mit.edu)
            """)
        with col3:
            st.markdown("""
            **💰 Goldman Sachs Research**
            - Economic Growth Analysis
            - 📈 GDP impact projections
            - 🌍 Global economic effects
            - 💼 Industry transformation
            [GS Research](https://www.goldmansachs.com/intelligence)
            """)
        with col4:
            st.markdown("""
            **🔬 Academic Research**
            - Sevilla et al., Eloundou et al.
            - 💻 Compute trends analysis
            - 👥 Labor market studies
            - 🧠 LLM capabilities research
            [arXiv Papers](https://arxiv.org)
            """)

    with source_tabs[1]:
        st.write("**Research Methodology:**")
        st.write("• **Survey Methods:** Large-scale enterprise surveys with statistical weighting")
        st.write("• **Data Collection:** Q3 2024 - Q1 2025 for most recent data")
        st.write("• **Adoption Definition:** Includes any AI use (pilots, experiments, production)")
        st.write("• **Geographic Scope:** Primarily U.S. focused for detailed city/state analysis, with global outlooks for broader trends.")
        st.write("• **Data Aggregation:** Sector, firm size, and geographic data are aggregated based on relevant industry classifications and demographic information.")
        st.write("• **AI Index 2025 Integration:** Latest findings from the Stanford AI Index Report 2025 have been integrated to provide up-to-date insights, particularly for investment, cost trends, and generational perceptions.")
        st.write("• **Token Economics:** Data collected from leading AI model providers and industry analyses.")
        st.write("• **Productivity Estimates:** Synthesized from various academic and institutional research papers.")

        st.markdown("---")
        st.subheader("Data Trust & Quality Indicators")
        st.markdown("""
        Ensuring the accuracy and reliability of the data presented is paramount. This dashboard incorporates several measures to build user trust and highlight data quality:
        """)

        # Enhanced with trust indicators
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
                    <small>Code available</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with trust_cols[4]:
            st.markdown("""
            <div style='text-align: center;'>
                <h4>🔒 Data Privacy</h4>
                <div>
                    No PII collected<br>
                    <small>Aggregated data only</small>
                </div>
            </div>
            """, unsafe_allow_html=True)


# Footer with links to GitHub
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h4>🌐 Explore More & Contribute</h4>
    <p style='font-size: 16px;'>
        This dashboard is open-source and continuously evolving. Your contributions and feedback are highly valued!
    </p>
    <p style='font-size: 18px;'>
        <a href='https://github.com/Rcasanova25/AI-Adoption-Dashboard' style='text-decoration: none; color: #0366d6;'>
            <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' width='24' height='24' style='vertical-align: middle; margin-right: 8px;'>
            GitHub Repository
        </a>
    </p>
    <p style='font-size: 14px;'>
        - [Documentation](https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki)
        - [Report Bug](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=bug)
        - [Request Feature](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=enhancement)
        - [Discussions](https://github.com/Rcasanova25/AI-Adoption-Dashboard/discussions)
    </p>
</div>
""", unsafe_allow_html=True)

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
        Powered by <a href='https://streamlit.io/' style='color: #1f77b4;'>Streamlit</a>
    </p>
</div>
""", unsafe_allow_html=True)