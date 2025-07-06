"""Scenario Analysis view for AI Adoption Dashboard.

This module provides Monte Carlo simulation, sensitivity analysis,
and scenario planning capabilities for AI adoption strategies.
"""

from typing import Any, Dict, List
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from business.scenario_engine import (
    ScenarioVariable,
    monte_carlo_simulation,
    sensitivity_analysis,
    adoption_s_curve,
    scenario_comparison,
    create_scenario_tornado_chart
)
from business.roi_analysis import compute_comprehensive_roi
from data.services import get_data_service


def render(data: Dict[str, Any]) -> None:
    """Render the Scenario Analysis view."""
    
    st.header("🎲 AI Adoption Scenario Analysis")
    st.markdown(
        "Explore different scenarios and uncertainties in AI adoption using "
        "Monte Carlo simulation, sensitivity analysis, and adoption curves."
    )
    
    # Create tabs for different analyses
    tabs = st.tabs([
        "📊 Monte Carlo Simulation",
        "🎯 Sensitivity Analysis", 
        "📈 Adoption Curves",
        "🔄 Scenario Comparison"
    ])
    
    with tabs[0]:
        _render_monte_carlo(data)
        
    with tabs[1]:
        _render_sensitivity_analysis(data)
        
    with tabs[2]:
        _render_adoption_curves(data)
        
    with tabs[3]:
        _render_scenario_comparison(data)


def _render_monte_carlo(data: Dict[str, Any]) -> None:
    """Render Monte Carlo simulation tab."""
    
    st.subheader("🎲 Monte Carlo Simulation")
    st.markdown(
        "Run thousands of scenarios to understand the range of possible outcomes "
        "and their probabilities."
    )
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Base Case Parameters")
        
        base_investment = st.number_input(
            "Base Investment ($)",
            min_value=50000.0,
            value=1000000.0,
            step=50000.0
        )
        
        base_annual_benefit = st.number_input(
            "Base Annual Benefit ($)",
            min_value=10000.0,
            value=400000.0,
            step=10000.0
        )
        
        base_annual_cost = st.number_input(
            "Base Annual Cost ($)",
            min_value=0.0,
            value=100000.0,
            step=10000.0
        )
        
        years = st.slider("Analysis Period (years)", 1, 10, 5)
        
    with col2:
        st.markdown("### Uncertainty Parameters")
        
        investment_variation = st.slider(
            "Investment Uncertainty (±%)",
            min_value=5,
            max_value=50,
            value=20,
            help="How much the actual investment might vary from estimate"
        ) / 100
        
        benefit_variation = st.slider(
            "Benefit Uncertainty (±%)",
            min_value=10,
            max_value=60,
            value=30,
            help="How much benefits might vary from estimate"
        ) / 100
        
        cost_variation = st.slider(
            "Cost Uncertainty (±%)",
            min_value=5,
            max_value=40,
            value=15,
            help="How much operating costs might vary"
        ) / 100
        
        iterations = st.select_slider(
            "Simulation Iterations",
            options=[1000, 5000, 10000, 25000, 50000],
            value=10000
        )
    
    # Run simulation button
    if st.button("Run Monte Carlo Simulation", type="primary"):
        with st.spinner(f"Running {iterations:,} simulations..."):
            
            # Define variables for simulation
            variables = [
                ScenarioVariable(
                    name="initial_investment",
                    base_value=base_investment,
                    min_value=base_investment * (1 - investment_variation),
                    max_value=base_investment * (1 + investment_variation),
                    distribution='triangular',
                    mode=base_investment
                ),
                ScenarioVariable(
                    name="annual_benefit",
                    base_value=base_annual_benefit,
                    min_value=base_annual_benefit * (1 - benefit_variation),
                    max_value=base_annual_benefit * (1 + benefit_variation),
                    distribution='normal',
                    std_dev=base_annual_benefit * benefit_variation / 3
                ),
                ScenarioVariable(
                    name="annual_cost",
                    base_value=base_annual_cost,
                    min_value=base_annual_cost * (1 - cost_variation),
                    max_value=base_annual_cost * (1 + cost_variation),
                    distribution='uniform'
                )
            ]
            
            # Define NPV calculation function
            def calculate_npv_scenario(initial_investment, annual_benefit, annual_cost):
                net_cash_flow = annual_benefit - annual_cost
                cash_flows = [net_cash_flow] * years
                
                # Simple NPV at 10% discount rate
                npv = -initial_investment
                for i, cf in enumerate(cash_flows):
                    npv += cf / (1.1 ** (i + 1))
                return npv
            
            # Run simulation
            base_case = {
                'initial_investment': base_investment,
                'annual_benefit': base_annual_benefit,
                'annual_cost': base_annual_cost
            }
            
            results = monte_carlo_simulation(
                base_case=base_case,
                variables=variables,
                model_function=calculate_npv_scenario,
                iterations=iterations
            )
            
            # Display results
            st.success(f"Completed {results['iterations']:,} simulations")
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Mean NPV",
                    f"${results['mean']:,.0f}",
                    delta=f"±${results['std_dev']:,.0f} std"
                )
                
            with col2:
                st.metric(
                    "90% Confidence Range",
                    f"${results['confidence_interval_90'][0]:,.0f} to ${results['confidence_interval_90'][1]:,.0f}"
                )
                
            with col3:
                prob_positive = sum(1 for v in results['histogram_data']['values'] if v > 0) / results['iterations'] * 100
                st.metric(
                    "Probability NPV > 0",
                    f"{prob_positive:.1f}%",
                    delta="Success likelihood"
                )
                
            with col4:
                st.metric(
                    "Coefficient of Variation",
                    f"{results['coefficient_of_variation']:.2f}",
                    help="Lower is more certain"
                )
            
            # Histogram of results
            st.markdown("### NPV Distribution")
            
            fig_hist = go.Figure()
            
            fig_hist.add_trace(go.Histogram(
                x=results['histogram_data']['values'],
                nbinsx=50,
                name='NPV Distribution',
                marker_color='blue',
                opacity=0.7
            ))
            
            # Add mean line
            fig_hist.add_vline(
                x=results['mean'],
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mean: ${results['mean']:,.0f}"
            )
            
            # Add percentile lines
            for percentile, value in results['percentiles'].items():
                if percentile in ['p5', 'p95']:
                    fig_hist.add_vline(
                        x=value,
                        line_dash="dot",
                        line_color="green",
                        annotation_text=f"{percentile}: ${value:,.0f}"
                    )
            
            fig_hist.update_layout(
                title="Monte Carlo NPV Distribution",
                xaxis_title="Net Present Value ($)",
                yaxis_title="Frequency",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Correlation analysis
            st.markdown("### Input Sensitivity")
            
            corr_data = []
            for var_name, corr_info in results['correlations'].items():
                corr_data.append({
                    'Variable': var_name.replace('_', ' ').title(),
                    'Correlation': corr_info['correlation'],
                    'Significance': '***' if corr_info['p_value'] < 0.001 else
                                   '**' if corr_info['p_value'] < 0.01 else
                                   '*' if corr_info['p_value'] < 0.05 else '',
                    'Impact': 'Strong' if abs(corr_info['correlation']) > 0.7 else
                             'Moderate' if abs(corr_info['correlation']) > 0.3 else 'Weak'
                })
            
            corr_df = pd.DataFrame(corr_data)
            corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
            
            # Create correlation bar chart
            fig_corr = px.bar(
                corr_df,
                x='Correlation',
                y='Variable',
                orientation='h',
                color='Correlation',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title="Variable Impact on NPV"
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Risk metrics
            st.markdown("### Risk Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Value at Risk
                var_95 = np.percentile(results['histogram_data']['values'], 5)
                st.metric(
                    "Value at Risk (95%)",
                    f"${var_95:,.0f}",
                    help="5% chance of NPV being worse than this"
                )
                
                # Downside risk
                downside_values = [v for v in results['histogram_data']['values'] if v < 0]
                if downside_values:
                    avg_downside = np.mean(downside_values)
                    st.metric(
                        "Average Downside",
                        f"${avg_downside:,.0f}",
                        help="Average loss when NPV is negative"
                    )
                
            with col2:
                # Upside potential
                upside_values = [v for v in results['histogram_data']['values'] if v > results['mean']]
                if upside_values:
                    avg_upside = np.mean(upside_values)
                    st.metric(
                        "Average Upside",
                        f"${avg_upside:,.0f}",
                        help="Average NPV when above mean"
                    )
                
                # Best/worst case from simulation
                st.metric(
                    "Best/Worst Case",
                    f"${results['max']:,.0f} / ${results['min']:,.0f}",
                    help="From simulation results"
                )


def _render_sensitivity_analysis(data: Dict[str, Any]) -> None:
    """Render sensitivity analysis tab."""
    
    st.subheader("🎯 Sensitivity Analysis")
    st.markdown(
        "Understand which variables have the biggest impact on your AI investment outcomes."
    )
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Base Case Inputs")
        
        base_params = {
            'initial_investment': st.number_input(
                "Initial Investment ($)",
                min_value=50000.0,
                value=1000000.0,
                step=50000.0,
                key='sens_investment'
            ),
            'annual_revenue': st.number_input(
                "Annual Revenue Increase ($)",
                min_value=0.0,
                value=300000.0,
                step=10000.0,
                key='sens_revenue'
            ),
            'annual_cost_savings': st.number_input(
                "Annual Cost Savings ($)",
                min_value=0.0,
                value=200000.0,
                step=10000.0,
                key='sens_savings'
            ),
            'annual_operating_cost': st.number_input(
                "Annual Operating Cost ($)",
                min_value=0.0,
                value=100000.0,
                step=10000.0,
                key='sens_opcost'
            ),
            'productivity_gain': st.slider(
                "Productivity Gain (%)",
                min_value=0.0,
                max_value=50.0,
                value=15.0,
                key='sens_prod'
            ) / 100,
            'years': st.slider(
                "Analysis Period (years)",
                min_value=1,
                max_value=10,
                value=5,
                key='sens_years'
            )
        }
        
    with col2:
        st.markdown("### Analysis Settings")
        
        variation_pct = st.slider(
            "Variation Range (±%)",
            min_value=10,
            max_value=50,
            value=25,
            help="How much to vary each parameter"
        ) / 100
        
        steps = st.slider(
            "Analysis Steps",
            min_value=3,
            max_value=11,
            value=5,
            step=2,
            help="Number of values to test for each parameter"
        )
        
        variables_to_analyze = st.multiselect(
            "Variables to Analyze",
            options=list(base_params.keys()),
            default=['initial_investment', 'annual_revenue', 'annual_cost_savings', 'productivity_gain']
        )
    
    # Run analysis button
    if st.button("Run Sensitivity Analysis", type="primary", key='run_sensitivity'):
        with st.spinner("Analyzing parameter sensitivity..."):
            
            # Define model function for sensitivity analysis
            def roi_model(**params):
                annual_benefit = params.get('annual_revenue', 0) + params.get('annual_cost_savings', 0)
                net_cash_flow = annual_benefit - params.get('annual_operating_cost', 0)
                
                # Add productivity gains if applicable
                if params.get('productivity_gain', 0) > 0:
                    # Assume 100 employees with $75k average salary
                    productivity_value = 100 * 75000 * params.get('productivity_gain', 0)
                    net_cash_flow += productivity_value
                
                # Calculate NPV
                initial_investment = params.get('initial_investment', 1000000)
                years = int(params.get('years', 5))
                
                npv = -initial_investment
                for year in range(years):
                    npv += net_cash_flow / (1.1 ** (year + 1))
                
                return npv
            
            # Run sensitivity analysis
            results = sensitivity_analysis(
                base_case=base_params,
                variables=variables_to_analyze,
                model_function=roi_model,
                variation_pct=variation_pct,
                steps=steps
            )
            
            # Display tornado chart
            st.markdown("### Tornado Chart - Parameter Impact")
            
            tornado_data = create_scenario_tornado_chart(
                results,
                variable_names={
                    'initial_investment': 'Initial Investment',
                    'annual_revenue': 'Annual Revenue',
                    'annual_cost_savings': 'Cost Savings',
                    'annual_operating_cost': 'Operating Cost',
                    'productivity_gain': 'Productivity Gain',
                    'years': 'Time Horizon'
                }
            )
            
            # Create tornado chart
            fig_tornado = go.Figure()
            
            for item in tornado_data['data']:
                # Low impact bar
                fig_tornado.add_trace(go.Bar(
                    name=item['variable'],
                    y=[item['variable']],
                    x=[item['min_deviation']],
                    orientation='h',
                    marker_color='red',
                    showlegend=False,
                    hovertext=f"Min: ${item['min_impact']:,.0f}"
                ))
                
                # High impact bar
                fig_tornado.add_trace(go.Bar(
                    name=item['variable'],
                    y=[item['variable']],
                    x=[item['max_deviation']],
                    orientation='h',
                    marker_color='green',
                    showlegend=False,
                    hovertext=f"Max: ${item['max_impact']:,.0f}"
                ))
            
            # Add base case line
            fig_tornado.add_vline(
                x=0,
                line_dash="solid",
                line_color="black",
                line_width=2
            )
            
            fig_tornado.update_layout(
                title=f"Parameter Sensitivity (Base NPV: ${tornado_data['base_result']:,.0f})",
                xaxis_title="NPV Impact ($)",
                barmode='overlay',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_tornado, use_container_width=True)
            
            # Elasticity table
            st.markdown("### Parameter Elasticity")
            
            elasticity_data = []
            for var in variables_to_analyze:
                if var in results and var != 'base_result':
                    elasticity_data.append({
                        'Parameter': var.replace('_', ' ').title(),
                        'Elasticity': f"{results[var]['elasticity']:.2f}",
                        'Interpretation': _interpret_elasticity(results[var]['elasticity'])
                    })
            
            elasticity_df = pd.DataFrame(elasticity_data)
            elasticity_df = elasticity_df.sort_values('Elasticity', key=lambda x: x.astype(float).abs(), ascending=False)
            
            st.dataframe(elasticity_df, use_container_width=True, hide_index=True)
            
            # Detailed parameter plots
            st.markdown("### Detailed Parameter Analysis")
            
            selected_param = st.selectbox(
                "Select parameter for detailed view:",
                options=variables_to_analyze,
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if selected_param in results:
                param_data = results[selected_param]['values']
                
                df_param = pd.DataFrame(param_data)
                
                fig_detail = go.Figure()
                
                fig_detail.add_trace(go.Scatter(
                    x=df_param['value'],
                    y=df_param['result'],
                    mode='lines+markers',
                    name='NPV',
                    line=dict(width=3, color='blue'),
                    marker=dict(size=8)
                ))
                
                # Add base case marker
                base_value = base_params[selected_param]
                base_result = results['base_result']
                
                fig_detail.add_trace(go.Scatter(
                    x=[base_value],
                    y=[base_result],
                    mode='markers',
                    name='Base Case',
                    marker=dict(size=15, color='red', symbol='star')
                ))
                
                fig_detail.update_layout(
                    title=f"NPV Sensitivity to {selected_param.replace('_', ' ').title()}",
                    xaxis_title=selected_param.replace('_', ' ').title(),
                    yaxis_title="Net Present Value ($)",
                    height=400
                )
                
                st.plotly_chart(fig_detail, use_container_width=True)
                
                # Break-even analysis for this parameter
                if len(param_data) > 2:
                    # Find break-even point if it exists
                    for i in range(len(param_data) - 1):
                        if param_data[i]['result'] * param_data[i+1]['result'] < 0:
                            # Linear interpolation for break-even
                            x1, y1 = param_data[i]['value'], param_data[i]['result']
                            x2, y2 = param_data[i+1]['value'], param_data[i+1]['result']
                            break_even = x1 - y1 * (x2 - x1) / (y2 - y1)
                            
                            st.info(f"💡 Break-even {selected_param.replace('_', ' ')}: {break_even:,.2f}")
                            break


def _render_adoption_curves(data: Dict[str, Any]) -> None:
    """Render adoption curves tab."""
    
    st.subheader("📈 Technology Adoption Modeling")
    st.markdown(
        "Model realistic AI adoption patterns using S-curves and understand adoption dynamics."
    )
    
    # Parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Adoption Parameters")
        
        time_periods = st.slider(
            "Time Periods (Quarters)",
            min_value=8,
            max_value=40,
            value=20,
            step=4
        )
        
        max_adoption = st.slider(
            "Maximum Adoption Rate (%)",
            min_value=50.0,
            max_value=100.0,
            value=85.0,
            step=5.0
        )
        
        inflection_quarter = st.slider(
            "Inflection Point (Quarter)",
            min_value=4,
            max_value=time_periods-4,
            value=time_periods//2,
            help="Quarter where adoption accelerates most"
        )
        
    with col2:
        st.markdown("### Curve Characteristics")
        
        steepness = st.slider(
            "Adoption Speed",
            min_value=0.1,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="How quickly adoption spreads"
        )
        
        # Technology selection
        technologies = st.multiselect(
            "Technologies to Model",
            ["GenAI", "Process Automation", "Computer Vision", "NLP", "Predictive Analytics"],
            default=["GenAI", "Process Automation"]
        )
        
        correlation_type = st.radio(
            "Technology Relationship",
            ["complementary", "competitive", "mixed"],
            help="How technologies affect each other's adoption"
        )
    
    # Generate adoption curves
    if st.button("Generate Adoption Curves", type="primary"):
        
        # Create figure
        fig = go.Figure()
        
        # Generate base S-curve
        base_adoption = adoption_s_curve(
            time_periods=time_periods,
            max_adoption=max_adoption,
            inflection_point=inflection_quarter,
            steepness=steepness
        )
        
        # Time axis
        quarters = [f"Q{i//4+1} Y{i%4+1}" if i%4==0 else f"Q{i%4+1}" for i in range(time_periods)]
        
        # Plot curves for each technology
        for i, tech in enumerate(technologies):
            # Adjust curve for each technology
            tech_steepness = steepness * (1 + np.random.uniform(-0.2, 0.2))
            tech_inflection = inflection_quarter + np.random.randint(-2, 3)
            tech_max = max_adoption * (0.9 + np.random.uniform(0, 0.2))
            
            tech_adoption = adoption_s_curve(
                time_periods=time_periods,
                max_adoption=tech_max,
                inflection_point=tech_inflection,
                steepness=tech_steepness
            )
            
            fig.add_trace(go.Scatter(
                x=list(range(time_periods)),
                y=tech_adoption,
                mode='lines',
                name=tech,
                line=dict(width=3)
            ))
        
        # Add average line if multiple technologies
        if len(technologies) > 1:
            avg_adoption = np.mean([
                adoption_s_curve(
                    time_periods=time_periods,
                    max_adoption=max_adoption * (0.9 + np.random.uniform(0, 0.2)),
                    inflection_point=inflection_quarter + np.random.randint(-2, 3),
                    steepness=steepness * (1 + np.random.uniform(-0.2, 0.2))
                ) for _ in technologies
            ], axis=0)
            
            fig.add_trace(go.Scatter(
                x=list(range(time_periods)),
                y=avg_adoption,
                mode='lines',
                name='Industry Average',
                line=dict(width=4, dash='dash', color='black')
            ))
        
        # Update layout
        fig.update_layout(
            title="AI Technology Adoption Curves",
            xaxis_title="Time Period (Quarters)",
            yaxis_title="Adoption Rate (%)",
            yaxis_range=[0, 100],
            height=500,
            hovermode='x unified'
        )
        
        # Add inflection point marker
        fig.add_vline(
            x=inflection_quarter,
            line_dash="dot",
            line_color="gray",
            annotation_text="Inflection Point"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Adoption metrics
        st.markdown("### Adoption Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Time to 50% adoption
            time_to_50 = next((i for i, v in enumerate(base_adoption) if v >= 50), None)
            if time_to_50:
                st.metric(
                    "Time to 50% Adoption",
                    f"{time_to_50} quarters",
                    delta=f"{time_to_50/4:.1f} years"
                )
        
        with col2:
            # Maximum growth rate
            growth_rates = [base_adoption[i] - base_adoption[i-1] for i in range(1, len(base_adoption))]
            max_growth = max(growth_rates)
            max_growth_quarter = growth_rates.index(max_growth) + 1
            
            st.metric(
                "Peak Growth Rate",
                f"{max_growth:.1f}% per quarter",
                delta=f"In Q{max_growth_quarter}"
            )
        
        with col3:
            # Final adoption
            final_adoption = base_adoption[-1]
            st.metric(
                "Final Adoption Rate",
                f"{final_adoption:.1f}%",
                delta=f"After {time_periods/4:.1f} years"
            )
        
        # Adoption phases
        st.markdown("### Adoption Phases")
        
        # Define phases based on adoption levels
        phases = []
        if time_to_50:
            innovators_end = next((i for i, v in enumerate(base_adoption) if v >= 2.5), 0)
            early_adopters_end = next((i for i, v in enumerate(base_adoption) if v >= 16), innovators_end)
            early_majority_end = next((i for i, v in enumerate(base_adoption) if v >= 50), early_adopters_end)
            late_majority_end = next((i for i, v in enumerate(base_adoption) if v >= 84), early_majority_end)
            
            phase_data = pd.DataFrame({
                'Phase': ['Innovators', 'Early Adopters', 'Early Majority', 'Late Majority', 'Laggards'],
                'Start Quarter': [0, innovators_end, early_adopters_end, early_majority_end, late_majority_end],
                'Duration (Quarters)': [
                    innovators_end,
                    early_adopters_end - innovators_end,
                    early_majority_end - early_adopters_end,
                    late_majority_end - early_majority_end,
                    time_periods - late_majority_end
                ],
                'Adoption Range': ['0-2.5%', '2.5-16%', '16-50%', '50-84%', '84%+']
            })
            
            st.dataframe(phase_data, use_container_width=True, hide_index=True)


def _render_scenario_comparison(data: Dict[str, Any]) -> None:
    """Render scenario comparison tab."""
    
    st.subheader("🔄 Multi-Scenario Comparison")
    st.markdown(
        "Compare different AI adoption scenarios side by side to make informed decisions."
    )
    
    # Scenario definitions
    st.markdown("### Define Scenarios")
    
    num_scenarios = st.slider("Number of scenarios to compare", 2, 5, 3)
    
    scenarios = {}
    tabs = st.tabs([f"Scenario {i+1}" for i in range(num_scenarios)])
    
    # Default scenario names
    default_names = ["Conservative", "Base Case", "Optimistic", "Aggressive", "Best Case"]
    
    for i, tab in enumerate(tabs):
        with tab:
            scenario_name = st.text_input(
                "Scenario Name",
                value=default_names[i] if i < len(default_names) else f"Scenario {i+1}",
                key=f"scenario_name_{i}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                investment = st.number_input(
                    "Initial Investment ($)",
                    min_value=50000.0,
                    value=500000.0 * (1 + i * 0.5),
                    step=50000.0,
                    key=f"investment_{i}"
                )
                
                revenue = st.number_input(
                    "Annual Revenue Increase ($)",
                    min_value=0.0,
                    value=200000.0 * (1 + i * 0.3),
                    step=10000.0,
                    key=f"revenue_{i}"
                )
                
                cost_savings = st.number_input(
                    "Annual Cost Savings ($)",
                    min_value=0.0,
                    value=150000.0 * (1 + i * 0.2),
                    step=10000.0,
                    key=f"savings_{i}"
                )
                
            with col2:
                operating_cost = st.number_input(
                    "Annual Operating Cost ($)",
                    min_value=0.0,
                    value=100000.0 * (1 + i * 0.1),
                    step=10000.0,
                    key=f"opcost_{i}"
                )
                
                risk_level = st.selectbox(
                    "Risk Level",
                    ["Low", "Medium", "High", "Very High"],
                    index=min(i, 3),
                    key=f"risk_{i}"
                )
                
                adoption_rate = st.slider(
                    "Expected Adoption Rate (%)",
                    min_value=20.0,
                    max_value=100.0,
                    value=50.0 + i * 15.0,
                    step=5.0,
                    key=f"adoption_{i}"
                ) / 100
            
            scenarios[scenario_name] = {
                'initial_investment': investment,
                'annual_benefit': revenue + cost_savings,
                'annual_cost': operating_cost,
                'risk_level': risk_level,
                'adoption_rate': adoption_rate
            }
    
    # Compare scenarios
    if st.button("Compare Scenarios", type="primary"):
        
        # Calculate metrics for each scenario
        def calculate_scenario_metrics(**params):
            # NPV calculation
            net_cash_flow = params['annual_benefit'] - params['annual_cost']
            cash_flows = [net_cash_flow * params['adoption_rate']] * 5  # 5 year analysis
            
            npv = -params['initial_investment']
            for i, cf in enumerate(cash_flows):
                npv += cf / (1.1 ** (i + 1))
            
            # Simple ROI
            total_benefit = sum(cash_flows)
            roi = ((total_benefit - params['initial_investment']) / params['initial_investment']) * 100
            
            # Payback period
            if net_cash_flow > 0:
                payback = params['initial_investment'] / (net_cash_flow * params['adoption_rate'])
            else:
                payback = float('inf')
            
            return {
                'NPV': npv,
                'ROI %': roi,
                'Payback Years': payback,
                'Annual Net Benefit': net_cash_flow * params['adoption_rate'],
                'Risk Level': params['risk_level']
            }
        
        # Compare scenarios
        comparison_df = scenario_comparison(scenarios, calculate_scenario_metrics)
        
        # Display comparison table
        st.markdown("### Scenario Comparison Results")
        
        # Format the dataframe
        formatted_df = comparison_df.copy()
        formatted_df['NPV'] = formatted_df['NPV'].apply(lambda x: f"${x:,.0f}")
        formatted_df['ROI %'] = formatted_df['ROI %'].apply(lambda x: f"{x:.1f}%")
        formatted_df['Payback Years'] = formatted_df['Payback Years'].apply(
            lambda x: f"{x:.1f}" if x != float('inf') else "Never"
        )
        formatted_df['Annual Net Benefit'] = formatted_df['Annual Net Benefit'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "scenario": "Scenario",
                "NPV": st.column_config.TextColumn("NPV", help="Net Present Value"),
                "ROI %": st.column_config.TextColumn("ROI", help="Return on Investment"),
                "Payback Years": st.column_config.TextColumn("Payback", help="Years to recover investment"),
                "Risk Level": st.column_config.TextColumn("Risk", help="Implementation risk")
            }
        )
        
        # Visual comparisons
        st.markdown("### Visual Comparison")
        
        # NPV comparison chart
        fig_npv = px.bar(
            comparison_df,
            x='scenario',
            y='NPV',
            color='NPV',
            color_continuous_scale='RdYlGn',
            title="NPV by Scenario"
        )
        
        fig_npv.add_hline(y=0, line_dash="dash", line_color="black")
        
        st.plotly_chart(fig_npv, use_container_width=True)
        
        # Multi-metric radar chart
        st.markdown("### Multi-Criteria Analysis")
        
        # Normalize metrics for radar chart
        metrics_for_radar = ['NPV', 'ROI %', 'Annual Net Benefit']
        
        fig_radar = go.Figure()
        
        for scenario in comparison_df['scenario']:
            scenario_data = comparison_df[comparison_df['scenario'] == scenario].iloc[0]
            
            # Normalize values (0-10 scale)
            values = []
            for metric in metrics_for_radar:
                if metric == 'NPV':
                    # Normalize NPV
                    min_npv = comparison_df['NPV'].min()
                    max_npv = comparison_df['NPV'].max()
                    if max_npv > min_npv:
                        normalized = (scenario_data['NPV'] - min_npv) / (max_npv - min_npv) * 10
                    else:
                        normalized = 5
                elif metric == 'ROI %':
                    # Normalize ROI
                    normalized = min(scenario_data['ROI %'] / 50, 10)  # 500% = 10
                else:
                    # Normalize Annual Net Benefit
                    max_benefit = comparison_df['Annual Net Benefit'].max()
                    normalized = (scenario_data['Annual Net Benefit'] / max_benefit) * 10 if max_benefit > 0 else 0
                
                values.append(normalized)
            
            # Add risk score (inverted - lower risk is better)
            risk_scores = {'Low': 10, 'Medium': 7, 'High': 4, 'Very High': 1}
            values.append(risk_scores.get(scenario_data['Risk Level'], 5))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=['NPV', 'ROI', 'Annual Benefit', 'Low Risk'],
                fill='toself',
                name=scenario
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            showlegend=True,
            title="Multi-Criteria Scenario Comparison"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Recommendations
        st.markdown("### Recommendations")
        
        # Find best scenario by NPV
        best_npv_scenario = comparison_df.loc[comparison_df['NPV'].idxmax(), 'scenario']
        best_roi_scenario = comparison_df.loc[comparison_df['ROI %'].idxmax(), 'scenario']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"**Highest NPV**: {best_npv_scenario}")
            best_npv_value = comparison_df.loc[comparison_df['NPV'].idxmax(), 'NPV']
            st.write(f"NPV: ${best_npv_value:,.0f}")
            
        with col2:
            st.success(f"**Highest ROI**: {best_roi_scenario}")
            best_roi_value = comparison_df.loc[comparison_df['ROI %'].idxmax(), 'ROI %']
            st.write(f"ROI: {best_roi_value:.1f}%")
        
        # Risk-adjusted recommendation
        # Simple scoring: NPV weight 40%, ROI weight 30%, Risk weight 30%
        comparison_df['Score'] = (
            comparison_df['NPV'] / comparison_df['NPV'].max() * 0.4 +
            comparison_df['ROI %'] / comparison_df['ROI %'].max() * 0.3 +
            comparison_df['Risk Level'].map({'Low': 1, 'Medium': 0.7, 'High': 0.4, 'Very High': 0.1}) * 0.3
        )
        
        best_overall = comparison_df.loc[comparison_df['Score'].idxmax(), 'scenario']
        
        st.info(f"**Risk-Adjusted Recommendation**: {best_overall}")
        st.write("This scenario provides the best balance of return and risk.")


def _interpret_elasticity(elasticity: float) -> str:
    """Interpret elasticity value."""
    abs_elasticity = abs(elasticity)
    
    if abs_elasticity < 0.5:
        return "Low sensitivity"
    elif abs_elasticity < 1.0:
        return "Moderate sensitivity"
    elif abs_elasticity < 2.0:
        return "High sensitivity"
    else:
        return "Very high sensitivity"