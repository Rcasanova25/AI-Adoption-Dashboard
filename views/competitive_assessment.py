"""Competitive Assessment view for AI Adoption Dashboard."""

from typing import Any, Dict

import pandas as pd
import streamlit as st

from components.competitive_assessor import CompetitivePositionAssessor
from components.economic_insights import EconomicInsights


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the competitive assessment view.

    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Initialize competitive assessor
        sector_data = data.get("sector_adoption")
        firm_size_data = data.get("firm_size_adoption")
        adoption_trends = data.get("adoption_metrics")
        investment_data = data.get("investment_trends")

        if (
            sector_data is None or sector_data.empty or
            firm_size_data is None or firm_size_data.empty or
            adoption_trends is None or adoption_trends.empty or
            investment_data is None or investment_data.empty
        ):
            st.error("Required competitive assessment data is missing or empty. Please check data sources.")
            st.stop()

        assessor = CompetitivePositionAssessor(
            sector_data=sector_data,
            firm_size_data=firm_size_data,
            adoption_trends=adoption_trends,
            investment_data=investment_data
        )

        # Display competitive assessment interface
        st.markdown("### 🎯 AI Competitive Position Assessment")
        st.markdown(
            "Evaluate your organization's AI readiness and competitive position in the market."
        )

        # Render the main assessment interface
        assessor.render()

        # Add economic insights
        EconomicInsights.display_executive_summary(
            title="Strategic AI Assessment Summary",
            key_points=[
                "78% of organizations report some AI use in 2025, up from 55% in 2023",
                "GenAI adoption doubled from 33% to 71% in just two years",
                "AI inference costs dropped 280x since November 2022",
                "Organizations with comprehensive AI strategies show 4.2x better ROI",
            ],
            recommendations=[
                "Complete competitive assessment to identify gaps and opportunities",
                "Develop comprehensive AI strategy aligned with business objectives",
                "Invest in employee training and change management",
                "Start with high-impact, low-complexity use cases",
            ],
            urgency="high",
        )

    except Exception as e:
        st.error(f"Error rendering competitive assessment view: {str(e)}")
