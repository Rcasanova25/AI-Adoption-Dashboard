import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Page config must be the first Streamlit command.
st.set_page_config(
    page_title="AI Adoption Dashboard | 2018-2025 Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create all data directly in the app
@st.cache_data
def create_data():
    """Create all dashboard data"""
    
    # Historical trends data
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
        'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
    })
    
    # AI cost reduction data
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
        'cost_per_million_tokens': [20.00, 0.14, 0.07],
        'year': [2022, 2024, 2024]
    })
    
    # Token economics data
    token_economics = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B', 
                  'Claude 3 Haiku', 'Llama 3 70B', 'GPT-4', 'Claude 3.5 Sonnet'],
        'cost_per_million_input': [20.00, 0.14, 0.07, 0.25, 0.35, 15.00, 3.00],
        'cost_per_million_output': [20.00, 0.14, 0.07, 1.25, 0.40, 30.00, 15.00],
        'context_window': [4096, 16385, 1000000, 200000, 8192, 128000, 200000],
        'tokens_per_second': [50, 150, 200, 180, 120, 80, 100]
    })
    
    # Financial impact data
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],
        'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],
        'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]
    })
    
    # AI perception data
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
        'expect_job_change': [67, 65, 58, 49],
        'expect_job_replacement': [42, 40, 34, 28]
    })
    
    # Firm size data
    firm_size = pd.DataFrame({
        'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                '500-999', '1000-2499', '2500-4999', '5000+'],
        'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5]
    })
    
    # Technology stack data
    tech_stack = pd.DataFrame({
        'technology': ['AI Only', 'AI + Cloud', 'AI + Digitization', 'AI + Cloud + Digitization'],
        'percentage': [15, 23, 24, 38]
    })
    
    # AI maturity data
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
    
    # Productivity data
    productivity_data = pd.DataFrame({
        'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
        'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
    })
    
    # Geographic data
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
    
    # OECD data
    oecd_g7_adoption = pd.DataFrame({
        'country': ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Japan'],
        'adoption_rate': [45, 38, 42, 40, 35, 32, 48],
        'manufacturing': [52, 45, 48, 55, 42, 40, 58],
        'ict_sector': [68, 62, 65, 63, 58, 55, 70]
    })
    
    # Barriers data
    barriers_data = pd.DataFrame({
        'barrier': ['Lack of skilled personnel', 'Data availability/quality', 'Integration with legacy systems',
                   'Regulatory uncertainty', 'High implementation costs', 'Security concerns',
                   'Unclear ROI', 'Organizational resistance'],
        'percentage': [68, 62, 58, 55, 52, 48, 45, 40]
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
    
    return {
        'historical_data': historical_data,
        'ai_cost_reduction': ai_cost_reduction,
        'token_economics': token_economics,
        'financial_impact': financial_impact,
        'ai_perception': ai_perception,
        'firm_size': firm_size,
        'tech_stack': tech_stack,
        'ai_maturity': ai_maturity,
        'productivity_data': productivity_data,
        'geographic': geographic,
        'oecd_g7_adoption': oecd_g7_adoption,
        'barriers_data': barriers_data,
        'skill_gap_data': skill_gap_data,
        'ai_governance': ai_governance
    }

# Load data
data = create_data()

# Navigation
st.sidebar.title("🤖 AI Adoption Dashboard")
view_type = st.sidebar.selectbox(
    "Analysis View", 
    ["🚀 Strategic Brief", "AI Cost Trends", "Token Economics", "Financial Impact", 
     "Labor Impact", "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
     "Productivity Research", "Geographic Distribution", "OECD 2025 Findings", 
     "Barriers & Support", "Skill Gap Analysis", "AI Governance"]
)

# Route to appropriate view
if view_type == "🚀 Strategic Brief":
    st.title("🎯 Strategic Brief")
    st.markdown("*5-minute strategic intelligence for leadership decisions*")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Market Adoption", "78%", "+23pp vs 2023")
    with col2:
        st.metric("Cost Reduction", "280x", "Since Nov 2022")
    with col3:
        st.metric("Avg ROI", "3.2x", "Across sectors")
    with col4:
        st.metric("Time to Impact", "12-18 months", "Typical payback")
    
    st.success("✅ Dashboard is working with simplified data loading!")

elif view_type == "AI Cost Trends":
    st.write("💸 **AI Cost Revolution: 2022-2024**")
    
    # Cost overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cost Reduction", "286x", "Since Nov 2022")
    with col2:
        st.metric("Current Cost", "$0.07", "Per million tokens")
    with col3:
        st.metric("Original Cost", "$20.00", "Per million tokens")
    with col4:
        st.metric("Savings", "99.65%", "Cost reduction")
    
    # Cost evolution chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['ai_cost_reduction']['model'],
        y=data['ai_cost_reduction']['cost_per_million_tokens'],
        mode='lines+markers',
        name='Cost per Million Tokens',
        line=dict(width=4, color='#E74C3C'),
        marker=dict(size=12),
        text=[f'${x:.2f}' for x in data['ai_cost_reduction']['cost_per_million_tokens']],
        textposition='top center'
    ))
    fig.update_layout(
        title="AI Processing Cost Collapse",
        xaxis_title="Model & Timeline",
        yaxis_title="Cost per Million Tokens ($)",
        yaxis_type="log",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Download cost data
    csv = data['ai_cost_reduction'].to_csv(index=False)
    st.download_button(
        label="📥 Download Cost Data (CSV)",
        data=csv,
        file_name="ai_cost_trends.csv",
        mime="text/csv"
    )

elif view_type == "Token Economics":
    st.write("🪙 **AI Token Economics Analysis**")
    
    # Token economics overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Lowest Cost", "$0.07", "Per million tokens")
    with col2:
        st.metric("Highest Cost", "$30.00", "Per million tokens")
    with col3:
        st.metric("Cost Range", "429x", "Difference")
    with col4:
        st.metric("Avg Cost", "$8.50", "Per million tokens")
    
    # Token cost comparison
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['token_economics']['model'],
        y=data['token_economics']['cost_per_million_input'],
        name='Input Cost',
        marker_color='#3498DB',
        text=[f'${x:.2f}' for x in data['token_economics']['cost_per_million_input']],
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        x=data['token_economics']['model'],
        y=data['token_economics']['cost_per_million_output'],
        name='Output Cost',
        marker_color='#E74C3C',
        text=[f'${x:.2f}' for x in data['token_economics']['cost_per_million_output']],
        textposition='outside'
    ))
    fig.update_layout(
        title="Token Costs by Model",
        xaxis_title="Model",
        yaxis_title="Cost per Million Tokens ($)",
        barmode='group',
        height=500,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Download token data
    csv = data['token_economics'].to_csv(index=False)
    st.download_button(
        label="📥 Download Token Economics Data (CSV)",
        data=csv,
        file_name="token_economics.csv",
        mime="text/csv"
    )

elif view_type == "Financial Impact":
    st.write("💰 **AI Financial Impact by Business Function**")
    
    # Financial overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cost Savings", "49%", "Service Operations")
    with col2:
        st.metric("Revenue Gains", "71%", "Marketing & Sales")
    with col3:
        st.metric("Avg Cost Reduction", "8%", "For adopters")
    with col4:
        st.metric("Avg Revenue Increase", "4%", "For adopters")
    
    # Financial impact visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Companies Reporting Cost Savings',
        x=data['financial_impact']['function'],
        y=data['financial_impact']['companies_reporting_cost_savings'],
        marker_color='#3498DB',
        text=[f'{x}%' for x in data['financial_impact']['companies_reporting_cost_savings']],
        textposition='outside'
    ))
    fig.add_trace(go.Bar(
        name='Companies Reporting Revenue Gains',
        x=data['financial_impact']['function'],
        y=data['financial_impact']['companies_reporting_revenue_gains'],
        marker_color='#E74C3C',
        text=[f'{x}%' for x in data['financial_impact']['companies_reporting_revenue_gains']],
        textposition='outside'
    ))
    fig.update_layout(
        title="AI Financial Impact: Cost Savings vs Revenue Gains",
        xaxis_title="Business Function",
        yaxis_title="Percentage of Companies",
        barmode='group',
        height=500,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Download financial data
    csv = data['financial_impact'].to_csv(index=False)
    st.download_button(
        label="📥 Download Financial Impact Data (CSV)",
        data=csv,
        file_name="ai_financial_impact.csv",
        mime="text/csv"
    )

else:
    st.info(f"View '{view_type}' is available in the full dashboard. This simplified version focuses on core functionality.")
    st.success("✅ Simplified dashboard is working correctly!") 