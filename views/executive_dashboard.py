"""
Executive Dashboard view for AI Adoption Dashboard
Provides comprehensive executive-level analytics and strategic insights
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from Utils.data_validation import safe_plot_check, DataValidator, safe_download_button
from Utils.helpers import clean_filename
from business.roi_calculator import roi_calculator
from business.metrics import business_metrics

logger = logging.getLogger(__name__)


def show_executive_dashboard(
    data_year: str,
    dashboard_data: Dict[str, Any] = None,
    sources_data: pd.DataFrame = None
) -> None:
    """
    Display comprehensive executive dashboard with strategic insights
    
    Args:
        data_year: Selected year (e.g., "2025")
        dashboard_data: Full dashboard data dict
        sources_data: DataFrame with source information
    """
    
    def show_source_info(source_type: str) -> str:
        """Return source information for different data types"""
        if source_type == 'executive_summary':
            return "**Source**: Stanford AI Index 2025, McKinsey Global Survey, Goldman Sachs Economics Analysis\n\n**Methodology**: Comprehensive analysis of AI adoption trends, economic impact, and strategic positioning across industries."
        elif source_type == 'strategic_metrics':
            return "**Source**: Federal Reserve Productivity Research, IMF Working Papers, NBER Studies\n\n**Methodology**: Analysis of productivity gains, ROI metrics, and competitive positioning from authoritative economic research."
        return "**Source**: AI Executive Intelligence 2025"
    
    st.write("👔 **Executive Dashboard: Strategic AI Intelligence**")
    
    # Extract key datasets
    historical_data = dashboard_data.get('historical_data', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    sector_2025 = dashboard_data.get('sector_2025', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    financial_impact = dashboard_data.get('financial_impact', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    ai_investment = dashboard_data.get('ai_investment', pd.DataFrame()) if dashboard_data else pd.DataFrame()
    
    # Create executive tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Summary",
        "🎯 Strategic Positioning", 
        "💰 Financial Performance",
        "🔮 Strategic Outlook",
        "📈 Action Insights"
    ])
    
    with tab1:
        show_executive_summary(historical_data, sector_2025, financial_impact, data_year)
    
    with tab2:
        show_strategic_positioning(sector_2025, financial_impact, data_year)
    
    with tab3:
        show_financial_performance(financial_impact, ai_investment, data_year)
    
    with tab4:
        show_strategic_outlook(historical_data, ai_investment, data_year)
    
    with tab5:
        show_action_insights(sector_2025, financial_impact, data_year)


def show_executive_summary(
    historical_data: pd.DataFrame,
    sector_2025: pd.DataFrame, 
    financial_impact: pd.DataFrame,
    data_year: str
) -> None:
    """Display executive summary with key metrics"""
    
    st.markdown("### 📊 Executive Summary")
    st.markdown("*Comprehensive AI adoption and performance overview*")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not sector_2025.empty and 'adoption_rate' in sector_2025.columns:
            avg_adoption = sector_2025['adoption_rate'].mean()
            st.metric(
                label="Average AI Adoption",
                value=f"{avg_adoption:.1f}%",
                delta=f"+{avg_adoption - 65:.1f}% vs 2023"
            )
        else:
            st.metric("Average AI Adoption", "78%", "+13% vs 2023")
    
    with col2:
        if not sector_2025.empty and 'avg_roi' in sector_2025.columns:
            avg_roi = sector_2025['avg_roi'].mean()
            st.metric(
                label="Average ROI",
                value=f"{avg_roi:.1f}x",
                delta=f"+{avg_roi - 2.8:.1f}x vs industry"
            )
        else:
            st.metric("Average ROI", "3.4x", "+0.6x vs industry")
    
    with col3:
        if not financial_impact.empty and 'companies_reporting_revenue_gains' in financial_impact.columns:
            revenue_impact = financial_impact['companies_reporting_revenue_gains'].mean()
            st.metric(
                label="Revenue Impact",
                value=f"{revenue_impact:.0f}%",
                delta="+8% improvement"
            )
        else:
            st.metric("Revenue Impact", "52%", "+8% improvement")
    
    with col4:
        st.metric(
            label="Market Position",
            value="Leading",
            delta="Top quartile performance"
        )
    
    # Strategic insights
    col1, col2 = st.columns(2)
    
    with col1:
        if not historical_data.empty:
            fig = create_adoption_trend_chart(historical_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not sector_2025.empty:
            fig = create_sector_performance_chart(sector_2025)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Executive insights box
    st.markdown("### 🎯 Key Strategic Insights")
    insights_data = get_executive_insights(sector_2025, financial_impact)
    for insight in insights_data:
        st.success(f"✅ {insight}")


def show_strategic_positioning(
    sector_2025: pd.DataFrame,
    financial_impact: pd.DataFrame,
    data_year: str
) -> None:
    """Display strategic positioning analysis"""
    
    st.markdown("### 🎯 Strategic Positioning")
    st.markdown("*Competitive landscape and market positioning analysis*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not sector_2025.empty:
            fig = create_competitive_positioning_chart(sector_2025)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not financial_impact.empty:
            fig = create_roi_heatmap(financial_impact)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Strategic recommendations
    st.markdown("### 📋 Strategic Recommendations")
    recommendations = get_strategic_recommendations(sector_2025)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")


def show_financial_performance(
    financial_impact: pd.DataFrame,
    ai_investment: pd.DataFrame,
    data_year: str
) -> None:
    """Display financial performance analysis"""
    
    st.markdown("### 💰 Financial Performance")
    st.markdown("*Investment returns and financial impact analysis*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not financial_impact.empty:
            fig = create_revenue_impact_chart(financial_impact)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not ai_investment.empty:
            fig = create_investment_growth_chart(ai_investment)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Financial metrics table
    if not financial_impact.empty:
        st.markdown("### 📊 Financial Metrics by Function")
        display_financial_metrics_table(financial_impact)


def show_strategic_outlook(
    historical_data: pd.DataFrame,
    ai_investment: pd.DataFrame,
    data_year: str
) -> None:
    """Display strategic outlook and projections"""
    
    st.markdown("### 🔮 Strategic Outlook")
    st.markdown("*Future trends and strategic projections*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_projection_chart(historical_data)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not ai_investment.empty:
            fig = create_investment_projection_chart(ai_investment)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Strategic outlook insights
    st.markdown("### 🔍 Strategic Outlook Insights")
    outlook_insights = get_outlook_insights()
    for insight in outlook_insights:
        st.info(f"💡 {insight}")


def show_action_insights(
    sector_2025: pd.DataFrame,
    financial_impact: pd.DataFrame,
    data_year: str
) -> None:
    """Display actionable insights and recommendations"""
    
    st.markdown("### 📈 Action Insights")
    st.markdown("*Immediate actions and strategic initiatives*")
    
    # Priority actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 High Priority Actions")
        high_priority = get_high_priority_actions(sector_2025)
        for action in high_priority:
            st.markdown(f"🔥 {action}")
    
    with col2:
        st.markdown("#### ⚡ Quick Wins")
        quick_wins = get_quick_wins(financial_impact)
        for win in quick_wins:
            st.markdown(f"⚡ {win}")
    
    # Investment recommendations
    st.markdown("#### 💰 Investment Recommendations")
    investment_recs = get_investment_recommendations(sector_2025, financial_impact)
    for rec in investment_recs:
        st.markdown(f"💰 {rec}")


# Chart creation functions
def create_adoption_trend_chart(historical_data: pd.DataFrame) -> Optional[go.Figure]:
    """Create adoption trend chart"""
    try:
        if historical_data.empty:
            return None
        
        fig = go.Figure()
        
        if 'ai_use' in historical_data.columns:
            fig.add_trace(go.Scatter(
                x=historical_data['year'],
                y=historical_data['ai_use'],
                mode='lines+markers',
                name='AI Adoption',
                line=dict(color='#1f77b4', width=3)
            ))
        
        if 'genai_use' in historical_data.columns:
            fig.add_trace(go.Scatter(
                x=historical_data['year'],
                y=historical_data['genai_use'],
                mode='lines+markers',
                name='GenAI Adoption',
                line=dict(color='#ff7f0e', width=3)
            ))
        
        fig.update_layout(
            title="AI Adoption Trends",
            xaxis_title="Year",
            yaxis_title="Adoption Rate (%)",
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating adoption trend chart: {e}")
        return None


def create_sector_performance_chart(sector_2025: pd.DataFrame) -> Optional[go.Figure]:
    """Create sector performance chart"""
    try:
        if sector_2025.empty or 'adoption_rate' not in sector_2025.columns:
            return None
        
        fig = px.bar(
            sector_2025.head(6),
            x='adoption_rate',
            y='sector',
            orientation='h',
            title="Sector AI Adoption Leaders",
            color='adoption_rate',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating sector performance chart: {e}")
        return None


def create_competitive_positioning_chart(sector_2025: pd.DataFrame) -> Optional[go.Figure]:
    """Create competitive positioning scatter plot"""
    try:
        if sector_2025.empty:
            return None
        
        fig = px.scatter(
            sector_2025,
            x='adoption_rate' if 'adoption_rate' in sector_2025.columns else sector_2025.columns[1],
            y='avg_roi' if 'avg_roi' in sector_2025.columns else sector_2025.columns[2],
            size='genai_adoption' if 'genai_adoption' in sector_2025.columns else None,
            color='sector',
            title="Competitive Positioning: Adoption vs ROI",
            hover_data=['sector']
        )
        
        fig.update_layout(
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating competitive positioning chart: {e}")
        return None


def create_roi_heatmap(financial_impact: pd.DataFrame) -> Optional[go.Figure]:
    """Create ROI heatmap"""
    try:
        if financial_impact.empty:
            return None
        
        # Create a simplified heatmap of financial impact
        fig = px.bar(
            financial_impact.head(6),
            x='companies_reporting_revenue_gains' if 'companies_reporting_revenue_gains' in financial_impact.columns else financial_impact.columns[1],
            y='function' if 'function' in financial_impact.columns else financial_impact.columns[0],
            orientation='h',
            title="Revenue Impact by Function",
            color='companies_reporting_revenue_gains' if 'companies_reporting_revenue_gains' in financial_impact.columns else financial_impact.columns[1],
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating ROI heatmap: {e}")
        return None


def create_revenue_impact_chart(financial_impact: pd.DataFrame) -> Optional[go.Figure]:
    """Create revenue impact chart"""
    try:
        if financial_impact.empty:
            return None
        
        fig = go.Figure()
        
        if 'companies_reporting_revenue_gains' in financial_impact.columns:
            fig.add_trace(go.Bar(
                x=financial_impact['function'] if 'function' in financial_impact.columns else range(len(financial_impact)),
                y=financial_impact['companies_reporting_revenue_gains'],
                name='Revenue Gains',
                marker_color='green'
            ))
        
        if 'companies_reporting_cost_savings' in financial_impact.columns:
            fig.add_trace(go.Bar(
                x=financial_impact['function'] if 'function' in financial_impact.columns else range(len(financial_impact)),
                y=financial_impact['companies_reporting_cost_savings'],
                name='Cost Savings',
                marker_color='blue'
            ))
        
        fig.update_layout(
            title="Financial Impact by Function",
            xaxis_title="Function",
            yaxis_title="Companies Reporting Impact (%)",
            template="plotly_white",
            height=400,
            barmode='group'
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating revenue impact chart: {e}")
        return None


def create_investment_growth_chart(ai_investment: pd.DataFrame) -> Optional[go.Figure]:
    """Create investment growth chart"""
    try:
        if ai_investment.empty:
            return None
        
        fig = go.Figure()
        
        if 'total_investment' in ai_investment.columns:
            fig.add_trace(go.Scatter(
                x=ai_investment['year'],
                y=ai_investment['total_investment'],
                mode='lines+markers',
                name='Total Investment',
                line=dict(color='#1f77b4', width=3)
            ))
        
        if 'genai_investment' in ai_investment.columns:
            fig.add_trace(go.Scatter(
                x=ai_investment['year'],
                y=ai_investment['genai_investment'],
                mode='lines+markers',
                name='GenAI Investment',
                line=dict(color='#ff7f0e', width=3)
            ))
        
        fig.update_layout(
            title="AI Investment Growth",
            xaxis_title="Year",
            yaxis_title="Investment ($B)",
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating investment growth chart: {e}")
        return None


def create_projection_chart(historical_data: pd.DataFrame) -> go.Figure:
    """Create future projections chart"""
    try:
        # Create projection data
        years = list(range(2024, 2028))
        conservative = [78, 82, 85, 87]
        realistic = [78, 85, 90, 94]
        optimistic = [78, 88, 95, 98]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=conservative,
            mode='lines+markers',
            name='Conservative',
            line=dict(color='orange', dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=realistic,
            mode='lines+markers',
            name='Realistic',
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=optimistic,
            mode='lines+markers',
            name='Optimistic',
            line=dict(color='green', dash='dot')
        ))
        
        fig.update_layout(
            title="AI Adoption Projections (2024-2027)",
            xaxis_title="Year",
            yaxis_title="Projected Adoption Rate (%)",
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating projection chart: {e}")
        return go.Figure()


def create_investment_projection_chart(ai_investment: pd.DataFrame) -> Optional[go.Figure]:
    """Create investment projection chart"""
    try:
        # Create investment projections
        years = list(range(2024, 2028))
        projected_investment = [252, 320, 410, 520]
        
        fig = go.Figure()
        
        if not ai_investment.empty and 'total_investment' in ai_investment.columns:
            # Add historical data
            fig.add_trace(go.Scatter(
                x=ai_investment['year'],
                y=ai_investment['total_investment'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='blue')
            ))
        
        # Add projections
        fig.add_trace(go.Scatter(
            x=years,
            y=projected_investment,
            mode='lines+markers',
            name='Projected',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title="AI Investment Projections",
            xaxis_title="Year",
            yaxis_title="Investment ($B)",
            template="plotly_white",
            height=400
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating investment projection chart: {e}")
        return None


def display_financial_metrics_table(financial_impact: pd.DataFrame) -> None:
    """Display financial metrics in a formatted table"""
    try:
        if financial_impact.empty:
            st.warning("No financial data available")
            return
        
        # Create formatted display
        display_df = financial_impact.copy()
        
        if 'companies_reporting_revenue_gains' in display_df.columns:
            display_df['Revenue Impact'] = display_df['companies_reporting_revenue_gains'].apply(lambda x: f"{x}%")
        
        if 'companies_reporting_cost_savings' in display_df.columns:
            display_df['Cost Savings'] = display_df['companies_reporting_cost_savings'].apply(lambda x: f"{x}%")
        
        # Select display columns
        display_cols = ['function'] if 'function' in display_df.columns else [display_df.columns[0]]
        if 'Revenue Impact' in display_df.columns:
            display_cols.append('Revenue Impact')
        if 'Cost Savings' in display_df.columns:
            display_cols.append('Cost Savings')
        
        st.dataframe(display_df[display_cols], use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error displaying financial metrics table: {e}")
        st.error("Error displaying financial metrics")


# Insight generation functions
def get_executive_insights(sector_2025: pd.DataFrame, financial_impact: pd.DataFrame) -> list:
    """Generate executive insights"""
    insights = []
    
    try:
        if not sector_2025.empty and 'adoption_rate' in sector_2025.columns:
            top_sector = sector_2025.loc[sector_2025['adoption_rate'].idxmax(), 'sector']
            top_rate = sector_2025['adoption_rate'].max()
            insights.append(f"{top_sector} leads AI adoption at {top_rate:.1f}%")
        
        if not financial_impact.empty and 'companies_reporting_revenue_gains' in financial_impact.columns:
            top_function = financial_impact.loc[
                financial_impact['companies_reporting_revenue_gains'].idxmax(),
                'function' if 'function' in financial_impact.columns else financial_impact.columns[0]
            ]
            insights.append(f"{top_function} shows highest revenue impact")
        
        insights.append("AI adoption accelerating across all major sectors")
        insights.append("ROI improving with matured implementation strategies")
        
    except Exception as e:
        logger.error(f"Error generating executive insights: {e}")
        insights = ["AI adoption continues to drive business value"]
    
    return insights


def get_strategic_recommendations(sector_2025: pd.DataFrame) -> list:
    """Generate strategic recommendations"""
    recommendations = [
        "**Accelerate AI adoption** in underperforming business functions to capture competitive advantage",
        "**Invest in GenAI capabilities** to enhance productivity and innovation outcomes", 
        "**Develop AI governance frameworks** to ensure responsible and effective deployment",
        "**Build internal AI expertise** through targeted hiring and training programs",
        "**Create AI Centers of Excellence** to drive enterprise-wide adoption and best practices"
    ]
    
    return recommendations


def get_outlook_insights() -> list:
    """Generate strategic outlook insights"""
    insights = [
        "AI adoption expected to reach 90%+ by 2027 across leading sectors",
        "GenAI integration will drive next wave of productivity improvements", 
        "Investment in AI infrastructure will accelerate competitive differentiation",
        "Regulatory frameworks will shape enterprise AI deployment strategies",
        "Skills development becomes critical competitive advantage"
    ]
    
    return insights


def get_high_priority_actions(sector_2025: pd.DataFrame) -> list:
    """Generate high priority actions"""
    actions = [
        "**Establish AI governance framework** with clear ROI metrics and risk management",
        "**Launch pilot programs** in highest-ROI business functions",
        "**Invest in data infrastructure** to support AI/ML model deployment",
        "**Develop AI talent strategy** including hiring and upskilling programs"
    ]
    
    return actions


def get_quick_wins(financial_impact: pd.DataFrame) -> list:
    """Generate quick win opportunities"""
    wins = [
        "**Automate routine processes** in marketing and sales operations",
        "**Implement AI-powered analytics** for customer service optimization",
        "**Deploy GenAI tools** for content creation and document processing",
        "**Optimize supply chain** with predictive analytics and demand forecasting"
    ]
    
    return wins


def get_investment_recommendations(sector_2025: pd.DataFrame, financial_impact: pd.DataFrame) -> list:
    """Generate investment recommendations"""
    recommendations = [
        "**Prioritize technology infrastructure** investments to support scalable AI deployment",
        "**Fund AI talent acquisition** and development programs for competitive advantage",
        "**Invest in data quality initiatives** to maximize AI model effectiveness",
        "**Allocate budget for AI governance** and risk management capabilities"
    ]
    
    return recommendations