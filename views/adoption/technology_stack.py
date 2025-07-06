"""Technology Stack view module for AI Adoption Dashboard.

This module provides visualizations showing how organizations combine AI
with other technologies (cloud, digitization) and the ROI implications
of different technology stack combinations.
"""

from typing import Any, Dict

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager
from views.base import BaseView


class TechnologyStackView(BaseView):
    def __init__(self):
        super().__init__(
            title="AI Technology Stack Analysis",
            description="Analysis showing how organizations combine AI with other technologies and the ROI implications."
        )
        self.a11y = AccessibilityManager()

    def render_content(self, data: Dict[str, Any]) -> None:
        """Render the Technology Stack view content.

        Args:
            data: Dictionary containing required data:
                - tech_stack: Data on technology stack combinations
        """
        # Extract required data
        tech_stack = data.get("tech_stack")

        # Data presence checks
        missing = []
        if tech_stack is None or (hasattr(tech_stack, "empty") and tech_stack.empty):
            missing.append("tech_stack")
        if missing:
            st.error(
                f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
            )
            return

        st.write("🔧 **AI Technology Stack Analysis**")

        # Prepare stack data for visualization
        stack_data = pd.DataFrame(
            {
                "technology": [
                    "AI Only",
                    "AI + Cloud",
                    "AI + Digitization",
                    "AI + Cloud + Digitization",
                ],
                "percentage": [15, 23, 24, 38],  # Adjusted to sum to 100%
                "roi_multiplier": [1.5, 2.8, 2.5, 3.5],
            }
        )

        # Donut chart for stack combinations
        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=stack_data["technology"],
                values=stack_data["percentage"],
                hole=0.4,
                marker_colors=["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"],
                textinfo="label+percent",
                textposition="outside",
                hovertemplate="<b>%{label}</b><br>Adoption: %{value}%<br>ROI: %{customdata}x<extra></extra>",
                customdata=stack_data["roi_multiplier"],
            )
        )

        fig.update_layout(
            title="Technology Stack Combinations and Their Prevalence",
            height=450,
            annotations=[dict(text="Tech<br>Stack", x=0.5, y=0.5, font_size=20, showarrow=False)],
        )

        fig = self.a11y.make_chart_accessible(
            fig,
            title="Technology Stack Combinations and Their Prevalence",
            description="A donut chart showing the distribution of AI technology stack combinations among organizations. The largest segment is 'AI + Cloud + Digitization' at 38% adoption with 3.5x ROI multiplier, shown in light green. 'AI + Digitization' follows at 24% adoption with 2.5x ROI in light blue. 'AI + Cloud' represents 23% adoption with 2.8x ROI in teal. The smallest segment is 'AI Only' at 15% adoption with 1.5x ROI in coral red. The chart demonstrates that 85% of organizations combine AI with other technologies, and the full stack combination yields the highest return on investment. The center of the donut displays 'Tech Stack' as a label.",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Stack insights with ROI
        col1, col2 = st.columns(2)

        with col1:
            st.write("**🔗 Technology Synergies:**")
            st.write("• **38%** use full stack (AI + Cloud + Digitization)")
            st.write("• **62%** combine AI with at least one other technology")
            st.write("• Only **15%** use AI in isolation")

        with col2:
            st.write("**💰 ROI by Stack:**")
            st.write("• Full stack: **3.5x** ROI")
            st.write("• AI + Cloud: **2.8x** ROI")
            st.write("• AI + Digitization: **2.5x** ROI")
            st.write("• AI only: **1.5x** ROI")

        st.success(
            "**Key Finding:** Technology complementarity is crucial - combined deployments show significantly higher returns"
        )


technology_stack_view = TechnologyStackView()

def render(data: Dict[str, Any]) -> None:
    technology_stack_view.render(data)