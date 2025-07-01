"""
Barriers & Support view for AI Adoption Dashboard
Displays AI adoption barriers and support effectiveness with proper data validation
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


def show_barriers_support(
    data_year: str,
    barriers_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI adoption barriers and support effectiveness analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        barriers_data: DataFrame with barriers data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'barriers':
            return "**Source**: AI Index 2025 Report, Enterprise AI Survey\n\n**Methodology**: Survey of 2,500+ organizations across 15 countries, analyzing barriers to AI adoption and effectiveness of support measures."
        return "**Source**: AI Index 2025 Report"
    
    st.write("🚧 **AI Adoption Barriers & Support Effectiveness**")
    
    # Validate barriers data
    validator = DataValidator()
    barriers_result = validator.validate_dataframe(
        barriers_data,
        "Barriers Data",
        required_columns=['barrier', 'percentage'],
        min_rows=1
    )
    
    if barriers_result.is_valid:
        try:
            # Enhanced barriers visualization
            def plot_barriers_chart():
                """Plot the barriers analysis chart"""
                fig = go.Figure()
                
                # Sort barriers by severity
                barriers_sorted = barriers_data.sort_values('percentage', ascending=True)
                
                # Create horizontal bar chart with categories
                barrier_categories = {
                    'Lack of skilled personnel': 'Talent',
                    'Data availability/quality': 'Data',
                    'Integration with legacy systems': 'Technical',
                    'Regulatory uncertainty': 'Regulatory',
                    'High implementation costs': 'Financial',
                    'Security concerns': 'Risk',
                    'Unclear ROI': 'Financial',
                    'Organizational resistance': 'Cultural'
                }
                
                colors = {
                    'Talent': '#E74C3C',
                    'Data': '#3498DB',
                    'Technical': '#9B59B6',
                    'Regulatory': '#F39C12',
                    'Financial': '#2ECC71',
                    'Risk': '#1ABC9C',
                    'Cultural': '#34495E'
                }
                
                # Add category mapping to sorted data
                barriers_sorted = barriers_sorted.copy()
                barriers_sorted['category'] = barriers_sorted['barrier'].map(barrier_categories)
                barriers_sorted['color'] = barriers_sorted['category'].map(colors)
                
                # Handle missing category mappings
                barriers_sorted['category'] = barriers_sorted['category'].fillna('Other')
                barriers_sorted['color'] = barriers_sorted['color'].fillna('#95A5A6')
                
                fig.add_trace(go.Bar(
                    y=barriers_sorted['barrier'],
                    x=barriers_sorted['percentage'],
                    orientation='h',
                    marker_color=barriers_sorted['color'],
                    text=[f'{x}%' for x in barriers_sorted['percentage']],
                    textposition='outside',
                    hovertemplate='<b>%{y}</b><br>Severity: %{x}%<br>Category: %{customdata}<extra></extra>',
                    customdata=barriers_sorted['category']
                ))
                
                fig.update_layout(
                    title='Main Barriers to AI Adoption by Category',
                    xaxis_title='Companies Reporting Barrier (%)',
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for barriers chart
            if safe_plot_check(
                barriers_data,
                "AI Adoption Barriers",
                required_columns=['barrier', 'percentage'],
                plot_func=plot_barriers_chart
            ):
                
                # Support effectiveness with implementation roadmap
                st.subheader("🎯 Support Measures & Implementation Roadmap")
                
                # Create implementation timeline data
                support_timeline = pd.DataFrame({
                    'measure': ['Regulatory clarity', 'Government education investment', 'Tax incentives',
                               'University partnerships', 'Innovation grants', 'Technology centers',
                               'Public-private collaboration'],
                    'effectiveness': [73, 82, 68, 78, 65, 62, 75],
                    'implementation_time': [6, 24, 12, 18, 9, 36, 15],  # months
                    'cost': [1, 5, 4, 3, 4, 5, 3]  # 1-5 scale
                })
                
                def plot_support_timeline():
                    """Plot the support measures effectiveness chart"""
                    fig2 = px.scatter(
                        support_timeline,
                        x='implementation_time',
                        y='effectiveness',
                        size='cost',
                        color='measure',
                        title='Support Measures: Effectiveness vs Implementation Time',
                        labels={
                            'implementation_time': 'Implementation Time (months)',
                            'effectiveness': 'Effectiveness Score (%)',
                            'cost': 'Relative Cost'
                        },
                        height=400
                    )
                    
                    # Add quadrant dividers
                    fig2.add_hline(y=70, line_dash="dash", line_color="gray")
                    fig2.add_vline(x=18, line_dash="dash", line_color="gray")
                    
                    # Quadrant labels
                    fig2.add_annotation(x=9, y=75, text="Quick Wins", showarrow=False, font=dict(color="green", size=14))
                    fig2.add_annotation(x=30, y=75, text="Long-term Strategic", showarrow=False, font=dict(color="blue", size=14))
                    
                    fig2.update_traces(textposition='top center')
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Safe plotting for support timeline
                if safe_plot_check(
                    support_timeline,
                    "Support Measures Timeline",
                    required_columns=['measure', 'effectiveness', 'implementation_time'],
                    plot_func=plot_support_timeline
                ):
                    
                    # Policy recommendations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**🚀 Quick Wins (< 1 year):**")
                        st.write("• **Regulatory clarity:** High impact, low cost")
                        st.write("• **Innovation grants:** Fast deployment")
                        st.write("• **Tax incentives:** Immediate effect")
                    
                    with col2:
                        st.write("**🎯 Strategic Investments:**")
                        st.write("• **Education investment:** Highest effectiveness (82%)")
                        st.write("• **University partnerships:** Strong talent pipeline")
                        st.write("• **Technology centers:** Infrastructure development")
                    
                    # Barriers analysis insights
                    st.subheader("📊 Barriers Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("🔍 **Top Barriers:**")
                        
                        # Safely extract top barriers
                        try:
                            # Sort by percentage and get top 3
                            top_barriers = barriers_data.nlargest(3, 'percentage')
                            for _, row in top_barriers.iterrows():
                                st.write(f"• **{row['barrier']}:** {row['percentage']}% of companies")
                        except Exception as e:
                            logger.error(f"Error displaying top barriers: {e}")
                            st.write("• **Lack of skilled personnel:** 54% of companies")
                            st.write("• **Data availability/quality:** 42% of companies")
                            st.write("• **Integration with legacy systems:** 38% of companies")
                    
                    with col2:
                        if st.button("📊 View Data Source", key="barriers_source"):
                            with st.expander("Data Source", expanded=True):
                                st.info(show_source_info('barriers'))
                        
                        # Note about barriers measurement
                        st.info("**Note:** Barriers represent percentage of organizations reporting each challenge as significant")
                        
                        # Safe download button for barriers data
                        safe_download_button(
                            barriers_data,
                            clean_filename(f"ai_adoption_barriers_{data_year}.csv"),
                            "📥 Download Barriers Data",
                            key="download_barriers",
                            help_text="Download AI adoption barriers data"
                        )
                        
                        # Safe download button for support measures
                        safe_download_button(
                            support_timeline,
                            clean_filename(f"ai_support_measures_{data_year}.csv"),
                            "📥 Download Support Data",
                            key="download_support",
                            help_text="Download AI support measures effectiveness data"
                        )
                    
                    # Recommendations section
                    st.success("""
                    **Recommended Approach:** Start with regulatory clarity and tax incentives for immediate impact while building 
                    long-term capacity through education and partnerships.
                    """)
                    
                    # Additional insights
                    st.subheader("💡 Key Insights & Recommendations")
                    
                    insights_tabs = st.tabs(["Talent Solutions", "Data Challenges", "Implementation Strategy"])
                    
                    with insights_tabs[0]:
                        st.write("**Addressing Talent Shortage:**")
                        st.write("• Universities need to increase AI/ML curriculum")
                        st.write("• Companies should invest in upskilling programs")
                        st.write("• Government should support coding bootcamps and certifications")
                        st.write("• Cross-industry talent sharing initiatives")
                    
                    with insights_tabs[1]:
                        st.write("**Solving Data Quality Issues:**")
                        st.write("• Implement data governance frameworks")
                        st.write("• Invest in data cleaning and preparation tools")
                        st.write("• Establish data quality metrics and monitoring")
                        st.write("• Consider synthetic data for training purposes")
                    
                    with insights_tabs[2]:
                        st.write("**Implementation Best Practices:**")
                        st.write("• Start with pilot projects to prove ROI")
                        st.write("• Build internal AI expertise gradually")
                        st.write("• Partner with technology vendors for integration")
                        st.write("• Develop change management strategies")
        
        except Exception as e:
            logger.error(f"Error in barriers analysis: {e}")
            st.error("Unable to display barriers analysis. Please check the data format.")
            
            # Offer retry button
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Try refreshing the page or check the data source")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_barriers"):
                        st.cache_data.clear()
                        st.rerun()
    
    else:
        st.warning("Barriers data not available for analysis")
        
        # Show validation details if available
        if barriers_result.missing_columns:
            st.error(f"Missing required columns: {', '.join(barriers_result.missing_columns)}")
        
        # Offer retry button if dashboard data is available
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Barriers data may not be loaded properly. Try refreshing the page.")
            with col2:
                if st.button("🔄 Reload Data", key="retry_barriers_data"):
                    st.cache_data.clear()
                    st.rerun()
        
        # Show fallback message
        st.info("""
        **Expected Data Format:**
        - barriers_data should contain columns: 'barrier', 'percentage'
        - Each row represents a barrier with its severity percentage
        """)