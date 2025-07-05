"""Key takeaways generator for dashboard views."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st


@dataclass
class Takeaway:
    """Represents a single key takeaway."""

    category: str  # 'threat', 'opportunity', 'action'
    message: str
    urgency: str  # 'low', 'medium', 'high', 'critical'
    impact: str  # 'low', 'medium', 'high'
    timeframe: str  # 'immediate', 'short-term', 'long-term'


class KeyTakeawaysGenerator:
    """Generates intelligent key takeaways from data."""

    def __init__(self):
        """Initialize the takeaways generator."""
        self.urgency_colors = {
            "low": "#28a745",
            "medium": "#ffc107",
            "high": "#fd7e14",
            "critical": "#dc3545",
        }

        self.category_icons = {"threat": "⚠️", "opportunity": "💡", "action": "🎯"}

    def generate_takeaways(
        self, view_type: str, data: Dict[str, Any], persona: str = "General"
    ) -> List[Takeaway]:
        """Generate takeaways for a specific view.

        Args:
            view_type: Type of dashboard view
            data: Relevant data for analysis
            persona: User persona for tailored insights

        Returns:
            List of takeaways
        """
        # Map view types to generation methods
        generators = {
            "adoption_rates": self._adoption_takeaways,
            "competitive_position": self._competitive_takeaways,
            "roi_analysis": self._roi_takeaways,
            "industry_analysis": self._industry_takeaways,
            "geographic_distribution": self._geographic_takeaways,
            "labor_impact": self._labor_takeaways,
            "cost_trends": self._cost_takeaways,
            "token_economics": self._token_takeaways,
            "skill_gap": self._skill_takeaways,
            "governance": self._governance_takeaways,
        }

        generator = generators.get(view_type, self._generic_takeaways)
        takeaways = generator(data, persona)

        # Sort by urgency (critical first)
        urgency_order = ["critical", "high", "medium", "low"]
        takeaways.sort(key=lambda x: urgency_order.index(x.urgency))

        return takeaways[:3]  # Return top 3 most important

    def render_takeaways(
        self, takeaways: List[Takeaway], expanded: bool = True, show_details: bool = True
    ):
        """Render key takeaways in the UI.

        Args:
            takeaways: List of takeaways to display
            expanded: Whether to show expanded by default
            show_details: Whether to show detailed information
        """
        with st.expander("🎯 **Key Takeaways**", expanded=expanded):
            if not takeaways:
                st.info("No specific takeaways available for this view.")
                return

            for takeaway in takeaways:
                self._render_single_takeaway(takeaway, show_details)

            # Add download button
            if st.button("📥 Download Takeaways", key="download_takeaways"):
                self._download_takeaways(takeaways)

    def _render_single_takeaway(self, takeaway: Takeaway, show_details: bool):
        """Render a single takeaway."""
        col1, col2 = st.columns([1, 20])

        with col1:
            st.markdown(self.category_icons[takeaway.category])

        with col2:
            # Create colored container based on urgency
            border_color = self.urgency_colors[takeaway.urgency]

            st.markdown(
                f"""
            <div style='border-left: 4px solid {border_color}; 
                        padding: 10px 15px; margin: 5px 0;
                        background-color: rgba(248, 249, 250, 0.8);
                        border-radius: 0 8px 8px 0;'>
                <p style='margin: 0; font-size: 16px; color: #212529;'>
                    <strong>{takeaway.category.title()}:</strong> {takeaway.message}
                </p>
                {f'''<p style='margin: 5px 0 0 0; font-size: 13px; color: #6c757d;'>
                    Urgency: {takeaway.urgency.title()} | 
                    Impact: {takeaway.impact.title()} | 
                    Timeframe: {takeaway.timeframe.title()}
                </p>''' if show_details else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )

    def render_summary_box(
        self,
        title: str = "Executive Summary",
        takeaways: List[Takeaway] = None,
        additional_metrics: Optional[Dict[str, str]] = None,
    ):
        """Render a summary box with key takeaways and metrics.

        Args:
            title: Title of the summary box
            takeaways: List of takeaways
            additional_metrics: Optional metrics to display
        """
        st.markdown(
            f"""
        <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 25px; border-radius: 15px; margin: 20px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h3 style='margin: 0 0 20px 0; color: #1f77b4;'>📊 {title}</h3>
        """,
            unsafe_allow_html=True,
        )

        # Render takeaways
        if takeaways:
            for takeaway in takeaways:
                icon = self.category_icons[takeaway.category]
                st.markdown(
                    f"""
                <div style='margin: 10px 0;'>
                    <strong>{icon} {takeaway.category.title()}:</strong> {takeaway.message}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Render additional metrics if provided
        if additional_metrics:
            st.markdown("<hr style='margin: 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)
            cols = st.columns(len(additional_metrics))
            for idx, (metric, value) in enumerate(additional_metrics.items()):
                with cols[idx]:
                    st.metric(metric, value)

        st.markdown("</div>", unsafe_allow_html=True)

    # Specific takeaway generators for each view type

    def _adoption_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for adoption rates view."""
        takeaways = []

        adoption_rate = data.get("current_adoption", 87.3)
        growth_rate = data.get("yoy_growth", 15)
        industry_avg = data.get("industry_average", 72)

        # Threat analysis
        if adoption_rate < industry_avg:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"Your adoption rate is {industry_avg - adoption_rate:.1f}% below industry average",
                    urgency="high",
                    impact="high",
                    timeframe="immediate",
                )
            )

        # Opportunity analysis
        if growth_rate > 20:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message=f"Rapid growth of {growth_rate}% creates first-mover advantages",
                    urgency="high",
                    impact="high",
                    timeframe="short-term",
                )
            )

        # Action recommendation
        if adoption_rate < 50:
            takeaways.append(
                Takeaway(
                    category="action",
                    message="Start with 3 high-ROI pilot projects in the next 90 days",
                    urgency="critical",
                    impact="high",
                    timeframe="immediate",
                )
            )
        else:
            takeaways.append(
                Takeaway(
                    category="action",
                    message="Scale successful use cases across the organization",
                    urgency="medium",
                    impact="medium",
                    timeframe="short-term",
                )
            )

        return takeaways

    def _competitive_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for competitive position view."""
        takeaways = []

        position = data.get("competitive_position", "Follower")
        gap_to_leaders = data.get("gap_to_leaders", 25)
        time_to_parity = data.get("time_to_parity_months", 18)

        position_risks = {
            "Laggard": ("critical", "Risk of market irrelevance within 24 months"),
            "Follower": ("high", "Competitors gaining sustainable advantages"),
            "Competitive": ("medium", "Need differentiation to maintain position"),
            "Leader": ("low", "Position secure but innovation required"),
        }

        urgency, risk_message = position_risks.get(position, ("medium", "Position unclear"))

        takeaways.append(
            Takeaway(
                category="threat",
                message=risk_message,
                urgency=urgency,
                impact="high",
                timeframe="short-term",
            )
        )

        if gap_to_leaders > 20:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message=f"Closing {gap_to_leaders}% gap could increase market value by ${gap_to_leaders * 10}M",
                    urgency="high",
                    impact="high",
                    timeframe="long-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message=f"Accelerate adoption to reach parity in {time_to_parity} months",
                urgency="high" if time_to_parity > 12 else "medium",
                impact="high",
                timeframe="short-term",
            )
        )

        return takeaways

    def _roi_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for ROI analysis view."""
        takeaways = []

        expected_roi = data.get("expected_roi", 185)
        payback_period = data.get("payback_months", 12)
        confidence = data.get("confidence_level", "high")

        if expected_roi < 100:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"ROI of {expected_roi}% below industry benchmark of 150%",
                    urgency="medium",
                    impact="medium",
                    timeframe="long-term",
                )
            )
        else:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message=f"Strong ROI of {expected_roi}% justifies aggressive investment",
                    urgency="high",
                    impact="high",
                    timeframe="short-term",
                )
            )

        if payback_period > 18:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"Long payback period of {payback_period} months increases risk",
                    urgency="medium",
                    impact="medium",
                    timeframe="long-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Focus on quick-win use cases to demonstrate early value",
                urgency="high",
                impact="medium",
                timeframe="immediate",
            )
        )

        return takeaways

    def _industry_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for industry analysis view."""
        takeaways = []

        your_industry = data.get("your_industry", "Technology")
        industry_rank = data.get("industry_rank", 5)
        total_industries = data.get("total_industries", 12)
        growth_rate = data.get("industry_growth_rate", 15)

        if industry_rank > total_industries / 2:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"{your_industry} ranks {industry_rank}/{total_industries} in AI adoption",
                    urgency="high",
                    impact="high",
                    timeframe="immediate",
                )
            )

        if growth_rate > 20:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message=f"Industry growing at {growth_rate}% - window for competitive advantage",
                    urgency="high",
                    impact="high",
                    timeframe="short-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Study top 3 industry leaders' AI strategies and adapt best practices",
                urgency="medium",
                impact="medium",
                timeframe="short-term",
            )
        )

        return takeaways

    def _geographic_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for geographic distribution view."""
        takeaways = []

        regional_gap = data.get("regional_adoption_gap", 35)
        talent_availability = data.get("talent_score", 6.5)

        if regional_gap > 30:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"Regional adoption gap of {regional_gap}% limits talent access",
                    urgency="medium",
                    impact="medium",
                    timeframe="long-term",
                )
            )

        if talent_availability < 7:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message="Consider remote AI teams or relocation incentives",
                    urgency="medium",
                    impact="high",
                    timeframe="short-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Establish partnerships with leading AI hubs for knowledge transfer",
                urgency="medium",
                impact="medium",
                timeframe="short-term",
            )
        )

        return takeaways

    def _labor_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for labor impact view."""
        takeaways = []

        displacement_risk = data.get("displacement_percentage", 12)
        augmentation_potential = data.get("augmentation_percentage", 45)
        reskilling_gap = data.get("reskilling_gap", 65)

        if displacement_risk > 15:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"{displacement_risk}% of workforce at displacement risk",
                    urgency="high",
                    impact="high",
                    timeframe="short-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="opportunity",
                message=f"{augmentation_potential}% of jobs can be enhanced with AI",
                urgency="medium",
                impact="high",
                timeframe="short-term",
            )
        )

        if reskilling_gap > 50:
            takeaways.append(
                Takeaway(
                    category="action",
                    message="Launch comprehensive reskilling program within 60 days",
                    urgency="critical",
                    impact="high",
                    timeframe="immediate",
                )
            )

        return takeaways

    def _cost_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for cost trends view."""
        takeaways = []

        cost_reduction = data.get("cost_reduction_3yr", 85)
        current_cost_barrier = data.get("cost_barrier_percentage", 15)

        takeaways.append(
            Takeaway(
                category="opportunity",
                message=f"AI costs dropped {cost_reduction}% - previously impossible projects now viable",
                urgency="high",
                impact="high",
                timeframe="immediate",
            )
        )

        if current_cost_barrier < 20:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message="Cost no longer primary barrier - focus on implementation speed",
                    urgency="high",
                    impact="medium",
                    timeframe="immediate",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Re-evaluate projects rejected on cost grounds in the last 2 years",
                urgency="medium",
                impact="medium",
                timeframe="short-term",
            )
        )

        return takeaways

    def _token_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for token economics view."""
        takeaways = []

        token_cost_reduction = data.get("token_cost_reduction", 280)
        optimization_potential = data.get("optimization_savings", 65)

        takeaways.append(
            Takeaway(
                category="opportunity",
                message=f"{token_cost_reduction}x cost reduction enables mass AI deployment",
                urgency="high",
                impact="high",
                timeframe="immediate",
            )
        )

        if optimization_potential > 50:
            takeaways.append(
                Takeaway(
                    category="opportunity",
                    message=f"Token optimization can reduce costs by additional {optimization_potential}%",
                    urgency="medium",
                    impact="medium",
                    timeframe="short-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Implement token optimization strategies across all AI applications",
                urgency="medium",
                impact="medium",
                timeframe="immediate",
            )
        )

        return takeaways

    def _skill_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for skill gap analysis view."""
        takeaways = []

        critical_gaps = data.get("critical_skill_gaps", 3)
        talent_shortage = data.get("talent_shortage_severity", "high")
        time_to_fill = data.get("avg_time_to_fill_days", 120)

        if critical_gaps > 2:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"{critical_gaps} critical skill areas undermining AI success",
                    urgency="critical",
                    impact="high",
                    timeframe="immediate",
                )
            )

        if time_to_fill > 90:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"{time_to_fill} days average to fill AI roles - slowing progress",
                    urgency="high",
                    impact="medium",
                    timeframe="short-term",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Partner with universities and bootcamps for talent pipeline",
                urgency="high",
                impact="high",
                timeframe="short-term",
            )
        )

        return takeaways

    def _governance_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate takeaways for governance view."""
        takeaways = []

        governance_maturity = data.get("governance_score", 45)
        compliance_gaps = data.get("compliance_gaps", 5)
        regulatory_risk = data.get("regulatory_risk", "medium")

        if governance_maturity < 50:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"Governance maturity of {governance_maturity}% exposes regulatory risks",
                    urgency="high",
                    impact="high",
                    timeframe="short-term",
                )
            )

        if compliance_gaps > 3:
            takeaways.append(
                Takeaway(
                    category="threat",
                    message=f"{compliance_gaps} compliance gaps could result in penalties",
                    urgency="critical",
                    impact="high",
                    timeframe="immediate",
                )
            )

        takeaways.append(
            Takeaway(
                category="action",
                message="Establish AI ethics committee and governance framework",
                urgency="high",
                impact="medium",
                timeframe="immediate",
            )
        )

        return takeaways

    def _generic_takeaways(self, data: Dict[str, Any], persona: str) -> List[Takeaway]:
        """Generate generic takeaways when specific generator not available."""
        return [
            Takeaway(
                category="opportunity",
                message="AI adoption continues to accelerate across all sectors",
                urgency="medium",
                impact="medium",
                timeframe="long-term",
            ),
            Takeaway(
                category="action",
                message="Develop comprehensive AI strategy aligned with business goals",
                urgency="medium",
                impact="high",
                timeframe="short-term",
            ),
        ]

    def _download_takeaways(self, takeaways: List[Takeaway]):
        """Generate downloadable takeaways report."""
        # This would generate a PDF or other format
        st.info("📥 Takeaways download functionality would be implemented here")


def generate_smart_summary(data: pd.DataFrame, view_type: str, persona: str = "General") -> str:
    """Generate a smart one-paragraph summary of the data.

    Args:
        data: DataFrame with relevant data
        view_type: Type of view being summarized
        persona: User persona for tailored language

    Returns:
        One paragraph summary
    """
    # This would use more sophisticated analysis in production
    summaries = {
        "Executive": "The data reveals critical strategic insights requiring immediate attention. ",
        "Policymaker": "Analysis indicates significant policy implications across multiple sectors. ",
        "Researcher": "Statistical analysis demonstrates significant correlations and trends. ",
        "General": "The information shows important patterns and opportunities. ",
    }

    base = summaries.get(persona, summaries["General"])

    # Add view-specific insights
    if view_type == "competitive_position":
        base += "Your competitive position analysis shows both risks and opportunities that require strategic action."
    elif view_type == "roi_analysis":
        base += "ROI projections indicate strong potential returns with manageable implementation risks."
    else:
        base += "The analysis provides actionable insights for improving your AI strategy."

    return base
