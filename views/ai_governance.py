"""AI Governance view module for AI Adoption Dashboard.

This module provides visualizations for AI governance and ethics implementation,
showing adoption rates and maturity levels across different governance aspects.
"""

from typing import Any, Dict

import plotly.graph_objects as go
import streamlit as st

from business.policy_simulation import simulate_policy_impact
from data.models.governance import GovernanceMetrics, PolicyFramework


def render(data: Dict[str, Any]) -> None:
    """Render the AI Governance view.

    Args:
        data: Dictionary containing required data:
            - ai_governance: Data on governance aspects, adoption rates, and maturity
            - a11y: Accessibility helper module
    """
    # Extract required data
    ai_governance = data.get("ai_governance")
    a11y = data.get("a11y")

    # Data presence checks
    missing = []
    if ai_governance is None or (hasattr(ai_governance, "empty") and ai_governance.empty):
        missing.append("ai_governance")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

    st.write("⚖️ **AI Governance & Ethics Implementation**")

    # Governance maturity visualization
    fig = go.Figure()

    # Create radar chart for maturity
    categories = ai_governance["aspect"].tolist()

    fig.add_trace(
        go.Scatterpolar(
            r=ai_governance["adoption_rate"],
            theta=categories,
            fill="toself",
            name="Adoption Rate (%)",
            line_color="#3498DB",
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=[x * 20 for x in ai_governance["maturity_score"]],  # Scale to 100
            theta=categories,
            fill="toself",
            name="Maturity Score (scaled)",
            line_color="#E74C3C",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="AI Governance Implementation and Maturity",
        height=500,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Governance Implementation and Maturity",
        description=(
            "A radar chart displaying AI governance aspects across six dimensions, with two overlapping polygons "
            "showing adoption rates (blue) and maturity scores (red, scaled to 100). Data Privacy leads with 78% "
            "adoption and 76 maturity score (3.8/5). Regulatory Compliance follows with 72% adoption and 70 maturity "
            "(3.5/5). Ethics Guidelines shows 62% adoption and 64 maturity (3.2/5). Transparency has 52% adoption and "
            "56 maturity (2.8/5). Accountability Framework shows 48% adoption and 52 maturity (2.6/5). Bias Detection "
            "lags with only 45% adoption and 50 maturity (2.5/5). The chart reveals that while traditional compliance "
            "areas are well-established, emerging AI-specific governance areas like bias detection and accountability "
            "need significant improvement."
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Governance insights
    col1, col2 = st.columns(2)

    with col1:
        st.write("✅ **Well-Established Areas:**")
        st.write("• **Data Privacy:** 78% adoption, 3.8/5 maturity")
        st.write("• **Regulatory Compliance:** 72% adoption, 3.5/5 maturity")
        st.write("• **Ethics Guidelines:** 62% adoption, 3.2/5 maturity")

    with col2:
        st.write("⚠️ **Areas Needing Attention:**")
        st.write("• **Bias Detection:** Only 45% adoption, 2.5/5 maturity")
        st.write("• **Accountability Framework:** 48% adoption, 2.6/5 maturity")
        st.write("• **Transparency:** 52% adoption, 2.8/5 maturity")

    # Example: Allow user to select policy scenarios
    if not data or "policy_frameworks" not in data:
        raise ValueError("Missing required real, validated data for policy frameworks.")
    policies = data["policy_frameworks"]
    if not policies:
        raise ValueError("No policy frameworks provided in real data.")
    if "governance_metrics" not in data or not data["governance_metrics"]:
        raise ValueError("Missing required real, validated data for governance metrics.")
    base_metrics = data["governance_metrics"]
    simulated = simulate_policy_impact(base_metrics, policies)
    st.info(
        f"Simulated Maturity Score: {simulated.maturity_score}, Compliance: {simulated.compliance_status}"
    )
