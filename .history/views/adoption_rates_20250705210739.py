"""Adoption Rates view module for AI Adoption Dashboard.

This module provides visualizations for AI adoption rates across business
functions and sectors, with both current (2025) and historical (2018)
perspectives.
"""

from typing import Any, Dict

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render(data: Dict[str, Any]) -> None:
    """Render the Adoption Rates view.

    Args:
        data: Dictionary containing required data:
            - data_year: The selected year filter
            - financial_impact: Financial impact data by function
            - sector_2018: 2018 sector adoption data
            - genai_2025: 2025 GenAI adoption data
            - a11y: Accessibility helper module
            - show_source_info: Function to display source information
    """
    # Extract required data
    data_year = data.get("data_year", "2025")
    financial_impact = data.get("financial_impact")
    sector_2018 = data.get("sector_2018")
    genai_2025 = data.get("genai_2025")
    a11y = data.get("a11y")
    show_source_info = data.get("show_source_info")

    # Data presence checks
    missing = []
    if financial_impact is None or (hasattr(financial_impact, "empty") and financial_impact.empty):
        missing.append("financial_impact")
    if sector_2018 is None or (hasattr(sector_2018, "empty") and sector_2018.empty):
        missing.append("sector_2018")
    if genai_2025 is None or (hasattr(genai_2025, "empty") and genai_2025.empty):
        missing.append("genai_2025")
    if a11y is None:
        missing.append("a11y")
    if show_source_info is None:
        missing.append("show_source_info")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    if "2025" in data_year:
        st.write("📊 **GenAI Adoption by Business Function (2025)**")

        # Enhanced function data with financial impact
        function_data = financial_impact.copy()
        function_data["adoption"] = [42, 23, 7, 22, 28, 23, 13, 15]  # GenAI adoption rates

        # Create comprehensive visualization
        fig = go.Figure()

        # Adoption rate bars
        fig.add_trace(
            go.Bar(
                x=function_data["function"],
                y=function_data["adoption"],
                name="GenAI Adoption Rate",
                marker_color="#3498DB",
                yaxis="y",
                text=[f"{x}%" for x in function_data["adoption"]],
                textposition="outside",
            )
        )

        # Revenue impact line
        fig.add_trace(
            go.Scatter(
                x=function_data["function"],
                y=function_data["companies_reporting_revenue_gains"],
                mode="lines+markers",
                name="% Reporting Revenue Gains",
                line=dict(width=3, color="#2ECC71"),
                marker=dict(size=8),
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="GenAI Adoption and Business Impact by Function",
            xaxis_tickangle=45,
            yaxis=dict(title="GenAI Adoption Rate (%)", side="left"),
            yaxis2=dict(title="% Reporting Revenue Gains", side="right", overlaying="y"),
            height=500,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        fig = a11y.make_chart_accessible(
            fig,
            title="GenAI Adoption and Business Impact by Function",
            description=(
                "A dual-axis chart showing GenAI adoption rates and business impact across eight "
                "business functions. Blue bars represent GenAI adoption rates on the left y-axis, "
                "while a green line shows the percentage of companies reporting revenue gains on "
                "the right y-axis. Marketing & Sales leads with 42% adoption and 71% reporting "
                "revenue gains. Product Development follows with 28% adoption and 52% revenue gains. "
                "Service Operations, Operations, and Customer Service all show 23% adoption with "
                "varying revenue impacts (49%, 51%, and 45% respectively). Supply Chain Management "
                "shows 22% adoption with 48% revenue gains. Risk Management has 15% adoption with "
                "38% revenue gains, while HR has the lowest adoption at 13% with 36% reporting gains. "
                "The chart demonstrates a positive correlation between adoption rates and business "
                "impact, with customer-facing functions showing the highest returns."
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Function insights
        col1, col2 = st.columns(2)

        with col1:
            st.write("🎯 **Top Functions:**")
            st.write("• **Marketing & Sales:** 42% adoption, 71% see revenue gains")
            st.write("• **Product Development:** 28% adoption, 52% see revenue gains")
            st.write("• **Service Operations:** 23% adoption, 49% see cost savings")

        with col2:
            if st.button("📊 View Data Source", key="adoption_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info("mckinsey"))

        # Note about adoption definition
        st.info(
            "**Note:** Adoption rates include any GenAI use (pilots, experiments, production) among firms using AI"
        )

    else:
        # 2018 view
        weighting = st.sidebar.radio("Weighting Method", ["Firm-Weighted", "Employment-Weighted"])
        y_col = "firm_weighted" if weighting == "Firm-Weighted" else "employment_weighted"

        fig = px.bar(
            sector_2018,
            x="sector",
            y=y_col,
            title=f"AI Adoption by Sector (2018) - {weighting}",
            color=y_col,
            color_continuous_scale="blues",
            text=y_col,
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        fig.update_layout(xaxis_tickangle=45, height=500)
        fig = a11y.make_chart_accessible(
            fig,
            title=f"AI Adoption by Sector (2018) - {weighting}",
            description=(
                f"A bar chart showing AI adoption rates across different sectors in 2018 using "
                f"{weighting.lower()} data. The chart uses a blue color gradient where darker colors "
                f"indicate higher adoption rates. Manufacturing and Information sectors lead with 12% "
                f"adoption each, followed by Wholesale (8%), Finance & Insurance (7%), and Retail Trade (6%). "
                f"Lower adoption is seen in sectors like Educational Services (4%), Health Care (4%), and "
                f"Construction (3%). The data represents early AI adoption patterns before the widespread "
                f"deployment of generative AI technologies."
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "🏭 **Key Insight**: Manufacturing and Information sectors led early AI adoption at 12% each"
        )
