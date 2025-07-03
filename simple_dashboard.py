# -*- coding: utf-8 -*-
"""
Simple AI Adoption Dashboard
A clean, working Dash application
"""

import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AI Adoption Dashboard"
app.config.suppress_callback_exceptions = True

# Add URL component for callbacks
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Create sample data
def create_data():
    years = list(range(2018, 2026))
    historical_data = pd.DataFrame({
        'year': years,
        'ai_adoption_rate': [5, 8, 12, 18, 25, 35, 55, 78],
        'investment_billions': [10, 15, 25, 40, 60, 100, 150, 252.3]
    })
    
    industry_data = pd.DataFrame({
        'industry': ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail'],
        'adoption_rate': [91, 85, 72, 68, 79],
        'roi_multiplier': [3.2, 2.8, 2.5, 2.1, 2.9]
    })
    
    return historical_data, industry_data

# Create charts
def create_adoption_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['ai_adoption_rate'],
        mode='lines+markers', name='AI Adoption Rate',
        line=dict(color='#1f77b4', width=3)
    ))
    fig.update_layout(
        title='AI Adoption Trends (2018-2025)',
        xaxis_title='Year', yaxis_title='Adoption Rate (%)',
        template='plotly_white', height=400
    )
    return fig

def create_investment_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['year'], y=data['investment_billions'],
        mode='lines+markers', name='AI Investment',
        line=dict(color='#2ca02c', width=3), fill='tonexty'
    ))
    fig.update_layout(
        title='Global AI Investment Trends',
        xaxis_title='Year', yaxis_title='Investment (Billions USD)',
        template='plotly_white', height=400
    )
    return fig

def create_industry_chart(data):
    fig = px.bar(data, x='industry', y=['adoption_rate', 'roi_multiplier'],
                 title='Industry Performance Comparison',
                 barmode='group')
    fig.update_layout(template='plotly_white', height=400)
    return fig

# Create metric cards
def create_metric_card(title, value, delta, color="primary"):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H3(value, className=f"text-{color} mb-1"),
                html.H6(title, className="text-muted mb-1"),
                html.Small(delta, className="text-success")
            ], className="text-center")
        ])
    ], className="h-100 shadow-sm")

# Main layout
main_layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("AI Adoption Dashboard", className="text-center mb-2"),
            html.P("Comprehensive analysis of AI adoption trends from 2018 to 2025", 
                   className="text-center text-muted lead")
        ])
    ], className="mb-4"),
    
    # Key metrics
    dbc.Row([
        dbc.Col([create_metric_card("Overall AI Adoption", "78%", "+23pp from 2023", "primary")], width=3),
        dbc.Col([create_metric_card("GenAI Adoption", "71%", "+38pp from 2023", "success")], width=3),
        dbc.Col([create_metric_card("2024 Investment", "$252.3B", "+44.5% YoY", "warning")], width=3),
        dbc.Col([create_metric_card("Productivity Gain", "3.2x", "+0.7x vs 2023", "info")], width=3)
    ], className="mb-4"),
    
    # Charts
    dbc.Row([
        dbc.Col([dcc.Graph(id='adoption-chart')], width=6),
        dbc.Col([dcc.Graph(id='investment-chart')], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([dcc.Graph(id='industry-chart')], width=12)
    ], className="mb-4"),
    
    # Insights
    dbc.Row([
        dbc.Col([
            html.H3("Key Insights", className="mb-3"),
            dbc.Alert([
                html.H5("Rapid Growth"),
                html.P("AI adoption has accelerated dramatically since 2023, with generative AI driving much of the recent growth.")
            ], color="success", className="mb-3"),
            dbc.Alert([
                html.H5("Investment Surge"),
                html.P("Global AI investment reached $252.3 billion in 2024, representing a 44.5% increase from 2023.")
            ], color="info", className="mb-3")
        ])
    ]),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Data sources: AI Index Report 2025, McKinsey Global Survey, Goldman Sachs Economics Analysis",
                   className="text-center text-muted small")
        ])
    ], className="mt-4")
    
], fluid=True, className="py-4")

# Callbacks
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    return main_layout

@app.callback(Output('adoption-chart', 'figure'), Input('url', 'pathname'))
def update_adoption_chart(pathname):
    data, _ = create_data()
    return create_adoption_chart(data)

@app.callback(Output('investment-chart', 'figure'), Input('url', 'pathname'))
def update_investment_chart(pathname):
    data, _ = create_data()
    return create_investment_chart(data)

@app.callback(Output('industry-chart', 'figure'), Input('url', 'pathname'))
def update_industry_chart(pathname):
    _, data = create_data()
    return create_industry_chart(data)

if __name__ == '__main__':
    print("Starting AI Adoption Dashboard")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        print(f"Error starting dashboard: {e}") 