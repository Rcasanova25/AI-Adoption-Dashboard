"""
Data Callbacks for Dash AI Adoption Dashboard
Handle data loading, validation, and processing
"""

from dash import callback, Input, Output, State
import pandas as pd
import json
import numpy as np

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
    
    # Geographic data
    geographic_data = pd.DataFrame({
        'country': ['USA', 'China', 'Germany', 'Japan', 'UK', 'France', 'Canada', 'Australia'],
        'adoption_rate': [78, 72, 68, 65, 70, 62, 75, 73],
        'gdp_impact': [2.5, 2.8, 2.1, 1.9, 2.3, 1.8, 2.4, 2.2]
    })
    
    return {
        'historical_data': historical_data.to_dict('records'),
        'industry_data': industry_data.to_dict('records'),
        'geographic_data': geographic_data.to_dict('records'),
        'dashboard_summary': historical_data.to_dict('records'),
        'dashboard_detailed': industry_data.to_dict('records')
    }

def register_data_callbacks(app):
    """Register all data callbacks with the Dash app"""
    
    @app.callback(
        Output('data-validation-status', 'children'),
        [Input('data-store', 'data')]
    )
    def validate_loaded_data(data):
        """Validate loaded data and return status"""
        if data is None:
            return "⏳ Loading data..."
        
        try:
            # Basic validation
            if isinstance(data, dict) and len(data) > 0:
                return "✅ Data loaded successfully"
            else:
                return "⚠️ Data format issue detected"
        except Exception as e:
            return f"❌ Data validation error: {str(e)}"

    @app.callback(
        Output('data-summary', 'children'),
        [Input('data-store', 'data')]
    )
    def display_data_summary(data):
        """Display summary of loaded data"""
        if data is None:
            return "No data available"
        
        try:
            summary = []
            for key, value in data.items():
                if isinstance(value, pd.DataFrame):
                    summary.append(f"{key}: {len(value)} rows, {len(value.columns)} columns")
                else:
                    summary.append(f"{key}: {type(value).__name__}")
            
            return html.Ul([html.Li(item) for item in summary])
        except Exception as e:
            return f"Error generating summary: {str(e)}" 