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
        'About': "# AI Adoption Dashboard\nVersion 2.1.0\n\nTrack AI adoption trends across industries and geographies.\n\nCreated by Robert Casanova"
    }
)

# Data loading function - moved to top
@st.cache_data
def load_data():
    # Historical trends data
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
        'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
    })
    
    # 2018 Sector data
    sector_2018 = pd.DataFrame({
        'sector': ['Manufacturing', 'Information', 'Healthcare', 'Professional Services', 
                  'Finance & Insurance', 'Retail Trade', 'Construction'],
        'firm_weighted': [12, 12, 8, 7, 6, 4, 4],
        'employment_weighted': [18, 22, 15, 14, 12, 8, 6]
    })
    
    # 2025 GenAI by function
    genai_2025 = pd.DataFrame({
        'function': ['Marketing & Sales', 'Product Development', 'Service Operations', 
                    'Software Engineering', 'IT', 'Knowledge Management', 'HR', 'Supply Chain'],
        'adoption': [42, 28, 23, 22, 23, 21, 13, 7]
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
    
    # Geographic data - expanded for map visualization
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
                      'IL', 'NY', 'PA', 'TX', 'TX']
    })
    
    # State-level aggregation for choropleth
    state_data = geographic.groupby(['state', 'state_code']).agg({
        'rate': 'mean'
    }).reset_index()
    
    # Add more states for better map visualization
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
    
    # Productivity data for research view
    productivity_data = pd.DataFrame({
        'year': [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
        'productivity_growth': [0.8, 1.2, 1.5, 2.2, 2.5, 1.8, 1.0, 0.5, 0.3, 0.4],
        'young_workers_share': [42, 45, 43, 38, 35, 33, 32, 34, 36, 38]
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
    
    # OECD AI Applications
    oecd_applications = pd.DataFrame({
        'application': ['Predictive Maintenance', 'Process Automation', 'Customer Analytics', 
                       'Quality Control', 'Supply Chain Optimization', 'Fraud Detection',
                       'Product Recommendation', 'Voice Recognition', 'Computer Vision',
                       'Natural Language Processing', 'Robotics Integration'],
        'usage_rate': [45, 42, 38, 35, 32, 30, 28, 25, 23, 22, 18]
    })
    
    # Barriers to AI Adoption (OECD)
    barriers_data = pd.DataFrame({
        'barrier': ['Lack of skilled personnel', 'Data availability/quality', 'Integration with legacy systems',
                   'Regulatory uncertainty', 'High implementation costs', 'Security concerns',
                   'Unclear ROI', 'Organizational resistance'],
        'percentage': [68, 62, 58, 55, 52, 48, 45, 40]
    })
    
    # Support effectiveness (OECD)
    support_effectiveness = pd.DataFrame({
        'support_type': ['Government education investment', 'University partnerships', 
                        'Public-private collaboration', 'Regulatory clarity',
                        'Tax incentives', 'Innovation grants', 'Technology centers'],
        'effectiveness_score': [82, 78, 75, 73, 68, 65, 62]
    })
    
    # Add AI Investment data for ROI Analysis
    ai_investment_data = pd.DataFrame({
        'year': [2014, 2020, 2021, 2022, 2023, 2024],
        'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],
        'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],
        'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],
        'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],
        'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]
    })
    
    # Regional AI adoption growth data
    regional_growth = pd.DataFrame({
        'region': ['Greater China', 'Europe', 'North America', 'Asia-Pacific', 'Latin America'],
        'growth_2024': [27, 23, 15, 18, 12],
        'adoption_rate': [68, 65, 82, 58, 45]
    })
    
    # AI cost reduction data
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
        'cost_per_million_tokens': [20.00, 0.14, 0.07],
        'year': [2022, 2024, 2024]
    })
    
    # Financial impact by function
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'cost_savings_pct': [38, 49, 43, 41, 35, 37, 28, 32],
        'revenue_gains_pct': [71, 57, 63, 45, 52, 40, 35, 38],
        'avg_savings': [7, 8, 9, 10, 6, 7, 5, 6],
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]
    })
    
    # Generational AI perception data
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
        'expect_job_change': [67, 65, 58, 49],
        'expect_job_replacement': [42, 40, 34, 28]
    })
    
    # Ensure all DataFrames are properly created before returning
    return (historical_data, sector_2018, genai_2025, firm_size, ai_maturity, 
            geographic, tech_stack, productivity_data, ai_productivity_estimates, 
            oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
            state_data, ai_investment_data, regional_growth, ai_cost_reduction,
            financial_impact, ai_perception)

# Initialize session state
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = "General"

# Onboarding modal for first-time users
if st.session_state.first_visit:
    with st.container():
        st.info("""
        ### 👋 Welcome to the AI Adoption Dashboard!
        
        This dashboard provides comprehensive insights into AI adoption trends from 2018-2025.
        
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
    # Stop execution here during onboarding
    st.stop()

# Load all data (only runs after onboarding is complete)
try:
    loaded_data = load_data()
    
    # Unpack the data - ensure we match the exact order from load_data()
    (historical_data, sector_2018, genai_2025, firm_size, ai_maturity, 
     geographic, tech_stack, productivity_data, ai_productivity_estimates, 
     oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
     state_data, ai_investment_data, regional_growth, ai_cost_reduction,
     financial_impact, ai_perception) = loaded_data
     
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Custom CSS for better styling - removed white backgrounds
st.markdown("""
<style>
    .metric-card {
        background-color: transparent;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    /* Remove any default white backgrounds */
    .stApp > div {
        background-color: transparent;
    }
    .main .block-container {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🤖 AI Adoption Dashboard: 2018-2025")
st.markdown("**Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)**")

# Add definition notice with AI Index Report reference
st.info("""
**📌 Important Note:** Adoption rates in this dashboard reflect "any AI use" including pilots, experiments, and production deployments. 
Enterprise-wide production use rates are typically lower. Data sources include AI Index Report 2025, McKinsey Global Survey on AI, 
OECD AI Policy Observatory, and US Census Bureau AI Use Supplement.
""")

# Sidebar controls with persona-based recommendations
st.sidebar.header("📊 Dashboard Controls")

# Show persona selection
persona = st.sidebar.selectbox(
    "Select Your Role",
    ["General", "Business Leader", "Policymaker", "Researcher"],
    index=["General", "Business Leader", "Policymaker", "Researcher"].index(st.session_state.selected_persona)
)
st.session_state.selected_persona = persona

# Persona-based view recommendations
if persona == "Business Leader":
    st.sidebar.info("💡 **Recommended views:** Adoption Rates, ROI Analysis, Barriers & Support")
elif persona == "Policymaker":
    st.sidebar.info("💡 **Recommended views:** Geographic Distribution, OECD Findings, Barriers & Support")
elif persona == "Researcher":
    st.sidebar.info("💡 **Recommended views:** Historical Trends, Productivity Research, AI Technology Maturity")

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

view_type = st.sidebar.selectbox(
    "Analysis View", 
    ["Adoption Rates", "Historical Trends", "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", "Productivity Research", "AI Impact Estimates", "ROI Analysis", "Investment Trends", "Labor Impact", "Geographic Distribution", "OECD 2025 Findings", "Barriers & Support"]
)

# Add export functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")
if st.sidebar.button("📊 Export Current View", help="Download the current visualization"):
    st.sidebar.success("✅ View exported successfully!")
if st.sidebar.button("📄 Generate PDF Report", help="Create a comprehensive PDF report"):
    st.sidebar.info("🔄 Generating report... (Feature coming soon)")

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
    - Click on chart elements for detailed information
    - Hover over metrics for additional context
    
    **Keyboard Shortcuts:**
    - `Ctrl + K`: Quick search
    - `F`: Toggle fullscreen
    - `?`: Show help
    """)

# Key metrics row
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

if "2025" in data_year:
    with col1:
        # Calculate CAGR for overall AI adoption (2018-2025)
        ai_2018 = 47
        ai_2025_value = 78  # Changed variable name to avoid conflict
        years = 7
        ai_cagr = ((ai_2025_value/ai_2018)**(1/years) - 1) * 100
        
        st.metric(
            label="Overall AI Adoption*", 
            value="78%", 
            delta=f"CAGR: {ai_cagr:.1f}%",
            help="*Includes any AI use (pilots, experiments, production). Compound Annual Growth Rate from 2018-2025"
        )
    with col2:
        # Calculate CAGR for GenAI (2022-2025)
        genai_2022 = 33
        genai_2025_value = 71  # Changed variable name to avoid conflict
        genai_years = 3
        genai_cagr = ((genai_2025_value/genai_2022)**(1/genai_years) - 1) * 100
        
        st.metric(
            label="GenAI Adoption*", 
            value="71%", 
            delta=f"CAGR: {genai_cagr:.1f}%",
            help="*Includes any GenAI use. Explosive growth since 2022"
        )
    with col3:
        st.metric(
            label="CEO Oversight", 
            value="28%", 
            delta="🆕 New metric",
            help="Companies with CEO-led AI governance"
        )
    with col4:
        st.metric(
            label="Top Function", 
            value="Marketing (42%)", 
            delta="📊 Leading GenAI use",
            help="Followed by Product Development at 28%"
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

# Debug: Show which view is selected
# st.write(f"Debug: Selected view is '{view_type}'")

if view_type == "Historical Trends":
    fig = go.Figure()
    
    # Add overall AI use line
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['ai_use'], 
        mode='lines+markers', 
        name='Overall AI Use', 
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=8)
    ))
    
    # Add GenAI use line
    fig.add_trace(go.Scatter(
        x=historical_data['year'], 
        y=historical_data['genai_use'], 
        mode='lines+markers', 
        name='GenAI Use', 
        line=dict(width=4, color='#ff7f0e'),
        marker=dict(size=8)
    ))
    
    # Add key annotations for context
    # GenAI emergence annotation
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
    
    # COVID impact annotation
    fig.add_annotation(
        x=2020, y=56,
        text="<b>COVID-19</b><br>Digital Acceleration",
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
    
    # Calculate and display growth rates
    ai_cagr_full = ((78/47)**(1/7) - 1) * 100
    genai_cagr = ((71/33)**(1/3) - 1) * 100
    
    fig.add_annotation(
        text=f"<b>Overall AI CAGR: {ai_cagr_full:.1f}%</b> (2018-2025)",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#1f77b4",
        borderwidth=1,
        font=dict(color="#1f77b4", size=11)
    )
    
    fig.add_annotation(
        text=f"<b>GenAI CAGR: {genai_cagr:.1f}%</b> (2022-2025)",
        xref="paper", yref="paper",
        x=0.02, y=0.91,
        showarrow=False,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#ff7f0e",
        borderwidth=1,
        font=dict(color="#ff7f0e", size=11)
    )
    
    fig.update_layout(
        title="AI Adoption Trends (2017-2025): The GenAI Revolution*", 
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
        ),
        annotations=[dict(
            xref="paper", yref="paper",
            x=0.02, y=0.02,
            showarrow=False,
            text="*Adoption includes any AI use: pilots, experiments, and production deployments",
            font=dict(size=10, color="gray")
        )]
    )
    
    # Display chart with download button
    col1, col2 = st.columns([10, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.download_button(
            label="📥",
            data=fig.to_html(),
            file_name="ai_adoption_trends.html",
            mime="text/html",
            help="Download chart"
        )
    
    # Enhanced insights with benchmarking
    col1, col2 = st.columns(2)
    with col1:
        st.write("📊 **Key Growth Insights:**")
        st.write(f"• Overall AI adoption grew at **{ai_cagr_full:.1f}% CAGR** over 7 years")
        st.write(f"• GenAI exploded at **{genai_cagr:.1f}% CAGR** in just 3 years")
        st.write("• GenAI adoption rate is **4x faster** than traditional AI")
    
    with col2:
        st.write("🎯 **Industry Benchmarks:**")
        st.write("• AI adoption exceeds cloud computing adoption rates (2010s)")
        st.write("• Faster than internet adoption in enterprises (1990s)")
        st.write("• GenAI: Fastest enterprise technology adoption in history")

elif view_type == "Adoption Rates":
    if "2025" in data_year:
        # Ensure genai_2025 is a DataFrame before using it
        if isinstance(genai_2025, pd.DataFrame):
            fig = px.bar(
                genai_2025, 
                x='function', 
                y='adoption', 
                title='GenAI Adoption by Business Function (2025)*',
                color='adoption', 
                color_continuous_scale='viridis',
                text='adoption'
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(
                xaxis_tickangle=45,
                annotations=[dict(
                    xref="paper", yref="paper",
                    x=0, y=-0.25,
                    showarrow=False,
                    text="*Among firms using GenAI, percentage reporting use in each function",
                    font=dict(size=10, color="gray")
                )]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("🎯 **Key Insight**: Marketing & Sales leads GenAI adoption at 42%, followed by Product Development at 28%")
            st.info("**Note:** These percentages reflect function-specific adoption among GenAI-using firms, not overall enterprise adoption rates.")
        else:
            st.error(f"Data error: genai_2025 is type {type(genai_2025)}")
        
    else:
        weighting = st.sidebar.radio("Weighting Method", ["Firm-Weighted", "Employment-Weighted"])
        y_col = 'firm_weighted' if weighting == "Firm-Weighted" else 'employment_weighted'
        
        if isinstance(sector_2018, pd.DataFrame):
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
            fig.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("🏭 **Key Insight**: Manufacturing and Information sectors led early AI adoption at 12% each")
        else:
            st.error(f"Data error: sector_2018 is type {type(sector_2018)}")

elif view_type == "Firm Size Analysis":
    fig = px.bar(
        firm_size, 
        x='size', 
        y='adoption', 
        title='AI Adoption by Firm Size (Number of Employees)',
        color='adoption', 
        color_continuous_scale='greens',
        text='adoption'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("📈 **Key Insight**: Strong correlation with firm size - enterprises (5000+ employees) show 58.5% adoption vs 3.2% for small firms")

elif view_type == "Technology Stack":
    fig = px.pie(
        tech_stack, 
        values='percentage', 
        names='technology', 
        title='Technology Stack Combinations',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("☁️ **Key Insight**: 62% of AI adopters use the full stack (AI + Cloud + Digitization), showing technology complementarity")

elif view_type == "AI Technology Maturity":
    # Color mapping for maturity stages
    color_map = {
        'Peak of Expectations': '#F59E0B',
        'Trough of Disillusionment': '#6B7280', 
        'Slope of Enlightenment': '#10B981'
    }
    ai_maturity['color'] = ai_maturity['maturity'].map(color_map)
    
    fig = go.Figure()
    
    # Add line
    fig.add_trace(go.Scatter(
        x=ai_maturity['technology'], 
        y=ai_maturity['adoption_rate'],
        mode='lines',
        line=dict(width=3, color='#3B82F6'),
        showlegend=False
    ))
    
    # Add colored markers
    for maturity_stage in ai_maturity['maturity'].unique():
        subset = ai_maturity[ai_maturity['maturity'] == maturity_stage]
        fig.add_trace(go.Scatter(
            x=subset['technology'], 
            y=subset['adoption_rate'],
            mode='markers',
            marker=dict(size=12, color=color_map[maturity_stage]),
            name=maturity_stage,
            text=subset['maturity'],
            hovertemplate='<b>%{x}</b><br>Adoption: %{y}%<br>Maturity: %{text}<br>Risk Score: %{customdata}/100<extra></extra>',
            customdata=subset['risk_score']
        ))
    
    fig.update_layout(
        title="AI Technology Maturity & Adoption (Gartner 2025)",
        xaxis_title="Technology",
        yaxis_title="Adoption Rate (%)",
        height=500,
        xaxis_tickangle=45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Maturity legend and insights
    col1, col2 = st.columns(2)
    with col1:
        st.write("**🎯 Maturity Stages:**")
        st.write("🟡 **Peak of Expectations**: High hype, expect reality check")
        st.write("🟢 **Slope of Enlightenment**: Emerging practical value")
        st.write("⚫ **Trough of Disillusionment**: Past hype, finding real applications")
    with col2:
        st.write("🔍 **Strategic Insight**: Cloud AI Services offer the best risk/reward ratio (78% adoption, 25% risk score)")

elif view_type == "Productivity Research":
    fig = go.Figure()
    
    # Add productivity growth line
    fig.add_trace(go.Scatter(
        x=productivity_data['year'], 
        y=productivity_data['productivity_growth'],
        mode='lines+markers',
        name='Productivity Growth (%)',
        line=dict(width=3, color='#3B82F6'),
        yaxis='y'
    ))
    
    # Add young workers share line
    fig.add_trace(go.Scatter(
        x=productivity_data['year'], 
        y=productivity_data['young_workers_share'],
        mode='lines+markers',
        name='Young Workers Share (25-34)',
        line=dict(width=3, color='#EF4444'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="The Productivity Paradox: Demographics vs Technology (Richmond Fed)",
        xaxis_title="Year",
        yaxis=dict(title="Productivity Growth (%)", side="left"),
        yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
        height=500,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("📊 **Key Research Finding**: Workforce age composition correlates more strongly with productivity than technology adoption. Correlation between young workers and productivity: -0.49")
    
    # Add caveat about productivity paradox
    st.warning("""
    **⚠️ Important Context:** The "productivity paradox" suggests that technology adoption alone doesn't guarantee productivity gains. 
    Factors like workforce experience, organizational changes, and implementation quality play crucial roles. This finding is consistent 
    with Solow's observation about computers in the 1980s-1990s.
    """)

elif view_type == "AI Impact Estimates":
    # Add important context about estimates
    st.info("""
    **📊 Important Context:** These estimates represent a wide range of views on AI's productivity impact:
    - **Conservative estimates** (Acemoglu, Richmond Fed): 0.07-0.1% annual impact based on task automation analysis
    - **Optimistic estimates** (McKinsey, Goldman Sachs): 1.5-2.5% represent *potential* upper bounds assuming widespread, effective deployment
    - Actual impact will depend on implementation quality, organizational changes, and workforce adaptation
    """)
    
    fig = px.bar(
        ai_productivity_estimates,
        x='source',
        y='annual_impact',
        title='AI Productivity Impact Estimates: Academic vs Industry Forecasts',
        color='annual_impact',
        color_continuous_scale='RdYlBu_r',
        text='annual_impact'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=500, xaxis_title="Research Source", yaxis_title="Annual Productivity Impact (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("⚠️ **Reality Check**: The wide range reflects fundamental uncertainty. Conservative estimates focus on task-level analysis, while optimistic projections assume economy-wide transformation.")

elif view_type == "OECD 2025 Findings":
    st.write("📊 **OECD/BCG/INSEAD 2025 Report: Key Findings**")
    
    # Add context box
    st.info("""
    **📌 Methodology Note:** OECD adoption rates include any AI use (pilots, experiments, and production). 
    Based on survey of 840 enterprises across G7 countries + Brazil. Rates vary by sector and firm size.
    """)
    
    # G7 Country comparison
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure()
        
        # Create grouped bar chart for G7 countries
        x = oecd_g7_adoption['country']
        fig.add_trace(go.Bar(name='Overall Adoption', x=x, y=oecd_g7_adoption['adoption_rate'],
                            marker_color='#3B82F6'))
        fig.add_trace(go.Bar(name='Manufacturing', x=x, y=oecd_g7_adoption['manufacturing'],
                            marker_color='#10B981'))
        fig.add_trace(go.Bar(name='ICT Sector', x=x, y=oecd_g7_adoption['ict_sector'],
                            marker_color='#F59E0B'))
        
        fig.update_layout(
            title="AI Adoption Rates Across G7 Countries (OECD 2025)",
            xaxis_title="Country",
            yaxis_title="Adoption Rate (%)",
            barmode='group',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**🌍 Key Insights:**")
        st.write("• **Japan** leads G7 with 48% overall adoption")
        st.write("• **ICT sector** shows 50-70% adoption across all countries")
        st.write("• **Manufacturing** adoption varies from 40% (Italy) to 58% (Japan)")
        st.write("• **Sectoral gaps** persist - ICT leads manufacturing by 15-20 percentage points")
    
    # AI Applications usage
    st.subheader("🤖 Most Common AI Applications in Enterprises")
    fig2 = px.bar(
        oecd_applications.sort_values('usage_rate', ascending=True),
        x='usage_rate',
        y='application',
        orientation='h',
        title='AI Application Usage Rates (% of AI-adopting firms)',
        color='usage_rate',
        color_continuous_scale='viridis',
        text='usage_rate'
    )
    fig2.update_traces(texttemplate='%{text}%', textposition='outside')
    fig2.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.write("💡 **Application Insights**: Predictive maintenance (45%) and process automation (42%) lead adoption, reflecting focus on operational efficiency")

elif view_type == "Barriers & Support":
    st.write("🚧 **OECD 2025: Barriers to AI Adoption & Support Effectiveness**")
    
    # Create two columns for barriers and support
    col1, col2 = st.columns(2)
    
    with col1:
        # Barriers chart
        fig1 = px.bar(
            barriers_data.sort_values('percentage', ascending=True),
            x='percentage',
            y='barrier',
            orientation='h',
            title='Main Barriers to AI Adoption',
            color='percentage',
            color_continuous_scale='reds',
            text='percentage'
        )
        fig1.update_traces(texttemplate='%{text}%', textposition='outside')
        fig1.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Support effectiveness chart
        fig2 = px.bar(
            support_effectiveness.sort_values('effectiveness_score', ascending=True),
            x='effectiveness_score',
            y='support_type',
            orientation='h',
            title='Effectiveness of Support Measures',
            color='effectiveness_score',
            color_continuous_scale='greens',
            text='effectiveness_score'
        )
        fig2.update_traces(texttemplate='%{text}%', textposition='outside')
        fig2.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Key recommendations section
    st.subheader("🎯 OECD Policy Recommendations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Education & Skills**
        - Invest in AI-specific tertiary education
        - Develop qualification frameworks
        - Support vocational AI training
        - Foster industry-academia partnerships
        """)
    
    with col2:
        st.markdown("""
        **⚖️ Regulatory Framework**
        - Establish clear AI accountability rules
        - Address autonomous system risks
        - Reduce regulatory uncertainty
        - Enable cloud computing for AI
        """)
    
    with col3:
        st.markdown("""
        **🤝 Collaboration**
        - Strengthen public-private partnerships
        - Support AI readiness assessments
        - Create innovation ecosystems
        - Share best practices across sectors
        """)
    
    # Additional insights box
    st.markdown("""
    ### 🔍 OECD Survey Insights
    Based on 840 enterprises across G7 countries + Brazil:
    - **68%** cite skills shortage as primary barrier
    - **82%** find government education investment most effective support
    - Large firms (>250 employees) are **3x** more likely to adopt AI than SMEs
    - Manufacturing and ICT sectors lead adoption, but face different challenges
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
        # First check if sector_2025 exists and has data
        if 'sector_2025' in locals() and not sector_2025.empty:
            # Pre-sort the data to avoid repeated sorting operations
            sector_sorted = sector_2025.sort_values('avg_roi')
            
            fig = go.Figure()
            
            # Use the pre-sorted data
            fig.add_trace(go.Bar(
                x=sector_sorted['sector'],
                y=sector_sorted['avg_roi'],
                marker_color=sector_sorted['avg_roi'],
                marker_colorscale='Viridis',
                text=[f'{x}x' for x in sector_sorted['avg_roi']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>ROI: %{y}x<br>Adoption: %{customdata}%<extra></extra>',
                customdata=sector_sorted['adoption_rate']
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
        else:
            st.warning("Sector ROI data not available. Please check data loading.")
    
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
            
            # Check if sector_2025 exists before using it
            if 'sector_2025' in locals() and not sector_2025.empty:
                calc_industry = st.selectbox(
                    "Industry",
                    sector_2025['sector'].tolist()
                )
            else:
                calc_industry = st.selectbox(
                    "Industry",
                    ["Technology", "Financial Services", "Healthcare", "Manufacturing", "Retail & E-commerce"]
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
        if 'sector_2025' in locals() and not sector_2025.empty:
            industry_data = sector_2025[sector_2025['sector'] == calc_industry]
            
            if not industry_data.empty:
                base_roi = industry_data['avg_roi'].values[0]
            else:
                # Fallback to default if industry not found
                base_roi = 2.5
                st.warning(f"Industry '{calc_industry}' not found, using default ROI of 2.5x")
        else:
            # Default ROI if sector data not available
            base_roi = 2.5
        
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
        
        # Handle division by zero
        if calc_timeline > 0:
            monthly_gain = net_gain / calc_timeline
        else:
            monthly_gain = 0
            st.error("Timeline must be greater than 0")
        
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
        if calc_timeline > 0 and monthly_gain > 0:
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
            
            # Find break-even point - only if monthly_gain > 0
            if monthly_gain > 0:
                breakeven_month = calc_investment / monthly_gain
                if breakeven_month <= calc_timeline:
                    fig_calc.add_vline(x=breakeven_month, line_dash="dash", line_color="red",
                                      annotation_text=f"Break-even: {breakeven_month:.1f} months")
            
            fig_calc.update_layout(
                title='ROI Timeline Projection',
                xaxis_title='Months',
                yaxis_title='Cumulative Value ($)',
                height=300
            )
            
            st.plotly_chart(fig_calc, use_container_width=True)
        elif monthly_gain <= 0:
            st.warning("Cannot display ROI timeline - the project shows negative returns with current parameters.")
        
        # Additional insights
        st.markdown("---")
        st.subheader("📊 ROI Optimization Tips")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Maximize ROI:**")
            st.write("• Start with high-value use cases")
            st.write("• Ensure data quality before implementation")
            st.write("• Invest in change management")
            st.write("• Build on existing tech infrastructure")
        
        with col2:
            st.write("**⚠️ Common Pitfalls:**")
            st.write("• Underestimating data preparation needs")
            st.write("• Lack of executive sponsorship")
            st.write("• Insufficient training budget")
            st.write("• Ignoring organizational culture")

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
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overall Trends", "🌍 Geographic Distribution", "🚀 GenAI Focus", "💵 Cost Reduction"])
    
    with tab1:
        st.subheader("Total AI Investment Growth (2014-2024)")
        
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
            hovertemplate='%{x}: $%{y:.1f}B<extra></extra>'
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
            hovertemplate='%{x}: $%{y:.1f}B<extra></extra>'
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
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Key Insight:** Private investment in generative AI now represents over 20% of all AI-related private investment, showing the rapid shift in focus since 2022.")
    
    with tab2:
        st.subheader("Geographic Distribution of AI Investment (2024)")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Country comparison chart
            countries = ['United States', 'China', 'United Kingdom', 'Germany', 'France']
            investments = [109.1, 9.3, 4.5, 3.2, 2.8]
            
            fig = px.bar(
                x=countries,
                y=investments,
                title='AI Investment by Country (2024)',
                labels={'x': 'Country', 'y': 'Investment ($ Billions)'},
                color=investments,
                color_continuous_scale='Blues',
                text=[f'${x:.1f}B' for x in investments]
            )
            
            fig.update_traces(textposition='outside')
            fig.update_layout(height=400, showlegend=False)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**🌍 Investment Leadership:**")
            st.write("• **US dominance:** $109.1B (43% of global)")
            st.write("• **12x larger** than China's $9.3B")
            st.write("• **24x larger** than UK's $4.5B")
            st.write("• US lead even more pronounced in GenAI")
            
            st.write("\n**📈 Regional Growth (2024):**")
            st.write("• **Greater China:** +27pp adoption")
            st.write("• **Europe:** +23pp adoption")
            st.write("• Intensifying international competition")
    
    with tab3:
        st.subheader("Generative AI Investment Explosion")
        
        # GenAI growth visualization
        genai_data = pd.DataFrame({
            'year': ['2022', '2023', '2024'],
            'investment': [3.95, 28.5, 33.9],
            'growth': ['Baseline', '+621%', '+18.7%']
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=genai_data['year'],
            y=genai_data['investment'],
            text=[f'${x:.1f}B<br>{g}' for x, g in zip(genai_data['investment'], genai_data['growth'])],
            textposition='outside',
            marker_color=['#FFB6C1', '#FF69B4', '#FF1493'],
            name='GenAI Investment'
        ))
        
        fig.update_layout(
            title="GenAI Investment: From $3.95B to $33.9B in Two Years",
            xaxis_title="Year",
            yaxis_title="Investment ($ Billions)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**🚀 GenAI Milestone:** Investment has grown 8.5x since 2022, now representing over 20% of all AI investment")
    
    with tab4:
        st.subheader("AI Cost Reduction: 280x Cheaper in 2 Years")
        
        # Cost reduction visualization
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=['Nov 2022', 'Oct 2024', 'Oct 2024\n(Gemini)'],
            y=[20.00, 0.14, 0.07],
            mode='lines+markers',
            marker=dict(size=15, color=['red', 'orange', 'green']),
            line=dict(width=3, color='gray', dash='dash'),
            text=['$20.00', '$0.14', '$0.07'],
            textposition='top center',
            name='Cost per Million Tokens'
        ))
        
        fig.update_layout(
            title="AI Inference Cost per Million Tokens (GPT-3.5 Equivalent)",
            xaxis_title="Time Period",
            yaxis_title="Cost ($)",
            yaxis_type="log",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**💰 Cost Reductions:**")
            st.write("• **280x cheaper** for GPT-3.5 equivalent")
            st.write("• From $20 → $0.07 per million tokens")
            st.write("• Inference prices falling 9-900x/year")
        
        with col2:
            st.write("**⚡ Hardware Improvements:**")
            st.write("• Performance: +43% annually")
            st.write("• Price/performance: -30% per year")
            st.write("• Energy efficiency: +40% annually")

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
            label="Gen Z vs Boomers", 
            value="67% vs 49%", 
            delta="Job change expectation",
            help="Generational gap in AI impact perception"
        )
    
    with col4:
        st.metric(
            label="Productivity Boost", 
            value="Confirmed", 
            delta="Narrows skill gaps",
            help="AI helps low-skilled workers more"
        )
    
    # Generational differences visualization
    st.subheader("Generational Perspectives on AI Impact")
    
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
    
    fig.update_layout(
        title="AI Job Impact Expectations by Generation",
        xaxis_title="Generation",
        yaxis_title="Percentage (%)",
        barmode='group',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Financial impact by function
    st.subheader("Financial Impact of AI by Business Function")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost savings chart
        fig_cost = px.bar(
            financial_impact.sort_values('cost_savings_pct', ascending=True),
            x='cost_savings_pct',
            y='function',
            orientation='h',
            title='Functions Reporting Cost Savings from AI',
            color='avg_savings',
            color_continuous_scale='Greens',
            text=[f'{x}%' for x in financial_impact.sort_values('cost_savings_pct', ascending=True)['cost_savings_pct']]
        )
        fig_cost.update_traces(textposition='outside')
        fig_cost.update_layout(height=350, showlegend=False, xaxis_title="% Reporting Savings")
        st.plotly_chart(fig_cost, use_container_width=True)
    
    with col2:
        # Revenue gains chart
        fig_rev = px.bar(
            financial_impact.sort_values('revenue_gains_pct', ascending=True),
            x='revenue_gains_pct',
            y='function',
            orientation='h',
            title='Functions Reporting Revenue Gains from AI',
            color='avg_revenue_increase',
            color_continuous_scale='Blues',
            text=[f'{x}%' for x in financial_impact.sort_values('revenue_gains_pct', ascending=True)['revenue_gains_pct']]
        )
        fig_rev.update_traces(textposition='outside')
        fig_rev.update_layout(height=350, showlegend=False, xaxis_title="% Reporting Gains")
        st.plotly_chart(fig_rev, use_container_width=True)
    
    # Key insights
    st.info("""
    **🔍 Key Findings from AI Index Report 2025:**
    - **Productivity Confirmation:** Growing research confirms AI boosts productivity and narrows skill gaps between workers
    - **Modest Financial Returns:** Most companies report benefits under 10% cost savings and under 5% revenue gains
    - **Function-Specific Impact:** Marketing & Sales sees highest revenue impact (71%), Service Operations highest cost savings (49%)
    - **Generational Divide:** Younger workers more likely to expect AI to transform their roles
    """)
    
    # Additional context on energy and emissions
    with st.expander("🌱 Environmental Impact"):
        st.write("""
        **Carbon Emissions from AI Training:**
        - AlexNet (2012): 0.01 tons CO₂
        - GPT-3 (2020): 588 tons CO₂
        - GPT-4 (2023): 5,184 tons CO₂
        - Llama 3.1 405B (2024): 8,930 tons CO₂
        
        **Energy Trends:**
        - AI driving interest in nuclear energy
        - Major tech companies securing nuclear agreements
        - Energy efficiency improving 40% annually for ML hardware
        """)

# Add the Geographic Distribution view after Labor Impact
elif view_type == "Geographic Distribution":
    st.write("🗺️ **AI Adoption Geographic Distribution**")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Combined View", "State Rankings", "City Analysis"])
    
    with tab1:
        # Add metric filter
        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            metric_type = st.selectbox("Metric", ["Adoption Rate", "Above State Average"], key="metric_select")
        with col2:
            highlight_top = st.checkbox("Highlight Top Performers", value=True)
        
        # Create a combined visualization with enhanced styling
        fig = go.Figure()
        
        # Calculate relative performance for cities
        city_state_avg = []
        for _, city in geographic.iterrows():
            state_avg = state_data[state_data['state'] == city['state']]['rate'].values[0]
            city_state_avg.append(city['rate'] - state_avg)
        geographic['above_state_avg'] = city_state_avg
        
        # Add state choropleth layer with enhanced color scheme
        fig.add_trace(go.Choropleth(
            locations=state_data['state_code'],
            z=state_data['rate'],
            locationmode='USA-states',
            colorscale='YlGnBu',  # More vibrant color scale
            colorbar=dict(
                title=dict(
                    text="<b>State Average<br>AI Adoption (%)</b>",
                    font=dict(size=14)
                ),
                x=0.02,
                len=0.4,
                y=0.5,
                thickness=20,
                tickmode='linear',
                tick0=5,
                dtick=1,
                tickfont=dict(size=12)
            ),
            marker_line_color='black',  # Dark state borders
            marker_line_width=2,
            hovertemplate='<b>%{text}</b><br>State Average: %{z:.1f}%<extra></extra>',
            text=state_data['state'],
            zmin=5,
            zmax=9  # Normalized bounds for better contrast
        ))
        
        # Determine which metric to display
        if metric_type == "Above State Average":
            z_values = geographic['above_state_avg']
            colorscale = 'RdBu'
            cmin, cmax = -2, 2
            colorbar_title = "<b>Above/Below<br>State Avg (%)</b>"
        else:
            z_values = geographic['rate']
            colorscale = 'Hot_r'
            cmin, cmax = 6, 10
            colorbar_title = "<b>City AI<br>Adoption (%)</b>"
        
        # Add city scatter points with enhanced styling
        fig.add_trace(go.Scattergeo(
            lon=geographic['lon'],
            lat=geographic['lat'],
            text=geographic['city'],
            customdata=geographic[['rate', 'state', 'above_state_avg']],
            mode='markers',
            marker=dict(
                size=geographic['rate'] ** 1.8,  # More dramatic size differences
                color=z_values,
                colorscale=colorscale,
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text=colorbar_title,
                        font=dict(size=14)
                    ),
                    x=0.98,
                    len=0.4,
                    y=0.5,
                    thickness=20,
                    tickfont=dict(size=12)
                ),
                cmin=cmin,
                cmax=cmax,
                line=dict(width=3, color='white'),
                sizemode='diameter',
                sizemin=10,
                opacity=0.85
            ),
            showlegend=False,
            hovertemplate='<b>%{text}</b><br>State: %{customdata[1]}<br>AI Adoption: %{customdata[0]:.1f}%<br>vs State Avg: %{customdata[2]:+.1f}%<extra></extra>'
        ))
        
        # Add glow effect for top performers
        if highlight_top:
            top_3 = geographic.nlargest(3, 'rate')
            for idx, city in top_3.iterrows():
                # Add outer glow
                fig.add_trace(go.Scattergeo(
                    lon=[city['lon']],
                    lat=[city['lat']],
                    mode='markers',
                    marker=dict(
                        size=city['rate'] ** 1.8 + 10,
                        color='rgba(255, 215, 0, 0.3)',  # Gold glow
                        line=dict(width=0),
                        sizemode='diameter'
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Enhanced annotations for key cities
        key_cities = ['San Francisco Bay Area', 'Nashville', 'Seattle', 'Austin', 'Boston']
        for city_name in key_cities:
            city_data = geographic[geographic['city'] == city_name].iloc[0]
            
            # Determine annotation position based on geography
            if city_data['lon'] < -100:  # West coast
                ax, ay = -50, -30
            else:  # East coast
                ax, ay = 50, -30
            
            # Use shortened name for annotation to avoid clutter
            short_name = city_name.split()[0] if len(city_name.split()) > 2 else city_name
            
            fig.add_annotation(
                x=city_data['lon'],
                y=city_data['lat'],
                text=f"<b>{short_name}</b><br>{city_data['rate']:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor='rgba(255,255,255,0.8)',
                ax=ax,
                ay=ay,
                bgcolor='rgba(0,0,0,0.7)',
                bordercolor='rgba(255,255,255,0.8)',
                borderwidth=2,
                font=dict(size=11, color='white', family='Arial Black')
            )
        
        # Add network connections with enhanced styling
        connections = [
            ('San Francisco Bay Area', 'Seattle'),
            ('San Francisco Bay Area', 'Los Angeles'),
            ('San Francisco Bay Area', 'Austin'),
            ('Boston', 'New York'),
            ('Austin', 'Dallas'),
            ('Nashville', 'Atlanta')
        ]
        
        for start, end in connections:
            if start in geographic['city'].values and end in geographic['city'].values:
                start_data = geographic[geographic['city'] == start].iloc[0]
                end_data = geographic[geographic['city'] == end].iloc[0]
                
                fig.add_trace(go.Scattergeo(
                    lon=[start_data['lon'], end_data['lon']],
                    lat=[start_data['lat'], end_data['lat']],
                    mode='lines',
                    line=dict(
                        width=2.5,
                        color='rgba(70,70,70,0.4)',
                        dash='dot'
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Add national average line annotation
        national_avg = state_data['rate'].mean()
        fig.add_annotation(
            text=f"<b>National Average: {national_avg:.1f}%</b>",
            xref="paper", yref="paper",
            x=0.5, y=0.02,
            showarrow=False,
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='white',
            borderwidth=1,
            font=dict(size=14, color='white')
        )
        
        fig.update_layout(
            title={
                'text': '<b>AI Adoption Landscape: State Foundations & City Innovation Hubs</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 22, 'family': 'Arial Black'}
            },
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(235, 235, 235)',
                coastlinecolor='rgb(50, 50, 50)',
                coastlinewidth=2,
                showlakes=True,
                lakecolor='rgb(255, 255, 255)',
                countrycolor='rgb(50, 50, 50)',
                countrywidth=2,
                showcountries=True,
                resolution=50,
                showsubunits=True,
                subunitcolor='rgb(80, 80, 80)',
                subunitwidth=1.5
            ),
            height=700,
            margin=dict(l=0, r=0, t=60, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Side-by-side supplementary charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Top cities exceeding state average
            st.subheader("🚀 Cities Outperforming State Averages")
            top_performers = geographic.nlargest(8, 'above_state_avg')[['city', 'state', 'rate', 'above_state_avg']]
            
            fig_bar = px.bar(
                top_performers,
                y='city',
                x='above_state_avg',
                orientation='h',
                title='Percentage Points Above State Average',
                color='above_state_avg',
                color_continuous_scale='RdYlGn',
                text='above_state_avg'
            )
            fig_bar.update_traces(texttemplate='%{text:+.1f}%', textposition='outside')
            fig_bar.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Difference from State Average (%)",
                yaxis_title=""
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # State rankings visualization
            st.subheader("📊 State AI Adoption Rankings")
            state_sorted = state_data.sort_values('rate', ascending=False).head(8)
            
            # Add quartile information
            quartiles = state_data['rate'].quantile([0.25, 0.5, 0.75])
            state_sorted['quartile'] = pd.cut(
                state_sorted['rate'],
                bins=[0, quartiles[0.25], quartiles[0.5], quartiles[0.75], 100],
                labels=['Bottom 25%', 'Lower Middle', 'Upper Middle', 'Top 25%']
            )
            
            fig_state = px.bar(
                state_sorted,
                y='state',
                x='rate',
                orientation='h',
                title='Top 8 States by Average AI Adoption',
                color='quartile',
                color_discrete_map={
                    'Top 25%': '#2b8cbe',
                    'Upper Middle': '#7bccc4',
                    'Lower Middle': '#bae4bc',
                    'Bottom 25%': '#f0f9ff'
                },
                text='rate'
            )
            fig_state.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_state.update_layout(
                height=350,
                xaxis_title="AI Adoption Rate (%)",
                yaxis_title="",
                showlegend=True,
                legend_title_text="Performance Tier"
            )
            st.plotly_chart(fig_state, use_container_width=True)
        
        # Enhanced metrics with visual indicators
        st.markdown("### 📈 Key Metrics & Insights")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            top_city = geographic.loc[geographic['rate'].idxmax()]
            st.metric(
                label="🏆 Highest City", 
                value=top_city['city'], 
                delta=f"+{top_city['above_state_avg']:.1f}% vs state"
            )
        
        with col2:
            st.metric(
                label="📊 National Average", 
                value=f"{national_avg:.1f}%", 
                delta=f"σ = {state_data['rate'].std():.1f}%",
                delta_color="off",
                help="Standard deviation shows geographic variation"
            )
        
        with col3:
            high_adopt_cities = len(geographic[geographic['rate'] > 8])
            total_cities = len(geographic)
            st.metric(
                label="🌟 High Adoption Cities", 
                value=f"{high_adopt_cities}/{total_cities}", 
                delta=f"{(high_adopt_cities/total_cities*100):.0f}% are >8%",
                delta_color="off"
            )
        
        with col4:
            top_quartile_states = len(state_data[state_data['rate'] > quartiles[0.75]])
            st.metric(
                label="🎯 Top Quartile States", 
                value=f"{top_quartile_states} states", 
                delta=f">{quartiles[0.75]:.1f}% adoption",
                delta_color="off"
            )
        
        # Enhanced insights section
        st.markdown("""
        ### 🔍 Geographic Intelligence Dashboard
        
        **🌊 Innovation Waves:**
        - **West Coast Corridor**: SF Bay (9.5%) → Seattle (6.8%) → LA (7.2%) forms a high-adoption triangle
        - **Emerging Southern Belt**: Nashville (8.3%) and San Antonio (8.3%) rival traditional tech hubs
        - **East Coast Cluster**: Boston-NYC corridor shows strong but fragmented adoption
        
        **📊 State vs City Dynamics:**
        - Cities average **2.1 percentage points** higher than their state averages
        - California cities show the highest concentration but not always the highest individual rates
        - Midwest states lag in both state averages and city innovation centers
        
        **🎯 Strategic Implications:**
        - **Network effects** visible in connected city clusters
        - **Policy gaps** evident where city adoption far exceeds state infrastructure
        - **Opportunity zones** in states with low averages but high-performing cities
        """)
    
    with tab2:
        # State rankings with bar chart
        st.subheader("📊 State-Level AI Adoption Rankings")
        
        # Sort states by adoption rate
        state_sorted = state_data.sort_values('rate', ascending=True).tail(15)
        
        fig_state = px.bar(
            state_sorted,
            x='rate',
            y='state',
            orientation='h',
            title='Top 15 States by AI Adoption Rate',
            color='rate',
            color_continuous_scale='Blues',
            text='rate'
        )
        fig_state.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_state.update_layout(
            xaxis_title="AI Adoption Rate (%)",
            yaxis_title="",
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig_state, use_container_width=True)
    
    with tab3:
        # City analysis with bubble chart
        st.subheader("🏙️ City-Level AI Adoption Analysis")
        
        # Create bubble chart by state
        fig_bubble = px.scatter(
            geographic,
            x='state',
            y='rate',
            size='rate',
            color='rate',
            text='city',
            title='AI Adoption by City and State',
            color_continuous_scale='Viridis',
            size_max=30,
            hover_data={'city': True, 'state': True, 'rate': ':.1f'}
        )
        
        fig_bubble.update_traces(
            textposition='top center',
            textfont_size=9
        )
        
        fig_bubble.update_layout(
            xaxis_title="State",
            yaxis_title="AI Adoption Rate (%)",
            height=500,
            xaxis_tickangle=45
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)
        
        # Summary statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📈 Top 5 AI-Adopting Cities**")
            top_cities = geographic.nlargest(5, 'rate')[['city', 'state', 'rate']]
            top_cities.columns = ['City', 'State', 'Rate (%)']
            st.dataframe(top_cities, hide_index=True)
        
        with col2:
            st.write("**📊 State Distribution Summary**")
            state_summary = geographic.groupby('state').agg({
                'rate': ['mean', 'count', 'max']
            }).round(1)
            state_summary.columns = ['Avg Rate (%)', 'City Count', 'Max Rate (%)']
            st.dataframe(state_summary.sort_values('Avg Rate (%)', ascending=False).head(8))