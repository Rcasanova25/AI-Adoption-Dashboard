"""Industry Analysis view for AI Adoption Dashboard."""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
from components.accessibility import AccessibilityManager
from components.view_enhancements import ViewEnhancements


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the industry analysis view.
    
    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        sector_2025 = data.get('sector_2025', pd.DataFrame())
        
        # Initialize accessibility manager
        a11y = AccessibilityManager()
        
        st.write("🏭 **AI Adoption by Industry (2025)**")
        
        # Industry comparison
        fig = go.Figure()
        
        # Create grouped bar chart
        fig.add_trace(go.Bar(
            name='Overall AI Adoption',
            x=sector_2025['sector'],
            y=sector_2025['adoption_rate'],
            marker_color='#3498DB',
            text=[f'{x}%' for x in sector_2025['adoption_rate']],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='GenAI Adoption',
            x=sector_2025['sector'],
            y=sector_2025['genai_adoption'],
            marker_color='#E74C3C',
            text=[f'{x}%' for x in sector_2025['genai_adoption']],
            textposition='outside'
        ))
        
        # Add ROI as line chart
        fig.add_trace(go.Scatter(
            name='Average ROI',
            x=sector_2025['sector'],
            y=sector_2025['avg_roi'],
            mode='lines+markers',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            yaxis='y2',
            text=[f'{x}x' for x in sector_2025['avg_roi']],
            textposition='top center'
        ))
        
        fig.update_layout(
            title="AI Adoption and ROI by Industry Sector",
            xaxis_title="Industry",
            yaxis=dict(title="Adoption Rate (%)", side="left"),
            yaxis2=dict(title="Average ROI (x)", side="right", overlaying="y"),
            barmode='group',
            height=500,
            hovermode='x unified',
            xaxis_tickangle=45
        )
        
        fig = a11y.make_chart_accessible(
            fig,
            title="AI Adoption and ROI by Industry Sector",
            description="Combined bar and line chart showing AI adoption rates and ROI by industry sector. Technology sector leads with 92% overall AI adoption and 88% GenAI adoption, achieving 4.2x ROI. Financial Services follows with 85% overall adoption and 3.8x ROI. Healthcare shows 78% adoption with 3.2x ROI. Government has the lowest adoption at 52% with 2.2x ROI."
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Industry insights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Top Adopter", "Technology (92%)", delta="+7% vs Finance")
        with col2:
            st.metric("Highest ROI", "Technology (4.2x)", delta="Best returns")
        with col3:
            st.metric("Fastest Growing", "Healthcare", delta="+15pp YoY")
        
        # Add enhanced insights using ViewEnhancements
        ViewEnhancements.add_industry_analysis_insights(sector_2025)
        
        # Export option
        csv = sector_2025.to_csv(index=False)
        st.download_button(
            label="📥 Download Industry Data (CSV)",
            data=csv,
            file_name="ai_adoption_by_industry_2025.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error rendering industry analysis view: {str(e)}")