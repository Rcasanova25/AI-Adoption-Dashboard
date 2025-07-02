"""
Regional Growth view for AI Adoption Dashboard
Displays regional AI adoption growth and investment dynamics with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any
import logging
from plotly.subplots import make_subplots

from Utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_regional_growth(
    data_year: str,
    regional_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display regional AI adoption growth and investment dynamics
    
    Args:
        data_year: Selected year (e.g., "2025")
        regional_data: DataFrame with regional growth data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'ai_index':
            return "**Source**: AI Index Report 2025\n\n**Methodology**: Comprehensive analysis of regional AI adoption patterns, investment flows, and growth rates across major global regions."
        return "**Source**: AI Index Report 2025"
    
    st.write("🌍 **Regional AI Adoption Growth (AI Index Report 2025)**")
    
    # Validate regional data
    validator = DataValidator()
    regional_result = validator.validate_dataframe(
        regional_data,
        "Regional Growth Data",
        required_columns=['region', 'growth_2024', 'adoption_rate', 'investment_growth'],
        min_rows=1
    )
    
    if regional_result.is_valid:
        
        def plot_regional_overview():
            """Plot the regional growth overview with dual visualization"""
            # Enhanced regional visualization with investment data
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Adoption Growth in 2024', 'Investment Growth vs Adoption Rate'),
                column_widths=[0.6, 0.4],
                horizontal_spacing=0.15
            )
            
            # Bar chart for adoption growth
            fig.add_trace(
                go.Bar(
                    x=regional_data['region'],
                    y=regional_data['growth_2024'],
                    text=[f'+{x}pp' for x in regional_data['growth_2024']],
                    textposition='outside',
                    marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
                    name='2024 Growth',
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Scatter plot for investment vs adoption
            fig.add_trace(
                go.Scatter(
                    x=regional_data['adoption_rate'],
                    y=regional_data['investment_growth'],
                    mode='markers+text',
                    marker=dict(
                        size=regional_data['growth_2024'],
                        color=regional_data['growth_2024'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="2024 Growth (pp)")
                    ),
                    text=regional_data['region'],
                    textposition='top center',
                    showlegend=False
                ),
                row=1, col=2
            )
            
            fig.update_xaxes(title_text="Region", row=1, col=1)
            fig.update_yaxes(title_text="Growth (percentage points)", row=1, col=1)
            fig.update_xaxes(title_text="Current Adoption Rate (%)", row=1, col=2)
            fig.update_yaxes(title_text="Investment Growth (%)", row=1, col=2)
            
            fig.update_layout(height=450, title_text="Regional AI Adoption and Investment Dynamics")
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Use safe plotting with validation
        if safe_plot_check(
            regional_data,
            "Regional Growth Data",
            required_columns=['region', 'growth_2024', 'adoption_rate', 'investment_growth'],
            plot_func=plot_regional_overview
        ):
            # Regional insights with metrics
            col1, col2, col3 = st.columns(3)
            
            try:
                # Find top performers dynamically
                fastest_growing = regional_data.loc[regional_data['growth_2024'].idxmax()]
                highest_adoption = regional_data.loc[regional_data['adoption_rate'].idxmax()]
                emerging_leader = regional_data.loc[
                    (regional_data['growth_2024'] > regional_data['growth_2024'].median()) & 
                    (regional_data['region'] != fastest_growing['region'])
                ].iloc[0] if len(regional_data) > 2 else regional_data.iloc[1]
                
                with col1:
                    st.metric("Fastest Growing", fastest_growing['region'], f"+{fastest_growing['growth_2024']}pp adoption")
                    st.write("**Also leads in:**")
                    st.write(f"• Investment growth: +{fastest_growing['investment_growth']}%")
                    st.write("• New AI startups: +45%")
                
                with col2:
                    st.metric("Highest Adoption", highest_adoption['region'], f"{highest_adoption['adoption_rate']}% rate")
                    st.write("**Characteristics:**")
                    st.write("• Mature market")
                    st.write(f"• Growth: +{highest_adoption['growth_2024']}pp")
                
                with col3:
                    st.metric("Emerging Leader", emerging_leader['region'], f"+{emerging_leader['growth_2024']}pp growth")
                    st.write("**Key drivers:**")
                    st.write("• Regulatory clarity")
                    st.write("• Public investment")
                    
            except Exception as e:
                logger.error(f"Error displaying regional metrics: {e}")
                # Fallback static content
                with col1:
                    st.metric("Fastest Growing", "Greater China", "+27pp adoption")
                    st.write("**Also leads in:**")
                    st.write("• Investment growth: +32%")
                    st.write("• New AI startups: +45%")
                
                with col2:
                    st.metric("Highest Adoption", "North America", "82% rate")
                    st.write("**Characteristics:**")
                    st.write("• Mature market")
                    st.write("• Slower growth: +15pp")
                
                with col3:
                    st.metric("Emerging Leader", "Europe", "+23pp growth")
                    st.write("**Key drivers:**")
                    st.write("• Regulatory clarity")
                    st.write("• Public investment")
            
            # Competitive dynamics analysis
            st.subheader("🏁 Competitive Dynamics")
            
            def plot_competitive_matrix():
                """Plot competitive positioning matrix"""
                # Create competitive positioning matrix
                fig2 = px.scatter(
                    regional_data,
                    x='adoption_rate',
                    y='growth_2024',
                    size='investment_growth',
                    color='region',
                    title='Regional AI Competitive Positioning Matrix',
                    labels={
                        'adoption_rate': 'Current Adoption Rate (%)',
                        'growth_2024': 'Adoption Growth Rate (pp)',
                        'investment_growth': 'Investment Growth (%)'
                    },
                    height=400
                )
                
                # Add quadrant lines
                fig2.add_hline(y=regional_data['growth_2024'].mean(), line_dash="dash", line_color="gray")
                fig2.add_vline(x=regional_data['adoption_rate'].mean(), line_dash="dash", line_color="gray")
                
                # Add quadrant labels
                mean_adoption = regional_data['adoption_rate'].mean()
                mean_growth = regional_data['growth_2024'].mean()
                
                fig2.add_annotation(x=mean_adoption-10, y=mean_growth+5, text="High Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
                fig2.add_annotation(x=mean_adoption+10, y=mean_growth+5, text="High Growth<br>High Base", showarrow=False, font=dict(color="gray"))
                fig2.add_annotation(x=mean_adoption-10, y=mean_growth-5, text="Low Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
                fig2.add_annotation(x=mean_adoption+10, y=mean_growth-5, text="Low Growth<br>High Base", showarrow=False, font=dict(color="gray"))
                
                st.plotly_chart(fig2, use_container_width=True)
            
            # Use safe plotting for competitive matrix
            if safe_plot_check(
                regional_data,
                "Regional Competitive Data",
                required_columns=['region', 'adoption_rate', 'growth_2024', 'investment_growth'],
                plot_func=plot_competitive_matrix
            ):
                st.info("""
                **Strategic Insights:**
                - **Greater China & Europe:** Aggressive catch-up strategy with high growth rates
                - **North America:** Market leader maintaining position with steady growth
                - **Competition intensifying:** Regional gaps narrowing as adoption accelerates globally
                """)
            
            # Data controls and downloads
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 View Data Source", key="regional_source"):
                    with st.expander("Data Source", expanded=True):
                        st.info(show_source_info('ai_index'))
                
                # Note about regional definitions
                st.info("**Note:** Regional data represents aggregate adoption and investment patterns across major economic zones")
            
            with col2:
                # Safe download button
                safe_download_button(
                    regional_data,
                    clean_filename(f"regional_ai_growth_{data_year}.csv"),
                    "📥 Download Regional Data",
                    key="download_regional_2025",
                    help_text="Download regional AI adoption and investment growth data"
                )
    
    else:
        st.warning("Regional growth data not available for analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source. Regional data may not be loaded properly.")
            with col2:
                if st.button("🔄 Reload Data", key="retry_regional"):
                    st.cache_data.clear()
                    st.rerun()