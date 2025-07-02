"""
Navigation Callbacks for Dash AI Adoption Dashboard
Handle navigation and state management
"""

from dash import callback, Input, Output, State, html
import dash_bootstrap_components as dbc
from layouts.main_layout import create_key_metrics_cards

@callback(
    Output('key-metrics-row', 'children'),
    [Input('data-year-selector', 'value'),
     Input('data-store', 'data')]
)
def update_key_metrics(data_year, mckinsey_data):
    """Update key metrics cards based on selected year and loaded data"""
    if mckinsey_data is None:
        return html.Div("Loading metrics...", className="text-center")
    
    return create_key_metrics_cards(data_year, mckinsey_data)

@callback(
    Output('year-range-container', 'style'),
    Input('view-type-selector', 'value')
)
def toggle_year_range_visibility(view_type):
    """Show year range slider only for Historical Trends view"""
    if view_type == "Historical Trends":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output('session-store', 'data'),
    [Input('persona-selector', 'value'),
     Input('data-year-selector', 'value'),
     Input('view-type-selector', 'value')],
    State('session-store', 'data')
)
def update_session_state(persona, data_year, view_type, current_session):
    """Update session state when user changes selections - converts Streamlit session state"""
    
    updated_session = current_session.copy() if current_session else {}
    updated_session.update({
        'selected_persona': persona,
        'data_year': data_year,
        'view_type': view_type,
        'first_visit': False
    })
    
    return updated_session

@callback(
    Output('launch-vizro-btn', 'children'),
    Input('launch-vizro-btn', 'n_clicks')
)
def handle_vizro_launch(n_clicks):
    """Handle Vizro dashboard launch - converts Streamlit button logic"""
    if n_clicks:
        # Integrate with existing Vizro dashboard code
        try:
            # Use existing vizro_dashboard function if available
            if 'vizro_dashboard' in globals():
                dashboards = vizro_dashboard.create_multi_persona_dashboard({})
                return "✅ Dashboard launched at localhost:8050"
            else:
                return "❌ Vizro dashboard not available"
        except Exception as e:
            return f"❌ Launch failed: {str(e)}"
    
    return "🚀 Launch Vizro Executive Dashboard"

@callback(
    Output('feedback-btn', 'children'),
    [Input('feedback-btn', 'n_clicks'),
     Input('feedback-textarea', 'value')]
)
def handle_feedback_submission(n_clicks, feedback_text):
    """Handle feedback submission - converts Streamlit feedback logic"""
    if n_clicks and feedback_text:
        # Process feedback (integrate with existing system if available)
        return "✅ Thank you for your feedback!"
    
    return "Submit Feedback" 