"""
Sidebar Layout for Dash AI Adoption Dashboard
Converts Streamlit sidebar controls to Dash components
"""

import dash_bootstrap_components as dbc
from dash import html, dcc

def create_sidebar_layout():
    """Create sidebar layout - converts Streamlit sidebar controls"""
    
    sidebar = html.Div([
        # Dashboard Controls header
        html.H4("📊 Dashboard Controls", className="sidebar-header"),
        
        # McKinsey Tools section
        html.Hr(),
        html.H5("🏢 McKinsey Tools"),
        
        # Causal Analysis status (converts Streamlit metrics)
        dbc.Card([
            dbc.CardBody([
                html.P("CausalNx Analysis", className="card-title"),
                html.H6("✅ Complete", className="text-success"),
                html.Small("Confidence: 85.2%", className="text-muted")
            ])
        ], className="mb-3"),
        
        # Kedro Pipeline status
        dbc.Card([
            dbc.CardBody([
                html.P("Kedro Pipeline", className="card-title"),
                html.H6("✅ Connected", className="text-success")
            ])
        ], className="mb-3"),
        
        # Vizro Dashboard launcher
        html.H6("🎯 Advanced Dashboards"),
        dbc.Button("🚀 Launch Vizro Executive Dashboard", 
                  id="launch-vizro-btn", 
                  color="primary", 
                  className="mb-3 w-100"),
        
        html.Hr(),
        
        # Persona selection (converts Streamlit selectbox)
        html.Label("Select Your Role:", className="form-label"),
        dcc.Dropdown(
            id='persona-selector',
            options=[
                {'label': 'General', 'value': 'General'},
                {'label': 'Business Leader', 'value': 'Business Leader'},
                {'label': 'Policymaker', 'value': 'Policymaker'},
                {'label': 'Researcher', 'value': 'Researcher'}
            ],
            value='General',
            className="mb-3"
        ),
        
        # Data year selection (converts Streamlit selectbox)
        html.Label("Select Data Year:", className="form-label"),
        dcc.Dropdown(
            id='data-year-selector',
            options=[
                {'label': '2018 (Early AI)', 'value': '2018 (Early AI)'},
                {'label': '2025 (GenAI Era)', 'value': '2025 (GenAI Era)'}
            ],
            value='2025 (GenAI Era)',
            className="mb-3"
        ),
        
        # View type selection (converts Streamlit selectbox)
        html.Label("Analysis View:", className="form-label"),
        dcc.Dropdown(
            id='view-type-selector',
            options=[
                {'label': 'Adoption Rates', 'value': 'Adoption Rates'},
                {'label': 'Historical Trends', 'value': 'Historical Trends'},
                {'label': 'Industry Analysis', 'value': 'Industry Analysis'},
                {'label': 'Investment Trends', 'value': 'Investment Trends'},
                {'label': 'Regional Growth', 'value': 'Regional Growth'},
                {'label': 'AI Cost Trends', 'value': 'AI Cost Trends'},
                {'label': 'Token Economics', 'value': 'Token Economics'},
                {'label': 'Financial Impact', 'value': 'Financial Impact'},
                {'label': 'Labor Impact', 'value': 'Labor Impact'},
                {'label': 'Firm Size Analysis', 'value': 'Firm Size Analysis'},
                {'label': 'Technology Stack', 'value': 'Technology Stack'},
                {'label': 'AI Technology Maturity', 'value': 'AI Technology Maturity'},
                {'label': 'Productivity Research', 'value': 'Productivity Research'},
                {'label': 'Environmental Impact', 'value': 'Environmental Impact'},
                {'label': 'Geographic Distribution', 'value': 'Geographic Distribution'},
                {'label': 'OECD 2025 Findings', 'value': 'OECD 2025 Findings'},
                {'label': 'Barriers & Support', 'value': 'Barriers & Support'},
                {'label': 'ROI Analysis', 'value': 'ROI Analysis'},
                {'label': 'Skill Gap Analysis', 'value': 'Skill Gap Analysis'},
                {'label': 'AI Governance', 'value': 'AI Governance'},
                {'label': 'Causal Analysis', 'value': 'Causal Analysis'},
                {'label': 'Bibliography & Sources', 'value': 'Bibliography & Sources'},
                {'label': 'AI Chart Generator', 'value': 'AI Chart Generator'}  # New Vizro-AI view
            ],
            value='Adoption Rates',
            className="mb-3"
        ),
        
        html.Hr(),
        
        # Advanced options section
        html.H6("🔧 Advanced Options"),
        
        # Year range slider for historical trends
        html.Div([
            html.Label("Year Range:", className="form-label"),
            dcc.RangeSlider(
                id='year-range-slider',
                min=2017,
                max=2025,
                value=[2017, 2025],
                marks={i: str(i) for i in range(2017, 2026)},
                step=1,
                className="mb-3"
            )
        ], id='year-range-container', style={'display': 'none'}),
        
        html.Hr(),
        
        # Export options
        html.H6("📥 Export Options"),
        dcc.Dropdown(
            id='export-format-selector',
            options=[
                {'label': 'CSV Data', 'value': 'CSV Data'},
                {'label': 'PNG Image', 'value': 'PNG Image'},
                {'label': 'PDF Report (Beta)', 'value': 'PDF Report (Beta)'}
            ],
            value='CSV Data',
            className="mb-3"
        ),
        
        dbc.Button("📥 Export Current View", 
                  id="export-btn", 
                  color="secondary", 
                  className="mb-3 w-100"),
        
        html.Hr(),
        
        # Feedback section
        html.H6("💬 Feedback"),
        dbc.Textarea(
            id="feedback-textarea",
            placeholder="Share your thoughts or request features...",
            style={"height": "100px"},
            className="mb-3"
        ),
        dbc.Button("Submit Feedback", 
                  id="feedback-btn", 
                  color="success", 
                  className="mb-3 w-100"),
        
        # Help section (converts Streamlit expander)
        dbc.Accordion([
            dbc.AccordionItem([
                html.Div([
                    html.Strong("Navigation Tips:"),
                    html.Ul([
                        html.Li("Use the Analysis View dropdown to explore different perspectives"),
                        html.Li("Click 📊 icons for data source information"),
                        html.Li("Hover over chart elements for details")
                    ]),
                    html.Strong("Keyboard Shortcuts:"),
                    html.Ul([
                        html.Li("Ctrl + K: Quick search"),
                        html.Li("F: Toggle fullscreen"),
                        html.Li("?: Show help")
                    ])
                ])
            ], title="❓ Need Help?")
        ], start_collapsed=True)
        
    ], className="sidebar-content")
    
    return sidebar 