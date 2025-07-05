"""AI Cost Trends view for AI Adoption Dashboard."""

from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the AI cost trends view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("💰 **AI Cost Reduction: Dramatic Improvements (AI Index Report 2025)**")

        # Cost reduction visualization with context
        tab1, tab2, tab3 = st.tabs(["Inference Costs", "Hardware Improvements", "Cost Projections"])

        with tab1:
            _render_inference_costs(a11y)

        with tab2:
            _render_hardware_improvements(a11y)

        with tab3:
            _render_cost_projections(a11y)

    except Exception as e:
        st.error(f"Error rendering AI cost trends view: {str(e)}")


def _render_inference_costs(a11y: AccessibilityManager) -> None:
    """Render inference costs tab."""
    # Enhanced cost reduction chart
    fig = go.Figure()

    # Add cost trajectory
    fig.add_trace(
        go.Scatter(
            x=["Nov 2022", "Jan 2023", "Jul 2023", "Jan 2024", "Oct 2024", "Oct 2024\n(Gemini)"],
            y=[20.00, 10.00, 2.00, 0.50, 0.14, 0.07],
            mode="lines+markers",
            marker=dict(
                size=[15, 10, 10, 10, 15, 20],
                color=["red", "orange", "yellow", "lightgreen", "green", "darkgreen"],
            ),
            line=dict(width=3, color="gray", dash="dash"),
            text=["$20.00", "$10.00", "$2.00", "$0.50", "$0.14", "$0.07"],
            textposition="top center",
            name="Cost per Million Tokens",
            hovertemplate="Date: %{x}<br>Cost: %{text}<br>Reduction: %{customdata}<extra></extra>",
            customdata=[
                "Baseline",
                "2x cheaper",
                "10x cheaper",
                "40x cheaper",
                "143x cheaper",
                "286x cheaper",
            ],
        )
    )

    # Add annotations for key milestones
    fig.add_annotation(
        x="Nov 2022",
        y=20,
        text="<b>GPT-3.5 Launch</b><br>$20/M tokens",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
    )

    fig.add_annotation(
        x="Oct 2024\n(Gemini)",
        y=0.07,
        text="<b>286x Cost Reduction</b><br>$0.07/M tokens",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=40,
    )

    fig.update_layout(
        title="AI Inference Cost Collapse: 286x Reduction in 2 Years",
        xaxis_title="Time Period",
        yaxis_title="Cost per Million Tokens ($)",
        yaxis_type="log",
        height=450,
        showlegend=False,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Inference Cost Collapse: 286x Reduction in 2 Years",
        description="Line chart on logarithmic scale showing dramatic AI inference cost reduction from November 2022 to October 2024. Costs dropped from $20.00 per million tokens at GPT-3.5 launch to $0.07 with Gemini, representing a 286x cost reduction. Key milestones marked include 2x reduction by January 2023, 10x by July 2023, 40x by January 2024, and 143x by October 2024.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cost impact analysis
    col1, col2 = st.columns(2)

    with col1:
        st.write("**💡 What This Means:**")
        st.write("• Processing 1B tokens now costs $70 (was $20,000)")
        st.write("• Enables mass deployment of AI applications")
        st.write("• Makes AI accessible to smaller organizations")

    with col2:
        st.write("**📈 Rate of Improvement:**")
        st.write("• Prices falling 9-900x per year by task")
        st.write("• Outpacing Moore's Law significantly")
        st.write("• Driven by competition and efficiency gains")


def _render_hardware_improvements(a11y: AccessibilityManager) -> None:
    """Render hardware improvements tab."""
    # Hardware improvements
    hardware_metrics = pd.DataFrame(
        {
            "metric": ["Performance Growth", "Price/Performance", "Energy Efficiency"],
            "annual_rate": [43, -30, 40],
            "cumulative_5yr": [680, -83, 538],
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Annual Rate (%)",
            x=hardware_metrics["metric"],
            y=hardware_metrics["annual_rate"],
            marker_color=[
                "#2ECC71" if x > 0 else "#E74C3C" for x in hardware_metrics["annual_rate"]
            ],
            text=[f"{x:+d}%" for x in hardware_metrics["annual_rate"]],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="ML Hardware Annual Improvement Rates",
        xaxis_title="Metric",
        yaxis_title="Annual Change (%)",
        height=400,
        showlegend=False,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="ML Hardware Annual Improvement Rates",
        description="Bar chart showing annual improvement rates for ML hardware metrics. Performance Growth shows +43% annual improvement in green, Energy Efficiency shows +40% annual improvement in green, while Price/Performance shows -30% annual change (cost reduction) displayed in red to indicate decreasing costs.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        """
    **🚀 Hardware Revolution:**
    - Performance improving **43% annually** (16-bit operations)
    - Cost dropping **30% per year** for same performance
    - Energy efficiency gaining **40% annually**
    - Enabling larger models at lower costs
    """
    )


def _render_cost_projections(a11y: AccessibilityManager) -> None:
    """Render cost projections tab."""
    st.write("**Future Cost Projections**")

    # Create projection data
    years = list(range(2024, 2028))
    conservative = [0.07, 0.035, 0.018, 0.009]
    aggressive = [0.07, 0.014, 0.003, 0.0006]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=conservative,
            mode="lines+markers",
            name="Conservative (50% annual reduction)",
            line=dict(width=3, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(52, 152, 219, 0.1)",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=years,
            y=aggressive,
            mode="lines+markers",
            name="Aggressive (80% annual reduction)",
            line=dict(width=3),
            fill="tozeroy",
            fillcolor="rgba(231, 76, 60, 0.1)",
        )
    )

    fig.update_layout(
        title="AI Cost Projections: 2024-2027",
        xaxis_title="Year",
        yaxis_title="Cost per Million Tokens ($)",
        yaxis_type="log",
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Cost Projections: 2024-2027",
        description="Line chart with logarithmic scale showing AI cost projections from 2024-2027. Two scenarios plotted: Conservative scenario assumes 50% annual cost reduction, dropping from $0.07 in 2024 to $0.009 in 2027. Aggressive scenario assumes 80% annual reduction, reaching $0.0006 by 2027. Both scenarios use filled areas to show the range of possible outcomes.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
    **📊 Projection Assumptions:**
    - **Conservative:** Based on historical semiconductor improvements
    - **Aggressive:** Based on current AI-specific optimization rates
    - By 2027, costs could be 1000-10,000x lower than 2022
    """
    )
