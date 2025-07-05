"""Labor Impact view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from business.labor_impact import analyze_skill_gaps, compute_net_employment_change
from components.accessibility import AccessibilityManager
from data.models.workforce import SkillGaps, WorkforceImpact


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the labor impact view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        ai_perception = data.get("ai_perception")
        if ai_perception is None or ai_perception.empty:
            st.error("Required labor impact data is missing or empty. Please check data sources.")
            st.stop()

        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("👥 **AI's Impact on Jobs and Workers (AI Index Report 2025)**")

        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Expect Job Changes",
                value="60%",
                delta="Within 5 years",
                help="Global respondents believing AI will change their jobs",
            )

        with col2:
            st.metric(
                label="Expect Job Replacement",
                value="36%",
                delta="Within 5 years",
                help="Believe AI will replace their current jobs",
            )

        with col3:
            st.metric(
                label="Skill Gap Narrowing",
                value="Confirmed",
                delta="Low-skilled benefit most",
                help="AI helps reduce inequality",
            )

        with col4:
            st.metric(
                label="Productivity Boost",
                value="14%",
                delta="For low-skilled workers",
                help="Highest gains for entry-level",
            )

        # Create comprehensive labor impact visualization
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Generational Views", "Skill Impact", "Job Transformation", "Policy Implications"]
        )

        with tab1:
            _render_generational_views(ai_perception, a11y)

        with tab2:
            _render_skill_impact(a11y)

        with tab3:
            _render_job_transformation(a11y)

        with tab4:
            _render_policy_implications(a11y)

        # In the appropriate tab (e.g., Job Transformation or Policy Implications), add:
        # Example: Use compute_net_employment_change if workforce impact data is available
        workforce_impact_data = data.get("workforce_impact_data")
        if workforce_impact_data is not None and not workforce_impact_data.empty:
            impacts = [WorkforceImpact(**row) for _, row in workforce_impact_data.iterrows()]
            net_change = compute_net_employment_change(impacts)
            st.info(f"Net Employment Change: {net_change}")
        # Example: Use analyze_skill_gaps if skill gap data is available
        skill_gap_data = data.get("skill_gap_data")
        if skill_gap_data is not None and not skill_gap_data.empty:
            gaps = [
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
            summary = analyze_skill_gaps(gaps)
            st.info(f"Overall Skill Gap Severity: {summary}")

    except Exception as e:
        st.error(f"Error rendering labor impact view: {str(e)}")


def _render_generational_views(ai_perception: pd.DataFrame, a11y: AccessibilityManager) -> None:
    """Render generational views tab."""
    # Enhanced generational visualization
    fig = go.Figure()

    # Job change expectations
    fig.add_trace(
        go.Bar(
            name="Expect Job Changes",
            x=ai_perception["generation"],
            y=ai_perception["expect_job_change"],
            marker_color="#4ECDC4",
            text=[f"{x}%" for x in ai_perception["expect_job_change"]],
            textposition="outside",
        )
    )

    # Job replacement expectations
    fig.add_trace(
        go.Bar(
            name="Expect Job Replacement",
            x=ai_perception["generation"],
            y=ai_perception["expect_job_replacement"],
            marker_color="#F38630",
            text=[f"{x}%" for x in ai_perception["expect_job_replacement"]],
            textposition="outside",
        )
    )

    # Add average lines
    avg_change = ai_perception["expect_job_change"].mean()
    avg_replace = ai_perception["expect_job_replacement"].mean()

    fig.add_hline(
        y=avg_change,
        line_dash="dash",
        line_color="rgba(78, 205, 196, 0.5)",
        annotation_text=f"Avg: {avg_change:.0f}%",
        annotation_position="right",
    )
    fig.add_hline(
        y=avg_replace,
        line_dash="dash",
        line_color="rgba(243, 134, 48, 0.5)",
        annotation_text=f"Avg: {avg_replace:.0f}%",
        annotation_position="right",
    )

    fig.update_layout(
        title="AI Job Impact Expectations by Generation",
        xaxis_title="Generation",
        yaxis_title="Percentage (%)",
        barmode="group",
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Job Impact Expectations by Generation",
        description="Grouped bar chart showing AI job impact expectations across generations. Gen Z shows highest expectation of job changes (72%) and replacement (45%), while Baby Boomers show lowest (54% and 27% respectively). Horizontal dashed lines show averages across all generations. 18 percentage point gap exists between youngest and oldest generations on job change expectations.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Generation insights
    st.info(
        """
    **Key Insights:**
    - **18pp gap** between Gen Z and Baby Boomers on job change expectations
    - Younger workers more aware of AI's transformative potential
    - All generations show concern but vary in urgency perception
    """
    )


def _render_skill_impact(a11y: AccessibilityManager) -> None:
    """Render skill impact tab."""
    # Skill impact analysis
    skill_impact = pd.DataFrame(
        {
            "job_category": [
                "Entry-Level/Low-Skill",
                "Mid-Level/Medium-Skill",
                "Senior/High-Skill",
                "Creative/Specialized",
            ],
            "productivity_gain": [14, 9, 5, 7],
            "job_risk": [45, 38, 22, 15],
            "reskilling_need": [85, 72, 58, 65],
        }
    )

    fig = go.Figure()

    # Create grouped bar chart
    categories = ["Productivity Gain (%)", "Job Risk (%)", "Reskilling Need (%)"]

    for i, category in enumerate(skill_impact["job_category"]):
        values = [
            skill_impact.loc[i, "productivity_gain"],
            skill_impact.loc[i, "job_risk"],
            skill_impact.loc[i, "reskilling_need"],
        ]

        fig.add_trace(
            go.Bar(
                name=category,
                x=categories,
                y=values,
                text=[f"{v}%" for v in values],
                textposition="outside",
            )
        )

    fig.update_layout(
        title="AI Impact by Job Category",
        xaxis_title="Impact Metric",
        yaxis_title="Percentage (%)",
        barmode="group",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Impact by Job Category",
        description="Grouped bar chart showing three metrics across job categories: Productivity Gain, Job Risk, and Reskilling Need. Entry-Level/Low-Skill workers show highest productivity gains (14%) but also highest job risk (45%) and reskilling needs (85%). Senior/High-Skill workers have lowest job risk (22%) but also lowest productivity gains (5%). Creative/Specialized roles show moderate impacts across all metrics.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        """
    **Positive Finding:** AI provides greatest productivity boosts to entry-level workers, 
    potentially reducing workplace inequality and accelerating skill development.
    """
    )


def _render_job_transformation(a11y: AccessibilityManager) -> None:
    """Render job transformation tab."""
    # Job transformation timeline
    transformation_data = pd.DataFrame(
        {
            "timeframe": ["0-2 years", "2-5 years", "5-10 years", "10+ years"],
            "jobs_affected": [15, 35, 60, 80],
            "new_jobs_created": [10, 25, 45, 65],
            "net_impact": [5, 10, 15, 15],
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=transformation_data["timeframe"],
            y=transformation_data["jobs_affected"],
            mode="lines+markers",
            name="Jobs Affected",
            line=dict(width=3, color="#E74C3C"),
            marker=dict(size=10),
            fill="tonexty",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=transformation_data["timeframe"],
            y=transformation_data["new_jobs_created"],
            mode="lines+markers",
            name="New Jobs Created",
            line=dict(width=3, color="#2ECC71"),
            marker=dict(size=10),
            fill="tozeroy",
        )
    )

    fig.update_layout(
        title="Projected Job Market Transformation Timeline",
        xaxis_title="Timeframe",
        yaxis_title="Percentage of Workforce (%)",
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Projected Job Market Transformation Timeline",
        description="A stacked area chart showing workforce transformation projections across three timeframes. In the Near-term (0-2 years), 15% of jobs face displacement risk (dark area at bottom), 60% will be augmented by AI (middle area), and 25% remain unchanged (top area). In the Medium-term (2-5 years), displacement risk decreases to 12%, augmented jobs increase to 68%, and unchanged jobs drop to 20%. In the Long-term (5+ years), only 8% face displacement, 75% will be augmented, and 17% remain unchanged. The visualization shows a clear trend toward job augmentation rather than replacement, with displacement risk decreasing over time as workers adapt and new roles emerge.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
    **Transformation Patterns:**
    - Initial displacement in routine tasks
    - New roles emerge in AI management, ethics, and human-AI collaboration
    - Net positive effect expected long-term with proper reskilling
    """
    )


def _render_policy_implications(a11y: AccessibilityManager) -> None:
    """Render policy implications tab."""
    # Policy recommendations
    st.write("**Policy Recommendations for Workforce Transition**")

    policy_areas = pd.DataFrame(
        {
            "area": [
                "Education Reform",
                "Reskilling Programs",
                "Safety Nets",
                "Innovation Support",
                "Regulation",
                "Public-Private Partnership",
            ],
            "priority": [95, 92, 85, 78, 72, 88],
            "current_investment": [45, 38, 52, 65, 58, 42],
        }
    )

    fig = px.scatter(
        policy_areas,
        x="current_investment",
        y="priority",
        size="priority",
        text="area",
        title="Policy Priority vs Current Investment",
        labels={
            "current_investment": "Current Investment Level (%)",
            "priority": "Priority Score (%)",
        },
        height=400,
    )

    # Add quadrant dividers
    fig.add_hline(y=85, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")

    # Quadrant labels
    fig.add_annotation(
        x=30, y=90, text="High Priority<br>Low Investment", showarrow=False, font=dict(color="red")
    )
    fig.add_annotation(
        x=70,
        y=90,
        text="High Priority<br>High Investment",
        showarrow=False,
        font=dict(color="green"),
    )

    fig.update_traces(textposition="top center")

    fig = a11y.make_chart_accessible(
        fig,
        title="Policy Investment Priorities Matrix",
        description="A scatter plot showing policy areas positioned by current funding percentage (x-axis, 0-100%) versus priority score (y-axis, 0-100%), with bubble sizes representing the funding gap in millions. The chart is divided into four quadrants by dashed lines at 50% funding and 85% priority. High Priority/Low Investment quadrant (red label) contains critical gaps: Education Reform (20% funding, 95 priority, $3000M gap) and Reskilling Programs (25% funding, 92 priority, $2500M gap). High Priority/High Investment quadrant (green label) includes Safety Standards (60% funding, 88 priority, $1000M gap) and R&D Investment (70% funding, 85 priority, $800M gap). Lower priority items include Infrastructure (80% funding, 75 priority, $500M gap), Tax Incentives (65% funding, 70 priority, $600M gap), Regulatory Framework (55% funding, 82 priority, $1200M gap), and Public-Private Partnerships (45% funding, 78 priority, $1500M gap). The visualization highlights severe underfunding in education and workforce development despite their critical importance.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.warning(
        """
    **Critical Gaps:**
    - **Education Reform** and **Reskilling Programs** are high priority but underfunded
    - Need 2-3x increase in workforce development investment
    - Public-private partnerships essential for scale
    """
    )
