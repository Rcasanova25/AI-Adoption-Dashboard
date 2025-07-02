#!/usr/bin/env python3
"""
Simple Vizro Dashboard Demo for AI Adoption Analytics
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from vizro import Vizro
from vizro.models import Dashboard, Page, Graph, Card, Container
from vizro.models.types import capture

# Create sample data
def create_sample_data():
    """Create sample data for the dashboard"""
    
    # Adoption data by sector and year
    years = [2020, 2021, 2022, 2023, 2024]
    sectors = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail']
    
    data_rows = []
    for year in years:
        for sector in sectors:
            data_rows.append({
                'year': year,
                'sector': sector,
                'adoption_rate': 30 + (year - 2020) * 10 + hash(sector) % 20,
                'roi_percentage': 80 + (year - 2020) * 15 + hash(sector) % 30,
                'productivity_index': 0.8 + (year - 2020) * 0.2 + (hash(sector) % 20) / 100
            })
    
    return pd.DataFrame(data_rows)

# Create charts using @capture decorator
@capture("adoption_trends")
def create_adoption_trends_chart():
    """Create adoption trends chart"""
    df = create_sample_data()
    
    fig = px.line(
        df.groupby('year')['adoption_rate'].mean().reset_index(),
        x='year',
        y='adoption_rate',
        title='AI Adoption Trends Over Time',
        markers=True
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Year",
        yaxis_title="Adoption Rate (%)",
        template="plotly_white"
    )
    
    return fig

@capture("sector_comparison")
def create_sector_comparison_chart():
    """Create sector comparison chart"""
    df = create_sample_data()
    
    fig = px.bar(
        df.groupby('sector')['adoption_rate'].mean().reset_index(),
        x='sector',
        y='adoption_rate',
        title='AI Adoption by Industry Sector',
        color='adoption_rate',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Sector",
        yaxis_title="Adoption Rate (%)",
        template="plotly_white"
    )
    
    return fig

@capture("roi_analysis")
def create_roi_analysis_chart():
    """Create ROI analysis chart"""
    df = create_sample_data()
    
    fig = px.scatter(
        df,
        x='adoption_rate',
        y='roi_percentage',
        color='sector',
        size='productivity_index',
        title='ROI vs Adoption Rate by Sector',
        hover_data=['year', 'productivity_index']
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Adoption Rate (%)",
        yaxis_title="ROI (%)",
        template="plotly_white"
    )
    
    return fig

@capture("productivity_trends")
def create_productivity_trends_chart():
    """Create productivity trends chart"""
    df = create_sample_data()
    
    fig = px.line(
        df.groupby(['year', 'sector'])['productivity_index'].mean().reset_index(),
        x='year',
        y='productivity_index',
        color='sector',
        title='Productivity Index Trends by Sector',
        markers=True
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Year",
        yaxis_title="Productivity Index",
        template="plotly_white"
    )
    
    return fig

def main():
    """Create and run the Vizro dashboard"""
    
    print("Creating AI Adoption Analytics Dashboard...")
    
    # Create dashboard pages
    overview_page = Page(
        title="Overview",
        components=[
            Card(
                text="""
                # AI Adoption Analytics Dashboard
                
                This dashboard provides comprehensive insights into AI adoption trends across different sectors.
                
                **Key Metrics:**
                - Adoption Rates by Sector
                - ROI Analysis
                - Productivity Impact
                - Temporal Trends
                """,
                id="overview_card"
            ),
            Graph(
                figure=create_adoption_trends_chart,
                id="adoption_trends"
            ),
            Graph(
                figure=create_sector_comparison_chart,
                id="sector_comparison"
            )
        ],
        id="overview_page"
    )
    
    analysis_page = Page(
        title="Analysis",
        components=[
            Card(
                text="""
                # Detailed Analysis
                
                Explore the relationships between AI adoption, ROI, and productivity across different sectors.
                """,
                id="analysis_header"
            ),
            Graph(
                figure=create_roi_analysis_chart,
                id="roi_analysis"
            ),
            Graph(
                figure=create_productivity_trends_chart,
                id="productivity_trends"
            )
        ],
        id="analysis_page"
    )
    
    # Create the dashboard
    dashboard = Dashboard(
        title="AI Adoption Analytics",
        pages=[overview_page, analysis_page],
        theme="vizro_dark"
    )
    
    # Build and run the dashboard
    app = Vizro()
    app.build(dashboard)
    
    print("Dashboard created successfully!")
    print("Launching dashboard at http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(host="127.0.0.1", port=8050, debug=True)
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error running dashboard: {e}")

if __name__ == "__main__":
    main() 