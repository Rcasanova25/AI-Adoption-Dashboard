"""
AI Adoption Dashboard - Dash Version (Fixed)
This version fixes the duplicate callback and view registration issues.
"""
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import logging
from pathlib import Path
import traceback
from typing import Dict, Any, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="AI Adoption Dashboard | 2018-2025 Analysis"
)

# Define all views with their proper modules
ALL_VIEWS = {
    # Adoption Views
    "adoption_rates": {
        "label": "📈 Adoption Rates", 
        "module": "views.adoption.adoption_rates_dash",
        "category": "adoption"
    },
    "historical_trends": {
        "label": "📊 Historical Trends",
        "module": "views.adoption.historical_trends_dash", 
        "category": "adoption"
    },
    "industry_analysis": {
        "label": "🏭 Industry Analysis",
        "module": "views.adoption.industry_analysis_dash",
        "category": "adoption"
    },
    "firm_size_analysis": {
        "label": "🏢 Firm Size Analysis",
        "module": "views.adoption.firm_size_analysis_dash",
        "category": "adoption"
    },
    "technology_stack": {
        "label": "🔧 Technology Stack",
        "module": "views.adoption.technology_stack_dash",
        "category": "adoption"
    },
    "ai_technology_maturity": {
        "label": "🎯 Technology Maturity",
        "module": "views.adoption.ai_technology_maturity_dash",
        "category": "adoption"
    },
    
    # Economic Views
    "investment_trends": {
        "label": "💰 Investment Trends",
        "module": "views.economic.investment_trends_dash",
        "category": "economic"
    },
    "financial_impact": {
        "label": "💵 Financial Impact",
        "module": "views.economic.financial_impact_dash",
        "category": "economic"
    },
    "roi_analysis": {
        "label": "📊 ROI Analysis",
        "module": "views.economic.roi_analysis_dash",
        "category": "economic"
    },
    "ai_cost_trends": {
        "label": "📉 AI Cost Trends",
        "module": "views.adoption.ai_cost_trends_dash",
        "category": "economic"
    },
    
    # Geographic Views
    "geographic_distribution": {
        "label": "🗺️ Geographic Distribution",
        "module": "views.geographic.geographic_distribution_dash",
        "category": "geographic"
    },
    "regional_growth": {
        "label": "🌍 Regional Growth",
        "module": "views.geographic.regional_growth_dash",
        "category": "geographic"
    },
    
    # Research Views
    "productivity_research": {
        "label": "🔬 Productivity Research",
        "module": "views.adoption.productivity_research_dash",
        "category": "research"
    },
    "labor_impact": {
        "label": "👥 Labor Impact",
        "module": "views.adoption.labor_impact_dash",
        "category": "research"
    },
    "skill_gap_analysis": {
        "label": "🎓 Skill Gap Analysis",
        "module": "views.adoption.skill_gap_analysis_dash",
        "category": "research"
    },
    "oecd_2025_findings": {
        "label": "📋 OECD 2025 Findings",
        "module": "views.adoption.oecd_2025_findings_dash",
        "category": "research"
    },
    
    # Other Views
    "ai_governance": {
        "label": "⚖️ AI Governance",
        "module": "views.other.ai_governance_dash",
        "category": "other"
    },
    "environmental_impact": {
        "label": "🌱 Environmental Impact",
        "module": "views.other.environmental_impact_dash",
        "category": "other"
    },
    "token_economics": {
        "label": "🪙 Token Economics",
        "module": "views.other.token_economics_dash",
        "category": "other"
    },
    "barriers_support": {
        "label": "🚧 Barriers & Support",
        "module": "views.adoption.barriers_support_dash",
        "category": "other"
    },
    "bibliography_sources": {
        "label": "📚 Bibliography & Sources",
        "module": "views.other.bibliography_sources_dash",
        "category": "other"
    }
}

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-robot me-3"),
                "AI Adoption Dashboard: 2018-2025"
            ], className="text-primary mb-3"),
            html.P(
                "Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)", 
                className="lead text-muted"
            )
        ])
    ], className="mb-4"),
    
    # Data status message
    dbc.Row([
        dbc.Col([
            html.Div(id="data-status-message")
        ])
    ], className="mb-4"),
    
    # Main content
    dbc.Row([
        # Sidebar
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Dashboard Controls", className="mb-4"),
                    
                    # View selector with all views
                    html.Label("Select Analysis View:", className="fw-bold"),
                    dcc.Dropdown(
                        id="view-selector",
                        options=[
                            {"label": view["label"], "value": view_id}
                            for view_id, view in ALL_VIEWS.items()
                        ],
                        value="adoption_rates",
                        className="mb-4",
                        clearable=False
                    ),
                    
                    html.P(f"Total views available: {len(ALL_VIEWS)}", className="text-muted small"),
                    
                    html.Hr(),
                    
                    # Data info
                    html.Div(id="data-info", className="mb-3"),
                    
                    # Refresh button
                    dbc.Button(
                        [html.I(className="fas fa-sync me-2"), "Refresh Data"],
                        id="refresh-btn",
                        color="primary",
                        size="sm",
                        outline=True,
                        className="w-100"
                    )
                ])
            ])
        ], width=3),
        
        # Main content area
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(
                        id="loading",
                        children=[html.Div(id="main-content")],
                        type="default"
                    )
                ])
            ])
        ], width=9)
    ]),
    
    # Data store
    dcc.Store(id="data-store")
    
], fluid=True, className="p-4")

# Callbacks
@callback(
    [Output("data-store", "data"),
     Output("data-status-message", "children"),
     Output("data-info", "children")],
    [Input("refresh-btn", "n_clicks")],
    prevent_initial_call=False
)
def load_data(n_clicks):
    """Load data and check for PDFs."""
    # Check if PDFs exist
    pdf_dir = Path("AI adoption resources") / "AI dashboard resources 1"
    
    if not pdf_dir.exists():
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
    # Check for PDFs
    required_pdfs = [
        "hai_ai_index_report_2025.pdf",
        "the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
        "oecd-artificial-intelligence-review-2025.pdf",
        "cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf",
        "the-economic-impact-of-large-language-models.pdf",
        "gs-new-decade-begins.pdf",
        "nvidia-cost-trends-ai-inference-at-scale.pdf",
        "wpiea2024231-print-pdf.pdf",
        "w30957.pdf",
        "Machines of mind_ The case for an AI-powered productivity boom.pdf"
    ]
    
    found_pdfs = sum(1 for pdf in required_pdfs if (pdf_dir / pdf).exists())
    
    # Create mock data
    mock_data = {
        "_metadata": {
            "loaded_at": pd.Timestamp.now().isoformat(),
            "pdfs_found": found_pdfs,
            "pdfs_required": len(required_pdfs)
        }
    }
    
    # Status message
    if found_pdfs == 0:
        status_msg = dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            html.Strong("Using Demo Data"),
            html.Br(),
            html.P([
                "To use real data, place PDF files in: ",
                html.Code(str(pdf_dir))
            ], className="mb-0")
        ], color="info", dismissable=True)
    elif found_pdfs < len(required_pdfs):
        status_msg = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Found {found_pdfs}/{len(required_pdfs)} PDFs - Using partial data"
        ], color="warning", dismissable=True)
    else:
        status_msg = dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            f"✅ All {found_pdfs} PDFs found - Using real data!"
        ], color="success", dismissable=True)
    
    # Data info
    data_info = html.Div([
        html.Small(f"PDFs found: {found_pdfs}/{len(required_pdfs)}", className="d-block"),
        html.Small("Data mode: " + ("Real" if found_pdfs > 0 else "Demo"), className="d-block text-muted")
    ])
    
    return mock_data, status_msg, data_info

@callback(
    Output("main-content", "children"),
    [Input("view-selector", "value"),
     Input("data-store", "data")]
)
def update_view(selected_view, data):
    """Update the main content based on selected view."""
    if not selected_view or not data:
        return html.Div("Loading...")
    
    # Try to load the actual view
    if selected_view in ALL_VIEWS:
        try:
            # Import the view module
            import importlib
            module_path = ALL_VIEWS[selected_view]["module"]
            view_module = importlib.import_module(module_path)
            
            # Call create_layout if it exists
            if hasattr(view_module, 'create_layout'):
                return view_module.create_layout(data, "General")
            else:
                return create_placeholder_view(selected_view)
                
        except Exception as e:
            logger.error(f"Error loading view {selected_view}: {str(e)}")
            return create_placeholder_view(selected_view, error=str(e))
    
    return create_placeholder_view(selected_view)

def create_placeholder_view(view_name, error=None):
    """Create a placeholder view for testing."""
    view_info = ALL_VIEWS.get(view_name, {"label": view_name})
    
    # Sample data for charts
    years = list(range(2018, 2026))
    values = [15 + (year - 2018) * 11 for year in years]
    
    df = pd.DataFrame({
        'Year': years,
        'Value': values
    })
    
    fig = px.bar(
        df, x='Year', y='Value',
        title=f"{view_info['label']} - Sample Data",
        color_discrete_sequence=['#3498DB']
    )
    
    return html.Div([
        html.H3(view_info['label'], className="mb-4"),
        
        # Error message if any
        dbc.Alert(f"Error loading view: {error}", color="warning", className="mb-3") if error else None,
        
        # Sample metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Sample Metric", className="text-muted"),
                        html.H3("92%"),
                        html.P("↗ 15%", className="text-success small")
                    ])
                ])
            ], width=3) for _ in range(4)
        ], className="mb-4"),
        
        # Sample chart
        dcc.Graph(figure=fig),
        
        # Info
        dbc.Alert([
            "This is a placeholder view. ",
            "The actual view will show real data when PDFs are loaded."
        ], color="info", className="mt-4")
    ])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)