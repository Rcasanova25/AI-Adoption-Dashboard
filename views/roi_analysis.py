"""ROI Analysis view module for AI Adoption Dashboard.

This module provides comprehensive ROI analysis visualizations including
investment returns, payback analysis, sector-specific ROI, and an
interactive ROI calculator.
"""

from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render(data: Dict[str, Any]) -> None:
    """Render the ROI Analysis view.

    Args:
        data: Dictionary containing required data:
            - sector_2025: Sector data including ROI metrics
            - a11y: Accessibility helper module
    """
    # Extract required data
    sector_2025 = data.get("sector_2025")
    a11y = data.get("a11y")

    st.write("💰 **ROI Analysis: Comprehensive Economic Impact**")

    # Create detailed ROI dashboard
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Investment Returns", "Payback Analysis", "Sector ROI", "ROI Calculator"]
    )

    with tab1:
        _render_investment_returns(a11y)

    with tab2:
        _render_payback_analysis(a11y)

    with tab3:
        _render_sector_roi(sector_2025, a11y)

    with tab4:
        _render_roi_calculator()


def _render_investment_returns(a11y: Any) -> None:
    """Render the investment returns tab."""
    # Investment returns visualization
    roi_data = pd.DataFrame(
        {
            "investment_level": [
                "Pilot (<$100K)",
                "Small ($100K-$500K)",
                "Medium ($500K-$2M)",
                "Large ($2M-$10M)",
                "Enterprise ($10M+)",
            ],
            "avg_roi": [1.8, 2.5, 3.2, 3.8, 4.5],
            "time_to_roi": [6, 9, 12, 18, 24],  # months
            "success_rate": [45, 58, 72, 81, 87],  # % of projects achieving positive ROI
        }
    )

    fig = go.Figure()

    # ROI bars
    fig.add_trace(
        go.Bar(
            name="Average ROI",
            x=roi_data["investment_level"],
            y=roi_data["avg_roi"],
            yaxis="y",
            marker_color="#2ECC71",
            text=[f"{x}x" for x in roi_data["avg_roi"]],
            textposition="outside",
        )
    )

    # Success rate line
    fig.add_trace(
        go.Scatter(
            name="Success Rate",
            x=roi_data["investment_level"],
            y=roi_data["success_rate"],
            yaxis="y2",
            mode="lines+markers",
            line=dict(width=3, color="#3498DB"),
            marker=dict(size=10),
        )
    )

    fig.update_layout(
        title="AI ROI by Investment Level",
        xaxis_title="Investment Level",
        yaxis=dict(title="Average ROI (x)", side="left"),
        yaxis2=dict(title="Success Rate (%)", side="right", overlaying="y"),
        height=400,
        hovermode="x unified",
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI ROI by Investment Level",
        description="A dual-axis chart showing the relationship between AI investment levels and returns. Green bars display average ROI multipliers on the left y-axis: Small investments (<$100K) yield 1.2x ROI, Medium ($100K-$1M) achieve 2.5x, Large ($1M-$10M) reach 3.8x, and Enterprise (>$10M) deliver 4.5x returns. A blue line shows success rates on the right y-axis, increasing from 45% for small investments to 58% for medium, 72% for large, and 85% for enterprise-level investments. The chart demonstrates that larger AI investments correlate with both higher returns and greater success rates, suggesting economies of scale and the importance of comprehensive AI strategies.",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        """
    **Key Insights:**
    - Larger investments show higher ROI and success rates
    - Enterprise projects (87% success) benefit from better resources and planning
    - Even small pilots can achieve 1.8x ROI with 45% success rate
    """
    )


def _render_payback_analysis(a11y: Any) -> None:
    """Render the payback analysis tab."""
    # Payback period analysis
    payback_data = pd.DataFrame(
        {
            "scenario": ["Best Case", "Typical", "Conservative"],
            "months": [8, 15, 24],
            "probability": [20, 60, 20],
        }
    )

    fig = go.Figure()

    # Create funnel chart for payback scenarios
    fig.add_trace(
        go.Funnel(
            y=payback_data["scenario"],
            x=payback_data["months"],
            textinfo="text+percent initial",
            text=[f"{x} months" for x in payback_data["months"]],
            marker=dict(color=["#2ECC71", "#F39C12", "#E74C3C"]),
        )
    )

    fig.update_layout(
        title="AI Investment Payback Period Distribution",
        xaxis_title="Months to Payback",
        height=350,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="AI Investment Payback Period Distribution",
        description="A funnel chart showing the distribution of AI investment payback periods across three scenarios. Best Case scenario (green, 20% probability) achieves payback in 8 months. Typical scenario (orange, 60% probability) reaches payback in 15 months. Conservative scenario (red, 20% probability) requires 24 months for payback. The visualization shows that most AI investments (60%) achieve payback within 15 months, with only 20% taking longer than 2 years, indicating generally favorable return timelines for well-executed AI initiatives.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Time to value breakdown
    st.subheader("⏱️ Time to Value by AI Capability")

    time_to_value = pd.DataFrame(
        {
            "capability": [
                "Process Automation",
                "Predictive Analytics",
                "Natural Language Processing",
                "Computer Vision",
                "Recommendation Systems",
                "GenAI Applications",
            ],
            "months_to_value": [3, 6, 9, 12, 6, 4],
            "complexity": [2, 3, 4, 5, 3, 2],  # 1-5 scale
        }
    )

    fig2 = px.bar(
        time_to_value,
        x="capability",
        y="months_to_value",
        color="complexity",
        color_continuous_scale="RdYlGn_r",
        title="Time to Value by AI Capability",
        labels={"months_to_value": "Months to Value", "complexity": "Implementation Complexity"},
    )

    fig2.update_traces(texttemplate="%{y} months", textposition="outside")
    fig2.update_layout(xaxis_tickangle=45, height=400)

    fig2 = a11y.make_chart_accessible(
        fig2,
        title="Time to Value by AI Capability",
        description="A bar chart showing time to value for different AI capabilities, colored by implementation complexity (1-5 scale, red=high, green=low). Process Automation delivers value in 3 months with low complexity (2). GenAI Applications show quick returns at 4 months with low complexity (2). Predictive Analytics and Recommendation Systems both achieve value in 6 months with medium complexity (3). Natural Language Processing requires 9 months with high complexity (4). Computer Vision has the longest time to value at 12 months with the highest complexity (5). The chart helps organizations prioritize AI initiatives based on speed of return and implementation difficulty.",
    )
    st.plotly_chart(fig2, use_container_width=True)


def _render_sector_roi(sector_2025: pd.DataFrame, a11y: Any) -> None:
    """Render the sector ROI tab."""
    # Sector-specific ROI analysis
    fig = go.Figure()

    # Create bubble chart
    fig.add_trace(
        go.Scatter(
            x=sector_2025["adoption_rate"],
            y=sector_2025["avg_roi"],
            mode="markers+text",
            marker=dict(
                size=sector_2025["genai_adoption"],
                color=sector_2025["avg_roi"],
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="ROI (x)"),
            ),
            text=sector_2025["sector"],
            textposition="top center",
            hovertemplate="<b>%{text}</b><br>Adoption: %{x}%<br>ROI: %{y}x<br>GenAI Adoption: %{marker.size}%<extra></extra>",
        )
    )

    # Add trend line
    z = np.polyfit(sector_2025["adoption_rate"], sector_2025["avg_roi"], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(
        sector_2025["adoption_rate"].min(), sector_2025["adoption_rate"].max(), 100
    )

    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=p(x_trend),
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Trend",
            showlegend=True,
        )
    )

    fig.update_layout(
        title="Sector AI Adoption vs ROI (Bubble Size = GenAI Adoption)",
        xaxis_title="Overall AI Adoption Rate (%)",
        yaxis_title="Average ROI (x)",
        height=500,
    )

    fig = a11y.make_chart_accessible(
        fig,
        title="Sector AI Adoption vs ROI",
        description="A bubble chart plotting AI adoption rates (x-axis) against average ROI (y-axis) across sectors, with bubble sizes representing GenAI adoption rates. Technology sector leads with 92% adoption and 4.2x ROI. Financial Services follows with 85% adoption and 3.8x ROI. Healthcare shows 78% adoption with 3.2x ROI. Manufacturing has 75% adoption and 3.5x ROI. Retail & E-commerce displays 72% adoption with 3.0x ROI. Education shows 65% adoption and 2.5x ROI. Energy & Utilities has 58% adoption with 2.8x ROI. Government trails with 52% adoption and 2.2x ROI. A red dashed trend line shows positive correlation between adoption and ROI. The visualization reveals that sectors with higher adoption rates generally achieve better returns, with technology and financial services leading both metrics.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ROI components breakdown
    st.subheader("💡 ROI Components by Sector")

    roi_components = pd.DataFrame(
        {
            "component": [
                "Cost Reduction",
                "Revenue Growth",
                "Productivity Gains",
                "Quality Improvement",
            ],
            "Technology": [25, 40, 20, 15],
            "Financial Services": [30, 35, 25, 10],
            "Healthcare": [20, 25, 30, 25],
            "Manufacturing": [35, 20, 25, 20],
        }
    )

    fig2 = go.Figure()

    for sector in ["Technology", "Financial Services", "Healthcare", "Manufacturing"]:
        fig2.add_trace(
            go.Bar(
                name=sector,
                x=roi_components["component"],
                y=roi_components[sector],
                text=[f"{x}%" for x in roi_components[sector]],
                textposition="outside",
            )
        )

    fig2.update_layout(
        title="ROI Component Contribution by Sector",
        xaxis_title="ROI Component",
        yaxis_title="Contribution to Total ROI (%)",
        barmode="group",
        height=400,
    )

    st.plotly_chart(fig2, use_container_width=True)


def _render_roi_calculator() -> None:
    """Render the ROI calculator tab."""
    st.subheader("🧮 Interactive AI ROI Calculator")

    st.info("Estimate your potential AI investment returns based on your specific parameters")

    col1, col2 = st.columns(2)

    with col1:
        investment = st.number_input(
            "Initial Investment ($)",
            min_value=10000,
            max_value=50000000,
            value=500000,
            step=50000,
            help="Total upfront AI investment including technology, talent, and implementation",
        )

        sector = st.selectbox(
            "Industry Sector",
            [
                "Technology",
                "Financial Services",
                "Healthcare",
                "Manufacturing",
                "Retail & E-commerce",
                "Education",
                "Energy & Utilities",
                "Government",
            ],
        )

        company_size = st.selectbox(
            "Company Size",
            [
                "Small (<250 employees)",
                "Medium (250-1000)",
                "Large (1000-5000)",
                "Enterprise (5000+)",
            ],
        )

    with col2:
        ai_maturity = st.slider(
            "Current AI Maturity Level",
            min_value=1,
            max_value=5,
            value=2,
            help="1=No AI experience, 5=Advanced AI capabilities",
        )

        implementation_quality = st.slider(
            "Implementation Quality Score",
            min_value=1,
            max_value=5,
            value=3,
            help="1=Basic implementation, 5=Best-in-class execution",
        )

        timeline = st.selectbox(
            "Implementation Timeline",
            ["3 months", "6 months", "12 months", "18 months", "24 months"],
        )

    # Additional factors
    st.subheader("Additional Factors")

    col3, col4 = st.columns(2)

    with col3:
        data_readiness = st.slider(
            "Data Readiness",
            min_value=1,
            max_value=5,
            value=3,
            help="1=Poor data quality, 5=Excellent data infrastructure",
        )

        talent_availability = st.checkbox("Access to AI talent", value=True)
        cloud_infrastructure = st.checkbox("Existing cloud infrastructure", value=True)

    with col4:
        use_case_clarity = st.slider(
            "Use Case Clarity",
            min_value=1,
            max_value=5,
            value=3,
            help="1=Unclear objectives, 5=Well-defined use cases",
        )

        executive_support = st.checkbox("Strong executive sponsorship", value=True)
        change_management = st.checkbox("Change management program", value=False)

    # Calculate ROI
    if st.button("Calculate ROI", type="primary"):
        # Base ROI by sector
        sector_roi = {
            "Technology": 4.2,
            "Financial Services": 3.8,
            "Healthcare": 3.2,
            "Manufacturing": 3.5,
            "Retail & E-commerce": 3.0,
            "Education": 2.5,
            "Energy & Utilities": 2.8,
            "Government": 2.2,
        }

        base_roi = sector_roi.get(sector, 3.0)

        # Adjust for various factors
        # Company size adjustment
        size_multiplier = {
            "Small (<250 employees)": 0.8,
            "Medium (250-1000)": 0.9,
            "Large (1000-5000)": 1.0,
            "Enterprise (5000+)": 1.1,
        }
        base_roi *= size_multiplier.get(company_size, 1.0)

        # Quality adjustments
        base_roi *= 0.8 + (implementation_quality * 0.1)
        base_roi *= 0.8 + (data_readiness * 0.08)
        base_roi *= 0.8 + (use_case_clarity * 0.08)
        base_roi *= 0.9 + (ai_maturity * 0.05)

        # Boolean adjustments
        if talent_availability:
            base_roi *= 1.1
        if cloud_infrastructure:
            base_roi *= 1.05
        if executive_support:
            base_roi *= 1.15
        if change_management:
            base_roi *= 1.1

        # Timeline adjustment
        timeline_factor = {
            "3 months": 0.7,
            "6 months": 0.85,
            "12 months": 1.0,
            "18 months": 1.1,
            "24 months": 1.2,
        }
        timeline_months = int(timeline.split()[0])
        base_roi *= timeline_factor.get(timeline, 1.0)

        # Add some randomness to simulate uncertainty
        uncertainty = np.random.normal(1.0, 0.1)
        final_roi = max(0.5, base_roi * uncertainty)

        # Calculate returns
        expected_return = investment * final_roi
        net_benefit = expected_return - investment
        annual_return = (final_roi - 1) * 100
        payback_months = int(timeline_months / final_roi) if final_roi > 1 else 999

        # Display results
        st.success("**ROI Calculation Complete!**")

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric("Expected ROI", f"{final_roi:.1f}x", f"{annual_return:.0f}% return")
        with col6:
            st.metric("Total Return", f"${expected_return:,.0f}")
        with col7:
            st.metric("Net Benefit", f"${net_benefit:,.0f}")
        with col8:
            st.metric(
                "Payback Period", f"{payback_months} months" if payback_months < 999 else "N/A"
            )

        # Risk assessment
        risk_score = 5 - (implementation_quality + data_readiness + use_case_clarity) / 3
        risk_level = "Low" if risk_score < 2 else "Medium" if risk_score < 3.5 else "High"

        st.warning(
            f"**Risk Assessment:** {risk_level} risk project based on implementation factors"
        )

        # Recommendations
        st.subheader("📋 Recommendations")

        recommendations = []
        if data_readiness < 4:
            recommendations.append("• Invest in data quality and infrastructure improvements")
        if not talent_availability:
            recommendations.append("• Develop AI talent acquisition or training programs")
        if use_case_clarity < 4:
            recommendations.append("• Conduct thorough use case discovery workshops")
        if not change_management:
            recommendations.append("• Implement comprehensive change management program")
        if implementation_quality < 4:
            recommendations.append("• Partner with experienced AI implementation vendors")

        if recommendations:
            st.markdown("**To improve ROI potential:**")
            for rec in recommendations:
                st.markdown(rec)
        else:
            st.markdown("**Strong foundation in place!** Focus on execution excellence.")

        # Export analysis
        analysis_text = f"""
        AI ROI Analysis Report
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Investment Parameters:
        - Initial Investment: ${investment:,.0f}
        - Sector: {sector}
        - Company Size: {company_size}
        - Timeline: {timeline}
        
        Quality Metrics:
        - Implementation Quality: {implementation_quality}/5
        - Data Readiness: {data_readiness}/5
        
        Projected Results:
        - Expected ROI: {final_roi:.1f}x
        - Total Return: ${expected_return:,.0f}
        - Net Benefit: ${net_benefit:,.0f}
        - Payback Period: {payback_months} months
        - Risk Level: {risk_level}
        """

        st.download_button(
            label="Download Analysis",
            data=analysis_text,
            file_name=f"ai_roi_analysis_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )
