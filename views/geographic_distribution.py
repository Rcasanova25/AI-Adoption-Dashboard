"""
Geographic Distribution view for AI Adoption Dashboard
Displays AI adoption geographic distribution with research infrastructure
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


def show_geographic_distribution(
    data_year: str,
    geographic_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI adoption geographic distribution with research infrastructure
    
    Args:
        data_year: Selected year (e.g., "2025")
        geographic_data: DataFrame with geographic distribution data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'geographic':
            return "**Source**: AI Index 2025 Report, NSF AI Research Institutes Program\n\n**Methodology**: Combined analysis of metro-level AI adoption, federal research funding, NSF institute locations, and private investment data."
        return "**Source**: AI Index 2025 Report"
    
    st.write("🗺️ **AI Adoption Geographic Distribution with Research Infrastructure**")
    
    # Validate geographic data
    validator = DataValidator()
    geo_result = validator.validate_dataframe(
        geographic_data,
        "Geographic Data",
        required_columns=['city', 'state', 'lat', 'lon'],
        min_rows=1
    )
    
    if not geo_result.is_valid:
        st.warning("Geographic data not available. Using fallback data structure.")
        
        # Enhanced geographic data with academic and government investments
        enhanced_geographic = pd.DataFrame({
            'city': ['San Francisco Bay Area', 'Nashville', 'San Antonio', 'Las Vegas', 
                    'New Orleans', 'San Diego', 'Seattle', 'Boston', 'Los Angeles',
                    'Phoenix', 'Denver', 'Austin', 'Portland', 'Miami', 'Atlanta',
                    'Chicago', 'New York', 'Philadelphia', 'Dallas', 'Houston'],
            'state': ['California', 'Tennessee', 'Texas', 'Nevada', 
                     'Louisiana', 'California', 'Washington', 'Massachusetts', 'California',
                     'Arizona', 'Colorado', 'Texas', 'Oregon', 'Florida', 'Georgia',
                     'Illinois', 'New York', 'Pennsylvania', 'Texas', 'Texas'],
            'lat': [37.7749, 36.1627, 29.4241, 36.1699, 
                   29.9511, 32.7157, 47.6062, 42.3601, 34.0522,
                   33.4484, 39.7392, 30.2672, 45.5152, 25.7617, 33.7490,
                   41.8781, 40.7128, 39.9526, 32.7767, 29.7604],
            'lon': [-122.4194, -86.7816, -98.4936, -115.1398, 
                   -90.0715, -117.1611, -122.3321, -71.0589, -118.2437,
                   -112.0740, -104.9903, -97.7431, -122.6784, -80.1918, -84.3880,
                   -87.6298, -74.0060, -75.1652, -96.7970, -95.3698],
            'ai_adoption_rate': [9.5, 8.3, 8.3, 7.7, 
                                7.4, 7.4, 6.8, 6.7, 7.2,
                                6.5, 6.3, 7.8, 6.2, 6.9, 7.1,
                                7.0, 8.0, 6.6, 7.5, 7.3],
            'state_code': ['CA', 'TN', 'TX', 'NV', 
                          'LA', 'CA', 'WA', 'MA', 'CA',
                          'AZ', 'CO', 'TX', 'OR', 'FL', 'GA',
                          'IL', 'NY', 'PA', 'TX', 'TX'],
            'population_millions': [7.7, 0.7, 1.5, 0.6, 
                                   0.4, 1.4, 0.8, 0.7, 4.0,
                                   1.7, 0.7, 1.0, 0.7, 0.5, 0.5,
                                   2.7, 8.3, 1.6, 1.3, 2.3],
            'gdp_billions': [535, 48, 98, 68, 
                            25, 253, 392, 463, 860,
                            162, 201, 148, 121, 345, 396,
                            610, 1487, 388, 368, 356],
            # Academic and Research Infrastructure
            'major_universities': [12, 2, 3, 1, 2, 5, 4, 8, 6, 2, 3, 4, 2, 3, 4, 5, 7, 4, 3, 4],
            'ai_research_centers': [15, 1, 2, 0, 1, 3, 5, 12, 4, 1, 2, 3, 2, 2, 3, 4, 8, 3, 2, 3],
            'federal_ai_funding_millions': [2100, 45, 125, 15, 35, 180, 350, 890, 420, 55, 85, 165, 75, 95, 145, 285, 650, 225, 185, 245],
            'nsf_ai_institutes': [2, 0, 1, 0, 0, 1, 1, 3, 1, 0, 1, 1, 0, 0, 1, 1, 2, 1, 1, 1],
            # Innovation Metrics
            'ai_startups': [850, 15, 35, 8, 12, 95, 145, 325, 185, 25, 45, 85, 35, 55, 85, 125, 450, 95, 75, 125],
            'ai_patents_2024': [2450, 25, 85, 12, 18, 165, 285, 780, 385, 45, 95, 145, 65, 85, 125, 245, 825, 185, 155, 225],
            'venture_capital_millions': [15800, 125, 285, 45, 85, 1250, 2850, 4200, 3850, 185, 345, 650, 225, 385, 485, 1250, 8500, 650, 485, 850]
        })
        
        # Create state-level research infrastructure data
        state_research_data = pd.DataFrame({
            'state': ['California', 'Massachusetts', 'New York', 'Texas', 'Washington', 
                     'Illinois', 'Pennsylvania', 'Georgia', 'Colorado', 'Florida',
                     'Michigan', 'Ohio', 'North Carolina', 'Virginia', 'Maryland'],
            'state_code': ['CA', 'MA', 'NY', 'TX', 'WA', 'IL', 'PA', 'GA', 'CO', 'FL',
                          'MI', 'OH', 'NC', 'VA', 'MD'],
            'ai_adoption_rate': [8.2, 6.7, 8.0, 7.5, 6.8, 7.0, 6.6, 7.1, 6.3, 6.9,
                                5.5, 5.8, 6.0, 6.2, 6.4],
            'nsf_ai_institutes_total': [5, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2],
            'total_federal_funding_billions': [3.2, 1.1, 1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2,
                                              0.15, 0.12, 0.25, 0.35, 0.45],
            'r1_universities': [9, 4, 7, 8, 2, 3, 4, 2, 2, 3, 3, 3, 3, 2, 2],
            'ai_workforce_thousands': [285, 95, 185, 125, 85, 65, 55, 45, 35, 55, 35, 25, 45, 55, 65]
        })
        
        # Retry button for data reload
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Using fallback geographic data. Try refreshing for latest data.")
            with col2:
                if st.button("🔄 Reload Data", key="retry_geographic"):
                    st.cache_data.clear()
                    st.rerun()
        
    else:
        enhanced_geographic = geographic_data.copy()
        
        # Ensure required columns exist for plotting
        required_cols = ['ai_adoption_rate', 'federal_ai_funding_millions', 'ai_research_centers', 
                        'ai_startups', 'venture_capital_millions', 'nsf_ai_institutes', 'major_universities']
        for col in required_cols:
            if col not in enhanced_geographic.columns:
                enhanced_geographic[col] = 0  # Default values if missing
        
        # Create state research data if not available
        if 'state_research_data' not in dashboard_data or dashboard_data['state_research_data'].empty:
            state_research_data = _create_default_state_data()
        else:
            state_research_data = dashboard_data['state_research_data']
    
    # Create comprehensive tabs for different geographic analyses
    geo_tabs = st.tabs(["🗺️ Interactive Map", "🏛️ Research Infrastructure", "📊 State Comparisons", "🎓 Academic Centers", "💰 Investment Flows"])
    
    with geo_tabs[0]:
        # Enhanced interactive map with multiple layers
        st.subheader("AI Ecosystem Map: Adoption, Research & Investment")
        
        # Map controls
        col1, col2, col3 = st.columns(3)
        with col1:
            map_metric = st.selectbox(
                "Primary Metric",
                ["AI Adoption Rate", "Federal AI Funding", "AI Research Centers", "AI Startups", "Venture Capital"]
            )
        with col2:
            show_nsf_institutes = st.checkbox("Show NSF AI Institutes", value=True)
        with col3:
            show_universities = st.checkbox("Show Major Universities", value=False)
        
        # Validate required columns before plotting
        map_validation = validator.validate_dataframe(
            enhanced_geographic,
            "Enhanced Geographic Data",
            required_columns=['lat', 'lon', 'city', 'ai_adoption_rate'],
            min_rows=1
        )
        
        if map_validation.is_valid:
            def plot_geographic_map():
                """Plot the interactive geographic map"""
                # Metric mapping with proper units
                metric_mapping = {
                    "AI Adoption Rate": ('ai_adoption_rate', '%'),
                    "Federal AI Funding": ('federal_ai_funding_millions', '$M'),
                    "AI Research Centers": ('ai_research_centers', 'centers'),
                    "AI Startups": ('ai_startups', 'startups'),
                    "Venture Capital": ('venture_capital_millions', '$M')
                }
                
                selected_metric, unit = metric_mapping[map_metric]
                
                # Get metric values and create better normalization
                if selected_metric in enhanced_geographic.columns:
                    metric_values = enhanced_geographic[selected_metric]
                    
                    # Normalize sizes with more dramatic scaling (10-50 range)
                    min_val, max_val = metric_values.min(), metric_values.max()
                    if max_val > min_val:
                        normalized_sizes = 10 + (metric_values - min_val) / (max_val - min_val) * 40
                    else:
                        normalized_sizes = [25] * len(metric_values)
                else:
                    metric_values = [0] * len(enhanced_geographic)
                    normalized_sizes = [25] * len(enhanced_geographic)
                    min_val, max_val = 0, 1
                
                # Create the enhanced map
                fig = go.Figure()
                
                # State choropleth (if state data available)
                if not state_research_data.empty and 'state_code' in state_research_data.columns:
                    fig.add_trace(go.Choropleth(
                        locations=state_research_data['state_code'],
                        z=state_research_data['ai_adoption_rate'],
                        locationmode='USA-states',
                        colorscale='Blues',
                        colorbar=dict(
                            title="State AI<br>Adoption (%)",
                            x=-0.05,
                            len=0.35,
                            y=0.75,
                            thickness=15
                        ),
                        marker_line_color='black',
                        marker_line_width=1,
                        hovertemplate='<b>%{text}</b><br>AI Adoption: %{z:.1f}%<br>NSF Institutes: %{customdata[0]}<br>Federal Funding: $%{customdata[1]:.1f}B<extra></extra>',
                        text=state_research_data['state'],
                        customdata=state_research_data[['nsf_ai_institutes_total', 'total_federal_funding_billions']],
                        name="State Infrastructure",
                        showlegend=False
                    ))
                
                # Dynamic city markers
                fig.add_trace(go.Scattergeo(
                    lon=enhanced_geographic['lon'],
                    lat=enhanced_geographic['lat'],
                    text=enhanced_geographic['city'],
                    customdata=enhanced_geographic[[
                        'ai_adoption_rate', 'federal_ai_funding_millions', 'ai_research_centers', 
                        'ai_startups', 'venture_capital_millions', 'nsf_ai_institutes', 'major_universities'
                    ]],
                    mode='markers',
                    marker=dict(
                        size=normalized_sizes,
                        color=metric_values,
                        colorscale='Reds',
                        showscale=True,
                        colorbar=dict(
                            title=f"{map_metric}<br>({unit})",
                            x=1.02,
                            len=0.35,
                            y=0.35,
                            thickness=15
                        ),
                        line=dict(width=2, color='white'),
                        sizemode='diameter',
                        opacity=0.8,
                        cmin=min_val,
                        cmax=max_val
                    ),
                    showlegend=False,
                    hovertemplate='<b>%{text}</b><br>' +
                                 f'{map_metric}: %{{marker.color}}{unit}<br>' +
                                 'AI Adoption: %{customdata[0]:.1f}%<br>' +
                                 'Federal Funding: $%{customdata[1]:.0f}M<br>' +
                                 'Research Centers: %{customdata[2]}<br>' +
                                 'AI Startups: %{customdata[3]}<br>' +
                                 'VC Investment: $%{customdata[4]:.0f}M<br>' +
                                 'NSF Institutes: %{customdata[5]}<br>' +
                                 'Major Universities: %{customdata[6]}<extra></extra>',
                    name="Cities"
                ))
                
                # Add NSF AI Institutes as special markers
                if show_nsf_institutes and 'nsf_ai_institutes' in enhanced_geographic.columns:
                    nsf_cities = enhanced_geographic[enhanced_geographic['nsf_ai_institutes'] > 0]
                    if len(nsf_cities) > 0:
                        fig.add_trace(go.Scattergeo(
                            lon=nsf_cities['lon'],
                            lat=nsf_cities['lat'],
                            text=nsf_cities['city'],
                            mode='markers',
                            marker=dict(
                                size=20,
                                color='gold',
                                symbol='star',
                                line=dict(width=3, color='darkblue')
                            ),
                            name="NSF AI Institutes",
                            showlegend=True,
                            hovertemplate='<b>%{text}</b><br>NSF AI Institute Location<extra></extra>'
                        ))
                
                # Add major university indicators
                if show_universities and 'major_universities' in enhanced_geographic.columns:
                    major_uni_cities = enhanced_geographic[enhanced_geographic['major_universities'] >= 5]
                    if len(major_uni_cities) > 0:
                        fig.add_trace(go.Scattergeo(
                            lon=major_uni_cities['lon'],
                            lat=major_uni_cities['lat'],
                            text=major_uni_cities['city'],
                            mode='markers',
                            marker=dict(
                                size=15,
                                color='purple',
                                symbol='diamond',
                                line=dict(width=2, color='white')
                            ),
                            name="Major University Hubs",
                            showlegend=True,
                            hovertemplate='<b>%{text}</b><br>Universities: %{customdata}<extra></extra>',
                            customdata=major_uni_cities['major_universities']
                        ))
                
                fig.update_layout(
                    title=f'US AI Ecosystem: {map_metric} Distribution',
                    geo=dict(
                        scope='usa',
                        projection_type='albers usa',
                        showland=True,
                        landcolor='rgb(235, 235, 235)',
                        coastlinecolor='rgb(50, 50, 50)',
                        coastlinewidth=2
                    ),
                    height=700,
                    showlegend=True,
                    legend=dict(
                        x=0.85,
                        y=0.95,
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='rgba(0,0,0,0.2)',
                        borderwidth=1
                    ),
                    margin=dict(l=50, r=80, t=50, b=50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            if safe_plot_check(
                enhanced_geographic,
                "Geographic Map Data",
                required_columns=['lat', 'lon', 'city'],
                plot_func=plot_geographic_map
            ):
                # Dynamic insights based on selected metric
                _show_metric_insights(enhanced_geographic, map_metric)
        
        else:
            st.error("Cannot display map: Required geographic data is missing")
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Check data source or try refreshing")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_map_data"):
                        st.cache_data.clear()
                        st.rerun()
    
    with geo_tabs[1]:
        # Research infrastructure deep dive
        st.subheader("🏛️ Federal Research Infrastructure & NSF AI Institutes")
        
        # Validate state research data
        state_validation = validator.validate_dataframe(
            state_research_data,
            "State Research Data",
            required_columns=['state'],
            min_rows=1
        )
        
        if state_validation.is_valid:
            def plot_research_infrastructure():
                """Plot research infrastructure analysis"""
                # NSF AI Institutes overview
                col1, col2, col3, col4 = st.columns(4)
                
                # Safe metric calculations
                try:
                    total_institutes = state_research_data['nsf_ai_institutes_total'].sum() if 'nsf_ai_institutes_total' in state_research_data.columns else 0
                    total_funding = state_research_data['total_federal_funding_billions'].sum() if 'total_federal_funding_billions' in state_research_data.columns else 0
                    states_with_institutes = len(state_research_data[state_research_data['nsf_ai_institutes_total'] > 0]) if 'nsf_ai_institutes_total' in state_research_data.columns else 0
                    
                    with col1:
                        st.metric("Total NSF AI Institutes", total_institutes, help="Across all states")
                    with col2:
                        st.metric("States with Institutes", states_with_institutes, f"of {len(state_research_data)}")
                    with col3:
                        st.metric("Total Federal Funding", f"${total_funding:.1f}B", "Research infrastructure")
                    with col4:
                        avg_funding = total_funding / len(state_research_data) if len(state_research_data) > 0 else 0
                        st.metric("Average per State", f"${avg_funding:.2f}B", "Funding distribution")
                
                except Exception as e:
                    logger.error(f"Error calculating research metrics: {e}")
                    st.warning("Some research metrics unavailable")
                
                # Research infrastructure visualization
                try:
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('NSF AI Institutes by State', 'Federal Research Funding', 
                                       'R1 Research Universities', 'AI Workforce Concentration'),
                        specs=[[{"type": "bar"}, {"type": "bar"}],
                               [{"type": "bar"}, {"type": "scatter"}]]
                    )
                    
                    # Sort by institutes for better visualization
                    if 'nsf_ai_institutes_total' in state_research_data.columns:
                        institutes_sorted = state_research_data.nlargest(10, 'nsf_ai_institutes_total')
                        
                        fig.add_trace(go.Bar(
                            x=institutes_sorted['state'],
                            y=institutes_sorted['nsf_ai_institutes_total'],
                            marker_color='#3498DB',
                            text=institutes_sorted['nsf_ai_institutes_total'],
                            textposition='outside',
                            name='NSF Institutes'
                        ), row=1, col=1)
                    
                    if 'total_federal_funding_billions' in state_research_data.columns:
                        funding_sorted = state_research_data.nlargest(10, 'total_federal_funding_billions')
                        fig.add_trace(go.Bar(
                            x=funding_sorted['state'],
                            y=funding_sorted['total_federal_funding_billions'],
                            marker_color='#2ECC71',
                            text=[f'${x:.1f}B' for x in funding_sorted['total_federal_funding_billions']],
                            textposition='outside',
                            name='Federal Funding'
                        ), row=1, col=2)
                    
                    if 'r1_universities' in state_research_data.columns:
                        unis_sorted = state_research_data.nlargest(10, 'r1_universities')
                        fig.add_trace(go.Bar(
                            x=unis_sorted['state'],
                            y=unis_sorted['r1_universities'],
                            marker_color='#9B59B6',
                            text=unis_sorted['r1_universities'],
                            textposition='outside',
                            name='R1 Universities'
                        ), row=2, col=1)
                    
                    # Scatter plot for funding vs workforce
                    if all(col in state_research_data.columns for col in ['total_federal_funding_billions', 'ai_workforce_thousands', 'nsf_ai_institutes_total', 'ai_adoption_rate']):
                        fig.add_trace(go.Scatter(
                            x=state_research_data['total_federal_funding_billions'],
                            y=state_research_data['ai_workforce_thousands'],
                            mode='markers+text',
                            marker=dict(
                                size=state_research_data['nsf_ai_institutes_total'] * 10 + 10,
                                color=state_research_data['ai_adoption_rate'],
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="AI Adoption Rate")
                            ),
                            text=state_research_data['state_code'] if 'state_code' in state_research_data.columns else state_research_data['state'],
                            textposition='middle center',
                            name='Funding vs Workforce'
                        ), row=2, col=2)
                    
                    fig.update_xaxes(tickangle=45)
                    fig.update_layout(height=600, showlegend=False, title_text="Federal AI Research Infrastructure by State")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    logger.error(f"Error creating research infrastructure plot: {e}")
                    st.error("Unable to create research infrastructure visualization")
            
            # Use safe plotting
            if safe_plot_check(
                state_research_data,
                "Research Infrastructure Data",
                required_columns=['state'],
                plot_func=plot_research_infrastructure
            ):
                # Research infrastructure insights
                with st.expander("📊 Research Infrastructure Analysis"):
                    st.markdown("""
                    #### NSF AI Research Institutes Program Impact
                    
                    **Established 2020-2021** with $220M initial federal investment:
                    - **Geographic Distribution:** 27 institutes across 40+ states
                    - **Research Focus Areas:** Machine learning, human-AI interaction, AI safety, sector applications
                    - **Collaboration Model:** University-industry-government partnerships
                    
                    **Key Findings:**
                    - **California leads** with 5 institutes, reflecting existing tech ecosystem
                    - **Massachusetts concentration** in Boston area with 4 institutes near MIT/Harvard
                    - **Distributed strategy** ensures geographic diversity beyond coastal hubs
                    - **Federal coordination** creates national research network
                    
                    **Source:** NSF National AI Research Institutes Program, AI Index Report 2025
                    """)
        else:
            st.warning("Research infrastructure data not available")
            if dashboard_data:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.info("Research data may not be loaded")
                with col2:
                    if st.button("🔄 Reload Data", key="retry_research"):
                        st.cache_data.clear()
                        st.rerun()
    
    with geo_tabs[2]:
        # State-by-state comparison
        st.subheader("📊 State AI Ecosystem Comparison")
        
        if not state_research_data.empty:
            def plot_state_comparison():
                """Plot state-by-state comparison"""
                # Create comprehensive state scorecard
                state_scorecard = state_research_data.copy()
                
                # Normalize metrics for scoring (0-100 scale)
                metrics_to_normalize = ['ai_adoption_rate', 'nsf_ai_institutes_total', 'total_federal_funding_billions', 
                                       'r1_universities', 'ai_workforce_thousands']
                
                available_metrics = [col for col in metrics_to_normalize if col in state_scorecard.columns]
                
                for metric in available_metrics:
                    try:
                        max_val = state_scorecard[metric].max()
                        min_val = state_scorecard[metric].min()
                        if max_val > min_val:
                            state_scorecard[f'{metric}_score'] = ((state_scorecard[metric] - min_val) / (max_val - min_val)) * 100
                        else:
                            state_scorecard[f'{metric}_score'] = 50  # Default middle score if all values are the same
                    except Exception as e:
                        logger.error(f"Error normalizing metric {metric}: {e}")
                        state_scorecard[f'{metric}_score'] = 50
                
                # Calculate composite AI ecosystem score
                score_columns = [f'{metric}_score' for metric in available_metrics]
                if score_columns:
                    weights = [0.3, 0.2, 0.2, 0.15, 0.15][:len(score_columns)]  # Adjust weights based on available metrics
                    weights = [w/sum(weights) for w in weights]  # Normalize weights
                    
                    state_scorecard['composite_score'] = sum(
                        state_scorecard[col] * weight for col, weight in zip(score_columns, weights)
                    )
                else:
                    state_scorecard['composite_score'] = 50  # Default score
                
                # Top performers analysis
                top_states = state_scorecard.nlargest(10, 'composite_score')
                
                fig = go.Figure()
                
                # Create stacked bar chart showing component scores
                if f'ai_adoption_rate_score' in state_scorecard.columns:
                    fig.add_trace(go.Bar(
                        name='AI Adoption',
                        x=top_states['state'],
                        y=top_states['ai_adoption_rate_score'],
                        marker_color='#3498DB'
                    ))
                
                if f'nsf_ai_institutes_total_score' in state_scorecard.columns:
                    fig.add_trace(go.Bar(
                        name='NSF Institutes',
                        x=top_states['state'],
                        y=top_states['nsf_ai_institutes_total_score'],
                        marker_color='#E74C3C'
                    ))
                
                if f'total_federal_funding_billions_score' in state_scorecard.columns:
                    fig.add_trace(go.Bar(
                        name='Federal Funding',
                        x=top_states['state'],
                        y=top_states['total_federal_funding_billions_score'],
                        marker_color='#2ECC71'
                    ))
                
                if f'r1_universities_score' in state_scorecard.columns:
                    fig.add_trace(go.Bar(
                        name='Universities',
                        x=top_states['state'],
                        y=top_states['r1_universities_score'],
                        marker_color='#9B59B6'
                    ))
                
                if f'ai_workforce_thousands_score' in state_scorecard.columns:
                    fig.add_trace(go.Bar(
                        name='AI Workforce',
                        x=top_states['state'],
                        y=top_states['ai_workforce_thousands_score'],
                        marker_color='#F39C12'
                    ))
                
                fig.update_layout(
                    title='State AI Ecosystem Composite Scores (Top 10)',
                    xaxis_title='State',
                    yaxis_title='Normalized Score (0-100)',
                    barmode='stack',
                    height=500,
                    xaxis_tickangle=45
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # State rankings table
                st.subheader("🏆 State AI Ecosystem Rankings")
                
                try:
                    display_cols = ['state', 'composite_score']
                    for col in ['ai_adoption_rate', 'nsf_ai_institutes_total', 'total_federal_funding_billions', 'ai_workforce_thousands']:
                        if col in state_scorecard.columns:
                            display_cols.append(col)
                    
                    rankings_display = state_scorecard[display_cols].sort_values(by='composite_score', ascending=False).reset_index(drop=True)
                    rankings_display['rank'] = range(1, len(rankings_display) + 1)
                    rankings_display = rankings_display[['rank'] + display_cols]
                    
                    # Rename columns for display
                    column_renames = {
                        'rank': 'Rank',
                        'state': 'State',
                        'composite_score': 'Composite Score',
                        'ai_adoption_rate': 'AI Adoption (%)',
                        'nsf_ai_institutes_total': 'NSF Institutes',
                        'total_federal_funding_billions': 'Federal Funding ($B)',
                        'ai_workforce_thousands': 'AI Workforce (K)'
                    }
                    
                    # Only rename columns that exist
                    existing_renames = {k: v for k, v in column_renames.items() if k in rankings_display.columns}
                    rankings_display = rankings_display.rename(columns=existing_renames)
                    
                    # Format numerical columns
                    if 'Composite Score' in rankings_display.columns:
                        rankings_display['Composite Score'] = rankings_display['Composite Score'].round(1)
                    if 'Federal Funding ($B)' in rankings_display.columns:
                        rankings_display['Federal Funding ($B)'] = rankings_display['Federal Funding ($B)'].round(2)
                    
                    st.dataframe(rankings_display, hide_index=True, use_container_width=True)
                    
                except Exception as e:
                    logger.error(f"Error creating rankings table: {e}")
                    st.error("Unable to create rankings table")
            
            # Use safe plotting
            if safe_plot_check(
                state_research_data,
                "State Comparison Data",
                required_columns=['state'],
                plot_func=plot_state_comparison
            ):
                pass  # Additional content can be added here
        else:
            st.warning("State comparison data not available")
    
    with geo_tabs[3]:
        # Academic centers analysis
        st.subheader("🎓 Academic AI Research Centers & University Ecosystem")
        
        def plot_academic_analysis():
            """Plot academic centers analysis"""
            try:
                # University ecosystem analysis
                if 'state' in enhanced_geographic.columns:
                    university_metrics = enhanced_geographic.groupby('state').agg({
                        'major_universities': 'sum' if 'major_universities' in enhanced_geographic.columns else lambda x: 0,
                        'ai_research_centers': 'sum' if 'ai_research_centers' in enhanced_geographic.columns else lambda x: 0,
                        'federal_ai_funding_millions': 'sum' if 'federal_ai_funding_millions' in enhanced_geographic.columns else lambda x: 0,
                        'ai_patents_2024': 'sum' if 'ai_patents_2024' in enhanced_geographic.columns else lambda x: 0
                    }).reset_index()
                    
                    if not state_research_data.empty and 'r1_universities' in state_research_data.columns:
                        university_metrics = university_metrics.merge(
                            state_research_data[['state', 'r1_universities']], 
                            on='state', 
                            how='left'
                        ).fillna(0)
                    else:
                        university_metrics['r1_universities'] = 0
                    
                    # Top academic states
                    if 'ai_research_centers' in university_metrics.columns:
                        top_academic = university_metrics.nlargest(8, 'ai_research_centers')
                        
                        fig = make_subplots(
                            rows=1, cols=2,
                            subplot_titles=('AI Research Centers by State', 'Research Output vs Funding'),
                            column_widths=[0.6, 0.4]
                        )
                        
                        fig.add_trace(go.Bar(
                            x=top_academic['ai_research_centers'],
                            y=top_academic['state'],
                            orientation='h',
                            marker_color='#3498DB',
                            text=[f'{x} centers' for x in top_academic['ai_research_centers']],
                            textposition='outside',
                            name='Research Centers'
                        ), row=1, col=1)
                        
                        if all(col in university_metrics.columns for col in ['federal_ai_funding_millions', 'ai_patents_2024', 'major_universities']):
                            fig.add_trace(go.Scatter(
                                x=university_metrics['federal_ai_funding_millions'],
                                y=university_metrics['ai_patents_2024'],
                                mode='markers+text',
                                marker=dict(
                                    size=university_metrics['ai_research_centers'] * 3,
                                    color=university_metrics['major_universities'],
                                    colorscale='Viridis',
                                    showscale=True,
                                    colorbar=dict(title="Major Universities")
                                ),
                                text=university_metrics['state'],
                                textposition='top center',
                                name='Funding vs Patents'
                            ), row=1, col=2)
                        
                        fig.update_layout(height=400, title_text="Academic AI Research Ecosystem")
                        fig.update_xaxes(title_text="Research Centers", row=1, col=1)
                        fig.update_yaxes(title_text="State", row=1, col=1)
                        fig.update_xaxes(title_text="Federal Funding ($M)", row=1, col=2)
                        fig.update_yaxes(title_text="AI Patents (2024)", row=1, col=2)
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Research centers data not available for academic analysis")
                
                # Academic insights
                st.success("""
                **🎓 Academic Research Insights:**
                - **California dominance:** 15 major AI research centers, led by Stanford, UC Berkeley, Caltech
                - **Massachusetts concentration:** MIT, Harvard creating dense research ecosystem
                - **Federal research strategy:** NSF institutes strategically distributed to build national capacity
                - **Industry-academia bridges:** Highest correlation between research centers and private investment
                """)
                
            except Exception as e:
                logger.error(f"Error in academic analysis: {e}")
                st.error("Unable to create academic centers visualization")
        
        # Use safe plotting
        if safe_plot_check(
            enhanced_geographic,
            "Academic Centers Data",
            required_columns=['city', 'state'],
            plot_func=plot_academic_analysis
        ):
            pass
    
    with geo_tabs[4]:
        # Investment flows analysis
        st.subheader("💰 AI Investment Flows: Private Capital & Government Funding")
        
        def plot_investment_analysis():
            """Plot investment flows analysis"""
            try:
                # Investment flow analysis
                if 'state' in enhanced_geographic.columns:
                    investment_flow = enhanced_geographic.groupby('state').agg({
                        'venture_capital_millions': 'sum' if 'venture_capital_millions' in enhanced_geographic.columns else lambda x: 0,
                        'federal_ai_funding_millions': 'sum' if 'federal_ai_funding_millions' in enhanced_geographic.columns else lambda x: 0,
                        'ai_startups': 'sum' if 'ai_startups' in enhanced_geographic.columns else lambda x: 0,
                        'ai_adoption_rate': 'mean' if 'ai_adoption_rate' in enhanced_geographic.columns else lambda x: 0
                    }).reset_index()
                    
                    # Calculate investment ratios
                    investment_flow['private_to_federal_ratio'] = (
                        investment_flow['venture_capital_millions'] / 
                        investment_flow['federal_ai_funding_millions'].replace(0, 1)
                    )
                    
                    investment_flow['investment_per_startup'] = (
                        investment_flow['venture_capital_millions'] / 
                        investment_flow['ai_startups'].replace(0, 1)
                    )
                    
                    # Top investment states
                    top_investment = investment_flow.nlargest(8, 'venture_capital_millions')
                    
                    fig = make_subplots(
                        rows=2, cols=2,
                        subplot_titles=('Private vs Federal Investment', 'Investment Concentration', 
                                       'Private-to-Federal Ratio', 'Investment Efficiency'),
                        specs=[[{"secondary_y": True}, {"type": "pie"}],
                               [{"type": "bar"}, {"type": "scatter"}]]
                    )
                    
                    # Private vs Federal comparison
                    fig.add_trace(go.Bar(
                        name='Venture Capital',
                        x=top_investment['state'],
                        y=top_investment['venture_capital_millions'],
                        marker_color='#E74C3C',
                        yaxis='y'
                    ), row=1, col=1)
                    
                    fig.add_trace(go.Bar(
                        name='Federal Funding',
                        x=top_investment['state'],
                        y=top_investment['federal_ai_funding_millions'],
                        marker_color='#3498DB',
                        yaxis='y2'
                    ), row=1, col=1)
                    
                    # Investment concentration pie chart
                    fig.add_trace(go.Pie(
                        labels=top_investment['state'],
                        values=top_investment['venture_capital_millions'],
                        name="VC Distribution"
                    ), row=1, col=2)
                    
                    # Private-to-federal ratio
                    ratio_data = investment_flow.nlargest(8, 'private_to_federal_ratio')
                    fig.add_trace(go.Bar(
                        x=ratio_data['state'],
                        y=ratio_data['private_to_federal_ratio'],
                        marker_color='#F39C12',
                        text=[f'{x:.1f}x' for x in ratio_data['private_to_federal_ratio']],
                        textposition='outside'
                    ), row=2, col=1)
                    
                    # Investment efficiency scatter
                    fig.add_trace(go.Scatter(
                        x=investment_flow['ai_startups'],
                        y=investment_flow['investment_per_startup'],
                        mode='markers+text',
                        marker=dict(
                            size=investment_flow['ai_adoption_rate'] * 5,
                            color=investment_flow['venture_capital_millions'],
                            colorscale='Reds',
                            showscale=True
                        ),
                        text=investment_flow['state'],
                        textposition='top center'
                    ), row=2, col=2)
                    
                    fig.update_layout(height=700, title_text="AI Investment Ecosystem Analysis")
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Investment flow data not available")
                    
            except Exception as e:
                logger.error(f"Error in investment analysis: {e}")
                st.error("Unable to create investment flows visualization")
        
        # Use safe plotting
        if safe_plot_check(
            enhanced_geographic,
            "Investment Flows Data",
            required_columns=['city', 'state'],
            plot_func=plot_investment_analysis
        ):
            pass
    
    # Data source and download options
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("📊 View Data Source", key="geographic_source"):
            with st.expander("Data Source", expanded=True):
                st.info(show_source_info('geographic'))
    
    with col2:
        # Safe download button for enhanced geographic data
        safe_download_button(
            enhanced_geographic,
            clean_filename(f"ai_geographic_distribution_{data_year}.csv"),
            "📥 Download Geographic Data",
            key="download_geographic",
            help_text="Download AI geographic distribution and ecosystem data"
        )
    
    # Export complete dataset option
    if st.button("📥 Export Geographic Analysis Data"):
        try:
            # Combine all geographic data for export
            if not state_research_data.empty and 'state' in enhanced_geographic.columns and 'state' in state_research_data.columns:
                export_data = enhanced_geographic.merge(
                    state_research_data[['state', 'nsf_ai_institutes_total', 'total_federal_funding_billions']], 
                    on='state', 
                    how='left'
                )
            else:
                export_data = enhanced_geographic
            
            csv = export_data.to_csv(index=False)
            st.download_button(
                label="Download Complete Geographic Dataset (CSV)",
                data=csv,
                file_name=clean_filename("ai_geographic_ecosystem_analysis.csv"),
                mime="text/csv"
            )
        except Exception as e:
            logger.error(f"Error creating export data: {e}")
            st.error("Unable to create export dataset")


def _create_default_state_data() -> pd.DataFrame:
    """Create default state research data if not available"""
    return pd.DataFrame({
        'state': ['California', 'Massachusetts', 'New York', 'Texas', 'Washington', 
                 'Illinois', 'Pennsylvania', 'Georgia', 'Colorado', 'Florida'],
        'state_code': ['CA', 'MA', 'NY', 'TX', 'WA', 'IL', 'PA', 'GA', 'CO', 'FL'],
        'ai_adoption_rate': [8.2, 6.7, 8.0, 7.5, 6.8, 7.0, 6.6, 7.1, 6.3, 6.9],
        'nsf_ai_institutes_total': [5, 4, 3, 3, 2, 2, 2, 1, 2, 1],
        'total_federal_funding_billions': [3.2, 1.1, 1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2],
        'r1_universities': [9, 4, 7, 8, 2, 3, 4, 2, 2, 3],
        'ai_workforce_thousands': [285, 95, 185, 125, 85, 65, 55, 45, 35, 55]
    })


def _show_metric_insights(enhanced_geographic: pd.DataFrame, map_metric: str) -> None:
    """Show dynamic insights based on selected metric"""
    try:
        if map_metric == "AI Adoption Rate" and 'ai_adoption_rate' in enhanced_geographic.columns:
            max_idx = enhanced_geographic['ai_adoption_rate'].idxmax()
            max_city = enhanced_geographic.loc[max_idx, 'city']
            max_rate = enhanced_geographic['ai_adoption_rate'].max()
            min_rate = enhanced_geographic['ai_adoption_rate'].min()
            
            insight_text = f"""
            **🗺️ AI Adoption Geographic Insights:**
            - **Highest adoption:** {max_city} ({max_rate:.1f}%)
            - **Regional variation:** {max_rate - min_rate:.1f} percentage point spread
            - **Coastal concentration:** West Coast and Northeast lead in AI implementation
            - **Digital divide:** Significant disparities between innovation hubs and interior regions
            """
            
        elif map_metric == "Federal AI Funding" and 'federal_ai_funding_millions' in enhanced_geographic.columns:
            max_idx = enhanced_geographic['federal_ai_funding_millions'].idxmax()
            top_funding_city = enhanced_geographic.loc[max_idx, 'city']
            top_funding_amount = enhanced_geographic['federal_ai_funding_millions'].max()
            total_funding = enhanced_geographic['federal_ai_funding_millions'].sum()
            top_5_funding = enhanced_geographic.nlargest(5, 'federal_ai_funding_millions')['federal_ai_funding_millions'].sum()
            
            insight_text = f"""
            **🏛️ Federal Investment Geographic Insights:**
            - **Largest recipient:** {top_funding_city} (${top_funding_amount:.0f}M federal funding)
            - **Investment concentration:** Top 5 metros receive {(top_5_funding/total_funding)*100:.0f}% of federal AI research funding
            - **Total investment:** ${total_funding:.0f}M across all metros
            - **Research focus:** Federal funding concentrated in university-rich areas
            """
            
        elif map_metric == "AI Startups" and 'ai_startups' in enhanced_geographic.columns:
            max_idx = enhanced_geographic['ai_startups'].idxmax()
            top_startup_city = enhanced_geographic.loc[max_idx, 'city']
            top_startup_count = enhanced_geographic['ai_startups'].max()
            total_startups = enhanced_geographic['ai_startups'].sum()
            
            insight_text = f"""
            **🚀 AI Startup Geographic Insights:**
            - **Startup capital:** {top_startup_city} ({top_startup_count} AI startups)
            - **Total startups:** {total_startups} across all metros
            - **Entrepreneurship hubs:** Concentrated in venture capital centers
            - **Innovation clusters:** Research-industry alignment drives startup formation
            """
            
        elif map_metric == "Venture Capital" and 'venture_capital_millions' in enhanced_geographic.columns:
            max_idx = enhanced_geographic['venture_capital_millions'].idxmax()
            top_vc_city = enhanced_geographic.loc[max_idx, 'city']
            top_vc_amount = enhanced_geographic['venture_capital_millions'].max()
            total_vc = enhanced_geographic['venture_capital_millions'].sum()
            
            insight_text = f"""
            **💰 Venture Capital Geographic Insights:**
            - **Investment leader:** {top_vc_city} (${top_vc_amount:.0f}M in VC investment)
            - **Capital concentration:** {(top_vc_amount / total_vc * 100):.1f}% of total investment in top city
            - **Total VC:** ${total_vc:.0f}M across all metros
            - **Regional gaps:** 85% of private investment concentrated in coastal states
            """
            
        else:  # AI Research Centers
            if 'ai_research_centers' in enhanced_geographic.columns:
                max_idx = enhanced_geographic['ai_research_centers'].idxmax()
                top_research_city = enhanced_geographic.loc[max_idx, 'city']
                top_research_count = enhanced_geographic['ai_research_centers'].max()
                total_research_centers = enhanced_geographic['ai_research_centers'].sum()
                
                if 'nsf_ai_institutes' in enhanced_geographic.columns:
                    cities_with_nsf = len(enhanced_geographic[enhanced_geographic['nsf_ai_institutes'] > 0])
                    total_nsf_institutes = enhanced_geographic['nsf_ai_institutes'].sum()
                else:
                    cities_with_nsf = 0
                    total_nsf_institutes = 0
                
                insight_text = f"""
                **🔬 AI Research Geographic Insights:**
                - **Research leader:** {top_research_city} ({top_research_count} research centers)
                - **NSF AI Institutes:** {total_nsf_institutes} institutes across {cities_with_nsf} metropolitan areas
                - **Total centers:** {total_research_centers} across all metros
                - **Academic concentration:** Research centers cluster near major universities
                """
            else:
                insight_text = "**🔬 AI Research Geographic Insights:** Research center data not available"
        
        st.info(insight_text)
        
    except Exception as e:
        logger.error(f"Error generating metric insights: {e}")
        st.info(f"**{map_metric} Insights:** Analysis not available - check data completeness")