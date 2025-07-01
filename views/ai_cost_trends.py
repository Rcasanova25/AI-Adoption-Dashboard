"""
AI Cost Trends view for AI Adoption Dashboard
Displays AI cost reduction trends and hardware improvements with proper data validation
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
import logging

from utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename

logger = logging.getLogger(__name__)


def show_ai_cost_trends(
    data_year: str,
    cost_data: pd.DataFrame,
    dashboard_data: Dict[str, Any] = None
) -> None:
    """
    Display AI cost reduction trends and hardware improvements
    
    Args:
        data_year: Selected year (e.g., "2025")
        cost_data: DataFrame with AI cost reduction data
        dashboard_data: Full dashboard data dict for fallback
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'ai_index':
            return "**Source**: AI Index Report 2025\n\n**Methodology**: Analysis of AI inference costs, hardware improvements, and cost projections based on industry data and pricing trends."
        return "**Source**: AI Index 2025 Report"
    
    st.write("💰 **AI Cost Reduction: Dramatic Improvements (AI Index Report 2025)**")
    
    # Validate cost data
    validator = DataValidator()
    cost_result = validator.validate_dataframe(
        cost_data,
        "AI Cost Reduction Data",
        required_columns=['model', 'cost_per_million_tokens'],
        min_rows=1
    )
    
    if cost_result.is_valid:
        # Cost reduction visualization with context
        tab1, tab2, tab3 = st.tabs(["Inference Costs", "Hardware Improvements", "Cost Projections"])
        
        with tab1:
            def plot_cost_reduction_chart():
                """Plot the cost reduction chart"""
                # Enhanced cost reduction chart
                fig = go.Figure()
                
                # Create comprehensive cost timeline data
                cost_timeline = pd.DataFrame({
                    'date': ['Nov 2022', 'Jan 2023', 'Jul 2023', 'Jan 2024', 'Oct 2024', 'Oct 2024\n(Gemini)'],
                    'cost': [20.00, 10.00, 2.00, 0.50, 0.14, 0.07],
                    'reduction_factor': ['Baseline', '2x cheaper', '10x cheaper', '40x cheaper', '143x cheaper', '286x cheaper']
                })
                
                # Add cost trajectory
                fig.add_trace(go.Scatter(
                    x=cost_timeline['date'],
                    y=cost_timeline['cost'],
                    mode='lines+markers',
                    marker=dict(
                        size=[15, 10, 10, 10, 15, 20],
                        color=['red', 'orange', 'yellow', 'lightgreen', 'green', 'darkgreen']
                    ),
                    line=dict(width=3, color='gray', dash='dash'),
                    text=[f'${x:.2f}' for x in cost_timeline['cost']],
                    textposition='top center',
                    name='Cost per Million Tokens',
                    hovertemplate='Date: %{x}<br>Cost: %{text}<br>Reduction: %{customdata}<extra></extra>',
                    customdata=cost_timeline['reduction_factor']
                ))
                
                # Add annotations for key milestones
                fig.add_annotation(
                    x='Nov 2022', y=20,
                    text="<b>GPT-3.5 Launch</b><br>$20/M tokens",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=-40
                )
                
                fig.add_annotation(
                    x='Oct 2024\n(Gemini)', y=0.07,
                    text="<b>286x Cost Reduction</b><br>$0.07/M tokens",
                    showarrow=True,
                    arrowhead=2,
                    ax=0, ay=40
                )
                
                fig.update_layout(
                    title="AI Inference Cost Collapse: 286x Reduction in 2 Years",
                    xaxis_title="Time Period",
                    yaxis_title="Cost per Million Tokens ($)",
                    yaxis_type="log",
                    height=450,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting
            if safe_plot_check(
                cost_data,
                "AI Cost Reduction Data",
                required_columns=['model', 'cost_per_million_tokens'],
                plot_func=plot_cost_reduction_chart
            ):
                # Cost impact analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**💡 What This Means:**")
                    st.write("• Processing 1B tokens now costs $70 (was $20,000)")
                    st.write("• Enables mass deployment of AI applications")
                    st.write("• Makes AI accessible to smaller organizations")
                    
                with col2:
                    st.write("**📈 Rate of Improvement:**")
                    st.write("• Prices falling 9-900x per year by task")
                    st.write("• Outpacing Moore's Law significantly")
                    st.write("• Driven by competition and efficiency gains")
        
        with tab2:
            # Hardware improvements
            hardware_metrics = pd.DataFrame({
                'metric': ['Performance Growth', 'Price/Performance', 'Energy Efficiency'],
                'annual_rate': [43, -30, 40],
                'cumulative_5yr': [680, -83, 538]
            })
            
            def plot_hardware_improvements():
                """Plot hardware improvement metrics"""
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Annual Rate (%)',
                    x=hardware_metrics['metric'],
                    y=hardware_metrics['annual_rate'],
                    marker_color=['#2ECC71' if x > 0 else '#E74C3C' for x in hardware_metrics['annual_rate']],
                    text=[f'{x:+d}%' for x in hardware_metrics['annual_rate']],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title="ML Hardware Annual Improvement Rates",
                    xaxis_title="Metric",
                    yaxis_title="Annual Change (%)",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Use safe plotting for hardware metrics
            if safe_plot_check(
                hardware_metrics,
                "Hardware Metrics Data",
                required_columns=['metric', 'annual_rate'],
                plot_func=plot_hardware_improvements
            ):
                st.success("""
                **🚀 Hardware Revolution:**
                - Performance improving **43% annually** (16-bit operations)
                - Cost dropping **30% per year** for same performance
                - Energy efficiency gaining **40% annually**
                - Enabling larger models at lower costs
                """)
        
        with tab3:
            # Cost projections
            st.write("**Future Cost Projections**")
            
            def plot_cost_projections():
                """Plot future cost projections"""
                # Create projection data
                years = list(range(2024, 2028))
                conservative = [0.07, 0.035, 0.018, 0.009]
                aggressive = [0.07, 0.014, 0.003, 0.0006]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=conservative,
                    mode='lines+markers',
                    name='Conservative (50% annual reduction)',
                    line=dict(width=3, dash='dash'),
                    fill='tonexty',
                    fillcolor='rgba(52, 152, 219, 0.1)'
                ))
                
                fig.add_trace(go.Scatter(
                    x=years,
                    y=aggressive,
                    mode='lines+markers',
                    name='Aggressive (80% annual reduction)',
                    line=dict(width=3),
                    fill='tozeroy',
                    fillcolor='rgba(231, 76, 60, 0.1)'
                ))
                
                fig.update_layout(
                    title="AI Cost Projections: 2024-2027",
                    xaxis_title="Year",
                    yaxis_title="Cost per Million Tokens ($)",
                    yaxis_type="log",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Create simple projection data for validation
            projection_data = pd.DataFrame({
                'year': list(range(2024, 2028)),
                'conservative': [0.07, 0.035, 0.018, 0.009],
                'aggressive': [0.07, 0.014, 0.003, 0.0006]
            })
            
            # Use safe plotting for projections
            if safe_plot_check(
                projection_data,
                "Cost Projection Data",
                required_columns=['year', 'conservative', 'aggressive'],
                plot_func=plot_cost_projections
            ):
                st.info("""
                **📊 Projection Assumptions:**
                - **Conservative:** Based on historical semiconductor improvements
                - **Aggressive:** Based on current AI-specific optimization rates
                - By 2027, costs could be 1000-10,000x lower than 2022
                """)
        
        # Additional insights and data source
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("🎯 **Key Cost Drivers:**")
            try:
                # Calculate cost reduction metrics from available data
                if len(cost_data) >= 2:
                    max_cost = cost_data['cost_per_million_tokens'].max()
                    min_cost = cost_data['cost_per_million_tokens'].min()
                    reduction_factor = max_cost / min_cost if min_cost > 0 else 0
                    st.write(f"• **Total reduction:** {reduction_factor:.0f}x cost decrease")
                
                st.write("• **Algorithm efficiency:** Model optimizations")
                st.write("• **Hardware advances:** Specialized AI chips")
                st.write("• **Scale effects:** Larger deployment volumes")
                st.write("• **Competition:** Multiple AI providers")
            except Exception as e:
                logger.error(f"Error calculating cost metrics: {e}")
                st.write("• **Algorithm efficiency:** Model optimizations")
                st.write("• **Hardware advances:** Specialized AI chips")
                st.write("• **Scale effects:** Larger deployment volumes")
                st.write("• **Competition:** Multiple AI providers")
        
        with col2:
            if st.button("📊 View Data Source", key="cost_trends_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('ai_index'))
            
            # Calculate cost per FLOP if possible
            st.info("**💡 Cost per FLOP:** AI hardware efficiency improvements enable dramatic cost reductions beyond traditional computing")
            
            # Safe download button
            safe_download_button(
                cost_data,
                clean_filename(f"ai_cost_trends_{data_year}.csv"),
                "📥 Download Cost Data",
                key="download_cost_trends",
                help_text="Download AI cost reduction and hardware improvement data"
            )
    
    else:
        st.warning("AI cost reduction data not available for analysis")
        # Offer retry button if needed
        if dashboard_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.info("Try refreshing the page or check the data source")
            with col2:
                if st.button("🔄 Reload Data", key="retry_cost_data"):
                    st.cache_data.clear()
                    st.rerun()
        
        # Fallback content with static data
        st.write("**📊 Key Cost Reduction Facts (AI Index 2025):**")
        st.write("• AI inference costs dropped **286x** in 2 years")
        st.write("• From $20 to $0.07 per million tokens")
        st.write("• Hardware performance improving **43% annually**")
        st.write("• Price/performance improving **30% annually**")