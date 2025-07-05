"""View enhancement utilities for adding economic narratives to existing views."""

from typing import Dict, List, Optional, Tuple

import pandas as pd
import streamlit as st


class ViewEnhancer:
    """Enhance existing views with economic insights and executive summaries."""

    @staticmethod
    def add_adoption_rates_insights(adoption_data: pd.DataFrame, sector_data: pd.DataFrame):
        """Add insights to Adoption Rates view."""
        current_adoption = adoption_data.iloc[-1]["overall_adoption"]
        yoy_growth = current_adoption - adoption_data.iloc[-2]["overall_adoption"]

        key_points = [
            f"Global AI adoption reached {current_adoption:.1f}% in 2025",
            f"Year-over-year growth of {yoy_growth:.1f} percentage points",
            "GenAI driving 70% of new adoption",
            "Enterprise adoption outpacing SMBs by 3x",
        ]

        recommendations = [
            "Accelerate adoption to maintain competitive parity",
            "Focus on GenAI for maximum impact",
            "Invest in change management for successful adoption",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "What This Means for You",
            key_points,
            recommendations,
            urgency="high" if current_adoption > 80 else "medium",
        )

    @staticmethod
    def add_industry_analysis_insights(
        sector_data: pd.DataFrame, your_industry: Optional[str] = None
    ):
        """Add insights to Industry Analysis view with sector-specific parameters."""
        from .economic_models import AIEconomicModels, EconomicParameters

        models = AIEconomicModels()
        params = EconomicParameters()

        # Top and bottom performers
        top_3 = sector_data.nlargest(3, "adoption_rate")
        bottom_3 = sector_data.nsmallest(3, "adoption_rate")

        key_points = [
            f"Technology leads with {top_3.iloc[0]['adoption_rate']:.0f}% adoption (40% productivity potential)",
            f"Bottom sectors lag by {top_3.iloc[0]['adoption_rate'] - bottom_3.iloc[0]['adoption_rate']:.0f} points",
            "Financial services: 35% productivity gains, 18-month payback",
            "Healthcare: 30% gains but 24-month implementation cycle",
        ]

        if your_industry:
            industry_data = sector_data[sector_data["sector"] == your_industry].iloc[0]
            rank = (
                len(sector_data)
                - (sector_data["adoption_rate"] > industry_data["adoption_rate"]).sum()
            )

            # Get industry-specific parameters
            productivity = params.sector_productivity_gains.get(your_industry, 0.30) * 100
            payback = params.industry_payback_periods.get(your_industry, 18)

            key_points.append(
                f"{your_industry}: #{rank} rank, {productivity:.0f}% productivity gain, {payback}-month payback"
            )

        recommendations = [
            "Target sector-specific productivity gains (25-40% range)",
            "Plan for industry-specific implementation timelines",
            "Leverage industry P/E ratios for value creation",
            "Account for sector learning curves",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Industry Competitive Dynamics", key_points, recommendations, urgency="high"
        )

    @staticmethod
    def add_investment_insights(investment_data: pd.DataFrame):
        """Add insights to Investment Trends view."""
        latest_investment = investment_data.iloc[-1]["global_investment_billions"]
        cagr = (
            (latest_investment / investment_data.iloc[0]["global_investment_billions"])
            ** (1 / len(investment_data))
            - 1
        ) * 100

        key_points = [
            f"Global AI investment reached ${latest_investment:.1f}B in 2025",
            f"CAGR of {cagr:.1f}% over past {len(investment_data)} years",
            "US maintaining 40% share of global investment",
            "China closing gap with aggressive state funding",
        ]

        recommendations = [
            "Increase AI budget to match market growth",
            "Focus on partnerships to leverage investment",
            "Consider AI-as-a-Service to reduce capex",
        ]

        urgency = "critical" if cagr > 30 else "high"

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Investment Landscape Analysis", key_points, recommendations, urgency=urgency
        )

    @staticmethod
    def add_roi_insights(roi_data: Dict[str, float], industry: str = "Other"):
        """Add insights to ROI Analysis view with accurate calculations."""
        from .economic_models import AIEconomicModels

        models = AIEconomicModels()

        # Calculate market value impact
        market_impact = models.calculate_market_value_impact(
            revenue=100_000_000,  # Example $100M revenue
            industry=industry,
            ai_adoption_level=50,  # 50% adoption
            competitive_position="Average",
        )

        # Calculate payback period
        payback = models.calculate_payback_period(
            investment=1_000_000, annual_benefit=2_500_000, industry=industry  # Based on avg ROI
        )

        key_points = [
            f"Average ROI of {roi_data.get('avg_roi', 150):.0f}% with {payback['payback_months']:.0f}-month payback",
            f"Market value increase potential: {market_impact['market_value_increase_percentage']:.0f}%",
            f"Industry P/E ratio: {market_impact['pe_ratio']:.1f}x",
            f"Network effect multiplier: {market_impact['network_effect_multiplier']:.2f}x",
            "Implementation includes {:.0f}-month ramp-up period".format(payback["ramp_up_months"]),
        ]

        recommendations = [
            "Account for learning curve in ROI projections",
            "Leverage network effects for exponential value",
            "Plan for {:.0f}-month total implementation".format(
                payback["total_implementation_months"]
            ),
            "Focus on market value creation, not just cost savings",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "ROI Maximization Strategy", key_points, recommendations, urgency="medium"
        )

    @staticmethod
    def add_token_economics_insights(token_data: pd.DataFrame):
        """Add insights to Token Economics view."""
        cost_reduction = (
            (
                token_data.iloc[0]["cost_per_million_tokens"]
                - token_data.iloc[-1]["cost_per_million_tokens"]
            )
            / token_data.iloc[0]["cost_per_million_tokens"]
            * 100
        )

        key_points = [
            f"Token costs dropped {cost_reduction:.0f}% in 3 years",
            "Open source models 10x cheaper than proprietary",
            "Cost no longer primary barrier to adoption",
            "Quality-to-cost ratio improving exponentially",
        ]

        recommendations = [
            "Reevaluate projects rejected on cost grounds",
            "Implement token optimization strategies",
            "Consider hybrid model approach for cost efficiency",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Token Economics Revolution", key_points, recommendations, urgency="high"
        )

    @staticmethod
    def add_labor_impact_insights(labor_data: pd.DataFrame):
        """Add insights to Labor Impact view."""
        augmented_pct = labor_data[labor_data["job_category"] == "Augmented"][
            "percentage_of_workforce"
        ].iloc[0]
        displaced_pct = labor_data[labor_data["job_category"] == "Displaced"][
            "percentage_of_workforce"
        ].iloc[0]

        key_points = [
            f"{augmented_pct}% of jobs will be augmented by AI",
            f"Only {displaced_pct}% face displacement risk",
            "Low-skilled workers seeing highest productivity gains",
            "New job categories emerging rapidly",
        ]

        recommendations = [
            "Invest in reskilling programs now",
            "Focus on human-AI collaboration",
            "Communicate transparently about changes",
            "Create internal mobility pathways",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Workforce Transformation Roadmap", key_points, recommendations, urgency="critical"
        )

    @staticmethod
    def add_geographic_insights(geographic_data: pd.DataFrame):
        """Add insights to Geographic Distribution view."""
        top_cities = geographic_data.nlargest(5, "adoption_rate")
        avg_adoption = geographic_data["adoption_rate"].mean()

        key_points = [
            f"Top 5 cities average {top_cities['adoption_rate'].mean():.0f}% adoption",
            f"Geographic divide of {top_cities['adoption_rate'].mean() - avg_adoption:.0f} points",
            "Emerging hubs in unexpected locations",
            "Talent concentration driving adoption patterns",
        ]

        recommendations = [
            "Consider distributed AI teams",
            "Tap into emerging talent markets",
            "Leverage remote work for talent access",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Geographic Strategy Insights", key_points, recommendations, urgency="medium"
        )

    @staticmethod
    def add_cost_trends_insights(cost_data: pd.DataFrame):
        """Add insights to AI Cost Trends view."""
        cost_drop = (
            (
                cost_data.iloc[0]["training_cost_per_model"]
                - cost_data.iloc[-1]["training_cost_per_model"]
            )
            / cost_data.iloc[0]["training_cost_per_model"]
            * 100
        )

        key_points = [
            f"Training costs dropped {cost_drop:.0f}% since 2020",
            "Inference costs approaching zero for basic models",
            "Cloud AI democratizing access",
            "Cost barriers effectively eliminated for most use cases",
        ]

        recommendations = [
            "Shift focus from cost to value creation",
            "Experiment broadly given low costs",
            "Invest savings into scaling adoption",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Cost Revolution Implications", key_points, recommendations, urgency="high"
        )

    @staticmethod
    def add_skill_gap_insights(skill_data: pd.DataFrame):
        """Add insights to Skill Gap Analysis view."""
        critical_gaps = skill_data[skill_data["gap_severity"] == "Critical"]
        avg_gap = (skill_data["demand_index"] - skill_data["supply_index"]).mean()

        key_points = [
            f"{len(critical_gaps)} skill areas at critical shortage",
            f"Average supply-demand gap of {avg_gap:.0f} points",
            "ML Engineering most severe shortage",
            "Prompt engineering emerging as key skill",
        ]

        recommendations = [
            "Launch aggressive upskilling programs",
            "Partner with universities for talent pipeline",
            "Consider acqui-hiring for critical skills",
            "Implement AI-assisted training",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Talent Strategy Imperatives", key_points, recommendations, urgency="critical"
        )

    @staticmethod
    def add_governance_insights(governance_data: pd.DataFrame):
        """Add insights to AI Governance view."""
        avg_implementation = governance_data["implementation_rate"].mean()
        critical_areas = governance_data[governance_data["implementation_rate"] < 50]

        key_points = [
            f"Average governance implementation at {avg_implementation:.0f}%",
            f"{len(critical_areas)} areas below 50% implementation",
            "Data privacy leading, bias detection lagging",
            "Regulatory requirements accelerating",
        ]

        recommendations = [
            "Establish AI ethics committee",
            "Implement bias detection tools",
            "Document AI decision processes",
            "Prepare for regulatory audits",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Governance Risk Assessment", key_points, recommendations, urgency="high"
        )

    @staticmethod
    def add_productivity_insights(productivity_data: pd.DataFrame, industry: str = "Other"):
        """Add insights to Productivity Research view with accurate models."""
        from .economic_models import AIEconomicModels

        models = AIEconomicModels()

        avg_gain = productivity_data["productivity_gain"].mean()
        max_gain = productivity_data.iloc[productivity_data["productivity_gain"].idxmax()]

        # Calculate industry-specific productivity gains
        productivity_calc = models.calculate_productivity_gain(
            revenue=100_000_000,  # Example $100M revenue
            years=3,
            industry=industry,
            skill_level="Mixed",
        )

        key_points = [
            f"Industry baseline productivity gain: {productivity_calc['industry_baseline']:.0f}% (Goldman Sachs data)",
            f"Skill-adjusted potential: {productivity_calc['skill_adjusted_gain']:.0f}%",
            f"{max_gain['worker_category']} seeing {max_gain['productivity_gain']:.0f}% improvement",
            "Low-skilled workers benefit most from AI augmentation",
            "Diminishing returns factor: {:.0%}".format(productivity_calc["time_adjusted_factor"]),
        ]

        recommendations = [
            "Focus on low-skilled worker augmentation for maximum impact",
            "Implement learning curve optimization strategies",
            "Plan for diminishing returns in long-term projections",
            "Measure both productivity and quality improvements",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Productivity Transformation Guide", key_points, recommendations, urgency="high"
        )

    @staticmethod
    def add_environmental_insights(environmental_data: pd.DataFrame):
        """Add insights to Environmental Impact view."""
        avg_improvement = environmental_data["impact_percentage"].mean()

        key_points = [
            f"Average environmental improvement of {avg_improvement:.0f}%",
            "AI optimization reducing energy use significantly",
            "Predictive maintenance cutting waste",
            "Smart systems enabling sustainability",
        ]

        recommendations = [
            "Integrate AI into sustainability strategy",
            "Measure and report environmental gains",
            "Use AI for carbon footprint reduction",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Sustainability Through AI", key_points, recommendations, urgency="medium"
        )

    @staticmethod
    def add_oecd_insights(oecd_data: pd.DataFrame):
        """Add insights to OECD Findings view."""
        us_adoption = oecd_data[oecd_data["country"] == "United States"]["adoption_rate"].iloc[0]
        avg_adoption = oecd_data["adoption_rate"].mean()

        key_points = [
            f"OECD average adoption at {avg_adoption:.0f}%",
            f"US leads with {us_adoption:.0f}% adoption",
            "Policy frameworks accelerating adoption",
            "International cooperation increasing",
        ]

        recommendations = [
            "Monitor regulatory developments",
            "Engage in policy discussions",
            "Prepare for compliance requirements",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Global Policy Landscape", key_points, recommendations, urgency="medium"
        )

    @staticmethod
    def add_barriers_insights(barriers_data: pd.DataFrame):
        """Add insights to Barriers & Support view."""
        top_barriers = barriers_data.nlargest(3, "percentage_citing")

        key_points = [
            f"Top barrier: {top_barriers.iloc[0]['barrier']} ({top_barriers.iloc[0]['percentage_citing']:.0f}%)",
            "Skill shortage remains critical constraint",
            "Data quality issues underestimated",
            "Cultural resistance declining",
        ]

        recommendations = [
            "Address top 3 barriers systematically",
            "Build coalition for change",
            "Celebrate early wins publicly",
            "Invest in data infrastructure",
        ]

        from .economic_insights import EconomicInsights

        EconomicInsights.display_executive_summary(
            "Barrier Mitigation Strategy", key_points, recommendations, urgency="high"
        )
