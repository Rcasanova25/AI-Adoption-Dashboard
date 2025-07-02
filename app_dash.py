#!/usr/bin/env python3
"""
Main Dash Application for AI Adoption Dashboard
Migrated from Streamlit to Plotly Dash for enterprise deployment
"""

import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import logging

# Import existing business logic (unchanged)
try:
    from business.metrics import business_metrics, CompetitivePosition, InvestmentRecommendation
    from business.roi_calculator import roi_calculator
    from business.causal_analysis import causal_engine, CausalAnalysisResult, ProductivityMetric
    from data.kedro_pipeline import kedro_manager, AIAdoptionKedroManager
    from visualization.vizro_dashboard import vizro_dashboard, PersonaType
except ImportError:
    print("Warning: Some business modules not available, using fallback implementations")

# Import existing data infrastructure (unchanged)
try:
    from data.loaders import load_all_datasets, validate_all_loaded_data
    from data.models import safe_validate_data
    from data.geographic import get_geographic_data, get_country_details, generate_geographic_insights
except ImportError:
    print("Warning: Some data modules not available, using fallback implementations")

# Import layouts
from layouts.main_layout import create_main_layout
from layouts.sidebar_layout import create_sidebar_layout

# Import callbacks
from callbacks.navigation_callbacks import register_navigation_callbacks
from callbacks.data_callbacks import register_data_callbacks
from callbacks.visualization_callbacks import register_visualization_callbacks

# Import views
from views.industry_analysis import create_industry_analysis_view
from views.financial_impact import create_financial_impact_view
from views.adoption_rates import create_adoption_rates_view
from views.productivity_research import create_productivity_research_view
from views.executive_dashboard import create_executive_dashboard_view

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app with Bootstrap theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "AI Adoption Dashboard | 2018-2025 Analysis"
app.config.suppress_callback_exceptions = True

# Load data using existing function (unchanged)
@callback(
    Output('data-store', 'data'),
    Input('app-init', 'id')
)
def load_dashboard_data(init_trigger):
    """Load data using existing McKinsey-powered pipeline"""
    try:
        # Try to use existing data loading function
        if 'load_all_datasets' in globals():
            mckinsey_data = load_all_datasets()
            return mckinsey_data
        else:
            # Fallback to sample data
            return load_fallback_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return load_fallback_data()

def load_fallback_data():
    """Load fallback data when main data sources are unavailable"""
    # Create sample data for testing
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    
    # Historical trends data
    historical_data = pd.DataFrame({
        'year': years,
        'ai_use': [5, 8, 12, 18, 25, 35, 55, 78],
        'genai_use': [0, 0, 0, 0, 0, 15, 33, 71],
        'investment_billions': [10, 15, 25, 40, 60, 100, 150, 252.3]
    })
    
    # Industry data
    industry_data = pd.DataFrame({
        'sector': ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail'],
        'adoption_rate': [91, 85, 72, 68, 79],
        'roi_percentage': [180, 165, 155, 145, 150],
        'productivity_gain': [2.1, 1.8, 1.5, 1.3, 1.6]
    })
    
    return {
        'historical_data': historical_data,
        'industry_data': industry_data,
        'dashboard_summary': historical_data,
        'dashboard_detailed': industry_data
    }

# Create main app layout
app.layout = html.Div([
    # Hidden div to trigger data loading
    html.Div(id='app-init', style={'display': 'none'}),
    
    # Data storage component
    dcc.Store(id='data-store'),
    dcc.Store(id='session-store', data={
        'selected_persona': 'General',
        'data_year': '2025 (GenAI Era)',
        'view_type': 'Adoption Rates',
        'first_visit': True
    }),
    
    # Main layout
    create_main_layout()
])

# Register all callbacks
register_navigation_callbacks(app)
register_data_callbacks(app)
register_visualization_callbacks(app)

# Main callback to update content based on navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """Display the appropriate page based on URL pathname"""
    if pathname == '/':
        return create_executive_dashboard_view()
    elif pathname == '/industry-analysis':
        return create_industry_analysis_view()
    elif pathname == '/financial-impact':
        return create_financial_impact_view()
    elif pathname == '/adoption-rates':
        return create_adoption_rates_view()
    elif pathname == '/productivity-research':
        return create_productivity_research_view()
    elif pathname == '/executive-dashboard':
        return create_executive_dashboard_view()
    else:
        return html.Div([
            html.H1("404 - Page Not Found", className="error-title"),
            html.P("The page you're looking for doesn't exist.", className="error-message"),
            dcc.Link("Go back to home", href="/", className="error-link")
        ], className="error-container")

# Error handling callback
@app.callback(
    Output('error-container', 'children'),
    [Input('error-trigger', 'n_clicks')]
)
def handle_errors(n_clicks):
    """Handle application errors"""
    if n_clicks:
        return html.Div([
            html.H3("An error occurred", className="error-title"),
            html.P("Please try refreshing the page or contact support.", className="error-message")
        ])
    return ""

if __name__ == '__main__':
    print("🚀 Starting AI Adoption Dashboard (Dash Version)")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🔄 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")
        print(f"❌ Error starting dashboard: {e}") 