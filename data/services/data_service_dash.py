"""Data service module for the AI Adoption Dashboard - Dash compatible version."""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table

from ..data_integration_dash import load_data as load_integrated_data
from ..data_manager_dash import DataManagerDash

logger = logging.getLogger(__name__)


class DataService:
    """Service class for managing data operations in the dashboard."""
    
    def __init__(self):
        """Initialize the data service."""
        self.data_manager = None
        self._initialize_data_manager()
        
    def _initialize_data_manager(self):
        """Initialize the data manager with error handling."""
        try:
            self.data_manager = DataManagerDash()
            logger.info("Data manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize data manager: {e}")
            self.data_manager = None
            
    def load_all_data(self) -> Dict[str, pd.DataFrame]:
        """Load all data using the integrated data loader."""
        try:
            # Use the integrated data loader which returns a tuple
            data_tuple = load_integrated_data()
            
            # Convert tuple to dictionary for easier access
            data_dict = {
                "historical_data": data_tuple[0],
                "sector_data": data_tuple[1],
                "geographic_df": data_tuple[2],
                "firm_size_data": data_tuple[3],
                "ai_maturity_df": data_tuple[4],
                "ai_investment_df": data_tuple[5],
                "financial_impact_data": data_tuple[6],
                "use_case_data": data_tuple[7],
                "barriers_data": data_tuple[8],
                "talent_data": data_tuple[9],
                "productivity_data": data_tuple[10],
                "governance_data": data_tuple[11],
                "strategy_data": data_tuple[12],
                "use_case_data_full": data_tuple[13],
                "public_sector_data": data_tuple[14]
            }
            
            return data_dict
            
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            return {}
            
    def get_dataset(self, dataset_name: str, source: Optional[str] = None) -> pd.DataFrame:
        """Get a specific dataset."""
        if not self.data_manager:
            logger.error("Data manager not initialized")
            return pd.DataFrame()
            
        try:
            return self.data_manager.get_dataset(dataset_name, source)
        except Exception as e:
            logger.error(f"Failed to get dataset {dataset_name}: {e}")
            return pd.DataFrame()
            
    def get_data_status_summary(self) -> pd.DataFrame:
        """Get a summary of data availability status."""
        if not self.data_manager:
            return pd.DataFrame({
                "dataset": ["No data manager"],
                "available": [False],
                "source": ["N/A"],
                "records": [0]
            })
            
        try:
            all_datasets = self.data_manager.list_datasets()
            status_data = []
            
            for dataset in all_datasets:
                try:
                    df = self.data_manager.get_dataset(dataset)
                    status_data.append({
                        "dataset": dataset,
                        "available": True,
                        "source": "data_manager",
                        "records": len(df)
                    })
                except:
                    status_data.append({
                        "dataset": dataset,
                        "available": False,
                        "source": "data_manager",
                        "records": 0
                    })
                    
            return pd.DataFrame(status_data)
            
        except Exception as e:
            logger.error(f"Failed to get data status: {e}")
            return pd.DataFrame()
            
    def validate_data(self) -> Dict:
        """Validate all data sources."""
        if not self.data_manager:
            return {"error": "Data manager not initialized"}
            
        try:
            return self.data_manager.validate_data()
        except Exception as e:
            logger.error(f"Failed to validate data: {e}")
            return {"error": str(e)}


# Global instance
_data_service_instance = None


def get_data_service() -> DataService:
    """Get or create the global data service instance."""
    global _data_service_instance
    if _data_service_instance is None:
        _data_service_instance = DataService()
    return _data_service_instance


def create_data_error_component(error_message: str, 
                               recovery_suggestions: Optional[list] = None,
                               callback_id_prefix: str = "") -> html.Div:
    """
    Create a Dash component for displaying data errors.
    
    Args:
        error_message: The error message to display
        recovery_suggestions: Optional list of recovery suggestions
        callback_id_prefix: Prefix for component IDs to avoid conflicts
        
    Returns:
        A Dash HTML component displaying the error
    """
    components = []
    
    # Error alert
    components.append(
        dbc.Alert(
            [
                html.I(className="fas fa-exclamation-triangle me-2"),
                error_message
            ],
            color="danger",
            className="mb-3"
        )
    )
    
    # Recovery suggestions
    if recovery_suggestions:
        suggestion_items = [
            html.Li(suggestion) for suggestion in recovery_suggestions
        ]
        
        components.append(
            dbc.Card([
                dbc.CardHeader([
                    html.I(className="fas fa-tools me-2"),
                    "Troubleshooting Steps"
                ]),
                dbc.CardBody([
                    html.Ol(suggestion_items)
                ])
            ], className="mb-3")
        )
    
    # Info tip
    components.append(
        dbc.Alert(
            [
                html.I(className="fas fa-lightbulb me-2"),
                html.Strong("Tip: "),
                "Refresh the page or check the data status below."
            ],
            color="info",
            dismissable=True
        )
    )
    
    # Data status button and container
    components.extend([
        dbc.Button(
            [html.I(className="fas fa-search me-2"), "Check Data Status"],
            id=f"{callback_id_prefix}check-data-status-btn",
            color="primary",
            className="mb-3"
        ),
        dcc.Loading(
            id=f"{callback_id_prefix}loading-data-status",
            children=[
                html.Div(id=f"{callback_id_prefix}data-status-container")
            ]
        )
    ])
    
    return html.Div(components, className="p-3")


def create_data_status_display(status_df: pd.DataFrame) -> html.Div:
    """Create a Dash component displaying data status summary."""
    if status_df.empty:
        return html.Div("No data status available")
    
    # Calculate metrics
    total = len(status_df)
    available = status_df["available"].sum() if "available" in status_df else 0
    missing = total - available
    
    # Create metric cards
    metrics = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Datasets", className="text-muted"),
                    html.H3(str(total))
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Available", className="text-muted"),
                    html.H3(str(available)),
                    html.Small(f"{available/total*100:.0f}%", className="text-success")
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Missing", className="text-muted"),
                    html.H3(str(missing)),
                    html.Small(f"{missing/total*100:.0f}%", className="text-danger")
                ])
            ])
        ], width=4)
    ], className="mb-4")
    
    # Create data table
    table = dash_table.DataTable(
        data=status_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in status_df.columns],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{available} = True',
                    'column_id': 'available'
                },
                'backgroundColor': '#90EE90',
            },
            {
                'if': {
                    'filter_query': '{available} = False',
                    'column_id': 'available'
                },
                'backgroundColor': '#FFB6C1',
            }
        ],
        style_cell={'textAlign': 'left'},
        style_table={'overflowX': 'auto'}
    )
    
    return html.Div([metrics, table])