"""
Productivity Research view for AI Adoption Dashboard
Displays AI productivity impact research with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import logging

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_productivity_research(
    data_year: str,
    productivity_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI productivity impact research analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        productivity_data: DataFrame with productivity trend data
        dashboard_data: Full dashboard data dict for additional datasets
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'ai_index':
            return "**Source**: AI Index 2025 Report\n\n**Methodology**: Comprehensive analysis of AI productivity impact across skill levels and economic sectors, drawing from multiple academic and industry studies."
        elif source_type == 'academic':
            return "**Source**: Academic Research Compilation\n\n**Studies Include**: Acemoglu (2024), Brynjolfsson et al. (2023), Richmond Fed analysis, and peer-reviewed productivity studies."
        return "**Source**: AI Index 2025 Report"
    
    st.write("📊 **AI Productivity Impact Research**")
    
    # Create tabs for different productivity views
    tab1, tab2, tab3 = st.tabs(["Historical Context", "Skill-Level Impact", "Economic Estimates"])
    
    with tab1:
        st.write("### The Productivity Paradox: Demographics vs Technology")
        
        # Validate productivity data
        validator = DataValidator()
        productivity_result = validator.validate_dataframe(
            productivity_data,
            "Productivity Trend Data",
            required_columns=['year', 'productivity_growth'],
            min_rows=1
        )
        
        if productivity_result.is_valid:
            
            def plot_productivity_paradox():
                """Plot the historical productivity paradox chart"""
                fig = go.Figure()
                
                # Productivity growth line
                fig.add_trace(go.Scatter(
                    x=productivity_data['year'], 
                    y=productivity_data['productivity_growth'],
                    mode='lines+markers',
                    name='Productivity Growth (%)',
                    line=dict(width=3, color='#3B82F6'),
                    yaxis='y',
                    hovertemplate='Year: %{x}<br>Productivity Growth: %{y}%<extra></extra>'
                ))
                
                # Young workers share if available
                if 'young_workers_share' in productivity_data.columns:
                    fig.add_trace(go.Scatter(
                        x=productivity_data['year'], 
                        y=productivity_data['young_workers_share'],
                        mode='lines+markers',
                        name='Young Workers Share (25-34)',
                        line=dict(width=3, color='#EF4444'),
                        yaxis='y2',
                        hovertemplate='Year: %{x}<br>Young Workers: %{y}%<extra></extra>'
                    ))
                
                fig.update_layout(
                    title="The Productivity Paradox: Demographics vs Technology",
                    xaxis_title="Year",
                    yaxis=dict(title="Productivity Growth (%)", side="left"),
                    yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y") if 'young_workers_share' in productivity_data.columns else None,
                    height=500,
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            required_cols = ['year', 'productivity_growth']
            if 'young_workers_share' in productivity_data.columns:
                required_cols.append('young_workers_share')
                
            if safe_plot_check(
                productivity_data,
                "Productivity Trend Data",
                required_columns=required_cols,
                plot_func=plot_productivity_paradox
            ):
                # Insights and analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("""
                    **📈 Historical Context:**
                    - Productivity growth peaked in the 1990s-2000s (dot-com era)
                    - Significant decline since 2010 despite technological advances
                    - AI may represent the next productivity frontier
                    """)
                
                with col2:
                    if st.button("📊 View Data Source", key="productivity_source"):
                        with st.expander("Data Source", expanded=True):
                            st.info(show_source_info('ai_index'))
                    
                    # Safe download button
                    safe_download_button(
                        productivity_data,
                        clean_filename(f"productivity_trends_{data_year}.csv"),
                        "📥 Download Trend Data",
                        key="download_productivity_trends",
                        help_text="Download historical productivity trend data"
                    )
        
        else:
            st.warning("Productivity trend data not available for historical analysis")
            # Offer retry button if needed
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Try refreshing the page or check the data source")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_productivity"):
                        st.cache_data.clear()
                        st.rerun()
    
    with tab2:
        st.write("### AI Impact by Worker Skill Level")
        
        # Get productivity by skill data from dashboard_data
        productivity_by_skill = dashboard_data.get('productivity_by_skill', pd.DataFrame()) if dashboard_data else pd.DataFrame()
        
        # Validate skill-level productivity data
        skill_result = validator.validate_dataframe(
            productivity_by_skill,
            "Skill-Level Productivity Data",
            required_columns=['skill_level', 'productivity_gain'],
            min_rows=1
        )
        
        if skill_result.is_valid:
            
            def plot_skill_impact():
                """Plot AI impact by skill level"""
                # Determine available columns for plotting
                y_columns = ['productivity_gain']
                if 'skill_gap_reduction' in productivity_by_skill.columns:
                    y_columns.append('skill_gap_reduction')
                
                fig = px.bar(
                    productivity_by_skill,
                    x='skill_level',
                    y=y_columns,
                    title='AI Impact by Worker Skill Level',
                    labels={'value': 'Percentage (%)', 'variable': 'Impact Type'},
                    barmode='group',
                    color_discrete_map={
                        'productivity_gain': '#2ECC71', 
                        'skill_gap_reduction': '#3498DB'
                    }
                )
                
                fig.update_layout(
                    height=400,
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            required_skill_cols = ['skill_level', 'productivity_gain']
            if 'skill_gap_reduction' in productivity_by_skill.columns:
                required_skill_cols.append('skill_gap_reduction')
            
            if safe_plot_check(
                productivity_by_skill,
                "Skill-Level Impact Data",
                required_columns=required_skill_cols,
                plot_func=plot_skill_impact
            ):
                # Key findings
                st.success("""
                **✅ AI Index 2025 Finding:** AI provides the greatest productivity boost to low-skilled workers (14%), 
                helping to narrow skill gaps and potentially reduce workplace inequality.
                """)
                
                # Detailed insights
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("🎯 **Impact by Skill Level:**")
                    try:
                        for _, row in productivity_by_skill.iterrows():
                            productivity_gain = row.get('productivity_gain', 0)
                            skill_gap_reduction = row.get('skill_gap_reduction', 'N/A')
                            skill_gap_text = f", {skill_gap_reduction}% skill gap reduction" if skill_gap_reduction != 'N/A' else ""
                            st.write(f"• **{row['skill_level']}:** {productivity_gain}% productivity gain{skill_gap_text}")
                    except Exception as e:
                        logger.error(f"Error displaying skill impact: {e}")
                        st.write("• **Low-skilled:** 14% productivity gain")
                        st.write("• **Medium-skilled:** 9% productivity gain")
                        st.write("• **High-skilled:** 5% productivity gain")
                
                with col2:
                    # Safe download button
                    safe_download_button(
                        productivity_by_skill,
                        clean_filename(f"ai_skill_impact_{data_year}.csv"),
                        "📥 Download Skill Data",
                        key="download_skill_impact",
                        help_text="Download AI impact data by skill level"
                    )
        
        else:
            st.warning("Skill-level productivity data not available")
            # Show fallback content with retry option
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Skill-level impact data may not be loaded")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_skill_data"):
                        st.cache_data.clear()
                        st.rerun()
    
    with tab3:
        st.write("### Economic Impact Estimates")
        
        # Get AI productivity estimates from dashboard_data
        ai_productivity_estimates = dashboard_data.get('ai_productivity_estimates', pd.DataFrame()) if dashboard_data else pd.DataFrame()
        
        # Validate economic estimates data
        estimates_result = validator.validate_dataframe(
            ai_productivity_estimates,
            "Economic Impact Estimates",
            required_columns=['source', 'annual_impact'],
            min_rows=1
        )
        
        if estimates_result.is_valid:
            
            def plot_economic_estimates():
                """Plot economic impact estimates"""
                fig = px.bar(
                    ai_productivity_estimates,
                    x='source',
                    y='annual_impact',
                    title='AI Productivity Impact Estimates: Academic vs Industry',
                    color='annual_impact',
                    color_continuous_scale='RdYlBu_r',
                    text='annual_impact'
                )
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                fig.update_layout(
                    height=450,
                    xaxis_tickangle=45,
                    hovermode='x'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            if safe_plot_check(
                ai_productivity_estimates,
                "Economic Estimates Data",
                required_columns=['source', 'annual_impact'],
                plot_func=plot_economic_estimates
            ):
                # Analysis and insights
                st.info("""
                **📊 Note on Estimates:**
                - Conservative estimates (0.07-0.1%) focus on task-level automation
                - Optimistic estimates (1.5-2.5%) assume economy-wide transformation  
                - Actual impact depends on implementation quality and complementary investments
                """)
                
                # Detailed breakdown
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("📈 **Research Insights:**")
                    try:
                        # Sort by impact and show key findings
                        sorted_estimates = ai_productivity_estimates.sort_values('annual_impact', ascending=False)
                        for _, row in sorted_estimates.head(3).iterrows():
                            impact_category = "Optimistic" if row['annual_impact'] > 1.0 else "Conservative"
                            st.write(f"• **{row['source']}:** {row['annual_impact']}% ({impact_category})")
                    except Exception as e:
                        logger.error(f"Error displaying estimates: {e}")
                        st.write("• **Goldman Sachs:** 2.5% (Optimistic)")
                        st.write("• **McKinsey:** 2.0% (Optimistic)")
                        st.write("• **Brynjolfsson et al.:** 1.5% (Moderate)")
                
                with col2:
                    if st.button("📊 View Research Sources", key="estimates_source"):
                        with st.expander("Research Sources", expanded=True):
                            st.info(show_source_info('academic'))
                    
                    # Safe download button
                    safe_download_button(
                        ai_productivity_estimates,
                        clean_filename(f"ai_economic_estimates_{data_year}.csv"),
                        "📥 Download Estimates",
                        key="download_economic_estimates",
                        help_text="Download AI economic impact estimates"
                    )
        
        else:
            st.warning("Economic impact estimates not available")
            # Show fallback content with retry option
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Economic estimates data may not be loaded")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_estimates"):
                        st.cache_data.clear()
                        st.rerun()
    
    # Overall summary section
    st.write("---")
    st.write("### 🔍 **Key Research Findings**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Greatest Impact Sector",
            value="Low-Skilled Workers",
            delta="14% productivity gain"
        )
    
    with col2:
        st.metric(
            label="Estimated Range",
            value="0.07% - 2.5%",
            delta="Annual productivity growth"
        )
    
    with col3:
        st.metric(
            label="Implementation Key",
            value="Quality & Investment",
            delta="Determines actual impact"
        )