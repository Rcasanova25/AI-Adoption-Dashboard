import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots

# Page config must be the first Streamlit command.
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

# Add feature flags for safe deployment
if 'feature_flags' not in st.session_state:
    st.session_state.feature_flags = {
        'executive_mode': True,
        'visual_redesign': True,
        'strategic_callouts': True,
        'competitive_homepage': False  # Start disabled, enable after testing
    }

# These view lists are created based on the options available in the script.
all_views = [
    "Adoption Rates", "Historical Trends", "Industry Analysis", "Investment Trends", 
    "Regional Growth", "AI Cost Trends", "Token Economics", "Financial Impact", 
    "Labor Impact", "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
    "Productivity Research", "Environmental Impact", "Geographic Distribution", 
    "OECD 2025 Findings", "Barriers & Support", "ROI Analysis", "Skill Gap Analysis", 
    "AI Governance"
]

persona_views = {
    "General": ["Historical Trends"],
    "Business Leader": ["Financial Impact", "ROI Analysis", "Industry Analysis"],
    "Policymaker": ["Labor Impact", "Geographic Distribution", "Barriers & Support"],
    "Researcher": ["Productivity Research", "AI Technology Maturity", "Historical Trends"]
}

# Executive navigation function
def create_executive_navigation():
    """Simplified, executive-focused navigation"""
    st.sidebar.markdown("## 🎯 Executive Command Center")
    
    # Primary executive decision views
    exec_view = st.sidebar.radio(
        "Strategic Intelligence",
        ["🚀 Strategic Brief", "⚖️ Competitive Position", "💰 Investment Case", 
         "📊 Market Intelligence", "🎯 Action Planning"],
        help="Core executive decision support tools"
    )
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Key Market Metrics")
    st.sidebar.metric("Market Adoption", "78%", "+23pp")
    st.sidebar.metric("Cost Reduction", "280x", "Since 2022")
    st.sidebar.metric("Avg ROI", "3.2x", "Across sectors")
    
    # Secondary analysis (collapsed by default)
    st.sidebar.markdown("---")
    with st.sidebar.expander("📋 Detailed Analysis", expanded=False):
        detailed_view = st.selectbox("Analysis Type", 
                                   ["Historical Trends", "Industry Deep Dive", "Geographic Distribution", 
                                    "Technology Maturity", "Financial Impact", "Labor Impact"])
        use_detailed = st.checkbox("Switch to detailed view")
        
        if use_detailed:
            return detailed_view, True
    
    return exec_view, False

# Toggle between executive and detailed modes
def determine_navigation_mode():
    """Determine which navigation system to use"""
    
    # Let users choose their experience
    mode = st.sidebar.selectbox(
        "Dashboard Mode",
        ["🎯 Executive (Streamlined)", "📊 Analyst (Detailed)"],
        help="Choose your experience level"
    )
    
    if "Executive" in mode and st.session_state.feature_flags['executive_mode']:
        return create_executive_navigation()
    else:
        # Use your existing navigation
        view_type = st.sidebar.selectbox(
            "Analysis View", 
            ["Adoption Rates", "Historical Trends", "Industry Analysis", "Investment Trends", 
             "Regional Growth", "AI Cost Trends", "Token Economics", "Financial Impact", 
             "Labor Impact", "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
             "Productivity Research", "Environmental Impact", "Geographic Distribution", 
             "OECD 2025 Findings", "Barriers & Support", "ROI Analysis", "Skill Gap Analysis", 
             "AI Governance"]
        )
        return view_type, False

def apply_executive_styling():
    """Enhanced visual design for executive experience"""
    if not st.session_state.feature_flags['visual_redesign']:
        return
        
    st.markdown("""
    <style>
    .exec-metric {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .exec-metric h3 {
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .exec-metric h2 {
        margin: 0 0 0.25rem 0;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    .strategic-insight {
        border-left: 4px solid #2E86AB;
        background: rgba(46, 134, 171, 0.1);
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .strategic-insight h4 {
        color: #2E86AB;
        margin-top: 0;
    }
    
    .action-required {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    .action-required h4 {
        margin-top: 0;
        color: white;
    }
    
    .opportunity-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    /* FIXED: Eye-catching executive brief background */
    .exec-brief-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #3d5af1;
        color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .exec-brief-section h4 {
        color: #ffffff;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    
    .exec-brief-section p {
        color: #f8f9fa;
        line-height: 1.6;
    }
    
    .exec-brief-section ol li {
        color: #f8f9fa;
        margin-bottom: 0.5rem;
    }
    
    .exec-brief-section strong {
        color: #ffffff;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# [The rest of your function definitions continue here, starting with executive_metric()]
# ...
# def executive_metric(...):
# ...

# [Then, remove the old st.set_page_config() call from later in the script]
# Enhanced metric display function
def executive_metric(label, value, delta, insight, help_text=""):
    """Create visually appealing executive metrics"""
    st.markdown(f"""
    <div class="exec-metric">
        <h3>{label}</h3>
        <h2>{value}</h2>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">{delta}</p>
        <small style="opacity: 0.8;">{insight}</small>
    </div>
    """, unsafe_allow_html=True)

def executive_strategic_brief():
    """5-minute strategic intelligence for executives"""
    
    
    st.title("🎯Strategic Brief")
    st.markdown("*5-minute strategic intelligence for leadership decisions*")
    st.markdown("**Updated:** June 2025 | **Sources:** Stanford AI Index, McKinsey, OECD")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Critical metrics row
    st.subheader("📊 Market Reality Check")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        executive_metric("Market Adoption", "78%", "+23pp vs 2023", "Competitive table stakes")
    
    with col2:
        executive_metric("Cost Revolution", "280x cheaper", "Since Nov 2022", "Barriers eliminated")
    
    with col3:
        executive_metric("ROI Range", "2.5-4.2x", "Proven returns", "Strong business case")
    
    with col4:
        executive_metric("Time to Impact", "12-18 months", "Typical payback", "Fast value creation")
    
    # Strategic intelligence grid
    st.subheader("🧠 Strategic Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-required">
        <h4>⚠️ COMPETITIVE THREAT</h4>
        <p><strong>Market Reality:</strong></p>
        <ul>
        <li>78% of businesses now use AI (vs 55% in 2023)</li>
        <li>Non-adopters becoming minority position</li>
        <li>First-mover advantages accelerating</li>
        <li>GenAI adoption doubled to 71% in one year</li>
        </ul>
        <p><strong>→ Action Required:</strong> Assess competitive gap within 30 days</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="opportunity-box">
        <h4>💰 ECONOMIC OPPORTUNITY</h4>
        <p><strong>Investment Case:</strong></p>
        <ul>
        <li>280x cost reduction enables mass deployment</li>
        <li>Consistent 2.5-4.2x ROI across all sectors</li>
        <li>Productivity gains: 5-14% measured improvement</li>
        <li>$252B global investment validates market</li>
        </ul>
        <p><strong>→ Strategic Move:</strong> Build investment business case now</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="strategic-insight">
        <h4>🎯 IMPLEMENTATION REALITY</h4>
        <p><strong>Success Factors:</strong></p>
        <ul>
        <li>68% cite "lack of skilled personnel" as top barrier</li>
        <li>Full-stack approach (AI+Cloud+Digital) shows 3.5x ROI</li>
        <li>Technology leaders (92% adoption) set the pace</li>
        <li>Skills development is the critical bottleneck</li>
        </ul>
        <p><strong>→ Foundation Move:</strong> Start talent development immediately</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="strategic-insight">
        <h4>⏰ TIMING FACTORS</h4>
        <p><strong>Market Dynamics:</strong></p>
        <ul>
        <li>Technology maturity reaching enterprise readiness</li>
        <li>Regulatory frameworks stabilizing globally</li>
        <li>Talent market still accessible (but tightening)</li>
        <li>Investment costs at historic lows</li>
        </ul>
        <p><strong>→ Window of Opportunity:</strong> Move from pilot to production</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick competitive assessment
    st.subheader("⚖️ Quick Competitive Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        industry = st.selectbox("Your Industry", 
            ["Technology (92% adoption)", "Financial Services (85%)", "Healthcare (78%)", 
             "Manufacturing (75%)", "Retail & E-commerce (72%)", "Education (65%)",
             "Energy & Utilities (58%)", "Government (52%)"])
        
        company_size = st.selectbox("Company Size",
            ["1-50 employees (3% adoption)", "51-250 (12% adoption)", 
             "251-1000 (25% adoption)", "1000-5000 (42% adoption)", "5000+ (58% adoption)"])
    
    with col2:
        if st.button("🎯 Assess My Position", type="primary", use_container_width=True):
            assess_competitive_position(industry, company_size)
    
    # Executive summary
    st.subheader("🎯 Executive Summary")
    st.markdown("""
    **Bottom Line Up Front (BLUF):**

    AI adoption has reached irreversible market tipping point. The combination of 78% business adoption, 
    280x cost reduction, and proven ROI means competitive advantage now flows to implementation speed and quality, 
    not adoption decisions.

    **Strategic Imperative:**

    Move immediately from "Should we invest in AI?" to "How fast can we scale AI capabilities?" 
    Focus on talent development, full-stack integration, and production deployment over pilots.

    **Next 90 Days:**
    1. **Week 1-2:** Competitive gap analysis and investment case development
    2. **Week 3-8:** Talent assessment and capability building strategy  
    3. **Week 9-12:** Production deployment of highest-ROI use cases
    """)

def assess_competitive_position(industry, company_size):
    """Quick competitive assessment logic"""
    
    # Extract adoption rates from selections
    industry_adoption = int(industry.split('(')[1].split('%')[0])
    size_adoption = int(company_size.split('(')[1].split('%')[0])
    
    # Simple scoring logic
    competitive_score = (industry_adoption + size_adoption) / 2
    
    if competitive_score >= 70:
        status = "LEADER"
        color = "success"
        message = "You're in a leading position. Focus on maintaining advantage and innovation."
    elif competitive_score >= 50:
        status = "COMPETITIVE"
        color = "warning" 
        message = "You're competitive but need to accelerate to avoid falling behind."
    else:
        status = "AT RISK"
        color = "error"
        message = "Urgent action required. You're falling behind market adoption."
    
    if color == "success":
        st.success(f"**Status: {status}**\n\n{message}")
    elif color == "warning":
        st.warning(f"**Status: {status}**\n\n{message}")
    else:
        st.error(f"**Status: {status}**\n\n{message}")

# Apply styling
apply_executive_styling()

# Helper function to validate chart data before plotting
def validate_chart_data(data, required_columns):
    """Validate data has required columns for charting"""
    if data is None:
        return False, "Data is None"
    
    if hasattr(data, 'empty') and data.empty:
        return False, "Data is empty"
    
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        return False, f"Missing columns: {missing_cols}"
    
    return True, "Data is valid"

def safe_data_check(data, data_name):
    """Safe data validation with user-friendly error messages"""
    if data is None:
        st.error(f"❌ {data_name} is not available.")
        st.info("Please check data loading or contact support.")
        return False
    
    if hasattr(data, 'empty') and data.empty:
        st.error(f"❌ {data_name} is empty.")
        st.info("Please check data sources or refresh the application.")
        return False
    
    return True

# Data loading function - updated with AI Index 2025 data
def load_data():
    """Load all dashboard data with comprehensive error handling"""
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
                        'Traditional AI', 'Traditional AI', 'Traditional AI', 'GenAI', 'Traditional AI', 'Traditional AI']
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
        
        # Token pricing evolution - Simplified to avoid datetime issues
        token_pricing_evolution = pd.DataFrame({
            'date': ['2022-11-01', '2023-02-01', '2023-05-01', '2023-08-01', '2023-11-01',
                     '2024-02-01', '2024-05-01', '2024-08-01', '2024-11-01', '2025-02-01', '2025-05-01'],
            'avg_price_input': [20.0, 18.0, 15.0, 10.0, 5.0, 3.0, 1.5, 0.8, 0.5, 0.3, 0.2],
            'avg_price_output': [20.0, 19.0, 16.0, 12.0, 8.0, 5.0, 3.0, 2.0, 1.5, 1.0, 0.8],
            'models_available': [5, 8, 12, 18, 25, 35, 45, 58, 72, 85, 95]
        })
        
        return (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, geographic, 
                state_data, tech_stack, productivity_data, productivity_by_skill, ai_productivity_estimates, 
                oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
                ai_investment_data, regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
                skill_gap_data, ai_governance, token_economics, token_usage_patterns, token_optimization, token_pricing_evolution)
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Load data first to ensure all variables are available
try:
    loaded_data = load_data()
    
    # Initialize all variables to None first
    historical_data = sector_2018 = sector_2025 = firm_size = ai_maturity = geographic = state_data = tech_stack = productivity_data = productivity_by_skill = ai_productivity_estimates = oecd_g7_adoption = oecd_applications = barriers_data = support_effectiveness = ai_investment_data = regional_growth = ai_cost_reduction = financial_impact = ai_perception = skill_gap_data = ai_governance = token_economics = token_usage_patterns = token_optimization = token_pricing_evolution = None
    
    # Only unpack if data loading was successful
    if loaded_data is not None:
        try:
            (historical_data, sector_2018, sector_2025, firm_size, ai_maturity, geographic, 
             state_data, tech_stack, productivity_data, productivity_by_skill, ai_productivity_estimates, 
             oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness, 
             ai_investment_data, regional_growth, ai_cost_reduction, financial_impact, ai_perception, 
             skill_gap_data, ai_governance, token_economics, token_usage_patterns, token_optimization, token_pricing_evolution) = loaded_data
            st.success("✓ Data loaded and unpacked successfully!")
        except Exception as e:
            st.error(f"❌ Error unpacking data: {str(e)}")
            st.error("Dashboard will run with limited functionality.")
    else:
        st.error("❌ Data loading failed. Dashboard will run with limited functionality.")
        st.info("Please refresh the page or contact support if the issue persists.")
        
except Exception as e:
    st.error(f"❌ Critical error in data loading: {str(e)}")
    # Create minimal fallback data to prevent crashes
    historical_data = pd.DataFrame({'year': [2024], 'ai_use': [78], 'genai_use': [71]})
    ai_cost_reduction = pd.DataFrame({'model': ['Test'], 'cost_per_million_tokens': [0.07], 'year': [2024]})
    token_economics = pd.DataFrame({'model': ['Test'], 'cost_per_million_input': [0.07], 'cost_per_million_output': [0.07]})
    financial_impact = pd.DataFrame({'function': ['Test'], 'companies_reporting_cost_savings': [49], 'companies_reporting_revenue_gains': [57]})
    ai_perception = pd.DataFrame({'generation': ['Test'], 'expect_job_change': [65], 'expect_job_replacement': [40]})
    firm_size = pd.DataFrame({'size': ['Test'], 'adoption': [25]})
    tech_stack = pd.DataFrame({'technology': ['Test'], 'percentage': [100]})
    ai_maturity = pd.DataFrame({'technology': ['Test'], 'adoption_rate': [50], 'risk_score': [50], 'time_to_value': [3]})
    productivity_data = pd.DataFrame({'year': [2025], 'productivity_growth': [0.4], 'young_workers_share': [38]})
    geographic = pd.DataFrame({'city': ['Test'], 'state': ['Test'], 'lat': [0], 'lon': [0], 'rate': [7], 'state_code': ['XX']})
    state_data = pd.DataFrame({'state': ['Test'], 'state_code': ['XX'], 'rate': [7]})
    oecd_g7_adoption = pd.DataFrame({'country': ['Test'], 'adoption_rate': [45], 'manufacturing': [52], 'ict_sector': [68]})
    oecd_applications = pd.DataFrame({'application': ['Test'], 'usage_rate': [50], 'category': ['Traditional AI']})
    barriers_data = pd.DataFrame({'barrier': ['Test'], 'percentage': [68]})
    support_effectiveness = pd.DataFrame({'support_type': ['Test'], 'effectiveness_score': [82]})
    ai_investment_data = pd.DataFrame({'year': [2024], 'total_investment': [252.3], 'genai_investment': [33.9]})
    regional_growth = pd.DataFrame({'region': ['Test'], 'growth_2024': [20], 'adoption_rate': [70]})
    ai_perception = pd.DataFrame({'generation': ['Test'], 'expect_job_change': [65], 'expect_job_replacement': [40]})
    skill_gap_data = pd.DataFrame({'skill': ['Test'], 'gap_severity': [85], 'training_initiatives': [45]})
    ai_governance = pd.DataFrame({'aspect': ['Test'], 'adoption_rate': [62], 'maturity_score': [3.2]})
    token_usage_patterns = pd.DataFrame({'use_case': ['Test'], 'avg_input_tokens': [100], 'avg_output_tokens': [200]})
    token_optimization = pd.DataFrame({'strategy': ['Test'], 'cost_reduction': [30], 'implementation_complexity': [2]})
    token_pricing_evolution = pd.DataFrame({'date': ['2024-01-01'], 'avg_price_input': [0.2], 'avg_price_output': [0.8]})
    sector_2018 = pd.DataFrame({'sector': ['Test'], 'firm_weighted': [10], 'employment_weighted': [15]})
    sector_2025 = pd.DataFrame({'sector': ['Test'], 'adoption_rate': [75], 'genai_adoption': [60], 'avg_roi': [3.0]})
    productivity_by_skill = pd.DataFrame({'skill_level': ['Test'], 'productivity_gain': [10], 'skill_gap_reduction': [20]})
    ai_productivity_estimates = pd.DataFrame({'source': ['Test'], 'annual_impact': [1.0]})
    
    st.warning("⚠️ Using fallback data due to loading error. Some features may be limited.")

# Determine navigation mode
current_view, is_detailed = determine_navigation_mode()

# Route to appropriate view
if not is_detailed:
    # Executive views
    if current_view == "🚀 Strategic Brief":
        executive_strategic_brief()
    elif current_view == "⚖️ Competitive Position":
        st.subheader("⚖️ Competitive Position Intelligence")
        st.markdown("*Understand your strategic position in the AI adoption landscape*")
        
        # Quick positioning assessment
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Position Your Company")
            
            industry = st.selectbox("Your Industry", [
                "Technology (92% adoption)",
                "Financial Services (85% adoption)", 
                "Healthcare (78% adoption)",
                "Manufacturing (75% adoption)",
                "Retail & E-commerce (72% adoption)",
                "Education (65% adoption)",
                "Energy & Utilities (58% adoption)",
                "Government (52% adoption)"
            ], help="Select your primary industry")
            
            company_size = st.selectbox("Company Size", [
                "1-50 employees (3% adoption)",
                "51-250 employees (12% adoption)",
                "251-1000 employees (25% adoption)", 
                "1000-5000 employees (42% adoption)",
                "5000+ employees (58% adoption)"
            ], help="Select your company size range")
            
            current_ai_maturity = st.select_slider("Current AI Maturity", [
                "Exploring (0-10%)",
                "Piloting (10-30%)", 
                "Implementing (30-60%)",
                "Scaling (60-80%)",
                "Leading (80%+)"
            ], help="Estimate your current AI implementation level")
        
        with col2:
            if st.button("🎯 Assess My Position", type="primary", use_container_width=True):
                # Extract percentages for calculation
                industry_rate = int(industry.split('(')[1].split('%')[0])
                size_rate = int(company_size.split('(')[1].split('%')[0])
                maturity_score = {"Exploring (0-10%)": 5, "Piloting (10-30%)": 20, 
                                "Implementing (30-60%)": 45, "Scaling (60-80%)": 70, 
                                "Leading (80%+)": 90}[current_ai_maturity]
                
                # Calculate competitive position
                competitive_score = (industry_rate * 0.4 + size_rate * 0.4 + maturity_score * 0.2)
                
                if competitive_score >= 70:
                    st.success(f"""
                    **🏆 COMPETITIVE LEADER**
                    
                    **Position Score:** {competitive_score:.0f}/100
                    
                    **Status:** You're ahead of most competitors
                    **Focus:** Innovation and market expansion
                    **Risk Level:** Low - maintain leadership
                    """)
                elif competitive_score >= 50:
                    st.warning(f"""
                    **⚖️ COMPETITIVE POSITION**
                    
                    **Position Score:** {competitive_score:.0f}/100
                    
                    **Status:** Keeping pace with market
                    **Focus:** Accelerate to gain advantage  
                    **Risk Level:** Medium - must not fall behind
                    """)
                else:
                    st.error(f"""
                    **⚠️ COMPETITIVE RISK**
                    
                    **Position Score:** {competitive_score:.0f}/100
                    
                    **Status:** Behind market adoption curve
                    **Focus:** Urgent catch-up required
                    **Risk Level:** High - immediate action needed
                    """)
        
        # Competitive landscape visualization
        st.markdown("### 📊 Competitive Landscape Analysis")
        if firm_size is not None:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=firm_size['size'], 
                y=firm_size['adoption'],
                marker=dict(
                    color=firm_size['adoption'],
                    colorscale='RdYlGn',
                    colorbar=dict(title="Competitive Position")
                ),
                text=[f'{x}%' for x in firm_size['adoption']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Adoption: %{y}%<br>Position: %{customdata}<extra></extra>',
                customdata=['High Risk', 'High Risk', 'At Risk', 'At Risk', 'Below Average',
                           'Average', 'Competitive', 'Strong', 'Very Strong', 'Leader', 'Dominant']
            ))
            fig.add_hline(y=25, line_dash="dash", line_color="orange", 
                          annotation_text="Competitive Threshold (25%)", annotation_position="right")
            fig.add_hline(y=50, line_dash="dash", line_color="green",
                          annotation_text="Strong Position (50%)", annotation_position="right")
            fig.add_hrect(y0=0, y1=25, fillcolor="red", opacity=0.1, 
                          annotation_text="Risk Zone", annotation_position="top left")
            fig.add_hrect(y0=25, y1=50, fillcolor="yellow", opacity=0.1,
                          annotation_text="Competitive Zone", annotation_position="top left")  
            fig.add_hrect(y0=50, y1=100, fillcolor="green", opacity=0.1,
                          annotation_text="Leadership Zone", annotation_position="top left")
            fig.update_layout(
                title='Competitive Position by Company Size - Where Do You Stand?',
                xaxis_title='Company Size (Employees)',
                yaxis_title='AI Adoption Rate (%)',
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Firm size data not available. Competitive landscape chart cannot be displayed.")
    
    elif current_view == "💰 Investment Case":
        st.subheader("💰 AI Investment Case Builder")
        st.markdown("*Build a compelling business case for AI investment*")
        
        # Investment context from market data
        st.markdown("### 📊 Investment Market Context")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("2024 Global Investment", "$252.3B", "+44.5% YoY", 
                     help="Total corporate AI investment reached record levels")
        with col2:
            st.metric("US Investment Lead", "12x vs China", "$109.1B vs $9.3B", 
                     help="US dominates global AI investment")
        with col3:
            st.metric("Average ROI Range", "2.5-4.2x", "Across all sectors", 
                     help="Consistent returns validate AI investment")
        with col4:
            st.metric("Typical Payback", "12-18 months", "Fast value creation", 
                     help="Faster than most technology investments")

        # Investment case builder
        st.markdown("### 🎯 Build Your Investment Case")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Investment Parameters**")

            investment_amount = st.number_input(
                "Total Investment Budget ($)", 
                min_value=10000, 
                max_value=10000000, 
                value=500000, 
                step=50000,
                help="Include technology, talent, and implementation costs"
            )

            investment_timeline = st.selectbox(
                "Investment Timeline",
                ["6 months", "12 months", "18 months", "24 months", "36 months"],
                index=2,
                help="Time horizon for full investment deployment"
            )

            primary_goal = st.selectbox(
                "Primary Investment Goal",
                ["Operational Efficiency", "Revenue Growth", "Cost Reduction", 
                 "Innovation & New Products", "Risk Management", "Customer Experience"],
                help="Main strategic objective for AI investment"
            )

            industry_context = st.selectbox(
                "Your Industry",
                ["Technology", "Financial Services", "Healthcare", "Manufacturing", 
                 "Retail", "Education", "Energy", "Government"],
                help="Industry affects ROI expectations and implementation approach"
            )

        with col2:
            st.markdown("**Expected Outcomes**")

            # Calculate investment projections
            timeline_months = int(investment_timeline.split()[0])

            # Industry ROI multipliers
            industry_roi = {
                "Technology": 4.2, "Financial Services": 3.8, "Healthcare": 3.2,
                "Manufacturing": 3.5, "Retail": 3.0, "Education": 2.5,
                "Energy": 2.8, "Government": 2.2
            }

            base_roi = industry_roi.get(industry_context, 3.0)

            # Goal impact multipliers
            goal_multiplier = {
                "Operational Efficiency": 1.2, "Revenue Growth": 1.1, "Cost Reduction": 1.3,
                "Innovation & New Products": 1.0, "Risk Management": 0.9, "Customer Experience": 1.1
            }

            adjusted_roi = base_roi * goal_multiplier.get(primary_goal, 1.0)

            # Calculate projections
            total_return = investment_amount * adjusted_roi
            net_benefit = total_return - investment_amount
            monthly_benefit = net_benefit / timeline_months
            payback_months = max(6, int(timeline_months / adjusted_roi))

            st.metric("Projected ROI", f"{adjusted_roi:.1f}x", 
                     f"Based on {industry_context} average")
            st.metric("Total Expected Return", f"${total_return:,.0f}", 
                     f"Over {timeline_months} months")
            st.metric("Net Benefit", f"${net_benefit:,.0f}", 
                     f"${monthly_benefit:,.0f}/month average")
            st.metric("Payback Period", f"{payback_months} months", 
                     "Time to recover investment")

        # Generate business case
        if st.button("📋 Generate Business Case", type="primary", use_container_width=True):

            st.markdown("---")
            st.markdown("### 📋 Executive Business Case Summary")

            # Create business case document
            business_case = f"""
            ## AI Investment Business Case

            **Investment Request:** ${investment_amount:,} over {timeline_months} months

            **Strategic Objective:** {primary_goal}

            **Financial Projections:**
            - Expected ROI: {adjusted_roi:.1f}x
            - Total Return: ${total_return:,.0f}
            - Net Benefit: ${net_benefit:,.0f}
            - Payback Period: {payback_months} months
            - Monthly Value Creation: ${monthly_benefit:,.0f}

            **Market Context:**
            - Industry average ROI: {industry_roi[industry_context]:.1f}x
            - 2024 global AI investment: $252.3B (+44.5% YoY)
            - 78% of businesses now use AI
            - Typical payback: 12-18 months

            **Risk Assessment:**
            - Market Risk: Low (proven ROI across sectors)
            - Technology Risk: Medium (rapid evolution)
            - Implementation Risk: Medium (depends on execution)
            - Competitive Risk: High (cost of inaction)

            **Recommendation:** {"APPROVE" if adjusted_roi >= 2.5 else "REVIEW SCOPE"}

            **Rationale:** {"Strong ROI projection above 2.5x threshold with proven market validation" if adjusted_roi >= 2.5 else "ROI below recommended threshold - consider smaller scope or different approach"}
            """

            st.markdown(business_case)

            # Risk vs reward analysis
            st.markdown("### ⚖️ Risk vs Reward Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Investment Risks:**")
                st.write("• Technology complexity and integration challenges")
                st.write("• Talent acquisition and skills development needs")
                st.write("• Change management and organizational adoption")
                st.write("• Rapid technology evolution requiring updates")

            with col2:
                st.markdown("**Competitive Risks of NOT Investing:**")
                st.write("• Productivity disadvantage vs AI-adopting competitors")
                st.write("• Higher operational costs and slower processes")
                st.write("• Talent retention challenges (employees want AI tools)")
                st.write("• Missing market opportunities and customer expectations")

            # Success factors
            st.markdown("### 🎯 Critical Success Factors")

            success_factors = f"""
            **For {primary_goal} in {industry_context}:**

            1. **Executive Sponsorship:** C-level champion and clear mandate
            2. **Talent Strategy:** Hire/train AI specialists and upskill existing team  
            3. **Data Foundation:** Clean, accessible data infrastructure
            4. **Change Management:** User adoption and process transformation
            5. **Vendor Selection:** Right technology partners and platforms
            6. **Measurement:** Clear KPIs and ROI tracking from day one
            """

            st.info(success_factors)

            # Download business case
            st.download_button(
                label="📥 Download Business Case",
                data=business_case,
                file_name=f"AI_Investment_Case_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        # Benchmarking section
        st.markdown("### 📊 Industry Investment Benchmarks")

        # Use your existing sector data for benchmarking
        benchmark_data = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                      'Retail', 'Education', 'Energy', 'Government'],
            'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'avg_investment': [2.5, 1.8, 1.2, 1.5, 1.0, 0.8, 1.1, 0.9]  # Millions
        })

        fig = px.scatter(
            benchmark_data,
            x='avg_investment',
            y='avg_roi',
            size='adoption_rate',
            color='sector',
            title='Industry AI Investment Benchmarks',
            labels={
                'avg_investment': 'Average Investment ($M)',
                'avg_roi': 'Average ROI (x)',
                'adoption_rate': 'Adoption Rate (%)'
            },
            height=400
        )

        fig.update_traces(textposition='top center')

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **Investment Intelligence:**
        - Technology sector leads both investment levels and ROI
        - Financial Services shows strong ROI with high investment
        - Manufacturing offers solid returns with moderate investment
        - Government shows lower ROI but strategic importance
        """) 

    elif current_view == "📊 Market Intelligence":
        st.subheader("📊 Market Intelligence Dashboard")
        st.markdown("*Key market trends and competitive dynamics for strategic decision-making*")
        
        # Market overview metrics
        st.markdown("### 🌍 Global AI Market Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Global Adoption", "78%", "+23pp vs 2023", 
                     help="Businesses using any AI technology")
        with col2:
            st.metric("GenAI Adoption", "71%", "+38pp vs 2023", 
                     help="More than doubled in one year")
        with col3:
            st.metric("Investment Growth", "+44.5%", "$252.3B in 2024", 
                     help="Record year-over-year growth")
        with col4:
            st.metric("Cost Reduction", "280x", "Since Nov 2022", 
                     help="AI processing costs collapsed")
        
        # Market trends visualization
        st.markdown("### 📈 Market Adoption Acceleration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Historical trends chart
            if historical_data is not None:
                try:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=historical_data['year'], 
                        y=historical_data['ai_use'], 
                        mode='lines+markers',
                        name='Overall AI Use',
                        line=dict(width=4, color='#1f77b4'),
                        marker=dict(size=8),
                        text=[f'{x}%' for x in historical_data['ai_use']],
                        textposition='top center'
                    ))
                    fig.add_trace(go.Scatter(
                        x=historical_data['year'], 
                        y=historical_data['genai_use'], 
                        mode='lines+markers',
                        name='GenAI Use',
                        line=dict(width=4, color='#ff7f0e'),
                        marker=dict(size=8),
                        text=[f'{x}%' for x in historical_data['genai_use']],
                        textposition='bottom center'
                    ))
                    fig.add_annotation(
                        x=2022, y=33,
                        text="ChatGPT Launch<br>GenAI Revolution",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="#ff7f0e",
                        ax=-30, ay=-40,
                        bgcolor="rgba(255,127,14,0.1)",
                        bordercolor="#ff7f0e"
                    )
                    fig.update_layout(
                        title="AI Adoption Explosion: 2017-2025",
                        xaxis_title="Year",
                        yaxis_title="Adoption Rate (%)",
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.info(f"Could not plot historical data: {e}")
            else:
                st.info("Historical data not available.")
        
        with col2:
            st.markdown("**📊 Market Intelligence:**")
            st.success("""
            **Tipping Point Reached**
            - 78% adoption = AI is now mainstream
            - GenAI doubled to 71% in one year
            - Non-adopters becoming minority
            """)
            
            st.info("""
            **Cost Revolution**
            - 280x cost reduction enables mass deployment
            - Processing barriers eliminated
            - SMEs can now afford enterprise AI
            """)
            
            st.warning("""
            **Competitive Urgency**
            - First-mover advantages accelerating
            - Talent market tightening rapidly
            - Technology maturity enabling scale
            """)
        
        # Industry leadership analysis
        st.markdown("### 🏭 Industry Leadership Landscape")
        
        # Use your existing sector data
        industry_leaders = pd.DataFrame({
            'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                      'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
            'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
            'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
            'momentum': ['High', 'High', 'Very High', 'Medium', 'High', 'Medium', 'Low', 'Low']
        })
        
        fig = go.Figure()
        
        # Create bubble chart
        fig.add_trace(go.Scatter(
            x=industry_leaders['adoption_rate'],
            y=industry_leaders['genai_adoption'],
            mode='markers+text',
            marker=dict(
                size=[20, 18, 16, 14, 12, 10, 8, 6],  # Size by market importance
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=industry_leaders['sector'],
            textposition='middle center',
            textfont=dict(size=10, color='white'),
            hovertemplate='<b>%{text}</b><br>Overall AI: %{x}%<br>GenAI: %{y}%<extra></extra>'
        ))
        
        # Add quadrant lines
        fig.add_hline(y=65, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=70, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=85, y=80, text="Leaders<br>(High AI + High GenAI)", 
                          showarrow=False, font=dict(color="green", size=12))
        fig.add_annotation(x=85, y=50, text="Traditional AI Leaders<br>(High AI + Low GenAI)", 
                          showarrow=False, font=dict(color="blue", size=12))
        fig.add_annotation(x=55, y=80, text="GenAI Early Adopters<br>(Low AI + High GenAI)", 
                          showarrow=False, font=dict(color="orange", size=12))
        fig.add_annotation(x=55, y=50, text="Emerging Markets<br>(Low AI + Low GenAI)", 
                          showarrow=False, font=dict(color="red", size=12))
        
        fig.update_layout(
            title='Industry AI Leadership Matrix: Overall vs GenAI Adoption',
            xaxis_title='Overall AI Adoption Rate (%)',
            yaxis_title='GenAI Adoption Rate (%)',
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Regional intelligence
        st.markdown("### 🌍 Regional Market Dynamics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional growth chart
            regions = ['North America', 'Greater China', 'Europe', 'Asia-Pacific', 'Latin America']
            adoption_rates = [82, 68, 65, 58, 45]
            growth_rates = [15, 27, 23, 18, 12]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Current Adoption',
                x=regions,
                y=adoption_rates,
                marker_color='#3498DB',
                text=[f'{x}%' for x in adoption_rates],
                textposition='outside'
            ))
            
            # Add growth rate as line
            fig.add_trace(go.Scatter(
                name='2024 Growth Rate',
                x=regions,
                y=growth_rates,
                mode='lines+markers',
                line=dict(width=3, color='#E74C3C'),
                marker=dict(size=10),
                yaxis='y2',
                text=[f'+{x}pp' for x in growth_rates],
                textposition='top center'
            ))
            
            fig.update_layout(
                title='Regional AI Adoption vs Growth Rates',
                xaxis_title='Region',
                yaxis=dict(title='Adoption Rate (%)', side='left'),
                yaxis2=dict(title='Growth Rate (pp)', side='right', overlaying='y'),
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🌍 Regional Intelligence:**")
            
            st.info("""
            **North America**
            - Leads adoption at 82%
            - Mature market with slower growth
            - Focus on advanced applications
            """)
            
            st.warning("""
            **Greater China** 
            - Fastest growth at +27pp
            - Rapid catch-up trajectory
            - Government-backed initiatives
            """)
            
            st.success("""
            **Europe**
            - Balanced growth at +23pp
            - Strong regulatory framework
            - Focus on ethical AI
            """)
        
        # Investment flow analysis
        st.markdown("### 💰 Global Investment Intelligence")
        
        # Investment by region
        investment_regions = pd.DataFrame({
            'region': ['United States', 'China', 'United Kingdom', 'Germany', 'Rest of World'],
            'investment_2024': [109.1, 9.3, 4.5, 3.2, 126.2],
            'share': [43.2, 3.7, 1.8, 1.3, 50.0]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Investment pie chart
            fig = px.pie(
                investment_regions,
                values='investment_2024',
                names='region',
                title='2024 AI Investment by Region ($252.3B Total)',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**💰 Investment Insights:**")
            
            st.metric("US Dominance", "43.2%", "12x larger than China")
            st.metric("Top 4 Countries", "59%", "Concentrated investment")
            st.metric("Growth Rate", "+44.5%", "Record investment year")
            
            st.info("""
            **Investment Patterns:**
            - US leads with $109.1B (12x China)
            - Europe combined: ~$15B
            - Asia-Pacific growing rapidly
            - Private investment concentrated in coastal hubs
            """)
        
        # Market predictions
        st.markdown("### 🔮 Market Outlook & Predictions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📈 2025 Predictions**")
            st.write("• Adoption plateaus around 85-90%")
            st.write("• Focus shifts to AI quality & ROI")
            st.write("• Consolidation in AI vendor market")
            st.write("• Regulatory frameworks solidify")
            
        with col2:
            st.markdown("**⚡ Key Accelerators**")
            st.write("• Continued cost reduction (10-100x)")
            st.write("• Multi-modal AI capabilities")
            st.write("• Enterprise-ready AI platforms")
            st.write("• Skills development programs")
        
        with col3:
            st.markdown("**⚠️ Risk Factors**")
            st.write("• Talent shortage intensifying")
            st.write("• Regulatory uncertainty")
            st.write("• Technology complexity")
            st.write("• Economic downturn impact")
        
        # Market intelligence summary
        st.markdown("### 🎯 Strategic Market Intelligence Summary")
        
        st.success("""
        **Bottom Line for Leadership:**
        
        **Market Reality:** AI adoption has crossed the mainstream threshold (78%). The question is no longer "Should we adopt AI?" but "How fast can we scale high-quality AI implementations?"
        
        **Competitive Dynamics:** Technology and Financial Services sectors have pulled ahead (85-92% adoption). Other sectors have 6-18 month window to catch up before significant competitive disadvantages emerge.
        
        **Investment Environment:** Record $252B investment validates market opportunity. 280x cost reduction has eliminated economic barriers. Focus should shift from proof-of-concept to production scaling.
        
        **Strategic Imperative:** Move immediately from pilot projects to production deployment. Prioritize talent development, full-stack integration, and measurable business outcomes.
        """)
    elif current_view == "🎯 Action Planning":
        st.subheader("🎯 Evidence-Based Action Planning")
        st.markdown("*Strategic decisions based on comprehensive academic and institutional research*")
        
        # Multi-source competitive urgency assessment
        st.markdown("### ⏰ Competitive Timing Analysis")
        st.markdown("*Synthesized from Stanford AI Index 2025, U.S. Census Bureau AI Use Supplement, and Federal Reserve research*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            industry_selection = st.selectbox("Your Industry", [
                "Technology (92% adoption)",
                "Financial Services (85% adoption)", 
                "Healthcare (78% adoption)",
                "Manufacturing (75% adoption)",
                "Retail & E-commerce (72% adoption)",
                "Education (65% adoption)",
                "Energy & Utilities (58% adoption)",
                "Government (52% adoption)"
            ])
            
            company_size_selection = st.selectbox("Company Size", [
                "1-50 employees (3% adoption)",
                "51-250 employees (12% adoption)",
                "251-1000 employees (25% adoption)", 
                "1000-5000 employees (42% adoption)",
                "5000+ employees (58% adoption)"
            ])
        
        with col2:
            if industry_selection is not None and company_size_selection is not None:
                try:
                    industry_rate = int(industry_selection.split('(')[1].split('%')[0])
                    size_rate = int(company_size_selection.split('(')[1].split('%')[0])
                    st.metric("Industry Adoption", f"{industry_rate}%", "U.S. Census Bureau data")
                    st.metric("Size Category", f"{size_rate}%", "850,000 firms surveyed")
                    market_pressure = (industry_rate + size_rate) / 2
                    if market_pressure >= 70:
                        st.error("**HIGH COMPETITIVE PRESSURE**")
                        st.write("🚨 Federal Reserve research shows productivity gaps widening")
                    elif market_pressure >= 40:
                        st.warning("**MODERATE COMPETITIVE PRESSURE**") 
                        st.write("⚠️ Brynjolfsson et al. (2023) documents acceleration phase")
                    else:
                        st.info("**EARLY OPPORTUNITY WINDOW**")
                        st.write("💡 Acemoglu (2024) models show first-mover advantages")
                except Exception as e:
                    st.info(f"Could not calculate market pressure: {e}")
            else:
                st.info("Industry or company size selection not available.")
        
        # Academic research on implementation patterns
        st.markdown("### 📊 Implementation Success Patterns")
        st.markdown("*Multi-source academic analysis: Bick, Blandin & Deming (2024, 2025), Brynjolfsson et al. (2023), Federal Reserve research*")
        
        # Enhanced implementation data with academic backing
        implementation_data = pd.DataFrame({
            'approach': ['Full-Stack\n(AI+Cloud+Digital)', 'AI + Cloud', 'AI + Digitization', 'AI Only'],
            'companies_using': [38, 23, 24, 15],  # Your tech_stack data
            'fed_research_roi': [3.8, 2.9, 2.6, 1.7],  # Federal Reserve estimates
            'academic_success_rate': [82, 68, 62, 45]  # Academic literature synthesis
        })
        
        if implementation_data is not None:
            fig = px.scatter(
                implementation_data,
                x='companies_using',
                y='fed_research_roi',
                size='academic_success_rate',
                color='approach',
                title='Implementation Patterns: Federal Reserve & Academic Research',
                labels={
                    'companies_using': 'Adoption Rate (% of Companies)',
                    'fed_research_roi': 'Federal Reserve ROI Estimates',
                    'academic_success_rate': 'Academic Success Rate (%)'
                },
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Implementation data not available.")
        
        st.info("""
        **Multi-Source Validation:** Federal Reserve working papers (Bick, Blandin & Deming, 2024) 
        confirm 2.2x higher productivity gains from integrated approaches. Brynjolfsson et al. (2023) 
        document similar patterns in their NBER working paper on generative AI at work.
        """)
        
        # Academic research on productivity impact
        st.markdown("### 📈 Productivity Impact Research")
        st.markdown("*Federal Reserve, MIT, NBER, and Goldman Sachs research synthesis*")
        
        research_tabs = st.tabs(["🏛️ Federal Reserve", "🎓 MIT Research", "📊 NBER Studies", "🏢 Goldman Sachs"])
        
        with research_tabs[0]:
            st.markdown("**Federal Reserve Research (Bick, Blandin & Deming, 2024-2025):**")
            st.write("• **Worker-level analysis:** 15% productivity improvement with AI access")
            st.write("• **Task-level impact:** 47-56% of tasks affected by AI capabilities")
            st.write("• **Adoption timeline:** Voluntary adoption shows stronger correlation with productivity")
            st.write("• **Macroeconomic effect:** 0.4% aggregate productivity gain with full beneficial adoption")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Worker Productivity Gain", "+15%", "With AI tool access")
            with col2:
                st.metric("Task Acceleration", "47-56%", "Of tasks can be enhanced")
        
        with research_tabs[1]:
            st.markdown("**MIT Research (Acemoglu, 2024):**")
            st.write("• **Economic modeling:** Simple macroeconomics framework for AI impact")
            st.write("• **Productivity estimate:** +0.66% total factor productivity over 10 years")
            st.write("• **Task substitution:** 15% of tasks can be completed significantly faster")
            st.write("• **Conservative outlook:** Modest but nontrivial macroeconomic effects")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("10-Year TFP Growth", "+0.66%", "Conservative estimate")
            with col2:
                st.metric("Task Acceleration", "15%", "Significantly faster completion")
        
        with research_tabs[2]:
            st.markdown("**NBER Research (Brynjolfsson et al., 2023):**")
            st.write("• **Generative AI study:** Comprehensive analysis of workplace impact")
            st.write("• **Customer service:** 14% increase in productivity in real-world trials")
            st.write("• **Skill inequality:** Largest benefits for less-experienced workers")
            st.write("• **Learning effects:** Productivity gains increase with continued use")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Customer Service Gains", "+14%", "Real-world trial results")
            with col2:
                st.metric("Inequality Reduction", "Yes", "Helps lower-skilled workers")
        
        with research_tabs[3]:
            st.markdown("**Goldman Sachs Research (Briggs & Kodnani, 2023):**")
            st.write("• **Economic growth model:** Potential for significant GDP impact")
            st.write("• **Investment thesis:** AI as a general-purpose technology")
            st.write("• **Timeline:** Effects realized over 10-year horizon")
            st.write("• **Global impact:** Transformative potential across all sectors")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Potential GDP Impact", "+7%", "Over 10 years")
            with col2:
                st.metric("Investment Validation", "Strong", "General-purpose tech")
        
        # NIST and government framework guidance
        st.markdown("### 🏛️ Government Framework Implementation")
        st.markdown("*NIST AI Risk Management Framework, NSF AI Research Institutes, FDA guidance*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**NIST AI RMF 1.0 (January 2023) Guidelines:**")
            st.write("• **Governance:** Establish AI oversight and accountability")
            st.write("• **Risk Management:** Systematic assessment and mitigation")
            st.write("• **Trustworthy AI:** Focus on reliability, fairness, explainability")
            st.write("• **Multi-stakeholder:** 240+ organizations contributed to framework")
            
            st.success("""
            **NIST Recommendation:** Start with governance framework 
            before scaling AI implementations across organization.
            """)
        
        with col2:
            st.markdown("**NSF AI Research Institutes ($220M investment):**")
            st.write("• **27 institutes** across 40+ states providing research foundation")
            st.write("• **University partnerships** for workforce development")
            st.write("• **Public-private collaboration** models proven effective")
            st.write("• **Regional distribution** ensures national AI capacity building")
            
            st.info("""
            **NSF Pattern:** Successful AI adoption requires 
            research-industry-government collaboration model.
            """)
        
        # IEEE and technical standards
        st.markdown("### 🔬 Technical Implementation Standards")
        st.markdown("*IEEE Computer Society, Nature Machine Intelligence, academic technical research*")
        
        technical_standards = pd.DataFrame({
            'standard_area': ['Model Development', 'Data Quality', 'System Integration', 'Performance Monitoring'],
            'ieee_guidance': ['IEEE 2857-2021', 'IEEE 2671-2021', 'IEEE 2857-2021', 'IEEE 2857-2021'],
            'academic_support': ['Nature MI papers', 'MIT Tech Review', 'Multiple journals', 'NBER studies'],
            'implementation_priority': [1, 2, 3, 4]
        })
        
        st.dataframe(technical_standards, hide_index=True, use_container_width=True)
        
        st.warning("""
        **Technical Research Consensus:** Data quality (IEEE 2671-2021) is consistently 
        cited as the foundation for successful AI implementation across all academic sources.
        """)
        
        # Multi-source barrier analysis
        st.markdown("### 🚧 Research-Validated Implementation Barriers")
        st.markdown("*OECD AI Policy Observatory, U.S. Census Bureau, McKinsey synthesis*")
        
        # Enhanced barriers with multi-source validation
        barriers_with_sources = pd.DataFrame({
            'barrier': ['Lack of skilled personnel', 'Data availability/quality', 'Integration complexity', 
                       'Regulatory uncertainty', 'High implementation costs'],
            'oecd_percentage': [68, 62, 58, 55, 52],
            'census_validation': ['Confirmed', 'Confirmed', 'Confirmed', 'Partial', 'Confirmed'],
            'academic_support': ['Fed Reserve', 'IEEE standards', 'MIT research', 'NIST framework', 'Goldman Sachs']
        })
        
        fig = px.bar(
            barriers_with_sources,
            x='oecd_percentage',
            y='barrier',
            orientation='h',
            color='oecd_percentage',
            color_continuous_scale='Reds',
            title='Implementation Barriers: Multi-Source Validation',
            text='academic_support'
        )
        fig.update_layout(height=350)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Evidence-based action framework
        st.markdown("### 📋 Multi-Source Action Framework")
        if 'market_pressure' in locals():
            if market_pressure >= 70:
                st.error("""
                **HIGH-ADOPTION INDUSTRY ACTION PLAN**
                *Based on Federal Reserve, NIST, and academic research*
                
                **Immediate (30 days) - Federal Reserve Priority:**
                • Conduct productivity gap analysis using Bick-Blandin methodology
                • Implement NIST AI RMF governance framework basics
                • Address #1 barrier: acquire AI talent (68% cite this - OECD data)
                
                **Near-term (60-90 days) - Academic Best Practices:**
                • Deploy GenAI in customer service (Brynjolfsson +14% validated)
                • Focus on task-level acceleration (47-56% of tasks - Fed research)
                • Implement IEEE data quality standards (2671-2021)
                
                **Medium-term (3-6 months) - Government Framework:**
                • Scale using NSF research institute collaboration model
                • Full NIST framework implementation for enterprise readiness
                • FDA pathway planning if healthcare applications involved
                
                **Research Validation:** Your industry's 80%+ adoption creates urgent 
                competitive pressure documented in multiple Federal Reserve working papers.
                """)
            elif market_pressure >= 40:
                st.warning("""
                **GROWTH-PHASE INDUSTRY ACTION PLAN**
                *Based on NBER, MIT, and institutional research*
                
                **Foundation (Month 1) - NIST Framework:**
                • Establish AI governance using NIST AI RMF 1.0 guidelines
                • Baseline productivity measurement (Federal Reserve methodology)
                • IEEE standards assessment for data quality (2671-2021)
                
                **Pilot (Months 2-3) - Academic Best Practices:**
                • Launch customer service AI pilot (Brynjolfsson validated +14%)
                • Target task acceleration opportunities (MIT 15% faster completion)
                • Implement full-stack approach for 2.2x productivity (Fed research)
                
                **Scale (Months 4-6) - Multi-Source Integration:**
                • Expand using NSF research institute collaboration model
                • Apply Goldman Sachs investment framework for scaling
                • Monitor using Federal Reserve productivity metrics
                
                **Research Validation:** Growth-phase industries show optimal 
                implementation windows according to Acemoglu (2024) economic modeling.
                """)
            else:
                st.info("""
                **EARLY-STAGE INDUSTRY ACTION PLAN**
                *Based on comprehensive academic and government research*
                
                **Strategic Planning (Months 1-3) - Academic Foundation:**
                • Apply MIT economic modeling for ROI projections (Acemoglu framework)
                • Use NIST guidelines for comprehensive risk assessment
                • Leverage NSF research institute partnerships for capability building
                
                **Capability Building (Months 4-9) - Technical Standards:**
                • Implement IEEE technical standards from ground up
                • Focus on data infrastructure (consistently cited in Nature MI)
                • Build talent pipeline using NSF collaboration model
                
                **Market Leadership (Months 10-18) - Integrated Approach:**
                • Deploy advanced applications using federal research insights
                • Establish competitive moats using Goldman Sachs strategic framework
                • Scale using validated Federal Reserve productivity patterns
                
                **Research Validation:** Early-stage industries have first-mover 
                advantages documented in multiple academic economic analyses.
                """)
        else:
            st.info("Market pressure not available. Action framework cannot be generated.")

        # Download multi-source action framework
        if 'market_pressure' in locals() and st.button("📥 Download Multi-Source Action Framework", use_container_width=True):
            framework_content = f"""
            # Multi-Source Evidence-Based AI Action Framework
            
            **Generated:** {datetime.now().strftime('%Y-%m-%d')}
            **Research Foundation:** 25+ authoritative sources across government, academic, and industry research
            
            ## Your Competitive Context
            - Industry: {industry_selection}
            - Company Size: {company_size_selection}
            - Market Pressure: {market_pressure:.0f}/100 (Multi-source analysis)
            
            ## Research Synthesis
            **Federal Reserve Research:**
            - 15% worker productivity improvement with AI access
            - 47-56% of tasks can be enhanced by AI capabilities
            - 0.4% aggregate productivity gain potential
            
            **MIT Economic Analysis:**
            - +0.66% total factor productivity over 10 years
            - 15% of tasks can be completed significantly faster
            - Conservative but validated macroeconomic modeling
            
            **NBER Studies:**
            - +14% productivity in customer service (real-world trials)
            - Largest benefits for less-experienced workers
            - Learning effects increase productivity over time
            
            **Government Framework (NIST/NSF):**
            - NIST AI RMF 1.0: 240+ organization collaborative framework
            - NSF Research Institutes: $220M investment, proven collaboration model
            - FDA guidance: Clear regulatory pathways for AI applications
            
            ## Evidence-Based Recommendations
            [Specific recommendations based on market pressure level]
            
            ## Complete Source List
            **Government Sources:**
            - Stanford AI Index Report 2025
            - U.S. Census Bureau AI Use Supplement
            - NIST AI Risk Management Framework
            - NSF National AI Research Institutes
            - OECD AI Policy Observatory
            
            **Academic Research:**
            - Federal Reserve working papers (Bick, Blandin, Deming)
            - MIT Economics (Acemoglu)
            - NBER studies (Brynjolfsson et al.)
            - Nature publications (AlphaFold research)
            - Multiple peer-reviewed papers
            
            **Industry Analysis:**
            - McKinsey Global Survey (1,491 organizations)
            - Goldman Sachs economic research
            - BCG/INSEAD enterprise studies
            - Technology company primary sources
            
            **Technical Standards:**
            - IEEE Computer Society standards
            - Nature Machine Intelligence research
            - MIT Technology Review analysis
            - Gartner technology maturity models
            
            ## Validation Methodology
            - Cross-referenced findings across multiple independent sources
            - Prioritized peer-reviewed and government research
            - Validated industry patterns against academic studies
            - Synthesized recommendations based on convergent evidence
            """
            
            st.download_button(
                label="Download Framework",
                data=framework_content,
                file_name=f"Multi_Source_AI_Framework_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
        elif 'market_pressure' not in locals():
            st.info("Market pressure not available. Download not available.")
    elif current_view == "AI Cost Trends":
        st.write("💸 **AI Cost Revolution: 2022-2024**")
        
        if not safe_data_check(ai_cost_reduction, "AI cost trends data"):
            st.stop()
        
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
            x=ai_cost_reduction['model'],
            y=ai_cost_reduction['cost_per_million_tokens'],
            mode='lines+markers',
            name='Cost per Million Tokens',
            line=dict(width=4, color='#E74C3C'),
            marker=dict(size=12),
            text=[f'${x:.2f}' for x in ai_cost_reduction['cost_per_million_tokens']],
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
        
        # Cost impact analysis
        col1, col2 = st.columns(2)
        with col1:
            st.write("**💰 Cost Impact Analysis:**")
            st.write("• **Barrier elimination**: Cost no longer limits adoption")
            st.write("• **SME accessibility**: Small businesses can afford AI")
            st.write("• **Scale economics**: Volume processing becomes viable")
            st.write("• **Innovation acceleration**: Lower costs enable experimentation")
            st.write("• **Competitive pressure**: Cost advantages erode")
        
        with col2:
            st.write("**📊 Business Implications:**")
            st.write("• **ROI improvement**: Lower costs increase returns")
            st.write("• **Use case expansion**: More applications become viable")
            st.write("• **Market democratization**: AI accessible to all")
            st.write("• **Talent focus**: Skills become the limiting factor")
            st.write("• **Quality emphasis**: Cost advantage shifts to quality")
        
        # Download cost data
        csv = ai_cost_reduction.to_csv(index=False)
        st.download_button(
            label="📥 Download Cost Data (CSV)",
            data=csv,
            file_name="ai_cost_trends.csv",
            mime="text/csv"
        )
    elif current_view == "Token Economics":
        st.write("🪙 **AI Token Economics Analysis**")
        
        if not safe_data_check(token_economics, "Token economics data"):
            st.stop()
        
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
            x=token_economics['model'],
            y=token_economics['cost_per_million_input'],
            name='Input Cost',
            marker_color='#3498DB',
            text=[f'${x:.2f}' for x in token_economics['cost_per_million_input']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            x=token_economics['model'],
            y=token_economics['cost_per_million_output'],
            name='Output Cost',
            marker_color='#E74C3C',
            text=[f'${x:.2f}' for x in token_economics['cost_per_million_output']],
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
        
        # Token usage patterns
        if token_usage_patterns is not None:
            st.subheader("Token Usage Patterns")
            fig2 = px.scatter(
                token_usage_patterns,
                x='avg_input_tokens',
                y='avg_output_tokens',
                size='input_output_ratio',
                color='use_case',
                title='Token Usage by Use Case',
                labels={
                    'avg_input_tokens': 'Average Input Tokens',
                    'avg_output_tokens': 'Average Output Tokens',
                    'input_output_ratio': 'Input/Output Ratio'
                },
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Download token data
        csv = token_economics.to_csv(index=False)
        st.download_button(
            label="📥 Download Token Economics Data (CSV)",
            data=csv,
            file_name="token_economics.csv",
            mime="text/csv"
        )
    elif current_view == "Financial Impact":
        st.write("💰 **AI Financial Impact by Business Function**")
        
        if not safe_data_check(financial_impact, "Financial impact data"):
            st.stop()
        
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
            x=financial_impact['function'],
            y=financial_impact['companies_reporting_cost_savings'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in financial_impact['companies_reporting_cost_savings']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Companies Reporting Revenue Gains',
            x=financial_impact['function'],
            y=financial_impact['companies_reporting_revenue_gains'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in financial_impact['companies_reporting_revenue_gains']],
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
        
        # ROI analysis by function
        st.subheader("ROI Analysis by Business Function")
        roi_data = financial_impact.copy()
        roi_data['roi_score'] = (roi_data['avg_revenue_increase'] + roi_data['avg_cost_reduction']) / 2
        roi_data = roi_data.sort_values('roi_score', ascending=False)
        
        fig2 = px.bar(
            roi_data,
            x='function',
            y='roi_score',
            color='roi_score',
            color_continuous_scale='RdYlGn',
            title='ROI Score by Business Function',
            labels={'roi_score': 'ROI Score (%)', 'function': 'Business Function'},
            height=400
        )
        fig2.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Download financial data
        csv = financial_impact.to_csv(index=False)
        st.download_button(
            label="📥 Download Financial Impact Data (CSV)",
            data=csv,
            file_name="ai_financial_impact.csv",
            mime="text/csv"
        )
    elif current_view == "Labor Impact":
        st.write("👥 **AI Labor Market Impact**")
        
        if not safe_data_check(ai_perception, "Labor impact data"):
            st.stop()
        
        # Labor impact overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Job Change Expectation", "67%", "Gen Z")
        with col2:
            st.metric("Job Replacement Fear", "42%", "Gen Z")
        with col3:
            st.metric("Millennial Concern", "65%", "Job change expected")
        with col4:
            st.metric("Boomer Concern", "49%", "Job change expected")
        
        # Generational perception chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Expect Job Change',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_change'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in ai_perception['expect_job_change']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Expect Job Replacement',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_replacement'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in ai_perception['expect_job_replacement']],
            textposition='outside'
        ))
        fig.update_layout(
            title="AI Labor Market Impact by Generation",
            xaxis_title="Generation",
            yaxis_title="Percentage",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Labor market insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**📊 Labor Market Trends:**")
            st.write("• **Generational divide**: Younger workers more concerned")
            st.write("• **Skill evolution**: New AI-related roles emerging")
            st.write("• **Productivity gains**: AI augments human capabilities")
            st.write("• **Job transformation**: Roles evolve rather than disappear")
            st.write("• **Upskilling imperative**: Continuous learning required")
        
        with col2:
            st.write("**🎯 Strategic Implications:**")
            st.write("• **Talent retention**: Address AI concerns proactively")
            st.write("• **Skills development**: Invest in AI literacy programs")
            st.write("• **Change management**: Support workforce transitions")
            st.write("• **Job redesign**: Focus on human-AI collaboration")
            st.write("• **Competitive advantage**: AI-savvy workforce")
        
        # Download labor data
        csv = ai_perception.to_csv(index=False)
        st.download_button(
            label="📥 Download Labor Impact Data (CSV)",
            data=csv,
            file_name="ai_labor_impact.csv",
            mime="text/csv"
        )
    elif current_view == "Firm Size Analysis":
        st.write("🏢 **AI Adoption by Firm Size**")
        
        if not safe_data_check(firm_size, "Firm size data"):
            st.stop()
        
        # Firm size overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Largest Firms", "58.5%", "5000+ employees")
        with col2:
            st.metric("Smallest Firms", "3.2%", "1-4 employees")
        with col3:
            st.metric("Adoption Gap", "55.3pp", "Large vs small")
        with col4:
            st.metric("Mid-size Firms", "25.6%", "500-999 employees")
        
        # Firm size adoption chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=firm_size['size'],
            y=firm_size['adoption'],
            marker_color=firm_size['adoption'],
            colorscale='RdYlGn',
            text=[f'{x}%' for x in firm_size['adoption']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Adoption: %{y}%<extra></extra>'
        ))
        fig.update_layout(
            title="AI Adoption by Firm Size",
            xaxis_title="Number of Employees",
            yaxis_title="AI Adoption Rate (%)",
            height=500,
            coloraxis_showscale=True,
            coloraxis_colorbar=dict(title="Adoption Rate (%)")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Size-based insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**📊 Size-Based Patterns:**")
            st.write("• **Resource advantage**: Larger firms have more resources")
            st.write("• **Scale benefits**: Bigger companies see better ROI")
            st.write("• **Talent access**: Large firms attract AI specialists")
            st.write("• **Risk tolerance**: Bigger budgets for experimentation")
            st.write("• **Infrastructure**: Existing tech stack advantage")
        
        with col2:
            st.write("**🎯 Strategic Implications:**")
            st.write("• **SME opportunity**: Significant growth potential")
            st.write("• **Partnership models**: Cloud and AI-as-a-service")
            st.write("• **Cost barriers**: Lower costs help smaller firms")
            st.write("• **Talent strategies**: Different approaches needed")
            st.write("• **Competitive dynamics**: Size advantage eroding")
        
        # Download firm size data
        csv = firm_size.to_csv(index=False)
        st.download_button(
            label="📥 Download Firm Size Data (CSV)",
            data=csv,
            file_name="ai_adoption_by_firm_size.csv",
            mime="text/csv"
        )
    elif current_view == "Technology Stack":
        st.write("🛠️ **AI Technology Stack Analysis**")
        
        if not safe_data_check(tech_stack, "Technology stack data"):
            st.stop()
        
        # Technology stack overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Full Stack", "38%", "AI+Cloud+Digital")
        with col2:
            st.metric("AI + Digitization", "24%", "Partial integration")
        with col3:
            st.metric("AI + Cloud", "23%", "Cloud-based AI")
        with col4:
            st.metric("AI Only", "15%", "Standalone AI")
        
        # Technology stack pie chart
        fig = px.pie(
            tech_stack,
            values='percentage',
            names='technology',
            title='AI Technology Stack Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Stack effectiveness analysis
        st.subheader("Technology Stack Effectiveness")
        
        # Create effectiveness data (based on research)
        effectiveness_data = pd.DataFrame({
            'stack_type': ['AI + Cloud + Digitization', 'AI + Cloud', 'AI + Digitization', 'AI Only'],
            'roi_multiplier': [3.5, 2.9, 2.6, 1.7],
            'success_rate': [82, 68, 62, 45],
            'implementation_time': [18, 12, 15, 8]  # months
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.bar(
                effectiveness_data,
                x='stack_type',
                y='roi_multiplier',
                color='roi_multiplier',
                color_continuous_scale='RdYlGn',
                title='ROI by Technology Stack',
                labels={'roi_multiplier': 'ROI Multiplier', 'stack_type': 'Stack Type'},
                height=400
            )
            fig2.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            fig3 = px.scatter(
                effectiveness_data,
                x='implementation_time',
                y='roi_multiplier',
                size='success_rate',
                color='stack_type',
                title='Implementation Time vs ROI',
                labels={
                    'implementation_time': 'Implementation Time (months)',
                    'roi_multiplier': 'ROI Multiplier',
                    'success_rate': 'Success Rate (%)'
                },
                height=400
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Download technology stack data
        csv = tech_stack.to_csv(index=False)
        st.download_button(
            label="📥 Download Technology Stack Data (CSV)",
            data=csv,
            file_name="ai_technology_stack.csv",
            mime="text/csv"
        )
    elif current_view == "AI Technology Maturity":
        st.write("🔬 **AI Technology Maturity Analysis**")
        
        if not safe_data_check(ai_maturity, "AI technology maturity data"):
            st.stop()
        
        # Maturity overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Most Mature", "Cloud AI Services", "78% adoption")
        with col2:
            st.metric("Highest Risk", "AI Agents", "90% risk score")
        with col3:
            st.metric("Fastest Value", "Cloud AI", "1 month")
        with col4:
            st.metric("Slowest Value", "Composite AI", "7 months")
        
        # Technology maturity chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ai_maturity['adoption_rate'],
            y=ai_maturity['risk_score'],
            mode='markers+text',
            marker=dict(
                size=ai_maturity['time_to_value'] * 10,
                color=ai_maturity['adoption_rate'],
                colorscale='RdYlGn',
                colorbar=dict(title="Adoption Rate (%)")
            ),
            text=ai_maturity['technology'],
            textposition='middle center',
            textfont=dict(size=10, color='white'),
            hovertemplate='<b>%{text}</b><br>Adoption: %{x}%<br>Risk: %{y}%<br>Time to Value: %{marker.size/10} months<extra></extra>'
        ))
        fig.update_layout(
            title="AI Technology Maturity Matrix",
            xaxis_title="Adoption Rate (%)",
            yaxis_title="Risk Score (%)",
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Maturity insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🔬 Maturity Insights:**")
            st.write("• **Cloud AI Services**: Most mature and lowest risk")
            st.write("• **Generative AI**: High adoption but moderate risk")
            st.write("• **AI Agents**: High risk but emerging potential")
            st.write("• **Foundation Models**: Moderate adoption, high complexity")
            st.write("• **Composite AI**: Early stage, high potential")
        
        with col2:
            st.write("**🎯 Strategic Recommendations:**")
            st.write("• **Start with Cloud AI**: Low risk, proven value")
            st.write("• **Gradual GenAI adoption**: Build on cloud foundation")
            st.write("• **Monitor AI Agents**: High risk but future potential")
            st.write("• **Invest in skills**: Foundation models require expertise")
            st.write("• **Plan for composite AI**: Future integration strategy")
        
        # Download maturity data
        csv = ai_maturity.to_csv(index=False)
        st.download_button(
            label="📥 Download Technology Maturity Data (CSV)",
            data=csv,
            file_name="ai_technology_maturity.csv",
            mime="text/csv"
        )
    elif current_view == "Productivity Research":
        st.write("📈 **AI Productivity Research Analysis**")
        
        if not safe_data_check(productivity_data, "Productivity research data"):
            st.stop()
        
        # Productivity overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Growth", "0.4%", "2025 productivity")
        with col2:
            st.metric("Peak Growth", "2.5%", "2000 productivity")
        with col3:
            st.metric("AI Impact", "14%", "Customer service gains")
        with col4:
            st.metric("Skill Gap Reduction", "28%", "Low-skilled workers")
        
        # Historical productivity trends
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=productivity_data['year'],
            y=productivity_data['productivity_growth'],
            mode='lines+markers',
            name='Productivity Growth',
            line=dict(width=4, color='#3498DB'),
            marker=dict(size=8),
            fill='tonexty',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=productivity_data['year'],
            y=productivity_data['young_workers_share'],
            mode='lines+markers',
            name='Young Workers Share',
            line=dict(width=4, color='#E74C3C'),
            marker=dict(size=8),
            yaxis='y2'
        ))
        fig.update_layout(
            title="Productivity Growth Trends: 1980-2025",
            xaxis_title="Year",
            yaxis=dict(title="Productivity Growth (%)", side="left"),
            yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI productivity by skill level
        if productivity_by_skill is not None:
            st.subheader("AI Productivity Impact by Skill Level")
            fig2 = px.bar(
                productivity_by_skill,
                x='skill_level',
                y=['productivity_gain', 'skill_gap_reduction'],
                title='AI Productivity Gains by Skill Level',
                barmode='group',
                labels={'value': 'Percentage (%)', 'variable': 'Impact Type'},
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Research insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**📊 Research Findings:**")
            st.write("• **Productivity decline**: Growth slowed since 2000")
            st.write("• **AI acceleration**: Recent productivity gains")
            st.write("• **Skill level impact**: Lower-skilled workers benefit most")
            st.write("• **Customer service**: 14% productivity improvement")
            st.write("• **Learning effects**: Gains increase with use")
        
        with col2:
            st.write("**🎯 Strategic Implications:**")
            st.write("• **Target low-skilled roles**: Highest ROI potential")
            st.write("• **Focus on customer service**: Proven productivity gains")
            st.write("• **Invest in training**: Learning effects matter")
            st.write("• **Monitor productivity**: Track AI impact")
            st.write("• **Skill development**: Balance automation and upskilling")
        
        # Download productivity data
        csv = productivity_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Productivity Research Data (CSV)",
            data=csv,
            file_name="ai_productivity_research.csv",
            mime="text/csv"
        )
    elif current_view == "Environmental Impact":
        st.write("🌱 **AI Environmental Impact Analysis**")
        
        # Environmental impact overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Training Emissions", "552 metric tons", "GPT-3 equivalent")
        with col2:
            st.metric("Inference Energy", "High", "Per query cost")
        with col3:
            st.metric("Efficiency Gains", "15-30%", "Energy optimization")
        with col4:
            st.metric("Carbon Offset", "Potential", "Through optimization")
        
        # Create environmental impact data
        env_data = pd.DataFrame({
            'model': ['GPT-3', 'GPT-4', 'Claude 3', 'Gemini', 'Llama 3'],
            'training_emissions': [552, 850, 420, 380, 280],  # metric tons CO2
            'inference_efficiency': [1.0, 0.8, 1.2, 1.1, 1.3],  # relative efficiency
            'energy_optimization': [15, 25, 30, 20, 35]  # % improvement
        })
        
        # Environmental impact visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Training Emissions',
            x=env_data['model'],
            y=env_data['training_emissions'],
            marker_color='#E74C3C',
            text=[f'{x} tons' for x in env_data['training_emissions']],
            textposition='outside'
        ))
        fig.add_trace(go.Scatter(
            name='Energy Optimization',
            x=env_data['model'],
            y=env_data['energy_optimization'],
            mode='lines+markers',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            yaxis='y2',
            text=[f'{x}%' for x in env_data['energy_optimization']],
            textposition='top center'
        ))
        fig.update_layout(
            title="AI Environmental Impact: Training Emissions vs Energy Optimization",
            xaxis_title="AI Model",
            yaxis=dict(title="Training Emissions (metric tons CO2)", side="left"),
            yaxis2=dict(title="Energy Optimization (%)", side="right", overlaying="y"),
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Environmental insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🌱 Environmental Challenges:**")
            st.write("• **High training costs**: Large models require significant energy")
            st.write("• **Inference energy**: Each query consumes power")
            st.write("• **Data center growth**: AI infrastructure expansion")
            st.write("• **Carbon footprint**: Training emissions significant")
            st.write("• **Resource intensity**: Water and energy consumption")
        
        with col2:
            st.write("**♻️ Environmental Opportunities:**")
            st.write("• **Energy optimization**: AI can reduce energy waste")
            st.write("• **Smart grids**: AI improves energy distribution")
            st.write("• **Climate modeling**: Better environmental predictions")
            st.write("• **Efficiency gains**: Process optimization reduces waste")
            st.write("• **Renewable integration**: AI manages renewable energy")
        
        # Download environmental data
        csv = env_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Environmental Impact Data (CSV)",
            data=csv,
            file_name="ai_environmental_impact.csv",
            mime="text/csv"
        )
    elif current_view == "Geographic Distribution":
        st.write("🗺️ **Geographic Distribution of AI Adoption**")
        
        if not safe_data_check(geographic, "Geographic data"):
            st.stop()
        
        # Geographic overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top City", "San Francisco", "9.5% adoption")
        with col2:
            st.metric("Top State", "California", "Multiple hubs")
        with col3:
            st.metric("Population Weighted", "7.2%", "National average")
        with col4:
            st.metric("Geographic Spread", "20 cities", "Major metros")
        
        # US geographic distribution map
        fig = px.scatter_mapbox(
            geographic,
            lat='lat',
            lon='lon',
            size='rate',
            color='rate',
            hover_name='city',
            hover_data=['state', 'population_millions', 'gdp_billions'],
            color_continuous_scale='Viridis',
            size_max=25,
            zoom=3,
            title='AI Adoption by US Metropolitan Areas'
        )
        fig.update_layout(
            mapbox_style='carto-positron',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # State-level analysis
        if state_data is not None:
            st.subheader("State-Level AI Adoption")
            fig2 = px.bar(
                state_data,
                x='state_code',
                y='rate',
                color='rate',
                color_continuous_scale='RdYlGn',
                title='AI Adoption by State',
                labels={'rate': 'Adoption Rate (%)', 'state_code': 'State'},
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Geographic insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🗺️ Geographic Patterns:**")
            st.write("• **Tech hubs**: San Francisco, Seattle, Boston lead")
            st.write("• **Coastal concentration**: East and West coasts dominate")
            st.write("• **University cities**: Strong correlation with research")
            st.write("• **Economic centers**: GDP correlates with adoption")
            st.write("• **Population density**: Urban areas show higher adoption")
        
        with col2:
            st.write("**🎯 Strategic Implications:**")
            st.write("• **Talent clustering**: AI skills concentrated in hubs")
            st.write("• **Regional development**: Opportunity for emerging markets")
            st.write("• **Remote work**: Technology enables geographic dispersion")
            st.write("• **Investment patterns**: Follow talent and infrastructure")
            st.write("• **Policy focus**: Regional AI development strategies")
        
        # Download geographic data
        csv = geographic.to_csv(index=False)
        st.download_button(
            label="📥 Download Geographic Data (CSV)",
            data=csv,
            file_name="ai_geographic_distribution.csv",
            mime="text/csv"
        )
    elif current_view == "OECD 2025 Findings":
        st.write("🏛️ **OECD 2025 AI Adoption Findings**")
        
        if not safe_data_check(oecd_g7_adoption, "OECD G7 data"):
            st.stop()
        
        # OECD overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Japan Leads", "48%", "G7 adoption rate")
        with col2:
            st.metric("US Position", "45%", "G7 adoption rate")
        with col3:
            st.metric("Manufacturing", "52%", "Japan manufacturing")
        with col4:
            st.metric("ICT Sector", "70%", "Japan ICT adoption")
        
        # G7 adoption comparison
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Overall Adoption',
            x=oecd_g7_adoption['country'],
            y=oecd_g7_adoption['adoption_rate'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in oecd_g7_adoption['adoption_rate']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Manufacturing',
            x=oecd_g7_adoption['country'],
            y=oecd_g7_adoption['manufacturing'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in oecd_g7_adoption['manufacturing']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='ICT Sector',
            x=oecd_g7_adoption['country'],
            y=oecd_g7_adoption['ict_sector'],
            marker_color='#2ECC71',
            text=[f'{x}%' for x in oecd_g7_adoption['ict_sector']],
            textposition='outside'
        ))
        fig.update_layout(
            title="OECD G7 AI Adoption by Sector",
            xaxis_title="Country",
            yaxis_title="Adoption Rate (%)",
            barmode='group',
            height=500,
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # OECD applications analysis
        if oecd_applications is not None:
            st.subheader("OECD AI Applications Analysis")
            fig2 = px.bar(
                oecd_applications,
                x='usage_rate',
                y='application',
                color='category',
                orientation='h',
                title='AI Applications Usage Rates',
                labels={'usage_rate': 'Usage Rate (%)', 'application': 'Application'},
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # OECD insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🏛️ OECD Key Findings:**")
            st.write("• **Japan leadership**: Highest adoption across sectors")
            st.write("• **Manufacturing focus**: Strong industrial AI adoption")
            st.write("• **ICT advantage**: Technology sector leads adoption")
            st.write("• **G7 variation**: Significant differences between countries")
            st.write("• **Sector patterns**: Manufacturing and ICT lead")
        
        with col2:
            st.write("**🎯 Policy Implications:**")
            st.write("• **International coordination**: G7 collaboration needed")
            st.write("• **Sector-specific policies**: Manufacturing focus")
            st.write("• **Digital infrastructure**: ICT sector development")
            st.write("• **Skills development**: Cross-country learning")
            st.write("• **Regulatory alignment**: Harmonized AI policies")
        
        # Download OECD data
        csv = oecd_g7_adoption.to_csv(index=False)
        st.download_button(
            label="📥 Download OECD Data (CSV)",
            data=csv,
            file_name="oecd_2025_findings.csv",
            mime="text/csv"
        )
    elif current_view == "Barriers & Support":
        st.write("🚧 **AI Adoption Barriers & Support Effectiveness**")
        
        if not safe_data_check(barriers_data, "Barriers and support data"):
            st.stop()
        
        # Barriers overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top Barrier", "68%", "Lack of skilled personnel")
        with col2:
            st.metric("Data Issues", "62%", "Availability/quality")
        with col3:
            st.metric("Integration", "58%", "Legacy systems")
        with col4:
            st.metric("Regulatory", "55%", "Uncertainty")
        
        # Barriers visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=barriers_data['barrier'],
            y=barriers_data['percentage'],
            marker_color=barriers_data['percentage'],
            colorscale='Reds',
            text=[f'{x}%' for x in barriers_data['percentage']],
            textposition='outside'
        ))
        fig.update_layout(
            title="AI Adoption Barriers",
            xaxis_title="Barrier",
            yaxis_title="Percentage of Companies",
            height=500,
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Support effectiveness
        if support_effectiveness is not None:
            st.subheader("Support Effectiveness")
            fig2 = px.bar(
                support_effectiveness,
                x='effectiveness_score',
                y='support_type',
                orientation='h',
                color='effectiveness_score',
                color_continuous_scale='Greens',
                title='Support Effectiveness Scores',
                labels={'effectiveness_score': 'Effectiveness Score', 'support_type': 'Support Type'},
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Barriers and support insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🚧 Key Barriers:**")
            st.write("• **Skills shortage**: 68% cite lack of skilled personnel")
            st.write("• **Data challenges**: 62% face data quality issues")
            st.write("• **Integration complexity**: 58% struggle with legacy systems")
            st.write("• **Regulatory uncertainty**: 55% concerned about compliance")
            st.write("• **Cost concerns**: 52% cite high implementation costs")
        
        with col2:
            st.write("**🎯 Effective Support:**")
            st.write("• **Government education**: 82% effectiveness score")
            st.write("• **University partnerships**: 78% effectiveness score")
            st.write("• **Public-private collaboration**: 75% effectiveness score")
            st.write("• **Regulatory clarity**: 73% effectiveness score")
            st.write("• **Tax incentives**: 68% effectiveness score")
        
        # Download barriers data
        csv = barriers_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Barriers Data (CSV)",
            data=csv,
            file_name="ai_adoption_barriers.csv",
            mime="text/csv"
        )
    elif current_view == "ROI Analysis":
        st.write("💰 **AI Return on Investment Analysis**")
        
        if not safe_data_check(sector_2025, "ROI analysis data"):
            st.stop()
        
        # ROI overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Highest ROI", "4.2x", "Technology sector")
        with col2:
            st.metric("Average ROI", "3.1x", "Across sectors")
        with col3:
            st.metric("Lowest ROI", "2.2x", "Government sector")
        with col4:
            st.metric("ROI Range", "2.0x", "Technology to Government")
        
        # ROI by sector
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=sector_2025['sector'],
            y=sector_2025['avg_roi'],
            marker_color=sector_2025['avg_roi'],
            colorscale='RdYlGn',
            text=[f'{x}x' for x in sector_2025['avg_roi']],
            textposition='outside'
        ))
        fig.update_layout(
            title="AI ROI by Industry Sector",
            xaxis_title="Sector",
            yaxis_title="Average ROI (x)",
            height=500,
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ROI vs adoption correlation
        fig2 = px.scatter(
            sector_2025,
            x='adoption_rate',
            y='avg_roi',
            size='genai_adoption',
            color='sector',
            title='ROI vs Adoption Rate Correlation',
            labels={
                'adoption_rate': 'AI Adoption Rate (%)',
                'avg_roi': 'Average ROI (x)',
                'genai_adoption': 'GenAI Adoption (%)'
            },
            height=400
        )
        
        # Add correlation line
        import numpy as np
        z = np.polyfit(sector_2025['adoption_rate'], sector_2025['avg_roi'], 1)
        p = np.poly1d(z)
        fig2.add_trace(go.Scatter(
            x=sector_2025['adoption_rate'],
            y=p(sector_2025['adoption_rate']),
            mode='lines',
            name='Trend Line',
            line=dict(dash='dash', color='gray')
        ))
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # ROI insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**💰 ROI Patterns:**")
            st.write("• **Technology leads**: 4.2x ROI in tech sector")
            st.write("• **Financial services**: 3.8x ROI with high adoption")
            st.write("• **Manufacturing**: 3.5x ROI, strong industrial focus")
            st.write("• **Government lag**: 2.2x ROI, regulatory constraints")
            st.write("• **Correlation**: Higher adoption generally means higher ROI")
        
        with col2:
            st.write("**🎯 Investment Strategy:**")
            st.write("• **Sector targeting**: Focus on high-ROI sectors")
            st.write("• **Adoption acceleration**: Speed drives ROI")
            st.write("• **GenAI focus**: Higher adoption correlates with ROI")
            st.write("• **Government opportunity**: Lower ROI but strategic value")
            st.write("• **Risk assessment**: Balance ROI with implementation risk")
        
        # Download ROI data
        csv = sector_2025.to_csv(index=False)
        st.download_button(
            label="📥 Download ROI Analysis Data (CSV)",
            data=csv,
            file_name="ai_roi_analysis.csv",
            mime="text/csv"
        )
    elif current_view == "Skill Gap Analysis":
        st.write("🎓 **AI Skills Gap Analysis**")
        
        if not safe_data_check(skill_gap_data, "Skill gap data"):
            st.stop()
        
        # Skill gap overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Highest Gap", "85%", "AI/ML Engineering")
        with col2:
            st.metric("Data Science", "78%", "Gap severity")
        with col3:
            st.metric("AI Ethics", "72%", "Gap severity")
        with col4:
            st.metric("Training Coverage", "45%", "AI/ML Engineering")
        
        # Skills gap visualization
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Gap Severity',
            x=skill_gap_data['skill'],
            y=skill_gap_data['gap_severity'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in skill_gap_data['gap_severity']],
            textposition='outside'
        ))
        fig.add_trace(go.Bar(
            name='Training Initiatives',
            x=skill_gap_data['skill'],
            y=skill_gap_data['training_initiatives'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in skill_gap_data['training_initiatives']],
            textposition='outside'
        ))
        fig.update_layout(
            title="AI Skills Gap vs Training Coverage",
            xaxis_title="Skill Area",
            yaxis_title="Percentage",
            barmode='group',
            height=500,
            xaxis_tickangle=45
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis insights
        col1, col2 = st.columns(2)
        with col1:
            st.write("**🎓 Skills Gap Analysis:**")
            st.write("• **AI/ML Engineering**: 85% gap, highest demand")
            st.write("• **Data Science**: 78% gap, foundational skill")
            st.write("• **AI Ethics**: 72% gap, emerging importance")
            st.write("• **Prompt Engineering**: 68% gap, GenAI specific")
            st.write("• **AI Product Management**: 65% gap, strategic role")
        
        with col2:
            st.write("**🎯 Training Priorities:**")
            st.write("• **Focus on engineering**: Highest gap, highest need")
            st.write("• **Data science foundation**: Core AI competency")
            st.write("• **Ethics training**: Critical for responsible AI")
            st.write("• **Prompt engineering**: GenAI-specific skills")
            st.write("• **Product management**: Bridge technical and business")
        
        # Skills development recommendations
        st.subheader("Skills Development Recommendations")
        
        recommendations_data = pd.DataFrame({
            'skill': ['AI/ML Engineering', 'Data Science', 'AI Ethics', 'Prompt Engineering'],
            'priority': ['Critical', 'High', 'High', 'Medium'],
            'training_time': ['6-12 months', '3-6 months', '1-3 months', '1-2 months'],
            'investment_level': ['High', 'Medium', 'Medium', 'Low']
        })
        
        st.dataframe(recommendations_data, hide_index=True, use_container_width=True)
        
        # Download skill gap data
        csv = skill_gap_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Skill Gap Data (CSV)",
            data=csv,
            file_name="ai_skill_gap_analysis.csv",
            mime="text/csv"
        )
    elif current_view == "AI Governance":
        st.write("⚖️ **AI Governance & Ethics Implementation**")
        
        if not safe_data_check(ai_governance, "AI governance data"):
            st.stop()
        
        # Governance overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Data Privacy", "78%", "Highest adoption")
        with col2:
            st.metric("Regulatory Compliance", "72%", "Strong compliance")
        with col3:
            st.metric("Ethics Guidelines", "62%", "Growing adoption")
        with col4:
            st.metric("Avg Maturity", "3.1/5", "Moderate maturity")
        
        # Governance radar chart
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
        
        # Governance analysis
        col1, col2 = st.columns(2)
        with col1:
            st.write("✅ **Well-Established Areas:**")
            st.write("• **Data Privacy:** 78% adoption, 3.8/5 maturity")
            st.write("• **Regulatory Compliance:** 72% adoption, 3.5/5 maturity")
            st.write("• **Ethics Guidelines:** 62% adoption, 3.2/5 maturity")
            st.write("• **Risk Assessment:** 55% adoption, 3.0/5 maturity")
            
            st.success("""
            **Strong Foundation:** Organizations are building solid 
            governance foundations, particularly in data privacy and 
            regulatory compliance areas.
            """)
        
        with col2:
            st.write("⚠️ **Areas Needing Attention:**")
            st.write("• **Bias Detection:** Only 45% adoption, 2.5/5 maturity")
            st.write("• **Accountability Framework:** 48% adoption, 2.6/5 maturity")
            st.write("• **Transparency:** 52% adoption, 2.8/5 maturity")
            
            st.warning("""
            **Development Needed:** Technical governance areas like 
            bias detection and transparency need more focus and investment.
            """)
        
        # Governance maturity analysis
        st.subheader("Governance Maturity Analysis")
        fig2 = px.scatter(
            ai_governance,
            x='adoption_rate',
            y='maturity_score',
            size='adoption_rate',
            color='aspect',
            title='Governance Maturity vs Adoption Rate',
            labels={
                'adoption_rate': 'Adoption Rate (%)',
                'maturity_score': 'Maturity Score (1-5)',
                'aspect': 'Governance Aspect'
            },
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Download governance data
        csv = ai_governance.to_csv(index=False)
        st.download_button(
            label="📥 Download AI Governance Data (CSV)",
            data=csv,
            file_name="ai_governance_analysis.csv",
            mime="text/csv"
        )
    else:
        st.error(f"View '{current_view}' is not fully implemented yet.")
        st.info("Please select a different view from the sidebar.")
        
        # Show available views
        st.write("**Available detailed views:**")
        for view in all_views:
            st.write(f"• {view}")