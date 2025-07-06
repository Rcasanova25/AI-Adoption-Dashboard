"""OECD 2025 Findings view module for AI Adoption Dashboard.

This module provides visualizations and analysis of the OECD/BCG/INSEAD 2025 Report
on enterprise AI adoption, including country comparisons, application trends,
and success factors analysis.
"""

from typing import Any, Dict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render(data: Dict[str, Any]) -> None:
    """Render the OECD 2025 Findings view.

    Args:
        data: Dictionary containing required data:
            - oecd_g7_adoption: G7 country adoption data
            - oecd_applications: AI application usage data
            - a11y: Accessibility helper module
            - show_source_info: Function to display source information
    """
    # Extract required data
    oecd_g7_adoption = data.get("oecd_g7_adoption")
    oecd_applications = data.get("oecd_applications")
    a11y = data.get("a11y")
    show_source_info = data.get("show_source_info")

    # Data presence checks
    missing = []
    if oecd_g7_adoption is None or (hasattr(oecd_g7_adoption, "empty") and oecd_g7_adoption.empty):
        missing.append("oecd_g7_adoption")
    if oecd_applications is None or (
        hasattr(oecd_applications, "empty") and oecd_applications.empty
    ):
        missing.append("oecd_applications")
    if a11y is None:
        missing.append("a11y")
    if show_source_info is None:
        missing.append("show_source_info")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("📊 **OECD/BCG/INSEAD 2025 Report: Enterprise AI Adoption**")

    # Enhanced OECD visualization
    tab1, tab2, tab3 = st.tabs(["Country Analysis", "Application Trends", "Success Factors"])

    with tab1:
        _render_country_analysis(oecd_g7_adoption, a11y, show_source_info)

    with tab2:
        _render_application_trends(oecd_applications, a11y)

    with tab3:
        _render_success_factors(a11y)


def _render_country_analysis(oecd_g7_adoption, a11y, show_source_info):
    """Render G7 country analysis tab."""
    fig = go.Figure()
    x = oecd_g7_adoption["country"]

    fig.add_trace(
        go.Bar(
            name="Overall Adoption",
            x=x,
            y=oecd_g7_adoption["adoption_rate"],
            marker_color="#3B82F6",
            text=[f"{v}%" for v in oecd_g7_adoption["adoption_rate"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Manufacturing",
            x=x,
            y=oecd_g7_adoption["manufacturing"],
            marker_color="#10B981",
            text=[f"{v}%" for v in oecd_g7_adoption["manufacturing"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            name="ICT Sector",
            x=x,
            y=oecd_g7_adoption["ict_sector"],
            marker_color="#F59E0B",
            text=[f"{v}%" for v in oecd_g7_adoption["ict_sector"]],
            textposition="outside",
        )
    )

    g7_avg = oecd_g7_adoption["adoption_rate"].mean()
    fig.add_hline(
        y=g7_avg,
        line_dash="dash",
        line_color="red",
        annotation_text=f"G7 Average: {g7_avg:.0f}%",
        annotation_position="right",
    )

    fig.update_layout(
        title="AI Adoption Rates Across G7 Countries by Sector",
        xaxis_title="Country",
        yaxis_title="Adoption Rate (%)",
        barmode="group",
        height=450,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Adoption Rates Across G7 Countries by Sector",
        description="A grouped bar chart comparing AI adoption rates across G7 countries with three categories per country: Overall Adoption (blue), Manufacturing (green), and ICT Sector (orange). Japan leads with 48% overall adoption, 52% in manufacturing, and 65% in ICT. United States follows with 45% overall, 48% manufacturing, and 62% ICT. Canada shows 42% overall, 45% manufacturing, and 60% ICT. United Kingdom has 40% overall, 43% manufacturing, and 58% ICT. Germany displays 38% overall, 42% manufacturing, and 55% ICT. France shows 35% overall, 38% manufacturing, and 52% ICT. Italy has the lowest rates at 32% overall, 35% manufacturing, and 50% ICT. A red dashed line indicates the G7 average of 40%. The chart reveals that ICT sectors consistently lead adoption across all countries, with a 15-20 percentage point gap compared to other sectors.",
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**🌍 Key Findings:**")
        st.write("• **Japan** leads G7 with 48% overall adoption")
        st.write("• **ICT sector** universally leads (55-70%)")
        st.write("• **15-20pp** gap between ICT and other sectors")
    with col2:
        if st.button("📊 View OECD Methodology", key="oecd_method"):
            with st.expander("Methodology", expanded=True):
                st.info(show_source_info("oecd"))


def _render_application_trends(oecd_applications, a11y):
    """Render application trends tab."""
    genai_apps = oecd_applications[oecd_applications["category"] == "GenAI"]
    traditional_apps = oecd_applications[oecd_applications["category"] == "Traditional AI"]

    fig = go.Figure()
    # GenAI applications
    fig.add_trace(
        go.Bar(
            name="GenAI Applications",
            y=genai_apps.sort_values("usage_rate")["application"],
            x=genai_apps.sort_values("usage_rate")["usage_rate"],
            orientation="h",
            marker_color="#E74C3C",
            text=[f"{x}%" for x in genai_apps.sort_values("usage_rate")["usage_rate"]],
            textposition="outside",
        )
    )
    # Traditional AI applications
    fig.add_trace(
        go.Bar(
            name="Traditional AI",
            y=traditional_apps.sort_values("usage_rate")["application"],
            x=traditional_apps.sort_values("usage_rate")["usage_rate"],
            orientation="h",
            marker_color="#3498DB",
            text=[f"{x}%" for x in traditional_apps.sort_values("usage_rate")["usage_rate"]],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="AI Application Usage: GenAI vs Traditional AI",
        xaxis_title="Usage Rate (% of AI-adopting firms)",
        height=600,
        showlegend=True,
        barmode="overlay",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Application Usage: GenAI vs Traditional AI",
        description="A horizontal bar chart comparing usage rates of GenAI applications (red) versus Traditional AI applications (blue) among AI-adopting firms. GenAI applications are led by Content Generation at 68%, followed by Code Generation at 55%, Chatbots/Virtual Assistants at 48%, and Knowledge Management at 42%. Traditional AI applications show Computer Vision at 45%, Recommendation Systems at 38%, Fraud Detection at 35%, Predictive Maintenance at 32%, and Process Automation at 28%. The chart demonstrates that GenAI applications, particularly content and code generation, have overtaken traditional AI use cases in enterprise adoption, reflecting the transformative impact of large language models on business operations.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "**Key Trend:** GenAI applications (content generation, code generation, chatbots) now lead adoption rates"
    )


def _render_success_factors(a11y):
    """Render success factors tab."""
    success_factors = pd.DataFrame(
        {
            "factor": [
                "Leadership Commitment",
                "Data Infrastructure",
                "Talent Availability",
                "Change Management",
                "Partnership Ecosystem",
                "Regulatory Clarity",
            ],
            "importance": [92, 88, 85, 78, 72, 68],
            "readiness": [65, 72, 45, 52, 58, 48],
        }
    )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Importance",
            x=success_factors["factor"],
            y=success_factors["importance"],
            marker_color="#3498DB",
            text=[f"{x}%" for x in success_factors["importance"]],
            textposition="outside",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Current Readiness",
            x=success_factors["factor"],
            y=success_factors["readiness"],
            marker_color="#E74C3C",
            text=[f"{x}%" for x in success_factors["readiness"]],
            textposition="outside",
        )
    )

    # Calculate and display gaps
    gaps = success_factors["importance"] - success_factors["readiness"]
    fig.add_trace(
        go.Scatter(
            name="Gap",
            x=success_factors["factor"],
            y=gaps,
            mode="markers+text",
            marker=dict(size=15, color="orange"),
            text=[f"-{x}pp" for x in gaps],
            textposition="top center",
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="AI Success Factors: Importance vs Readiness Gap",
        xaxis_title="Success Factor",
        yaxis=dict(title="Score (%)", side="left"),
        yaxis2=dict(title="Gap (pp)", side="right", overlaying="y", range=[0, 50]),
        height=450,
        barmode="group",
        xaxis_tickangle=45,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Success Factors: Importance vs Readiness Gap",
        description="A combination chart showing AI success factors with three metrics: Importance (blue bars), Readiness (red bars), and the Gap between them (orange scatter points with values). Leadership Commitment, Data Infrastructure, and Talent Availability show the largest gaps between importance and readiness, highlighting the global AI skills shortage.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        "**Critical Gap:** Talent availability shows the largest readiness gap (40pp), highlighting the global AI skills shortage"
    )
