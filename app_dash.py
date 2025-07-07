"""
AI Adoption Dashboard - Dash Version
Enterprise-grade AI investment analysis platform with async data loading
"""
import dash
from dash import html, dcc, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc
from typing import Dict, Any, List, Optional
import importlib
import traceback
import logging
import json
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import existing systems with error handling
try:
    from data.data_manager import DataManager
except ImportError:
    logger.warning("DataManager not available, using mock data")
    DataManager = None

try:
    from core.business import roi_analysis
    # Create a wrapper class for ROI functions
    class ROICalculator:
        @staticmethod
        def compute_roi(*args, **kwargs):
            return roi_analysis.compute_roi(*args, **kwargs)
except ImportError:
    logger.warning("ROI analysis not available")
    ROICalculator = None

try:
    from core.business.scenario_engine import ScenarioEngine
except ImportError:
    logger.warning("ScenarioEngine not available")
    ScenarioEngine = None

try:
    from core.business import industry_models
    # Create a wrapper class for industry functions
    class IndustryAnalyzer:
        @staticmethod
        def get_industry_profile(*args, **kwargs):
            return industry_models.get_industry_profile(*args, **kwargs)
except ImportError:
    logger.warning("Industry models not available")
    IndustryAnalyzer = None

try:
    from performance.monitor import PerformanceMonitor
except ImportError:
    logger.warning("PerformanceMonitor not available")
    PerformanceMonitor = None

try:
    from config.settings import get_settings
except ImportError:
    logger.warning("Settings not available, using defaults")
    def get_settings():
        return {}

class DashboardApp:
    """Main Dash application class for AI Adoption Dashboard."""
    
    def __init__(self):
        """Initialize the Dash application."""
        # Initialize Dash app with Bootstrap theme
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP, 
                dbc.icons.FONT_AWESOME,
                "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
            ],
            suppress_callback_exceptions=True,
            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                {"name": "description", "content": "Enterprise AI Adoption Dashboard - 2018-2025 Analysis"}
            ],
            title="AI Adoption Dashboard | 2018-2025 Analysis"
        )
        
        # Initialize systems (lazy loading)
        self.data_manager = None
        self.roi_calculator = None
        self.scenario_engine = None
        self.industry_analyzer = None
        self.performance_monitor = PerformanceMonitor() if PerformanceMonitor else None
        self.settings = get_settings() if callable(get_settings) else {}
        
        # View registry
        self.view_manager = None
        
        # Setup app
        self.setup_layout()
        self.register_callbacks()
        
    def setup_layout(self):
        """Create the main application layout."""
        self.app.layout = dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1([
                            html.I(className="fas fa-robot me-3"),
                            "AI Adoption Dashboard: 2018-2025"
                        ], className="text-primary mb-3"),
                        html.P(
                            "Comprehensive analysis from early AI adoption (2018) to current GenAI trends (2025)", 
                            className="lead mb-4 text-muted"
                        )
                    ])
                ], width=12)
            ], className="header-section mb-4"),
            
            # Data loading progress
            dbc.Row([
                dbc.Col([
                    html.Div(id="data-loading-progress", className="mb-4")
                ], width=12)
            ], id="loading-section"),
            
            # Main content area
            dbc.Row([
                # Sidebar
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id="sidebar-content"),
                            html.Hr(className="my-4"),
                            # Performance monitor
                            html.Div(id="performance-monitor", className="mt-4")
                        ])
                    ], className="h-100 shadow-sm")
                ], width=3, className="sidebar-column"),
                
                # Main view area
                dbc.Col([
                    dcc.Loading(
                        id="main-loading",
                        children=[
                            html.Div(id="main-content", className="main-content-area")
                        ],
                        type="default",
                        className="loading-wrapper"
                    )
                ], width=9, className="main-column")
            ], className="content-area g-4"),
            
            # Hidden stores for state management
            dcc.Store(id="data-store", storage_type="memory"),
            dcc.Store(id="view-store", storage_type="session", data="adoption_rates"),
            dcc.Store(id="persona-store", storage_type="session", data="General"),
            dcc.Store(id="settings-store", storage_type="local"),
            
            # Intervals for updates
            dcc.Interval(id="performance-interval", interval=5000, n_intervals=0),
            dcc.Interval(id="data-check-interval", interval=30000, n_intervals=0),
            
            # Error modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Error")),
                dbc.ModalBody(id="error-content"),
                dbc.ModalFooter([
                    dbc.Button("Close", id="close-error", className="ms-auto", n_clicks=0)
                ])
            ], id="error-modal", is_open=False, size="lg"),
            
            # Success notification area
            html.Div(id="notification-area", style={"position": "fixed", "top": 20, "right": 20, "width": 350})
            
        ], fluid=True, className="dashboard-container")
        
    def register_callbacks(self):
        """Register all Dash callbacks."""
        # Import callback modules
        from callbacks.data_callbacks import register_data_callbacks
        from callbacks.view_callbacks import register_view_callbacks
        from callbacks.performance_callbacks import register_performance_callbacks
        
        # Register callbacks
        register_data_callbacks(self.app)
        register_view_callbacks(self.app)
        register_performance_callbacks(self.app)

    def run(self, debug=True, host="0.0.0.0", port=8050):
        """Run the Dash application."""
        logger.info(f"Starting AI Adoption Dashboard on {host}:{port}")
        self.app.run_server(debug=debug, host=host, port=port)

# Custom CSS styling
custom_css = """
<style>
    /* Custom fonts and overall styling */
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f8f9fa;
    }
    
    .dashboard-container {
        padding: 2rem;
        max-width: 1600px;
        margin: 0 auto;
    }
    
    .header-section h1 {
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    .sidebar-column {
        position: sticky;
        top: 20px;
        height: calc(100vh - 200px);
        overflow-y: auto;
    }
    
    .main-column {
        min-height: calc(100vh - 200px);
    }
    
    .main-content-area {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Loading states */
    .loading-wrapper {
        min-height: 400px;
    }
    
    /* Metric cards */
    .metric-card {
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .metric-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
        margin: 0.5rem 0;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Progress bars */
    .progress-container {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Charts */
    .main-chart {
        margin-top: 1rem;
    }
    
    /* Data tables */
    .dash-table-container {
        margin-top: 2rem;
    }
    
    /* Dropdown styling */
    .Select-control {
        border-radius: 6px !important;
        border-color: #dee2e6 !important;
    }
    
    .Select-control:hover {
        border-color: #adb5bd !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
"""

if __name__ == "__main__":
    # Create and run the application
    app_instance = DashboardApp()
    app_instance.run(debug=True)