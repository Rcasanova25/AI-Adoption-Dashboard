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

from business.roi_analysis import (
    compute_roi,
    compute_comprehensive_roi,
    analyze_roi_by_company_size
)
from data.services import get_data_service, show_data_error


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

    # Data presence checks
    missing = []
    if sector_2025 is None or (hasattr(sector_2025, "empty") and sector_2025.empty):
        missing.append("sector_2025")
    if a11y is None:
        missing.append("a11y")
    if missing:
        st.error(
            f"Missing or empty data for: {', '.join(missing)}. Please check your data sources or contact support."
        )
        return

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
        _render_roi_calculator(a11y)


def _render_investment_returns(a11y: Any) -> None:
    """Render the investment returns tab."""
    # Load ROI data from actual data source
    try:
        data_service = get_data_service()
        roi_data = data_service.get_required_data("roi_analysis", "roi_data")
    except ValueError as e:
        show_data_error(
            str(e),
            recovery_suggestions=[
                "Ensure McKinsey data PDF is available",
                "Check that ROI metrics were extracted successfully",
                "Verify data mapping configuration"
            ]
        )
        roi_data = pd.DataFrame()

    fig = go.Figure()

    if not roi_data.empty:
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
    else:
        # Show placeholder when no data available
        fig.add_annotation(
            text="ROI data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
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
        description="A dual-axis chart showing the relationship between AI investment levels and returns. Green bars display average ROI multipliers on the left y-axis: Small investments (<$100K) yield 1.8x ROI, Medium ($100K-$500K) achieve 2.5x, Large ($500K-$2M) reach 3.2x, Enterprise ($2M-$10M) deliver 3.8x, and Enterprise ($10M+) deliver 4.5x returns. A blue line shows success rates on the right y-axis, increasing from 45% for small investments to 87% for enterprise-level investments. The chart demonstrates that larger AI investments correlate with both higher returns and greater success rates.",
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
    # Load payback data from actual data source
    try:
        data_service = get_data_service()
        payback_data = data_service.get_required_data("roi_analysis", "payback_data")
    except ValueError as e:
        show_data_error(
            str(e),
            recovery_suggestions=[
                "Ensure McKinsey data PDF is available",
                "Check that payback scenarios were extracted",
                "Verify data mapping configuration"
            ]
        )
        payback_data = pd.DataFrame()

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
        description="A funnel chart showing the distribution of AI investment payback periods across three scenarios. Best Case scenario (green, 20% probability) achieves payback in 8 months. Typical scenario (orange, 60% probability) reaches payback in 15 months. Conservative scenario (red, 20% probability) requires 24 months for payback. The visualization shows that most AI investments (60%) achieve payback within 15 months, with only 20% taking longer than 2 years.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Time to value breakdown
    st.subheader("⏱️ Time to Value by AI Capability")

    # Load time to value data from actual data source
    try:
        data_service = get_data_service()
        time_to_value = data_service.get_required_data("roi_analysis", "time_to_value")
    except ValueError as e:
        show_data_error(
            str(e),
            recovery_suggestions=[
                "Ensure McKinsey data PDF is available",
                "Check that time to value metrics were extracted",
                "Verify data mapping configuration"
            ]
        )
        time_to_value = pd.DataFrame()

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
        description="A bar chart showing time to value for different AI capabilities, colored by implementation complexity (1-5 scale, red=high, green=low). Process Automation delivers value in 3 months with low complexity (2). GenAI Applications show quick returns at 4 months with low complexity (2). Predictive Analytics and Recommendation Systems both achieve value in 6 months with medium complexity (3). Natural Language Processing requires 9 months with high complexity (4). Computer Vision has the longest time to value at 12 months with the highest complexity (5).",
    )
    st.plotly_chart(fig2, use_container_width=True)


def _render_sector_roi(sector_2025: pd.DataFrame, a11y: Any) -> None:
    """Render the sector ROI tab."""
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
        description="A bubble chart plotting AI adoption rates (x-axis) against average ROI (y-axis) across sectors, with bubble sizes representing GenAI adoption rates. Technology sector leads with 92% adoption and 4.2x ROI. Financial Services follows with 85% adoption and 3.8x ROI. Healthcare shows 78% adoption with 3.2x ROI. Manufacturing has 75% adoption and 3.5x ROI. Retail & E-commerce displays 72% adoption with 3.0x ROI. Education shows 65% adoption and 2.5x ROI. Energy & Utilities has 58% adoption with 2.8x ROI. Government trails with 52% adoption and 2.2x ROI. A red dashed trend line shows positive correlation between adoption and ROI.",
    )
    st.plotly_chart(fig, use_container_width=True)

    # ROI components breakdown
    st.subheader("💡 ROI Components by Sector")

    # Load ROI components data from actual data source
    try:
        data_service = get_data_service()
        roi_components = data_service.get_required_data("roi_analysis", "roi_components")
    except ValueError as e:
        show_data_error(
            str(e),
            recovery_suggestions=[
                "Ensure McKinsey data PDF is available",
                "Check that ROI components by sector were extracted",
                "Verify data mapping configuration"
            ]
        )
        roi_components = pd.DataFrame()

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


def _render_roi_calculator(a11y: Any) -> None:
    """Render the enhanced ROI calculator tab with comprehensive financial analysis."""
    st.subheader("🧮 Advanced AI ROI Calculator")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Investment Parameters")
        initial_investment = st.number_input(
            "Initial Investment ($)", 
            min_value=10000.0, 
            max_value=50000000.0,
            value=500000.0,
            step=10000.0,
            help="One-time implementation cost including software, hardware, and setup"
        )
        
        years = st.slider(
            "Analysis Period (years)", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="Number of years to analyze ROI"
        )
        
        annual_revenue_increase = st.number_input(
            "Annual Revenue Increase ($)",
            min_value=0.0,
            value=200000.0,
            step=10000.0,
            help="Expected additional revenue from AI implementation"
        )
        
        annual_cost_savings = st.number_input(
            "Annual Cost Savings ($)",
            min_value=0.0,
            value=150000.0,
            step=10000.0,
            help="Expected cost reductions from efficiency gains"
        )
        
        annual_operating_cost = st.number_input(
            "Annual Operating Cost ($)",
            min_value=0.0,
            value=50000.0,
            step=5000.0,
            help="Ongoing costs for licenses, maintenance, support"
        )
        
    with col2:
        st.markdown("### Risk & Context Parameters")
        risk_level = st.selectbox(
            "Risk Level", 
            ["Low", "Medium", "High", "Very High"], 
            index=1,
            help="Implementation complexity and uncertainty level"
        )
        
        company_size = st.selectbox(
            "Company Size",
            ["Small", "Medium", "Large", "Enterprise"],
            index=1,
            help="Used for benchmark comparisons"
        )
        
        ai_use_case = st.selectbox(
            "Primary Use Case",
            ["Process Automation", "Customer Service", "Predictive Analytics", 
             "Supply Chain", "Marketing Personalization", "Fraud Detection", 
             "Quality Control"],
            help="Main AI application area"
        )
        
        discount_rate = st.slider(
            "Discount Rate (%)",
            min_value=5.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            help="Cost of capital for NPV calculation"
        ) / 100
        
        # Productivity impact section
        st.markdown("### Productivity Impact (Optional)")
        include_productivity = st.checkbox("Include productivity analysis")
        
        if include_productivity:
            num_employees = st.number_input(
                "Number of Affected Employees",
                min_value=1,
                value=50,
                help="Employees who will use the AI system"
            )
            avg_salary = st.number_input(
                "Average Annual Salary ($)",
                min_value=20000.0,
                value=75000.0,
                step=5000.0
            )
            productivity_gain = st.slider(
                "Productivity Gain (%)",
                min_value=5.0,
                max_value=50.0,
                value=20.0,
                step=5.0
            ) / 100
        else:
            num_employees = None
            avg_salary = None
            productivity_gain = None
    
    # Calculate button
    if st.button("Calculate Comprehensive ROI", type="primary", use_container_width=True):
        # Prepare cash flows
        annual_net_benefit = annual_revenue_increase + annual_cost_savings - annual_operating_cost
        annual_cash_flows = [annual_net_benefit] * years
        annual_operating_costs = [annual_operating_cost] * years
        
        # Compute comprehensive ROI
        results = compute_comprehensive_roi(
            initial_investment=initial_investment,
            annual_cash_flows=annual_cash_flows,
            annual_operating_costs=annual_operating_costs,
            risk_level=risk_level,
            discount_rate=discount_rate,
            num_employees=num_employees,
            avg_salary=avg_salary,
            productivity_gain_pct=productivity_gain
        )
        
        # Get company size benchmarks
        benchmarks = analyze_roi_by_company_size(company_size, ai_use_case)
        
        # Display results in tabs
        result_tabs = st.tabs(["📊 Financial Metrics", "💰 TCO Analysis", "⚠️ Risk Analysis", 
                               "👥 Productivity Impact", "📈 Benchmarks", "✅ Decision"])
        
        with result_tabs[0]:
            st.markdown("### Core Financial Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                npv = results['financial_metrics']['npv']
                st.metric(
                    "Net Present Value",
                    f"${npv:,.0f}",
                    delta="Positive" if npv > 0 else "Negative",
                    delta_color="normal" if npv > 0 else "inverse"
                )
                
            with col2:
                irr = results['financial_metrics']['irr']
                if irr:
                    st.metric(
                        "Internal Rate of Return",
                        f"{irr*100:.1f}%",
                        delta=f"{(irr-discount_rate)*100:.1f}pp vs hurdle",
                        delta_color="normal" if irr > discount_rate else "inverse"
                    )
                else:
                    st.metric("IRR", "N/A", help="IRR cannot be calculated")
                    
            with col3:
                roi = results['financial_metrics']['simple_roi_pct']
                st.metric(
                    "Simple ROI",
                    f"{roi:.1f}%",
                    delta="Profitable" if roi > 0 else "Loss"
                )
                
            with col4:
                payback = results['financial_metrics']['payback_years']
                if payback:
                    st.metric(
                        "Payback Period",
                        f"{payback:.1f} years",
                        delta=f"{payback*12:.0f} months"
                    )
                else:
                    st.metric("Payback", "Never")
                    
        with result_tabs[1]:
            st.markdown("### Total Cost of Ownership")
            
            tco = results['tco_analysis']
            
            # Create TCO breakdown chart
            tco_data = pd.DataFrame({
                'Cost Component': ['Initial', 'Operating', 'Maintenance'],
                'Amount': [tco['initial_cost'], tco['operating_costs'], tco['maintenance_costs']]
            })
            
            fig_tco = px.pie(
                tco_data, 
                values='Amount', 
                names='Cost Component',
                title=f"TCO Breakdown (Total: ${tco['total_tco']:,.0f})"
            )
            st.plotly_chart(fig_tco, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total TCO", f"${tco['total_tco']:,.0f}")
                st.metric("Annual TCO", f"${tco['annual_tco']:,.0f}")
            with col2:
                st.metric("Operating Costs (PV)", f"${tco['operating_costs']:,.0f}")
                st.metric("Maintenance Costs (PV)", f"${tco['maintenance_costs']:,.0f}")
                
        with result_tabs[2]:
            st.markdown("### Risk-Adjusted Analysis")
            
            risk = results['risk_analysis']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Expected Return", f"{risk['expected_return']*100:.1f}%")
                st.metric("Required Return", f"{risk['required_return']*100:.1f}%")
                st.metric("Risk Premium", f"{risk['risk_premium']*100:.1f}%")
            with col2:
                st.metric("Risk-Adjusted Return", f"{risk['risk_adjusted_return']*100:.1f}%")
                st.metric("Sharpe Ratio", f"{risk['sharpe_ratio']:.2f}")
                
                if risk['meets_threshold']:
                    st.success("✅ Meets risk-adjusted return threshold")
                else:
                    st.error("❌ Below risk-adjusted return threshold")
                    
        with result_tabs[3]:
            if results['productivity_analysis']:
                st.markdown("### Productivity Impact Analysis")
                
                prod = results['productivity_analysis']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Annual Productivity Value", f"${prod['annual_productivity_value']:,.0f}")
                    st.metric("Total Benefit", f"${prod['total_benefit']:,.0f}")
                    st.metric("Benefit/Cost Ratio", f"{prod['benefit_cost_ratio']:.2f}x")
                with col2:
                    st.metric("Productivity ROI", f"{prod['simple_roi_pct']:.1f}%")
                    st.metric("Productivity NPV", f"${prod['npv']:,.0f}")
                    if prod['payback_years']:
                        st.metric("Productivity Payback", f"{prod['payback_years']:.1f} years")
            else:
                st.info("Enable productivity analysis above to see workforce impact metrics")
                
        with result_tabs[4]:
            st.markdown("### Industry Benchmarks")
            
            st.write(benchmarks['recommendation'])
            
            # Comparison metrics
            col1, col2 = st.columns(2)
            with col1:
                expected_low, expected_high = benchmarks['expected_roi_range']
                st.metric(
                    "Industry ROI Range",
                    f"{expected_low:.0f}% - {expected_high:.0f}%",
                    delta=f"Your ROI: {roi:.1f}%"
                )
                
                st.metric(
                    "Typical Investment",
                    f"${benchmarks['investment_range'][0]:,.0f} - ${benchmarks['investment_range'][1]:,.0f}",
                    delta=f"Your Investment: ${initial_investment:,.0f}"
                )
                
            with col2:
                st.metric(
                    "Success Probability",
                    f"{benchmarks['success_probability']*100:.0f}%",
                    help="Based on company size and use case"
                )
                
                st.metric(
                    "Expected Payback",
                    f"{benchmarks['typical_payback_months']} months",
                    delta=f"Your estimate: {payback*12:.0f} months" if payback else "N/A"
                )
                
            # Risk factors
            st.markdown("#### Key Risk Factors for Your Profile")
            for risk in benchmarks['key_risks']:
                st.write(f"• {risk}")
                
        with result_tabs[5]:
            st.markdown("### 🎯 Investment Decision Summary")
            
            decision = results['investment_decision']
            
            # Overall recommendation
            if decision['recommended']:
                st.success("### ✅ RECOMMENDED: Proceed with Investment")
                st.balloons()
            else:
                st.error("### ❌ NOT RECOMMENDED: Reconsider Investment")
                
            # Decision criteria breakdown
            st.markdown("#### Decision Criteria Analysis")
            
            criteria = {
                "NPV Positive": decision['npv_positive'],
                "IRR Exceeds Hurdle Rate": decision['irr_exceeds_hurdle'],
                "Risk-Adjusted Returns Acceptable": decision['risk_acceptable']
            }
            
            for criterion, passed in criteria.items():
                if passed:
                    st.write(f"✅ {criterion}")
                else:
                    st.write(f"❌ {criterion}")
                    
            # Additional insights
            st.markdown("#### Key Insights")
            
            if npv > 0:
                st.write(f"• Project adds ${npv:,.0f} in value after accounting for time value of money")
            else:
                st.write(f"• Project destroys ${-npv:,.0f} in value - costs exceed benefits")
                
            if irr and irr > 0.15:
                st.write(f"• Strong {irr*100:.1f}% return significantly exceeds typical hurdle rates")
            elif irr and irr > discount_rate:
                st.write(f"• Acceptable {irr*100:.1f}% return exceeds your {discount_rate*100:.1f}% hurdle rate")
            elif irr:
                st.write(f"• Weak {irr*100:.1f}% return below your {discount_rate*100:.1f}% hurdle rate")
                
            if payback and payback < 2:
                st.write(f"• Fast payback in {payback:.1f} years reduces implementation risk")
            elif payback and payback < 3:
                st.write(f"• Reasonable payback in {payback:.1f} years")
            elif payback:
                st.write(f"• Slow payback of {payback:.1f} years increases risk")
