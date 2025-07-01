"""
ROI Analysis view for AI Adoption Dashboard
Displays comprehensive ROI analysis with investment returns, payback analysis, and sector ROI
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
import logging
from datetime import datetime

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename
from business.roi_calculator import roi_calculator

logger = logging.getLogger(__name__)


def show_roi_analysis(
    data_year: str,
    roi_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display comprehensive ROI analysis for AI investments
    
    Args:
        data_year: Selected year (e.g., "2025")
        roi_data: DataFrame with ROI data (sector_2025 from dashboard_data)
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'roi_industry':
            return "**Source**: AI Index 2025 Report & Industry Analysis\n\n**Methodology**: Analysis of AI investment returns across industry sectors based on reported financial outcomes and adoption metrics."
        elif source_type == 'investment_levels':
            return "**Source**: Comprehensive ROI Analysis Framework\n\n**Methodology**: Analysis based on investment levels, success rates, and time-to-ROI metrics from enterprise AI implementations."
        return "**Source**: AI Investment Analysis 2025"
    
    st.write("💰 **ROI Analysis: Comprehensive Economic Impact**")
    
    # Validate ROI data
    validator = DataValidator()
    roi_result = validator.validate_dataframe(
        roi_data,
        "ROI Data",
        required_columns=['sector', 'avg_roi'],
        min_rows=1
    )
    
    if roi_result.is_valid:
        # Create detailed ROI dashboard
        tab1, tab2, tab3, tab4 = st.tabs(["Investment Returns", "Payback Analysis", "Sector ROI", "ROI Calculator"])
        
        with tab1:
            st.write("📈 **Investment Returns by Level**")
            
            # Investment returns visualization
            investment_data = pd.DataFrame({
                'investment_level': ['Pilot (<$100K)', 'Small ($100K-$500K)', 'Medium ($500K-$2M)', 
                                   'Large ($2M-$10M)', 'Enterprise ($10M+)'],
                'avg_roi': [1.8, 2.5, 3.2, 3.8, 4.5],
                'time_to_roi': [6, 9, 12, 18, 24],  # months
                'success_rate': [45, 58, 72, 81, 87]  # % of projects achieving positive ROI
            })
            
            def plot_investment_returns():
                """Plot investment returns chart"""
                fig = go.Figure()
                
                # ROI bars
                fig.add_trace(go.Bar(
                    name='Average ROI',
                    x=investment_data['investment_level'],
                    y=investment_data['avg_roi'],
                    yaxis='y',
                    marker_color='#2ECC71',
                    text=[f'{x}x' for x in investment_data['avg_roi']],
                    textposition='outside'
                ))
                
                # Success rate line
                fig.add_trace(go.Scatter(
                    name='Success Rate',
                    x=investment_data['investment_level'],
                    y=investment_data['success_rate'],
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
            
            # Use safe plotting
            if safe_plot_check(
                investment_data,
                "Investment Returns Data",
                required_columns=['investment_level', 'avg_roi', 'success_rate'],
                plot_func=plot_investment_returns
            ):
                st.info("""
                **Key Insights:**
                - Larger investments show higher ROI and success rates
                - Enterprise projects (87% success) benefit from better resources and planning
                - Even small pilots can achieve 1.8x ROI with 45% success rate
                """)
                
                # Safe download button
                safe_download_button(
                    investment_data,
                    clean_filename(f"ai_investment_returns_{data_year}.csv"),
                    "📥 Download Investment Returns Data",
                    key="download_investment_returns",
                    help_text="Download AI investment returns data by investment level"
                )
        
        with tab2:
            st.write("⏱️ **Payback Period Analysis**")
            
            # Payback period analysis
            payback_data = pd.DataFrame({
                'scenario': ['Best Case', 'Typical', 'Conservative'],
                'months': [8, 15, 24],
                'probability': [20, 60, 20]
            })
            
            def plot_payback_analysis():
                """Plot payback analysis chart"""
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=payback_data['scenario'],
                    y=payback_data['months'],
                    text=[f'{x} months' for x in payback_data['months']],
                    textposition='outside',
                    marker_color=['#2ECC71', '#F39C12', '#E74C3C'],
                    hovertemplate='<b>%{x}</b><br>Payback: %{y} months<br>Probability: %{customdata}%<extra></extra>',
                    customdata=payback_data['probability']
                ))
                
                fig.update_layout(
                    title='AI Investment Payback Period Scenarios',
                    xaxis_title='Scenario',
                    yaxis_title='Payback Period (Months)',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            if safe_plot_check(
                payback_data,
                "Payback Analysis Data",
                required_columns=['scenario', 'months'],
                plot_func=plot_payback_analysis
            ):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🚀 Accelerators:**")
                    st.write("• Clear business objectives")
                    st.write("• Quality data available")
                    st.write("• Executive sponsorship")
                    st.write("• Skilled team in place")
                
                with col2:
                    st.write("**🐌 Delays:**")
                    st.write("• Poor data quality")
                    st.write("• Integration challenges")
                    st.write("• Organizational resistance")
                    st.write("• Scope creep")
                
                # Safe download button
                safe_download_button(
                    payback_data,
                    clean_filename(f"ai_payback_scenarios_{data_year}.csv"),
                    "📥 Download Payback Scenarios",
                    key="download_payback_scenarios",
                    help_text="Download AI investment payback scenario data"
                )
        
        with tab3:
            st.write("🏭 **ROI by Industry Sector**")
            
            def plot_sector_roi():
                """Plot sector-specific ROI"""
                # Sort by ROI for better visualization
                sorted_roi_data = roi_data.sort_values('avg_roi')
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=sorted_roi_data['sector'],
                    y=sorted_roi_data['avg_roi'],
                    marker_color=sorted_roi_data['avg_roi'],
                    marker_colorscale='Viridis',
                    text=[f'{x}x' for x in sorted_roi_data['avg_roi']],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>ROI: %{y}x<br>Adoption: %{customdata}%<extra></extra>',
                    customdata=sorted_roi_data['adoption_rate'] if 'adoption_rate' in sorted_roi_data.columns else None
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
            
            if safe_plot_check(
                roi_data,
                "Sector ROI Data",
                required_columns=['sector', 'avg_roi'],
                plot_func=plot_sector_roi
            ):
                # Top performers analysis
                try:
                    top_sectors = roi_data.nlargest(3, 'avg_roi')
                    
                    st.write("**🏆 Top ROI Performers:**")
                    for _, sector in top_sectors.iterrows():
                        adoption_text = ""
                        if 'adoption_rate' in sector:
                            adoption_text = f", {sector['adoption_rate']}% adoption"
                        st.write(f"• **{sector['sector']}:** {sector['avg_roi']}x ROI{adoption_text}")
                    
                    # Calculate sector rankings using ROI calculator
                    if hasattr(roi_calculator, 'calculate_sector_roi_ranking'):
                        sector_rankings = roi_calculator.calculate_sector_roi_ranking(roi_data)
                        if sector_rankings:
                            st.write("**📊 Investment Recommendations:**")
                            for ranking in sector_rankings[:5]:  # Top 5
                                st.write(f"• **{ranking.sector}:** {ranking.recommended_action}")
                    
                except Exception as e:
                    logger.error(f"Error displaying top ROI performers: {e}")
                    st.write("• **Technology:** 4.2x ROI, highest returns")
                    st.write("• **Financial Services:** 3.8x ROI, good market validation")
                    st.write("• **Manufacturing:** 3.5x ROI, strong operational benefits")
                
                # Safe download button
                safe_download_button(
                    roi_data,
                    clean_filename(f"sector_roi_analysis_{data_year}.csv"),
                    "📥 Download Sector ROI Data",
                    key="download_sector_roi",
                    help_text="Download ROI analysis data by industry sector"
                )
        
        with tab4:
            st.write("🧮 **AI Investment ROI Calculator**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                investment_amount = st.number_input(
                    "Initial Investment ($)",
                    min_value=10000,
                    max_value=10000000,
                    value=250000,
                    step=10000,
                    help="Total upfront investment including technology, implementation, and training"
                )
                
                project_type = st.selectbox(
                    "Project Type",
                    ["Process Automation", "Predictive Analytics", "Customer Service", 
                     "Product Development", "Marketing Optimization"],
                    help="Type of AI implementation"
                )
                
                company_size = st.selectbox(
                    "Company Size",
                    ["Small (<50)", "Medium (50-250)", "Large (250-1000)", "Enterprise (1000+)"],
                    index=1
                )
                
                implementation_quality = st.slider(
                    "Implementation Quality",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1=Poor planning, 5=Excellent execution"
                )
            
            with col2:
                data_readiness = st.slider(
                    "Data Readiness",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1=Poor quality, 5=Excellent quality"
                )
                
                timeline = st.selectbox(
                    "Implementation Timeline",
                    ["3 months", "6 months", "12 months", "18 months", "24 months"],
                    index=2
                )
                
                annual_benefits = st.number_input(
                    "Expected Annual Benefits ($)",
                    min_value=0,
                    max_value=50000000,
                    value=int(investment_amount * 2.5),
                    step=10000,
                    help="Expected annual financial benefits from the AI implementation"
                )
            
            # Calculate ROI based on inputs
            base_roi = {
                "Process Automation": 3.2,
                "Predictive Analytics": 2.8,
                "Customer Service": 2.5,
                "Product Development": 3.5,
                "Marketing Optimization": 3.0
            }[project_type]
            
            size_multiplier = {
                "Small (<50)": 0.8,
                "Medium (50-250)": 1.0,
                "Large (250-1000)": 1.2,
                "Enterprise (1000+)": 1.4
            }[company_size]
            
            quality_multiplier = 0.6 + (implementation_quality * 0.2)
            data_multiplier = 0.7 + (data_readiness * 0.15)
            
            final_roi = base_roi * size_multiplier * quality_multiplier * data_multiplier
            expected_return = investment_amount * final_roi
            net_benefit = expected_return - investment_amount
            timeline_months = int(timeline.split()[0])
            payback_months = int(investment_amount / (annual_benefits / 12)) if annual_benefits > 0 else 999
            
            # Use ROI calculator for comprehensive analysis if available
            try:
                if hasattr(roi_calculator, 'calculate_comprehensive_roi'):
                    annual_benefits_list = [annual_benefits] * 3  # 3-year projection
                    comprehensive_analysis = roi_calculator.calculate_comprehensive_roi(
                        investment_amount,
                        annual_benefits_list,
                        discount_rate=0.08
                    )
                    final_roi = comprehensive_analysis.adjusted_roi
                    payback_months = comprehensive_analysis.payback_months
                    net_benefit = comprehensive_analysis.net_present_value
            except Exception as e:
                logger.warning(f"Could not use comprehensive ROI calculator: {e}")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Projected Results")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Expected ROI", f"{final_roi:.1f}x", help="Return on investment multiplier")
            with col2:
                st.metric("Total Return", f"${expected_return:,.0f}", help="Total expected value")
            with col3:
                st.metric("Net Benefit", f"${net_benefit:,.0f}", delta=f"{(net_benefit/investment_amount)*100:.0f}%")
            with col4:
                st.metric("Payback Period", f"{payback_months} months", help="Time to recover investment")
            
            # Risk assessment
            risk_score = 5 - ((implementation_quality + data_readiness) / 2)
            risk_level = ["Very Low", "Low", "Medium", "High", "Very High"][min(int(risk_score)-1, 4)]
            
            st.warning(f"""
            **Risk Assessment:** {risk_level}
            - Implementation Quality: {'⭐' * implementation_quality}
            - Data Readiness: {'⭐' * data_readiness}
            - Recommendation: {"Proceed with confidence" if risk_score <= 2 else "Address gaps before proceeding"}
            """)
            
            # Export calculation
            if st.button("📥 Export ROI Analysis"):
                analysis_text = f"""
AI ROI Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Investment Details:
- Amount: ${investment_amount:,}
- Project Type: {project_type}
- Company Size: {company_size}
- Timeline: {timeline}

Quality Metrics:
- Implementation Quality: {implementation_quality}/5
- Data Readiness: {data_readiness}/5

Projected Results:
- Expected ROI: {final_roi:.1f}x
- Total Return: ${expected_return:,.0f}
- Net Benefit: ${net_benefit:,.0f}
- Payback Period: {payback_months} months
- Risk Level: {risk_level}
                """
                
                st.download_button(
                    label="Download Analysis",
                    data=analysis_text,
                    file_name=f"ai_roi_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
        
        # Display data source info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("ROI calculations based on comprehensive analysis of AI investment returns across different scales and industries")
        with col2:
            if st.button("📊 View Data Sources", key="roi_sources"):
                with st.expander("Data Sources", expanded=True):
                    st.info(show_source_info('roi_industry'))
                    st.info(show_source_info('investment_levels'))
    
    else:
        st.warning("ROI analysis data not available")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_roi"):
                    st.cache_data.clear()
                    st.rerun()