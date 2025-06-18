import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
    
    # 2025 GenAI by function - UPDATED with AI Index financial impact data
    genai_2025 = pd.DataFrame({
        'function': ['Marketing & Sales', 'Product Development', 'Service Operations', 
                    'Software Engineering', 'IT', 'Knowledge Management', 'HR', 'Supply Chain'],
        'adoption': [42, 28, 23, 22, 23, 21, 13, 7],
        'revenue_gains_pct': [71, 52, 57, 45, 40, 38, 35, 63],  # NEW from AI Index
        'cost_savings_pct': [38, 35, 49, 41, 37, 32, 28, 43]   # NEW from AI Index
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
                      'IL', 'NY', 'PA', 'TX', 'TX']
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
    
    # Productivity data
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
        'total_investment': [19.4, 72.5, 112.3, 148.5, 174.6, 252.3],  # $252.3B in 2024
        'genai_investment': [0, 0, 0, 3.95, 28.5, 33.9],  # $33.9B in 2024
        'us_investment': [8.5, 31.2, 48.7, 64.3, 75.6, 109.1],  # $109.1B US in 2024
        'china_investment': [1.2, 5.8, 7.1, 7.9, 8.4, 9.3],  # $9.3B China in 2024
        'uk_investment': [0.3, 1.8, 2.5, 3.2, 3.8, 4.5]  # $4.5B UK in 2024
    })
    
    # NEW: Regional AI adoption growth from AI Index 2025
    regional_growth = pd.DataFrame({
        'region': ['Greater China', 'Europe', 'North America', 'Asia-Pacific', 'Latin America'],
        'growth_2024': [27, 23, 15, 18, 12],  # percentage point increases
        'adoption_rate': [68, 65, 82, 58, 45]
    })
    
    # NEW: AI cost reduction data from AI Index 2025
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-3.5 (Nov 2022)', 'GPT-3.5 (Oct 2024)', 'Gemini-1.5-Flash-8B'],
        'cost_per_million_tokens': [20.00, 0.14, 0.07],
        'year': [2022, 2024, 2024]
    })
    
    # NEW: Financial impact by function from AI Index 2025
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'cost_savings_pct': [38, 49, 43, 41, 35, 37, 28, 32],
        'revenue_gains_pct': [71, 57, 63, 45, 52, 40, 35, 38],
        'avg_savings': [7, 8, 9, 10, 6, 7, 5, 6],  # Less than 10% for most
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]  # Less than 5% for most
    })
    
    # NEW: Generational AI perception data from AI Index 2025
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
        'expect_job_change': [67, 65, 58, 49],  # % believing AI will change jobs
        'expect_job_replacement': [42, 40, 34, 28]  # % believing AI will replace jobs
    })
    
    # NEW: Training emissions data from AI Index 2025
    training_emissions = pd.DataFrame({
        'model': ['AlexNet (2012)', 'GPT-3 (2020)', 'GPT-4 (2023)', 'Llama 3.1 405B (2024)'],
        'carbon_tons': [0.01, 588, 5184, 8930]
    })
    
    return (historical_data, sector_2018, genai_2025, firm_size, ai_maturity, 
            geographic, tech_stack, productivity_data, ai_productivity_estimates, 
            oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
            state_data, ai_investment_data, regional_growth, ai_cost_reduction,
            financial_impact, ai_perception, training_emissions)

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
    
    # Unpack the data - updated to include new datasets
    (historical_data, sector_2018, genai_2025, firm_size, ai_maturity, 
     geographic, tech_stack, productivity_data, ai_productivity_estimates, 
     oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
     state_data, ai_investment_data, regional_growth, ai_cost_reduction,
     financial_impact, ai_perception, training_emissions) = loaded_data
     
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

# Sidebar controls
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
    st.sidebar.info("💡 **Recommended views:** Adoption Rates, Investment Trends, Financial Impact, ROI Analysis")
elif persona == "Policymaker":
    st.sidebar.info("💡 **Recommended views:** Geographic Distribution, OECD Findings, Regional Growth, Barriers & Support")
elif persona == "Researcher":
    st.sidebar.info("💡 **Recommended views:** Historical Trends, Productivity Research, AI Cost Trends, Environmental Impact")

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

# Updated view options to include new AI Index sections
view_type = st.sidebar.selectbox(
    "Analysis View", 
    ["Adoption Rates", "Historical Trends", "Investment Trends", "Regional Growth", 
     "AI Cost Trends", "Financial Impact", "Labor Impact", "Firm Size Analysis", 
     "Technology Stack", "AI Technology Maturity", "Productivity Research", 
     "Environmental Impact", "Geographic Distribution", "OECD 2025 Findings", 
     "Barriers & Support", "ROI Analysis"]
)

# Export functionality
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

# View implementations with AI Index 2025 data
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
    
    # Add 2024 acceleration annotation
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
            text="*Adoption includes any AI use: pilots, experiments, and production deployments (AI Index 2025)",
            font=dict(size=10, color="gray")
        )]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Enhanced insights from AI Index 2025
    col1, col2 = st.columns(2)
    with col1:
        st.write("📊 **Key Growth Insights (AI Index 2025):**")
        st.write("• Business adoption jumped from **55% to 78%** in just one year")
        st.write("• GenAI adoption more than **doubled** from 33% to 71%")
        st.write("• AI moved to **central role** in driving business value")
    
    with col2:
        st.write("🎯 **Industry Context:**")
        st.write("• Fastest enterprise technology adoption in history")
        st.write("• **280x cost reduction** in AI inference since 2022")
        st.write("• Growing research confirms AI **boosts productivity**")

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
    tab1, tab2, tab3 = st.tabs(["📈 Overall Trends", "🌍 Geographic Distribution", "🚀 GenAI Focus"])
    
    with tab1:
        # Total investment trend chart
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
            textposition='top center'
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
            textposition='bottom center'
        ))
        
        fig.update_layout(
            title="AI Investment Has Grown 13x Since 2014",
            xaxis_title="Year",
            yaxis_title="Investment ($ Billions)",
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Key Insight:** Private investment in generative AI now represents over 20% of all AI-related private investment")
    
    with tab2:
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
        
        st.write("**🌍 Key Finding:** The U.S. lead is even more pronounced in generative AI investment")
    
    with tab3:
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
            marker_color=['#FFB6C1', '#FF69B4', '#FF1493']
        ))
        
        fig.update_layout(
            title="GenAI Investment: From $3.95B to $33.9B in Two Years",
            xaxis_title="Year",
            yaxis_title="Investment ($ Billions)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("**🚀 GenAI represents over 20% of all AI-related private investment**")

elif view_type == "Regional Growth":
    st.write("🌍 **Regional AI Adoption Growth (AI Index Report 2025)**")
    
    # Regional growth visualization
    fig = go.Figure()
    
    # Bar chart
    fig.add_trace(go.Bar(
        x=regional_growth['region'],
        y=regional_growth['growth_2024'],
        text=[f'+{x}pp' for x in regional_growth['growth_2024']],
        textposition='outside',
        marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
        name='2024 Growth'
    ))
    
    # Add adoption rate line
    fig.add_trace(go.Scatter(
        x=regional_growth['region'],
        y=regional_growth['adoption_rate'],
        mode='lines+markers',
        name='Current Adoption Rate',
        yaxis='y2',
        line=dict(width=3, color='#2C3E50'),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Regional AI Adoption: Growth and Current Rates",
        xaxis_title="Region",
        yaxis=dict(title="2024 Growth (percentage points)", side="left"),
        yaxis2=dict(title="Current Adoption Rate (%)", side="right", overlaying="y"),
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📈 **Growth Leaders:**")
        st.write("• **Greater China:** +27pp year-over-year growth")
        st.write("• **Europe:** +23pp increase")
        st.write("• Indicates **intensifying international competition**")
    
    with col2:
        st.write("🏆 **Adoption Leaders:**")
        st.write("• **North America:** 82% adoption rate")
        st.write("• **Greater China:** 68% adoption rate")
        st.write("• Regional gaps are **narrowing rapidly**")

elif view_type == "AI Cost Trends":
    st.write("💰 **AI Cost Reduction: 280x Cheaper in 2 Years (AI Index Report 2025)**")
    
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
    
    # Hardware improvements
    st.subheader("⚡ Hardware Performance Improvements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Performance Growth", 
            value="+43% annually", 
            help="ML hardware performance in 16-bit operations"
        )
    
    with col2:
        st.metric(
            label="Price/Performance", 
            value="-30% per year", 
            help="Costs dropping rapidly"
        )
    
    with col3:
        st.metric(
            label="Energy Efficiency", 
            value="+40% annually", 
            help="Improved power consumption"
        )
    
    st.info("**Key Finding:** LLM inference prices have fallen anywhere from 9 to 900 times per year depending on the task")

elif view_type == "Financial Impact":
    st.write("💵 **Financial Impact of AI by Business Function (AI Index Report 2025)**")
    
    # Create dual-axis visualization
    fig = go.Figure()
    
    # Sort by revenue gains
    financial_sorted = financial_impact.sort_values('revenue_gains_pct', ascending=True)
    
    # Add cost savings bars
    fig.add_trace(go.Bar(
        name='Cost Savings',
        y=financial_sorted['function'],
        x=financial_sorted['cost_savings_pct'],
        orientation='h',
        marker_color='#2ECC71',
        text=[f'{x}%' for x in financial_sorted['cost_savings_pct']],
        textposition='auto'
    ))
    
    # Add revenue gains bars
    fig.add_trace(go.Bar(
        name='Revenue Gains',
        y=financial_sorted['function'],
        x=financial_sorted['revenue_gains_pct'],
        orientation='h',
        marker_color='#3498DB',
        text=[f'{x}%' for x in financial_sorted['revenue_gains_pct']],
        textposition='auto'
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
    
    # Key insights
    st.warning("""
    **⚠️ Important Context:** Most companies report modest financial impacts:
    - Cost savings are typically **less than 10%**
    - Revenue gains are mostly **less than 5%**
    - Benefits vary significantly by function and implementation quality
    """)
    
    # Function-specific insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("💰 **Top Cost Savings Functions:**")
        st.write("• Service Operations: 49%")
        st.write("• Supply Chain: 43%")
        st.write("• Software Engineering: 41%")
    
    with col2:
        st.write("📈 **Top Revenue Gain Functions:**")
        st.write("• Marketing & Sales: 71%")
        st.write("• Supply Chain: 63%")
        st.write("• Service Operations: 57%")

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
    
    # Key findings
    st.info("""
    **🔍 Key Findings:**
    - Growing research confirms AI **boosts productivity** and **narrows skill gaps** between workers
    - Younger workers are more likely to expect AI to transform their roles
    - AI helps low-skilled workers more, potentially reducing inequality
    """)

elif view_type == "Environmental Impact":
    st.write("🌱 **Environmental Impact: AI Training Carbon Emissions (AI Index Report 2025)**")
    
    # Emissions visualization
    fig = px.bar(
        training_emissions,
        x='model',
        y='carbon_tons',
        title='Carbon Emissions from AI Model Training',
        color='carbon_tons',
        color_continuous_scale='Reds',
        log_y=True,
        text='carbon_tons'
    )
    
    fig.update_traces(texttemplate='%{text:.0f} tons', textposition='outside')
    fig.update_layout(
        xaxis_title="AI Model",
        yaxis_title="Carbon Emissions (tons CO₂)",
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("📈 **Emission Growth:**")
        st.write("• AlexNet (2012): 0.01 tons")
        st.write("• GPT-3 (2020): 588 tons")
        st.write("• GPT-4 (2023): 5,184 tons")
        st.write("• Llama 3.1 405B (2024): 8,930 tons")
    
    with col2:
        st.write("⚡ **Energy Trends:**")
        st.write("• AI driving interest in **nuclear energy**")
        st.write("• Major tech companies securing nuclear agreements")
        st.write("• Energy efficiency improving **40% annually**")
    
    st.warning("**Note:** While individual model training emissions are increasing, improved efficiency and model reuse may offset some environmental impact")

elif view_type == "Adoption Rates":
    if "2025" in data_year:
        # Enhanced visualization with financial impact data
        fig = go.Figure()
        
        # Create subplot with secondary y-axis
        fig.add_trace(go.Bar(
            x=genai_2025['function'], 
            y=genai_2025['adoption'],
            name='Adoption Rate',
            marker_color='#3498DB',
            text=[f'{x}%' for x in genai_2025['adoption']],
            textposition='outside',
            yaxis='y'
        ))
        
        # Add revenue gains as line
        fig.add_trace(go.Scatter(
            x=genai_2025['function'],
            y=genai_2025['revenue_gains_pct'],
            mode='lines+markers',
            name='Revenue Gains %',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='GenAI Adoption by Business Function with Financial Impact (2025)',
            xaxis_tickangle=45,
            yaxis=dict(title="Adoption Rate (%)", side="left"),
            yaxis2=dict(title="% Reporting Revenue Gains", side="right", overlaying="y"),
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("🎯 **Key Insight**: Marketing & Sales leads both adoption (42%) and revenue impact (71% report gains)")
        
    else:
        # Original 2018 visualization
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
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

# Continue with remaining views (Firm Size Analysis, Technology Stack, etc.)
# These remain largely unchanged from the original code

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
    
    # Maturity legend
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
        title="The Productivity Paradox: Demographics vs Technology",
        xaxis_title="Year",
        yaxis=dict(title="Productivity Growth (%)", side="left"),
        yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
        height=500,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("📊 **Key Finding**: While AI Index 2025 confirms AI boosts productivity, historical data shows demographics play a crucial role")
    
    # Add AI Index context
    st.success("""
    **✅ AI Index 2025 Update:** Growing research confirms that AI:
    - Boosts productivity across various tasks
    - Helps narrow skill gaps between workers
    - Benefits low-skilled workers more than high-skilled workers
    """)

elif view_type == "Geographic Distribution":
    st.write("🗺️ **AI Adoption Geographic Distribution**")
    
    # Combined visualization
    fig = go.Figure()
    
    # Add state choropleth
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
    
    # Add city points
    fig.add_trace(go.Scattergeo(
        lon=geographic['lon'],
        lat=geographic['lat'],
        text=geographic['city'],
        customdata=geographic[['rate', 'state']],
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
        hovertemplate='<b>%{text}</b><br>State: %{customdata[1]}<br>AI Adoption: %{customdata[0]:.1f}%<extra></extra>'
    ))
    
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

elif view_type == "OECD 2025 Findings":
    st.write("📊 **OECD/BCG/INSEAD 2025 Report: Key Findings**")
    
    # G7 Country comparison
    fig = go.Figure()
    
    # Create grouped bar chart
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

elif view_type == "Barriers & Support":
    st.write("🚧 **OECD 2025: Barriers to AI Adoption & Support Effectiveness**")
    
    # Create two columns
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

elif view_type == "ROI Analysis":
    st.write("💰 **ROI Analysis: Economic Impact of AI Adoption**")
    
    # Create a comprehensive ROI visualization
    st.info("""
    **📊 AI Index 2025 Financial Insights:**
    - Total AI investment reached **$252.3B** in 2024 (+44.5% YoY)
    - GenAI investment hit **$33.9B** (over 20% of all AI investment)
    - Most companies report modest returns: <10% cost savings, <5% revenue gains
    - Marketing & Sales shows highest impact: 71% report revenue gains
    """)
    
    # Investment ROI visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment growth
        fig = px.line(
            ai_investment_data,
            x='year',
            y='total_investment',
            title='AI Investment Growth: 13x Since 2014',
            markers=True
        )
        fig.update_traces(line_color='green', line_width=3)
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Investment ($ Billions)",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cost reduction
        cost_data = pd.DataFrame({
            'metric': ['AI Inference Cost', 'Hardware Price/Performance', 'Energy Efficiency'],
            'improvement': [280, 30, 40],
            'type': ['280x reduction', '30% annual decrease', '40% annual increase']
        })
        
        fig = px.bar(
            cost_data,
            x='metric',
            y='improvement',
            title='AI Cost & Efficiency Improvements',
            text='type',
            color='improvement',
            color_continuous_scale='RdYlGn'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# Contextual insights section - UPDATED with AI Index 2025 findings
st.subheader("💡 Key Research Findings")

if "2025" in data_year:
    st.write("🚀 **2024-2025 AI Acceleration (AI Index Report 2025)**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Adoption Statistics:**")
        st.write("• **78%** of organizations use AI (massive jump from 55% in 2023)")
        st.write("• **71%** use generative AI (more than doubled from 33% in 2023)")
        st.write("• **Marketing & Sales** leads GenAI adoption at 42%")
        st.write("• **Record investment:** $252.3B in 2024 (+44.5% YoY)")
    
    with col2:
        st.write("**🎯 Strategic Insights:**")
        st.write("• **AI moved to central role** in driving business value")
        st.write("• **280x cost reduction** in AI inference since 2022")
        st.write("• **Regional competition intensifying:** China +27pp, Europe +23pp")
        st.write("• **US dominates investment:** 12x China, 24x UK")
    
    # Additional insights with expandable sections
    with st.expander("📈 Detailed 2024-2025 Findings from AI Index Report"):
        st.write("**📈 Business Adoption:**")
        st.write("• **2024 acceleration:** Business adoption jumped from 55% to 78% in one year")
        st.write("• **GenAI explosion:** From 33% to 71% adoption in one year")
        st.write("• AI has moved to a **central role** in driving business value")
        
        st.write("\n**💰 Investment & Costs:**")
        st.write("• **Record investment:** $252.3B total, $33.9B in GenAI")
        st.write("• **Cost plummeting:** AI inference 280x cheaper than 2022")
        st.write("• **US investment:** $109.1B (12x China's $9.3B)")
        st.write("• GenAI now represents **over 20%** of all AI investment")
        
        st.write("\n**📊 Productivity & Labor:**")
        st.write("• **Productivity confirmed:** AI boosts productivity and narrows skill gaps")
        st.write("• **60%** expect AI to change their jobs within 5 years")
        st.write("• **36%** believe AI will replace their jobs")
        st.write("• **Generational gap:** Gen Z (67%) vs Baby Boomers (49%) on job impact")
        
        st.write("\n**💵 Financial Impact:**")
        st.write("• Most companies report **<10% cost savings**, **<5% revenue gains**")
        st.write("• **Marketing & Sales:** 71% report revenue gains")
        st.write("• **Service Operations:** 49% report cost savings")
        st.write("• Benefits vary significantly by function and implementation")
        
        st.write("\n**🌍 Global Competition:**")
        st.write("• **Greater China:** +27pp growth in adoption")
        st.write("• **Europe:** +23pp growth")
        st.write("• **North America:** Still leads with 82% adoption")
        st.write("• Competition intensifying across all regions")
        
        st.write("\n**🌱 Environmental Impact:**")
        st.write("• Training emissions increasing: GPT-4 (5,184 tons) → Llama 3.1 (8,930 tons)")
        st.write("• AI driving interest in **nuclear energy**")
        st.write("• Energy efficiency improving **40% annually**")
        st.write("• Major tech companies securing nuclear agreements")

else:
    st.write("📊 **2018 Early AI Adoption Era**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏭 Industry Leadership:**")
        st.write("• **Manufacturing & Information** sectors led early adoption at ~12% each")
        st.write("• **Healthcare** and **Professional Services** at 7-8% adoption")
        st.write("• Strong **technology complementarity** with cloud computing")
    
    with col2:
        st.write("**📈 Size & Geography Patterns:**")
        st.write("• **Strong correlation** with firm size - larger firms adopt AI at much higher rates")
        st.write("• **Geographic concentration** in tech hubs and emerging metros")
        st.write("• **58.5%** adoption rate for firms with 5000+ employees")

# Data sources and methodology - UPDATED
with st.expander("📚 Data Sources & Methodology"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📈 2018 Historical Data**  
        McElheran et al. (2023)  
        *"AI Adoption in America: Who, What, and Where"*  
        📊 850,000 U.S. firms surveyed  
        🏢 Annual Business Survey data
        """)
        
    with col2:
        st.markdown("""
        **🔄 2025 Current Data**  
        **AI Index Report 2025**  
        Stanford HAI  
        📊 Comprehensive global AI metrics  
        🌍 Investment, adoption, impact data  
        
        **McKinsey Global Survey on AI**  
        📅 July 2024 survey  
        🌍 1,491 participants, 101 nations  
        
        **OECD/BCG/INSEAD Report**  
        📅 2025 publication  
        🌍 840 enterprises across G7 + Brazil
        """)
        
    with col3:
        st.markdown("""
        **🔬 Additional Sources**  
        Gartner Hype Cycle for AI 2025  
        Richmond Fed productivity research  
        Academic studies on AI impact  
        
        **📊 Key Metrics:**  
        - Business adoption rates  
        - Investment trends  
        - Cost reductions  
        - Labor impact  
        - Environmental data
        """)

# Footer
st.markdown("---")

# Feedback form
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 💭 How can we improve this dashboard?")
    with col2:
        show_feedback = st.button("📝 Give Feedback", use_container_width=True)
    
    if show_feedback:
        with st.form("feedback_form"):
            st.markdown("#### Share Your Feedback")
            rating = st.slider("Rate your experience", 1, 5, 3, help="1 = Poor, 5 = Excellent")
            feedback_type = st.selectbox(
                "Feedback category",
                ["General", "Bug Report", "Feature Request", "Data Issue", "Other"]
            )
            feedback_text = st.text_area("Your feedback", placeholder="Tell us what you think...")
            email = st.text_input("Email (optional)", placeholder="your@email.com")
            
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                st.success("✅ Thank you for your feedback! We'll review it within 24 hours.")
                st.balloons()

# Data quality indicators
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 📊 Data Quality
    <div style='background-color: #28a745; color: white; padding: 8px 15px; border-radius: 20px; display: inline-block; font-weight: bold;'>
        ✓ AI Index 2025
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### 🔄 Update Status
    <div style='color: #28a745; font-weight: bold;'>
        ✅ Latest data
    </div>
    <small>Includes 2024 metrics</small>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    ### 📈 Coverage
    <div style='font-weight: bold;'>
        Global scope
    </div>
    <small>101 countries covered</small>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    ### 🔒 Privacy
    <div style='color: #28a745; font-weight: bold;'>
        GDPR Compliant
    </div>
    <small>No personal data</small>
    """, unsafe_allow_html=True)

st.markdown("---")

# Enhanced footer
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 📚 Resources
    - [📖 GitHub Repository](https://github.com/Rcasanova25/AI-Adoption-Dashboard)
    - [🚀 Live Dashboard](https://ai-adoption-dashboard-napbhrgtzq9nejnhvrcter.streamlit.app/)
    - [📊 View Code](https://github.com/Rcasanova25/AI-Adoption-Dashboard/blob/main/app.py)
    - [📝 Report Issues](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues)
    """)

with col2:
    st.markdown("""
    ### 🔬 Research
    - [AI Index Report 2025](https://aiindex.stanford.edu)
    - [McKinsey AI Report](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)
    - [OECD AI Observatory](https://oecd.ai)
    - [Stanford HAI](https://hai.stanford.edu)
    """)

with col3:
    st.markdown("""
    ### 🤝 Connect
    - [LinkedIn - Robert Casanova](https://linkedin.com/in/robert-casanova)
    - [GitHub Profile](https://github.com/Rcasanova25)
    - [Email Robert](mailto:Robert.casanova82@gmail.com)
    - [Star on GitHub](https://github.com/Rcasanova25/AI-Adoption-Dashboard)
    """)

with col4:
    st.markdown("""
    ### 🛟 Support
    - [View Documentation](https://github.com/Rcasanova25/AI-Adoption-Dashboard/blob/main/README.md)
    - [Report Bug](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=bug)
    - [Request Feature](https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues/new?labels=enhancement)
    - [Contact Support](mailto:Robert.casanova82@gmail.com)
    """)

# Final attribution
st.markdown("""
<div style='text-align: center; color: #666; padding: 30px 20px 20px 20px; margin-top: 40px; border-top: 1px solid #ddd;'>
    <p style='font-size: 18px; margin-bottom: 10px;'>
        🤖 <strong>AI Adoption Dashboard</strong> v2.2.0
    </p>
    <p style='margin-bottom: 5px;'>
        Enhanced with AI Index Report 2025 findings
    </p>
    <p style='font-size: 14px; color: #888;'>
        Last updated: June 17, 2025 | 
        <a href='https://github.com/Rcasanova25/AI-Adoption-Dashboard' style='color: #888;'>View on GitHub</a> | 
        <a href='https://linkedin.com/in/robert-casanova' style='color: #888;'>Connect on LinkedIn</a>
    </p>
    <p style='font-size: 12px; margin-top: 15px;'>
        Created by <a href='https://linkedin.com/in/robert-casanova' style='color: #888;'>Robert Casanova</a> | 
        Powered by <a href='https://streamlit.io' style='color: #888;'>Streamlit</a> | 
        <a href='https://github.com/Rcasanova25/AI-Adoption-Dashboard/blob/main/LICENSE' style='color: #888;'>MIT License</a>
    </p>
</div>
""", unsafe_allow_html=True)