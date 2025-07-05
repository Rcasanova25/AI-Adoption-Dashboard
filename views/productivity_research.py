"""Productivity Research view module for AI Adoption Dashboard.

This module provides comprehensive visualizations and analysis of AI's impact
on productivity across different dimensions including historical context,
skill-level impacts, and economic estimates.
"""

from typing import Any, Dict

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render(data: Dict[str, Any]) -> None:
    """Render the Productivity Research view.

    Args:
        data: Dictionary containing required data:
            - productivity_data: Historical productivity and demographics data
            - productivity_by_skill: Productivity impact by skill level
            - ai_productivity_estimates: Various productivity estimates by source
            - a11y: Accessibility helper module
    """
    # Extract required data
    productivity_data = data.get("productivity_data")
    productivity_by_skill = data.get("productivity_by_skill")
    ai_productivity_estimates = data.get("ai_productivity_estimates")
    a11y = data.get("a11y")

    # Data presence checks (must be before any access to the data)
    missing = []
    if productivity_data is None or (
        hasattr(productivity_data, "empty") and productivity_data.empty
    ):
        missing.append("productivity_data")
    if productivity_by_skill is None or (
        hasattr(productivity_by_skill, "empty") and productivity_by_skill.empty
    ):
        missing.append("productivity_by_skill")
    if ai_productivity_estimates is None or (
        hasattr(ai_productivity_estimates, "empty") and ai_productivity_estimates.empty
    ):
        missing.append("ai_productivity_estimates")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("📊 **AI Productivity Impact Research**")

    # Create tabs for different productivity views
    tab1, tab2, tab3 = st.tabs(["Historical Context", "Skill-Level Impact", "Economic Estimates"])

    with tab1:
        # Historical productivity paradox
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=productivity_data["year"],
                y=productivity_data["productivity_growth"],
                mode="lines+markers",
                name="Productivity Growth (%)",
                line=dict(width=3, color="#3B82F6"),
                yaxis="y",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=productivity_data["year"],
                y=productivity_data["young_workers_share"],
                mode="lines+markers",
                name="Young Workers Share (25-34)",
                line=dict(width=3, color="#EF4444"),
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="The Productivity Paradox: Demographics vs Technology",
            xaxis_title="Year",
            yaxis=dict(title="Productivity Growth (%)", side="left"),
            yaxis2=dict(title="Young Workers Share (%)", side="right", overlaying="y"),
            height=500,
            hovermode="x unified",
        )
        fig = a11y.make_chart_accessible(
            fig,
            title="The Productivity Paradox: Demographics vs Technology",
            description="A dual-axis line chart showing the relationship between productivity growth and workforce demographics from 1950 to 2025. The blue line represents productivity growth percentage on the left y-axis, starting at 3.5% in 1950, peaking at 3.8% in 1960, then declining to 0.8% by 2010 before recovering slightly to 1.5% in 2025. The red line shows the share of young workers (ages 25-34) on the right y-axis, starting at 24% in 1950, declining to 19% in 1980, rising to 23% in 1990, then steadily declining to 20% by 2025. The chart illustrates the productivity paradox where technological advances haven't translated to productivity gains, partly explained by demographic shifts in the workforce.",
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # AI productivity by skill level
        fig = px.bar(
            productivity_by_skill,
            x="skill_level",
            y=["productivity_gain", "skill_gap_reduction"],
            title="AI Impact by Worker Skill Level",
            labels={"value": "Percentage (%)", "variable": "Impact Type"},
            barmode="group",
            color_discrete_map={"productivity_gain": "#2ECC71", "skill_gap_reduction": "#3498DB"},
        )

        fig.update_layout(height=400)
        fig = a11y.make_chart_accessible(
            fig,
            title="AI Impact by Worker Skill Level",
            description="A grouped bar chart comparing productivity gains (green bars) and skill gap reduction (blue bars) across three worker skill levels. Low-skilled workers see the highest productivity gain at 14% and 12% skill gap reduction. Medium-skilled workers experience 8% productivity gain and 7% skill gap reduction. High-skilled workers show the smallest gains with 5% productivity improvement and 4% skill gap reduction. This data demonstrates that AI tools provide the greatest relative benefit to low-skilled workers, potentially helping to reduce workplace inequality by narrowing the performance gap between skill levels.",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.success(
            """
        **✅ AI Index 2025 Finding:** AI provides the greatest productivity boost to low-skilled workers (14%), 
        helping to narrow skill gaps and potentially reduce workplace inequality.
        """
        )

    with tab3:
        # Economic impact estimates
        fig = px.bar(
            ai_productivity_estimates,
            x="source",
            y="annual_impact",
            title="AI Productivity Impact Estimates: Academic vs Industry",
            color="annual_impact",
            color_continuous_scale="RdYlBu_r",
            text="annual_impact",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(height=450)
        fig = a11y.make_chart_accessible(
            fig,
            title="AI Productivity Impact Estimates: Academic vs Industry",
            description="A bar chart comparing AI productivity impact estimates from different sources, colored using a red-yellow-blue reversed scale. Conservative academic estimates show the lowest impact: Brynjolfsson et al. at 0.07% and Acemoglu at 0.1% annual productivity growth. Moderate estimates come from Goldman Sachs at 0.5% and PWC at 0.8%. The most optimistic projections are from McKinsey at 1.5% and OpenAI at 2.5% annual impact. The wide range from 0.07% to 2.5% reflects different assumptions about AI implementation speed, scope, and complementary investments. Conservative estimates focus on task-level automation while optimistic projections assume economy-wide transformation.",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            """
        **📊 Note on Estimates:**
        - Conservative estimates (0.07-0.1%) focus on task-level automation
        - Optimistic estimates (1.5-2.5%) assume economy-wide transformation
        - Actual impact depends on implementation quality and complementary investments
        """
        )
