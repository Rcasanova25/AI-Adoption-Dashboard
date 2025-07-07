"""
Adoption Rates view module for AI Adoption Dashboard - Dash Version.

This module provides visualizations for AI adoption rates across business
functions and sectors, with both current (2025) and historical (2018)
perspectives.
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
    Create the layout for Adoption Rates view.
    
    Args:
        data: Dictionary containing all loaded datasets
        persona: Current user persona
        
    Returns:
        html.Div: The complete view layout
    """
    
    # Extract relevant data
    view_data = extract_view_data(data)
    
    return html.Div([
        # Header section
        create_header_section(),
        
        # Year selector (replacing Streamlit's data_year filter)
        create_year_selector(),
        
        # Metrics section
        create_metrics_section(view_data),
        
        # Main charts section
        create_charts_section(),
        
        # Key insights
        create_insights_section(persona),
        
        # Data table section
        create_data_section(),
        
        # Source info
        create_source_section()
    ], className="adoption-rates-view")


def create_header_section() -> html.Div:
    """Create the header section."""
    return html.Div([
        html.H2("📈 AI Adoption Rates Analysis", className="mb-3"),
        html.P(
            "Track AI adoption rates across business functions and industry sectors from 2018 to 2025, "
            "highlighting the dramatic shift with GenAI technologies.",
            className="text-muted mb-4"
        ),
        html.Hr()
    ], className="header-section mb-4")


def create_year_selector() -> html.Div:
    """Create year selection control."""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Time Period:", className="fw-bold"),
                    dcc.RadioItems(
                        id="year-selector",
                        options=[
                            {"label": "2025 (Current - GenAI Era)", "value": "2025"},
                            {"label": "2018 (Historical - Pre-GenAI)", "value": "2018"},
                            {"label": "Compare Both", "value": "compare"}
                        ],
                        value="2025",
                        inline=True,
                        className="mt-2"
                    )
                ], width=12)
            ])
        ])
    ], className="mb-4 shadow-sm")


def create_metrics_section(data: Dict[str, Any]) -> html.Div:
    """Create key metrics cards."""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Highest Adoption", className="text-muted mb-2"),
                    html.H3("Service Ops", className="mb-1"),
                    html.P("42% GenAI adoption", className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Revenue Impact", className="text-muted mb-2"),
                    html.H3("71%", className="mb-1"),
                    html.P("Report revenue gains", className="text-success mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Growth Since 2018", className="text-muted mb-2"),
                    html.H3("5.2x", className="mb-1"),
                    html.P("Increase in adoption", className="text-info mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Tech Sector Lead", className="text-muted mb-2"),
                    html.H3("85%", className="mb-1"),
                    html.P("AI implementation", className="text-primary mb-0 small")
                ])
            ], className="metric-card shadow-sm")
        ], width=6, lg=3, className="mb-3"),
    ], className="metrics-section mb-4")


def create_charts_section() -> html.Div:
    """Create the main charts section."""
    return html.Div([
        # Function adoption chart
        dbc.Card([
            dbc.CardBody([
                dcc.Loading(
                    children=[
                        dcc.Graph(id="function-adoption-chart", className="mb-3")
                    ],
                    type="default"
                )
            ])
        ], className="mb-4 shadow-sm"),
        
        # Sector comparison chart
        dbc.Card([
            dbc.CardBody([
                dcc.Loading(
                    children=[
                        dcc.Graph(id="sector-comparison-chart")
                    ],
                    type="default"
                )
            ])
        ], className="mb-4 shadow-sm")
    ])


def create_insights_section(persona: str) -> html.Div:
    """Create key insights section tailored to persona."""
    
    # Persona-specific insights
    insights_by_persona = {
        "Business Leader": [
            "Service Operations leads GenAI adoption at 42%, offering immediate ROI opportunities",
            "71% of companies report revenue gains from AI implementation",
            "Marketing and Sales show 23% adoption with strong customer engagement benefits"
        ],
        "Policymaker": [
            "Technology sector leads with 85% adoption, creating competitive advantages",
            "Significant sector disparities suggest need for targeted support programs",
            "Rapid GenAI adoption requires updated regulatory frameworks"
        ],
        "Researcher": [
            "5.2x growth in adoption from 2018 to 2025 indicates technology maturation",
            "Function-specific adoption patterns reveal operational vs strategic AI use",
            "GenAI marks a paradigm shift from specialized to general-purpose AI"
        ]
    }
    
    # Get insights for current persona or default
    insights = insights_by_persona.get(persona, [
        "AI adoption has grown exponentially, with GenAI accelerating the trend",
        "Service operations and customer-facing functions lead adoption rates",
        "Significant opportunities remain in HR, Strategy, and R&D functions"
    ])
    
    return dbc.Card([
        dbc.CardBody([
            html.H5("Key Insights", className="mb-3"),
            html.Ul([html.Li(insight) for insight in insights])
        ])
    ], className="insights-section mb-4 shadow-sm")


def create_data_section() -> html.Div:
    """Create the detailed data section."""
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H5("Detailed Data", className="d-inline-block mb-3"),
                    dbc.Button(
                        "Show/Hide",
                        id="toggle-adoption-data",
                        color="secondary",
                        size="sm",
                        className="float-end"
                    )
                ]),
                dbc.Collapse(
                    html.Div(id="adoption-data-table"),
                    id="adoption-data-collapse",
                    is_open=False
                )
            ])
        ], className="shadow-sm")
    ], className="data-section mb-4")


def create_source_section() -> html.Div:
    """Create source information section."""
    return html.Div([
        html.Hr(className="mt-5"),
        html.P([
            html.I(className="fas fa-info-circle me-2"),
            "Data Sources: Stanford AI Index 2025, McKinsey State of AI Report, OECD AI Adoption Survey"
        ], className="text-muted small"),
        html.P([
            html.I(className="fas fa-clock me-2"),
            "Last Updated: January 2025 | Historical baseline: 2018"
        ], className="text-muted small mb-0")
    ], className="source-section")


# Callbacks for interactivity
@callback(
    Output("function-adoption-chart", "figure"),
    Input("year-selector", "value"),
    prevent_initial_call=False
)
def update_function_chart(selected_year: str):
    """Update function adoption chart based on year selection."""
    
    if selected_year == "2025" or selected_year == "compare":
        # 2025 GenAI adoption data
        functions = ["Service Ops", "Marketing", "Product Dev", "Sales", "Manufacturing", 
                    "Supply Chain", "Strategy", "HR", "Risk", "R&D"]
        adoption_2025 = [42, 23, 7, 22, 28, 23, 13, 15, 8, 12]
        revenue_impact = [71, 65, 58, 63, 67, 61, 55, 52, 48, 54]
        
        fig = go.Figure()
        
        # Add 2025 data
        fig.add_trace(
            go.Bar(
                x=functions,
                y=adoption_2025,
                name="2025 GenAI Adoption",
                marker_color="#3498DB",
                text=[f"{x}%" for x in adoption_2025],
                textposition="outside"
            )
        )
        
        if selected_year == "compare":
            # Add 2018 data for comparison
            adoption_2018 = [8, 4, 2, 5, 6, 4, 3, 3, 2, 3]
            fig.add_trace(
                go.Bar(
                    x=functions,
                    y=adoption_2018,
                    name="2018 Adoption",
                    marker_color="#95A5A6",
                    text=[f"{x}%" for x in adoption_2018],
                    textposition="outside"
                )
            )
        
        # Add revenue impact line
        fig.add_trace(
            go.Scatter(
                x=functions,
                y=revenue_impact,
                mode="lines+markers",
                name="% Reporting Revenue Gains",
                line=dict(width=3, color="#2ECC71"),
                marker=dict(size=8),
                yaxis="y2"
            )
        )
        
        fig.update_layout(
            title="AI Adoption by Business Function",
            xaxis_tickangle=45,
            yaxis=dict(title="Adoption Rate (%)", side="left"),
            yaxis2=dict(title="% Reporting Revenue Gains", side="right", overlaying="y"),
            height=500,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            template="plotly_white"
        )
        
    else:  # 2018
        # 2018 traditional AI adoption data
        functions = ["Manufacturing", "Technology", "Sales", "Supply Chain", "Service Ops",
                    "Marketing", "Finance", "Strategy", "HR", "Legal"]
        adoption_2018 = [12, 10, 8, 7, 8, 4, 5, 3, 3, 2]
        
        fig = px.bar(
            x=functions,
            y=adoption_2018,
            title="AI Adoption by Business Function (2018)",
            labels={"x": "Business Function", "y": "Adoption Rate (%)"},
            color_discrete_sequence=["#95A5A6"]
        )
        
        fig.update_traces(text=[f"{x}%" for x in adoption_2018], textposition="outside")
        fig.update_layout(
            xaxis_tickangle=45,
            height=500,
            template="plotly_white"
        )
    
    return fig


@callback(
    Output("sector-comparison-chart", "figure"),
    Input("year-selector", "value"),
    prevent_initial_call=False
)
def update_sector_chart(selected_year: str):
    """Update sector comparison chart."""
    
    sectors = ["Technology", "Financial Services", "Healthcare", "Retail", 
               "Manufacturing", "Energy", "Education", "Government"]
    
    if selected_year == "2025":
        adoption = [85, 72, 68, 61, 58, 45, 38, 32]
        title = "AI Adoption by Industry Sector (2025)"
        color = "#E74C3C"
    elif selected_year == "2018":
        adoption = [32, 28, 15, 18, 22, 12, 8, 5]
        title = "AI Adoption by Industry Sector (2018)"
        color = "#95A5A6"
    else:  # compare
        # Create grouped bar chart
        fig = go.Figure()
        
        adoption_2018 = [32, 28, 15, 18, 22, 12, 8, 5]
        adoption_2025 = [85, 72, 68, 61, 58, 45, 38, 32]
        
        fig.add_trace(go.Bar(
            name='2018',
            x=sectors,
            y=adoption_2018,
            marker_color='#95A5A6'
        ))
        
        fig.add_trace(go.Bar(
            name='2025',
            x=sectors,
            y=adoption_2025,
            marker_color='#E74C3C'
        ))
        
        fig.update_layout(
            title="AI Adoption by Industry Sector: 2018 vs 2025",
            xaxis_tickangle=45,
            yaxis_title="Adoption Rate (%)",
            barmode='group',
            height=500,
            template="plotly_white",
            hovermode="x unified"
        )
        
        return fig
    
    # Single year chart
    fig = px.bar(
        x=sectors,
        y=adoption,
        title=title,
        labels={"x": "Industry Sector", "y": "Adoption Rate (%)"},
        color_discrete_sequence=[color]
    )
    
    fig.update_traces(text=[f"{x}%" for x in adoption], textposition="outside")
    fig.update_layout(
        xaxis_tickangle=45,
        height=500,
        template="plotly_white"
    )
    
    return fig


@callback(
    [Output("adoption-data-collapse", "is_open"),
     Output("adoption-data-table", "children")],
    [Input("toggle-adoption-data", "n_clicks")],
    [State("adoption-data-collapse", "is_open"),
     State("year-selector", "value")],
    prevent_initial_call=True
)
def toggle_data_table(n_clicks: int, is_open: bool, selected_year: str):
    """Toggle detailed data table."""
    if n_clicks:
        new_state = not is_open
        
        if new_state:
            # Create data based on selection
            if selected_year == "2025":
                df = pd.DataFrame({
                    "Function": ["Service Ops", "Marketing", "Manufacturing", "Supply Chain", 
                                "Sales", "Product Dev", "HR", "Strategy"],
                    "2025 Adoption (%)": [42, 23, 28, 23, 22, 7, 15, 13],
                    "Revenue Impact (%)": [71, 65, 67, 61, 63, 58, 52, 55],
                    "Cost Reduction (%)": [45, 38, 52, 48, 35, 42, 28, 32]
                })
            else:
                df = pd.DataFrame({
                    "Sector": ["Technology", "Financial Services", "Manufacturing", "Healthcare",
                              "Retail", "Energy", "Education", "Government"],
                    "2018 Adoption (%)": [32, 28, 22, 15, 18, 12, 8, 5],
                    "2025 Adoption (%)": [85, 72, 58, 68, 61, 45, 38, 32],
                    "Growth Multiple": [2.7, 2.6, 2.6, 4.5, 3.4, 3.8, 4.8, 6.4]
                })
            
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in df.columns],
                style_cell={'textAlign': 'left', 'padding': '10px'},
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
                sort_action="native",
                page_size=10
            )
            
            return new_state, table
        else:
            return new_state, html.Div()
    
    return is_open, dash.no_update


# Helper functions
def extract_view_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant data for adoption rates view."""
    view_data = {}
    
    # Extract financial impact data
    if "mckinsey_financial_impact" in data:
        view_data["financial_impact"] = data["mckinsey_financial_impact"].get("data")
    
    # Extract sector data
    if "ai_index_industry_adoption" in data:
        view_data["sector_data"] = data["ai_index_industry_adoption"].get("data")
    
    # Extract GenAI adoption data
    if "stanford_investment_trends" in data:
        view_data["genai_data"] = data["stanford_investment_trends"].get("data")
    
    return view_data