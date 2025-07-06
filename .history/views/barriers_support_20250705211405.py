"""Barriers & Support view module for AI Adoption Dashboard.

This module provides visualizations analyzing barriers to AI adoption
and the effectiveness of various support measures.
"""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render(data: Dict[str, Any]) -> None:
    """Render the Barriers & Support view.

    Args:
        data: Dictionary containing required data:
            - barriers_data: Data on adoption barriers
            - support_effectiveness: Data on support measure effectiveness
            - a11y: Accessibility helper module
    """
    # Extract required data
    barriers_data = data.get("barriers_data")
    support_effectiveness = data.get("support_effectiveness")
    a11y = data.get("a11y")

    # Data presence checks
    missing = []
    if barriers_data is None or (hasattr(barriers_data, "empty") and barriers_data.empty):
        missing.append("barriers_data")
    if support_effectiveness is None or (
        hasattr(support_effectiveness, "empty") and support_effectiveness.empty
    ):
        missing.append("support_effectiveness")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("🚧 **AI Adoption Barriers & Support Effectiveness**")

    # Enhanced barriers visualization
    fig = go.Figure()

    # Sort barriers by severity
    barriers_sorted = barriers_data.sort_values("percentage", ascending=True)

    # Create horizontal bar chart with categories
    barrier_categories = {
        "Lack of skilled personnel": "Talent",
        "Data availability/quality": "Data",
        "Integration with legacy systems": "Technical",
        "Regulatory uncertainty": "Regulatory",
        "High implementation costs": "Financial",
        "Security concerns": "Risk",
        "Unclear ROI": "Financial",
        "Organizational resistance": "Cultural",
    }

    colors = {
        "Talent": "#E74C3C",
        "Data": "#3498DB",
        "Technical": "#9B59B6",
        "Regulatory": "#F39C12",
        "Financial": "#2ECC71",
        "Risk": "#1ABC9C",
        "Cultural": "#34495E",
    }

    barriers_sorted["category"] = barriers_sorted["barrier"].map(barrier_categories)
    barriers_sorted["color"] = barriers_sorted["category"].map(colors)

    fig.add_trace(
        go.Bar(
            y=barriers_sorted["barrier"],
            x=barriers_sorted["percentage"],
            orientation="h",
            marker_color=barriers_sorted["color"],
            text=[f"{x}%" for x in barriers_sorted["percentage"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Severity: %{x}%<br>Category: %{customdata}<extra></extra>",
            customdata=barriers_sorted["category"],
        )
    )

    fig.update_layout(
        title="Main Barriers to AI Adoption by Category",
        xaxis_title="Companies Reporting Barrier (%)",
        height=400,
        showlegend=False,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Main Barriers to AI Adoption by Category",
        description=(
            "A horizontal bar chart showing barriers to AI adoption, color-coded by category and sorted by severity. "
            "Talent shortages and data quality issues are the most frequently cited barriers, followed by technical, "
            "financial, and regulatory challenges. Organizational resistance and unclear ROI are also significant. "
            "The visualization highlights that talent and data remain the most critical obstacles to AI adoption."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Support effectiveness with implementation roadmap
    st.subheader("🎯 Support Measures & Implementation Roadmap")

    # Create implementation timeline
    support_timeline = pd.DataFrame(
        {
            "measure": [
                "Regulatory clarity",
                "Government education investment",
                "Tax incentives",
                "University partnerships",
                "Innovation grants",
                "Technology centers",
                "Public-private collaboration",
            ],
            "effectiveness": [73, 82, 68, 78, 65, 62, 75],
            "implementation_time": [6, 24, 12, 18, 9, 36, 15],  # months
            "cost": [1, 5, 4, 3, 4, 5, 3],  # 1-5 scale
        }
    )

    fig2 = px.scatter(
        support_timeline,
        x="implementation_time",
        y="effectiveness",
        size="cost",
        color="measure",
        title="Support Measures: Effectiveness vs Implementation Time",
        labels={
            "implementation_time": "Implementation Time (months)",
            "effectiveness": "Effectiveness Score (%)",
            "cost": "Relative Cost",
        },
        height=400,
    )

    # Add quadrant dividers
    fig2.add_hline(y=70, line_dash="dash", line_color="gray")
    fig2.add_vline(x=18, line_dash="dash", line_color="gray")

    # Quadrant labels
    fig2.add_annotation(
        x=9, y=75, text="Quick Wins", showarrow=False, font=dict(color="green", size=14)
    )
    fig2.add_annotation(
        x=30, y=75, text="Long-term Strategic", showarrow=False, font=dict(color="blue", size=14)
    )

    fig2.update_traces(textposition="top center")

    fig2 = a11y.make_chart_accessible(
        fig2,
        title="Support Measures: Effectiveness vs Implementation Time",
        description=(
            "A scatter plot analyzing AI adoption support measures by their effectiveness (y-axis, 0-100%) versus implementation time (x-axis, in months). "
            "Bubble sizes represent relative cost (1-5 scale). The chart is divided into quadrants by dashed lines at 70% effectiveness and 18 months. "
            "Quick Wins quadrant (high effectiveness, short time) includes regulatory clarity, innovation grants, and tax incentives. "
            "Long-term Strategic quadrant includes education investment, university partnerships, and technology centers. "
            "The visualization helps organizations prioritize support measures based on their goals and resources."
        ),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Policy recommendations
    col1, col2 = st.columns(2)

    with col1:
        st.write("**🚀 Quick Wins (< 1 year):**")
        st.write("• **Regulatory clarity:** High impact, low cost")
        st.write("• **Innovation grants:** Fast deployment")
        st.write("• **Tax incentives:** Immediate effect")

    with col2:
        st.write("**🎯 Strategic Investments:**")
        st.write("• **Education investment:** Highest effectiveness (82%)")
        st.write("• **University partnerships:** Strong talent pipeline")
        st.write("• **Technology centers:** Infrastructure development")

    st.success(
        """
        **Recommended Approach:** Start with regulatory clarity and tax incentives for immediate impact while building 
        long-term capacity through education and partnerships.
        """
    )
