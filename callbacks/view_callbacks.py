"""
View management callbacks for the AI Adoption Dashboard.
Handles view selection, routing, and rendering.
"""
import dash
from dash import Input, Output, State, callback, html, dcc, ALL, MATCH
import dash_bootstrap_components as dbc
import logging
import traceback
from typing import List, Tuple, Any, Dict

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dash_view_manager import DashViewManager

logger = logging.getLogger(__name__)

def register_view_callbacks(app):
    """Register all view-related callbacks."""
    
    # Initialize view manager
    view_manager = DashViewManager()
    
    @app.callback(
        Output("sidebar-content", "children"),
        Input("persona-store", "data")
    )
    def render_sidebar(persona: str) -> html.Div:
        """Render the sidebar based on current persona."""
        return view_manager.create_sidebar_layout()
    
    @app.callback(
        [Output("view-selector", "options"),
         Output("view-selector", "value"),
         Output("persona-recommendations", "children")],
        [Input("persona-selector", "value"),
         Input("category-filter", "value")],
        [State("view-selector", "value")]
    )
    def update_view_options(persona: str, filters: List[str], current_view: str) -> Tuple[List[Dict], str, html.Div]:
        """Update available views based on persona and filters."""
        recommended_only = "recommended" in filters if filters else False
        
        # Get view options
        options = view_manager.get_view_options(persona, recommended_only)
        
        # Determine default view
        if current_view and any(opt["value"] == current_view for opt in options if not opt.get("disabled")):
            # Keep current view if it's still available
            default_view = current_view
        else:
            # Select first non-disabled option
            valid_options = [opt for opt in options if not opt.get("disabled")]
            default_view = valid_options[0]["value"] if valid_options else None
        
        # Create recommendations
        recommendations = view_manager.create_persona_recommendations(persona)
        
        return options, default_view, recommendations
    
    @app.callback(
        Output("view-description", "children"),
        Input("view-selector", "value")
    )
    def update_view_description(view_id: str) -> html.Div:
        """Update view description when selection changes."""
        return view_manager.create_view_description(view_id)
    
    @app.callback(
        [Output("main-content", "children"),
         Output("view-store", "data"),
         Output("error-modal", "is_open"),
         Output("error-content", "children")],
        [Input("view-selector", "value"),
         Input("data-store", "data")],
        [State("persona-store", "data")],
        prevent_initial_call=False
    )
    def render_main_view(view_id: str, data: Dict[str, Any], persona: str) -> Tuple[html.Div, str, bool, Any]:
        """Render the selected view with loaded data."""
        try:
            # Check if we have data
            if not data or "_metadata" not in data:
                loading_content = dbc.Container([
                    html.Div([
                        dbc.Spinner(color="primary", size="lg"),
                        html.H4("Loading data...", className="mt-3 text-muted")
                    ], className="text-center py-5")
                ])
                return loading_content, view_id, False, ""
            
            # Check if view is valid
            if not view_id or view_id.startswith("_category_"):
                placeholder = html.Div([
                    html.H4("Select a view to begin", className="text-muted text-center mt-5"),
                    html.P("Choose an analysis view from the dropdown menu", className="text-center")
                ])
                return placeholder, view_id, False, ""
            
            # Load view module
            view_module = view_manager.load_view_module(view_id)
            
            if not view_module:
                # Show error for missing view
                error_content = html.Div([
                    html.H5(f"View Not Available: {view_id}"),
                    html.P("This view has not been migrated to Dash yet."),
                    html.Hr(),
                    html.P("Please select another view or check back later.")
                ])
                
                placeholder = dbc.Alert([
                    html.H5("View Not Available", className="alert-heading"),
                    html.P(f"The '{view_id}' view is being migrated to the new system."),
                    html.P("Please select another view from the dropdown.", className="mb-0")
                ], color="warning")
                
                return placeholder, view_id, False, ""
            
            # Check if module has create_layout function
            if not hasattr(view_module, 'create_layout'):
                logger.error(f"View module '{view_id}' missing create_layout function")
                
                error_content = html.Div([
                    html.H5("View Configuration Error"),
                    html.P(f"The '{view_id}' view is not properly configured."),
                    html.P("Missing create_layout function in view module.")
                ])
                
                return create_error_view(view_id, "Configuration error"), view_id, True, error_content
            
            # Render the view
            try:
                view_content = view_module.create_layout(data, persona)
                
                # Wrap in container with consistent styling
                wrapped_content = html.Div([
                    # View header
                    html.Div([
                        html.H3(view_manager.all_views[view_id]["label"], className="mb-3"),
                        html.Hr(className="mb-4")
                    ]),
                    
                    # View content
                    view_content
                ], className="view-wrapper")
                
                return wrapped_content, view_id, False, ""
                
            except Exception as e:
                logger.error(f"Error rendering view '{view_id}': {str(e)}")
                logger.error(traceback.format_exc())
                
                error_content = html.Div([
                    html.H5("Error Rendering View"),
                    html.P(f"An error occurred while rendering '{view_id}':"),
                    dbc.Alert(str(e), color="danger"),
                    html.Details([
                        html.Summary("Technical Details"),
                        html.Pre(traceback.format_exc(), className="text-monospace small")
                    ])
                ])
                
                return create_error_view(view_id, str(e)), view_id, True, error_content
                
        except Exception as e:
            logger.error(f"Critical error in view rendering: {str(e)}")
            logger.error(traceback.format_exc())
            
            error_view = create_error_view("Unknown", str(e))
            error_modal_content = html.Div([
                html.H5("Critical Error"),
                html.P("A critical error occurred:"),
                dbc.Alert(str(e), color="danger")
            ])
            
            return error_view, "", True, error_modal_content
    
    @app.callback(
        Output("persona-store", "data"),
        Input("persona-selector", "value"),
        prevent_initial_call=True
    )
    def update_persona_store(persona: str) -> str:
        """Update persona in browser storage."""
        return persona
    
    @app.callback(
        Output("export-data-btn", "disabled"),
        [Input("view-store", "data"),
         Input("data-store", "data")]
    )
    def toggle_export_button(current_view: str, data: Dict) -> bool:
        """Enable/disable export button based on data availability."""
        return not (current_view and data and "_metadata" in data)
    
    @app.callback(
        Output("data-status", "children"),
        Input("data-store", "data"),
        prevent_initial_call=True
    )
    def update_data_status(data: Dict[str, Any]) -> html.Div:
        """Update data status indicator in sidebar."""
        if not data or "_metadata" not in data:
            return dbc.Alert("No data loaded", color="warning", className="small py-2")
        
        metadata = data["_metadata"]
        successful = metadata.get("successful_loads", 0)
        total = metadata.get("total_datasets", 0)
        
        if successful == total:
            color = "success"
            icon = "check-circle"
            text = f"All {total} datasets loaded"
        elif successful > 0:
            color = "warning"
            icon = "exclamation-triangle"
            text = f"{successful}/{total} datasets loaded"
        else:
            color = "danger"
            icon = "times-circle"
            text = "No datasets loaded"
        
        return dbc.Alert([
            html.I(className=f"fas fa-{icon} me-2"),
            text
        ], color=color, className="small py-2 mb-0")


def create_error_view(view_id: str, error_message: str) -> html.Div:
    """Create a user-friendly error view."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Error Loading View"
                    ], className="alert-heading"),
                    html.Hr(),
                    html.P(f"Failed to load view: {view_id}"),
                    html.P(error_message, className="mb-0 small text-muted")
                ], color="danger"),
                
                html.Div([
                    html.H5("What you can do:"),
                    html.Ul([
                        html.Li("Try selecting a different view"),
                        html.Li("Refresh the page"),
                        html.Li("Check the browser console for more details")
                    ])
                ], className="mt-4")
            ], width=8, className="mx-auto")
        ])
    ], className="mt-5")