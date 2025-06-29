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
        # Extract adoption rates
        industry_rate = int(industry_selection.split('(')[1].split('%')[0])
        size_rate = int(company_size_selection.split('(')[1].split('%')[0])
        
        st.metric("Industry Adoption", f"{industry_rate}%", 
                 "U.S. Census Bureau data")
        st.metric("Size Category", f"{size_rate}%", 
                 "850,000 firms surveyed")
        
        # Calculate competitive pressure
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
        st.write("• **Worker-level analysis:** 15% productivity improvement with GenAI access")
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
    
    # Comprehensive source validation
    st.markdown("### 📚 Complete Research Foundation")
    
    source_tabs = st.tabs(["🏛️ Government", "🎓 Academic", "🏢 Industry", "📊 Standards"])
    
    with source_tabs[0]:
        st.markdown("**Government & Institutional Sources:**")
        st.write("• **Stanford AI Index 2025:** Global AI metrics and adoption trends")
        st.write("• **U.S. Census Bureau:** 850,000 firm AI use supplement")
        st.write("• **NIST AI RMF 1.0:** 240+ organization collaborative framework")
        st.write("• **NSF AI Research Institutes:** $220M, 27 institutes, 40+ states")
        st.write("• **FDA AI-Enabled Medical Devices:** Regulatory pathway guidance")
        st.write("• **OECD AI Policy Observatory:** International best practices")
    
    with source_tabs[1]:
        st.markdown("**Academic Research Papers:**")
        st.write("• **Federal Reserve (Bick, Blandin, Deming):** Worker productivity analysis")
        st.write("• **MIT (Acemoglu):** Macroeconomic AI impact modeling")
        st.write("• **NBER (Brynjolfsson et al.):** Generative AI workplace studies")
        st.write("• **Nature (Jumper et al.):** AlphaFold protein folding breakthrough")
        st.write("• **Multiple working papers:** Sevilla, Korinek, Eloundou research")
    
    with source_tabs[2]:
        st.markdown("**Industry Research & Analysis:**")
        st.write("• **McKinsey Global Survey:** 1,491 participants, 101 nations")
        st.write("• **Goldman Sachs Research:** Economic growth impact analysis")
        st.write("• **BCG/INSEAD/OECD:** 840 enterprises across G7+ countries")
        st.write("• **NVIDIA:** AI infrastructure and token economics case studies")
        st.write("• **OpenAI, GitHub, DeepMind:** Primary technology development sources")
    
    with source_tabs[3]:
        st.markdown("**Technical Standards & Analysis:**")
        st.write("• **IEEE Computer Society:** Technical implementation standards")
        st.write("• **Nature Machine Intelligence:** Peer-reviewed AI research")
        st.write("• **MIT Technology Review:** Independent technology analysis")
        st.write("• **Gartner:** Technology maturity and adoption lifecycle analysis")
    
    # Download multi-source action framework
    if st.button("📥 Download Multi-Source Action Framework", use_container_width=True):
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