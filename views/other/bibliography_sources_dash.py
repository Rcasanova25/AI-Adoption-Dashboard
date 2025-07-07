"""
TEMPLATE FOR CONVERTING STREAMLIT VIEWS TO DASH
===============================================

This template provides the standard pattern for converting any Streamlit view to Dash.
Copy this template and modify it for each view conversion.

Key Conversion Patterns:
- st.title() → html.H2()
- st.columns() + st.metric() → dbc.Row() + metric cards
- st.selectbox() → dcc.Dropdown()
- st.plotly_chart() → dcc.Graph() + callback
- st.dataframe() → dash_table.DataTable()
- st.expander() → dbc.Collapse() or dbc.Accordion()
"""

import dash
from dash import html, dcc, Input, Output, State, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def create_layout(data: Dict[str, Any], persona: str = "General") -> html.Div:
    """
    Create the layout for bibliography_sources view.
    
    Args:
        data: Dictionary containing all loaded datasets
        persona: Current user persona
        
    Returns:
        html.Div: The complete view layout
    """
    
    # Extract data for this view
    view_data = extract_view_data(data)
    
    return html.Div([
        # Header section (convert from st.title, st.markdown)
        create_header_section(),
        
        # Metrics section (convert from st.columns + st.metric)
        create_metrics_section(view_data),
        
        # Controls section (convert from st.selectbox, st.slider, etc.)
        create_controls_section(view_data),
        
        # Main chart section (convert from st.plotly_chart)
        create_chart_section(),
        
        # Additional insights section
        create_insights_section(),
        
        # Data table section (convert from st.dataframe)
        create_data_section(),
        
        # Source info section (convert from st.caption)
        create_source_section(view_data)
    ], className="view-container")


def create_header_section() -> html.Div:
    """Convert Streamlit header to Dash header."""
    return html.Div([
        html.H2("📊 View Title", className="view-title mb-3"),
        html.P(
            "Analysis view for Bibliography Sources", 
            className="view-description text-muted mb-4"
        ),
        html.Hr()
    ], className="header-section mb-4")


def create_metrics_section(data: pd.DataFrame) -> html.Div:
    """Convert st.columns + st.metric to Dash metric cards."""
    # Calculate metrics from data
    metric1_value = "92%"  # Calculate from data
    metric1_delta = "↗ 8%"
    
    metric2_value = "15.8K"
    metric2_delta = "↗ 2.6K"
    
    metric3_value = "$156B"
    metric3_delta = "↗ $24B"
    
    metric4_value = "72%"
    metric4_delta = "↗ 15%"
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Metric 1 Title", className="text-muted mb-2"),
                    html.H3(metric1_value, className="mb-1"),
                    html.P(metric1_delta, className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Metric 2 Title", className="text-muted mb-2"),
                    html.H3(metric2_value, className="mb-1"),
                    html.P(metric2_delta, className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Metric 3 Title", className="text-muted mb-2"),
                    html.H3(metric3_value, className="mb-1"),
                    html.P(metric3_delta, className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Metric 4 Title", className="text-muted mb-2"),
                    html.H3(metric4_value, className="mb-1"),
                    html.P(metric4_delta, className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
    ], className="metrics-section mb-4")


def create_controls_section(data: pd.DataFrame) -> html.Div:
    """Convert Streamlit controls to Dash controls."""
    return dbc.Card([
        dbc.CardBody([
            html.H5("Filters & Controls", className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("Time Period:", className="fw-bold"),
                    dcc.Dropdown(
                        id="time-period-filter",
                        options=[
                            {"label": "All Years (2018-2025)", "value": "all"},
                            {"label": "Last 3 Years", "value": "3y"},
                            {"label": "Last Year", "value": "1y"},
                            {"label": "2025 Only", "value": "2025"}
                        ],
                        value="all",
                        clearable=False
                    )
                ], width=12, md=4, className="mb-3"),
                
                dbc.Col([
                    html.Label("Industry Sector:", className="fw-bold"),
                    dcc.Dropdown(
                        id="industry-filter",
                        options=[
                            {"label": "All Industries", "value": "all"},
                            {"label": "Technology", "value": "tech"},
                            {"label": "Healthcare", "value": "health"},
                            {"label": "Financial Services", "value": "finance"},
                            {"label": "Manufacturing", "value": "manufacturing"}
                        ],
                        value="all",
                        clearable=False
                    )
                ], width=12, md=4, className="mb-3"),
                
                dbc.Col([
                    html.Label("Chart Type:", className="fw-bold"),
                    dcc.RadioItems(
                        id="chart-type-selector",
                        options=[
                            {"label": "Bar Chart", "value": "bar"},
                            {"label": "Line Chart", "value": "line"},
                            {"label": "Area Chart", "value": "area"}
                        ],
                        value="bar",
                        inline=True,
                        className="mt-2"
                    )
                ], width=12, md=4, className="mb-3")
            ])
        ])
    ], className="controls-section mb-4 shadow-sm")


def create_chart_section() -> html.Div:
    """Convert st.plotly_chart to Dash chart with loading."""
    return dbc.Card([
        dbc.CardBody([
            dcc.Loading(
                id="chart-loading",
                children=[
                    dcc.Graph(
                        id="main-chart",
                        className="main-chart",
                        config={"displayModeBar": True, "displaylogo": False}
                    )
                ],
                type="default"
            )
        ])
    ], className="chart-section mb-4 shadow-sm")


def create_insights_section() -> html.Div:
    """Create insights section (replaces st.expander)."""
    return dbc.Card([
        dbc.CardBody([
            html.H5("Key Insights", className="mb-3"),
            dbc.Accordion([
                dbc.AccordionItem([
                    html.Ul([
                        html.Li("Insight 1: AI adoption has grown exponentially..."),
                        html.Li("Insight 2: Enterprise adoption leads consumer..."),
                        html.Li("Insight 3: GenAI marks a paradigm shift...")
                    ])
                ], title="Adoption Trends", item_id="1"),
                
                dbc.AccordionItem([
                    html.Ul([
                        html.Li("Technology sector leads with 92% adoption..."),
                        html.Li("Healthcare shows fastest growth rate..."),
                        html.Li("Manufacturing focuses on operational AI...")
                    ])
                ], title="Industry Analysis", item_id="2"),
                
                dbc.AccordionItem([
                    html.Ul([
                        html.Li("2025-2027: Consolidation phase expected..."),
                        html.Li("AI native companies will emerge..."),
                        html.Li("Regulation will shape adoption patterns...")
                    ])
                ], title="Future Outlook", item_id="3")
            ], start_collapsed=True, always_open=False)
        ])
    ], className="insights-section mb-4 shadow-sm")


def create_data_section() -> html.Div:
    """Convert st.dataframe to Dash data table."""
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H5("Detailed Data", className="d-inline-block mb-3"),
                    dbc.Button(
                        "Show/Hide Data",
                        id="toggle-data-btn",
                        color="secondary",
                        size="sm",
                        className="float-end"
                    )
                ]),
                dbc.Collapse(
                    html.Div(id="data-table-container"),
                    id="data-collapse",
                    is_open=False
                )
            ])
        ], className="shadow-sm")
    ], className="data-section mb-4")


def create_source_section(data: Dict[str, Any]) -> html.Div:
    """Create source information section."""
    return html.Div([
        html.Hr(className="mt-5"),
        html.P([
            html.I(className="fas fa-info-circle me-2"),
            "Data Sources: Stanford AI Index 2025, McKinsey Global Institute, OECD AI Report"
        ], className="text-muted small"),
        html.P([
            html.I(className="fas fa-clock me-2"),
            "Last Updated: January 2025"
        ], className="text-muted small mb-0")
    ], className="source-section")


# Callbacks for interactivity
@callback(
    Output("main-chart", "figure"),
    [Input("time-period-filter", "value"),
     Input("industry-filter", "value"),
     Input("chart-type-selector", "value")],
    prevent_initial_call=False
)
def update_main_chart(time_period: str, industry: str, chart_type: str):
    """Update chart based on user selections."""
    try:
        # Filter data based on selections
        df = get_filtered_data(time_period, industry)
        
        # Create chart based on type
        if chart_type == "bar":
            fig = px.bar(
                df, 
                x="year", 
                y="adoption_rate",
                title="AI Adoption Rate Over Time",
                labels={"adoption_rate": "Adoption Rate (%)", "year": "Year"},
                color_discrete_sequence=["#0066CC"]
            )
        elif chart_type == "line":
            fig = px.line(
                df,
                x="year",
                y="adoption_rate",
                title="AI Adoption Rate Over Time",
                labels={"adoption_rate": "Adoption Rate (%)", "year": "Year"},
                markers=True
            )
        else:  # area
            fig = px.area(
                df,
                x="year",
                y="adoption_rate",
                title="AI Adoption Rate Over Time",
                labels={"adoption_rate": "Adoption Rate (%)", "year": "Year"}
            )
        
        # Update layout
        fig.update_layout(
            height=500,
            template="plotly_white",
            hovermode="x unified",
            showlegend=False
        )
        
        fig.update_xaxis(dtick=1)
        fig.update_yaxis(tickformat=".0f", ticksuffix="%")
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating chart: {str(e)}")
        # Return empty figure with error message
        return {
            "data": [],
            "layout": {
                "title": "Error loading chart",
                "annotations": [{
                    "text": f"Error: {str(e)}",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"size": 14, "color": "red"}
                }]
            }
        }


@callback(
    [Output("data-collapse", "is_open"),
     Output("data-table-container", "children")],
    [Input("toggle-data-btn", "n_clicks")],
    [State("data-collapse", "is_open"),
     State("time-period-filter", "value"),
     State("industry-filter", "value")],
    prevent_initial_call=True
)
def toggle_data_table(n_clicks: int, is_open: bool, time_period: str, industry: str):
    """Toggle data table visibility and update content."""
    if n_clicks:
        new_state = not is_open
        
        if new_state:
            # Load and format data
            df = get_filtered_data(time_period, industry)
            
            # Create data table
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in df.columns],
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Inter, sans-serif'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10,
                sort_action="native",
                filter_action="native"
            )
            
            return new_state, table
        else:
            return new_state, html.Div()
    
    return is_open, dash.no_update


# Helper functions
def extract_view_data(data: Dict[str, Any]) -> pd.DataFrame:
    """Extract and prepare data for this specific view."""
    # This function extracts the relevant data for this view
    # Keep your existing data processing logic here
    
    # Example: extract adoption rates data
    if "ai_index_adoption_rates" in data:
        return data["ai_index_adoption_rates"].get("data", pd.DataFrame())
    
    # Return mock data if real data not available
    return pd.DataFrame({
        "year": list(range(2018, 2026)),
        "adoption_rate": [15, 22, 31, 42, 58, 72, 85, 92]
    })


def get_filtered_data(time_period: str = "all", industry: str = "all") -> pd.DataFrame:
    """Apply filters to data."""
    # Get base data
    df = pd.DataFrame({
        "year": list(range(2018, 2026)),
        "adoption_rate": [15, 22, 31, 42, 58, 72, 85, 92]
    })
    
    # Apply time period filter
    if time_period == "3y":
        df = df[df["year"] >= 2023]
    elif time_period == "1y":
        df = df[df["year"] >= 2024]
    elif time_period == "2025":
        df = df[df["year"] == 2025]
    
    # Apply industry filter (would filter by industry in real implementation)
    
    return df