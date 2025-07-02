"""
Data Callbacks for Dash AI Adoption Dashboard
Handle data loading and processing operations
"""

from dash import callback, Input, Output, State
import pandas as pd
import json

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