import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from datetime import datetime
from Utils.helpers import safe_execute, safe_data_check, clean_filename, monitor_performance
from data.loaders import load_all_datasets, get_dynamic_metrics, load_complete_datasets
from config.settings import DashboardConfig, FEATURE_FLAGS
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
    "🎯 Competitive Position Assessor", "💰 Investment Decision Engine", "⚖️ Regulatory Risk Radar",
    "Adoption Rates", "Historical Trends", "Industry Analysis", "Investment Trends", 
    "Regional Growth", "AI Cost Trends", "Token Economics", "Financial Impact", 
    "Labor Impact", "Firm Size Analysis", "Technology Stack", "AI Technology Maturity", 
    "Productivity Research", "Environmental Impact", "Geographic Distribution", 
    "OECD 2025 Findings", "Barriers & Support", "ROI Analysis", "Skill Gap Analysis", 
    "AI Governance", "Bibliography & Sources"
]

persona_views = {
    "General": ["🎯 Competitive Position Assessor", "Historical Trends"],
    "Business Leader": ["🎯 Competitive Position Assessor", "💰 Investment Decision Engine", "Financial Impact", "ROI Analysis"],
    "Policymaker": ["⚖️ Regulatory Risk Radar", "Labor Impact", "Geographic Distribution", "Barriers & Support"],
    "Researcher": ["Historical Trends", "Productivity Research", "AI Technology Maturity", "Bibliography & Sources"]
}

# Data loading function - now uses advanced caching
@smart_cache(ttl=7200, persist=True)
def load_data():
    """Load all dashboard data with advanced caching"""
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

# Helper function to safely clean filenames
def clean_filename(text):
    """Clean text for safe filename generation"""
    # Remove all emojis and special characters, replace spaces with underscores
    cleaned = re.sub(r'[^\w\s-]', '', text)  # Remove all non-word characters except spaces and hyphens
    cleaned = re.sub(r'\s+', '_', cleaned)   # Replace spaces with underscores
    cleaned = cleaned.lower().strip('_')      # Convert to lowercase and strip underscores
    return cleaned

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
        ["🚀 Strategic Brief", "⚖️ Competitive Position", "💰 Investment Case", 
         "📊 Market Intelligence", "🎯 Action Planning"],
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
                                   ["Historical Trends", "Industry Deep Dive", "Geographic Distribution", 
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
            ["Technology (92% adoption)", "Financial Services (85%)", "Healthcare (78%)", 
             "Manufacturing (75%)", "Retail & E-commerce (72%)", "Education (65%)",
             "Energy & Utilities (58%)", "Government (52%)"])
        
        company_size = st.selectbox("Company Size",
            ["1-50 employees (3% adoption)", "51-250 (12% adoption)", 
             "251-1000 (25% adoption)", "1000-5000 (42% adoption)", "5000+ (58% adoption)"])
    
    with col2:
        if st.button("🎯 Assess My Position", type="primary", use_container_width=True):
            display_competitive_assessment(industry, company_size)
    
    # Executive summary
    st.subheader("🎯 Executive Summary")
    st.markdown(f"""
    **Bottom Line Up Front (BLUF):**

    AI adoption has reached irreversible market tipping point. The combination of {current_adoption}% business adoption, 
    {dynamic_metrics['cost_reduction']} cost reduction, and proven ROI means competitive advantage now flows to implementation speed and quality, 
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
    """Determine which navigation system to use"""
    
    # Let users choose their experience
    mode = st.sidebar.selectbox(
        "Dashboard Mode",
        ["🎯 Executive (Streamlined)", "📊 Analyst (Detailed)"],
        help="Choose your experience level"
    )
    
    if "Executive" in mode and st.session_state.feature_flags['executive_mode']:
        return create_executive_navigation(dynamic_metrics)
    else:
        # Use existing navigation
        view_type = st.sidebar.selectbox(
            "Analysis View", 
            all_views
        )
        return view_type, False

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

# Helper function to create fallback data
def _create_fallback_data():
    """Create fallback data when loading fails"""
    global historical_data, sector_2018, sector_2025, firm_size, ai_maturity, geographic
    global state_data, tech_stack, productivity_data, productivity_by_skill, ai_productivity_estimates
    global oecd_g7_adoption, oecd_applications, barriers_data, support_effectiveness
    global ai_investment_data, regional_growth, ai_cost_reduction, financial_impact, ai_perception
    global training_emissions, skill_gap_data, ai_governance, token_economics, token_usage_patterns
    global token_optimization, token_pricing_evolution, genai_2025, sector_2025
    
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
    skill_gap_data = pd.DataFrame({'skill': ['Test'], 'gap_severity': [85], 'training_initiatives': [45]})
    ai_governance = pd.DataFrame({'aspect': ['Test'], 'adoption_rate': [62], 'maturity_score': [3.2]})
    token_usage_patterns = pd.DataFrame({'use_case': ['Test'], 'avg_input_tokens': [100], 'avg_output_tokens': [200]})
    token_optimization = pd.DataFrame({'strategy': ['Test'], 'cost_reduction': [30], 'implementation_complexity': [2]})
    token_pricing_evolution = pd.DataFrame({'date': pd.to_datetime(['2024-01-01']), 'avg_price_input': [0.2], 'avg_price_output': [0.8]})
    training_emissions = pd.DataFrame({'model': ['Test'], 'carbon_tons': [500]})
    genai_2025 = pd.DataFrame({'function': ['Test'], 'adoption': [25]})
    sector_2025 = pd.DataFrame({'sector': ['Test'], 'adoption_rate': [78], 'avg_roi': [3.2]})
    
    st.warning("⚠️ Using fallback data due to loading error. Some features may be limited.")

# Load all data
# Load all data using complete dataset function
loaded_datasets = safe_execute(
    load_data,
    default_value=None,
    error_message="Critical error in data loading"
)

# Initialize all variables
historical_data = sector_2018 = sector_2025 = firm_size = ai_maturity = geographic = state_data = tech_stack = productivity_data = productivity_by_skill = ai_productivity_estimates = oecd_g7_adoption = oecd_applications = barriers_data = support_effectiveness = ai_investment_data = regional_growth = ai_cost_reduction = financial_impact = ai_perception = training_emissions = skill_gap_data = ai_governance = token_economics = token_usage_patterns = token_optimization = token_pricing_evolution = genai_2025 = None

if loaded_datasets is not None:
    # Extract all datasets from the complete collection
    historical_data = loaded_datasets.get('historical_data')
    sector_2018 = loaded_datasets.get('sector_2018')
    sector_2025 = loaded_datasets.get('sector_2025')
    firm_size = loaded_datasets.get('firm_size')
    ai_maturity = loaded_datasets.get('ai_maturity')
    geographic = loaded_datasets.get('geographic')
    state_data = loaded_datasets.get('state_data')
    tech_stack = loaded_datasets.get('tech_stack')
    productivity_data = loaded_datasets.get('productivity_data')
    productivity_by_skill = loaded_datasets.get('productivity_by_skill')
    ai_productivity_estimates = loaded_datasets.get('ai_productivity_estimates')
    oecd_g7_adoption = loaded_datasets.get('oecd_g7_adoption')
    oecd_applications = loaded_datasets.get('oecd_applications')
    barriers_data = loaded_datasets.get('barriers_data')
    support_effectiveness = loaded_datasets.get('support_effectiveness')
    ai_investment_data = loaded_datasets.get('ai_investment_data')
    regional_growth = loaded_datasets.get('regional_growth')
    ai_cost_reduction = loaded_datasets.get('ai_cost_reduction')
    financial_impact = loaded_datasets.get('financial_impact')
    ai_perception = loaded_datasets.get('ai_perception')
    training_emissions = loaded_datasets.get('training_emissions')
    skill_gap_data = loaded_datasets.get('skill_gap_data')
    ai_governance = loaded_datasets.get('ai_governance')
    genai_2025 = loaded_datasets.get('genai_2025')
    token_economics = loaded_datasets.get('token_economics')
    token_usage_patterns = loaded_datasets.get('token_usage_patterns')
    token_optimization = loaded_datasets.get('token_optimization')
    token_pricing_evolution = loaded_datasets.get('token_pricing_evolution')
    
    st.success("✅ Complete datasets loaded successfully!")
else:
    st.error("❌ Complete data loading failed. Using fallback data.")
    _create_fallback_data()

# Generate dynamic metrics using complete datasets
dynamic_metrics = get_dynamic_metrics(loaded_datasets)

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
    st.stop()

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
    "Skill Gap Analysis": skill_gap_data,
    "AI Governance": ai_governance,
    "Productivity Research": productivity_data,
    "Investment Trends": ai_investment_data,
    "Regional Growth": regional_growth,
    "AI Cost Trends": ai_cost_reduction,
    "Token Economics": token_economics,
    "Labor Impact": ai_perception,
    "Environmental Impact": training_emissions,
    "Adoption Rates": genai_2025 if "2025" in data_year else sector_2018,
    "Firm Size Analysis": firm_size,
    "Technology Stack": tech_stack,
    "AI Technology Maturity": ai_maturity,
    "Geographic Distribution": geographic,
    "OECD 2025 Findings": oecd_g7_adoption,
    "Barriers & Support": barriers_data,
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
**🧠 Strategic Implications:** The 2022-2024 period represents a fundamental market transition. Organizations that don't adapt their AI strategy now risk falling permanently behind competitors who are gaining 15-40% productivity advantages.
""")

# Main visualization section
st.subheader(f"📊 {current_view}")

# Route to appropriate view
if not is_detailed:
    # Executive views - only handle true executive views
    if current_view == "🚀 Strategic Brief":
        executive_strategic_brief(dynamic_metrics, historical_data)
    elif current_view == "⚖️ Competitive Position":
        st.subheader("⚖️ Competitive Position Intelligence")
        st.markdown("*Understand your strategic position in the AI adoption landscape*")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
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
            
            maturity = st.select_slider("Current AI Maturity", [
                "Exploring (0-10%)",
                "Piloting (10-30%)", 
                "Implementing (30-60%)",
                "Scaling (60-80%)",
                "Leading (80%+)"
            ], help="Estimate your current AI implementation level")
            
            urgency = st.slider("Competitive Urgency (1-10)", 1, 10, 5, 
                               help="How urgent is it to act on AI adoption?")
        
        with col2:
            if st.button("🎯 Assess My Position", type="primary", use_container_width=True):
                assessment = display_competitive_assessment(industry, company_size, maturity, urgency)
        
        # Competitive landscape visualization
        st.markdown("### 📊 Competitive Landscape Analysis")
        if firm_size is not None and not firm_size.empty:
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
        
        # Investment context from market data - FIXED: Use dynamic metrics
        st.markdown("### 📊 Investment Market Context")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("2024 Global Investment", dynamic_metrics['investment_value'], 
                     dynamic_metrics['investment_delta'], 
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
            investment_amount = st.number_input(
                "Investment Budget ($)", 
                min_value=10000, 
                max_value=10000000, 
                value=500000, 
                step=50000,
                help="Include technology, talent, and implementation costs"
            )

            timeline = st.selectbox(
                "Timeline",
                ["6 months", "12 months", "18 months", "24 months", "36 months"],
                index=2,
                help="Time horizon for full investment deployment"
            )

            industry = st.selectbox(
                "Industry",
                ["Technology", "Financial Services", "Healthcare", "Manufacturing", 
                 "Retail", "Education", "Energy", "Government"],
                help="Industry affects ROI expectations and implementation approach"
            )

            goal = st.selectbox(
                "Primary Goal",
                ["Operational Efficiency", "Revenue Growth", "Cost Reduction", 
                 "Innovation & New Products", "Risk Management", "Customer Experience"],
                help="Main strategic objective for AI investment"
            )

            risk_tolerance = st.selectbox(
                "Risk Tolerance",
                ["Low", "Medium", "High"],
                index=1,
                help="Your organization's risk appetite for AI investment"
            )

        with col2:
            st.markdown("**Expected Outcomes**")
            
            # Show placeholder for expected outcomes
            st.info("📊 **Investment analysis will be generated when you click 'Generate Business Case'**")
            st.write("The business case will include:")
            st.write("• Expected ROI based on industry benchmarks")
            st.write("• Total return and net benefit projections")
            st.write("• Payback period analysis")
            st.write("• Risk assessment and success factors")

        # Generate business case
        if st.button("📋 Generate Business Case", type="primary", use_container_width=True):
            timeline_months = int(timeline.split()[0])
            case = display_investment_case(investment_amount, timeline_months, industry, goal, risk_tolerance)
    
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
                def create_historical_chart():
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

                chart = safe_execute(
                    create_historical_chart,
                    default_value=None,
                    error_message="Could not create historical chart"
                )

                if chart:
                    st.plotly_chart(chart, use_container_width=True)
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
    
    elif current_view == "🎯 Action Planning":
        st.subheader("🎯 Action Planning Engine")
        st.markdown("*Evidence-based strategic decisions for AI implementation*")
        
        # Quick action assessment
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
            
            urgency_level = st.slider("Competitive Urgency (1-10)", 1, 10, 5)
        
        with col2:
            company_size_selection = st.selectbox("Company Size", [
                "1-50 employees (3% adoption)",
                "51-250 employees (12% adoption)",
                "251-1000 employees (25% adoption)", 
                "1000-5000 employees (42% adoption)",
                "5000+ employees (58% adoption)"
            ])
            
            current_maturity = st.selectbox("Current AI Maturity", [
                "No AI (Starting from zero)",
                "Pilot Stage (1-2 projects)",
                "Early Adoption (3-10 projects)",
                "Scaling (10+ projects)",
                "Advanced (AI-first organization)"
            ])
        
        if st.button("🚀 Generate Action Plan", type="primary", use_container_width=True):
            # Generate action plan based on inputs
            industry_rate = int(industry_selection.split('(')[1].split('%')[0])
            size_rate = int(company_size_selection.split('(')[1].split('%')[0])
            
            st.markdown("---")
            st.subheader("📋 Your AI Action Plan")
            
            # Determine urgency level
            if urgency_level >= 8:
                urgency_desc = "CRITICAL - Immediate action required"
                urgency_color = "error"
            elif urgency_level >= 6:
                urgency_desc = "HIGH - Fast action needed"
                urgency_color = "warning"
            else:
                urgency_desc = "MODERATE - Strategic planning phase"
                urgency_color = "info"
            
            if urgency_color == "error":
                st.error(f"**Urgency Level:** {urgency_desc}")
            elif urgency_color == "warning":
                st.warning(f"**Urgency Level:** {urgency_desc}")
            else:
                st.info(f"**Urgency Level:** {urgency_desc}")
            
            # Generate specific recommendations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**⏰ Next 30 Days:**")
                if urgency_level >= 8:
                    st.write("• Emergency competitive analysis")
                    st.write("• Immediate budget allocation")
                    st.write("• Crisis response team formation")
                else:
                    st.write("• Share assessment with leadership")
                    st.write("• Conduct AI readiness audit")
                    st.write("• Identify quick-win opportunities")
            
            with col2:
                st.markdown("**📅 Next 90 Days:**")
                st.write("• Develop formal AI strategy")
                st.write("• Allocate budget for initiatives")
                st.write("• Launch pilot projects")
                st.write("• Establish governance framework")
            
            with col3:
                st.markdown("**📅 Next 12 Months:**")
                st.write("• Scale successful pilots")
                st.write("• Build internal capabilities")
                st.write("• Measure and optimize ROI")
                st.write("• Plan next-generation investments")
            
            # Download action plan
            action_plan = f"""
AI Strategic Action Plan
Generated: {datetime.now().strftime('%Y-%m-%d')}

Company Profile:
- Industry: {industry_selection}
- Size: {company_size_selection}
- Current Maturity: {current_maturity}
- Urgency Level: {urgency_level}/10

Strategic Recommendations:
[Generated action items based on assessment]

Timeline:
- 30 Days: Immediate actions
- 90 Days: Strategic implementation
- 12 Months: Scale and optimize
"""
            
            st.download_button(
                label="📥 Download Action Plan",
                data=action_plan,
                file_name=f"AI_Action_Plan_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    else:
        st.error(f"Executive view '{current_view}' is not fully implemented yet.")

# Continue with detailed views if selected
elif is_detailed:
    # Main view implementations continue here...
    if current_view == "🎯 Competitive Position Assessor":
        st.write("# 🎯 AI Competitive Position Assessment")
        st.write("**Get your strategic position and risk analysis in under 2 minutes**")
        
        # Add value proposition
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📊 **Data-Driven**\nBased on Stanford AI Index 2025 & McKinsey research")
        with col2:
            st.info("⚡ **Fast Results**\nComplete assessment in under 2 minutes")
        with col3:
            st.info("🎯 **Actionable**\nSpecific recommendations with timelines")
        
        st.markdown("---")
        
        # Complete competitive position assessor implementation
        st.info("🚧 **Full competitive position assessor implementation would continue here...**")
        st.markdown("This would include the complete assessment form, analysis engine, and report generation from the original implementation.")

    elif current_view == "Adoption Rates":
        st.write("📊 **Comprehensive AI Adoption Rates Analysis**")
        st.markdown("*Multi-dimensional analysis of AI adoption across industries, geographies, and firm sizes*")
        
        # Create tabs for different adoption perspectives
        adoption_tabs = st.tabs(["🏭 Industry Analysis", "🏢 Firm Size", "🌍 Geographic", "📈 Trends", "🔍 Deep Dive"])
        
        with adoption_tabs[0]:
            st.markdown("### 🏭 Industry-Specific Adoption Rates")
            
            if safe_data_check(sector_2025, "Industry adoption data") and sector_2025 is not None:
                # Industry adoption comparison
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Overall AI Adoption',
                    x=sector_2025['sector'],
                    y=sector_2025['adoption_rate'],
                    marker_color='#3498DB',
                    text=[f'{x}%' for x in sector_2025['adoption_rate']],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Adoption: %{y}%<br>GenAI: %{customdata}%<extra></extra>',
                    customdata=sector_2025['genai_adoption']
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
                    title="AI Adoption by Industry: Technology Leads, Government Lags",
                    xaxis_title="Industry Sector",
                    yaxis_title="Adoption Rate (%)",
                    barmode='group',
                    height=500,
                    xaxis_tickangle=45,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Industry insights
                col1, col2, col3 = st.columns(3)
                
                top_adopter = sector_2025.loc[sector_2025['adoption_rate'].idxmax()]
                lowest_adopter = sector_2025.loc[sector_2025['adoption_rate'].idxmin()]
                avg_adoption = sector_2025['adoption_rate'].mean()
                
                with col1:
                    st.metric("Top Adopter", top_adopter['sector'], f"{top_adopter['adoption_rate']}%")
                with col2:
                    st.metric("Lowest Adopter", lowest_adopter['sector'], f"{lowest_adopter['adoption_rate']}%")
                with col3:
                    st.metric("Average Adoption", f"{avg_adoption:.1f}%", "Across all sectors")
                
                # Adoption gap analysis
                st.markdown("### 📊 Adoption Gap Analysis")
                adoption_gap = top_adopter['adoption_rate'] - lowest_adopter['adoption_rate']
                st.info(f"**Adoption Gap:** {adoption_gap} percentage points between highest and lowest adopters")
                
                if adoption_gap > 30:
                    st.warning("**High Gap Alert:** Significant adoption disparities suggest competitive advantages for early adopters")
                elif adoption_gap > 20:
                    st.info("**Moderate Gap:** Industry-specific factors influence adoption rates")
                else:
                    st.success("**Low Gap:** Relatively uniform adoption across sectors")
        
        with adoption_tabs[1]:
            st.markdown("### 🏢 Firm Size Adoption Analysis")
            
            if safe_data_check(firm_size, "Firm size data") and firm_size is not None:
                # Firm size adoption chart
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=firm_size['size'],
                    y=firm_size['adoption'],
                    marker=dict(
                        color=firm_size['adoption'],
                        colorscale='RdYlGn',
                        colorbar=dict(title="Adoption Rate (%)")
                    ),
                    text=[f'{x}%' for x in firm_size['adoption']],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Adoption: %{y}%<extra></extra>'
                ))
                
                # Add threshold lines
                fig.add_hline(y=25, line_dash="dash", line_color="orange", 
                              annotation_text="Competitive Threshold (25%)")
                fig.add_hline(y=50, line_dash="dash", line_color="green",
                              annotation_text="Strong Position (50%)")
                
                fig.update_layout(
                    title="AI Adoption by Firm Size: Scale Matters",
                    xaxis_title="Firm Size (Employees)",
                    yaxis_title="Adoption Rate (%)",
                    height=500,
                    xaxis_tickangle=45
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Size-based insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success("**Large Firm Advantage:**")
                    st.write("• 5000+ employees: 58.5% adoption")
                    st.write("• 1000-2499 employees: 42.8% adoption")
                    st.write("• Resource advantage enables faster adoption")
                
                with col2:
                    st.warning("**Small Firm Challenge:**")
                    st.write("• 1-4 employees: 3.2% adoption")
                    st.write("• 5-9 employees: 3.8% adoption")
                    st.write("• Limited resources and expertise barriers")
        
        with adoption_tabs[2]:
            st.markdown("### 🌍 Geographic Adoption Patterns")
            
            if safe_data_check(geographic, "Geographic data") and geographic is not None:
                # Geographic adoption map
                fig = px.scatter_mapbox(
                    geographic,
                    lat='lat',
                    lon='lon',
                    size='rate',
                    color='rate',
                    hover_name='city',
                    hover_data=['state', 'population_millions', 'gdp_billions'],
                    color_continuous_scale='Viridis',
                    size_max=20,
                    title="AI Adoption by Geographic Region"
                )
                
                fig.update_layout(
                    mapbox_style="carto-positron",
                    height=500,
                    mapbox=dict(
                        center=dict(lat=39.8283, lon=-98.5795),
                        zoom=3
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Geographic insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top AI Hubs:**")
                    top_cities = geographic.nlargest(5, 'rate')
                    for _, city in top_cities.iterrows():
                        st.write(f"• **{city['city']}**: {city['rate']}% adoption")
                
                with col2:
                    st.markdown("**Regional Patterns:**")
                    st.write("• **West Coast**: Technology concentration")
                    st.write("• **Northeast**: Financial services hub")
                    st.write("• **Texas**: Energy and manufacturing")
                    st.write("• **Southeast**: Emerging tech centers")
        
        with adoption_tabs[3]:
            st.markdown("### 📈 Adoption Trends Over Time")
            
            if safe_data_check(historical_data, "Historical data") and historical_data is not None:
                # Historical trends
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=historical_data['year'],
                    y=historical_data['ai_use'],
                    mode='lines+markers',
                    name='Overall AI Use',
                    line=dict(width=4, color='#3498DB'),
                    marker=dict(size=8),
                    text=[f'{x}%' for x in historical_data['ai_use']],
                    textposition='top center'
                ))
                
                fig.add_trace(go.Scatter(
                    x=historical_data['year'],
                    y=historical_data['genai_use'],
                    mode='lines+markers',
                    name='GenAI Use',
                    line=dict(width=4, color='#E74C3C'),
                    marker=dict(size=8),
                    text=[f'{x}%' for x in historical_data['genai_use']],
                    textposition='bottom center'
                ))
                
                # Add milestone annotations
                fig.add_annotation(
                    x=2022, y=33,
                    text="ChatGPT Launch<br>GenAI Revolution",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#E74C3C",
                    ax=-30, ay=-40,
                    bgcolor="rgba(231,76,60,0.1)",
                    bordercolor="#E74C3C"
                )
                
                fig.add_annotation(
                    x=2024, y=78,
                    text="2024 Acceleration<br>AI Index Report",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#3498DB",
                    ax=30, ay=-30,
                    bgcolor="rgba(52,152,219,0.1)",
                    bordercolor="#3498DB"
                )
                
                fig.update_layout(
                    title="AI Adoption Explosion: 2017-2025",
                    xaxis_title="Year",
                    yaxis_title="Adoption Rate (%)",
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Trend insights
                st.success("**Key Trend Insights:**")
                st.write("• **2017-2021**: Steady growth in traditional AI adoption")
                st.write("• **2022**: ChatGPT launch triggers GenAI revolution")
                st.write("• **2023-2024**: Explosive growth in both AI and GenAI adoption")
                st.write("• **2025**: AI becomes mainstream with 78% business adoption")
        
        with adoption_tabs[4]:
            st.markdown("### 🔍 Deep Dive: Adoption Drivers")
            
            # Adoption barriers analysis
            if safe_data_check(barriers_data, "Barriers data") and barriers_data is not None:
                st.markdown("#### 🚧 Barriers to AI Adoption")
                
                fig = px.bar(barriers_data, x='percentage', y='barrier', orientation='h',
                            title="Top Barriers to AI Adoption",
                            color='percentage',
                            color_continuous_scale='Reds')
                
                fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Barrier insights
                top_barrier = barriers_data.loc[barriers_data['percentage'].idxmax()]
                st.warning(f"**Primary Barrier:** {top_barrier['barrier']} ({top_barrier['percentage']}% of firms)")
            
            # Support effectiveness
            if safe_data_check(support_effectiveness, "Support data") and support_effectiveness is not None:
                st.markdown("#### 🛠️ Support Program Effectiveness")
                
                fig = px.bar(support_effectiveness, x='effectiveness_score', y='support_type', orientation='h',
                            title="Effectiveness of AI Support Programs",
                            color='effectiveness_score',
                            color_continuous_scale='Greens')
                
                fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Support insights
                most_effective = support_effectiveness.loc[support_effectiveness['effectiveness_score'].idxmax()]
                st.success(f"**Most Effective Support:** {most_effective['support_type']} ({most_effective['effectiveness_score']}/100)")
        
        # Executive summary
        st.markdown("---")
        st.markdown("### 📋 Executive Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Adoption", "78%", "+23pp vs 2023")
        with col2:
            st.metric("GenAI Adoption", "71%", "+38pp vs 2023")
        with col3:
            st.metric("Top Industry", "Technology", "92% adoption")
        with col4:
            st.metric("Size Advantage", "Large Firms", "58.5% vs 3.2%")
        
        st.info("""
        **Strategic Implications:**
        - AI adoption has reached mainstream levels (78%)
        - GenAI adoption more than doubled in one year
        - Significant competitive advantages for early adopters
        - Technology and financial services lead adoption
        - Large firms have 18x higher adoption than small firms
        """)

    elif current_view == "Historical Trends":
        st.write("📊 **AI Adoption Historical Trends (2017-2025)**")
        
        if safe_data_check(historical_data, "Historical data") and historical_data is not None:
            # Apply year filter if set
            if 'year_range' in locals():
                filtered_data = historical_data[
                    (historical_data['year'] >= year_range[0]) & 
                    (historical_data['year'] <= year_range[1])
                ]
            else:
                filtered_data = historical_data
            
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
            
            # Add milestone annotations
            if 2022 in filtered_data['year'].tolist():
                fig.add_annotation(
                    x=2022, y=33,
                    text="<b>ChatGPT Launch</b><br>GenAI Era Begins<br><i>Source: Stanford AI Index</i>",
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
                    font=dict(color="#ff7f0e", size=11, family="Arial")
                )
            
            if 2024 in filtered_data['year'].tolist():
                fig.add_annotation(
                    x=2024, y=78,
                    text="<b>2024 Acceleration</b><br>AI Index Report findings<br><i>78% business adoption</i>",
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
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insights
            st.info("""
            **🎯 Key Research Findings:**
            
            **Stanford AI Index 2025 Evidence:**
            - Business adoption jumped from 55% to 78% in just one year (fastest enterprise technology adoption in history)
            - GenAI adoption more than doubled from 33% to 71%
            - 280x cost reduction in AI inference since November 2022
            """)
        else:
            st.error("Historical data not available.")

    elif current_view == "Industry Analysis":
        st.write("🏭 **AI Adoption by Industry (2025)**")
        
        if safe_data_check(sector_2025, "Industry analysis data") and sector_2025 is not None:
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
        else:
            st.error("Industry analysis data not available.")

    elif current_view == "AI Cost Trends":
        st.write("💰 **AI Cost Evolution & Trends**")
        
        if safe_data_check(ai_cost_reduction, "AI cost data"):
            # Cost reduction visualization
            fig = px.bar(ai_cost_reduction, x='model', y='cost_per_million_tokens',
                        title="Dramatic AI Cost Reduction: November 2022 to October 2024",
                        color='cost_per_million_tokens',
                        color_continuous_scale='Reds_r',
                        log_y=True)
            
            fig.update_layout(height=500, xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost metrics
            col1, col2, col3 = st.columns(3)
            
            highest_cost = ai_cost_reduction['cost_per_million_tokens'].max()
            lowest_cost = ai_cost_reduction['cost_per_million_tokens'].min()
            reduction_factor = highest_cost / lowest_cost
            
            with col1:
                st.metric("Starting Cost (Nov 2022)", f"${highest_cost:.2f}", "Per million tokens")
            with col2:
                st.metric("Current Cost (2024)", f"${lowest_cost:.3f}", "Per million tokens")
            with col3:
                st.metric("Total Reduction", f"{reduction_factor:.0f}x cheaper", "Dramatic deflation")
            
            # Token pricing evolution
            if token_pricing_evolution is not None:
                st.markdown("### 📈 Token Pricing Evolution Over Time")
                
                fig_evolution = go.Figure()
                
                fig_evolution.add_trace(go.Scatter(
                    x=token_pricing_evolution['date'],
                    y=token_pricing_evolution['avg_price_input'],
                    mode='lines+markers',
                    name='Input Token Price',
                    line=dict(width=3, color='#3498DB')
                ))
                
                fig_evolution.add_trace(go.Scatter(
                    x=token_pricing_evolution['date'],
                    y=token_pricing_evolution['avg_price_output'],
                    mode='lines+markers',
                    name='Output Token Price',
                    line=dict(width=3, color='#E74C3C')
                ))
                
                fig_evolution.update_layout(
                    title="Token Price Evolution: Continuous Cost Deflation",
                    xaxis_title="Date",
                    yaxis_title="Price per Million Tokens ($)",
                    height=400,
                    yaxis_type="log"
                )
                
                st.plotly_chart(fig_evolution, use_container_width=True)
                
        else:
            st.error("AI cost data not available.")

    elif current_view == "Technology Stack":
        st.write("🔧 **AI Technology Stack Analysis**")
        
        if safe_data_check(tech_stack, "Technology stack data"):
            # Technology stack distribution
            fig = px.pie(tech_stack, values='percentage', names='technology',
                        title="AI Implementation Approaches: Integration Strategies")
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Stack insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("**Most Common Approach**")
                max_approach = tech_stack.loc[tech_stack['percentage'].idxmax()]
                st.write(f"**{max_approach['technology']}**: {max_approach['percentage']}%")
                
                st.info("**Integration Benefits**")
                st.write("• Higher ROI with combined approaches")
                st.write("• Better scalability and performance")
                st.write("• Reduced implementation risk")
            
            with col2:
                st.markdown("**Technology Stack Breakdown:**")
                for _, row in tech_stack.iterrows():
                    st.metric(str(row['technology']), f"{row['percentage']}%", 
                             f"of implementations")
                
        else:
            st.error("Technology stack data not available.")

    elif current_view == "Productivity Research":
        st.write("📈 **AI Productivity Research Findings**")
        
        if safe_data_check(productivity_data, "Productivity research data"):
            # Productivity trends over time
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=productivity_data['year'],
                y=productivity_data['productivity_growth'],
                mode='lines+markers',
                name='Productivity Growth',
                line=dict(width=4, color='#3498DB'),
                marker=dict(size=8)
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
                title="Productivity Growth and Workforce Demographics (1980-2025)",
                xaxis_title="Year",
                yaxis=dict(title="Productivity Growth (%)", side="left"),
                yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Research estimates
            if ai_productivity_estimates is not None:
                st.markdown("### 🔬 AI Productivity Impact Estimates")
                
                fig_estimates = px.bar(ai_productivity_estimates, x='source', y='annual_impact',
                                      title="Annual Productivity Impact Estimates by Research Source",
                                      color='annual_impact',
                                      color_continuous_scale='Greens')
                
                fig_estimates.update_layout(height=400, xaxis_tickangle=45)
                st.plotly_chart(fig_estimates, use_container_width=True)
                
                # Research insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Highest Estimate", "Goldman Sachs", "2.5% annual impact")
                    st.metric("Conservative Estimate", "Acemoglu", "0.07% annual impact")
                
                with col2:
                    st.info("**Research Consensus:**")
                    st.write("• Wide range of productivity estimates")
                    st.write("• Potential for significant long-term impact")
                    st.write("• Depends on implementation quality")
            
        else:
            st.error("Productivity research data not available.")

    elif current_view == "ROI Analysis":
        st.write("💹 **AI Return on Investment Analysis**")
        
        if safe_data_check(sector_2025, "ROI analysis data"):
            # ROI by sector
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=sector_2025['sector'],
                y=sector_2025['avg_roi'],
                marker=dict(
                    color=sector_2025['avg_roi'],
                    colorscale='RdYlGn',
                    colorbar=dict(title="ROI Multiplier")
                ),
                text=[f'{x}x' for x in sector_2025['avg_roi']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>ROI: %{y}x<br>Adoption: %{customdata}%<extra></extra>',
                customdata=sector_2025['adoption_rate']
            ))
            
            # Add ROI threshold lines
            fig.add_hline(y=2.0, line_dash="dash", line_color="orange", 
                          annotation_text="Minimum Viable ROI (2.0x)")
            fig.add_hline(y=3.0, line_dash="dash", line_color="green",
                          annotation_text="Strong ROI Threshold (3.0x)")
            
            fig.update_layout(
                title="AI ROI by Industry Sector: Consistent Value Creation",
                xaxis_title="Industry Sector",
                yaxis_title="Average ROI (x)",
                height=500,
                xaxis_tickangle=45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # ROI insights
            col1, col2, col3, col4 = st.columns(4)
            
            best_roi = sector_2025.loc[sector_2025['avg_roi'].idxmax()]
            worst_roi = sector_2025.loc[sector_2025['avg_roi'].idxmin()]
            avg_roi = sector_2025['avg_roi'].mean()
            above_threshold = (sector_2025['avg_roi'] >= 3.0).sum()
            
            with col1:
                st.metric("Best ROI", best_roi['sector'], f"{best_roi['avg_roi']}x")
            with col2:
                st.metric("Lowest ROI", worst_roi['sector'], f"{worst_roi['avg_roi']}x")
            with col3:
                st.metric("Average ROI", f"{avg_roi:.1f}x", "Across all sectors")
            with col4:
                st.metric("Strong Performers", f"{above_threshold}/{len(sector_2025)}", "≥3.0x ROI")
            
            # ROI vs Adoption correlation
            st.markdown("### 📊 ROI vs Adoption Rate Analysis")
            
            fig_scatter = px.scatter(sector_2025, x='adoption_rate', y='avg_roi',
                                   size='adoption_rate', color='avg_roi',
                                   hover_name='sector',
                                   title="ROI vs Adoption Rate: Higher Adoption Drives Better Returns",
                                   color_continuous_scale='Viridis')
            
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        else:
            st.error("ROI analysis data not available.")

    elif current_view == "Bibliography & Sources":
        st.write("📚 **Complete Bibliography & Source Citations**")
        
        st.markdown("""
        This dashboard synthesizes data from multiple authoritative sources to provide comprehensive 
        AI adoption insights. All sources are cited using Chicago Manual of Style format.
        """)
        
        # Create tabs for different source categories
        bib_tabs = st.tabs(["🏛️ Government & Institutional", "🏢 Corporate & Industry", "🎓 Academic Research", 
                            "📰 News & Analysis", "📊 Databases & Collections"])
        
        with bib_tabs[0]:
            st.markdown("""
            ### Government and Institutional Sources
            
            1. **Stanford Human-Centered AI Institute.** "AI Index Report 2025." Stanford University. Accessed June 28, 2025. https://aiindex.stanford.edu/ai-index-report-2025/.

            2. **U.S. Census Bureau.** "AI Use Supplement." Washington, DC: U.S. Department of Commerce. Accessed June 28, 2025. https://www.census.gov.

            3. **National Science Foundation.** "National AI Research Institutes." Washington, DC: NSF. Accessed June 28, 2025. https://www.nsf.gov/focus-areas/artificial-intelligence.

            4. **National Institute of Standards and Technology.** "AI Risk Management Framework (AI RMF 1.0)." NIST AI 100-1. Gaithersburg, MD: NIST, January 2023.

            5. **Organisation for Economic Co-operation and Development.** "OECD AI Policy Observatory." Accessed June 28, 2025. https://oecd.ai.
            """)
            
        with bib_tabs[1]:
            st.markdown("""
            ### Corporate and Industry Sources
            
            6. **McKinsey & Company.** "The State of AI: McKinsey Global Survey on AI." McKinsey Global Institute. Accessed June 28, 2025.

            7. **OpenAI.** "Introducing DALL-E." OpenAI Blog, January 5, 2021.

            8. **GitHub.** "Introducing GitHub Copilot: AI Pair Programmer." GitHub Blog, June 29, 2021.

            9. **Goldman Sachs Research.** "The Potentially Large Effects of Artificial Intelligence on Economic Growth." Economic Research, 2023.
            """)
            
        with bib_tabs[2]:
            st.markdown("""
            ### Academic Publications
            
            10. **Bick, Alexander, Adam Blandin, and David Deming.** "The Rapid Adoption of Generative AI." Federal Reserve Bank working paper, 2024.

            11. **Brynjolfsson, Erik, Danielle Li, and Lindsey R. Raymond.** "Generative AI at Work." National Bureau of Economic Research Working Paper, 2023.

            12. **Acemoglu, Daron.** "The Simple Macroeconomics of AI." MIT Economics working paper, 2024.

            13. **Jumper, John, et al.** "Highly Accurate Protein Structure Prediction with AlphaFold." *Nature* 596, no. 7873 (2021): 583-589.
            """)
            
        with bib_tabs[3]:
            st.markdown("""
            ### News and Analysis Sources
            
            14. **MIT Technology Review.** "Artificial Intelligence." Accessed June 28, 2025.

            15. **Nature Machine Intelligence.** "Nature Machine Intelligence Journal." Accessed June 28, 2025.

            16. **IEEE Computer Society.** "IEEE Computer Society Publications." Accessed June 28, 2025.
            """)
            
        with bib_tabs[4]:
            st.markdown("""
            ### Multi-Source Collections and Databases
            
            17. **AI Index Report Database.** Stanford HAI. Multi-year compilation of AI metrics, 2017-2025.

            18. **OECD AI Database.** Cross-national AI policy and adoption metrics.

            19. **US Census AI Supplement.** Comprehensive business AI usage survey, 850,000 firms.
            """)

    else:
        # Generic view renderer for any unmapped views
        st.write(f"📊 **{current_view}**")
        
        if current_view in data_map and data_map[current_view] is not None:
            df = data_map[current_view]
            
            if safe_data_check(df, current_view):
                st.markdown(f"### Data Overview for {current_view}")
                st.dataframe(df, use_container_width=True)
                
                # Try to create a simple visualization if possible
                def create_auto_visualization():
                    if df is not None and len(df.columns) >= 2:
                        x_col = df.columns[0]
                        y_col = df.columns[1]
                        
                        # Check if we can make a simple bar chart
                        if pd.api.types.is_numeric_dtype(df[y_col]):
                            fig = px.bar(df, x=x_col, y=y_col, 
                                        title=f"{current_view}: {y_col} by {x_col}")
                            return fig
                        else:
                            st.info("Data available but not suitable for automatic visualization.")
                            return None
                    else:
                        st.info("Data has insufficient columns for automatic visualization.")
                        return None

                chart = safe_execute(
                    create_auto_visualization,
                    default_value=None,
                    error_message="Could not create automatic visualization"
                )

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
            label=f"📥 Download {current_view} Data (CSV)",
            data=csv,
            file_name=f"ai_adoption_{safe_filename}.csv",
            mime="text/csv"
        )

# --- Performance Integration Toggle ---
if 'performance_integrator' not in st.session_state:
    st.session_state.performance_integrator = PerformanceIntegrator()

st.sidebar.markdown("---")
use_optimized_dashboard = st.sidebar.checkbox(
    "⚡ Use Optimized Performance Dashboard (Beta)",
    value=False,
    help="Switch to the new fully optimized dashboard with advanced caching, chart, and memory management."
)

if use_optimized_dashboard:
    integrator = st.session_state.performance_integrator
    integrator.render_optimized_dashboard()
    st.stop()
