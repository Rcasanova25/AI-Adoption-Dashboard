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


# Add feature flags for safe deployment
if 'feature_flags' not in st.session_state:
    st.session_state.feature_flags = {
        'executive_mode': True,
        'visual_redesign': True,
        'strategic_callouts': True,
        'competitive_homepage': False  # Start disabled, enable after testing
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
                                   ["Historical Trends", "Industry Deep Dive", "Geographic Analysis", 
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

# Load data first to ensure all variables are available
# historical_data, sector_2018, sector_2025, firm_size, ai_maturity, geographic, state_data, tech_stack, productivity_data, productivity_by_skill, ai_productivity_estimates, oecd_g7_adoption, oecd_applications, barriers_data = load_data()

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

        # Check if firm_size data is available
        try:
            # Use your existing firm size data but with competitive context
            fig = go.Figure()
            
            # Enhanced firm size chart with competitive zones
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
            
            # Add competitive threshold lines
            fig.add_hline(y=25, line_dash="dash", line_color="orange", 
                          annotation_text="Competitive Threshold (25%)", annotation_position="right")
            fig.add_hline(y=50, line_dash="dash", line_color="green",
                          annotation_text="Strong Position (50%)", annotation_position="right")
            
            # Add shaded competitive zones
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

        except NameError:
            # Fallback: Create the chart with manual data if firm_size isn't available
            st.info("Loading competitive landscape data...")
            
            # Manual firm size data as fallback
            fallback_firm_size = pd.DataFrame({
                'size': ['1-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250-499', 
                        '500-999', '1000-2499', '2500-4999', '5000+'],
                'adoption': [3.2, 3.8, 4.5, 5.2, 7.8, 12.5, 18.2, 25.6, 35.4, 42.8, 58.5]
            })
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=fallback_firm_size['size'], 
                y=fallback_firm_size['adoption'],
                marker=dict(
                    color=fallback_firm_size['adoption'],
                    colorscale='RdYlGn',
                    colorbar=dict(title="Competitive Position")
                ),
                text=[f'{x}%' for x in fallback_firm_size['adoption']],
                textposition='outside'
            ))
            
            # Add competitive threshold lines
            fig.add_hline(y=25, line_dash="dash", line_color="orange", 
                          annotation_text="Competitive Threshold (25%)", annotation_position="right")
            fig.add_hline(y=50, line_dash="dash", line_color="green",
                          annotation_text="Strong Position (50%)", annotation_position="right")
            
            fig.update_layout(
                title='Competitive Position by Company Size - Where Do You Stand?',
                xaxis_title='Company Size (Employees)',
                yaxis_title='AI Adoption Rate (%)',
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
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
            try:
                # Try to use loaded historical data
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
                
                # Add key milestone annotations
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
                
            except NameError:
                # Fallback: Create chart with manual data
                st.info("Loading historical data...")
                
                # Manual historical data as fallback
                fallback_historical = pd.DataFrame({
                    'year': [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                    'ai_use': [20, 47, 58, 56, 55, 50, 55, 78, 78],
                    'genai_use': [0, 0, 0, 0, 0, 33, 33, 71, 71]
                })
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=fallback_historical['year'], 
                    y=fallback_historical['ai_use'], 
                    mode='lines+markers', 
                    name='Overall AI Use',
                    line=dict(width=4, color='#1f77b4'),
                    marker=dict(size=8),
                    text=[f'{x}%' for x in fallback_historical['ai_use']],
                    textposition='top center'
                ))
                
                fig.add_trace(go.Scatter(
                    x=fallback_historical['year'], 
                    y=fallback_historical['genai_use'], 
                    mode='lines+markers', 
                    name='GenAI Use',
                    line=dict(width=4, color='#ff7f0e'),
                    marker=dict(size=8),
                    text=[f'{x}%' for x in fallback_historical['genai_use']],
                    textposition='bottom center'
                ))
                
                # Add key milestone annotations
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
        st.subheader("🎯 Strategic Action Planning")
        st.markdown("*Convert insights into executable strategic actions*")
        
        # Quick assessment to determine starting point
        st.markdown("### 📊 Current State Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_maturity = st.selectbox("Current AI Maturity Level", [
                "Exploring (No AI in production)",
                "Piloting (1-2 AI projects)",
                "Implementing (3-5 AI projects)",
                "Scaling (AI across multiple functions)",
                "Leading (AI-first organization)"
            ], help="Select your current AI implementation level")
            
            primary_objective = st.selectbox("Primary Strategic Objective", [
                "Operational Efficiency",
                "Revenue Growth", 
                "Cost Reduction",
                "Innovation & New Products",
                "Risk Management",
                "Customer Experience",
                "Competitive Advantage"
            ], help="Main goal for AI implementation")
            
            urgency_level = st.selectbox("Implementation Urgency", [
                "Immediate (30-60 days)",
                "Near-term (3-6 months)",
                "Medium-term (6-12 months)",
                "Long-term (12+ months)"
            ], help="How quickly do you need to see results?")
        
        with col2:
            available_budget = st.selectbox("Available Budget Range", [
                "Under $100K",
                "$100K - $500K",
                "$500K - $2M",
                "$2M - $10M",
                "Over $10M"
            ], help="Total budget for AI initiatives")
            
            team_readiness = st.selectbox("Team AI Readiness", [
                "No AI experience",
                "Some training/awareness",
                "Basic AI skills",
                "Strong AI capabilities",
                "AI experts on team"
            ], help="Current team's AI knowledge and skills")
            
            executive_support = st.selectbox("Executive Support Level", [
                "Exploring/Curious",
                "Supportive",
                "Committed", 
                "Champion/Sponsor",
                "Board-level mandate"
            ], help="Level of leadership commitment")
        
        # Generate customized action plan
        if st.button("🎯 Generate My Action Plan", type="primary", use_container_width=True):
            
            # Determine recommended path based on inputs
            maturity_score = {
                "Exploring (No AI in production)": 1,
                "Piloting (1-2 AI projects)": 2,
                "Implementing (3-5 AI projects)": 3,
                "Scaling (AI across multiple functions)": 4,
                "Leading (AI-first organization)": 5
            }[current_maturity]
            
            budget_score = {
                "Under $100K": 1,
                "$100K - $500K": 2, 
                "$500K - $2M": 3,
                "$2M - $10M": 4,
                "Over $10M": 5
            }[available_budget]
            
            urgency_days = {
                "Immediate (30-60 days)": 45,
                "Near-term (3-6 months)": 120,
                "Medium-term (6-12 months)": 270,
                "Long-term (12+ months)": 365
            }[urgency_level]
            
            st.markdown("---")
            st.markdown("### 📋 Your Customized Action Plan")
            
            # Strategic approach based on maturity and budget
            if maturity_score <= 2 and budget_score <= 2:
                approach = "Quick Win Strategy"
                timeline = "90-Day Sprint"
            elif maturity_score <= 3 and budget_score <= 3:
                approach = "Scaling Strategy" 
                timeline = "6-Month Build"
            else:
                approach = "Transformation Strategy"
                timeline = "12-Month Journey"
            
            st.success(f"""
            **Recommended Approach:** {approach}  
            **Timeline:** {timeline}  
            **Focus:** {primary_objective}
            """)
            
            # Phase-based action plan
            if approach == "Quick Win Strategy":
                st.markdown("#### 🚀 Quick Win Strategy (90 Days)")
                
                phase1, phase2, phase3 = st.tabs(["📅 Days 1-30", "📅 Days 31-60", "📅 Days 61-90"])
                
                with phase1:
                    st.markdown("**Phase 1: Foundation & Quick Wins (Days 1-30)**")
                    st.write("**🎯 Primary Goals:** Establish foundation and deliver first value")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**✅ Key Actions:**")
                        st.write("• Conduct AI readiness assessment")
                        st.write("• Identify 2-3 high-impact, low-complexity use cases")
                        st.write("• Secure executive sponsor and budget approval")
                        st.write("• Launch AI literacy program for key stakeholders")
                        st.write("• Select and engage AI vendor/platform")
                    
                    with col2:
                        st.markdown("**📊 Success Metrics:**")
                        st.write("• Use cases identified and prioritized")
                        st.write("• Executive sponsor assigned")
                        st.write("• Team trained on AI basics")
                        st.write("• Vendor selected and contracted")
                        st.write("• Project timeline approved")
                
                with phase2:
                    st.markdown("**Phase 2: Implementation & Learning (Days 31-60)**")
                    st.write("**🎯 Primary Goals:** Launch first pilot and build capabilities")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**✅ Key Actions:**")
                        st.write("• Launch highest-ROI pilot project")
                        st.write("• Establish AI governance and ethics framework")
                        st.write("• Begin data preparation and quality improvement")
                        st.write("• Train core team on selected AI platform")
                        st.write("• Develop success measurement framework")
                    
                    with col2:
                        st.markdown("**📊 Success Metrics:**")
                        st.write("• First pilot project launched")
                        st.write("• Governance framework established")
                        st.write("• Data quality baseline established")
                        st.write("• Core team platform-certified")
                        st.write("• KPIs defined and tracking begun")
                
                with phase3:
                    st.markdown("**Phase 3: Scale & Optimize (Days 61-90)**")
                    st.write("**🎯 Primary Goals:** Demonstrate value and plan scaling")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**✅ Key Actions:**")
                        st.write("• Measure and document pilot results")
                        st.write("• Optimize first implementation based on learnings")
                        st.write("• Launch second pilot project")
                        st.write("• Develop AI talent acquisition strategy")
                        st.write("• Create scaling roadmap for next 6 months")
                    
                    with col2:
                        st.markdown("**📊 Success Metrics:**")
                        st.write("• Measurable ROI from first pilot")
                        st.write("• Second pilot launched successfully")
                        st.write("• Talent strategy approved")
                        st.write("• 6-month roadmap created")
                        st.write("• Stakeholder buy-in secured")
            
            elif approach == "Scaling Strategy":
                st.markdown("#### ⚡ Scaling Strategy (6 Months)")
                
                phase1, phase2, phase3 = st.tabs(["📅 Months 1-2", "📅 Months 3-4", "📅 Months 5-6"])
                
                with phase1:
                    st.markdown("**Phase 1: Strategic Foundation (Months 1-2)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("• Develop comprehensive AI strategy")
                        st.write("• Expand successful pilot projects")
                        st.write("• Build AI Center of Excellence")
                        st.write("• Implement advanced AI governance")
                    
                    with col2:
                        st.write("• AI strategy approved by board")
                        st.write("• 3+ pilot projects in production")
                        st.write("• CoE team hired and operational")
                        st.write("• Governance processes documented")
                
                with phase2:
                    st.markdown("**Phase 2: Capability Building (Months 3-4)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("• Scale AI across multiple business functions")
                        st.write("• Develop internal AI talent pipeline")
                        st.write("• Integrate AI into core business processes")
                        st.write("• Establish strategic vendor partnerships")
                    
                    with col2:
                        st.write("• AI deployed in 5+ business functions")
                        st.write("• Internal training program launched")
                        st.write("• Process integration completed")
                        st.write("• Strategic partnerships established")
                
                with phase3:
                    st.markdown("**Phase 3: Value Optimization (Months 5-6)**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("• Optimize AI implementations for maximum ROI")
                        st.write("• Develop AI-powered innovation pipeline")
                        st.write("• Create competitive AI advantages")
                        st.write("• Plan enterprise-wide transformation")
                    
                    with col2:
                        st.write("• Documented ROI improvements")
                        st.write("• Innovation pipeline established")
                        st.write("• Competitive advantages identified")
                        st.write("• Transformation roadmap approved")
            
            else:  # Transformation Strategy
                st.markdown("#### 🏗️ Transformation Strategy (12 Months)")
                
                phase1, phase2, phase3, phase4 = st.tabs(["📅 Q1", "📅 Q2", "📅 Q3", "📅 Q4"])
                
                with phase1:
                    st.markdown("**Q1: Strategic Architecture**")
                    st.write("• Develop enterprise AI architecture and roadmap")
                    st.write("• Establish AI-first organizational structure")
                    st.write("• Launch enterprise-wide AI transformation program")
                    st.write("• Begin cultural transformation initiatives")
                
                with phase2:
                    st.markdown("**Q2: Infrastructure & Capabilities**")
                    st.write("• Build enterprise AI infrastructure and platforms")
                    st.write("• Develop comprehensive AI talent strategy")
                    st.write("• Implement AI across all major business functions")
                    st.write("• Create AI innovation labs and experimentation")
                
                with phase3:
                    st.markdown("**Q3: Integration & Optimization**")
                    st.write("• Integrate AI into all core business processes")
                    st.write("• Optimize AI implementations for enterprise scale")
                    st.write("• Develop AI-powered products and services")
                    st.write("• Establish AI ecosystem partnerships")
                
                with phase4:
                    st.markdown("**Q4: Leadership & Innovation**")
                    st.write("• Achieve AI-first organizational transformation")
                    st.write("• Launch AI-powered competitive advantages")
                    st.write("• Establish thought leadership in AI applications")
                    st.write("• Plan next-generation AI initiatives")
            
            # Resource requirements
            st.markdown("### 📋 Resource Requirements")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**👥 Team & Talent**")
                if maturity_score <= 2:
                    st.write("• AI project manager")
                    st.write("• External AI consultant")
                    st.write("• 2-3 business stakeholders")
                    st.write("• IT/data support")
                elif maturity_score <= 3:
                    st.write("• AI program director")
                    st.write("• 2-3 AI specialists")
                    st.write("• Business function champions")
                    st.write("• Data engineering team")
                else:
                    st.write("• Chief AI Officer")
                    st.write("• AI Center of Excellence team")
                    st.write("• Cross-functional AI teams")
                    st.write("• Enterprise architecture team")
            
            with col2:
                st.markdown("**💰 Budget Allocation**")
                if budget_score <= 2:
                    st.write("• 40% - AI platform/tools")
                    st.write("• 30% - External consulting")
                    st.write("• 20% - Training & development")
                    st.write("• 10% - Infrastructure")
                elif budget_score <= 3:
                    st.write("• 35% - AI talent & hiring")
                    st.write("• 25% - AI platform/tools")
                    st.write("• 25% - Infrastructure & data")
                    st.write("• 15% - Training & consulting")
                else:
                    st.write("• 40% - AI talent & team building")
                    st.write("• 30% - Enterprise AI infrastructure")
                    st.write("• 20% - Innovation & R&D")
                    st.write("• 10% - Strategic partnerships")
            
            with col3:
                st.markdown("**⚠️ Risk Mitigation**")
                st.write("• Start with low-risk, high-value use cases")
                st.write("• Establish clear success metrics")
                st.write("• Plan for change management resistance")
                st.write("• Ensure data privacy and security")
                st.write("• Build vendor relationship management")
            
            # Success tracking framework
            st.markdown("### 📊 Success Tracking Framework")
            
            metrics_tab1, metrics_tab2, metrics_tab3 = st.tabs(["📈 Business Metrics", "🎯 AI Metrics", "👥 Organizational Metrics"])
            
            with metrics_tab1:
                st.markdown("**Business Impact Metrics:**")
                if primary_objective == "Operational Efficiency":
                    st.write("• Process automation rate")
                    st.write("• Time-to-completion improvements")
                    st.write("• Error rate reductions")
                    st.write("• Employee productivity gains")
                elif primary_objective == "Revenue Growth":
                    st.write("• Revenue from AI-powered products/services")
                    st.write("• Customer acquisition improvements")
                    st.write("• Sales process efficiency gains")
                    st.write("• Market share expansion")
                else:
                    st.write("• Cost reduction percentages")
                    st.write("• ROI on AI investments")
                    st.write("• Process efficiency improvements")
                    st.write("• Quality improvements")
            
            with metrics_tab2:
                st.markdown("**AI Implementation Metrics:**")
                st.write("• Number of AI use cases in production")
                st.write("• AI model accuracy and performance")
                st.write("• System uptime and reliability")
                st.write("• Data quality scores")
                st.write("• AI adoption rate across functions")
            
            with metrics_tab3:
                st.markdown("**Organizational Readiness Metrics:**")
                st.write("• Employee AI literacy scores")
                st.write("• Change management success rate")
                st.write("• Leadership engagement levels")
                st.write("• Talent retention and acquisition")
                st.write("• Cultural transformation indicators")
            
            # Download action plan
            action_plan_content = f"""
            # AI Strategic Action Plan
            
            **Generated:** {datetime.now().strftime('%Y-%m-%d')}
            **Approach:** {approach}
            **Timeline:** {timeline}
            **Primary Objective:** {primary_objective}
            
            ## Current State
            - Maturity Level: {current_maturity}
            - Budget Range: {available_budget}
            - Team Readiness: {team_readiness}
            - Executive Support: {executive_support}
            - Implementation Urgency: {urgency_level}
            
            ## Recommended Next Steps
            1. Secure executive sponsorship and budget approval
            2. Identify and prioritize high-impact AI use cases
            3. Build core AI team and capabilities
            4. Launch pilot projects with clear success metrics
            5. Scale successful implementations across organization
            
            ## Success Metrics
            - Business impact aligned with {primary_objective}
            - AI implementation progress tracking
            - Organizational readiness improvements
            
            ## Risk Mitigation
            - Start with proven, low-risk use cases
            - Establish clear governance and ethics framework
            - Plan for change management and adoption challenges
            - Ensure data security and privacy compliance
            """
            
            st.download_button(
                label="📥 Download Complete Action Plan",
                data=action_plan_content,
                file_name=f"AI_Action_Plan_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Quick reference guides
        st.markdown("### 📚 Quick Reference Guides")
        
        guide_tabs = st.tabs(["🚀 Quick Wins", "⚠️ Common Pitfalls", "🎯 Best Practices", "📞 When to Get Help"])
        
        with guide_tabs[0]:
            st.markdown("**🚀 Proven Quick Win AI Use Cases:**")
            st.write("• **Customer Service:** AI chatbots for common inquiries")
            st.write("• **Content Creation:** AI-powered marketing copy and social media")
            st.write("• **Data Analysis:** Automated reporting and insights generation")
            st.write("• **Email Management:** Smart email categorization and responses")
            st.write("• **Document Processing:** Automated form processing and data extraction")
        
        with guide_tabs[1]:
            st.markdown("**⚠️ Common Pitfalls to Avoid:**")
            st.write("• **Starting too big:** Begin with small, focused projects")
            st.write("• **Ignoring change management:** Plan for organizational resistance")
            st.write("• **Poor data quality:** Clean data before AI implementation")
            st.write("• **Lack of clear metrics:** Define success criteria upfront")
            st.write("• **Vendor lock-in:** Maintain flexibility in technology choices")
            st.write("• **Over-automation:** Keep human oversight for critical decisions")
        
        with guide_tabs[2]:
            st.markdown("**🎯 Best Practices for Success:**")
            st.write("• **Executive sponsorship:** Secure C-level champion from day one")
            st.write("• **Cross-functional teams:** Include business and technical stakeholders")
            st.write("• **Iterative approach:** Start small, learn, and scale")
            st.write("• **Clear governance:** Establish AI ethics and oversight framework")
            st.write("• **Continuous learning:** Invest in ongoing team development")
            st.write("• **Measurable outcomes:** Track ROI and business impact")
        
        with guide_tabs[3]:
            st.markdown("**📞 When to Seek External Help:**")
            st.write("• **Complex AI strategy:** When internal expertise is limited")
            st.write("• **Large-scale implementation:** For enterprise-wide deployments")
            st.write("• **Specialized use cases:** Industry-specific AI applications")
            st.write("• **Talent gaps:** When internal AI skills are insufficient")
            st.write("• **Regulatory compliance:** For heavily regulated industries")
            st.write("• **Integration challenges:** Complex legacy system integration")
        
        # Implementation checklist
        st.markdown("### ✅ Implementation Checklist")
        
        checklist_col1, checklist_col2 = st.columns(2)
        
        with checklist_col1:
            st.markdown("**📋 Pre-Implementation (Week 1-2)**")
            st.checkbox("Executive sponsor identified and committed")
            st.checkbox("AI strategy aligned with business objectives")
            st.checkbox("Budget approved and allocated")
            st.checkbox("Core team assembled and roles defined")
            st.checkbox("Initial use cases identified and prioritized")
            st.checkbox("Success metrics defined and baseline established")
        
        with checklist_col2:
            st.markdown("**📋 Implementation (Week 3-8)**")
            st.checkbox("AI platform/tools selected and procured")
            st.checkbox("Data quality assessment completed")
            st.checkbox("Team training and upskilling initiated")
            st.checkbox("First pilot project launched")
            st.checkbox("Governance framework established")
            st.checkbox("Change management plan executed")
        
        # Success stories and case studies
        st.markdown("### 📖 Success Stories & Case Studies")
        
        success_tabs = st.tabs(["🏭 Manufacturing", "🏦 Financial Services", "🏥 Healthcare", "🛒 Retail"])
        
        with success_tabs[0]:
            st.markdown("**🏭 Manufacturing Success Story**")
            st.write("**Company:** Global automotive manufacturer")
            st.write("**Challenge:** Quality control inefficiencies costing $2M annually")
            st.write("**Solution:** AI-powered computer vision for defect detection")
            st.write("**Results:** 95% defect detection rate, 40% cost reduction, 6-month ROI")
            st.write("**Key Learnings:** Start with high-value, repetitive processes")
        
        with success_tabs[1]:
            st.markdown("**🏦 Financial Services Success Story**")
            st.write("**Company:** Regional bank with 500+ branches")
            st.write("**Challenge:** Manual loan processing taking 5-7 days")
            st.write("**Solution:** AI-powered document processing and risk assessment")
            st.write("**Results:** 80% faster processing, 30% cost reduction, improved accuracy")
            st.write("**Key Learnings:** Focus on customer-facing processes first")
        
        with success_tabs[2]:
            st.markdown("**🏥 Healthcare Success Story**")
            st.write("**Company:** Multi-hospital healthcare system")
            st.write("**Challenge:** Patient appointment scheduling inefficiencies")
            st.write("**Solution:** AI-powered scheduling optimization")
            st.write("**Results:** 25% reduction in no-shows, 15% increase in capacity utilization")
            st.write("**Key Learnings:** Address clear pain points with measurable impact")
        
        with success_tabs[3]:
            st.markdown("**🛒 Retail Success Story**")
            st.write("**Company:** E-commerce platform with 1M+ customers")
            st.write("**Challenge:** High cart abandonment rates")
            st.write("**Solution:** AI-powered personalized recommendations")
            st.write("**Results:** 35% increase in conversion rates, 20% higher average order value")
            st.write("**Key Learnings:** Personalization drives immediate business value")
        
        # Next steps and resources
        st.markdown("### 🚀 Next Steps & Resources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📚 Recommended Reading**")
            st.write("• 'AI Superpowers' by Kai-Fu Lee")
            st.write("• 'The Business of AI' by Harvard Business Review")
            st.write("• 'AI Strategy' by McKinsey & Company")
            st.write("• 'Machine Learning Yearning' by Andrew Ng")
            st.write("• 'AI Index Report 2025' by Stanford HAI")
        
        with col2:
            st.markdown("**🔗 Useful Resources**")
            st.write("• [AI Ethics Guidelines](https://ai.gov/ethics)")
            st.write("• [AI Talent Networks](https://ai-talent.org)")
            st.write("• [AI Vendor Comparison](https://ai-vendors.com)")
            st.write("• [AI Implementation Templates](https://ai-templates.org)")
            st.write("• [AI ROI Calculator](https://ai-roi-calculator.com)")
        
        # Contact and support
        st.markdown("### 📞 Need Help?")
        
        st.info("""
        **Ready to start your AI journey?** 
        
        - **For strategy consulting:** Contact our AI strategy team
        - **For technical implementation:** Connect with our AI engineering team  
        - **For change management:** Work with our organizational transformation experts
        - **For vendor selection:** Get our AI vendor evaluation framework
        
        **Next Steps:**
        1. Download your customized action plan above
        2. Schedule a strategy session with our AI experts
        3. Begin with your first pilot project
        4. Track progress using the success metrics framework
        """)
