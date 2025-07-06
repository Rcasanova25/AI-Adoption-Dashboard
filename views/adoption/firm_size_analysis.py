"""Firm Size Analysis view module for AI Adoption Dashboard.

This module provides visualizations showing the correlation between firm size
(number of employees) and AI adoption rates, highlighting the adoption gap
between small and large enterprises.
"""

from typing import Any, Dict

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from components.accessibility import AccessibilityManager
from views.base import BaseView


class FirmSizeAnalysisView(BaseView):
    def __init__(self):
        super().__init__(
            title="AI Adoption by Firm Size",
            description="Analysis showing the correlation between firm size (number of employees) and AI adoption rates."
        )
        self.a11y = AccessibilityManager()

    def render_content(self, data: Dict[str, Any]) -> None:
        """Render the Firm Size Analysis view content.

        Args:
            data: Dictionary containing required data:
                - firm_size: Data on adoption rates by firm size
        """
        # Extract required data
        firm_size = data.get("firm_size")

        # Data presence checks
        missing = []
        if firm_size is None or (hasattr(firm_size, "empty") and firm_size.empty):
            missing.append("firm_size")
        if missing:
            st.error(
                f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
            )
            return

        st.write("🏢 **AI Adoption by Firm Size**")

        # Enhanced visualization with annotations
        fig = go.Figure()

        # Main bar chart
        fig.add_trace(
            go.Bar(
                x=firm_size["size"],
                y=firm_size["adoption"],
                marker_color=firm_size["adoption"],
                marker_colorscale="Greens",
                text=[f"{x}%" for x in firm_size["adoption"]],
                textposition="outside",
                hovertemplate="Size: %{x}<br>Adoption: %{y}%<br>Employees: %{customdata}<extra></extra>",
                customdata=firm_size["size"],
            )
        )

        # Add trend line
        x_numeric = list(range(len(firm_size)))
        z = np.polyfit(x_numeric, firm_size["adoption"], 2)
        p = np.poly1d(z)

        fig.add_trace(
            go.Scatter(
                x=firm_size["size"],
                y=p(x_numeric),
                mode="lines",
                line=dict(width=3, color="red", dash="dash"),
                name="Trend",
                showlegend=True,
            )
        )

        # Add annotations for key thresholds
        fig.add_annotation(
            x="100-249",
            y=12.5,
            text="<b>SME Threshold</b><br>12.5% adoption",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
        )

        fig.add_annotation(
            x="5000+",
            y=58.5,
            text="<b>Enterprise Leaders</b><br>58.5% adoption",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
        )

        fig.update_layout(
            title="AI Adoption Shows Strong Correlation with Firm Size",
            xaxis_title="Number of Employees",
            yaxis_title="AI Adoption Rate (%)",
            height=500,
            showlegend=True,
        )

        fig = self.a11y.make_chart_accessible(
            fig,
            title="AI Adoption Shows Strong Correlation with Firm Size",
            description=(
                "A bar chart with trend line showing AI adoption rates by company size, using a green color gradient. "
                "The x-axis shows employee count ranges from smallest (1-4 employees) to largest (5000+ employees). "
                "Adoption rates increase dramatically with firm size: 3.2% for 1-4 employees, 5.8% for 5-9, 8.5% for 10-19, "
                "11.2% for 20-49, 12.5% for 50-99, 15.3% for 100-249, 22.8% for 250-499, 31.5% for 500-999, "
                "42.7% for 1000-2499, 48.6% for 2500-4999, and 58.5% for 5000+ employees. "
                "A red dashed polynomial trend line emphasizes the exponential relationship. "
                "Key annotations highlight the SME threshold at 12.5% adoption (100-249 employees) and enterprise leaders at 58.5% (5000+ employees), "
                "showing an 18x gap between the smallest and largest firms."
            ),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Size insights
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Size Gap", "18x", "5000+ vs 1-4 employees")
        with col2:
            st.metric("SME Adoption", "<20%", "For firms <250 employees")
        with col3:
            st.metric("Enterprise Adoption", ">40%", "For firms >2500 employees")

        st.info(
            """
            **📈 Key Insights:**
            - Strong exponential relationship between size and adoption
            - Resource constraints limit small firm adoption
            - Enterprises benefit from economies of scale in AI deployment
            """
        )


firm_size_analysis_view = FirmSizeAnalysisView()

def render(data: Dict[str, Any]) -> None:
    firm_size_analysis_view.render(data)