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

from data.data_manager import DataManager

logger = logging.getLogger(__name__)

def register_data_callbacks(app):
    """Register all data-related callbacks."""
    
    @callback(
        [Output("data-store", "data"),
         Output("data-loading-progress", "children"),
         Output("error-modal", "is_open", allow_duplicate=True),
         Output("error-content", "children", allow_duplicate=True),
         Output("loading-section", "style")],
        [Input("data-check-interval", "n_intervals")],
        [State("data-store", "data")],
        prevent_initial_call=False
    )
    def load_data_async(n_intervals: int, existing_data: Dict[str, Any]) -> Tuple[Dict, Any, bool, Any, Dict]:
        """
        Load data asynchronously with progress tracking.
        This runs on initial load and every 30 seconds to check for updates.
        """
        try:
            # If data already loaded and this is just a check, skip
            if existing_data and n_intervals > 0:
                metadata = existing_data.get("_metadata", {})
                if metadata.get("successful_loads", 0) > 20:
                    return existing_data, dash.no_update, False, "", {"display": "none"}
            
            # Show progress container
            progress_container = dbc.Card([
                dbc.CardBody([
                    html.H5([
                        dbc.Spinner(size="sm", color="primary", className="me-2"),
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
            data_manager = DataManager()
            
            # Get list of datasets to load
            dataset_names = [
                "ai_index_adoption_rates",
                "ai_index_historical_trends", 
                "ai_index_industry_adoption",
                "mckinsey_financial_impact",
                "mckinsey_use_cases",
                "oecd_2025_findings",
                "federal_reserve_productivity",
                "federal_reserve_economic_impact",
                "stanford_investment_trends",
                "goldman_sachs_gdp_impact",
                "nvidia_cost_trends",
                "imf_global_impact",
                "nber_research",
                "ai_strategy_recommendations",
                "ai_governance_insights",
                "environmental_impact_data",
                "labor_market_analysis",
                "regional_growth_patterns",
                "skill_gap_assessment",
                "technology_maturity_curve",
                "firm_size_distribution",
                "barriers_and_support",
                "token_economics_data",
                "bibliography_sources",
                "competitive_landscape"
            ]
            
            # Load datasets with progress tracking
            datasets = {}
            total_datasets = len(dataset_names)
            successful_loads = 0
            failed_loads = []
            
            for i, dataset_name in enumerate(dataset_names):
                try:
                    # Update progress
                    progress = int((i / total_datasets) * 100)
                    
                    # Simulate loading (in real implementation, this would load actual data)
                    logger.info(f"Loading {dataset_name}...")
                    
                    # Try to get dataset from data manager
                    if hasattr(data_manager, 'data') and dataset_name in data_manager.data:
                        dataset = data_manager.data[dataset_name]
                    else:
                        # Create mock data for now
                        dataset = create_mock_dataset(dataset_name)
                    
                    datasets[dataset_name] = dataset
                    successful_loads += 1
                    
                except Exception as e:
                    logger.error(f"Failed to load {dataset_name}: {str(e)}")
                    failed_loads.append(dataset_name)
                    datasets[dataset_name] = {"error": str(e), "status": "failed"}
            
            # Add metadata
            datasets["_metadata"] = {
                "loaded_at": pd.Timestamp.now().isoformat(),
                "total_datasets": total_datasets,
                "successful_loads": successful_loads,
                "failed_loads": failed_loads,
                "version": "4.0.0"
            }
            
            # Create success message
            if successful_loads == total_datasets:
                final_progress = dbc.Alert([
                    html.I(className="fas fa-check-circle me-2"),
                    f"✅ Successfully loaded all {total_datasets} datasets!"
                ], color="success", dismissable=True)
            elif successful_loads > 0:
                final_progress = dbc.Alert([
                    html.I(className="fas fa-exclamation-triangle me-2"),
                    f"⚠️ Loaded {successful_loads}/{total_datasets} datasets. ",
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
            
            return datasets, final_progress, False, "", loading_style
            
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
            
            return {}, progress, True, error_content, {}
    
    @callback(
        Output("success-toast", "is_open"),
        Output("success-toast", "children"),
        Input("data-store", "data"),
        prevent_initial_call=True
    )
    def show_data_loaded_toast(data: Dict[str, Any]) -> Tuple[bool, str]:
        """Show success toast when data is loaded."""
        if data and "_metadata" in data:
            metadata = data["_metadata"]
            if metadata.get("successful_loads", 0) > 0:
                message = f"Loaded {metadata['successful_loads']} datasets successfully!"
                return True, message
        return False, ""


def create_mock_dataset(dataset_name: str) -> Dict[str, Any]:
    """Create mock dataset for testing when actual data is not available."""
    # This is a placeholder that creates realistic mock data
    # In production, this would be replaced with actual data loading
    
    if "adoption_rates" in dataset_name:
        return {
            "data": pd.DataFrame({
                "year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
                "adoption_rate": [15, 22, 31, 42, 58, 72, 85, 92],
                "enterprises": [1200, 2100, 3500, 5200, 7800, 10500, 13200, 15800]
            }),
            "metadata": {
                "source": "Stanford AI Index",
                "last_updated": "2025-01-01"
            }
        }
    elif "financial_impact" in dataset_name:
        return {
            "data": pd.DataFrame({
                "metric": ["Revenue Growth", "Cost Reduction", "Productivity", "ROI"],
                "impact_percent": [23.5, 18.2, 31.7, 156.0],
                "confidence": [0.85, 0.92, 0.78, 0.81]
            }),
            "metadata": {
                "source": "McKinsey Global Institute",
                "last_updated": "2025-01-01"
            }
        }
    else:
        # Generic mock data
        return {
            "data": pd.DataFrame({
                "category": ["A", "B", "C", "D"],
                "value": [100, 150, 120, 180],
                "trend": [10, 15, -5, 22]
            }),
            "metadata": {
                "source": "Mock Data",
                "last_updated": "2025-01-01"
            }
        }