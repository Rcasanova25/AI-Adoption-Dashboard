"""Economic insights and executive summary components for the Economics of AI Dashboard."""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from .economic_models import AIEconomicModels, EconomicParameters


class EconomicInsights:
    """Generate economic insights and executive summaries for dashboard views."""

    @staticmethod
    def display_executive_summary(
        title: str, key_points: List[str], recommendations: List[str], urgency: str = "medium"
    ):
        """Display executive summary box with key insights.

        Args:
            title: Summary title
            key_points: List of key insight points
            recommendations: List of actionable recommendations
            urgency: Urgency level (low, medium, high, critical)
        """
        urgency_colors = {
            "low": "#d4edda",
            "medium": "#fff3cd",
            "high": "#f8d7da",
            "critical": "#f5c6cb",
        }

        color = urgency_colors.get(urgency, urgency_colors["medium"])

        st.markdown(
            f"""
        <div style='background-color: {color}; border-left: 5px solid #1f77b4; 
                    padding: 20px; margin: 20px 0; border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='margin-top: 0; color: #1f77b4;'>💡 {title}</h3>
            <div style='margin-bottom: 15px;'>
                <h4 style='color: #495057; font-size: 16px;'>Key Points:</h4>
                <ul style='margin: 5px 0;'>
                    {''.join([f"<li style='margin: 5px 0;'>{point}</li>" for point in key_points])}
                </ul>
            </div>
            <div>
                <h4 style='color: #495057; font-size: 16px;'>Recommendations:</h4>
                <ul style='margin: 5px 0;'>
                    {''.join([f"<li style='margin: 5px 0;'>{rec}</li>" for rec in recommendations])}
                </ul>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def generate_adoption_insights(adoption_data: pd.DataFrame) -> Dict[str, List[str]]:
        """Generate insights for adoption rate data."""
        current_rate = adoption_data.iloc[-1]["overall_adoption"]
        growth_rate = (
            adoption_data.iloc[-1]["overall_adoption"] - adoption_data.iloc[-5]["overall_adoption"]
        ) / 5

        key_points = [
            f"Overall AI adoption has reached {current_rate:.1f}%",
            f"Annual growth rate averaging {growth_rate:.1f}% over past 5 years",
            "GenAI adoption accelerating 3x faster than traditional AI",
            "Industry leaders show 2x higher adoption than average",
        ]

        recommendations = []
        if current_rate < 50:
            recommendations.append("Accelerate adoption to avoid competitive disadvantage")
        if growth_rate < 10:
            recommendations.append("Increase investment to match market growth rates")
        recommendations.extend(
            [
                "Focus on GenAI capabilities for maximum impact",
                "Benchmark against industry leaders, not average",
            ]
        )

        return {"key_points": key_points, "recommendations": recommendations}

    @staticmethod
    def generate_sector_insights(
        sector_data: pd.DataFrame, your_sector: str
    ) -> Dict[str, List[str]]:
        """Generate sector-specific insights."""
        sector_info = sector_data[sector_data["sector"] == your_sector].iloc[0]
        avg_adoption = sector_data["adoption_rate"].mean()

        position = "leading" if sector_info["adoption_rate"] > avg_adoption else "lagging"
        gap = abs(sector_info["adoption_rate"] - avg_adoption)

        key_points = [
            f"{your_sector} is {position} with {sector_info['adoption_rate']:.0f}% adoption",
            f"Gap to average: {gap:.0f} percentage points",
            f"Investment level: ${sector_info['investment_millions']:.0f}M",
            f"GenAI adoption at {sector_info['genai_adoption']:.0f}%",
        ]

        recommendations = []
        if position == "lagging":
            recommendations.append(f"Increase investment by {gap*2:.0f}% to reach parity")
            recommendations.append("Prioritize quick wins in high-ROI use cases")
        else:
            recommendations.append("Maintain leadership through innovation")
            recommendations.append("Share best practices across organization")

        return {"key_points": key_points, "recommendations": recommendations}

    @staticmethod
    def calculate_cost_of_inaction(
        company_size: str,
        industry: str,
        delay_months: int,
        current_adoption: float,
        current_revenue: Optional[float] = None,
        competitors_adopting_pct: Optional[float] = None,
    ) -> Dict[str, float]:
        """Calculate the economic cost of delaying AI adoption using accurate models.

        Uses real data from Goldman Sachs (7% GDP growth) and sector-specific
        productivity gains.

        Returns:
            Dictionary with cost metrics
        """
        # Initialize economic models
        models = AIEconomicModels()

        # Estimate revenue if not provided
        if current_revenue is None:
            size_revenues = {
                "Small": 10_000_000,  # $10M
                "Medium": 100_000_000,  # $100M
                "Large": 1_000_000_000,  # $1B
                "Enterprise": 10_000_000_000,  # $10B
            }
            current_revenue = size_revenues.get(company_size, 100_000_000)

        # Estimate competitor adoption if not provided
        if competitors_adopting_pct is None:
            # Industry averages from data
            industry_adoption = {
                "Technology": 75,
                "Financial Services": 65,
                "Healthcare": 45,
                "Retail": 40,
                "Manufacturing": 35,
                "Other": 50,
            }
            competitors_adopting_pct = industry_adoption.get(industry, 50)

        # Convert months to years for calculation
        delay_years = delay_months / 12

        # Calculate using accurate models
        results = models.calculate_cost_of_inaction(
            current_revenue=current_revenue,
            years=delay_years,
            industry=industry,
            competitors_adopting_pct=competitors_adopting_pct,
            current_adoption_level=current_adoption,
        )

        # Add confidence intervals
        confidence = models.get_confidence_intervals(results["total_cost"], "cost_of_inaction")

        # Format for display
        return {
            "market_share_loss": results["market_share_loss"] / current_revenue * 100,
            "productivity_loss": results["productivity_loss"] / current_revenue * 100,
            "competitive_cycles": results["competitive_cycles_behind"],
            "revenue_impact": results["total_cost"],
            "innovation_gap": min(100, delay_months * 3),  # Scaled to percentage
            "total_cost": results["total_cost"],
            "annualized_cost": results["annualized_cost"],
            "market_position_risk": results["market_position_risk"],
            "confidence_low": confidence["pessimistic"],
            "confidence_high": confidence["optimistic"],
        }

    @staticmethod
    def display_cost_of_inaction(costs: Dict[str, float], delay_months: int):
        """Display cost of inaction analysis with confidence intervals."""
        # Format confidence range
        conf_range = f"${costs.get('confidence_low', costs['total_cost']*0.8):,.0f} - ${costs.get('confidence_high', costs['total_cost']*1.2):,.0f}"

        # Risk level styling
        risk_colors = {"Low": "green", "Medium": "orange", "High": "red", "Critical": "darkred"}
        risk_level = costs.get("market_position_risk", "Medium")
        risk_color = risk_colors.get(risk_level, "orange")

        st.error(
            f"""
        ⚠️ **Cost of Inaction Analysis** *(Based on Goldman Sachs & McKinsey Research)*
        
        Delaying AI adoption by {delay_months} months will result in:
        
        📉 **Market Position Impact**
        - Market Share Loss: **{costs['market_share_loss']:.1f}%**
        - Competitive Cycles Behind: **{costs['competitive_cycles']:.1f}**
        - Innovation Gap: **{costs['innovation_gap']:.0f}%**
        - Market Position Risk: **<span style='color: {risk_color}'>{risk_level}</span>**
        
        💰 **Financial Impact**
        - Total Economic Cost: **${costs['total_cost']:,.0f}**
        - Confidence Range (80%): {conf_range}
        - Annualized Cost: **${costs.get('annualized_cost', costs['total_cost']/max(1, delay_months/12)):,.0f}**
        - Productivity Loss: **{costs['productivity_loss']:.1f}%**
        
        📊 **Key Insights**
        - Based on 7% GDP growth impact from AI (Goldman Sachs)
        - Includes compound productivity gains and S-curve adoption effects
        - Accounts for competitive displacement and market share erosion
        
        ⏰ **Time is Money**: Every month of delay compounds these losses exponentially.
        """
        )

    @staticmethod
    def create_competitive_position_matrix(
        your_adoption: float, your_investment: float, sector_data: pd.DataFrame
    ) -> go.Figure:
        """Create competitive position visualization."""
        fig = go.Figure()

        # Add sector bubbles
        fig.add_trace(
            go.Scatter(
                x=sector_data["adoption_rate"],
                y=sector_data["investment_millions"],
                mode="markers+text",
                marker=dict(
                    size=sector_data["genai_adoption"],
                    color=sector_data["avg_roi"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="ROI %"),
                    sizemode="diameter",
                    sizeref=2,
                ),
                text=sector_data["sector"],
                textposition="top center",
                name="Industries",
            )
        )

        # Add your position
        fig.add_trace(
            go.Scatter(
                x=[your_adoption],
                y=[your_investment],
                mode="markers+text",
                marker=dict(
                    size=30, color="red", symbol="star", line=dict(color="darkred", width=2)
                ),
                text=["Your Position"],
                textposition="bottom center",
                name="You",
            )
        )

        # Add quadrant lines
        avg_adoption = sector_data["adoption_rate"].mean()
        avg_investment = sector_data["investment_millions"].mean()

        fig.add_hline(y=avg_investment, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=avg_adoption, line_dash="dash", line_color="gray", opacity=0.5)

        # Add quadrant labels
        fig.add_annotation(
            x=25, y=avg_investment * 2, text="Laggards<br>Over-investing", showarrow=False
        )
        fig.add_annotation(
            x=75, y=avg_investment * 2, text="Leaders<br>High Investment", showarrow=False
        )
        fig.add_annotation(
            x=25, y=avg_investment * 0.3, text="Slow Movers<br>Low Priority", showarrow=False
        )
        fig.add_annotation(
            x=75, y=avg_investment * 0.3, text="Efficient<br>Adopters", showarrow=False
        )

        fig.update_layout(
            title="AI Adoption Competitive Position Matrix",
            xaxis_title="AI Adoption Rate (%)",
            yaxis_title="AI Investment (Millions $)",
            height=600,
            showlegend=True,
        )

        return fig

    @staticmethod
    def generate_what_if_scenarios(
        base_data: Dict[str, float],
        scenario_type: str,
        company_size: str = "Medium",
        industry: str = "Other",
    ) -> pd.DataFrame:
        """Generate what-if scenario projections using accurate economic models."""
        scenarios = []
        models = AIEconomicModels()

        if scenario_type == "adoption_acceleration":
            base_investment = base_data.get("investment", 1000000)
            base_timeline = base_data.get("timeline_years", 3)

            for acceleration in [1.0, 1.5, 2.0, 3.0]:
                # Calculate accelerated timeline
                accelerated_timeline = max(1, base_timeline / acceleration)

                # Calculate ROI with acceleration
                roi_data = models.calculate_roi_with_real_data(
                    investment=base_investment * (1 + (acceleration - 1) * 0.3),
                    use_case=base_data.get("use_case", "Default"),
                    implementation_years=accelerated_timeline,
                    company_size=company_size,
                )

                scenario = {
                    "scenario": f"{acceleration}x Acceleration",
                    "time_to_roi": roi_data["payback_period_years"],
                    "total_roi": roi_data["total_roi_percentage"],
                    "npv": roi_data["npv"],
                    "efficiency_gain": roi_data["efficiency_gain_percentage"],
                    "implementation_cost": base_investment * (1 + (acceleration - 1) * 0.3),
                }
                scenarios.append(scenario)

        elif scenario_type == "investment_levels":
            base_investment = base_data.get("investment", 1000000)

            for investment_mult in [0.5, 1.0, 1.5, 2.0]:
                adjusted_investment = base_investment * investment_mult

                # Calculate cost of inaction for comparison
                inaction_cost = models.calculate_cost_of_inaction(
                    current_revenue=base_data.get("revenue", 10000000),
                    years=3,
                    industry=industry,
                    competitors_adopting_pct=50 + (investment_mult - 1) * 20,
                    current_adoption_level=base_data.get("adoption", 20),
                )

                # Calculate productivity impact
                sector_gain = models.params.sector_productivity_gains.get(industry, 0.30)
                adjusted_productivity = sector_gain * investment_mult**0.7

                scenario = {
                    "scenario": f"{investment_mult}x Investment",
                    "adoption_rate": min(
                        100, base_data.get("adoption", 20) * (1 + (investment_mult - 1) * 0.4)
                    ),
                    "productivity_gain": adjusted_productivity * 100,
                    "avoided_loss": inaction_cost["total_cost"] * investment_mult,
                    "market_position": "Leader" if investment_mult >= 1.5 else "Follower",
                }
                scenarios.append(scenario)

        elif scenario_type == "competitive_response":
            responses = ["No Response", "Match Competition", "Exceed by 25%", "Industry Leader"]
            investment_levels = [0, 1.0, 1.25, 1.5]

            for response, inv_level in zip(responses, investment_levels):
                if inv_level == 0:
                    # Calculate cost of no response
                    cost_data = models.calculate_cost_of_inaction(
                        current_revenue=base_data.get("revenue", 10000000),
                        years=5,
                        industry=industry,
                        competitors_adopting_pct=75,
                        current_adoption_level=0,
                    )
                    scenario = {
                        "scenario": response,
                        "market_position": "Laggard",
                        "revenue_impact": -cost_data["total_cost"],
                        "market_share_loss": cost_data["market_share_loss"],
                        "competitive_risk": "Critical",
                    }
                else:
                    # Calculate competitive response benefits
                    roi_data = models.calculate_roi_with_real_data(
                        investment=base_data.get("investment", 1000000) * inv_level,
                        use_case=base_data.get("use_case", "Default"),
                        implementation_years=3,
                        company_size=company_size,
                    )
                    scenario = {
                        "scenario": response,
                        "market_position": "Leader" if inv_level >= 1.25 else "Competitive",
                        "revenue_impact": roi_data["total_value_created"],
                        "roi_percentage": roi_data["total_roi_percentage"],
                        "competitive_risk": "Low" if inv_level >= 1.25 else "Medium",
                    }
                scenarios.append(scenario)

        return pd.DataFrame(scenarios)

    @staticmethod
    def display_data_sources():
        """Display data sources and methodology."""
        models = AIEconomicModels()
        sources = models.get_data_sources()

        st.info(
            """
        **Data Sources & Methodology**
        
        This analysis is based on real-world data from leading research:
        
        • **GDP Impact**: {gdp_impact}
        • **Productivity Gains**: {productivity_gains}
        • **ROI Data**: {roi_data}
        • **Adoption Models**: {adoption_curves}
        • **Competitive Analysis**: {competitive_dynamics}
        
        All calculations use compound growth models, S-curve adoption dynamics, 
        and sector-specific parameters derived from actual enterprise implementations.
        """.format(
                **sources
            )
        )

    @staticmethod
    def display_action_plan(
        urgency: str, timeline: str, key_actions: List[str], success_metrics: List[str]
    ):
        """Display actionable plan based on insights."""
        urgency_emoji = {"low": "📅", "medium": "⏰", "high": "🚨", "critical": "🔥"}

        emoji = urgency_emoji.get(urgency, "📋")

        with st.expander(
            f"{emoji} **Recommended Action Plan** - {urgency.upper()} Priority", expanded=True
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Timeline**: {timeline}")
                st.markdown("**Key Actions**:")
                for i, action in enumerate(key_actions, 1):
                    st.markdown(f"{i}. {action}")

            with col2:
                st.markdown("**Success Metrics**:")
                for metric in success_metrics:
                    st.markdown(f"✓ {metric}")

            st.info(
                """
            💡 **Pro Tip**: Download this action plan and share with your team. 
            Track progress monthly and adjust based on results.
            """
            )

    @staticmethod
    def calculate_roi_projection(
        investment: float,
        use_case: str,
        company_size: str,
        implementation_timeline: int,
        current_efficiency: float = 1.0,
        industry: str = "Other",
    ) -> Dict[str, float]:
        """Calculate ROI projection using McKinsey actual data with industry-specific models.

        Args:
            investment: Total AI investment amount
            use_case: Type of AI use case
            company_size: Company size category
            implementation_timeline: Years for implementation
            current_efficiency: Current operational efficiency
            industry: Industry sector for specific calculations

        Returns:
            Dictionary with ROI metrics
        """
        # Initialize models with industry-specific parameters
        models = AIEconomicModels()

        # Validate inputs
        is_valid, errors = models.validate_inputs(
            investment=investment, years=implementation_timeline
        )

        if not is_valid:
            raise ValueError(f"Invalid inputs: {', '.join(errors)}")

        # Calculate ROI with real data and industry-specific adjustments
        roi_results = models.calculate_roi_with_real_data(
            investment=investment,
            use_case=use_case,
            implementation_years=implementation_timeline,
            company_size=company_size,
            current_efficiency=current_efficiency,
            industry=industry,
        )

        # Add confidence intervals
        confidence = models.get_confidence_intervals(roi_results["total_roi_percentage"], "roi")

        roi_results["confidence_intervals"] = confidence
        roi_results["data_source"] = "McKinsey State of AI 2024 & Goldman Sachs Research"

        return roi_results

    @staticmethod
    def display_roi_analysis(roi_data: Dict[str, float], investment: float):
        """Display ROI analysis with visualizations."""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total ROI",
                f"{roi_data['total_roi_percentage']:.0f}%",
                f"NPV: ${roi_data['npv']:,.0f}",
            )

        with col2:
            st.metric(
                "Payback Period",
                f"{roi_data['payback_period_years']:.1f} years",
                f"IRR: {roi_data['irr']:.1f}%",
            )

        with col3:
            st.metric(
                "Efficiency Gain",
                f"{roi_data['efficiency_gain_percentage']:.0f}%",
                f"Risk-Adjusted: {roi_data['risk_adjusted_roi']*100:.0f}%",
            )

        # Confidence range
        conf = roi_data["confidence_intervals"]
        st.info(
            f"""
        **Confidence Range (80%)**: {conf['pessimistic']:.0f}% - {conf['optimistic']:.0f}% ROI
        
        *Based on {roi_data['data_source']} - actual enterprise AI implementation data*
        """
        )

    @staticmethod
    def create_economic_calculator():
        """Create an interactive economic calculator widget."""
        st.subheader("AI Investment Economic Calculator")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Company Information**")
            company_size = st.selectbox(
                "Company Size",
                ["Small", "Medium", "Large", "Enterprise"],
                help="Select your company size category",
            )

            industry = st.selectbox(
                "Industry",
                [
                    "Technology",
                    "Financial Services",
                    "Healthcare",
                    "Retail",
                    "Manufacturing",
                    "Professional Services",
                    "Other",
                ],
                help="Select your industry sector",
            )

            current_revenue = st.number_input(
                "Current Annual Revenue ($)",
                min_value=1000000,
                max_value=100000000000,
                value=100000000,
                step=1000000,
                help="Enter your current annual revenue",
            )

            current_adoption = st.slider(
                "Current AI Adoption Level (%)",
                min_value=0,
                max_value=100,
                value=20,
                help="Your current level of AI adoption",
            )

        with col2:
            st.markdown("**Investment Parameters**")
            investment = st.number_input(
                "Planned AI Investment ($)",
                min_value=10000,
                max_value=10000000000,
                value=1000000,
                step=10000,
                help="Total planned AI investment",
            )

            use_case = st.selectbox(
                "Primary Use Case",
                [
                    "Customer Service Automation",
                    "Sales & Marketing Optimization",
                    "Supply Chain Optimization",
                    "Predictive Maintenance",
                    "Fraud Detection",
                    "Document Processing",
                    "Software Development",
                    "HR & Recruitment",
                    "Default",
                ],
                help="Select your primary AI use case",
            )

            timeline = st.slider(
                "Implementation Timeline (years)",
                min_value=1,
                max_value=5,
                value=3,
                help="Expected implementation timeline",
            )

            delay_months = st.slider(
                "Potential Delay (months)",
                min_value=0,
                max_value=36,
                value=6,
                help="Months of delay to analyze",
            )

        if st.button("Calculate Economic Impact", type="primary"):
            # Calculate Cost of Inaction
            st.markdown("### Cost of Delaying AI Adoption")

            cost_data = EconomicInsights.calculate_cost_of_inaction(
                company_size=company_size,
                industry=industry,
                delay_months=delay_months,
                current_adoption=current_adoption,
                current_revenue=current_revenue,
                competitors_adopting_pct=65,  # Industry average
            )

            EconomicInsights.display_cost_of_inaction(cost_data, delay_months)

            # Calculate ROI Projection
            st.markdown("### Expected ROI from AI Investment")

            roi_data = EconomicInsights.calculate_roi_projection(
                investment=investment,
                use_case=use_case,
                company_size=company_size,
                implementation_timeline=timeline,
                current_efficiency=1.0,
                industry=industry,
            )

            EconomicInsights.display_roi_analysis(roi_data, investment)

            # Show data sources
            with st.expander("View Data Sources & Methodology"):
                EconomicInsights.display_data_sources()


class CompetitiveIntelligence:
    """Generate competitive intelligence insights with accurate economic models."""

    def __init__(self):
        """Initialize with economic models."""
        self.models = AIEconomicModels()

    def assess_competitive_position(
        self, your_metrics: Dict[str, float], industry_data: pd.DataFrame, peer_data: pd.DataFrame
    ) -> Dict[str, any]:
        """Comprehensive competitive position assessment using real data."""

        # Calculate percentiles
        adoption_percentile = (
            (peer_data["adoption_rate"] < your_metrics["adoption"]).sum() / len(peer_data) * 100
        )
        investment_percentile = (
            (peer_data["investment"] < your_metrics["investment"]).sum() / len(peer_data) * 100
        )

        # Determine position
        if adoption_percentile >= 75 and investment_percentile >= 75:
            position = "Leader"
            risk = "Low"
        elif adoption_percentile >= 50:
            position = "Competitive"
            risk = "Medium"
        elif adoption_percentile >= 25:
            position = "Follower"
            risk = "High"
        else:
            position = "Laggard"
            risk = "Critical"

        # Calculate gaps
        leader_adoption = peer_data["adoption_rate"].quantile(0.9)
        adoption_gap = leader_adoption - your_metrics["adoption"]

        # Time to parity calculation with S-curve dynamics
        if your_metrics["growth_rate"] > 0:
            # Account for S-curve acceleration
            s_curve_factor = 1 / (1 + np.exp(-0.5 * (adoption_gap / 20 - 3)))
            adjusted_growth_rate = your_metrics["growth_rate"] * (1 + s_curve_factor)
            time_to_parity = adoption_gap / adjusted_growth_rate
        else:
            time_to_parity = float("inf")

        # Calculate cost of competitive gap
        if "revenue" in your_metrics:
            gap_cost = self.models.calculate_cost_of_inaction(
                current_revenue=your_metrics["revenue"],
                years=time_to_parity if time_to_parity != float("inf") else 5,
                industry=your_metrics.get("industry", "Other"),
                competitors_adopting_pct=adoption_percentile,
                current_adoption_level=your_metrics["adoption"],
            )
        else:
            gap_cost = {"total_cost": 0}

        return {
            "position": position,
            "risk_level": risk,
            "adoption_percentile": adoption_percentile,
            "investment_percentile": investment_percentile,
            "adoption_gap": adoption_gap,
            "time_to_parity_months": time_to_parity * 12,
            "recommended_investment_increase": max(0, adoption_gap * 0.15),  # 15% of gap
            "competitive_gap_cost": gap_cost["total_cost"],
            "catch_up_investment_required": adoption_gap
            * your_metrics.get("investment", 1000000)
            / 10,
        }
