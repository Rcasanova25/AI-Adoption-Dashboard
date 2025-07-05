"""Regional Growth view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the regional growth view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    # Data presence check
    regional_growth = data.get("regional_growth")
    if regional_growth is None or regional_growth.empty:
        st.error("Required regional growth data is missing or empty. Please check data sources.")
        st.stop()
    # Initialize accessibility manager
    a11y = AccessibilityManager()

    st.write("🌍 **Regional AI Adoption Growth (AI Index Report 2025)**")

    # Enhanced regional visualization with investment data
    fig = go.Figure()

    # Create subplot figure
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Adoption Growth in 2024", "Investment Growth vs Adoption Rate"),
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.15,
    )

    # Bar chart for adoption growth
    fig.add_trace(
        go.Bar(
            x=regional_growth["region"],
            y=regional_growth["growth_2024"],
            text=[f"+{x}pp" for x in regional_growth["growth_2024"]],
            textposition="outside",
            marker_color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"],
            name="2024 Growth",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    # Scatter plot for investment vs adoption
    fig.add_trace(
        go.Scatter(
            x=regional_growth["adoption_rate"],
            y=regional_growth["investment_growth"],
            mode="markers+text",
            marker=dict(
                size=regional_growth["growth_2024"],
                color=regional_growth["growth_2024"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="2024 Growth (pp)"),
            ),
            text=regional_growth["region"],
            textposition="top center",
            showlegend=False,
        ),
        row=1,
        col=2,
    )

    fig.update_xaxes(title_text="Region", row=1, col=1)
    fig.update_yaxes(title_text="Growth (percentage points)", row=1, col=1)
    fig.update_xaxes(title_text="Current Adoption Rate (%)", row=1, col=2)
    fig.update_yaxes(title_text="Investment Growth (%)", row=1, col=2)

    fig.update_layout(height=450, title_text="Regional AI Adoption and Investment Dynamics")

    fig = a11y.make_chart_accessible(
        fig,
        title="Regional AI Adoption and Investment Dynamics",
        description="Two-panel chart showing regional AI growth patterns. Left panel shows 2024 adoption growth with Greater China leading at +27 percentage points, followed by Europe at +23pp and North America at +15pp. Right panel shows investment growth vs adoption rate scatter plot, with bubble sizes indicating 2024 growth. North America shows highest adoption rate at 82% but slower growth, while Greater China shows rapid growth with 32% investment increase.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Regional insights with metrics
    col1, col2, col3 = st.columns(3)

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

    # Create competitive positioning matrix
    fig2 = px.scatter(
        regional_growth,
        x="adoption_rate",
        y="growth_2024",
        size="investment_growth",
        color="region",
        title="Regional AI Competitive Positioning Matrix",
        labels={
            "adoption_rate": "Current Adoption Rate (%)",
            "growth_2024": "Adoption Growth Rate (pp)",
            "investment_growth": "Investment Growth (%)",
        },
        height=400,
    )

    # Add quadrant lines
    fig2.add_hline(y=regional_growth["growth_2024"].mean(), line_dash="dash", line_color="gray")
    fig2.add_vline(x=regional_growth["adoption_rate"].mean(), line_dash="dash", line_color="gray")

    # Add quadrant labels
    fig2.add_annotation(
        x=50, y=25, text="High Growth<br>Low Base", showarrow=False, font=dict(color="gray")
    )
    fig2.add_annotation(
        x=75, y=25, text="High Growth<br>High Base", showarrow=False, font=dict(color="gray")
    )
    fig2.add_annotation(
        x=50, y=13, text="Low Growth<br>Low Base", showarrow=False, font=dict(color="gray")
    )
    fig2.add_annotation(
        x=75, y=13, text="Low Growth<br>High Base", showarrow=False, font=dict(color="gray")
    )

    fig2 = a11y.make_chart_accessible(
        fig2,
        title="Regional AI Competitive Positioning Matrix",
        description="Scatter plot showing regional AI competitive positioning with four quadrants. X-axis shows current adoption rate, Y-axis shows growth rate, bubble size indicates investment growth. Greater China appears in High Growth/Low Base quadrant, Europe in High Growth/High Base, North America in Low Growth/High Base, and other regions distributed across quadrants. Quadrant lines divide regions by mean adoption rate and growth rate.",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        """
    **Strategic Insights:**
    - **Greater China & Europe:** Aggressive catch-up strategy with high growth rates
    - **North America:** Market leader maintaining position with steady growth
    - **Competition intensifying:** Regional gaps narrowing as adoption accelerates globally
    """
    )
