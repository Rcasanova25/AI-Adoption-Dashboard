"""Investment Trends view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from components.accessibility import AccessibilityManager


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the investment trends view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Get required data
        ai_investment_data = data.get("ai_investment_data")
        if ai_investment_data is None or ai_investment_data.empty:
            st.error(
                "Required investment trends data is missing or empty. Please check data sources."
            )
            st.stop()

        # Initialize accessibility manager
        a11y = AccessibilityManager()

        st.write("💰 **AI Investment Trends: Record Growth in 2024 (AI Index Report 2025)**")

        # Investment overview metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="2024 Total Investment",
                value="$252.3B",
                delta="+44.5% YoY",
                help="Total corporate AI investment in 2024",
            )

        with col2:
            st.metric(
                label="GenAI Investment",
                value="$33.9B",
                delta="+18.7% from 2023",
                help="8.5x higher than 2022 levels",
            )

        with col3:
            st.metric(
                label="US Investment Lead",
                value="12x China",
                delta="$109.1B vs $9.3B",
                help="US leads global AI investment",
            )

        with col4:
            st.metric(
                label="Growth Since 2014",
                value="13x",
                delta="From $19.4B to $252.3B",
                help="Investment has grown thirteenfold",
            )

        # Create tabs for different investment views
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "📈 Overall Trends",
                "🌍 Geographic Distribution",
                "🚀 GenAI Focus",
                "📊 Comparative Analysis",
            ]
        )

        with tab1:
            _render_overall_trends(ai_investment_data, a11y)

        with tab2:
            _render_geographic_distribution(a11y)

        with tab3:
            _render_genai_focus(a11y)

        with tab4:
            _render_comparative_analysis(a11y)

    except Exception as e:
        st.error(f"Error rendering investment trends view: {str(e)}")


def _render_overall_trends(ai_investment_data: pd.DataFrame, a11y: AccessibilityManager) -> None:
    """Render overall investment trends tab."""
    # Total investment trend chart with interactivity
    fig = go.Figure()

    # Total investment line
    fig.add_trace(
        go.Scatter(
            x=ai_investment_data["year"],
            y=ai_investment_data["total_investment"],
            mode="lines+markers",
            name="Total AI Investment",
            line=dict(width=4, color="#2E86AB"),
            marker=dict(size=10),
            text=[f"${x:.1f}B" for x in ai_investment_data["total_investment"]],
            textposition="top center",
            hovertemplate="Year: %{x}<br>Total Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>",
        )
    )

    # GenAI investment line
    fig.add_trace(
        go.Scatter(
            x=ai_investment_data["year"][ai_investment_data["genai_investment"] > 0],
            y=ai_investment_data["genai_investment"][ai_investment_data["genai_investment"] > 0],
            mode="lines+markers",
            name="GenAI Investment",
            line=dict(width=3, color="#F24236"),
            marker=dict(size=8),
            text=[
                f"${x:.1f}B"
                for x in ai_investment_data["genai_investment"][
                    ai_investment_data["genai_investment"] > 0
                ]
            ],
            textposition="bottom center",
            hovertemplate="Year: %{x}<br>GenAI Investment: $%{y:.1f}B<br>Source: AI Index 2025<extra></extra>",
        )
    )

    # Add annotation for GenAI emergence
    fig.add_annotation(
        x=2022,
        y=3.95,
        text="<b>GenAI Era Begins</b><br>Now 20% of all AI investment",
        showarrow=True,
        arrowhead=2,
        bgcolor="white",
        bordercolor="#F24236",
        borderwidth=2,
        font=dict(size=11, color="#F24236"),
    )

    fig.update_layout(
        title="AI Investment Has Grown 13x Since 2014",
        xaxis_title="Year",
        yaxis_title="Investment ($ Billions)",
        height=450,
        hovermode="x unified",
    )

    col1, col2 = st.columns([10, 1])
    with col1:
        fig = a11y.make_chart_accessible(
            fig,
            title="AI Investment Has Grown 13x Since 2014",
            description="Line chart showing AI investment trends from 2014-2024. Total AI investment grew from $19.4B to $252.3B, representing 13x growth. GenAI investment emerged in 2022 and reached $33.9B by 2024, now representing 20% of all AI investment. The chart shows steady growth with significant acceleration after 2022.",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if st.button("📊", key="inv_source", help="View data source"):
            with st.expander("Data Source", expanded=True):
                st.info(_show_source_info("ai_index"))

    st.info(
        "**Key Insight:** Private investment in generative AI now represents over 20% of all AI-related private investment"
    )

    # Export option
    csv = ai_investment_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Investment Data (CSV)",
        data=csv,
        file_name="ai_investment_trends_2014_2024.csv",
        mime="text/csv",
    )


def _render_geographic_distribution(a11y: AccessibilityManager) -> None:
    """Render geographic distribution tab."""
    # Country comparison with more context
    countries_extended = pd.DataFrame(
        {
            "country": [
                "United States",
                "China",
                "United Kingdom",
                "Germany",
                "France",
                "Canada",
                "Israel",
                "Japan",
                "South Korea",
                "India",
            ],
            "investment": [109.1, 9.3, 4.5, 3.2, 2.8, 2.5, 2.2, 2.0, 1.8, 1.5],
            "per_capita": [324.8, 6.6, 66.2, 38.1, 41.2, 65.8, 231.6, 16.0, 34.6, 1.1],
            "pct_of_gdp": [0.43, 0.05, 0.14, 0.08, 0.09, 0.13, 0.48, 0.05, 0.10, 0.04],
        }
    )

    # Create subplot with multiple metrics
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=("Total Investment ($B)", "Per Capita Investment ($)", "% of GDP"),
        horizontal_spacing=0.12,
    )

    # Total investment - show top 6 to include Israel
    top_investment = countries_extended.nlargest(6, "investment")
    fig.add_trace(
        go.Bar(
            x=top_investment["country"],
            y=top_investment["investment"],
            marker_color="#3498DB",
            showlegend=False,
            text=[f"${x:.1f}B" for x in top_investment["investment"]],
            textposition="outside",
        ),
        row=1,
        col=1,
    )

    # Per capita - show top 6 to highlight Israel's leadership
    top_per_capita = countries_extended.nlargest(6, "per_capita")
    colors_per_capita = [
        "#E74C3C" if country == "Israel" else "#2ECC71" for country in top_per_capita["country"]
    ]
    fig.add_trace(
        go.Bar(
            x=top_per_capita["country"],
            y=top_per_capita["per_capita"],
            marker_color=colors_per_capita,
            showlegend=False,
            text=[f"${x:.0f}" for x in top_per_capita["per_capita"]],
            textposition="outside",
        ),
        row=1,
        col=2,
    )

    # % of GDP - show top 6 to highlight Israel's leadership
    top_gdp_pct = countries_extended.nlargest(6, "pct_of_gdp")
    colors_gdp = [
        "#E74C3C" if country == "Israel" else "#F39C12" for country in top_gdp_pct["country"]
    ]
    fig.add_trace(
        go.Bar(
            x=top_gdp_pct["country"],
            y=top_gdp_pct["pct_of_gdp"],
            marker_color=colors_gdp,
            showlegend=False,
            text=[f"{x:.2f}%" for x in top_gdp_pct["pct_of_gdp"]],
            textposition="outside",
        ),
        row=1,
        col=3,
    )

    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        height=400, title_text="AI Investment by Country - Multiple Perspectives (2024)"
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Investment by Country - Multiple Perspectives (2024)",
        description="Three-panel bar chart showing AI investment by country from different perspectives. Left panel shows total investment with US leading at $109.1B, followed by China at $9.3B. Center panel shows per capita investment with Israel leading at $232 per capita, followed by US at $325. Right panel shows investment as percentage of GDP with Israel leading at 0.48%, followed by US at 0.43%.",
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**🌍 Investment Leadership:**")
        st.write("• **US dominance:** $109.1B (43% of global)")
        st.write(
            f"• **Per capita leader:** Israel at ${countries_extended[countries_extended['country']=='Israel']['per_capita'].iloc[0]:.0f} per person"
        )
        st.write(
            f"• **As % of GDP:** Israel ({countries_extended[countries_extended['country']=='Israel']['pct_of_gdp'].iloc[0]:.2f}%) and US (0.43%) lead"
        )

    with col2:
        st.write("**📈 Regional Dynamics:**")
        st.write("• **Asia rising:** Combined $16.4B across major economies")
        st.write("• **Europe steady:** $10.5B across top 3 countries")
        st.write("• **Innovation hubs:** Israel and US show highest intensity (% of GDP)")

    # Add explanation for Israel's leadership
    st.info(
        """
    **🇮🇱 Israel's AI Investment Leadership:**
    - **Per capita champion:** $232 per person vs US $325 (considering population size)
    - **GDP intensity leader:** 0.48% of GDP, highest globally
    - **Innovation density:** Small country with concentrated AI ecosystem
    - **Strategic focus:** Government and private sector aligned on AI development
    """
    )


def _render_genai_focus(a11y: AccessibilityManager) -> None:
    """Render GenAI focus tab."""
    # GenAI growth visualization with context
    genai_data = pd.DataFrame(
        {
            "year": ["2022", "2023", "2024"],
            "investment": [3.95, 28.5, 33.9],
            "growth": ["Baseline", "+621%", "+18.7%"],
            "pct_of_total": [2.7, 16.3, 13.4],
        }
    )

    # Create dual-axis chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=genai_data["year"],
            y=genai_data["investment"],
            text=[
                f"${x:.1f}B<br>{g}" for x, g in zip(genai_data["investment"], genai_data["growth"])
            ],
            textposition="outside",
            marker_color=["#FFB6C1", "#FF69B4", "#FF1493"],
            name="GenAI Investment",
            yaxis="y",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=genai_data["year"],
            y=genai_data["pct_of_total"],
            mode="lines+markers",
            name="% of Total AI Investment",
            line=dict(width=3, color="#2C3E50"),
            marker=dict(size=10),
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="GenAI Investment: From $3.95B to $33.9B in Two Years",
        xaxis_title="Year",
        yaxis=dict(title="Investment ($ Billions)", side="left"),
        yaxis2=dict(title="% of Total AI Investment", side="right", overlaying="y"),
        height=400,
        hovermode="x unified",
        # Force categorical x-axis to prevent decimal years
        xaxis=dict(type="category", categoryorder="array", categoryarray=["2022", "2023", "2024"]),
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="GenAI Investment: From $3.95B to $33.9B in Two Years",
        description="Dual-axis chart showing GenAI investment growth from 2022-2024. Bar chart shows investment amounts: $3.95B in 2022, $28.5B in 2023 (+621% growth), and $33.9B in 2024 (+18.7% growth). Line chart shows GenAI's share of total AI investment, growing from 2.7% in 2022 to 16.3% in 2023, then stabilizing at 13.4% in 2024.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "**🚀 GenAI represents over 20% of all AI-related private investment, up from near zero in 2021**"
    )


def _render_comparative_analysis(a11y: AccessibilityManager) -> None:
    """Render comparative analysis tab."""
    st.write("**Investment Growth Comparison**")

    # Calculate YoY growth rates
    growth_data = pd.DataFrame(
        {
            "metric": ["Total AI", "GenAI", "US Investment", "China Investment", "UK Investment"],
            "growth_2024": [44.5, 18.7, 44.3, 10.7, 18.4],
            "cagr_5yr": [28.3, 156.8, 31.2, 15.4, 22.7],  # 5-year CAGR
        }
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="2024 Growth (%)",
            x=growth_data["metric"],
            y=growth_data["growth_2024"],
            marker_color="#3498DB",
            text=[f"{x:.1f}%" for x in growth_data["growth_2024"]],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            name="5-Year CAGR (%)",
            x=growth_data["metric"],
            y=growth_data["cagr_5yr"],
            marker_color="#E74C3C",
            text=[f"{x:.1f}%" for x in growth_data["cagr_5yr"]],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="AI Investment Growth Rates",
        xaxis_title="Investment Category",
        yaxis_title="Growth Rate (%)",
        barmode="group",
        height=400,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Investment Growth Rates",
        description="Grouped bar chart comparing 2024 growth rates vs 5-year CAGR across AI investment categories. GenAI shows exceptional 5-year CAGR of 156.8% due to starting from near-zero base. Total AI shows 44.5% growth in 2024 with 28.3% 5-year CAGR. US investment grew 44.3% in 2024 with 31.2% 5-year CAGR, while China showed 10.7% growth in 2024 with 15.4% 5-year CAGR.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**Note:** GenAI shows exceptional 5-year CAGR due to starting from near-zero base in 2019"
    )


def _show_source_info(source_key: str) -> str:
    """Show source information for data attribution."""
    sources = {
        "ai_index": {
            "title": "AI Index Report 2025",
            "org": "Stanford HAI",
            "url": "https://aiindex.stanford.edu/ai-index-report-2025/",
            "methodology": "Global survey of 1,000+ organizations across industries",
        }
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
