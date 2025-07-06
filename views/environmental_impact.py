"""Environmental Impact view module for AI Adoption Dashboard.

This module provides visualizations and analysis of the environmental impact of AI,
including carbon emissions, energy trends, mitigation strategies, and sustainability metrics.
"""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the Environmental Impact view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        training_emissions = data.get("training_emissions")
        if training_emissions is None or training_emissions.empty:
            st.error(
                "Required environmental impact data is missing or empty. Please check data sources."
            )
            st.stop()

        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("🌱 **Environmental Impact: AI's Growing Carbon Footprint (AI Index Report 2025)**")

        # Create comprehensive environmental dashboard
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Training Emissions",
                "Energy Trends",
                "Mitigation Strategies",
                "Sustainability Metrics",
            ]
        )

        with tab1:
            _render_training_emissions(training_emissions, a11y)

        with tab2:
            _render_energy_trends(a11y)

        with tab3:
            _render_mitigation_strategies(a11y)

        with tab4:
            _render_sustainability_metrics(a11y)

    except Exception as e:
        st.error(f"Error rendering environmental impact view: {str(e)}")

    if not data or "environmental_impact" not in data:
        raise ValueError("Missing required real, validated data for environmental impact.")


def _render_training_emissions(
    training_emissions: pd.DataFrame, a11y: AccessibilityManager
) -> None:
    """Render training emissions tab."""
    fig = go.Figure()

    # Add bars for emissions
    fig.add_trace(
        go.Bar(
            x=training_emissions["model"],
            y=training_emissions["carbon_tons"],
            marker_color=["#90EE90", "#FFD700", "#FF6347", "#8B0000"],
            text=[f"{x:,.0f} tons" for x in training_emissions["carbon_tons"]],
            textposition="outside",
            hovertemplate="Model: %{x}<br>Emissions: %{text}<br>Equivalent: %{customdata}<extra></extra>",
            customdata=["Negligible", "~125 cars/year", "~1,100 cars/year", "~1,900 cars/year"],
        )
    )

    # Add trend line
    fig.add_trace(
        go.Scatter(
            x=training_emissions["model"],
            y=training_emissions["carbon_tons"],
            mode="lines",
            line=dict(width=3, color="red", dash="dash"),
            name="Exponential Growth Trend",
            showlegend=True,
        )
    )

    fig.update_layout(
        title="Carbon Emissions from AI Model Training: Exponential Growth",
        xaxis_title="AI Model",
        yaxis_title="Carbon Emissions (tons CO₂)",
        yaxis_type="log",
        height=450,
        showlegend=True,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Carbon Emissions from AI Model Training: Exponential Growth",
        description=(
            "A combination bar and line chart showing the exponential growth in carbon emissions from AI model training. "
            "The x-axis shows four AI models: BERT (2019), GPT-3 (2020), GPT-4 (2023), and Llama 3.1 (2024). "
            "The y-axis uses a logarithmic scale to show carbon emissions in tons of CO₂. "
            "BERT shows negligible emissions, GPT-3 produces 552 tons (equivalent to 125 cars per year), "
            "GPT-4 generates 4,850 tons (equivalent to 1,100 cars per year), and Llama 3.1 produces 8,930 tons "
            "(equivalent to 1,900 cars per year). A red dashed trend line illustrates the exponential growth pattern, "
            "showing a 900,000x increase from 2012 to 2024, with emissions roughly doubling every 2 years."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Emissions context
    col1, col2 = st.columns(2)

    with col1:
        st.write("**📈 Growth Rate:**")
        st.write("• 900,000x increase from 2012 to 2024")
        st.write("• Doubling approximately every 2 years")
        st.write("• Driven by model size and compute needs")

    with col2:
        st.write("**🌍 Context:**")
        st.write("• Llama 3.1 = Annual emissions of 1,900 cars")
        st.write("• One training run = 8,930 tons CO₂")
        st.write("• Excludes inference and retraining")


def _render_energy_trends(a11y: AccessibilityManager) -> None:
    """Render energy trends tab."""
    st.write("**⚡ Energy Consumption and Nuclear Renaissance**")

    # TODO: Load energy_data from actual data source
    energy_data = pd.DataFrame()

    fig = go.Figure()

    # Energy consumption
    fig.add_trace(
        go.Bar(
            x=energy_data["year"],
            y=energy_data["ai_energy_twh"],
            name="AI Energy Use (TWh)",
            marker_color="#3498DB",
            yaxis="y",
            text=[f"{x:.1f} TWh" for x in energy_data["ai_energy_twh"]],
            textposition="outside",
        )
    )

    # Nuclear deals
    fig.add_trace(
        go.Scatter(
            x=energy_data["year"],
            y=energy_data["nuclear_deals"],
            name="Nuclear Energy Deals",
            mode="lines+markers",
            line=dict(width=3, color="#2ECC71"),
            marker=dict(size=10),
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="AI Energy Consumption Driving Nuclear Energy Revival",
        xaxis_title="Year",
        yaxis=dict(title="Energy Consumption (TWh)", side="left"),
        yaxis2=dict(title="Nuclear Deals (#)", side="right", overlaying="y"),
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Energy Consumption Driving Nuclear Energy Revival",
        description=(
            "A dual-axis chart showing the relationship between AI energy consumption and nuclear energy deals from 2020 to 2025. "
            "The left y-axis displays AI energy use in terawatt hours (TWh) as blue bars, growing from 2.1 TWh in 2020 to 27.3 TWh in 2025. "
            "The right y-axis shows the number of nuclear energy deals as a green line with markers, increasing from 0 deals in 2020-2021 to 15 deals in 2025. "
            "The chart demonstrates how rapidly increasing AI energy demands are driving a revival in nuclear energy investments, "
            "with major tech companies like Microsoft, Google, Amazon, and Meta securing nuclear power agreements."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
        **🔋 Major Nuclear Agreements (2024-2025):**
        - Microsoft: Three Mile Island restart
        - Google: Kairos Power SMR partnership
        - Amazon: X-energy SMR development
        - Meta: Nuclear power exploration
        """
    )


def _render_mitigation_strategies(a11y: AccessibilityManager) -> None:
    """Render mitigation strategies tab."""
    # TODO: Load mitigation data from actual data source
    mitigation = pd.DataFrame()

    fig = px.scatter(
        mitigation,
        x="adoption_rate",
        y="potential_reduction",
        size="timeframe",
        color="strategy",
        title="AI Sustainability Strategies: Impact vs Adoption",
        labels={
            "adoption_rate": "Current Adoption Rate (%)",
            "potential_reduction": "Potential Emission Reduction (%)",
            "timeframe": "Implementation Time (years)",
        },
        height=400,
    )

    # Add target zone
    fig.add_shape(
        type="rect", x0=70, x1=100, y0=70, y1=100, fillcolor="lightgreen", opacity=0.2, line_width=0
    )
    fig.add_annotation(x=85, y=85, text="Target Zone", showarrow=False, font=dict(color="green"))

    fig.update_traces(textposition="top center")

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Sustainability Strategies: Impact vs Adoption",
        description=(
            "A scatter plot analyzing AI sustainability strategies by their potential emission reduction (y-axis, 0-100%) versus current adoption rate (x-axis, 0-100%). "
            "Point sizes represent implementation timeframe in years. Six strategies are shown: Model Reuse (95% reduction potential, 35% adoption, 1 year), "
            "Renewable Energy (85% reduction, 45% adoption, 3 years), Carbon Offsets (100% reduction, 30% adoption, 1 year), "
            "Edge Computing (60% reduction, 25% adoption, 2 years), Efficient Architectures (40% reduction, 65% adoption, 1 year), "
            "and Quantum Computing (90% reduction, 5% adoption, 7 years). A green 'Target Zone' is highlighted in the upper right (70-100% adoption, 70-100% reduction), "
            "representing the ideal high-impact, high-adoption area. Most strategies fall outside this zone, indicating significant opportunity for improvement."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        """
        **Most Promising Strategies:**
        - **Model Reuse:** 95% reduction potential, needs ecosystem development
        - **Renewable Energy:** 85% reduction, requires infrastructure investment
        - **Efficient Architectures:** Quick wins with 40% reduction potential
        """
    )


def _render_sustainability_metrics(a11y: AccessibilityManager) -> None:
    """Render sustainability metrics tab."""
    st.write("**Sustainability Performance Metrics**")

    # TODO: Load metrics data from actual data source
    metrics = pd.DataFrame()

    fig = go.Figure()

    categories = ["Renewable %", "Efficiency", "Transparency"]

    for _, company in metrics.iterrows():
        values = [
            company["renewable_pct"] / 10,  # Scale to 10
            company["efficiency_score"],
            company["transparency_score"],
        ]
        fig.add_trace(
            go.Scatterpolar(r=values, theta=categories, fill="toself", name=company["company"])
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title="AI Company Sustainability Scores",
        height=400,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Company Sustainability Scores",
        description=(
            "A radar chart comparing sustainability performance across five major AI companies: OpenAI, Google, Microsoft, Meta, and Amazon. "
            "Three metrics are displayed on a 0-10 scale: Renewable Energy Percentage (scaled), Efficiency Score, and Transparency Score. "
            "Google leads with the highest scores across all metrics (7.8 renewable, 8.5 efficiency, 8.2 transparency). "
            "Microsoft follows closely (6.5 renewable, 7.8 efficiency, 7.9 transparency). Amazon shows strength in efficiency (7.5) but lags in renewable energy (4.0). "
            "Meta and OpenAI show lower transparency scores (6.2 and 6.5 respectively). The overlapping polygons reveal that while companies are making progress, "
            "significant improvements are needed across all dimensions to achieve sustainability goals."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
        **Industry Trends:**
        - Increasing pressure for carbon neutrality
        - Hardware efficiency improving 40% annually
        - Growing focus on lifecycle emissions
        """
    )
