"""Competitive Assessment view for AI Adoption Dashboard."""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from components.competitive_assessor import CompetitiveAssessor
from components.economic_insights import EconomicInsights


def render(data: Dict[str, pd.DataFrame]) -> None:
    """Render the competitive assessment view.
    
    Args:
        data: Dictionary of dataframes needed by this view
    """
    try:
        # Initialize competitive assessor
        assessor = CompetitiveAssessor()
        
        # Display competitive assessment interface
        st.markdown("### 🎯 AI Competitive Position Assessment")
        st.markdown("Evaluate your organization's AI readiness and competitive position in the market.")
        
        # Render the main assessment interface
        assessor.render_assessment_interface()
        
        # Add economic insights
        EconomicInsights.display_executive_summary(
            title="Strategic AI Assessment Summary",
            key_points=[
                "78% of organizations report some AI use in 2025, up from 55% in 2023",
                "GenAI adoption doubled from 33% to 71% in just two years",
                "AI inference costs dropped 280x since November 2022",
                "Organizations with comprehensive AI strategies show 4.2x better ROI"
            ],
            recommendations=[
                "Complete competitive assessment to identify gaps and opportunities",
                "Develop comprehensive AI strategy aligned with business objectives",
                "Invest in employee training and change management",
                "Start with high-impact, low-complexity use cases"
            ],
            urgency="high"
        )
        
    except Exception as e:
        st.error(f"Error rendering competitive assessment view: {str(e)}")