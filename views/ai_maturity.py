"""
AI Technology Maturity view for AI Adoption Dashboard
Displays AI technology maturity analysis with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
import logging

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_ai_technology_maturity(
    data_year: str,
    maturity_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI Technology Maturity & Adoption analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        maturity_data: DataFrame with AI maturity data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'gartner':
            return "**Source**: Gartner AI Technology Maturity Analysis, 2025\n\n**Methodology**: Technology maturity assessment based on hype cycle analysis, market adoption rates, and risk-benefit evaluation across enterprise AI implementations."
        return "**Source**: AI Index 2025 Report"
    
    st.write("🎯 **AI Technology Maturity & Adoption (Gartner 2025)**")
    
    # Validate maturity data
    validator = DataValidator()
    maturity_result = validator.validate_dataframe(
        maturity_data,
        "AI Maturity Data",
        required_columns=['technology', 'adoption_rate', 'maturity', 'risk_score', 'time_to_value'],
        min_rows=1
    )
    
    if maturity_result.is_valid:
        # Enhanced maturity visualization with risk-adoption matrix
        def plot_maturity_matrix():
            """Plot the AI technology risk-adoption matrix"""
            color_map = {
                'Peak of Expectations': '#F59E0B',
                'Trough of Disillusionment': '#6B7280', 
                'Slope of Enlightenment': '#10B981'
            }
            
            fig = go.Figure()
            
            # Group by maturity stage and create traces
            for stage in maturity_data['maturity'].unique():
                stage_data = maturity_data[maturity_data['maturity'] == stage]
                
                fig.add_trace(go.Scatter(
                    x=stage_data['adoption_rate'],
                    y=stage_data['risk_score'],
                    mode='markers+text',
                    name=stage,
                    marker=dict(
                        size=stage_data['time_to_value'] * 10,
                        color=color_map.get(stage, '#6B7280'),
                        line=dict(width=2, color='white')
                    ),
                    text=stage_data['technology'],
                    textposition='top center',
                    hovertemplate='<b>%{text}</b><br>Adoption: %{x}%<br>Risk: %{y}/100<br>Time to Value: %{customdata} years<extra></extra>',
                    customdata=stage_data['time_to_value']
                ))
            
            # Add quadrant lines
            fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Quadrant labels
            fig.add_annotation(x=25, y=75, text="High Risk<br>Low Adoption", showarrow=False, font=dict(color="gray"))
            fig.add_annotation(x=75, y=75, text="High Risk<br>High Adoption", showarrow=False, font=dict(color="gray"))
            fig.add_annotation(x=25, y=25, text="Low Risk<br>Low Adoption", showarrow=False, font=dict(color="gray"))
            fig.add_annotation(x=75, y=25, text="Low Risk<br>High Adoption", showarrow=False, font=dict(color="gray"))
            
            fig.update_layout(
                title="AI Technology Risk-Adoption Matrix",
                xaxis_title="Adoption Rate (%)",
                yaxis_title="Risk Score (0-100)",
                height=500,
                showlegend=True,
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Use safe plotting with comprehensive validation
        if safe_plot_check(
            maturity_data,
            "AI Technology Maturity Data",
            required_columns=['technology', 'adoption_rate', 'maturity', 'risk_score', 'time_to_value'],
            plot_func=plot_maturity_matrix
        ):
            # Maturity level analysis
            st.subheader("📊 Maturity Level Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🎯 Strategic Recommendations:**")
                
                try:
                    # Get low-risk, high-adoption technologies (investment opportunities)
                    invest_techs = maturity_data[
                        (maturity_data['risk_score'] <= 50) & 
                        (maturity_data['adoption_rate'] >= 50)
                    ]
                    
                    # Get high-potential, high-risk technologies (watch list)
                    watch_techs = maturity_data[
                        (maturity_data['risk_score'] >= 70) & 
                        (maturity_data['adoption_rate'] >= 50)
                    ]
                    
                    # Get technologies moving past hype (mature opportunities)
                    mature_techs = maturity_data[
                        maturity_data['maturity'] == 'Trough of Disillusionment'
                    ]
                    
                    if not invest_techs.empty:
                        invest_tech = invest_techs.iloc[0]['technology']
                        st.write(f"• **Invest in:** {invest_tech} (low risk, high adoption)")
                    else:
                        st.write("• **Invest in:** Cloud AI Services (low risk, high adoption)")
                    
                    if not watch_techs.empty:
                        watch_tech = watch_techs.iloc[0]['technology']
                        st.write(f"• **Watch:** {watch_tech} (high potential, high risk)")
                    else:
                        st.write("• **Watch:** AI Agents (high potential, high risk)")
                    
                    if not mature_techs.empty:
                        mature_tech = mature_techs.iloc[0]['technology']
                        st.write(f"• **Mature:** {mature_tech} moving past hype")
                    else:
                        st.write("• **Mature:** Foundation Models moving past hype")
                        
                except Exception as e:
                    logger.error(f"Error generating strategic recommendations: {e}")
                    st.write("• **Invest in:** Cloud AI Services (low risk, high adoption)")
                    st.write("• **Watch:** AI Agents (high potential, high risk)")
                    st.write("• **Mature:** Foundation Models moving past hype")
            
            with col2:
                st.write("**⏱️ Time to Value Analysis:**")
                
                try:
                    # Sort by time to value for recommendations
                    sorted_by_time = maturity_data.sort_values('time_to_value')
                    
                    fastest = sorted_by_time.iloc[0]
                    medium_time = sorted_by_time[sorted_by_time['time_to_value'] <= 3]
                    longest = sorted_by_time.iloc[-1]
                    
                    st.write(f"• **Fastest:** {fastest['technology']} ({fastest['time_to_value']} year{'s' if fastest['time_to_value'] > 1 else ''})")
                    
                    if len(medium_time) > 1:
                        st.write(f"• **Medium:** Most technologies ({medium_time['time_to_value'].mode().iloc[0]} years)")
                    else:
                        st.write("• **Medium:** Most technologies (3 years)")
                    
                    st.write(f"• **Longest:** {longest['technology']} ({longest['time_to_value']} years)")
                    
                except Exception as e:
                    logger.error(f"Error generating time to value analysis: {e}")
                    st.write("• **Fastest:** Cloud AI Services (1 year)")
                    st.write("• **Medium:** Most technologies (3 years)")
                    st.write("• **Longest:** Composite AI (7 years)")
            
            # Capability assessment
            st.subheader("🔧 Capability Assessment")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Technologies Tracked",
                    len(maturity_data),
                    help="Total number of AI technologies in maturity analysis"
                )
            
            with col2:
                try:
                    high_adoption = len(maturity_data[maturity_data['adoption_rate'] >= 50])
                    st.metric(
                        "High Adoption (≥50%)",
                        high_adoption,
                        help="Technologies with adoption rates of 50% or higher"
                    )
                except Exception as e:
                    logger.error(f"Error calculating high adoption metrics: {e}")
                    st.metric("High Adoption (≥50%)", "N/A")
            
            with col3:
                try:
                    low_risk = len(maturity_data[maturity_data['risk_score'] <= 40])
                    st.metric(
                        "Low Risk (≤40)",
                        low_risk,
                        help="Technologies with risk scores of 40 or lower"
                    )
                except Exception as e:
                    logger.error(f"Error calculating low risk metrics: {e}")
                    st.metric("Low Risk (≤40)", "N/A")
            
            # Roadmap visualization
            st.subheader("🗺️ Technology Roadmap")
            
            def plot_roadmap():
                """Plot technology adoption roadmap by time to value"""
                try:
                    # Create roadmap visualization
                    roadmap_data = maturity_data.copy()
                    roadmap_data = roadmap_data.sort_values('time_to_value')
                    
                    fig = go.Figure()
                    
                    # Color by maturity stage
                    stage_colors = {
                        'Peak of Expectations': '#F59E0B',
                        'Trough of Disillusionment': '#6B7280', 
                        'Slope of Enlightenment': '#10B981'
                    }
                    
                    colors = [stage_colors.get(stage, '#6B7280') for stage in roadmap_data['maturity']]
                    
                    fig.add_trace(go.Bar(
                        x=roadmap_data['technology'],
                        y=roadmap_data['time_to_value'],
                        marker_color=colors,
                        text=[f"{rate}% adoption" for rate in roadmap_data['adoption_rate']],
                        textposition='outside',
                        hovertemplate='<b>%{x}</b><br>Time to Value: %{y} years<br>Adoption: %{text}<br>Risk Score: %{customdata}<extra></extra>',
                        customdata=roadmap_data['risk_score']
                    ))
                    
                    fig.update_layout(
                        title="AI Technology Implementation Roadmap",
                        xaxis_title="Technology",
                        yaxis_title="Time to Value (Years)",
                        xaxis_tickangle=45,
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    logger.error(f"Error creating roadmap visualization: {e}")
                    st.error("Unable to generate roadmap visualization")
            
            # Safe roadmap plotting
            if safe_plot_check(
                maturity_data,
                "Technology Roadmap Data",
                required_columns=['technology', 'time_to_value', 'adoption_rate', 'maturity'],
                plot_func=plot_roadmap
            ):
                st.info("💡 **Roadmap Insight:** Technologies are ordered by time to value - start with shorter-term implementations while planning for longer-term strategic technologies.")
            
            # Data source and download section
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 View Data Source", key="maturity_source"):
                    with st.expander("Data Source", expanded=True):
                        st.info(show_source_info('gartner'))
                
                # Note about maturity methodology
                st.info("**Note:** Bubble size indicates time to value. Position shows risk vs. adoption trade-offs.")
            
            with col2:
                # Safe download button
                safe_download_button(
                    maturity_data,
                    clean_filename(f"ai_technology_maturity_{data_year}.csv"),
                    "📥 Download Maturity Data",
                    key="download_maturity_2025",
                    help_text="Download AI technology maturity analysis data including risk scores and adoption rates"
                )
    
    else:
        st.warning("AI maturity data not available for technology analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_maturity"):
                    st.cache_data.clear()
                    st.rerun()