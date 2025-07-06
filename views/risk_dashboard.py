"""Risk Dashboard view for AI Adoption Dashboard.

This module provides comprehensive risk analysis and visualization
for AI implementation projects, including risk matrices, mitigation
strategies, and portfolio-level risk assessment.
"""

from typing import Any, Dict, List
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from business.financial_calculations import calculate_risk_adjusted_return
from data.services import get_data_service, show_data_error


def render(data: Dict[str, Any]) -> None:
    """Render the Risk Dashboard view."""
    
    st.header("⚠️ AI Implementation Risk Dashboard")
    st.markdown(
        "Comprehensive risk assessment and management for AI initiatives, "
        "including technical, organizational, and financial risk factors."
    )
    
    # Create tabs for different risk analyses
    tabs = st.tabs([
        "🎯 Risk Matrix",
        "📊 Risk by Category", 
        "🛡️ Mitigation Strategies",
        "💼 Portfolio Risk",
        "📈 Risk-Return Analysis"
    ])
    
    with tabs[0]:
        _render_risk_matrix(data)
        
    with tabs[1]:
        _render_risk_categories(data)
        
    with tabs[2]:
        _render_mitigation_strategies(data)
        
    with tabs[3]:
        _render_portfolio_risk(data)
        
    with tabs[4]:
        _render_risk_return_analysis(data)


def _render_risk_matrix(data: Dict[str, Any]) -> None:
    """Render risk matrix visualization."""
    
    st.subheader("🎯 AI Implementation Risk Matrix")
    
    # Load risk data from data service
    try:
        data_service = get_data_service()
        risk_data = data_service.get_required_data("risk_assessment", "implementation_risks")
    except ValueError as e:
        # Create sample risk data for demonstration
        risk_data = pd.DataFrame({
            'risk': [
                'Data Quality Issues', 'Model Bias', 'Integration Complexity',
                'Change Resistance', 'Regulatory Compliance', 'Cybersecurity',
                'Vendor Lock-in', 'Skills Gap', 'Cost Overrun', 'Performance Issues',
                'Ethical Concerns', 'Technical Debt', 'Scalability', 'Privacy Violations'
            ],
            'probability': [3, 2, 4, 3, 2, 3, 2, 4, 3, 2, 2, 3, 2, 1],
            'impact': [4, 5, 3, 3, 5, 5, 2, 3, 3, 4, 4, 3, 3, 5],
            'category': [
                'Technical', 'Technical', 'Technical', 'Organizational', 
                'Regulatory', 'Security', 'Strategic', 'Organizational',
                'Financial', 'Technical', 'Ethical', 'Technical',
                'Technical', 'Regulatory'
            ]
        })
    
    # Calculate risk scores
    risk_data['risk_score'] = risk_data['probability'] * risk_data['impact']
    
    # Create risk matrix heatmap
    fig = go.Figure()
    
    # Add grid background
    for i in range(1, 6):
        for j in range(1, 6):
            score = i * j
            if score <= 6:
                color = 'lightgreen'
                risk_level = 'Low'
            elif score <= 12:
                color = 'yellow'
                risk_level = 'Medium'
            else:
                color = 'lightcoral'
                risk_level = 'High'
                
            fig.add_shape(
                type="rect",
                x0=i-0.5, y0=j-0.5,
                x1=i+0.5, y1=j+0.5,
                fillcolor=color,
                opacity=0.3,
                line=dict(color="gray", width=1)
            )
    
    # Add risk points
    fig.add_trace(go.Scatter(
        x=risk_data['probability'],
        y=risk_data['impact'],
        mode='markers+text',
        text=risk_data['risk'],
        textposition="top center",
        marker=dict(
            size=risk_data['risk_score'] * 3,
            color=risk_data['risk_score'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Risk Score")
        ),
        hovertemplate="<b>%{text}</b><br>Probability: %{x}<br>Impact: %{y}<br>Score: %{marker.color}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Risk Assessment Matrix",
        xaxis=dict(
            title="Probability",
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
            range=[0.5, 5.5]
        ),
        yaxis=dict(
            title="Impact",
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
            range=[0.5, 5.5]
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk summary statistics
    col1, col2, col3 = st.columns(3)
    
    high_risks = len(risk_data[risk_data['risk_score'] > 12])
    medium_risks = len(risk_data[(risk_data['risk_score'] > 6) & (risk_data['risk_score'] <= 12)])
    low_risks = len(risk_data[risk_data['risk_score'] <= 6])
    
    with col1:
        st.metric("High Risk Items", high_risks, delta=f"{high_risks/len(risk_data)*100:.0f}%")
    with col2:
        st.metric("Medium Risk Items", medium_risks, delta=f"{medium_risks/len(risk_data)*100:.0f}%")
    with col3:
        st.metric("Low Risk Items", low_risks, delta=f"{low_risks/len(risk_data)*100:.0f}%")


def _render_risk_categories(data: Dict[str, Any]) -> None:
    """Render risk analysis by category."""
    
    st.subheader("📊 Risk Analysis by Category")
    
    # Load categorized risk data
    try:
        data_service = get_data_service()
        category_risks = data_service.get_required_data("risk_assessment", "category_risks")
    except ValueError:
        # Create sample data
        category_risks = pd.DataFrame({
            'category': ['Technical', 'Organizational', 'Financial', 'Regulatory', 'Security', 'Strategic', 'Ethical'],
            'avg_risk_score': [12, 9, 8, 15, 16, 7, 10],
            'num_risks': [6, 3, 2, 2, 1, 1, 1],
            'mitigation_cost': [250000, 150000, 100000, 300000, 400000, 50000, 75000]
        })
    
    # Create stacked bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Average Risk Score',
        x=category_risks['category'],
        y=category_risks['avg_risk_score'],
        yaxis='y',
        marker_color='indianred'
    ))
    
    fig.add_trace(go.Scatter(
        name='Mitigation Cost ($100k)',
        x=category_risks['category'],
        y=category_risks['mitigation_cost'] / 100000,
        yaxis='y2',
        mode='lines+markers',
        line=dict(width=3, color='darkblue'),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="Risk Profile by Category",
        xaxis_title="Risk Category",
        yaxis=dict(
            title="Average Risk Score",
            side="left"
        ),
        yaxis2=dict(
            title="Mitigation Cost ($100k)",
            side="right",
            overlaying="y"
        ),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk category details
    st.subheader("Category Risk Profiles")
    
    for _, row in category_risks.iterrows():
        with st.expander(f"{row['category']} Risk Analysis"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Risk Score", f"{row['avg_risk_score']:.1f}")
            with col2:
                st.metric("Number of Risks", row['num_risks'])
            with col3:
                st.metric("Mitigation Cost", f"${row['mitigation_cost']:,.0f}")
            
            # Risk level indicator
            if row['avg_risk_score'] > 12:
                st.error(f"⚠️ High risk category requiring immediate attention")
            elif row['avg_risk_score'] > 6:
                st.warning(f"⚡ Medium risk category requiring monitoring")
            else:
                st.success(f"✅ Low risk category under control")


def _render_mitigation_strategies(data: Dict[str, Any]) -> None:
    """Render risk mitigation strategies."""
    
    st.subheader("🛡️ Risk Mitigation Strategies")
    
    # Load mitigation strategies
    try:
        data_service = get_data_service()
        mitigation_data = data_service.get_required_data("risk_assessment", "mitigation_strategies")
    except ValueError:
        # Create comprehensive mitigation strategies
        mitigation_data = pd.DataFrame({
            'risk': [
                'Data Quality Issues', 'Model Bias', 'Integration Complexity',
                'Change Resistance', 'Regulatory Compliance', 'Cybersecurity'
            ],
            'strategy': [
                'Implement data validation pipelines and quality monitoring',
                'Regular bias audits and diverse training data',
                'Phased integration with API-first architecture',
                'Comprehensive change management and training program',
                'Legal review and compliance automation tools',
                'Zero-trust security model and regular penetration testing'
            ],
            'cost': [75000, 50000, 150000, 100000, 200000, 250000],
            'effectiveness': [0.85, 0.70, 0.80, 0.75, 0.90, 0.95],
            'implementation_time': [2, 3, 6, 4, 5, 4]  # months
        })
    
    # Create mitigation effectiveness chart
    fig = px.scatter(
        mitigation_data,
        x='cost',
        y='effectiveness',
        size='implementation_time',
        color='risk',
        title="Mitigation Strategy Cost-Effectiveness Analysis",
        labels={
            'cost': 'Implementation Cost ($)',
            'effectiveness': 'Risk Reduction Effectiveness',
            'implementation_time': 'Time (months)'
        },
        hover_data=['strategy']
    )
    
    # Add quadrant lines
    fig.add_hline(y=0.8, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=mitigation_data['cost'].median(), line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=50000, y=0.95, text="High Impact<br>Low Cost", showarrow=False)
    fig.add_annotation(x=200000, y=0.95, text="High Impact<br>High Cost", showarrow=False)
    fig.add_annotation(x=50000, y=0.65, text="Low Impact<br>Low Cost", showarrow=False)
    fig.add_annotation(x=200000, y=0.65, text="Low Impact<br>High Cost", showarrow=False)
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Mitigation roadmap
    st.subheader("📋 Mitigation Implementation Roadmap")
    
    # Sort by effectiveness/cost ratio
    mitigation_data['priority_score'] = mitigation_data['effectiveness'] / (mitigation_data['cost'] / 100000)
    mitigation_data = mitigation_data.sort_values('priority_score', ascending=False)
    
    for idx, row in mitigation_data.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{row['risk']}**")
                st.write(f"_{row['strategy']}_")
                
            with col2:
                st.metric("Cost", f"${row['cost']:,.0f}")
                
            with col3:
                st.metric("Effectiveness", f"{row['effectiveness']*100:.0f}%")
                
            with col4:
                st.metric("Timeline", f"{row['implementation_time']} mo")
                
            # Progress bar for priority
            st.progress(row['priority_score'] / mitigation_data['priority_score'].max())
            st.write("---")


def _render_portfolio_risk(data: Dict[str, Any]) -> None:
    """Render portfolio-level risk analysis."""
    
    st.subheader("💼 AI Portfolio Risk Assessment")
    
    # Portfolio configuration
    st.write("**Configure Your AI Project Portfolio**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_projects = st.slider("Number of AI Projects", 1, 10, 3)
        total_investment = st.number_input(
            "Total Portfolio Investment ($)",
            min_value=100000,
            max_value=50000000,
            value=5000000,
            step=100000
        )
        
    with col2:
        correlation = st.select_slider(
            "Project Correlation",
            options=["Independent", "Low", "Medium", "High"],
            value="Medium"
        )
        time_horizon = st.slider("Time Horizon (years)", 1, 5, 3)
    
    # Generate portfolio projects
    projects = []
    for i in range(num_projects):
        project = {
            'name': f'Project {i+1}',
            'investment': total_investment / num_projects * np.random.uniform(0.5, 1.5),
            'risk_score': np.random.uniform(5, 20),
            'expected_return': np.random.uniform(0.15, 0.45),
            'category': np.random.choice(['Process Automation', 'Analytics', 'Customer Service', 'R&D'])
        }
        projects.append(project)
    
    projects_df = pd.DataFrame(projects)
    
    # Portfolio metrics
    st.subheader("📊 Portfolio Risk Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate portfolio metrics
    total_risk = np.average(projects_df['risk_score'], weights=projects_df['investment'])
    expected_portfolio_return = np.average(projects_df['expected_return'], weights=projects_df['investment'])
    
    # Adjust for correlation
    correlation_factors = {"Independent": 0.7, "Low": 0.85, "Medium": 1.0, "High": 1.2}
    correlation_factor = correlation_factors[correlation]
    adjusted_risk = total_risk * correlation_factor
    
    with col1:
        st.metric("Portfolio Risk Score", f"{adjusted_risk:.1f}")
    with col2:
        st.metric("Expected Return", f"{expected_portfolio_return*100:.1f}%")
    with col3:
        st.metric("Risk-Adjusted Return", f"{(expected_portfolio_return / (adjusted_risk/20))*100:.1f}%")
    with col4:
        concentration = projects_df['investment'].max() / projects_df['investment'].sum()
        st.metric("Concentration Risk", f"{concentration*100:.0f}%")
    
    # Portfolio visualization
    fig = go.Figure()
    
    # Bubble chart of projects
    fig.add_trace(go.Scatter(
        x=projects_df['risk_score'],
        y=projects_df['expected_return'] * 100,
        mode='markers+text',
        text=projects_df['name'],
        textposition="top center",
        marker=dict(
            size=projects_df['investment'] / 50000,  # Scale for visibility
            color=projects_df['expected_return'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Expected<br>Return")
        ),
        hovertemplate="<b>%{text}</b><br>Risk: %{x:.1f}<br>Return: %{y:.1f}%<br>Investment: $%{marker.size:,.0f}<extra></extra>"
    ))
    
    # Add efficient frontier approximation
    x_frontier = np.linspace(5, 20, 50)
    y_frontier = 15 + 1.5 * x_frontier + 0.05 * x_frontier**2
    
    fig.add_trace(go.Scatter(
        x=x_frontier,
        y=y_frontier,
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='red', dash='dash'),
        showlegend=True
    ))
    
    fig.update_layout(
        title="Portfolio Risk-Return Profile",
        xaxis_title="Risk Score",
        yaxis_title="Expected Return (%)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Diversification analysis
    st.subheader("🎯 Diversification Analysis")
    
    category_dist = projects_df.groupby('category')['investment'].sum()
    
    fig_pie = px.pie(
        values=category_dist.values,
        names=category_dist.index,
        title="Portfolio Diversification by Category"
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 Portfolio Risk Recommendations")
    
    if adjusted_risk > 15:
        st.warning("⚠️ **High Portfolio Risk**: Consider diversifying across lower-risk projects")
    elif adjusted_risk > 10:
        st.info("ℹ️ **Moderate Portfolio Risk**: Well-balanced risk profile")
    else:
        st.success("✅ **Low Portfolio Risk**: Conservative portfolio with stable returns")
    
    if concentration > 0.4:
        st.warning("⚠️ **Concentration Risk**: Over 40% invested in single project")
    
    if correlation == "High":
        st.warning("⚠️ **Correlation Risk**: Projects are highly correlated, reducing diversification benefits")


def _render_risk_return_analysis(data: Dict[str, Any]) -> None:
    """Render risk-return analysis."""
    
    st.subheader("📈 Risk-Return Analysis")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.number_input(
            "Investment Amount ($)",
            min_value=10000,
            max_value=10000000,
            value=500000,
            step=10000
        )
        
        expected_return = st.slider(
            "Expected Annual Return (%)",
            min_value=5.0,
            max_value=50.0,
            value=25.0,
            step=5.0
        ) / 100
        
    with col2:
        risk_level = st.selectbox(
            "Risk Level",
            ["Low", "Medium", "High", "Very High"],
            index=1
        )
        
        time_horizon = st.slider(
            "Investment Horizon (years)",
            min_value=1,
            max_value=10,
            value=3
        )
    
    # Calculate risk-adjusted metrics
    risk_metrics = calculate_risk_adjusted_return(expected_return, risk_level)
    
    # Display risk-adjusted metrics
    st.subheader("Risk-Adjusted Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Risk-Adjusted Return",
            f"{risk_metrics['risk_adjusted_return']*100:.1f}%",
            delta=f"{(risk_metrics['risk_adjusted_return'] - expected_return)*100:.1f}pp"
        )
        
    with col2:
        st.metric(
            "Sharpe Ratio",
            f"{risk_metrics['sharpe_ratio']:.2f}",
            help="Risk-adjusted return per unit of volatility"
        )
        
    with col3:
        threshold_met = "✅ Yes" if risk_metrics['meets_threshold'] else "❌ No"
        st.metric(
            "Meets Risk Threshold",
            threshold_met
        )
    
    # Monte Carlo simulation for risk scenarios
    st.subheader("📊 Risk Scenario Analysis")
    
    # Generate scenarios
    scenarios = []
    for i in range(1000):
        # Simulate returns based on risk level
        volatility = risk_metrics['volatility']
        annual_return = np.random.normal(expected_return, volatility)
        
        # Calculate final value
        final_value = investment_amount * (1 + annual_return) ** time_horizon
        scenarios.append(final_value)
    
    scenarios = np.array(scenarios)
    
    # Calculate percentiles
    percentiles = [5, 25, 50, 75, 95]
    scenario_percentiles = np.percentile(scenarios, percentiles)
    
    # Create distribution chart
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=scenarios,
        nbinsx=50,
        name='Outcome Distribution',
        marker_color='lightblue',
        opacity=0.7
    ))
    
    # Add percentile lines
    colors = ['red', 'orange', 'green', 'orange', 'red']
    for i, (p, val) in enumerate(zip(percentiles, scenario_percentiles)):
        fig.add_vline(
            x=val,
            line_dash="dash",
            line_color=colors[i],
            annotation_text=f"P{p}: ${val:,.0f}",
            annotation_position="top"
        )
    
    fig.update_layout(
        title=f"Investment Value Distribution after {time_horizon} Years",
        xaxis_title="Final Investment Value ($)",
        yaxis_title="Frequency",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Value at Risk (VaR) analysis
    var_95 = investment_amount - scenario_percentiles[0]
    var_99 = investment_amount - np.percentile(scenarios, 1)
    
    st.subheader("⚠️ Value at Risk (VaR) Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "VaR 95%",
            f"${var_95:,.0f}",
            help="Maximum expected loss with 95% confidence"
        )
        
    with col2:
        st.metric(
            "VaR 99%",
            f"${var_99:,.0f}",
            help="Maximum expected loss with 99% confidence"
        )
        
    with col3:
        st.metric(
            "Expected Shortfall",
            f"${investment_amount - scenarios[scenarios < scenario_percentiles[0]].mean():,.0f}",
            help="Average loss in worst 5% of scenarios"
        )
    
    # Risk-return trade-off analysis
    st.subheader("🔄 Risk-Return Trade-off Analysis")
    
    # Generate efficient frontier
    risk_levels_all = ["Low", "Medium", "High", "Very High"]
    returns = []
    risks = []
    sharpes = []
    
    for level in risk_levels_all:
        metrics = calculate_risk_adjusted_return(expected_return, level)
        returns.append(metrics['risk_adjusted_return'] * 100)
        risks.append(metrics['volatility'] * 100)
        sharpes.append(metrics['sharpe_ratio'])
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=risks,
        y=returns,
        mode='markers+lines',
        text=risk_levels_all,
        textposition="top center",
        marker=dict(
            size=[s*20 for s in sharpes],
            color=sharpes,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe<br>Ratio")
        ),
        line=dict(width=2, dash='dash'),
        hovertemplate="<b>%{text}</b><br>Risk: %{x:.1f}%<br>Return: %{y:.1f}%<br>Sharpe: %{marker.color:.2f}<extra></extra>"
    ))
    
    # Highlight current selection
    current_metrics = calculate_risk_adjusted_return(expected_return, risk_level)
    fig2.add_trace(go.Scatter(
        x=[current_metrics['volatility'] * 100],
        y=[current_metrics['risk_adjusted_return'] * 100],
        mode='markers',
        marker=dict(size=20, color='red', symbol='star'),
        name='Current Selection',
        showlegend=True
    ))
    
    fig2.update_layout(
        title="Risk-Return Trade-off Curve",
        xaxis_title="Risk (Volatility %)",
        yaxis_title="Risk-Adjusted Return (%)",
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)