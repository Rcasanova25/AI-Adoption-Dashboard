import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Placeholder DataFrames (replace with your actual data loading)
growth_data = pd.DataFrame({
    'metric': ['AI Startups', 'AI Investment', 'GenAI Investment', 'Total AI R&D'],
    'cagr_5yr': [25, 18, 150, 20]
})

regional_growth = pd.DataFrame({
    'region': ['North America', 'Europe', 'Greater China', 'Asia Pacific (ex-China)', 'Rest of World'],
    'growth_2024': [15, 23, 27, 18, 10],
    'adoption_rate': [82, 65, 55, 48, 30],
    'investment_growth': [20, 28, 32, 25, 15]
})

training_emissions = pd.DataFrame({
    'model': ['GPT-2', 'Megatron-LM', 'LaMDA', 'Llama 3.1'],
    'carbon_tons': [0.03, 72, 600, 1000] # Adjusted values for demonstration
})

financial_impact = pd.DataFrame({
    'function': ['Marketing & Sales', 'Customer Service', 'HR', 'IT', 'Product Development', 'Supply Chain', 'Finance', 'Legal'],
    'companies_reporting_revenue_gains': [71, 45, 10, 30, 52, 28, 15, 5],
    'cost_savings': [65, 49, 30, 40, 35, 20, 25, 10]
})
financial_impact['adoption'] = [42, 23, 7, 22, 28, 23, 13, 15] # GenAI adoption rates added to financial_impact directly

ai_perception = pd.DataFrame({
    'generation': ['Gen Z', 'Millennials', 'Gen X', 'Baby Boomers'],
    'expect_job_change': [75, 68, 55, 40],
    'expect_job_replacement': [45, 40, 30, 20]
})

firm_size = pd.DataFrame({
    'size': ['1-4', '5-19', '20-99', '100-249', '250-499', '500-999', '1000-4999', '5000+'],
    'adoption': [3.5, 5.0, 8.0, 12.5, 22.0, 35.0, 48.0, 58.5]
})

sector_2018 = pd.DataFrame({
    'sector': ['Manufacturing', 'Information', 'Finance', 'Healthcare', 'Retail', 'Education', 'Other'],
    'firm_weighted': [12, 12, 10, 8, 7, 5, 9],
    'employment_weighted': [11, 13, 9, 7, 6, 4, 8]
})

def show_source_info(source_key):
    """Placeholder function to simulate showing data source info."""
    if source_key == 'mckinsey':
        return "Source: McKinsey & Company, 'The State of AI in 2024: Generative AI’s Breakout Year'"
    return f"Source information for {source_key} is not available."

# --- Streamlit Application Structure (assuming 'view_type' is selected elsewhere) ---

st.sidebar.title("AI Index Report 2025")
view_type = st.sidebar.radio("Select View", [
    "Investment Growth",
    "Regional Growth",
    "AI Cost Trends",
    "Labor Impact",
    "Environmental Impact",
    "Adoption Rates",
    "Firm Size Analysis"
])
data_year = st.sidebar.selectbox("Select Data Year", ["2025", "2018"], index=0)


if view_type == "Investment Growth":
    st.write("📈 **AI Investment Growth: Key Trends (AI Index Report 2025)**")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='5-Year CAGR (%)',
        x=growth_data['metric'],
        y=growth_data['cagr_5yr'],
        marker_color='#E74C3C',
        text=[f'{x:.1f}%' for x in growth_data['cagr_5yr']],
        textposition='outside'
    ))

    fig.update_layout(
        title="AI Investment Growth Rates",
        xaxis_title="Investment Category",
        yaxis_title="Growth Rate (%)",
        barmode='group',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("**Note:** GenAI shows exceptional 5-year CAGR due to starting from near-zero base in 2019")

elif view_type == "Regional Growth":
    st.write("🌍 **Regional AI Adoption Growth (AI Index Report 2025)**")

    # Create subplot figure
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Adoption Growth in 2024', 'Investment Growth vs Adoption Rate'),
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.15
    )

    # Bar chart for adoption growth
    fig.add_trace(
        go.Bar(
            x=regional_growth['region'],
            y=regional_growth['growth_2024'],
            text=[f'+{x}pp' for x in regional_growth['growth_2024']],
            textposition='outside',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'],
            name='2024 Growth',
            showlegend=False
        ),
        row=1, col=1
    )

    # Scatter plot for investment vs adoption
    fig.add_trace(
        go.Scatter(
            x=regional_growth['adoption_rate'],
            y=regional_growth['investment_growth'],
            mode='markers+text',
            marker=dict(
                size=regional_growth['growth_2024'],
                color=regional_growth['growth_2024'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="2024 Growth (pp)")
            ),
            text=regional_growth['region'],
            textposition='top center',
            showlegend=False
        ),
        row=1, col=2
    )

    fig.update_xaxes(title_text="Region", row=1, col=1)
    fig.update_yaxes(title_text="Growth (percentage points)", row=1, col=1)
    fig.update_xaxes(title_text="Current Adoption Rate (%)", row=1, col=2)
    fig.update_yaxes(title_text="Investment Growth (%)", row=1, col=2)

    fig.update_layout(height=450, title_text="Regional AI Adoption and Investment Dynamics")

    st.plotly_chart(fig, use_container_width=True)

    # Regional insights with metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fastest Growing", "Greater China", "+27pp adoption")
        st.write("**Also leads in:**")
        st.write("• Investment growth: +32%")
        st.write("• New AI startups: +45%")

    with col2:
        st.metric("Highest Adoption", "North America", "82% rate")
        st.write("**Characteristics:**")
        st.write("• Mature market")
        st.write("• Slower growth: +15pp")

    with col3:
        st.metric("Emerging Leader", "Europe", "+23pp growth")
        st.write("**Key drivers:**")
        st.write("• Regulatory clarity")
        st.write("• Public investment")

    # Competitive dynamics analysis
    st.subheader("🏁 Competitive Dynamics")

    # Create competitive positioning matrix
    fig2 = px.scatter(
        regional_growth,
        x='adoption_rate',
        y='growth_2024',
        size='investment_growth',
        color='region',
        title='Regional AI Competitive Positioning Matrix',
        labels={
            'adoption_rate': 'Current Adoption Rate (%)',
            'growth_2024': 'Adoption Growth Rate (pp)',
            'investment_growth': 'Investment Growth (%)'
        },
        height=400
    )

    # Add quadrant lines
    fig2.add_hline(y=regional_growth['growth_2024'].mean(), line_dash="dash", line_color="gray")
    fig2.add_vline(x=regional_growth['adoption_rate'].mean(), line_dash="dash", line_color="gray")

    # Add quadrant labels
    # Adjusted coordinates to center text within typical quadrant regions
    fig2.add_annotation(x=regional_growth['adoption_rate'].mean() - 15, y=regional_growth['growth_2024'].mean() + 5, text="High Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=regional_growth['adoption_rate'].mean() + 15, y=regional_growth['growth_2024'].mean() + 5, text="High Growth<br>High Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=regional_growth['adoption_rate'].mean() - 15, y=regional_growth['growth_2024'].mean() - 5, text="Low Growth<br>Low Base", showarrow=False, font=dict(color="gray"))
    fig2.add_annotation(x=regional_growth['adoption_rate'].mean() + 15, y=regional_growth['growth_2024'].mean() - 5, text="Low Growth<br>High Base", showarrow=False, font=dict(color="gray"))

    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    **Strategic Insights:**
    - **Greater China & Europe:** Aggressive catch-up strategy with high growth rates
    - **North America:** Market leader maintaining position with steady growth
    - **Competition intensifying:** Regional gaps narrowing as adoption accelerates globally
    """)

elif view_type == "AI Cost Trends":
    st.write("💰 **AI Cost Reduction: Dramatic Improvements (AI Index Report 2025)**")

    # Cost reduction visualization with context
    tab1, tab2, tab3 = st.tabs(["Inference Costs", "Hardware Improvements", "Cost Projections"])

    with tab1:
        # Enhanced cost reduction chart
        fig = go.Figure()

        # Add cost trajectory
        fig.add_trace(go.Scatter(
            x=['Nov 2022', 'Jan 2023', 'Jul 2023', 'Jan 2024', 'Oct 2024', 'Oct 2024\n(Gemini)'],
            y=[20.00, 10.00, 2.00, 0.50, 0.14, 0.07],
            mode='lines+markers',
            marker=dict(
                size=[15, 10, 10, 10, 15, 20],
                color=['red', 'orange', 'yellow', 'lightgreen', 'green', 'darkgreen']
            ),
            line=dict(width=3, color='gray', dash='dash'),
            text=['$20.00', '$10.00', '$2.00', '$0.50', '$0.14', '$0.07'],
            textposition='top center',
            name='Cost per Million Tokens',
            hovertemplate='Date: %{x}<br>Cost: %{text}<br>Reduction: %{customdata}<extra></extra>',
            customdata=['Baseline', '2x cheaper', '10x cheaper', '40x cheaper', '143x cheaper', '286x cheaper']
        ))

        # Add annotations for key milestones
        fig.add_annotation(
            x='Nov 2022', y=20,
            text="<b>GPT-3.5 Launch</b><br>$20/M tokens",
            showarrow=True,
            arrowhead=2,
            ax=0, ay=-40
        )

        fig.add_annotation(
            x='Oct 2024\n(Gemini)', y=0.07,
            text="<b>286x Cost Reduction</b><br>$0.07/M tokens",
            showarrow=True,
            arrowhead=2,
            ax=0, ay=40
        )

        fig.update_layout(
            title="AI Inference Cost Collapse: 286x Reduction in 2 Years",
            xaxis_title="Time Period",
            yaxis_title="Cost per Million Tokens ($)",
            yaxis_type="log",
            height=450,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        # Cost impact analysis
        col1, col2 = st.columns(2)

        with col1:
            st.write("**💡 What This Means:**")
            st.write("• Processing 1B tokens now costs $70 (was $20,000)")
            st.write("• Enables mass deployment of AI applications")
            st.write("• Makes AI accessible to smaller organizations")

        with col2:
            st.write("**📈 Rate of Improvement:**")
            st.write("• Prices falling 9-900x per year by task")
            st.write("• Outpacing Moore's Law significantly")
            st.write("• Driven by competition and efficiency gains")

    with tab2:
        # Hardware improvements
        hardware_metrics = pd.DataFrame({
            'metric': ['Performance Growth', 'Price/Performance', 'Energy Efficiency'],
            'annual_rate': [43, -30, 40],
            'cumulative_5yr': [680, -83, 538]
        })

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Annual Rate (%)',
            x=hardware_metrics['metric'],
            y=hardware_metrics['annual_rate'],
            marker_color=['#2ECC71' if x > 0 else '#E74C3C' for x in hardware_metrics['annual_rate']],
            text=[f'{x:+d}%' for x in hardware_metrics['annual_rate']],
            textposition='outside'
        ))

        fig.update_layout(
            title="ML Hardware Annual Improvement Rates",
            xaxis_title="Metric",
            yaxis_title="Annual Change (%)",
            height=400,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        **🚀 Hardware Revolution:**
        - Performance improving **43% annually** (16-bit operations)
        - Cost dropping **30% per year** for same performance
        - Energy efficiency gaining **40% annually**
        - Enabling larger models at lower costs
        """)

    with tab3:
        # Cost projections
        st.write("**Future Cost Projections**")

        # Create projection data
        years = list(range(2024, 2028))
        conservative = [0.07, 0.035, 0.018, 0.009]
        aggressive = [0.07, 0.014, 0.003, 0.0006]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=conservative,
            mode='lines+markers',
            name='Conservative (50% annual reduction)',
            line=dict(width=3, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(52, 152, 219, 0.1)'
        ))

        fig.add_trace(go.Scatter(
            x=years,
            y=aggressive,
            mode='lines+markers',
            name='Aggressive (80% annual reduction)',
            line=dict(width=3),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)'
        ))

        fig.update_layout(
            title="AI Cost Projections: 2024-2027",
            xaxis_title="Year",
            yaxis_title="Cost per Million Tokens ($)",
            yaxis_type="log",
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **📊 Projection Assumptions:**
        - **Conservative:** Based on historical semiconductor improvements
        - **Aggressive:** Based on current AI-specific optimization rates
        - By 2027, costs could be 1000-10,000x lower than 2022
        """)

elif view_type == "Labor Impact":
    st.write("👥 **AI's Impact on Jobs and Workers (AI Index Report 2025)**")

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Expect Job Changes",
            value="60%",
            delta="Within 5 years",
            help="Global respondents believing AI will change their jobs"
        )

    with col2:
        st.metric(
            label="Expect Job Replacement",
            value="36%",
            delta="Within 5 years",
            help="Believe AI will replace their current jobs"
        )

    with col3:
        st.metric(
            label="Skill Gap Narrowing",
            value="Confirmed",
            delta="Low-skilled benefit most",
            help="AI helps reduce inequality"
        )

    with col4:
        st.metric(
            label="Productivity Boost",
            value="14%",
            delta="For low-skilled workers",
            help="Highest gains for entry-level"
        )

    # Create comprehensive labor impact visualization
    tab1, tab2, tab3, tab4 = st.tabs(["Generational Views", "Skill Impact", "Job Transformation", "Policy Implications"])

    with tab1:
        # Enhanced generational visualization
        fig = go.Figure()

        # Job change expectations
        fig.add_trace(go.Bar(
            name='Expect Job Changes',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_change'],
            marker_color='#4ECDC4',
            text=[f'{x}%' for x in ai_perception['expect_job_change']],
            textposition='outside'
        ))

        # Job replacement expectations
        fig.add_trace(go.Bar(
            name='Expect Job Replacement',
            x=ai_perception['generation'],
            y=ai_perception['expect_job_replacement'],
            marker_color='#F38630',
            text=[f'{x}%' for x in ai_perception['expect_job_replacement']],
            textposition='outside'
        ))

        # Add average lines
        avg_change = ai_perception['expect_job_change'].mean()
        avg_replace = ai_perception['expect_job_replacement'].mean()

        fig.add_hline(y=avg_change, line_dash="dash", line_color="rgba(78, 205, 196, 0.5)",
                      annotation_text=f"Avg Change: {avg_change:.0f}%", annotation_position="right")
        fig.add_hline(y=avg_replace, line_dash="dash", line_color="rgba(243, 134, 48, 0.5)",
                      annotation_text=f"Avg Replace: {avg_replace:.0f}%", annotation_position="right")

        fig.update_layout(
            title="AI Job Impact Expectations by Generation",
            xaxis_title="Generation",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Generation insights
        st.info("""
        **Key Insights:**
        - **18pp gap** between Gen Z and Baby Boomers on job change expectations
        - Younger workers more aware of AI's transformative potential
        - All generations show concern but vary in urgency perception
        """)

    with tab2:
        # Skill impact analysis
        skill_impact = pd.DataFrame({
            'job_category': ['Entry-Level/Low-Skill', 'Mid-Level/Medium-Skill', 'Senior/High-Skill', 'Creative/Specialized'],
            'productivity_gain': [14, 9, 5, 7],
            'job_risk': [45, 38, 22, 15],
            'reskilling_need': [85, 72, 58, 65]
        })

        fig = go.Figure()

        # Create grouped bar chart
        # It's better to restructure the data for a grouped bar chart in Plotly Express or pivot it
        # For go.Figure, we need to iterate through metrics and add traces for each job category

        # Instead of iterating through categories for x, iterate through job categories for traces
        for category in skill_impact['job_category'].unique():
            subset = skill_impact[skill_impact['job_category'] == category]
            fig.add_trace(go.Bar(
                name=category,
                x=['Productivity Gain (%)', 'Job Risk (%)', 'Reskilling Need (%)'],
                y=[subset['productivity_gain'].iloc[0], subset['job_risk'].iloc[0], subset['reskilling_need'].iloc[0]],
                text=[f'{v}%' for v in [subset['productivity_gain'].iloc[0], subset['job_risk'].iloc[0], subset['reskilling_need'].iloc[0]]],
                textposition='outside'
            ))

        fig.update_layout(
            title="AI Impact by Job Category",
            xaxis_title="Impact Metric",
            yaxis_title="Percentage (%)",
            barmode='group',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        **Positive Finding:** AI provides greatest productivity boosts to entry-level workers,
        potentially reducing workplace inequality and accelerating skill development.
        """)

    with tab3:
        # Job transformation timeline
        transformation_data = pd.DataFrame({
            'timeframe': ['0-2 years', '2-5 years', '5-10 years', '10+ years'],
            'jobs_affected': [15, 35, 60, 80],
            'new_jobs_created': [10, 25, 45, 65],
            'net_impact': [5, 10, 15, 15]
        })

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=transformation_data['timeframe'],
            y=transformation_data['jobs_affected'],
            mode='lines+markers',
            name='Jobs Affected',
            line=dict(width=3, color='#E74C3C'),
            marker=dict(size=10),
            fill='tozeroy' # Changed 'tonexty' to 'tozeroy' for the first trace to fill to axis
        ))

        fig.add_trace(go.Scatter(
            x=transformation_data['timeframe'],
            y=transformation_data['new_jobs_created'],
            mode='lines+markers',
            name='New Jobs Created',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            fill='tozeroy'
        ))

        fig.update_layout(
            title="Projected Job Market Transformation Timeline",
            xaxis_title="Timeframe",
            yaxis_title="Percentage of Workforce (%)",
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **Transformation Patterns:**
        - Initial displacement in routine tasks
        - New roles emerge in AI management, ethics, and human-AI collaboration
        - Net positive effect expected long-term with proper reskilling
        """)

    with tab4:
        # Policy recommendations
        st.write("**Policy Recommendations for Workforce Transition**")

        policy_areas = pd.DataFrame({
            'area': ['Education Reform', 'Reskilling Programs', 'Safety Nets',
                     'Innovation Support', 'Regulation', 'Public-Private Partnership'],
            'priority': [95, 92, 85, 78, 72, 88],
            'current_investment': [45, 38, 52, 65, 58, 42]
        })

        fig = px.scatter(
            policy_areas,
            x='current_investment',
            y='priority',
            size='priority',
            text='area',
            color='area', # Added color by area for better distinction
            title='Policy Priority vs Current Investment',
            labels={
                'current_investment': 'Current Investment Level (%)',
                'priority': 'Priority Score (%)'
            },
            height=400
        )

        # Add quadrant dividers
        fig.add_hline(y=policy_areas['priority'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Priority", annotation_position="top left")
        fig.add_vline(x=policy_areas['current_investment'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Investment", annotation_position="top right")

        # Quadrant labels - Adjusted positions and content for clarity
        fig.add_annotation(x=policy_areas['current_investment'].mean() - 15, y=policy_areas['priority'].mean() + 5, text="High Priority<br>Low Investment",
                           showarrow=False, font=dict(color="red", size=10))
        fig.add_annotation(x=policy_areas['current_investment'].mean() + 15, y=policy_areas['priority'].mean() + 5, text="High Priority<br>High Investment",
                           showarrow=False, font=dict(color="green", size=10))
        fig.add_annotation(x=policy_areas['current_investment'].mean() - 15, y=policy_areas['priority'].mean() - 5, text="Low Priority<br>Low Investment",
                           showarrow=False, font=dict(color="gray", size=10))
        fig.add_annotation(x=policy_areas['current_investment'].mean() + 15, y=policy_areas['priority'].mean() - 5, text="Low Priority<br>High Investment",
                           showarrow=False, font=dict(color="gray", size=10))

        fig.update_traces(textposition='top center')

        st.plotly_chart(fig, use_container_width=True)

        st.warning("""
        **Critical Gaps:**
        - **Education Reform** and **Reskilling Programs** are high priority but underfunded
        - Need 2-3x increase in workforce development investment
        - Public-private partnerships essential for scale
        """)

elif view_type == "Environmental Impact":
    st.write("🌱 **Environmental Impact: AI's Growing Carbon Footprint (AI Index Report 2025)**")

    # Create comprehensive environmental dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["Training Emissions", "Energy Trends", "Mitigation Strategies", "Sustainability Metrics"])

    with tab1:
        # Enhanced emissions visualization
        fig = go.Figure()

        # Add bars for emissions
        fig.add_trace(go.Bar(
            x=training_emissions['model'],
            y=training_emissions['carbon_tons'],
            marker_color=['#90EE90', '#FFD700', '#FF6347', '#8B0000'],
            text=[f'{x:,.0f} tons' for x in training_emissions['carbon_tons']],
            textposition='outside',
            hovertemplate='Model: %{x}<br>Emissions: %{text}<br>Equivalent: %{customdata}<extra></extra>',
            customdata=['Negligible', '~125 cars/year', '~1,100 cars/year', '~1,900 cars/year']
        ))

        # Add trend line
        fig.add_trace(go.Scatter(
            x=training_emissions['model'],
            y=training_emissions['carbon_tons'],
            mode='lines',
            line=dict(width=3, color='red', dash='dash'),
            name='Exponential Growth Trend',
            showlegend=True
        ))

        fig.update_layout(
            title="Carbon Emissions from AI Model Training: Exponential Growth",
            xaxis_title="AI Model",
            yaxis_title="Carbon Emissions (tons CO₂)",
            yaxis_type="log", # Log scale is crucial for exponential growth visualization
            height=450,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Emissions context
        col1, col2 = st.columns(2)

        with col1:
            st.write("**📈 Growth Rate:**")
            st.write("• 900,000x increase from 2012 to 2024")
            st.write("• Doubling approximately every 2 years")
            st.write("• Driven by model size and compute needs")

        with col2:
            st.write("**🌍 Context:**")
            st.write("• Llama 3.1 = Annual emissions of 1,900 cars")
            st.write("• One training run = 8,930 tons CO₂")
            st.write("• Excludes inference and retraining")

    with tab2:
        # Energy trends and nuclear pivot
        st.write("**⚡ Energy Consumption and Nuclear Renaissance**")

        energy_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023, 2024, 2025],
            'ai_energy_twh': [2.1, 3.5, 5.8, 9.6, 16.2, 27.3],
            'nuclear_deals': [0, 0, 1, 3, 8, 15]
        })

        fig = go.Figure()

        # Energy consumption
        fig.add_trace(go.Bar(
            x=energy_data['year'],
            y=energy_data['ai_energy_twh'],
            name='AI Energy Use (TWh)',
            marker_color='#3498DB',
            yaxis='y',
            text=[f'{x:.1f} TWh' for x in energy_data['ai_energy_twh']],
            textposition='outside'
        ))

        # Nuclear deals
        fig.add_trace(go.Scatter(
            x=energy_data['year'],
            y=energy_data['nuclear_deals'],
            name='Nuclear Energy Deals',
            mode='lines+markers',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=10),
            yaxis='y2'
        ))

        fig.update_layout(
            title="AI Energy Consumption Driving Nuclear Energy Revival",
            xaxis_title="Year",
            yaxis=dict(title="Energy Consumption (TWh)", side="left"),
            yaxis2=dict(title="Nuclear Deals (#)", side="right", overlaying="y"),
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **🔋 Major Nuclear Agreements (2024-2025):**
        - Microsoft: Three Mile Island restart
        - Google: Kairos Power SMR partnership
        - Amazon: X-energy SMR development
        - Meta: Nuclear power exploration
        """)

    with tab3:
        # Mitigation strategies
        mitigation = pd.DataFrame({
            'strategy': ['Efficient Architectures', 'Renewable Energy', 'Model Reuse',
                         'Edge Computing', 'Quantum Computing', 'Carbon Offsets'],
            'potential_reduction': [40, 85, 95, 60, 90, 100],
            'adoption_rate': [65, 45, 35, 25, 5, 30],
            'timeframe': [1, 3, 1, 2, 7, 1]
        })

        fig = px.scatter(
            mitigation,
            x='adoption_rate',
            y='potential_reduction',
            size='timeframe',
            color='strategy',
            title='AI Sustainability Strategies: Impact vs Adoption',
            labels={
                'adoption_rate': 'Current Adoption Rate (%)',
                'potential_reduction': 'Potential Emission Reduction (%)',
                'timeframe': 'Implementation Time (years)'
            },
            height=400
        )

        # Add target zone
        fig.add_shape(
            type="rect",
            x0=70, x1=100,
            y0=70, y1=100,
            fillcolor="lightgreen",
            opacity=0.2,
            line_width=0
        )

        fig.add_annotation(
            x=85, y=85,
            text="Target Zone",
            showarrow=False,
            font=dict(color="green")
        )

        fig.update_traces(textposition='top center')

        st.plotly_chart(fig, use_container_width=True)

        st.success("""
        **Most Promising Strategies:**
        - **Model Reuse:** 95% reduction potential, needs ecosystem development
        - **Renewable Energy:** 85% reduction, requires infrastructure investment
        - **Efficient Architectures:** Quick wins with 40% reduction potential
        """)

    with tab4:
        # Sustainability metrics dashboard
        st.write("**Sustainability Performance Metrics**")

        # Create sustainability scorecard
        metrics = pd.DataFrame({
            'company': ['OpenAI', 'Google', 'Microsoft', 'Meta', 'Amazon'],
            'renewable_pct': [45, 78, 65, 52, 40],
            'efficiency_score': [7.2, 8.5, 7.8, 6.9, 7.5],
            'transparency_score': [6.5, 8.2, 7.9, 6.2, 7.0],
            'carbon_neutral_target': [2030, 2028, 2029, 2030, 2032]
        })

        fig = go.Figure()

        # Create radar chart
        categories = ['Renewable %', 'Efficiency', 'Transparency']

        for _, company in metrics.iterrows():
            values = [
                company['renewable_pct'] / 10,  # Scale to 10
                company['efficiency_score'],
                company['transparency_score']
            ]

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=company['company']
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="AI Company Sustainability Scores",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        st.info("""
        **Industry Trends:**
        - Increasing pressure for carbon neutrality
        - Hardware efficiency improving 40% annually
        - Growing focus on lifecycle emissions
        """)

elif view_type == "Adoption Rates":
    if "2025" in data_year:
        st.write("📊 **GenAI Adoption by Business Function (2025)**")

        # Enhanced function data with financial impact
        # function_data is already set from financial_impact.copy() above and 'adoption' column added.

        # Create comprehensive visualization
        fig = go.Figure()

        # Adoption rate bars
        fig.add_trace(go.Bar(
            x=financial_impact['function'],
            y=financial_impact['adoption'],
            name='GenAI Adoption Rate',
            marker_color='#3498DB',
            yaxis='y',
            text=[f'{x}%' for x in financial_impact['adoption']],
            textposition='outside'
        ))

        # Revenue impact line
        fig.add_trace(go.Scatter(
            x=financial_impact['function'],
            y=financial_impact['companies_reporting_revenue_gains'],
            mode='lines+markers',
            name='% Reporting Revenue Gains',
            line=dict(width=3, color='#2ECC71'),
            marker=dict(size=8),
            yaxis='y2'
        ))

        fig.update_layout(
            title='GenAI Adoption and Business Impact by Function',
            xaxis_tickangle=45,
            yaxis=dict(title="GenAI Adoption Rate (%)", side="left"),
            yaxis2=dict(title="% Reporting Revenue Gains", side="right", overlaying="y"),
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Function insights
        col1, col2 = st.columns(2)

        with col1:
            st.write("🎯 **Top Functions:**")
            st.write("• **Marketing & Sales:** 42% adoption, 71% see revenue gains")
            st.write("• **Product Development:** 28% adoption, 52% see revenue gains")
            st.write("• **Service Operations:** 23% adoption, 49% see cost savings")

        with col2:
            if st.button("📊 View Data Source", key="adoption_source"):
                with st.expander("Data Source", expanded=True):
                    st.info(show_source_info('mckinsey'))

        # Note about adoption definition
        st.info("**Note:** Adoption rates include any GenAI use (pilots, experiments, production) among firms using AI")

    else:
        # 2018 view
        weighting = st.sidebar.radio("Weighting Method", ["Firm-Weighted", "Employment-Weighted"])
        y_col = 'firm_weighted' if weighting == "Firm-Weighted" else 'employment_weighted'

        fig = px.bar(
            sector_2018,
            x='sector',
            y=y_col,
            title=f'AI Adoption by Sector (2018) - {weighting}',
            color=y_col,
            color_continuous_scale='blues',
            text=y_col
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(xaxis_tickangle=45, height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.write("🏭 **Key Insight**: Manufacturing and Information sectors led early AI adoption at 12% each")

elif view_type == "Firm Size Analysis":
    st.write("🏢 **AI Adoption by Firm Size**")

    # Enhanced visualization with annotations
    fig = go.Figure()

    # Main bar chart
    fig.add_trace(go.Bar(
        x=firm_size['size'],
        y=firm_size['adoption'],
        marker_color=firm_size['adoption'],
        marker_colorscale='Greens',
        text=[f'{x}%' for x in firm_size['adoption']],
        textposition='outside',
        hovertemplate='Size: %{x}<br>Adoption: %{y}%<br>Employees: %{customdata}<extra></extra>',
        customdata=firm_size['size']
    ))

    # Add trend line (polynomial fit)
    x_numeric = np.array(range(len(firm_size))) # Convert range to numpy array for polyfit
    z = np.polyfit(x_numeric, firm_size['adoption'], 2)
    p = np.poly1d(z)

    fig.add_trace(go.Scatter(
        x=firm_size['size'],
        y=p(x_numeric),
        mode='lines',
        line=dict(width=3, color='red', dash='dash'),
        name='Trend',
        showlegend=True
    ))

    # Add annotations for key thresholds
    fig.add_annotation(
        x='100-249', y=12.5,
        text="<b>SME Threshold</b><br>12.5% adoption",
        showarrow=True,
        arrowhead=2,
        ax=0, ay=-40
    )

    fig.add_annotation(
        x='5000+', y=58.5,
        text="<b>Enterprise Leaders</b><br>58.5% adoption",
        showarrow=True,
        arrowhead=2,
        ax=0, ay=-40
    )

    fig.update_layout(
        title='AI Adoption Shows Strong Correlation with Firm Size',
        xaxis_title='Number of Employees',
        yaxis_title='AI Adoption Rate (%)',
        height=500,
        showlegend=True
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

    st.info("""
    **📈 Key Insights:**
    - Strong exponential relationship between size and adoption
    - Resource constraints limit small firm adoption compared to larger enterprises
    - Targeted policies could help SMEs overcome adoption barriers.
    """)