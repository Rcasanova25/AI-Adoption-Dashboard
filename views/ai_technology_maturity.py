"""AI Technology Maturity view module for AI Adoption Dashboard.

This module provides visualizations of AI technology maturity levels,
adoption rates, and risk assessments based on Gartner's hype cycle framework.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any


def render(data: Dict[str, Any]) -> None:
    """Render the AI Technology Maturity view.
    
    Args:
        data: Dictionary containing required data:
            - ai_maturity: Data on AI technologies, adoption, maturity, and risk
            - a11y: Accessibility helper module
    """
    # Extract required data
    ai_maturity = data.get('ai_maturity')
    a11y = data.get('a11y')
    
    st.write("🎯 **AI Technology Maturity & Adoption (Gartner 2025)**")
    
    # Enhanced maturity visualization
    color_map = {
        'Peak of Expectations': '#F59E0B',
        'Trough of Disillusionment': '#6B7280', 
        'Slope of Enlightenment': '#10B981'
    }
    
    fig = go.Figure()
    
    # Group by maturity stage
    for stage in ai_maturity['maturity'].unique():
        stage_data = ai_maturity[ai_maturity['maturity'] == stage]
        
        fig.add_trace(go.Scatter(
            x=stage_data['adoption_rate'],
            y=stage_data['risk_score'],
            mode='markers+text',
            name=stage,
            marker=dict(
                size=stage_data['time_to_value'] * 10,
                color=color_map[stage],
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
        showlegend=True
    )
    
    fig = a11y.make_chart_accessible(
        fig,
        title="AI Technology Risk-Adoption Matrix",
        description="A scatter plot showing AI technologies positioned by adoption rate (x-axis, 0-100%) and risk score (y-axis, 0-100), with bubble sizes representing time to value in years. The chart is divided into four quadrants by dashed lines at 50% on each axis. Technologies are grouped by maturity stage: Peak of Expectations (orange) includes GenAI (68% adoption, 75 risk, 2 years), AI Agents (15% adoption, 85 risk, 4 years), and AGI (5% adoption, 95 risk, 10 years). Trough of Disillusionment (gray) includes Foundation Models (45% adoption, 60 risk, 3 years) and Edge AI (35% adoption, 40 risk, 3 years). Slope of Enlightenment (green) includes Cloud AI Services (82% adoption, 25 risk, 1 year), MLOps (55% adoption, 35 risk, 2 years), and Composite AI (25% adoption, 45 risk, 7 years). The chart helps identify mature, low-risk technologies versus emerging, high-risk opportunities."
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Maturity insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Strategic Recommendations:**")
        st.write("• **Invest in:** Cloud AI Services (low risk, high adoption)")
        st.write("• **Watch:** AI Agents (high potential, high risk)")
        st.write("• **Mature:** Foundation Models moving past hype")
    
    with col2:
        st.write("**⏱️ Time to Value:**")
        st.write("• **Fastest:** Cloud AI Services (1 year)")
        st.write("• **Medium:** Most technologies (3 years)")
        st.write("• **Longest:** Composite AI (7 years)")