"""Skill Gap Analysis view module for AI Adoption Dashboard.

This module provides visualizations analyzing the gap between AI skill requirements
and current workforce capabilities, along with training initiatives.
"""

from typing import Any, Dict

import plotly.graph_objects as go
import streamlit as st

from business.labor_impact import analyze_skill_gaps
from data.models.workforce import SkillGaps


def render(data: Dict[str, Any]) -> None:
    """Render the Skill Gap Analysis view.

    Args:
        data: Dictionary containing required data:
            - skill_gap_data: Data on skill gaps and training initiatives
            - a11y: Accessibility helper module
    """
    # Extract required data
    skill_gap_data = data.get("skill_gap_data")
    a11y = data.get("a11y")

    # Data presence checks
    missing = []
    if skill_gap_data is None or (hasattr(skill_gap_data, "empty") and skill_gap_data.empty):
        missing.append("skill_gap_data")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("🎓 **AI Skills Gap Analysis**")

    # Skills gap visualization
    fig = go.Figure()

    # Sort by gap severity
    skill_sorted = skill_gap_data.sort_values("gap_severity", ascending=True)

    # Create diverging bar chart
    fig.add_trace(
        go.Bar(
            name="Gap Severity",
            y=skill_sorted["skill"],
            x=skill_sorted["gap_severity"],
            orientation="h",
            marker_color="#E74C3C",
            text=[f"{x}%" for x in skill_sorted["gap_severity"]],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            name="Training Initiatives",
            y=skill_sorted["skill"],
            x=skill_sorted["training_initiatives"],
            orientation="h",
            marker_color="#2ECC71",
            text=[f"{x}%" for x in skill_sorted["training_initiatives"]],
            textposition="outside",
            xaxis="x2",
        )
    )

    fig.update_layout(
        title="AI Skills Gap vs Training Initiatives",
        xaxis=dict(title="Gap Severity (%)", side="bottom"),
        xaxis2=dict(title="Companies with Training (%)", overlaying="x", side="top"),
        yaxis_title="Skill Area",
        height=500,
        barmode="overlay",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Skills Gap vs Training Initiatives",
        description="A horizontal diverging bar chart comparing AI skills gap severity (red bars) against the percentage of companies with training initiatives (green bars) across seven skill areas. AI/ML Engineering shows the highest gap severity at 85% with only 45% of companies having training programs. Data Science follows with 75% gap severity and 42% training coverage. AI Strategy has a 65% gap with 35% training initiatives. Change Management shows a 55% gap but higher training coverage at 48%. Ethical AI Implementation has a 50% gap with 30% training programs. AI Product Management shows 45% gap severity with 38% training coverage. AI Security has the lowest gap at 40% with 25% of companies offering training. The chart reveals significant mismatches between skill needs and training investments, particularly in technical areas.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.info(
        """
    **🔍 Key Findings:**
    - **AI/ML Engineering** shows the highest gap severity (85%) with only 45% of companies having training programs
    - **Change Management** has a lower gap (55%) but higher training coverage (48%), showing organizational awareness
    - The gap between severity and training initiatives indicates significant opportunity for workforce development
    """
    )

    # Skill gap summary
    summary = analyze_skill_gaps(
        [
            SkillGaps(
                skill_category=row["skill"],
                demand_index=row.get("demand_index", 0),
                supply_index=row.get("supply_index", 0),
                gap_severity=row["gap_severity"],
                training_time_months=row.get("training_time_months"),
                salary_premium_percent=row.get("salary_premium_percent"),
            )
            for _, row in skill_gap_data.iterrows()
        ]
    )
    st.info(f"Overall Skill Gap Severity: {summary}")
