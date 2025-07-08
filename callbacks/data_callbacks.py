"""
Data loading and management callbacks for the AI Adoption Dashboard.
Handles async data loading with progress tracking.
"""
import dash
from dash import Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import json
import time
import logging
from typing import Dict, Any, Tuple
import traceback

try:
    from data.data_manager_dash import DataManagerDash as DataManager
except ImportError:
    from data.data_manager import DataManager

logger = logging.getLogger(__name__)

def register_data_callbacks(app):
    """Register all data-related callbacks."""
    
    @app.callback(
        [Output("data-store", "data"),
         Output("data-loading-progress", "children"),
         Output("loading-section", "style")],
        [Input("data-check-interval", "n_intervals")],
        [State("data-store", "data")],
        prevent_initial_call=False
    )
    def load_data_async(n_intervals: int, existing_data: Dict[str, Any]) -> Tuple[Dict, Any, Dict]:
        """
        Load data asynchronously with progress tracking.
        This runs on initial load and every 30 seconds to check for updates.
        """
        try:
            # If data already loaded and this is just a check, skip
            if existing_data and n_intervals > 0:
                metadata = existing_data.get("_metadata", {})
                if metadata.get("successful_loads", 0) > 20:
                    return existing_data, dash.no_update, {"display": "none"}
            
            # Show progress container
            progress_container = dbc.Card([
                dbc.CardBody([
                    html.H5([
                        dbc.Spinner(size="sm", color="primary", spinner_class_name="me-2"),
                        "Loading AI Adoption Data..."
                    ], className="mb-3"),
                    html.Div(id="progress-details", children=[
                        dbc.Progress(
                            id="loading-progress-bar",
                            value=0,
                            max=100,
                            striped=True,
                            animated=True,
                            className="mb-3",
                            style={"height": "25px"}
                        ),
                        html.P("Initializing data manager...", className="text-muted small")
                    ])
                ])
            ], className="shadow-sm")
            
            # Initialize data manager
            logger.info("Initializing DataManager...")
            
            # Try to use real DataManager, fall back to mock if not available
            try:
                # DataManager is already imported at the top of the file
                
                # Check if resources path exists
                from pathlib import Path
                resources_path = Path("AI adoption resources")
                
                if not resources_path.exists():
                    logger.warning(f"Resources directory not found at: {resources_path}")
                    logger.info("Creating resources directory structure...")
                    pdf_dir = resources_path / "AI dashboard resources 1"
                    pdf_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Create a README for PDF location
                    readme_path = pdf_dir / "README.txt"
                    readme_path.write_text(
                        "Place your PDF files here:\n\n" +
                        "\n".join([
                            "- hai_ai_index_report_2025.pdf",
                            "- the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
                            "- oecd-artificial-intelligence-review-2025.pdf",
                            "- cost-benefit-analysis-artificial-intelligence-evidence-from-a-field-experiment-on-gpt-4o-1.pdf",
                            "- the-economic-impact-of-large-language-models.pdf",
                            "- gs-new-decade-begins.pdf",
                            "- nvidia-cost-trends-ai-inference-at-scale.pdf",
                            "- wpiea2024231-print-pdf.pdf",
                            "- w30957.pdf",
                            "- Machines of mind_ The case for an AI-powered productivity boom.pdf"
                        ])
                    )
                
                data_manager = DataManager(resources_path)
                
                # Try to load real data
                logger.info("Attempting to load data from PDFs...")
                all_data = data_manager.load_all_data()
                
                if all_data and len(all_data) > 0:
                    logger.info(f"Successfully loaded {len(all_data)} datasets from PDFs")
                    datasets = all_data
                    successful_loads = len(all_data)
                    failed_loads = []
                else:
                    raise Exception("No data loaded from PDFs")
                    
            except Exception as e:
                logger.error(f"Failed to load data from PDFs: {str(e)}")
                # NO DEMO DATA - per CLAUDE.md requirements
                raise RuntimeError(
                    f"Failed to load data from PDFs: {str(e)}\n\n" +
                    "Please ensure:\n" +
                    "1. PDF files are present in 'AI adoption resources/AI dashboard resources 1/'\n" +
                    "2. The PDF files have read permissions\n" +
                    "3. Required PDF processing libraries are installed (PyMuPDF, pdfplumber, tabula-py)\n" +
                    "4. Java is installed (required by tabula-py)"
                )
            
            # Add metadata
            total_datasets = len(datasets)
            datasets["_metadata"] = {
                "loaded_at": pd.Timestamp.now().isoformat(),
                "total_datasets": total_datasets,
                "successful_loads": successful_loads,
                "failed_loads": failed_loads,
                "version": "4.0.0"
            }
            
            # Create success message
            if successful_loads == len(datasets) - 1:  # -1 for metadata
                final_progress = dbc.Alert([
                    html.I(className="fas fa-check-circle me-2"),
                    f"✅ Successfully loaded {successful_loads} datasets from PDFs!"
                ], color="success", dismissable=True)
            elif successful_loads > 0:
                final_progress = dbc.Alert([
                    html.I(className="fas fa-exclamation-triangle me-2"),
                    f"⚠️ Loaded {successful_loads} datasets. ",
                    html.Br(),
                    html.Small(f"Failed: {', '.join(failed_loads[:3])}")
                ], color="warning", dismissable=True)
            else:
                final_progress = dbc.Alert([
                    html.I(className="fas fa-times-circle me-2"),
                    "❌ Failed to load data"
                ], color="danger")
            
            # Hide loading section after initial load
            loading_style = {"display": "none"} if successful_loads > 0 else {}
            
            return datasets, final_progress, loading_style
            
        except Exception as e:
            logger.error(f"Critical error in data loading: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Show error modal
            error_content = dbc.Container([
                html.H5("Critical Data Loading Error", className="text-danger mb-3"),
                html.P("The dashboard encountered an error while loading data:"),
                dbc.Alert(str(e), color="danger", className="mb-3"),
                html.Hr(),
                html.H6("Troubleshooting Steps:", className="mb-2"),
                html.Ol([
                    html.Li("Check that all required PDF files are present in the data directory"),
                    html.Li("Ensure Java is installed for PDF processing (required by tabula-py)"),
                    html.Li("Verify internet connection for downloading data"),
                    html.Li("Check the logs for more detailed error information")
                ]),
                html.P("If the issue persists, please check the deployment guide or contact support.", 
                      className="text-muted mt-3")
            ])
            
            progress = dbc.Alert("❌ Data loading failed", color="danger")
            
            # Store error in data for view callbacks to handle
            error_data = {
                "_error": True,
                "_error_message": str(e),
                "_error_details": error_content
            }
            return error_data, progress, {}
    
    # Success toast is now handled in the main layout to avoid conflicts


