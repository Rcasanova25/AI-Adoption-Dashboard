#!/usr/bin/env python3
"""
Simple script to run the Vizro dashboard
"""

import pandas as pd
import numpy as np
from visualization.vizro_dashboard import AIAdoptionVizroDashboard, PersonaType

def create_sample_data():
    """Create sample data for the dashboard"""
    
    # Sample adoption data - fix the length mismatch
    years = [2020, 2021, 2022, 2023, 2024]
    sectors = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail']
    
    # Create data with proper lengths
    data_rows = []
    for year in years:
        for sector in sectors:
            data_rows.append({
                'year': year,
                'sector': sector,
                'adoption_rate': np.random.randint(30, 80),
                'roi_percentage': np.random.randint(80, 200),
                'productivity_index': np.random.uniform(0.8, 2.0),
                'investment_amount': np.random.randint(500000, 2000000)
            })
    
    adoption_data = pd.DataFrame(data_rows)
    
    # Sample geographic data
    geographic_data = pd.DataFrame({
        'country': ['USA', 'China', 'Germany', 'Japan', 'UK', 'France', 'Canada', 'Australia', 'South Korea', 'India'],
        'adoption_rate': [78, 72, 68, 65, 70, 62, 75, 73, 69, 55],
        'gdp_impact': [2.5, 2.8, 2.1, 1.9, 2.3, 1.8, 2.4, 2.2, 2.0, 1.5],
        'employment_effect': [0.8, 0.6, 0.9, 0.7, 0.8, 0.6, 0.9, 0.7, 0.8, 0.5]
    })
    
    # Sample research data
    research_data = pd.DataFrame({
        'study_id': range(1, 21),
        'publication_year': [2020, 2021, 2022, 2023, 2024] * 4,
        'sample_size': np.random.randint(100, 10000, 20),
        'effect_size': np.random.uniform(0.1, 0.8, 20),
        'confidence_interval': np.random.uniform(0.05, 0.15, 20),
        'statistical_significance': np.random.choice([True, False], 20, p=[0.8, 0.2])
    })
    
    return {
        'adoption_data': adoption_data,
        'geographic_data': geographic_data,
        'research_data': research_data
    }

def main():
    """Main function to run the dashboard"""
    
    print("Creating AI Adoption Vizro Dashboard...")
    
    # Create dashboard instance
    dashboard = AIAdoptionVizroDashboard()
    
    # Create sample data
    print("Generating sample data...")
    data_sources = create_sample_data()
    
    # Create multi-persona dashboard
    print("Building dashboard for all personas...")
    dashboards = dashboard.create_multi_persona_dashboard(data_sources)
    
    print(f"Created dashboards for {len(dashboards)} personas:")
    for persona, dashboard_obj in dashboards.items():
        print(f"  - {persona.value}")
    
    # Launch executive dashboard by default
    print("\nLaunching Executive dashboard...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("Press Ctrl+C to stop the server")
    
    try:
        dashboard.launch_dashboard(
            persona=PersonaType.EXECUTIVE,
            host="127.0.0.1",
            port=8050
        )
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        print("Trying fallback mode...")
        
        # Try to show fallback information
        for persona, dashboard_info in dashboards.items():
            print(f"\n{persona.value} Dashboard Info:")
            if isinstance(dashboard_info, dict) and 'message' in dashboard_info:
                print(f"  {dashboard_info['message']}")
            else:
                print(f"  Dashboard object: {type(dashboard_info)}")

if __name__ == "__main__":
    main() 