"""
Labor Impact view for AI Adoption Dashboard
Displays AI's impact on jobs and workers with proper data validation
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


def show_labor_impact(
    data_year: str,
    labor_impact: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI's impact on jobs and workers with comprehensive analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        labor_impact: DataFrame with AI perception/labor impact data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info() -> str:
        """Return source information for labor impact data"""
        return "**Source**: AI Index Report 2025\n\n**Methodology**: Global survey data on AI perception and workforce impact, including generational analysis and skill-based assessments."
    
    st.write("👥 **AI's Impact on Jobs and Workers (AI Index Report 2025)**")
    
    # Validate labor impact data
    validator = DataValidator()
    labor_result = validator.validate_dataframe(
        labor_impact,
        "Labor Impact Data",
        required_columns=['generation'],
        min_rows=1
    )
    
    if labor_result.is_valid:
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
                label="Skill Gap Narrowing", 
                value="Confirmed", 
                delta="Low-skilled benefit most",
                help="AI helps reduce inequality"
            )
        
        with col4:
            st.metric(
                label="Productivity Boost", 
                value="14%", 
                delta="For low-skilled workers",
                help="Highest gains for entry-level"
            )
        
        # Create comprehensive labor impact visualization
        tab1, tab2, tab3, tab4 = st.tabs(["Generational Views", "Skill Impact", "Job Transformation", "Policy Implications"])
        
        with tab1:
            # Enhanced generational visualization
            def plot_generational_views():
                """Plot generational AI impact expectations"""
                fig = go.Figure()
                
                # Check if required columns exist
                has_job_change = 'expect_job_change' in labor_impact.columns
                has_job_replacement = 'expect_job_replacement' in labor_impact.columns
                
                if has_job_change:
                    # Job change expectations
                    fig.add_trace(go.Bar(
                        name='Expect Job Changes',
                        x=labor_impact['generation'],
                        y=labor_impact['expect_job_change'],
                        marker_color='#4ECDC4',
                        text=[f'{x}%' for x in labor_impact['expect_job_change']],
                        textposition='outside'
                    ))
                
                if has_job_replacement:
                    # Job replacement expectations
                    fig.add_trace(go.Bar(
                        name='Expect Job Replacement',
                        x=labor_impact['generation'],
                        y=labor_impact['expect_job_replacement'],
                        marker_color='#F38630',
                        text=[f'{x}%' for x in labor_impact['expect_job_replacement']],
                        textposition='outside'
                    ))
                
                if has_job_change and has_job_replacement:
                    # Add average lines
                    avg_change = labor_impact['expect_job_change'].mean()
                    avg_replace = labor_impact['expect_job_replacement'].mean()
                    
                    fig.add_hline(y=avg_change, line_dash="dash", line_color="rgba(78, 205, 196, 0.5)",
                                  annotation_text=f"Avg: {avg_change:.0f}%", annotation_position="right")
                    fig.add_hline(y=avg_replace, line_dash="dash", line_color="rgba(243, 134, 48, 0.5)",
                                  annotation_text=f"Avg: {avg_replace:.0f}%", annotation_position="right")
                
                fig.update_layout(
                    title="AI Job Impact Expectations by Generation",
                    xaxis_title="Generation",
                    yaxis_title="Percentage (%)",
                    barmode='group',
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting with validation
            required_cols = ['generation']
            if 'expect_job_change' in labor_impact.columns:
                required_cols.append('expect_job_change')
            if 'expect_job_replacement' in labor_impact.columns:
                required_cols.append('expect_job_replacement')
            
            if safe_plot_check(
                labor_impact,
                "Generational Labor Impact Data",
                required_columns=required_cols,
                plot_func=plot_generational_views
            ):
                # Generation insights
                st.info("""
                **Key Insights:**
                - **18pp gap** between Gen Z and Baby Boomers on job change expectations
                - Younger workers more aware of AI's transformative potential
                - All generations show concern but vary in urgency perception
                """)
        
        with tab2:
            # Skill impact analysis
            skill_impact = pd.DataFrame({
                'job_category': ['Entry-Level/Low-Skill', 'Mid-Level/Medium-Skill', 'Senior/High-Skill', 'Creative/Specialized'],
                'productivity_gain': [14, 9, 5, 7],
                'job_risk': [45, 38, 22, 15],
                'reskilling_need': [85, 72, 58, 65]
            })
            
            def plot_skill_impact():
                """Plot skill-based impact analysis"""
                fig = go.Figure()
                
                # Create grouped bar chart
                categories = ['Productivity Gain (%)', 'Job Risk (%)', 'Reskilling Need (%)']
                
                for i, category in enumerate(skill_impact['job_category']):
                    values = [
                        skill_impact.loc[i, 'productivity_gain'],
                        skill_impact.loc[i, 'job_risk'],
                        skill_impact.loc[i, 'reskilling_need']
                    ]
                    
                    fig.add_trace(go.Bar(
                        name=category,
                        x=categories,
                        y=values,
                        text=[f'{v}%' for v in values],
                        textposition='outside'
                    ))
                
                fig.update_layout(
                    title="AI Impact by Job Category",
                    xaxis_title="Impact Metric",
                    yaxis_title="Percentage (%)",
                    barmode='group',
                    height=400,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for skill impact
            if safe_plot_check(
                skill_impact,
                "Skill Impact Analysis",
                required_columns=['job_category', 'productivity_gain', 'job_risk', 'reskilling_need'],
                plot_func=plot_skill_impact
            ):
                st.success("""
                **Positive Finding:** AI provides greatest productivity boosts to entry-level workers, 
                potentially reducing workplace inequality and accelerating skill development.
                """)
                
                # Safe download button for skill impact data
                safe_download_button(
                    skill_impact,
                    clean_filename(f"ai_skill_impact_analysis_{data_year}.csv"),
                    "📥 Download Skill Impact Data",
                    key="download_skill_impact",
                    help_text="Download AI impact analysis by job category"
                )
        
        with tab3:
            # Job transformation timeline
            transformation_data = pd.DataFrame({
                'timeframe': ['0-2 years', '2-5 years', '5-10 years', '10+ years'],
                'jobs_affected': [15, 35, 60, 80],
                'new_jobs_created': [10, 25, 45, 65],
                'net_impact': [5, 10, 15, 15]
            })
            
            def plot_transformation_timeline():
                """Plot job transformation timeline"""
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=transformation_data['timeframe'],
                    y=transformation_data['jobs_affected'],
                    mode='lines+markers',
                    name='Jobs Affected',
                    line=dict(width=3, color='#E74C3C'),
                    marker=dict(size=10),
                    fill='tonexty'
                ))
                
                fig.add_trace(go.Scatter(
                    x=transformation_data['timeframe'],
                    y=transformation_data['new_jobs_created'],
                    mode='lines+markers',
                    name='New Jobs Created',
                    line=dict(width=3, color='#2ECC71'),
                    marker=dict(size=10),
                    fill='tozeroy'
                ))
                
                fig.update_layout(
                    title="Projected Job Market Transformation Timeline",
                    xaxis_title="Timeframe",
                    yaxis_title="Percentage of Workforce (%)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for transformation timeline
            if safe_plot_check(
                transformation_data,
                "Job Transformation Timeline",
                required_columns=['timeframe', 'jobs_affected', 'new_jobs_created'],
                plot_func=plot_transformation_timeline
            ):
                st.info("""
                **Transformation Patterns:**
                - Initial displacement in routine tasks
                - New roles emerge in AI management, ethics, and human-AI collaboration
                - Net positive effect expected long-term with proper reskilling
                """)
                
                # Safe download button for transformation data
                safe_download_button(
                    transformation_data,
                    clean_filename(f"job_transformation_timeline_{data_year}.csv"),
                    "📥 Download Transformation Data",
                    key="download_transformation",
                    help_text="Download job transformation timeline projections"
                )
        
        with tab4:
            # Policy recommendations
            st.write("**Policy Recommendations for Workforce Transition**")
            
            policy_areas = pd.DataFrame({
                'area': ['Education Reform', 'Reskilling Programs', 'Safety Nets', 
                        'Innovation Support', 'Regulation', 'Public-Private Partnership'],
                'priority': [95, 92, 85, 78, 72, 88],
                'current_investment': [45, 38, 52, 65, 58, 42]
            })
            
            def plot_policy_analysis():
                """Plot policy priority vs investment analysis"""
                fig = px.scatter(
                    policy_areas,
                    x='current_investment',
                    y='priority',
                    size='priority',
                    text='area',
                    title='Policy Priority vs Current Investment',
                    labels={'current_investment': 'Current Investment Level (%)', 
                           'priority': 'Priority Score (%)'},
                    height=400
                )
                
                # Add quadrant dividers
                fig.add_hline(y=85, line_dash="dash", line_color="gray")
                fig.add_vline(x=50, line_dash="dash", line_color="gray")
                
                # Quadrant labels
                fig.add_annotation(x=30, y=90, text="High Priority<br>Low Investment", 
                                  showarrow=False, font=dict(color="red"))
                fig.add_annotation(x=70, y=90, text="High Priority<br>High Investment", 
                                  showarrow=False, font=dict(color="green"))
                
                fig.update_traces(textposition='top center')
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for policy analysis
            if safe_plot_check(
                policy_areas,
                "Policy Analysis",
                required_columns=['area', 'priority', 'current_investment'],
                plot_func=plot_policy_analysis
            ):
                st.warning("""
                **Critical Gaps:**
                - **Education Reform** and **Reskilling Programs** are high priority but underfunded
                - Need 2-3x increase in workforce development investment
                - Public-private partnerships essential for scale
                """)
                
                # Safe download button for policy data
                safe_download_button(
                    policy_areas,
                    clean_filename(f"policy_recommendations_{data_year}.csv"),
                    "📥 Download Policy Data",
                    key="download_policy",
                    help_text="Download policy priority and investment analysis"
                )
        
        # Data source information and main download
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 View Data Source", key="labor_impact_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info())
        
        with col2:
            # Safe download button for main labor impact data
            safe_download_button(
                labor_impact,
                clean_filename(f"labor_impact_data_{data_year}.csv"),
                "📥 Download Labor Impact Data",
                key="download_labor_impact_main",
                help_text="Download AI labor impact and perception data"
            )
    
    else:
        # Error handling with validation result
        st.warning(f"Labor impact data not available: {labor_result.message}")
        
        # Offer retry button if dashboard_data is available
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source. Using AI perception data as fallback.")
            with col2:
                if st.button("🔄 Reload Data", key="retry_labor_impact"):
                    st.cache_data.clear()
                    st.rerun()
            
            # Try to use alternative data from dashboard_data
            try:
                ai_perception = dashboard_data.get('ai_perception', pd.DataFrame())
                if not ai_perception.empty:
                    st.info("Displaying available AI perception data as fallback")
                    # Display basic metrics even with limited data
                    st.write("📊 **Available AI Perception Insights**")
                    
                    # Basic fallback visualization if we have some data
                    if 'generation' in ai_perception.columns:
                        st.write("Generational data available for basic analysis")
                    else:
                        st.write("Limited data available - showing general insights")
                        
                        # Show static insights when data is unavailable
                        st.markdown("""
                        **Key Labor Impact Findings (AI Index 2025):**
                        - 60% of workers expect AI to change their jobs within 5 years
                        - 36% expect AI to replace their current jobs
                        - AI provides 14% productivity boost for low-skilled workers
                        - Skill gap narrowing confirmed - low-skilled workers benefit most
                        """)
                        
            except Exception as e:
                logger.error(f"Error accessing fallback data: {e}")
                st.error("Unable to display labor impact data. Please check data sources.")