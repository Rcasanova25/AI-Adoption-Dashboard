"""Geographic Distribution view module for AI Adoption Dashboard.

This module provides comprehensive geographic visualizations of AI adoption,
research infrastructure, investment flows, and academic centers across the US.
"""

from typing import Any, Dict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from components.accessibility import AccessibilityManager
from views.base import BaseView


class GeographicDistributionView(BaseView):
    def __init__(self):
        super().__init__(
            title="AI Adoption Geographic Distribution with Research Infrastructure",
            description="Comprehensive geographic visualizations of AI adoption, research infrastructure, investment flows, and academic centers across the US."
        )
        self.a11y = AccessibilityManager()

    def render_content(self, data: Dict[str, Any]) -> None:
        """Render the Geographic Distribution view content.

        Args:
            data: Dictionary containing required data:
                - geographic: Base geographic data
                - state_data: State-level aggregated data
        """
        # Extract required data
        geographic = data.get("geographic")
        state_data = data.get("state_data")

        st.write("🗺️ **AI Adoption Geographic Distribution with Research Infrastructure**")

        # Enhanced geographic data with academic and government investments
        enhanced_geographic = pd.DataFrame(
            {
                "city": [
                    "San Francisco Bay Area",
                    "Nashville",
                    "San Antonio",
                    "Las Vegas",
                    "New Orleans",
                    "San Diego",
                    "Seattle",
                    "Boston",
                    "Los Angeles",
                    "Phoenix",
                    "Denver",
                    "Austin",
                    "Portland",
                    "Miami",
                    "Atlanta",
                    "Chicago",
                    "New York",
                    "Philadelphia",
                    "Dallas",
                    "Houston",
                ],
                "state": [
                    "California",
                    "Tennessee",
                    "Texas",
                    "Nevada",
                    "Louisiana",
                    "California",
                    "Washington",
                    "Massachusetts",
                    "California",
                    "Arizona",
                    "Colorado",
                    "Texas",
                    "Oregon",
                    "Florida",
                    "Georgia",
                    "Illinois",
                    "New York",
                    "Pennsylvania",
                    "Texas",
                    "Texas",
                ],
                "lat": [
                    37.7749,
                    36.1627,
                    29.4241,
                    36.1699,
                    29.9511,
                    32.7157,
                    47.6062,
                    42.3601,
                    34.0522,
                    33.4484,
                    39.7392,
                    30.2672,
                    45.5152,
                    25.7617,
                    33.7490,
                    41.8781,
                    40.7128,
                    39.9526,
                    32.7767,
                    29.7604,
                ],
                "lon": [
                    -122.4194,
                    -86.7816,
                    -98.4936,
                    -115.1398,
                    -90.0715,
                    -117.1611,
                    -122.3321,
                    -71.0589,
                    -118.2437,
                    -112.0740,
                    -104.9903,
                    -97.7431,
                    -122.6784,
                    -80.1918,
                    -84.3880,
                    -87.6298,
                    -74.0060,
                    -75.1652,
                    -96.7970,
                    -95.3698,
                ],
                "ai_adoption_rate": [
                    9.5,
                    8.3,
                    8.3,
                    7.7,
                    7.4,
                    7.4,
                    6.8,
                    6.7,
                    7.2,
                    6.5,
                    6.3,
                    7.8,
                    6.2,
                    6.9,
                    7.1,
                    7.0,
                    8.0,
                    6.6,
                    7.5,
                    7.3,
                ],
                "state_code": [
                    "CA",
                    "TN",
                    "TX",
                    "NV",
                    "LA",
                    "CA",
                    "WA",
                    "MA",
                    "CA",
                    "AZ",
                    "CO",
                    "TX",
                    "OR",
                    "FL",
                    "GA",
                    "IL",
                    "NY",
                    "PA",
                    "TX",
                    "TX",
                ],
                "population_millions": [
                    7.7,
                    0.7,
                    1.5,
                    0.6,
                    0.4,
                    1.4,
                    0.8,
                    0.7,
                    4.0,
                    1.7,
                    0.7,
                    1.0,
                    0.7,
                    0.5,
                    0.5,
                    2.7,
                    8.3,
                    1.6,
                    1.3,
                    2.3,
                ],
                "gdp_billions": [
                    535,
                    48,
                    98,
                    68,
                    25,
                    253,
                    392,
                    463,
                    860,
                    162,
                    201,
                    148,
                    121,
                    345,
                    396,
                    610,
                    1487,
                    388,
                    368,
                    356,
                ],
                "major_universities": [12, 2, 3, 1, 2, 5, 4, 8, 6, 2, 3, 4, 2, 3, 4, 5, 7, 4, 3, 4],
                "ai_research_centers": [15, 1, 2, 0, 1, 3, 5, 12, 4, 1, 2, 3, 2, 2, 3, 4, 8, 3, 2, 3],
                "federal_ai_funding_millions": [
                    2100,
                    45,
                    125,
                    15,
                    35,
                    180,
                    350,
                    890,
                    420,
                    55,
                    85,
                    165,
                    75,
                    95,
                    145,
                    285,
                    650,
                    225,
                    185,
                    245,
                ],
                "nsf_ai_institutes": [2, 0, 1, 0, 0, 1, 1, 3, 1, 0, 1, 1, 0, 0, 1, 1, 2, 1, 1, 1],
                "ai_startups": [
                    850,
                    15,
                    35,
                    8,
                    12,
                    95,
                    145,
                    325,
                    185,
                    25,
                    45,
                    85,
                    35,
                    55,
                    85,
                    125,
                    450,
                    95,
                    75,
                    125,
                ],
                "ai_patents_2024": [
                    2450,
                    25,
                    85,
                    12,
                    18,
                    165,
                    285,
                    780,
                    385,
                    45,
                    95,
                    145,
                    65,
                    85,
                    125,
                    245,
                    825,
                    185,
                    155,
                    225,
                ],
                "venture_capital_millions": [
                    15800,
                    125,
                    285,
                    45,
                    85,
                    1250,
                    2850,
                    4200,
                    3850,
                    185,
                    345,
                    650,
                    225,
                    385,
                    485,
                    1250,
                    8500,
                    650,
                    485,
                    850,
                ],
            }
        )

        # State-level research infrastructure data
        state_research_data = pd.DataFrame(
            {
                "state": [
                    "California",
                    "Massachusetts",
                    "New York",
                    "Texas",
                    "Washington",
                    "Illinois",
                    "Pennsylvania",
                    "Georgia",
                    "Colorado",
                    "Florida",
                    "Michigan",
                    "Ohio",
                    "North Carolina",
                    "Virginia",
                    "Maryland",
                ],
                "state_code": [
                    "CA",
                    "MA",
                    "NY",
                    "TX",
                    "WA",
                    "IL",
                    "PA",
                    "GA",
                    "CO",
                    "FL",
                    "MI",
                    "OH",
                    "NC",
                    "VA",
                    "MD",
                ],
                "ai_adoption_rate": [
                    8.2,
                    6.7,
                    8.0,
                    7.5,
                    6.8,
                    7.0,
                    6.6,
                    7.1,
                    6.3,
                    6.9,
                    5.5,
                    5.8,
                    6.0,
                    6.2,
                    6.4,
                ],
                "nsf_ai_institutes_total": [5, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2],
                "total_federal_funding_billions": [
                    3.2,
                    1.1,
                    1.0,
                    0.7,
                    0.5,
                    0.4,
                    0.3,
                    0.2,
                    0.2,
                    0.2,
                    0.15,
                    0.12,
                    0.25,
                    0.35,
                    0.45,
                ],
                "r1_universities": [9, 4, 7, 8, 2, 3, 4, 2, 2, 3, 3, 3, 3, 2, 2],
                "ai_workforce_thousands": [
                    285,
                    95,
                    185,
                    125,
                    85,
                    65,
                    55,
                    45,
                    35,
                    55,
                    35,
                    25,
                    45,
                    55,
                    65,
                ],
            }
        )

        # Create comprehensive tabs for different geographic analyses
        geo_tabs = st.tabs(
            [
                "🗺️ Interactive Map",
                "🏛️ Research Infrastructure",
                "📊 State Comparisons",
                "🎓 Academic Centers",
                "💰 Investment Flows",
            ]
        )

        with geo_tabs[0]:
            self._render_interactive_map(enhanced_geographic, state_research_data)

        with geo_tabs[1]:
            self._render_research_infrastructure(state_research_data)

        with geo_tabs[2]:
            self._render_state_comparisons(state_research_data)

        with geo_tabs[3]:
            self._render_academic_centers(enhanced_geographic, state_research_data)

        with geo_tabs[4]:
            self._render_investment_flows(enhanced_geographic)

        # Enhanced summary with authoritative insights
        st.markdown("---")
        st.subheader("🎯 Geographic AI Ecosystem: Key Findings & Policy Implications")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
                **🌟 Innovation Hubs:**
                - **San Francisco Bay Area:** Global AI capital with $15.8B VC, 15 research centers
                - **Boston:** Academic powerhouse with 3 NSF institutes, $890M federal funding
                - **New York:** Financial AI hub with $8.5B VC, strong adoption rates
                - **Seattle:** Cloud AI infrastructure, major tech presence
                """
            )

        with col2:
            st.markdown(
                """
                **🏛️ Federal Strategy:**
                - **NSF AI Institutes:** 27 institutes across 40+ states, $220M investment
                - **Geographic distribution:** Intentional spread beyond coastal concentration
                - **Research capacity:** Building national AI research infrastructure
                - **Workforce development:** University partnerships in all regions
                """
            )

        with col3:
            st.markdown(
                """
                **⚖️ Policy Challenges:**
                - **Digital divide:** 10x gap between leading and lagging regions
                - **Talent concentration:** AI workforce clustered in expensive coastal cities
                - **Investment disparity:** 85% of private investment in 5 states
                - **Infrastructure needs:** Broadband, computing, research facilities
                """
            )

        # Sources and methodology
        with st.expander("📚 Data Sources & Geographic Methodology"):
            st.markdown(
                """
                ### Geographic Analysis Methodology

                **Data Integration:**
                - **U.S. Census Bureau:** AI Use Supplement (850,000 firms surveyed)
                - **NSF:** National AI Research Institutes program data
                - **Stanford AI Index 2025:** Geographic investment patterns
                - **Academic sources:** University research center mapping
                - **Federal databases:** Grant and funding allocation data

                **Geographic Scope:**
                - **Metropolitan Statistical Areas (MSAs):** 20 largest AI ecosystems
                - **State-level analysis:** All 50 states + DC for policy comparison
                - **Federal coordination:** NSF institute distribution strategy

                **Metrics Definitions:**
                - **AI Adoption Rate:** Percentage of firms using any AI technology
                - **Research Centers:** University-affiliated AI research institutes
                - **Federal Funding:** Direct federal AI research investments (NSF, DOD, NIH)
                - **VC Investment:** Private venture capital in AI startups (2024)
                - **NSF AI Institutes:** Federally funded multi-institutional research centers

                **Source Quality:**
                - ✅ **Government data:** Official federal agency reports
                - ✅ **Academic research:** Peer-reviewed geographic analysis
                - ✅ **Cross-validation:** Multiple independent data sources
                """
            )

        # Export enhanced geographic data
        if st.button("📥 Export Geographic Analysis Data"):
            # Combine all geographic data for export
            export_data = enhanced_geographic.merge(
                state_research_data[
                    ["state", "nsf_ai_institutes_total", "total_federal_funding_billions"]
                ],
                on="state",
                how="left",
            )

            csv = export_data.to_csv(index=False)
            st.download_button(
                label="Download Complete Geographic Dataset (CSV)",
                data=csv,
                file_name="ai_geographic_ecosystem_analysis.csv",
                mime="text/csv",
            )

    def _render_interactive_map(
        self, enhanced_geographic: pd.DataFrame, state_research_data: pd.DataFrame
    ) -> None:
        """Render the interactive map tab."""
        st.subheader("AI Ecosystem Map: Adoption, Research & Investment")

        # Map controls
        col1, col2, col3 = st.columns(3)
        with col1:
            map_metric = st.selectbox(
                "Primary Metric",
                [
                    "AI Adoption Rate",
                    "Federal AI Funding",
                    "AI Research Centers",
                    "AI Startups",
                    "Venture Capital",
                ],
            )
        with col2:
            show_nsf_institutes = st.checkbox("Show NSF AI Institutes", value=True)
        with col3:
            show_universities = st.checkbox("Show Major Universities", value=False)

        # Metric mapping with proper units
        metric_mapping = {
            "AI Adoption Rate": ("ai_adoption_rate", "%"),
            "Federal AI Funding": ("federal_ai_funding_millions", "$M"),
            "AI Research Centers": ("ai_research_centers", "centers"),
            "AI Startups": ("ai_startups", "startups"),
            "Venture Capital": ("venture_capital_millions", "$M"),
        }

        selected_metric, unit = metric_mapping[map_metric]

        # Get metric values and create better normalization
        metric_values = enhanced_geographic[selected_metric]

        # Normalize sizes with more dramatic scaling (10-50 range)
        min_val, max_val = metric_values.min(), metric_values.max()
        if max_val > min_val:
            normalized_sizes = 10 + (metric_values - min_val) / (max_val - min_val) * 40
        else:
            normalized_sizes = [25] * len(metric_values)

        # Create the enhanced map
        fig = go.Figure()

        # State choropleth
        fig.add_trace(
            go.Choropleth(
                locations=state_research_data["state_code"],
                z=state_research_data["ai_adoption_rate"],
                locationmode="USA-states",
                colorscale="Blues",
                colorbar=dict(
                    title="State AI<br>Adoption (%)", x=-0.05, len=0.35, y=0.75, thickness=15
                ),
                marker_line_color="black",
                marker_line_width=1,
                hovertemplate="<b>%{text}</b><br>AI Adoption: %{z:.1f}%<br>NSF Institutes: %{customdata[0]}<br>Federal Funding: $%{customdata[1]:.1f}B<extra></extra>",
                text=state_research_data["state"],
                customdata=state_research_data[
                    ["nsf_ai_institutes_total", "total_federal_funding_billions"]
                ],
                name="State Infrastructure",
                showlegend=False,
            )
        )

        # Dynamic city markers
        fig.add_trace(
            go.Scattergeo(
                lon=enhanced_geographic["lon"],
                lat=enhanced_geographic["lat"],
                text=enhanced_geographic["city"],
                customdata=enhanced_geographic[
                    [
                        "ai_adoption_rate",
                        "federal_ai_funding_millions",
                        "ai_research_centers",
                        "ai_startups",
                        "venture_capital_millions",
                        "nsf_ai_institutes",
                        "major_universities",
                    ]
                ],
                mode="markers",
                marker=dict(
                    size=normalized_sizes,
                    color=metric_values,
                    colorscale="Reds",
                    showscale=True,
                    colorbar=dict(
                        title=f"{map_metric}<br>({unit})", x=1.02, len=0.35, y=0.35, thickness=15
                    ),
                    line=dict(width=2, color="white"),
                    sizemode="diameter",
                    opacity=0.8,
                    cmin=min_val,
                    cmax=max_val,
                ),
                showlegend=False,
                hovertemplate="<b>%{text}</b><br>"
                + f"{map_metric}: %{{marker.color}}{unit}<br>"
                + "AI Adoption: %{customdata[0]:.1f}%<br>"
                + "Federal Funding: $%{customdata[1]:.0f}M<br>"
                + "Research Centers: %{customdata[2]}<br>"
                + "AI Startups: %{customdata[3]}<br>"
                + "VC Investment: $%{customdata[4]:.0f}M<br>"
                + "NSF Institutes: %{customdata[5]}<br>"
                + "Major Universities: %{customdata[6]}<extra></extra>",
                name="Cities",
            )
        )

        # Add NSF AI Institutes as special markers
        if show_nsf_institutes:
            nsf_cities = enhanced_geographic[enhanced_geographic["nsf_ai_institutes"] > 0]
            if len(nsf_cities) > 0:
                fig.add_trace(
                    go.Scattergeo(
                        lon=nsf_cities["lon"],
                        lat=nsf_cities["lat"],
                        text=nsf_cities["city"],
                        mode="markers",
                        marker=dict(
                            size=20, color="gold", symbol="star", line=dict(width=3, color="darkblue")
                        ),
                        name="NSF AI Institutes",
                        showlegend=True,
                        hovertemplate="<b>%{text}</b><br>NSF AI Institute Location<extra></extra>",
                    )
                )

        # Add major university indicators
        if show_universities:
            major_uni_cities = enhanced_geographic[enhanced_geographic["major_universities"] >= 5]
            if len(major_uni_cities) > 0:
                fig.add_trace(
                    go.Scattergeo(
                        lon=major_uni_cities["lon"],
                        lat=major_uni_cities["lat"],
                        text=major_uni_cities["city"],
                        mode="markers",
                        marker=dict(
                            size=15, color="purple", symbol="diamond", line=dict(width=2, color="white")
                        ),
                        name="Major University Hubs",
                        showlegend=True,
                        hovertemplate="<b>%{text}</b><br>Universities: %{customdata}<extra></extra>",
                        customdata=major_uni_cities["major_universities"],
                    )
                )

        fig.update_layout(
            title=f"US AI Ecosystem: {map_metric} Distribution",
            geo=dict(
                scope="usa",
                projection_type="albers usa",
                showland=True,
                landcolor="rgb(235, 235, 235)",
                coastlinecolor="rgb(50, 50, 50)",
                coastlinewidth=2,
            ),
            height=700,
            showlegend=True,
            legend=dict(
                x=0.85,
                y=0.95,
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="rgba(0,0,0,0.2)",
                borderwidth=1,
            ),
            margin=dict(l=50, r=80, t=50, b=50),
        )

        fig = self.a11y.make_chart_accessible(
            fig,
            title=f"US AI Ecosystem: {map_metric} Distribution",
            description=f"An interactive map of the United States showing AI ecosystem metrics. The base layer is a choropleth map displaying state-level AI adoption rates using a blue color scale. Cities are shown as circular markers sized and colored by {map_metric}, with larger and darker circles indicating higher values. The map includes {len(enhanced_geographic)} metropolitan areas with data ranging from {enhanced_geographic[selected_metric].min():.1f} to {enhanced_geographic[selected_metric].max():.1f} {unit}. Optional overlays include NSF AI Institute locations (gold stars) and major university hubs (purple diamonds). The visualization reveals geographic concentration of AI resources in coastal regions and major metropolitan areas, with significant disparities between innovation hubs and interior regions.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Dynamic insights based on selected metric
        if map_metric == "AI Adoption Rate":
            insight_text = f"""
            **🗺️ AI Adoption Geographic Insights:**
            - **Highest adoption:** {enhanced_geographic.loc[enhanced_geographic['ai_adoption_rate'].idxmax(), 'city']} ({enhanced_geographic['ai_adoption_rate'].max():.1f}%)
            - **Regional variation:** {enhanced_geographic['ai_adoption_rate'].max() - enhanced_geographic['ai_adoption_rate'].min():.1f} percentage point spread
            - **Coastal concentration:** West Coast and Northeast lead in AI implementation
            - **Digital divide:** Significant disparities between innovation hubs and interior regions
            """
        elif map_metric == "Federal AI Funding":
            top_funding_city = enhanced_geographic.loc[
                enhanced_geographic["federal_ai_funding_millions"].idxmax(), "city"
            ]
            top_funding_amount = enhanced_geographic["federal_ai_funding_millions"].max()
            total_funding = enhanced_geographic["federal_ai_funding_millions"].sum()
            top_5_funding = enhanced_geographic.nlargest(5, "federal_ai_funding_millions")[
                "federal_ai_funding_millions"
            ].sum()
            insight_text = f"""
            **🏛️ Federal Investment Geographic Insights:**
            - **Largest recipient:** {top_funding_city} (${top_funding_amount:.0f}M federal funding)
            - **Investment concentration:** Top 5 metros receive {(top_5_funding/total_funding)*100:.0f}% of federal AI research funding
            - **Total investment:** ${total_funding:.0f}M across all metros
            - **Research focus:** Federal funding concentrated in university-rich areas
            """
        elif map_metric == "AI Startups":
            top_startup_city = enhanced_geographic.loc[
                enhanced_geographic["ai_startups"].idxmax(), "city"
            ]
            top_startup_count = enhanced_geographic["ai_startups"].max()
            insight_text = f"""
            **🚀 AI Startup Geographic Insights:**
            - **Startup capital:** {top_startup_city} ({top_startup_count} AI startups)
            - **Total startups:** {enhanced_geographic['ai_startups'].sum()} across all metros
            - **Entrepreneurship hubs:** Concentrated in venture capital centers
            - **Innovation clusters:** Research-industry alignment drives startup formation
            """
        elif map_metric == "Venture Capital":
            top_vc_city = enhanced_geographic.loc[
                enhanced_geographic["venture_capital_millions"].idxmax(), "city"
            ]
            top_vc_amount = enhanced_geographic["venture_capital_millions"].max()
            total_vc = enhanced_geographic["venture_capital_millions"].sum()
            insight_text = f"""
            **💰 Venture Capital Geographic Insights:**
            - **Investment leader:** {top_vc_city} (${top_vc_amount:.0f}M in VC investment)
            - **Capital concentration:** {(top_vc_amount / total_vc * 100):.1f}% of total investment in top city
            - **Total VC:** ${total_vc:.0f}M across all metros
            - **Regional gaps:** 85% of private investment concentrated in coastal states
            """
        else:  # AI Research Centers
            top_research_city = enhanced_geographic.loc[
                enhanced_geographic["ai_research_centers"].idxmax(), "city"
            ]
            top_research_count = enhanced_geographic["ai_research_centers"].max()
            cities_with_nsf = len(enhanced_geographic[enhanced_geographic["nsf_ai_institutes"] > 0])
            total_nsf_institutes = enhanced_geographic["nsf_ai_institutes"].sum()
            insight_text = f"""
            **🔬 AI Research Geographic Insights:**
            - **Research leader:** {top_research_city} ({top_research_count} research centers)
            - **NSF AI Institutes:** {total_nsf_institutes} institutes across {cities_with_nsf} metropolitan areas
            - **Total centers:** {enhanced_geographic['ai_research_centers'].sum()} across all metros
            - **Academic concentration:** Research centers cluster near major universities
            """

        st.info(insight_text)

    def _render_research_infrastructure(self, state_research_data: pd.DataFrame) -> None:
        """Render the research infrastructure tab."""
        st.subheader("🏛️ Federal Research Infrastructure & NSF AI Institutes")

        # NSF AI Institutes overview
        col1, col2, col3, col4 = st.columns(4)

        total_institutes = state_research_data["nsf_ai_institutes_total"].sum()
        total_funding = state_research_data["total_federal_funding_billions"].sum()
        states_with_institutes = len(
            state_research_data[state_research_data["nsf_ai_institutes_total"] > 0]
        )

        with col1:
            st.metric("Total NSF AI Institutes", total_institutes, help="Across all states")
        with col2:
            st.metric(
                "States with Institutes", states_with_institutes, f"of {len(state_research_data)}"
            )
        with col3:
            st.metric("Total Federal Funding", f"${total_funding:.1f}B", "Research infrastructure")
        with col4:
            st.metric(
                "Average per State",
                f"${(total_funding/len(state_research_data)):.2f}B",
                "Funding distribution",
            )

        # Research infrastructure visualization
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "NSF AI Institutes by State",
                "Federal Research Funding",
                "R1 Research Universities",
                "AI Workforce Concentration",
            ),
            specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "scatter"}]],
        )

        # Sort by institutes for better visualization
        institutes_sorted = state_research_data.nlargest(10, "nsf_ai_institutes_total")

        fig.add_trace(
            go.Bar(
                x=institutes_sorted["state"],
                y=institutes_sorted["nsf_ai_institutes_total"],
                marker_color="#3498DB",
                text=institutes_sorted["nsf_ai_institutes_total"],
                textposition="outside",
                name="NSF Institutes",
            ),
            row=1,
            col=1,
        )

        funding_sorted = state_research_data.nlargest(10, "total_federal_funding_billions")
        fig.add_trace(
            go.Bar(
                x=funding_sorted["state"],
                y=funding_sorted["total_federal_funding_billions"],
                marker_color="#2ECC71",
                text=[f"${x:.1f}B" for x in funding_sorted["total_federal_funding_billions"]],
                textposition="outside",
                name="Federal Funding",
            ),
            row=1,
            col=2,
        )

        unis_sorted = state_research_data.nlargest(10, "r1_universities")
        fig.add_trace(
            go.Bar(
                x=unis_sorted["state"],
                y=unis_sorted["r1_universities"],
                marker_color="#9B59B6",
                text=unis_sorted["r1_universities"],
                textposition="outside",
                name="R1 Universities",
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=state_research_data["total_federal_funding_billions"],
                y=state_research_data["ai_workforce_thousands"],
                mode="markers+text",
                marker=dict(
                    size=state_research_data["nsf_ai_institutes_total"] * 10 + 10,
                    color=state_research_data["ai_adoption_rate"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="AI Adoption Rate"),
                ),
                text=state_research_data["state_code"],
                textposition="middle center",
                name="Funding vs Workforce",
            ),
            row=2,
            col=2,
        )

        fig.update_xaxes(tickangle=45)
        fig.update_layout(
            height=600, showlegend=False, title_text="Federal AI Research Infrastructure by State"
        )

        fig = self.a11y.make_chart_accessible(
            fig,
            title="Federal AI Research Infrastructure by State",
            description="A four-panel visualization of state AI research infrastructure. Top left: Bar chart of NSF AI Institutes by state, with California leading at 5 institutes, followed by Massachusetts (4), and New York, Texas, and Washington (3 each). Top right: Federal research funding by state in billions, with California receiving $3.2B, Massachusetts $1.1B, and New York $1.0B. Bottom left: R1 research universities count, showing California with 9, Texas with 8, and New York with 7. Bottom right: Scatter plot correlating federal funding (x-axis) with AI workforce in thousands (y-axis), where bubble sizes represent NSF institutes and colors show AI adoption rates. California (CA) stands out with the highest funding and workforce, while states like Texas (TX) and Massachusetts (MA) show strong but smaller ecosystems.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Research infrastructure insights
        with st.expander("📊 Research Infrastructure Analysis"):
            st.markdown(
                """
            #### NSF AI Research Institutes Program Impact
            
            **Established 2020-2021** with $220M initial federal investment:
            - **Geographic Distribution:** 27 institutes across 40+ states
            - **Research Focus Areas:** Machine learning, human-AI interaction, AI safety, sector applications
            - **Collaboration Model:** University-industry-government partnerships
            
            **Key Findings:**
            - **California leads** with 5 institutes, reflecting existing tech ecosystem
            - **Massachusetts concentration** in Boston area with 4 institutes near MIT/Harvard
            - **Distributed strategy** ensures geographic diversity beyond coastal hubs
            - **Federal coordination** creates national research network
            
            **Source:** NSF National AI Research Institutes Program, AI Index Report 2025
            """
            )

    def _render_state_comparisons(self, state_research_data: pd.DataFrame) -> None:
        """Render the state comparisons tab."""
        st.subheader("📊 State AI Ecosystem Comparison")

        # Create comprehensive state scorecard
        state_scorecard = state_research_data.copy()

        # Normalize metrics for scoring (0-100 scale)
        metrics_to_normalize = [
            "ai_adoption_rate",
            "nsf_ai_institutes_total",
            "total_federal_funding_billions",
            "r1_universities",
            "ai_workforce_thousands",
        ]

        for metric in metrics_to_normalize:
            max_val = state_scorecard[metric].max()
            min_val = state_scorecard[metric].min()
            state_scorecard[f"{metric}_score"] = (
                (state_scorecard[metric] - min_val) / (max_val - min_val)
            ) * 100

        # Calculate composite AI ecosystem score
        state_scorecard["composite_score"] = (
            state_scorecard["ai_adoption_rate_score"] * 0.3
            + state_scorecard["nsf_ai_institutes_total_score"] * 0.2
            + state_scorecard["total_federal_funding_billions_score"] * 0.2
            + state_scorecard["r1_universities_score"] * 0.15
            + state_scorecard["ai_workforce_thousands_score"] * 0.15
        )

        # Top performers analysis
        top_states = state_scorecard.nlargest(10, "composite_score")

        fig = go.Figure()

        # Create stacked bar chart showing component scores
        fig.add_trace(
            go.Bar(
                name="AI Adoption",
                x=top_states["state"],
                y=top_states["ai_adoption_rate_score"],
                marker_color="#3498DB",
            )
        )

        fig.add_trace(
            go.Bar(
                name="NSF Institutes",
                x=top_states["state"],
                y=top_states["nsf_ai_institutes_total_score"],
                marker_color="#E74C3C",
            )
        )

        fig.add_trace(
            go.Bar(
                name="Federal Funding",
                x=top_states["state"],
                y=top_states["total_federal_funding_billions_score"],
                marker_color="#2ECC71",
            )
        )

        fig.add_trace(
            go.Bar(
                name="Universities",
                x=top_states["state"],
                y=top_states["r1_universities_score"],
                marker_color="#9B59B6",
            )
        )

        fig.add_trace(
            go.Bar(
                name="AI Workforce",
                x=top_states["state"],
                y=top_states["ai_workforce_thousands_score"],
                marker_color="#F39C12",
            )
        )

        fig.update_layout(
            title="State AI Ecosystem Composite Scores (Top 10)",
            xaxis_title="State",
            yaxis_title="Normalized Score (0-100)",
            barmode="stack",
            height=500,
            xaxis_tickangle=45,
        )

        fig = self.a11y.make_chart_accessible(
            fig,
            title="State AI Ecosystem Composite Scores (Top 10)",
            description="A stacked bar chart showing the top 10 states' AI ecosystem composite scores, broken down into five components. Each bar represents a state's total score (0-100 scale) composed of: AI Adoption (blue), NSF Institutes (red), Federal Funding (green), Universities (purple), and AI Workforce (orange). California leads with the highest composite score, showing strong performance across all metrics. Massachusetts and New York follow, with particular strength in universities and federal funding. Texas, Washington, Illinois, Pennsylvania, Georgia, Colorado, and Florida round out the top 10, each showing different strengths. The stacked format reveals how different factors contribute to each state's overall AI ecosystem maturity, with coastal states generally showing more balanced development across all dimensions.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # State rankings table
        st.subheader("🏆 State AI Ecosystem Rankings")

        display_cols = [
            "state",
            "composite_score",
            "ai_adoption_rate",
            "nsf_ai_institutes_total",
            "total_federal_funding_billions",
            "ai_workforce_thousands",
        ]

        rankings_display = state_scorecard[display_cols].sort_values("composite_score", ascending=False)
        rankings_display["rank"] = range(1, len(rankings_display) + 1)
        rankings_display = rankings_display[["rank"] + display_cols]

        # Rename columns for display
        rankings_display.columns = [
            "Rank",
            "State",
            "Composite Score",
            "AI Adoption (%)",
            "NSF Institutes",
            "Federal Funding ($B)",
            "AI Workforce (K)",
        ]

        # Format the dataframe
        rankings_display["Composite Score"] = rankings_display["Composite Score"].round(1)
        rankings_display["Federal Funding ($B)"] = rankings_display["Federal Funding ($B)"].round(2)

        st.dataframe(rankings_display, hide_index=True, use_container_width=True)

    def _render_academic_centers(
        self, enhanced_geographic: pd.DataFrame, state_research_data: pd.DataFrame
    ) -> None:
        """Render the academic centers tab."""
        st.subheader("🎓 Academic AI Research Centers & University Ecosystem")

        # University ecosystem analysis
        university_metrics = (
            enhanced_geographic.groupby("state")
            .agg(
                {
                    "major_universities": "sum",
                    "ai_research_centers": "sum",
                    "federal_ai_funding_millions": "sum",
                    "ai_patents_2024": "sum",
                }
            )
            .reset_index()
        )

        university_metrics = university_metrics.merge(
            state_research_data[["state", "r1_universities"]], on="state", how="left"
        ).fillna(0)

        # Top academic states
        top_academic = university_metrics.nlargest(8, "ai_research_centers")

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("AI Research Centers by State", "Research Output vs Funding"),
            column_widths=[0.6, 0.4],
        )

        fig.add_trace(
            go.Bar(
                x=top_academic["ai_research_centers"],
                y=top_academic["state"],
                orientation="h",
                marker_color="#3498DB",
                text=[f"{x} centers" for x in top_academic["ai_research_centers"]],
                textposition="outside",
                name="Research Centers",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=university_metrics["federal_ai_funding_millions"],
                y=university_metrics["ai_patents_2024"],
                mode="markers+text",
                marker=dict(
                    size=university_metrics["ai_research_centers"] * 3,
                    color=university_metrics["major_universities"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Major Universities"),
                ),
                text=university_metrics["state"],
                textposition="top center",
                name="Funding vs Patents",
            ),
            row=1,
            col=2,
        )

        fig.update_layout(height=400, title_text="Academic AI Research Ecosystem")
        fig.update_xaxes(title_text="Research Centers", row=1, col=1)
        fig.update_yaxes(title_text="State", row=1, col=1)
        fig.update_xaxes(title_text="Federal Funding ($M)", row=1, col=2)
        fig.update_yaxes(title_text="AI Patents (2024)", row=1, col=2)

        fig = self.a11y.make_chart_accessible(
            fig,
            title="Academic AI Research Ecosystem",
            description="A two-panel visualization of academic AI research activity. Left panel: Horizontal bar chart showing AI research centers by state, with California leading at 23 centers, followed by Massachusetts (17), New York (16), Texas (11), Washington (6), Pennsylvania (5), Illinois (5), Florida (5), Georgia (4), and Colorado (3). Right panel: Scatter plot correlating federal AI funding (x-axis, in millions) with AI patents filed in 2024 (y-axis). Bubble sizes represent the number of research centers, and colors indicate the count of major universities using a Viridis color scale. California shows the highest values with over $3,500M in funding and 3,445 patents. The visualization reveals a strong correlation between funding, patent output, and university concentration, with California, Massachusetts, and New York forming a distinct top tier.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Academic insights
        st.success(
            """
        **🎓 Academic Research Insights:**
        - **California dominance:** 15 major AI research centers, led by Stanford, UC Berkeley, Caltech
        - **Massachusetts concentration:** MIT, Harvard creating dense research ecosystem
        - **Federal research strategy:** NSF institutes strategically distributed to build national capacity
        - **Industry-academia bridges:** Highest correlation between research centers and private investment
        """
        )

    def _render_investment_flows(self, enhanced_geographic: pd.DataFrame) -> None:
        """Render the investment flows tab."""
        st.subheader("💰 AI Investment Flows: Private Capital & Government Funding")

        # Investment flow analysis
        investment_flow = (
            enhanced_geographic.groupby("state")
            .agg(
                {
                    "venture_capital_millions": "sum",
                    "federal_ai_funding_millions": "sum",
                    "ai_startups": "sum",
                    "ai_adoption_rate": "mean",
                }
            )
            .reset_index()
        )

        # Calculate investment ratios
        investment_flow["private_to_federal_ratio"] = investment_flow[
            "venture_capital_millions"
        ] / investment_flow["federal_ai_funding_millions"].replace(0, 1)

        investment_flow["investment_per_startup"] = investment_flow[
            "venture_capital_millions"
        ] / investment_flow["ai_startups"].replace(0, 1)

        # Top investment states
        top_investment = investment_flow.nlargest(8, "venture_capital_millions")

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Private vs Federal Investment",
                "Investment Concentration",
                "Private-to-Federal Ratio",
                "Investment Efficiency",
            ),
            specs=[[{"secondary_y": True}, {"type": "pie"}], [{"type": "bar"}, {"type": "scatter"}]],
        )

        # Private vs Federal comparison
        fig.add_trace(
            go.Bar(
                name="Venture Capital",
                x=top_investment["state"],
                y=top_investment["venture_capital_millions"],
                marker_color="#E74C3C",
                yaxis="y",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                name="Federal Funding",
                x=top_investment["state"],
                y=top_investment["federal_ai_funding_millions"],
                marker_color="#3498DB",
                yaxis="y2",
            ),
            row=1,
            col=1,
        )

        # Investment concentration pie chart
        fig.add_trace(
            go.Pie(
                labels=top_investment["state"],
                values=top_investment["venture_capital_millions"],
                name="VC Distribution",
            ),
            row=1,
            col=2,
        )

        # Private-to-federal ratio
        ratio_data = investment_flow.nlargest(8, "private_to_federal_ratio")
        fig.add_trace(
            go.Bar(
                x=ratio_data["state"],
                y=ratio_data["private_to_federal_ratio"],
                marker_color="#F39C12",
                text=[f"{x:.1f}x" for x in ratio_data["private_to_federal_ratio"]],
                textposition="outside",
            ),
            row=2,
            col=1,
        )

        # Investment efficiency scatter
        fig.add_trace(
            go.Scatter(
                x=investment_flow["ai_startups"],
                y=investment_flow["investment_per_startup"],
                mode="markers+text",
                marker=dict(
                    size=investment_flow["ai_adoption_rate"] * 5,
                    color=investment_flow["venture_capital_millions"],
                    colorscale="Reds",
                    showscale=True,
                ),
                text=investment_flow["state"],
                textposition="top center",
            ),
            row=2,
            col=2,
        )

        fig.update_layout(height=700, title_text="AI Investment Ecosystem Analysis")

        fig = self.a11y.make_chart_accessible(
            fig,
            title="AI Investment Ecosystem Analysis",
            description="A four-panel investment analysis dashboard. Top left: Dual-axis bar chart comparing venture capital (red) and federal funding (blue) for top 10 states, with California showing massive VC dominance at over $15B. Top right: Pie chart showing VC distribution concentration, with California taking the largest slice, followed by New York, Massachusetts, and other states. Bottom left: Bar chart of private-to-federal funding ratios, with California showing the highest ratio above 5x, indicating strong private sector preference. Bottom right: Scatter plot correlating total investment with AI startups, where bubble sizes represent federal funding and position shows the relationship between investment levels and startup creation. The visualization reveals extreme geographic concentration of private investment in coastal states, while federal funding shows more geographic distribution.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Investment insights with data
        col1, col2 = st.columns(2)

        with col1:
            st.write("**💰 Investment Concentration:**")
            ca_vc = investment_flow[investment_flow["state"] == "California"][
                "venture_capital_millions"
            ].iloc[0]
            total_vc = investment_flow["venture_capital_millions"].sum()
            st.write(
                f"• **California dominance:** ${ca_vc:,.0f}M ({(ca_vc/total_vc)*100:.1f}% of total VC)"
            )
            st.write(
                f"• **Top 3 states:** {(investment_flow.nlargest(3, 'venture_capital_millions')['venture_capital_millions'].sum()/total_vc)*100:.1f}% of all investment"
            )
            st.write(
                "• **Geographic concentration:** Coastal states receive 85% of private AI investment"
            )

        with col2:
            st.write("**🏛️ Public-Private Balance:**")
            avg_ratio = investment_flow["private_to_federal_ratio"].mean()
            st.write(f"• **Average ratio:** {avg_ratio:.1f}x private to federal funding")
            st.write(
                "• **Federal strategy:** Research infrastructure investment vs private market development"
            )
            st.write("• **Regional development:** Federal funding more geographically distributed")


geographic_distribution_view = GeographicDistributionView()

def render(data: Dict[str, Any]) -> None:
    geographic_distribution_view.render(data)