"""Competitive Position Assessor - Homepage component for the Economics of AI Dashboard."""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .economic_insights import CompetitiveIntelligence, EconomicInsights


class CompetitivePositionAssessor:
    """Main competitive position assessment interface."""

    def __init__(
        self,
        sector_data: pd.DataFrame,
        firm_size_data: pd.DataFrame,
        adoption_trends: pd.DataFrame,
        investment_data: pd.DataFrame,
    ):
        """Initialize with required data."""
        self.sector_data = sector_data
        self.firm_size_data = firm_size_data
        self.adoption_trends = adoption_trends
        self.investment_data = investment_data
        self.insights = EconomicInsights()
        self.intelligence = CompetitiveIntelligence()

    def render(self):
        """Render the complete competitive position assessor interface."""
        st.title("🎯 AI Competitive Position Assessor")
        st.markdown(
            """
        **Welcome to the Economics of AI Dashboard** - Your strategic companion for navigating 
        the AI transformation. This tool provides real-time competitive intelligence and 
        actionable insights tailored to your organization.
        """
        )

        # Quick assessment section
        st.markdown("---")
        st.subheader("📊 Quick Assessment")

        col1, col2, col3 = st.columns(3)

        with col1:
            industry = st.selectbox(
                "Your Industry",
                options=self.sector_data["sector"].tolist(),
                help="Select your primary industry sector",
            )

        with col2:
            company_size = st.selectbox(
                "Company Size",
                options=[
                    "Small (<50)",
                    "Medium (50-999)",
                    "Large (1000-4999)",
                    "Enterprise (5000+)",
                ],
                help="Select based on number of employees",
            )

        with col3:
            current_adoption = st.slider(
                "Current AI Adoption Level (%)",
                min_value=0,
                max_value=100,
                value=25,
                step=5,
                help="Estimate your organization's current AI adoption",
            )

        # Additional inputs in expandable section
        with st.expander("🔧 Advanced Settings", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                annual_revenue = st.number_input(
                    "Annual Revenue ($M)", min_value=0.0, value=100.0, step=10.0
                )
                ai_investment = st.number_input(
                    "Annual AI Investment ($M)", min_value=0.0, value=5.0, step=0.5
                )
            with col2:
                growth_target = st.slider(
                    "Growth Target (%)", min_value=0, max_value=100, value=20, step=5
                )
                risk_tolerance = st.select_slider(
                    "Risk Tolerance",
                    options=["Conservative", "Moderate", "Aggressive"],
                    value="Moderate",
                )

        # Generate assessment
        if st.button("🚀 Generate Assessment", type="primary", use_container_width=True):
            self._generate_assessment(
                industry,
                company_size,
                current_adoption,
                annual_revenue,
                ai_investment,
                growth_target,
                risk_tolerance,
            )

    def _generate_assessment(
        self,
        industry: str,
        company_size: str,
        current_adoption: float,
        annual_revenue: float,
        ai_investment: float,
        growth_target: float,
        risk_tolerance: str,
    ):
        """Generate comprehensive competitive assessment."""

        # Get relevant data
        sector_info = self.sector_data[self.sector_data["sector"] == industry].iloc[0]
        industry_avg_adoption = sector_info["adoption_rate"]
        industry_avg_investment = sector_info["investment_millions"]

        # Calculate metrics
        your_metrics = {
            "adoption": current_adoption,
            "investment": ai_investment,
            "growth_rate": growth_target / 100,
            "investment_intensity": (
                (ai_investment / annual_revenue) * 100 if annual_revenue > 0 else 0
            ),
        }

        # Create peer comparison data
        peer_data = self._create_peer_data(industry, company_size)

        # Get competitive position
        position_data = self.intelligence.assess_competitive_position(
            your_metrics, self.sector_data, peer_data
        )

        # Display results in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "📈 Executive Summary",
                "🎯 Competitive Position",
                "💰 Economic Impact",
                "🔮 What-If Scenarios",
                "📋 Action Plan",
            ]
        )

        with tab1:
            self._display_executive_summary(
                industry, current_adoption, industry_avg_adoption, position_data, sector_info
            )

        with tab2:
            self._display_competitive_position(your_metrics, sector_info, position_data, peer_data)

        with tab3:
            self._display_economic_impact(
                company_size,
                industry,
                current_adoption,
                annual_revenue,
                ai_investment,
                growth_target,
            )

        with tab4:
            self._display_what_if_scenarios(
                your_metrics, industry, company_size, annual_revenue, risk_tolerance
            )

        with tab5:
            self._display_action_plan(
                position_data, industry, company_size, current_adoption, growth_target
            )

    def _display_executive_summary(
        self,
        industry: str,
        current_adoption: float,
        industry_avg: float,
        position_data: Dict,
        sector_info: pd.Series,
    ):
        """Display executive summary with key insights."""

        # Determine urgency based on position
        urgency_map = {
            "Leader": "low",
            "Competitive": "medium",
            "Follower": "high",
            "Laggard": "critical",
        }
        urgency = urgency_map.get(position_data["position"], "medium")

        # Generate key points
        adoption_gap = industry_avg - current_adoption
        key_points = []

        if position_data["position"] == "Leader":
            key_points.append(
                f"You're ahead of {position_data['adoption_percentile']:.0f}% of peers"
            )
            key_points.append("Well-positioned to capture AI value creation")
        else:
            key_points.append(
                f"You're behind {100-position_data['adoption_percentile']:.0f}% of peers"
            )
            key_points.append(f"Gap to industry average: {abs(adoption_gap):.0f} percentage points")

        key_points.extend(
            [
                f"Industry leaders at {sector_info['adoption_rate']:.0f}% adoption",
                f"Time to reach parity: {position_data['time_to_parity_months']:.0f} months at current pace",
                f"GenAI adoption in your industry: {sector_info['genai_adoption']:.0f}%",
            ]
        )

        # Generate recommendations
        recommendations = []
        if position_data["position"] in ["Follower", "Laggard"]:
            recommendations.append(
                f"Increase AI investment by {position_data['recommended_investment_increase']:.0f}%"
            )
            recommendations.append("Focus on quick-win use cases for rapid value")
            recommendations.append("Establish AI Center of Excellence")
        else:
            recommendations.append("Maintain momentum with innovation focus")
            recommendations.append("Expand successful use cases across organization")
            recommendations.append("Invest in advanced AI capabilities (GenAI, ML)")

        # Display summary
        self.insights.display_executive_summary(
            title=f"Your AI Position: {position_data['position']}",
            key_points=key_points,
            recommendations=recommendations,
            urgency=urgency,
        )

        # Key metrics cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Competitive Position",
                position_data["position"],
                delta=f"{position_data['adoption_percentile']:.0f}th percentile",
            )

        with col2:
            st.metric(
                "Adoption Gap",
                f"{abs(adoption_gap):.0f}%",
                delta="Behind" if adoption_gap > 0 else "Ahead",
                delta_color="inverse" if adoption_gap > 0 else "normal",
            )

        with col3:
            st.metric(
                "Risk Level", position_data["risk_level"], help="Risk of competitive displacement"
            )

        with col4:
            months = position_data["time_to_parity_months"]
            if months == float("inf"):
                parity_text = "N/A"
            else:
                parity_text = f"{months:.0f} months"
            st.metric(
                "Time to Parity",
                parity_text,
                help="Time to reach industry average at current growth rate",
            )

    def _display_competitive_position(
        self,
        your_metrics: Dict,
        sector_info: pd.Series,
        position_data: Dict,
        peer_data: pd.DataFrame,
    ):
        """Display detailed competitive position analysis."""

        st.subheader("🎯 Competitive Position Analysis")

        # Create competitive position matrix
        fig = self.insights.create_competitive_position_matrix(
            your_metrics["adoption"], your_metrics["investment"], self.sector_data
        )
        st.plotly_chart(fig, use_container_width=True)

        # Peer comparison
        st.subheader("👥 Peer Comparison")

        col1, col2 = st.columns(2)

        with col1:
            # Adoption comparison
            fig_adoption = go.Figure()
            fig_adoption.add_trace(
                go.Box(y=peer_data["adoption_rate"], name="Industry Peers", boxpoints="outliers")
            )
            fig_adoption.add_trace(
                go.Scatter(
                    x=[0],
                    y=[your_metrics["adoption"]],
                    mode="markers",
                    marker=dict(size=15, color="red", symbol="star"),
                    name="Your Position",
                )
            )
            fig_adoption.update_layout(
                title="Adoption Rate Distribution",
                yaxis_title="Adoption Rate (%)",
                showlegend=True,
                height=400,
            )
            st.plotly_chart(fig_adoption, use_container_width=True)

        with col2:
            # Investment comparison
            fig_investment = go.Figure()
            fig_investment.add_trace(
                go.Box(y=peer_data["investment"], name="Industry Peers", boxpoints="outliers")
            )
            fig_investment.add_trace(
                go.Scatter(
                    x=[0],
                    y=[your_metrics["investment"]],
                    mode="markers",
                    marker=dict(size=15, color="red", symbol="star"),
                    name="Your Investment",
                )
            )
            fig_investment.update_layout(
                title="AI Investment Distribution",
                yaxis_title="Investment ($M)",
                showlegend=True,
                height=400,
            )
            st.plotly_chart(fig_investment, use_container_width=True)

        # Competitive advantages/disadvantages
        st.subheader("💪 Competitive Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Advantages**")
            advantages = self._identify_advantages(your_metrics, sector_info, peer_data)
            for adv in advantages:
                st.markdown(f"• {adv}")

        with col2:
            st.markdown("**⚠️ Gaps to Address**")
            gaps = self._identify_gaps(your_metrics, sector_info, peer_data)
            for gap in gaps:
                st.markdown(f"• {gap}")

    def _display_economic_impact(
        self,
        company_size: str,
        industry: str,
        current_adoption: float,
        annual_revenue: float,
        ai_investment: float,
        growth_target: float,
    ):
        """Display economic impact analysis."""

        st.subheader("💰 Economic Impact Analysis")

        # Cost of inaction calculator
        st.markdown("### Cost of Inaction")

        delay_months = st.slider(
            "Delay in AI adoption (months)",
            min_value=0,
            max_value=24,
            value=6,
            step=3,
            help="How long would you delay full AI adoption?",
        )

        if delay_months > 0:
            costs = self.insights.calculate_cost_of_inaction(
                company_size, industry, delay_months, current_adoption
            )
            self.insights.display_cost_of_inaction(costs, delay_months)

        # ROI projections
        st.markdown("### ROI Projections")

        # Create ROI timeline
        months = np.arange(0, 37, 3)
        conservative_roi = self._calculate_roi_curve(months, ai_investment, "conservative")
        expected_roi = self._calculate_roi_curve(months, ai_investment, "expected")
        optimistic_roi = self._calculate_roi_curve(months, ai_investment, "optimistic")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=months,
                y=conservative_roi,
                name="Conservative",
                line=dict(dash="dash", color="gray"),
            )
        )
        fig.add_trace(
            go.Scatter(x=months, y=expected_roi, name="Expected", line=dict(color="blue", width=3))
        )
        fig.add_trace(
            go.Scatter(
                x=months, y=optimistic_roi, name="Optimistic", line=dict(dash="dot", color="green")
            )
        )

        fig.add_hline(y=0, line_dash="solid", line_color="red", opacity=0.3)
        fig.update_layout(
            title="ROI Projection Timeline",
            xaxis_title="Months",
            yaxis_title="ROI (%)",
            height=400,
            hovermode="x",
        )

        st.plotly_chart(fig, use_container_width=True)

        # Key economic metrics
        st.markdown("### Key Economic Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            payback_period = self._calculate_payback_period(ai_investment, annual_revenue)
            st.metric(
                "Payback Period", f"{payback_period} months", help="Time to recover AI investment"
            )

        with col2:
            productivity_gain = self._estimate_productivity_gain(current_adoption, growth_target)
            st.metric(
                "Productivity Gain",
                f"{productivity_gain:.1f}%",
                delta=f"+{productivity_gain*annual_revenue/100:.1f}M value",
            )

        with col3:
            market_value = self._estimate_market_value_impact(current_adoption, ai_investment)
            st.metric(
                "Market Value Impact",
                f"{market_value:.1f}%",
                help="Estimated impact on company valuation",
            )

    def _display_what_if_scenarios(
        self,
        your_metrics: Dict,
        industry: str,
        company_size: str,
        annual_revenue: float,
        risk_tolerance: str,
    ):
        """Display what-if scenario analysis."""

        st.subheader("🔮 What-If Scenario Analysis")

        scenario_type = st.radio(
            "Select Scenario Type",
            ["Adoption Acceleration", "Investment Levels", "Competitive Response"],
            horizontal=True,
        )

        # Generate base data for scenarios
        base_data = {
            "adoption": your_metrics["adoption"],
            "investment": your_metrics["investment"],
            "time_to_roi": 12,
            "total_roi": 150,
            "risk_level": 5,
            "cost": your_metrics["investment"],
            "productivity": 25,
            "market_share": 15,
            "payback": 18,
            "position": 50,
            "revenue": annual_revenue,
            "talent": 70,
            "innovation": 60,
        }

        # Generate scenarios
        if scenario_type == "Adoption Acceleration":
            scenarios = self.insights.generate_what_if_scenarios(base_data, "adoption_acceleration")

            # Display scenario comparison
            fig = go.Figure()

            x = scenarios["scenario"]
            fig.add_trace(go.Bar(name="Time to ROI (months)", x=x, y=scenarios["time_to_roi"]))
            fig.add_trace(go.Bar(name="Total ROI (%)", x=x, y=scenarios["total_roi"]))

            fig.update_layout(
                title="Impact of Accelerating AI Adoption", barmode="group", height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            # Detailed metrics
            st.dataframe(
                scenarios.style.format(
                    {
                        "time_to_roi": "{:.1f} months",
                        "total_roi": "{:.0f}%",
                        "risk_level": "{:.1f}/10",
                        "implementation_cost": "${:,.0f}M",
                    }
                ),
                use_container_width=True,
            )

        elif scenario_type == "Investment Levels":
            scenarios = self.insights.generate_what_if_scenarios(base_data, "investment_levels")

            # Create multi-metric visualization
            fig = go.Figure()

            for metric in ["adoption_rate", "productivity_gain", "market_share_gain"]:
                fig.add_trace(
                    go.Scatter(
                        x=scenarios["scenario"],
                        y=scenarios[metric],
                        mode="lines+markers",
                        name=metric.replace("_", " ").title(),
                    )
                )

            fig.update_layout(
                title="Impact of Different Investment Levels",
                xaxis_title="Investment Scenario",
                yaxis_title="Impact (%)",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        else:  # Competitive Response
            scenarios = self.insights.generate_what_if_scenarios(base_data, "competitive_response")

            # Radar chart for competitive scenarios
            categories = [
                "Market Position",
                "Revenue Impact",
                "Talent Retention",
                "Innovation Score",
            ]

            fig = go.Figure()

            for _, row in scenarios.iterrows():
                fig.add_trace(
                    go.Scatterpolar(
                        r=[
                            row["market_position"],
                            row["revenue_impact"],
                            row["talent_retention"],
                            row["innovation_score"],
                        ],
                        theta=categories,
                        fill="toself",
                        name=row["scenario"],
                    )
                )

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Competitive Response Scenarios",
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Scenario recommendations
        st.info(
            """
        💡 **Scenario Insights**: Based on your risk tolerance and current position, 
        the optimal strategy appears to be moderate acceleration with focused investment 
        in high-ROI use cases. This balances risk with competitive necessity.
        """
        )

    def _display_action_plan(
        self,
        position_data: Dict,
        industry: str,
        company_size: str,
        current_adoption: float,
        growth_target: float,
    ):
        """Display actionable plan based on assessment."""

        st.subheader("📋 Your AI Action Plan")

        # Determine plan parameters based on position
        if position_data["position"] == "Laggard":
            urgency = "critical"
            timeline = "3-6 months"
            key_actions = [
                "Form AI task force with executive sponsorship",
                "Identify and implement 3 quick-win use cases",
                "Partner with AI consultancy for rapid capability building",
                "Allocate emergency budget for AI initiatives",
                "Benchmark against industry leaders",
            ]
            success_metrics = [
                "25% adoption within 6 months",
                "3 use cases in production",
                "ROI demonstrated in at least 1 use case",
                "AI team of 5+ people established",
            ]

        elif position_data["position"] == "Follower":
            urgency = "high"
            timeline = "6-12 months"
            key_actions = [
                "Develop comprehensive AI strategy",
                "Scale successful pilots to production",
                "Build internal AI capabilities through training",
                "Increase AI budget by 50%",
                "Establish AI governance framework",
            ]
            success_metrics = [
                "50% adoption within 12 months",
                "5+ use cases in production",
                "20% productivity improvement",
                "AI CoE fully operational",
            ]

        elif position_data["position"] == "Competitive":
            urgency = "medium"
            timeline = "12-18 months"
            key_actions = [
                "Focus on differentiation through AI innovation",
                "Expand AI to customer-facing applications",
                "Invest in advanced AI capabilities (GenAI)",
                "Share best practices across organization",
                "Develop proprietary AI solutions",
            ]
            success_metrics = [
                "75% adoption achieved",
                "Industry recognition for AI innovation",
                "30% ROI on AI investments",
                "AI-driven competitive advantages established",
            ]

        else:  # Leader
            urgency = "low"
            timeline = "Ongoing"
            key_actions = [
                "Maintain leadership through continuous innovation",
                "Explore cutting-edge AI technologies",
                "Contribute to industry AI standards",
                "Monetize AI capabilities",
                "Build AI ecosystem partnerships",
            ]
            success_metrics = [
                "90%+ adoption maintained",
                "Industry thought leadership",
                "New revenue streams from AI",
                "Partner ecosystem established",
            ]

        # Display the action plan
        self.insights.display_action_plan(urgency, timeline, key_actions, success_metrics)

        # Download action plan button
        if st.button("📥 Download Full Action Plan", use_container_width=True):
            st.info("Action plan download functionality coming soon!")

        # Next steps
        st.markdown("### 🚀 Immediate Next Steps")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                """
            **Week 1**
            - Share assessment with leadership
            - Form AI steering committee
            - Identify quick wins
            """
            )

        with col2:
            st.markdown(
                """
            **Month 1**
            - Develop AI roadmap
            - Allocate budget
            - Start pilot projects
            """
            )

        with col3:
            st.markdown(
                """
            **Quarter 1**
            - Launch first use cases
            - Measure initial ROI
            - Scale successful pilots
            """
            )

    # Helper methods
    def _create_peer_data(self, industry: str, company_size: str) -> pd.DataFrame:
        """Create synthetic peer comparison data."""
        np.random.seed(42)  # For consistency

        # Base metrics from sector data
        sector_info = self.sector_data[self.sector_data["sector"] == industry].iloc[0]
        base_adoption = sector_info["adoption_rate"]
        base_investment = sector_info["investment_millions"]

        # Size adjustments
        size_factors = {
            "Small (<50)": 0.3,
            "Medium (50-999)": 0.6,
            "Large (1000-4999)": 1.0,
            "Enterprise (5000+)": 1.5,
        }
        size_factor = size_factors.get(company_size, 1.0)

        # Generate peer data
        n_peers = 20
        peer_data = pd.DataFrame(
            {
                "company": [f"Peer {i+1}" for i in range(n_peers)],
                "adoption_rate": np.random.normal(base_adoption, 15, n_peers).clip(0, 100),
                "investment": np.random.normal(
                    base_investment * size_factor, base_investment * size_factor * 0.3, n_peers
                ).clip(0, None),
                "genai_adoption": np.random.normal(sector_info["genai_adoption"], 10, n_peers).clip(
                    0, 100
                ),
                "employees": np.random.normal(1000 * size_factor, 300 * size_factor, n_peers).clip(
                    50, None
                ),
            }
        )

        return peer_data

    def _identify_advantages(
        self, your_metrics: Dict, sector_info: pd.Series, peer_data: pd.DataFrame
    ) -> List[str]:
        """Identify competitive advantages."""
        advantages = []

        if your_metrics["adoption"] > sector_info["adoption_rate"]:
            advantages.append("Above industry average in AI adoption")

        if your_metrics["investment"] > peer_data["investment"].median():
            advantages.append("Higher AI investment than most peers")

        if your_metrics["growth_rate"] > 0.15:
            advantages.append("Aggressive growth strategy in place")

        if your_metrics["investment_intensity"] > 5:
            advantages.append("Strong commitment to AI transformation")

        if not advantages:
            advantages.append("Opportunity to leapfrog competition")

        return advantages

    def _identify_gaps(
        self, your_metrics: Dict, sector_info: pd.Series, peer_data: pd.DataFrame
    ) -> List[str]:
        """Identify competitive gaps."""
        gaps = []

        if your_metrics["adoption"] < sector_info["adoption_rate"]:
            gap = sector_info["adoption_rate"] - your_metrics["adoption"]
            gaps.append(f"Adoption {gap:.0f}% below industry average")

        if your_metrics["investment"] < peer_data["investment"].median():
            gaps.append("Investment below peer median")

        if your_metrics["adoption"] < sector_info["genai_adoption"]:
            gaps.append("Limited GenAI adoption")

        if your_metrics["growth_rate"] < 0.10:
            gaps.append("Slow AI expansion pace")

        return gaps

    def _calculate_roi_curve(
        self, months: np.ndarray, investment: float, scenario: str
    ) -> np.ndarray:
        """Calculate ROI curve for different scenarios."""
        # Base parameters by scenario
        params = {
            "conservative": {"break_even": 18, "max_roi": 120, "rate": 0.08},
            "expected": {"break_even": 12, "max_roi": 180, "rate": 0.12},
            "optimistic": {"break_even": 8, "max_roi": 250, "rate": 0.15},
        }

        p = params[scenario]

        # S-curve ROI model
        roi = np.zeros_like(months, dtype=float)
        for i, month in enumerate(months):
            if month < p["break_even"]:
                roi[i] = -100 * (1 - month / p["break_even"])
            else:
                t = month - p["break_even"]
                roi[i] = p["max_roi"] * (1 - np.exp(-p["rate"] * t))

        return roi

    def _calculate_payback_period(self, investment: float, revenue: float) -> int:
        """Calculate estimated payback period."""
        if revenue == 0:
            return 24

        # Estimate based on investment intensity
        intensity = investment / revenue

        if intensity < 0.02:
            return 18
        elif intensity < 0.05:
            return 12
        elif intensity < 0.10:
            return 8
        else:
            return 6

    def _estimate_productivity_gain(self, adoption: float, growth_target: float) -> float:
        """Estimate productivity gain from AI adoption."""
        base_gain = adoption * 0.3  # 0.3% gain per 1% adoption
        growth_multiplier = 1 + (growth_target / 100)
        return base_gain * growth_multiplier

    def _estimate_market_value_impact(self, adoption: float, investment: float) -> float:
        """Estimate impact on market valuation."""
        adoption_impact = adoption * 0.15  # 0.15% value per 1% adoption
        investment_signal = min(10, investment * 0.5)  # Investment signaling effect
        return adoption_impact + investment_signal
