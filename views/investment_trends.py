"""
Investment Trends view for AI Adoption Dashboard
Displays AI investment trends including total investment, GenAI investment, and regional analysis with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any
import logging

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_investment_trends(
    data_year: str,
    ai_investment: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI Investment trends with comprehensive analysis
    
    Args:
        data_year: Selected year (e.g., "2025")
        ai_investment: DataFrame with AI investment data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'ai_index':
            return "**Source**: AI Index Report 2025\n\n**Methodology**: Comprehensive analysis of AI investment metrics globally from Stanford HAI with data from various industry sources including startup funding databases and public market data."
        return "**Source**: AI Index 2025 Report"
    
    st.write("💰 **AI Investment Trends: Record Growth in 2024 (AI Index Report 2025)**")
    
    # Validate investment data
    validator = DataValidator()
    investment_result = validator.validate_dataframe(
        ai_investment,
        "AI Investment Data",
        required_columns=['year', 'total_investment'],
        min_rows=1
    )
    
    if investment_result.is_valid:
        # Investment overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Get latest year data for metrics
        try:
            latest_data = ai_investment[ai_investment['year'] == ai_investment['year'].max()]
            if not latest_data.empty:
                latest_total = latest_data['total_investment'].iloc[0]
                latest_genai = latest_data.get('genai_investment', pd.Series([0])).iloc[0]
                
                # Calculate growth rates if we have previous year data
                prev_year_data = ai_investment[ai_investment['year'] == (ai_investment['year'].max() - 1)]
                if not prev_year_data.empty:
                    prev_total = prev_year_data['total_investment'].iloc[0]
                    growth_rate = ((latest_total - prev_total) / prev_total) * 100
                else:
                    growth_rate = 0
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            latest_total = 252.3
            latest_genai = 33.9
            growth_rate = 44.5
        
        with col1:
            st.metric(
                label="2024 Total Investment", 
                value=f"${latest_total:.1f}B", 
                delta=f"+{growth_rate:.1f}% YoY",
                help="Total corporate AI investment in 2024"
            )
        
        with col2:
            st.metric(
                label="GenAI Investment", 
                value=f"${latest_genai:.1f}B", 
                delta="+18.7% from 2023",
                help="8.5x higher than 2022 levels"
            )
        
        with col3:
            st.metric(
                label="US Investment Lead", 
                value="12x China", 
                delta="$109.1B vs $9.3B",
                help="US leads global AI investment"
            )
        
        with col4:
            try:
                earliest_total = ai_investment[ai_investment['year'] == ai_investment['year'].min()]['total_investment'].iloc[0]
                growth_multiplier = latest_total / earliest_total
                st.metric(
                    label="Growth Since 2014", 
                    value=f"{growth_multiplier:.0f}x", 
                    delta=f"From ${earliest_total:.1f}B to ${latest_total:.1f}B",
                    help="Investment has grown multiple times over"
                )
            except Exception as e:
                logger.error(f"Error calculating growth multiplier: {e}")
                st.metric(
                    label="Growth Since 2014", 
                    value="13x", 
                    delta="From $19.4B to $252.3B",
                    help="Investment has grown thirteenfold"
                )
        
        # Create tabs for different investment views
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Overall Trends", "🌍 Geographic Distribution", "🚀 GenAI Focus", "📊 Comparative Analysis"])
        
        with tab1:
            def plot_overall_trends():
                """Plot the overall investment trends chart"""
                fig = go.Figure()
                
                # Total investment line
                fig.add_trace(go.Scatter(
                    x=ai_investment['year'],
                    y=ai_investment['total_investment'],
                    mode='lines+markers',
                    name='Total AI Investment',
                    line=dict(width=4, color='#2E86AB'),
                    marker=dict(size=10),
                    text=[f'${x:.1f}B' for x in ai_investment['total_investment']],
                    textposition='top center',
                    hovertemplate='Year: %{x}<br>Total Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>'
                ))
                
                # GenAI investment line (if available)
                if 'genai_investment' in ai_investment.columns:
                    genai_data = ai_investment[ai_investment['genai_investment'] > 0]
                    if not genai_data.empty:
                        fig.add_trace(go.Scatter(
                            x=genai_data['year'],
                            y=genai_data['genai_investment'],
                            mode='lines+markers',
                            name='GenAI Investment',
                            line=dict(width=3, color='#F24236'),
                            marker=dict(size=8),
                            text=[f'${x:.1f}B' for x in genai_data['genai_investment']],
                            textposition='bottom center',
                            hovertemplate='Year: %{x}<br>GenAI Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>'
                        ))
                        
                        # Add annotation for GenAI emergence
                        try:
                            genai_start_year = genai_data['year'].min()
                            genai_start_value = genai_data[genai_data['year'] == genai_start_year]['genai_investment'].iloc[0]
                            fig.add_annotation(
                                x=genai_start_year,
                                y=genai_start_value,
                                text="<b>GenAI Era Begins</b><br>Now 20% of all AI investment",
                                showarrow=True,
                                arrowhead=2,
                                bgcolor="white",
                                bordercolor="#F24236",
                                borderwidth=2,
                                font=dict(size=11, color="#F24236")
                            )
                        except Exception as e:
                            logger.warning(f"Could not add GenAI annotation: {e}")
                
                fig.update_layout(
                    title="AI Investment Has Grown Significantly Since 2014",
                    xaxis_title="Year",
                    yaxis_title="Investment ($ Billions)",
                    height=450,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            if safe_plot_check(
                ai_investment,
                "AI Investment Overall Trends",
                required_columns=['year', 'total_investment'],
                plot_func=plot_overall_trends
            ):
                col1, col2 = st.columns([10, 1])
                with col2:
                    if st.button("📊", key="inv_source", help="View data source"):
                        with st.expander("Data Source", expanded=True):
                            st.info(show_source_info('ai_index'))
                
                st.info("**Key Insight:** Private investment in generative AI now represents over 20% of all AI-related private investment")
                
                # Safe download button
                safe_download_button(
                    ai_investment,
                    clean_filename(f"ai_investment_trends_{data_year}.csv"),
                    "📥 Download Investment Data",
                    key="download_investment_trends",
                    help_text="Download AI investment trends data"
                )
        
        with tab2:
            # Country comparison with more context
            countries_data = pd.DataFrame({
                'country': ['United States', 'China', 'United Kingdom', 'Germany', 'France', 
                           'Canada', 'Israel', 'Japan', 'South Korea', 'India'],
                'investment': [109.1, 9.3, 4.5, 3.2, 2.8, 2.5, 2.2, 2.0, 1.8, 1.5],
                'per_capita': [324.8, 6.6, 66.2, 38.1, 41.2, 65.8, 231.6, 16.0, 34.6, 1.1],
                'pct_of_gdp': [0.43, 0.05, 0.14, 0.08, 0.09, 0.13, 0.48, 0.05, 0.10, 0.04]
            })
            
            def plot_geographic_distribution():
                """Plot geographic distribution of investment"""
                # Create subplot with multiple metrics
                fig = make_subplots(
                    rows=1, cols=3,
                    subplot_titles=('Total Investment ($B)', 'Per Capita Investment ($)', '% of GDP'),
                    horizontal_spacing=0.12
                )
                
                # Total investment - show top 6
                top_investment = countries_data.nlargest(6, 'investment')
                fig.add_trace(
                    go.Bar(x=top_investment['country'], y=top_investment['investment'],
                           marker_color='#3498DB', showlegend=False,
                           text=[f'${x:.1f}B' for x in top_investment['investment']],
                           textposition='outside'),
                    row=1, col=1
                )
                
                # Per capita - show top 6 to highlight leaders
                top_per_capita = countries_data.nlargest(6, 'per_capita')
                colors_per_capita = ['#E74C3C' if country == 'Israel' else '#2ECC71' for country in top_per_capita['country']]
                fig.add_trace(
                    go.Bar(x=top_per_capita['country'], y=top_per_capita['per_capita'],
                           marker_color=colors_per_capita, showlegend=False,
                           text=[f'${x:.0f}' for x in top_per_capita['per_capita']],
                           textposition='outside'),
                    row=1, col=2
                )
                
                # % of GDP - show top 6 to highlight leaders
                top_gdp_pct = countries_data.nlargest(6, 'pct_of_gdp')
                colors_gdp = ['#E74C3C' if country == 'Israel' else '#F39C12' for country in top_gdp_pct['country']]
                fig.add_trace(
                    go.Bar(x=top_gdp_pct['country'], y=top_gdp_pct['pct_of_gdp'],
                           marker_color=colors_gdp, showlegend=False,
                           text=[f'{x:.2f}%' for x in top_gdp_pct['pct_of_gdp']],
                           textposition='outside'),
                    row=1, col=3
                )
                
                fig.update_xaxes(tickangle=45)
                fig.update_layout(height=400, title_text="AI Investment by Country - Multiple Perspectives (2024)")
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for geographic data
            if safe_plot_check(
                countries_data,
                "Geographic Investment Distribution",
                required_columns=['country', 'investment'],
                plot_func=plot_geographic_distribution
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**🌍 Investment Leadership:**")
                    st.write("• **US dominance:** $109.1B (43% of global)")
                    israel_data = countries_data[countries_data['country']=='Israel']
                    if not israel_data.empty:
                        israel_per_capita = israel_data['per_capita'].iloc[0]
                        israel_pct_gdp = israel_data['pct_of_gdp'].iloc[0]
                        st.write(f"• **Per capita leader:** Israel at ${israel_per_capita:.0f} per person")
                        st.write(f"• **As % of GDP:** Israel ({israel_pct_gdp:.2f}%) and US (0.43%) lead")
                
                with col2:
                    st.write("**📈 Regional Dynamics:**")
                    st.write("• **Asia rising:** Combined $16.4B across major economies")
                    st.write("• **Europe steady:** $10.5B across top 3 countries")
                    st.write("• **Innovation hubs:** Israel and US show highest intensity (% of GDP)")
                
                # Add explanation for Israel's leadership
                st.info("""
                **🇮🇱 Israel's AI Investment Leadership:**
                - **Per capita champion:** $232 per person vs US $325 (considering population size)
                - **GDP intensity leader:** 0.48% of GDP, highest globally
                - **Innovation density:** Small country with concentrated AI ecosystem
                - **Strategic focus:** Government and private sector aligned on AI development
                """)
                
                # Safe download button for geographic data
                safe_download_button(
                    countries_data,
                    clean_filename(f"ai_investment_by_country_{data_year}.csv"),
                    "📥 Download Country Data",
                    key="download_country_investment",
                    help_text="Download country-level AI investment data"
                )
        
        with tab3:
            # GenAI focus analysis
            if 'genai_investment' in ai_investment.columns:
                genai_data = pd.DataFrame({
                    'year': ['2022', '2023', '2024'],
                    'investment': [3.95, 28.5, 33.9],
                    'growth': ['Baseline', '+621%', '+18.7%'],
                    'pct_of_total': [2.7, 16.3, 13.4]
                })
                
                def plot_genai_focus():
                    """Plot GenAI investment focus"""
                    # Create dual-axis chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=genai_data['year'],
                        y=genai_data['investment'],
                        text=[f'${x:.1f}B<br>{g}' for x, g in zip(genai_data['investment'], genai_data['growth'])],
                        textposition='outside',
                        marker_color=['#FFB6C1', '#FF69B4', '#FF1493'],
                        name='GenAI Investment',
                        yaxis='y'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=genai_data['year'],
                        y=genai_data['pct_of_total'],
                        mode='lines+markers',
                        name='% of Total AI Investment',
                        line=dict(width=3, color='#2C3E50'),
                        marker=dict(size=10),
                        yaxis='y2'
                    ))
                    
                    fig.update_layout(
                        title="GenAI Investment: From $3.95B to $33.9B in Two Years",
                        xaxis_title="Year",
                        yaxis=dict(title="Investment ($ Billions)", side="left"),
                        yaxis2=dict(title="% of Total AI Investment", side="right", overlaying="y"),
                        height=400,
                        hovermode='x unified',
                        xaxis=dict(
                            type='category',
                            categoryorder='array',
                            categoryarray=['2022', '2023', '2024']
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Use safe plotting for GenAI data
                if safe_plot_check(
                    genai_data,
                    "GenAI Investment Focus",
                    required_columns=['year', 'investment'],
                    plot_func=plot_genai_focus
                ):
                    st.success("**🚀 GenAI represents over 20% of all AI-related private investment, up from near zero in 2021**")
                    
                    # Safe download button for GenAI data
                    safe_download_button(
                        genai_data,
                        clean_filename(f"genai_investment_trends_{data_year}.csv"),
                        "📥 Download GenAI Data",
                        key="download_genai_investment",
                        help_text="Download GenAI-specific investment data"
                    )
            else:
                st.info("GenAI investment data not available in the current dataset")
        
        with tab4:
            # Comparative analysis
            st.write("**Investment Growth Comparison**")
            
            # Calculate growth rates from available data
            try:
                # Calculate YoY growth for total investment
                latest_year = ai_investment['year'].max()
                prev_year = latest_year - 1
                
                latest_total = ai_investment[ai_investment['year'] == latest_year]['total_investment'].iloc[0]
                prev_total = ai_investment[ai_investment['year'] == prev_year]['total_investment'].iloc[0]
                total_growth = ((latest_total - prev_total) / prev_total) * 100
                
                # GenAI growth if available
                if 'genai_investment' in ai_investment.columns:
                    latest_genai = ai_investment[ai_investment['year'] == latest_year]['genai_investment'].iloc[0]
                    prev_genai = ai_investment[ai_investment['year'] == prev_year]['genai_investment'].iloc[0]
                    genai_growth = ((latest_genai - prev_genai) / prev_genai) * 100 if prev_genai > 0 else 0
                else:
                    genai_growth = 18.7
                
                # Create growth comparison data
                growth_data = pd.DataFrame({
                    'metric': ['Total AI', 'GenAI', 'US Investment', 'China Investment', 'UK Investment'],
                    'growth_2024': [total_growth, genai_growth, 44.3, 10.7, 18.4],
                    'cagr_5yr': [28.3, 156.8, 31.2, 15.4, 22.7]  # 5-year CAGR estimates
                })
                
            except Exception as e:
                logger.error(f"Error calculating growth rates: {e}")
                # Fallback to predefined data
                growth_data = pd.DataFrame({
                    'metric': ['Total AI', 'GenAI', 'US Investment', 'China Investment', 'UK Investment'],
                    'growth_2024': [44.5, 18.7, 44.3, 10.7, 18.4],
                    'cagr_5yr': [28.3, 156.8, 31.2, 15.4, 22.7]
                })
            
            def plot_comparative_analysis():
                """Plot comparative growth analysis"""
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='2024 Growth (%)',
                    x=growth_data['metric'],
                    y=growth_data['growth_2024'],
                    marker_color='#3498DB',
                    text=[f'{x:.1f}%' for x in growth_data['growth_2024']],
                    textposition='outside'
                ))
                
                fig.add_trace(go.Bar(
                    name='5-Year CAGR (%)',
                    x=growth_data['metric'],
                    y=growth_data['cagr_5yr'],
                    marker_color='#E74C3C',
                    text=[f'{x:.1f}%' for x in growth_data['cagr_5yr']],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title="AI Investment Growth Rates",
                    xaxis_title="Investment Category",
                    yaxis_title="Growth Rate (%)",
                    barmode='group',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for comparative analysis
            if safe_plot_check(
                growth_data,
                "Investment Growth Comparison",
                required_columns=['metric', 'growth_2024'],
                plot_func=plot_comparative_analysis
            ):
                st.info("**Note:** GenAI shows exceptional 5-year CAGR due to starting from near-zero base in 2019")
                
                # Safe download button for growth data
                safe_download_button(
                    growth_data,
                    clean_filename(f"ai_investment_growth_rates_{data_year}.csv"),
                    "📥 Download Growth Data",
                    key="download_growth_rates",
                    help_text="Download investment growth rate comparison data"
                )
    
    else:
        st.warning("AI investment data not available for investment trends analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_investment"):
                    st.cache_data.clear()
                    st.rerun()