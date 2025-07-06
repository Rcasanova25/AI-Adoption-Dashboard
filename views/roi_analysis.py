"""ROI Analysis view module for AI Adoption Dashboard.

This module provides comprehensive ROI analysis visualizations including
investment returns, payback analysis, sector-specific ROI, and an
interactive ROI calculator.
"""

from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from business.roi_analysis import compute_roi


def render(data: Dict[str, Any]) -> None:
    """Render the ROI Analysis view.

    Args:
        data: Dictionary containing required data:
            - sector_2025: Sector data including ROI metrics
            - a11y: Accessibility helper module
    """
    # Extract required data
    sector_2025 = data.get("sector_2025")
    a11y = data.get("a11y")

    # Data presence checks
    missing = []
    if sector_2025 is None or (hasattr(sector_2025, "empty") and sector_2025.empty):
        missing.append("sector_2025")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("💰 **ROI Analysis: Comprehensive Economic Impact**")

    # Create detailed ROI dashboard
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Investment Returns", "Payback Analysis", "Sector ROI", "ROI Calculator"]
    )

    with tab1:
        _render_investment_returns(a11y)

    with tab2:
        _render_payback_analysis(a11y)

    with tab3:
        _render_sector_roi(sector_2025, a11y)

    with tab4:
        _render_roi_calculator(a11y)


def _render_investment_returns(a11y: Any) -> None:
    """Render the investment returns tab."""
    # TODO: Load roi_data from actual data source
    roi_data = pd.DataFrame()

    fig = go.Figure()

    # ROI bars
    fig.add_trace(
        go.Bar(
            name="Average ROI",
            x=roi_data["investment_level"],
            y=roi_data["avg_roi"],
            yaxis="y",
            marker_color="#2ECC71",
            text=[f"{x}x" for x in roi_data["avg_roi"]],
            textposition="outside",
        )
    )

    # Success rate line
    fig.add_trace(
        go.Scatter(
            name="Success Rate",
            x=roi_data["investment_level"],
            y=roi_data["success_rate"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(width=3, color="#3498DB"),
            marker=dict(size=10),
        )
    )

    fig.update_layout(
        title="AI ROI by Investment Level",
        xaxis_title="Investment Level",
        yaxis=dict(title="Average ROI (x)", side="left"),
        yaxis2=dict(title="Success Rate (%)", side="right", overlaying="y"),
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI ROI by Investment Level",
        description="A dual-axis chart showing the relationship between AI investment levels and returns. Green bars display average ROI multipliers on the left y-axis: Small investments (<$100K) yield 1.8x ROI, Medium ($100K-$500K) achieve 2.5x, Large ($500K-$2M) reach 3.2x, Enterprise ($2M-$10M) deliver 3.8x, and Enterprise ($10M+) deliver 4.5x returns. A blue line shows success rates on the right y-axis, increasing from 45% for small investments to 87% for enterprise-level investments. The chart demonstrates that larger AI investments correlate with both higher returns and greater success rates.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
    **Key Insights:**
    - Larger investments show higher ROI and success rates
    - Enterprise projects (87% success) benefit from better resources and planning
    - Even small pilots can achieve 1.8x ROI with 45% success rate
    """
    )


def _render_payback_analysis(a11y: Any) -> None:
    """Render the payback analysis tab."""
    # TODO: Load payback_data from actual data source
    payback_data = pd.DataFrame()

    fig = go.Figure()

    # Create funnel chart for payback scenarios
    fig.add_trace(
        go.Funnel(
            y=payback_data["scenario"],
            x=payback_data["months"],
            textinfo="text+percent initial",
            text=[f"{x} months" for x in payback_data["months"]],
            marker=dict(color=["#2ECC71", "#F39C12", "#E74C3C"]),
        )
    )

    fig.update_layout(
        title="AI Investment Payback Period Distribution",
        xaxis_title="Months to Payback",
        height=350,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Investment Payback Period Distribution",
        description="A funnel chart showing the distribution of AI investment payback periods across three scenarios. Best Case scenario (green, 20% probability) achieves payback in 8 months. Typical scenario (orange, 60% probability) reaches payback in 15 months. Conservative scenario (red, 20% probability) requires 24 months for payback. The visualization shows that most AI investments (60%) achieve payback within 15 months, with only 20% taking longer than 2 years.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Time to value breakdown
    st.subheader("⏱️ Time to Value by AI Capability")

    # TODO: Load time_to_value data from actual data source
    time_to_value = pd.DataFrame()

    fig2 = px.bar(
        time_to_value,
        x="capability",
        y="months_to_value",
        color="complexity",
        color_continuous_scale="RdYlGn_r",
        title="Time to Value by AI Capability",
        labels={"months_to_value": "Months to Value", "complexity": "Implementation Complexity"},
    )

    fig2.update_traces(texttemplate="%{y} months", textposition="outside")
    fig2.update_layout(xaxis_tickangle=45, height=400)

    fig2 = a11y.make_chart_accessible(
        fig2,
        title="Time to Value by AI Capability",
        description="A bar chart showing time to value for different AI capabilities, colored by implementation complexity (1-5 scale, red=high, green=low). Process Automation delivers value in 3 months with low complexity (2). GenAI Applications show quick returns at 4 months with low complexity (2). Predictive Analytics and Recommendation Systems both achieve value in 6 months with medium complexity (3). Natural Language Processing requires 9 months with high complexity (4). Computer Vision has the longest time to value at 12 months with the highest complexity (5).",
    )
    st.plotly_chart(fig2, use_container_width=True)


def _render_sector_roi(sector_2025: pd.DataFrame, a11y: Any) -> None:
    """Render the sector ROI tab."""
    fig = go.Figure()

    # Create bubble chart
    fig.add_trace(
        go.Scatter(
            x=sector_2025["adoption_rate"],
            y=sector_2025["avg_roi"],
            mode="markers+text",
            marker=dict(
                size=sector_2025["genai_adoption"],
                color=sector_2025["avg_roi"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="ROI (x)"),
            ),
            text=sector_2025["sector"],
            textposition="top center",
            hovertemplate="<b>%{text}</b><br>Adoption: %{x}%<br>ROI: %{y}x<br>GenAI Adoption: %{marker.size}%<extra></extra>",
        )
    )

    # Add trend line
    z = np.polyfit(sector_2025["adoption_rate"], sector_2025["avg_roi"], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(
        sector_2025["adoption_rate"].min(), sector_2025["adoption_rate"].max(), 100
    )

    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Trend",
            showlegend=True,
        )
    )

    fig.update_layout(
        title="Sector AI Adoption vs ROI (Bubble Size = GenAI Adoption)",
        xaxis_title="Overall AI Adoption Rate (%)",
        yaxis_title="Average ROI (x)",
        height=500,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Sector AI Adoption vs ROI",
        description="A bubble chart plotting AI adoption rates (x-axis) against average ROI (y-axis) across sectors, with bubble sizes representing GenAI adoption rates. Technology sector leads with 92% adoption and 4.2x ROI. Financial Services follows with 85% adoption and 3.8x ROI. Healthcare shows 78% adoption with 3.2x ROI. Manufacturing has 75% adoption and 3.5x ROI. Retail & E-commerce displays 72% adoption with 3.0x ROI. Education shows 65% adoption and 2.5x ROI. Energy & Utilities has 58% adoption with 2.8x ROI. Government trails with 52% adoption and 2.2x ROI. A red dashed trend line shows positive correlation between adoption and ROI.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ROI components breakdown
    st.subheader("💡 ROI Components by Sector")

    # TODO: Load roi_components data from actual data source
    roi_components = pd.DataFrame()

    fig2 = go.Figure()

    for sector in ["Technology", "Financial Services", "Healthcare", "Manufacturing"]:
        fig2.add_trace(
            go.Bar(
                name=sector,
                x=roi_components["component"],
                y=roi_components[sector],
                text=[f"{x}%" for x in roi_components[sector]],
                textposition="outside",
            )
        )

    fig2.update_layout(
        title="ROI Component Contribution by Sector",
        xaxis_title="ROI Component",
        yaxis_title="Contribution to Total ROI (%)",
        barmode="group",
        height=400,
    )

    st.plotly_chart(fig2, use_container_width=True)


def _render_roi_calculator(a11y: Any) -> None:
    """Render the ROI calculator tab."""
    st.subheader("ROI Calculator")
    with st.form("roi_form"):
        initial_investment = st.number_input(
            "Initial Investment ($)", min_value=0.0, value=100000.0
        )
        annual_savings = st.number_input("Annual Savings ($)", min_value=0.0, value=25000.0)
        payback_period_months = st.number_input("Payback Period (months)", min_value=1, value=12)
        risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High", "Very High"], index=1)
        productivity_gain_percent = st.number_input(
            "Productivity Gain (%)", min_value=0.0, value=10.0
        )
        submitted = st.form_submit_button("Calculate ROI")
    if submitted:
        roi_metrics = compute_roi(
            initial_investment=initial_investment,
            annual_savings=annual_savings,
            payback_period_months=payback_period_months,
            risk_level=risk_level,
            productivity_gain_percent=productivity_gain_percent,
        )
        st.success(f"Total ROI: {roi_metrics.total_roi_percent:.2f}%")
        st.info(
            f"Payback Period: {roi_metrics.payback_period_months} months\n"
            f"Breakeven: {roi_metrics.breakeven_months} months\n"
            f"Risk Level: {roi_metrics.risk_level}\n"
            f"Productivity Gain: {roi_metrics.productivity_gain_percent}%"
        )
