"""Dashboard integration module for economic calculations.

This module provides helper functions to integrate real economic models
into the existing dashboard views.
"""

from typing import Dict, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .economic_insights import EconomicInsights
from .economic_models import AIEconomicModels
from .economic_validation import EconomicValidator


class DashboardIntegration:
    """Integrates economic models into dashboard views."""

    def __init__(self):
        """Initialize integration components."""
        self.economic_models = AIEconomicModels()
        self.validator = EconomicValidator()
        self.insights = EconomicInsights()

    def enhance_roi_calculator(
        self,
        investment_amount: float,
        project_type: str,
        company_size: str,
        implementation_quality: int,
        data_readiness: int,
        timeline: str,
        industry: str = "Other",
    ) -> Dict:
        """Enhanced ROI calculator using real economic models.

        Args:
            investment_amount: Initial investment in dollars
            project_type: Type of AI project
            company_size: Company size category
            implementation_quality: Quality score (1-5)
            data_readiness: Data readiness score (1-5)
            timeline: Implementation timeline string
            industry: Industry sector

        Returns:
            Dictionary with calculated metrics and validation
        """
        # Extract timeline in years
        timeline_months = int(timeline.split()[0])
        timeline_years = timeline_months / 12

        # Validate inputs
        is_valid, errors, confidence = self.validator.validate_economic_inputs(
            ai_investment=investment_amount,
            company_size=company_size,
            project_type=project_type,
            timeline_months=timeline_months,
            sector=industry,
        )

        if not is_valid:
            return {"valid": False, "errors": errors, "confidence": confidence}

        # Map project types to use cases in economic model
        use_case_map = {
            "Process Automation": "Default",
            "Predictive Analytics": "Predictive Maintenance",
            "Customer Service": "Customer Service Automation",
            "Product Development": "Software Development",
            "Marketing Optimization": "Sales & Marketing Optimization",
        }

        use_case = use_case_map.get(project_type, "Default")

        # Calculate efficiency based on quality scores
        current_efficiency = 0.5 + (implementation_quality + data_readiness) * 0.1

        # Get ROI from real model
        roi_results = self.economic_models.calculate_roi_with_real_data(
            investment=investment_amount,
            use_case=use_case,
            implementation_years=int(timeline_years),
            company_size=company_size,
            current_efficiency=current_efficiency,
            industry=industry,
        )

        # Get confidence intervals
        roi_confidence = self.economic_models.get_confidence_intervals(
            roi_results["total_roi_percentage"], "roi"
        )

        # Risk assessment based on implementation factors
        risk_score = 5 - ((implementation_quality + data_readiness) / 2)
        risk_levels = ["Very Low", "Low", "Medium", "High", "Very High"]
        risk_level = risk_levels[max(0, min(4, int(risk_score) - 1))]

        return {
            "valid": True,
            "final_roi": roi_results["total_roi_percentage"] / 100,  # Convert to multiplier
            "expected_return": investment_amount * (roi_results["total_roi_percentage"] / 100),
            "net_benefit": roi_results["total_value_created"],
            "payback_months": int(roi_results["payback_period_years"] * 12),
            "npv": roi_results["npv"],
            "irr": roi_results["irr"],
            "efficiency_gain": roi_results["efficiency_gain_percentage"],
            "risk_level": risk_level,
            "risk_score": risk_score,
            "confidence_intervals": roi_confidence,
            "data_confidence": confidence.get("overall", 0.85),
            "errors": [],
            "methodology": "McKinsey ROI data with industry adjustments",
        }

    def enhance_sector_roi_display(self, sector_data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Enhance sector ROI display with real calculations.

        Args:
            sector_data: DataFrame with sector information

        Returns:
            Tuple of (enhanced_data, insights)
        """
        # Map sectors to economic model sectors
        sector_map = {
            "Finance": "Financial Services",
            "Technology/Telecom": "Technology",
            "Professional Services": "Professional Services",
            "Healthcare": "Healthcare",
            "Manufacturing": "Manufacturing",
            "Retail Trade": "Retail",
            "Other": "Other",
        }

        enhanced_data = sector_data.copy()
        insights = {}

        for idx, row in enhanced_data.iterrows():
            sector = row["sector"]
            mapped_sector = sector_map.get(sector, "Other")

            # Get real productivity gains
            prod_results = self.economic_models.calculate_productivity_gain(
                revenue=1_000_000_000,  # $1B baseline
                years=2,
                industry=mapped_sector,
                adoption_maturity=row["adoption_rate"] / 100,
            )

            # Get market value impact
            market_results = self.economic_models.calculate_market_value_impact(
                revenue=1_000_000_000,
                industry=mapped_sector,
                ai_adoption_level=row["adoption_rate"],
            )

            # Update with real calculations
            enhanced_data.at[idx, "productivity_gain"] = prod_results[
                "productivity_gain_percentage"
            ]
            enhanced_data.at[idx, "market_value_impact"] = market_results[
                "market_value_increase_percentage"
            ]

            # Store sector-specific insights
            insights[sector] = {
                "productivity_baseline": prod_results["industry_baseline"],
                "growth_multiple": market_results["growth_multiple"],
                "adoption_premium": market_results["adoption_premium"],
            }

        return enhanced_data, insights

    def validate_and_enhance_input_form(self, form_container) -> Dict:
        """Add validation and enhancement to input forms.

        Args:
            form_container: Streamlit container for the form

        Returns:
            Dictionary with form values and validation
        """
        with form_container:
            st.markdown("### 📝 Input Validation")

            # Show valid ranges
            col1, col2 = st.columns(2)

            with col1:
                st.info(
                    """
                **Valid Ranges:**
                - Revenue: $1M - $1T
                - Employees: 10 - 500,000
                - AI Investment: 0.1% - 10% of revenue
                """
                )

            with col2:
                st.info(
                    """
                **Recommended:**
                - Revenue: $10M - $1B
                - AI Investment: 1-5% of revenue
                - Timeline: 12-36 months
                """
                )

            # Real-time validation feedback
            validation_container = st.empty()

            return {"validation_container": validation_container, "validator": self.validator}

    def display_calculation_methodology(self):
        """Display the calculation methodology and data sources."""
        with st.expander("📚 Calculation Methodology & Data Sources"):
            st.markdown(
                """
            ### Economic Models
            
            **1. Cost of Inaction Model**
            - Based on compound growth effects
            - Includes competitive displacement risk (exponential decay model)
            - S-curve innovation gap dynamics
            - GDP opportunity cost from Goldman Sachs 7% impact
            
            **2. ROI Calculation Model**
            - McKinsey actual ROI data by use case
            - S-curve adoption with learning curve effects
            - Industry-specific productivity gains (Goldman Sachs)
            - NPV calculation with 10% discount rate
            - IRR using Newton's method
            
            **3. Productivity Model**
            - Goldman Sachs sector data (25-40% gains)
            - Skill-level impacts from AI Index
            - Diminishing returns over time
            - Maturity bonus for advanced adopters
            
            **4. Market Value Model**
            - Industry P/E ratios
            - Growth multiples by sector
            - Network effects (value = base * adoption^1.5)
            - Competitive position adjustments
            
            ### Data Sources
            - **Goldman Sachs**: "The Potentially Large Effects of AI on Economic Growth" (2023)
            - **McKinsey**: "The State of AI in 2024" - ROI and implementation data
            - **Stanford AI Index**: Adoption trends and competitive dynamics
            - **BCG**: Competitive displacement research
            
            ### Confidence Scoring
            - Input validation against industry benchmarks
            - Cross-validation of metrics
            - Typical range analysis
            - 80% confidence intervals provided
            """
            )

    def create_enhanced_roi_timeline_chart(
        self,
        investment: float,
        use_case: str,
        years: int,
        company_size: str,
        industry: str = "Other",
    ) -> go.Figure:
        """Create enhanced ROI timeline chart with real calculations.

        Args:
            investment: Total investment amount
            use_case: AI use case
            years: Implementation years
            company_size: Company size category
            industry: Industry sector

        Returns:
            Plotly figure with ROI timeline
        """
        # Calculate scenarios
        scenarios = ["pessimistic", "expected", "optimistic"]
        scenario_multipliers = {"pessimistic": 0.7, "expected": 1.0, "optimistic": 1.3}

        fig = go.Figure()

        for scenario in scenarios:
            # Calculate ROI for scenario
            adjusted_investment = investment * scenario_multipliers[scenario]

            roi_results = self.economic_models.calculate_roi_with_real_data(
                investment=adjusted_investment,
                use_case=use_case,
                implementation_years=years,
                company_size=company_size,
                industry=industry,
            )

            # Generate monthly timeline
            months = np.arange(0, years * 12 + 1, 3)
            roi_values = []

            for month in months:
                if month == 0:
                    roi_values.append(-100)
                else:
                    # S-curve adoption
                    year_progress = month / 12
                    adoption = 1 / (1 + np.exp(-0.5 * (year_progress - years / 2)))

                    # Calculate cumulative ROI
                    cumulative_roi = (roi_results["total_roi_percentage"] * adoption) - 100
                    roi_values.append(cumulative_roi)

            # Add trace
            line_styles = {
                "pessimistic": dict(dash="dash", color="gray"),
                "expected": dict(color="blue", width=3),
                "optimistic": dict(dash="dot", color="green"),
            }

            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=roi_values,
                    name=scenario.capitalize(),
                    mode="lines",
                    line=line_styles[scenario],
                    hovertemplate="%{x} months: %{y:.0f}% ROI<extra></extra>",
                )
            )

        # Add break-even line
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="red",
            opacity=0.3,
            annotation_text="Break-even",
            annotation_position="right",
        )

        # Add payback period marker
        payback_months = roi_results["payback_period_years"] * 12
        fig.add_vline(
            x=payback_months,
            line_dash="dash",
            line_color="orange",
            opacity=0.5,
            annotation_text=f"Expected payback: {payback_months:.0f} months",
        )

        fig.update_layout(
            title=f"ROI Projection Timeline - {use_case}",
            xaxis_title="Months",
            yaxis_title="Cumulative ROI (%)",
            height=400,
            hovermode="x unified",
            showlegend=True,
            legend=dict(x=0.02, y=0.98),
        )

        return fig

    def generate_executive_roi_summary(
        self,
        investment: float,
        revenue: float,
        industry: str,
        current_adoption: float,
        target_adoption: float,
        timeline_years: int,
    ) -> Dict:
        """Generate executive summary of ROI analysis.

        Args:
            investment: AI investment amount
            revenue: Annual revenue
            industry: Industry sector
            current_adoption: Current AI adoption percentage
            target_adoption: Target AI adoption percentage
            timeline_years: Implementation timeline

        Returns:
            Dictionary with executive summary metrics
        """
        # Calculate cost of inaction
        cost_of_inaction = self.economic_models.calculate_cost_of_inaction(
            current_revenue=revenue,
            years=timeline_years,
            industry=industry,
            competitors_adopting_pct=60,  # Assume 60% average
            current_adoption_level=current_adoption,
        )

        # Calculate ROI projection
        roi_projection = self.economic_models.calculate_roi_with_real_data(
            investment=investment,
            use_case="Default",
            implementation_years=timeline_years,
            company_size=self._estimate_company_size(revenue),
            industry=industry,
        )

        # Calculate productivity gains
        productivity = self.economic_models.calculate_productivity_gain(
            revenue=revenue,
            years=timeline_years,
            industry=industry,
            adoption_maturity=target_adoption / 100,
        )

        # Calculate market value impact
        market_value = self.economic_models.calculate_market_value_impact(
            revenue=revenue, industry=industry, ai_adoption_level=target_adoption
        )

        # Generate key metrics
        return {
            "investment_intensity": (investment / revenue) * 100,
            "cost_of_inaction": cost_of_inaction["total_cost"],
            "cost_of_inaction_pct": cost_of_inaction["total_revenue_impact_pct"],
            "expected_roi": roi_projection["total_roi_percentage"],
            "npv": roi_projection["npv"],
            "payback_years": roi_projection["payback_period_years"],
            "productivity_gain": productivity["productivity_gain_percentage"],
            "annual_productivity_value": productivity["annual_productivity_improvement"],
            "market_value_increase": market_value["market_value_increase"],
            "market_value_pct": market_value["market_value_increase_percentage"],
            "risk_level": cost_of_inaction["market_position_risk"],
            "competitive_cycles_behind": cost_of_inaction["competitive_cycles_behind"],
            "break_even_year": roi_projection["break_even_year"],
            "irr": roi_projection["irr"],
        }

    def _estimate_company_size(self, revenue: float) -> str:
        """Estimate company size based on revenue."""
        if revenue < 50_000_000:
            return "Small"
        elif revenue < 500_000_000:
            return "Medium"
        elif revenue < 5_000_000_000:
            return "Large"
        else:
            return "Enterprise"

    def format_executive_metrics(self, metrics: Dict) -> str:
        """Format executive metrics for display."""
        return f"""
        ### 📊 Executive Summary
        
        **Investment Analysis:**
        - Investment Intensity: {metrics['investment_intensity']:.1f}% of revenue
        - Expected ROI: {metrics['expected_roi']:.0f}%
        - NPV: ${metrics['npv']/1_000_000:.1f}M
        - IRR: {metrics['irr']:.1f}%
        - Payback Period: {metrics['payback_years']:.1f} years
        
        **Strategic Impact:**
        - Cost of Inaction: ${metrics['cost_of_inaction']/1_000_000:.1f}M ({metrics['cost_of_inaction_pct']:.1f}% of revenue)
        - Productivity Gain: {metrics['productivity_gain']:.0f}%
        - Annual Productivity Value: ${metrics['annual_productivity_value']/1_000_000:.1f}M
        - Market Value Increase: {metrics['market_value_pct']:.0f}%
        
        **Risk Assessment:**
        - Market Position Risk: {metrics['risk_level']}
        - Competitive Cycles Behind: {metrics['competitive_cycles_behind']:.1f}
        - Break-even Year: Year {metrics['break_even_year']}
        """
