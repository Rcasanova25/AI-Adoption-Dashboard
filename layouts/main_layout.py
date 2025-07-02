"""
Main Layout for Dash AI Adoption Dashboard
Converts Streamlit layout structure to Dash components
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from .sidebar_layout import create_sidebar_layout

def create_main_layout():
    """Create main dashboard layout - converts Streamlit structure to Dash"""
    
    layout = dbc.Container([
        # Header section (converts Streamlit title and description)
        dbc.Row([
            dbc.Col([
                html.H1("🤖 AI Adoption Dashboard: 2018-2025", className="mb-3"),
                html.P("Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)", 
                       className="lead mb-4"),
                
                # What's New section (converts Streamlit expander)
                dbc.Accordion([
                    dbc.AccordionItem([
                        html.Div([
                            html.H5("Latest Updates (June 2025):"),
                            html.Ul([
                                html.Li("✅ Integrated AI Index Report 2025 findings"),
                                html.Li("✅ Added industry-specific 2025 data"),
                                html.Li("✅ Enhanced financial impact clarity"),
                                html.Li("✅ New skill gap and governance metrics"),
                                html.Li("✅ Interactive filtering for charts"),
                                html.Li("✅ Source attribution for all data points"),
                                html.Li("✅ Export data as CSV functionality"),
                                html.Li("✅ Comprehensive academic analysis integration"),
                                html.Li("✅ Enhanced risks and safety analysis")
                            ])
                        ])
                    ], title="🆕 What's New in Version 2.2.0")
                ], start_collapsed=True, className="mb-4"),
                
                # Important note (converts Streamlit info box)
                dbc.Alert([
                    html.Strong("📌 Important Note: "),
                    "Adoption rates in this dashboard reflect \"any AI use\" including pilots, experiments, and production deployments. ",
                    "Enterprise-wide production use rates are typically lower. Data sources include AI Index Report 2025, McKinsey Global Survey on AI, ",
                    "OECD AI Policy Observatory, and US Census Bureau AI Use Supplement."
                ], color="info", className="mb-4")
            ])
        ]),
        
        # Main content area
        dbc.Row([
            # Sidebar (converts Streamlit sidebar)
            dbc.Col([
                create_sidebar_layout()
            ], width=3, className="sidebar"),
            
            # Main content (converts Streamlit main area)
            dbc.Col([
                # Key metrics row (converts Streamlit columns)
                html.Div(id="key-metrics-row", className="mb-4"),
                
                # Main visualization area (converts Streamlit view content)
                html.Div(id="main-content-area")
            ], width=9)
        ])
    ], fluid=True)
    
    return layout

def create_key_metrics_cards(data_year, mckinsey_data):
    """Create key metrics cards - converts Streamlit metric columns"""
    
    if "2025" in data_year:
        metrics = [
            {"label": "Overall AI Adoption*", "value": "78%", "delta": "+23pp from 2023", 
             "help": "*Includes any AI use. Jumped from 55% in 2023 (AI Index 2025)"},
            {"label": "GenAI Adoption*", "value": "71%", "delta": "+38pp from 2023", 
             "help": "*More than doubled from 33% in 2023 (AI Index 2025)"},
            {"label": "2024 AI Investment", "value": "$252.3B", "delta": "+44.5% YoY", 
             "help": "Total corporate AI investment reached record levels"},
            {"label": "Cost Reduction", "value": "280x cheaper", "delta": "Since Nov 2022", 
             "help": "AI inference cost dropped from $20 to $0.07 per million tokens"}
        ]
    else:
        metrics = [
            {"label": "Overall AI Adoption", "value": "5.8%", "delta": "📊 Firm-weighted"},
            {"label": "Large Firms (5000+)", "value": "58.5%", "delta": "🏢 High adoption"},
            {"label": "AI + Cloud", "value": "45%", "delta": "☁️ Technology stack"},
            {"label": "Top City", "value": "SF Bay (9.5%)", "delta": "🌍 Geographic leader"}
        ]
    
    metric_cards = []
    for metric in metrics:
        card = dbc.Card([
            dbc.CardBody([
                html.H4(metric["value"], className="text-primary"),
                html.P(metric["label"], className="card-title"),
                html.Small(metric["delta"], className="text-muted")
            ])
        ], className="metric-card mb-3")
        metric_cards.append(dbc.Col(card, width=3))
    
    return dbc.Row(metric_cards) 