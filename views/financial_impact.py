"""Financial Impact view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the financial impact view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        financial_impact = data.get("financial_impact", pd.DataFrame())

        # Data presence check
        if financial_impact is None or financial_impact.empty:
            st.error("Financial impact data is unavailable or empty. Please check your data sources or contact support.")
            return

        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("💵 **Financial Impact of AI by Business Function (AI Index Report 2025)**")

        # CORRECTED interpretation box
        st.warning(
            """
        **📊 Understanding the Data:** - The percentages below show the **proportion of companies reporting financial benefits** from AI
        - Among companies that see benefits, the **actual magnitude** is typically:
          - Cost savings: **Less than 10%** (average 5-10%)
          - Revenue gains: **Less than 5%** (average 2-4%)
        - Example: 71% of companies using AI in Marketing report revenue gains, but these gains average only 4%
        """
        )

        # Create visualization with clearer labels
        fig = go.Figure()

        # Sort by revenue gains
        financial_sorted = financial_impact.sort_values(
            "companies_reporting_revenue_gains", ascending=True
        )

        # Add bars showing % of companies reporting benefits
        fig.add_trace(
            go.Bar(
                name="Companies Reporting Cost Savings",
                y=financial_sorted["function"],
                x=financial_sorted["companies_reporting_cost_savings"],
                orientation="h",
                marker_color="#2ECC71",
                text=[f"{x}%" for x in financial_sorted["companies_reporting_cost_savings"]],
                textposition="auto",
                hovertemplate="Function: %{y}<br>Companies reporting savings: %{x}%<br>Avg magnitude: %{customdata}%<extra></extra>",
                customdata=financial_sorted["avg_cost_reduction"],
            )
        )

        fig.add_trace(
            go.Bar(
                name="Companies Reporting Revenue Gains",
                y=financial_sorted["function"],
                x=financial_sorted["companies_reporting_revenue_gains"],
                orientation="h",
                marker_color="#3498DB",
                text=[f"{x}%" for x in financial_sorted["companies_reporting_revenue_gains"]],
                textposition="auto",
                hovertemplate="Function: %{y}<br>Companies reporting gains: %{x}%<br>Avg magnitude: %{customdata}%<extra></extra>",
                customdata=financial_sorted["avg_revenue_increase"],
            )
        )

        fig.update_layout(
            title="Percentage of Companies Reporting Financial Benefits from AI",
            xaxis_title="Percentage of Companies (%)",
            yaxis_title="Business Function",
            barmode="group",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        fig = a11y.make_chart_accessible(
            fig,
            title="Percentage of Companies Reporting Financial Benefits from AI",
            description="Horizontal grouped bar chart showing percentage of companies reporting cost savings and revenue gains from AI by business function. Marketing & Sales leads with 71% reporting revenue gains, while Service Operations shows 49% reporting cost savings. Data shows the proportion of companies seeing benefits, with actual magnitude typically being modest (5-10% cost savings, 2-4% revenue gains).",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Function-specific insights with magnitude clarification
        col1, col2 = st.columns(2)

        with col1:
            st.write("💰 **Top Functions by Adoption Success:**")
            st.write("• **Service Operations:** 49% report cost savings (avg 8% reduction)")
            st.write("• **Marketing & Sales:** 71% report revenue gains (avg 4% increase)")
            st.write("• **Supply Chain:** 43% report cost savings (avg 9% reduction)")

        with col2:
            st.write("📈 **Reality Check:**")
            st.write("• Most benefits are **incremental**, not transformative")
            st.write("• Success varies significantly by implementation quality")
            st.write("• ROI typically takes **12-18 months** to materialize")

        # Add source info
        with st.expander("📊 Data Source & Methodology"):
            st.info(_show_source_info("ai_index"))

    except Exception as e:
        st.error(f"Error rendering financial impact view: {str(e)}")


def _show_source_info(source_key: str) -> str:
    """Show source information for data attribution."""
    sources = {
        "ai_index": {
            "title": "AI Index Report 2025",
            "org": "Stanford HAI",
            "url": "https://aiindex.stanford.edu/ai-index-report-2025/",
            "methodology": "Global survey of 1,000+ organizations across industries",
        },
        "mckinsey": {
            "title": "McKinsey Global Survey on AI",
            "org": "McKinsey & Company",
            "url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai",
            "methodology": "1,491 participants across 101 nations, July 2024",
        },
        "oecd": {
            "title": "OECD/BCG/INSEAD Report 2025",
            "org": "OECD AI Policy Observatory",
            "url": "https://oecd.ai",
            "methodology": "840 enterprises across G7 countries + Brazil",
        },
        "census": {
            "title": "US Census Bureau AI Use Supplement",
            "org": "US Census Bureau",
            "url": "https://www.census.gov",
            "methodology": "850,000 U.S. firms surveyed",
        },
    }

    if source_key in sources:
        source = sources[source_key]
        return f"""
        **Source:** {source['title']}  
        **Organization:** {source['org']}  
        **Methodology:** {source['methodology']}  
        [View Report]({source['url']})
        """
    return ""
