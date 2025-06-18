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
            hovertemplate='Date: %{x}<br>Cost: %{text}<br>Reduction: %{customdata}<extra