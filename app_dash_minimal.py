"""
Minimal Dash Application for AI Adoption Dashboard
This version runs without dependencies on the existing codebase
"""
import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MinimalDashboardApp:
    """Minimal Dash application that works standalone."""
    
    def __init__(self):
        # Initialize Dash app
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
            suppress_callback_exceptions=True,
            title="AI Adoption Dashboard | 2018-2025"
        )
        
        # Setup layout and callbacks
        self.setup_layout()
        self.register_callbacks()
    
    def setup_layout(self):
        """Create the main layout."""
        self.app.layout = dbc.Container([
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
            
            # Main content
            dbc.Row([
                # Sidebar
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("📊 Dashboard Controls", className="mb-4"),
                            
                            html.Label("Select View:", className="fw-bold"),
                            dcc.Dropdown(
                                id="view-selector",
                                options=[
                                    {"label": "📈 Adoption Rates", "value": "adoption"},
                                    {"label": "📊 Historical Trends", "value": "trends"},
                                    {"label": "💰 Financial Impact", "value": "financial"},
                                    {"label": "🌍 Geographic Distribution", "value": "geographic"}
                                ],
                                value="adoption",
                                className="mb-4"
                            ),
                            
                            html.Hr(),
                            
                            html.Label("Time Period:", className="fw-bold"),
                            dcc.RangeSlider(
                                id="year-slider",
                                min=2018,
                                max=2025,
                                value=[2018, 2025],
                                marks={i: str(i) for i in range(2018, 2026)},
                                className="mb-4"
                            ),
                            
                            html.Hr(),
                            
                            dbc.Alert([
                                html.I(className="fas fa-info-circle me-2"),
                                "This is a minimal demo version"
                            ], color="info", className="small")
                        ])
                    ])
                ], width=3),
                
                # Main content
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
            ])
        ], fluid=True, className="p-4")
    
    def register_callbacks(self):
        """Register callbacks for interactivity."""
        
        @self.app.callback(
            Output("main-content", "children"),
            [Input("view-selector", "value"),
             Input("year-slider", "value")]
        )
        def update_content(selected_view, year_range):
            """Update main content based on selection."""
            
            if selected_view == "adoption":
                return self.create_adoption_view(year_range)
            elif selected_view == "trends":
                return self.create_trends_view(year_range)
            elif selected_view == "financial":
                return self.create_financial_view(year_range)
            else:
                return self.create_geographic_view(year_range)
    
    def create_adoption_view(self, year_range):
        """Create adoption rates visualization."""
        # Create sample data
        years = list(range(year_range[0], year_range[1] + 1))
        adoption_rates = [15 + (year - 2018) * 11 for year in years]
        
        df = pd.DataFrame({
            'Year': years,
            'Adoption Rate (%)': adoption_rates
        })
        
        # Create chart
        fig = px.bar(
            df, 
            x='Year', 
            y='Adoption Rate (%)',
            title='AI Adoption Rates Over Time',
            color_discrete_sequence=['#3498DB']
        )
        
        fig.update_layout(
            height=500,
            template="plotly_white",
            hovermode="x unified"
        )
        
        return html.Div([
            html.H3("📈 AI Adoption Rates", className="mb-4"),
            
            # Metrics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Current Adoption", className="text-muted"),
                            html.H2("92%", className="text-primary"),
                            html.P("↗ 77% since 2018", className="text-success small")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Leading Sector", className="text-muted"),
                            html.H2("Tech", className="text-primary"),
                            html.P("85% adoption rate", className="text-info small")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Growth Rate", className="text-muted"),
                            html.H2("15%", className="text-primary"),
                            html.P("Annual average", className="text-info small")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Companies", className="text-muted"),
                            html.H2("15.8K", className="text-primary"),
                            html.P("Using AI in 2025", className="text-info small")
                        ])
                    ])
                ], width=3),
            ], className="mb-4"),
            
            # Chart
            dcc.Graph(figure=fig),
            
            # Insights
            dbc.Alert([
                html.H6("Key Insights", className="alert-heading"),
                html.Hr(),
                html.Ul([
                    html.Li("GenAI adoption accelerated dramatically in 2023-2024"),
                    html.Li("Service operations lead with 42% GenAI implementation"),
                    html.Li("Enterprise adoption outpaces consumer adoption by 3:1")
                ])
            ], color="light", className="mt-4")
        ])
    
    def create_trends_view(self, year_range):
        """Create historical trends visualization."""
        # Create sample trend data
        years = list(range(year_range[0], year_range[1] + 1))
        
        df = pd.DataFrame({
            'Year': years * 3,
            'Metric': ['Adoption'] * len(years) + ['Investment'] * len(years) + ['ROI'] * len(years),
            'Value': [15 + (y - 2018) * 11 for y in years] + 
                    [100 + (y - 2018) * 50 for y in years] +
                    [50 + (y - 2018) * 20 for y in years]
        })
        
        fig = px.line(
            df,
            x='Year',
            y='Value',
            color='Metric',
            title='AI Trends Over Time',
            markers=True
        )
        
        fig.update_layout(
            height=500,
            template="plotly_white",
            hovermode="x unified"
        )
        
        return html.Div([
            html.H3("📊 Historical Trends", className="mb-4"),
            dcc.Graph(figure=fig)
        ])
    
    def create_financial_view(self, year_range):
        """Create financial impact visualization."""
        categories = ['Revenue Growth', 'Cost Reduction', 'Productivity', 'Customer Satisfaction']
        values = [23.5, 18.2, 31.7, 28.4]
        
        fig = px.bar(
            x=categories,
            y=values,
            title='Financial Impact of AI Implementation (%)',
            color_discrete_sequence=['#2ECC71']
        )
        
        fig.update_layout(
            height=400,
            template="plotly_white",
            xaxis_title="Impact Category",
            yaxis_title="Improvement (%)"
        )
        
        return html.Div([
            html.H3("💰 Financial Impact", className="mb-4"),
            dcc.Graph(figure=fig),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("$156B", className="text-success"),
                            html.P("Total AI Investment (2025)", className="text-muted")
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("156%", className="text-info"),
                            html.P("Average ROI", className="text-muted")
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("18 mo", className="text-warning"),
                            html.P("Payback Period", className="text-muted")
                        ])
                    ])
                ], width=4)
            ], className="mt-4")
        ])
    
    def create_geographic_view(self, year_range):
        """Create geographic distribution visualization."""
        data = {
            'Region': ['North America', 'Europe', 'Asia Pacific', 'Rest of World'],
            'Adoption Rate': [78, 65, 82, 45]
        }
        
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df,
            values='Adoption Rate',
            names='Region',
            title='AI Adoption by Region (2025)'
        )
        
        fig.update_layout(
            height=500,
            template="plotly_white"
        )
        
        return html.Div([
            html.H3("🌍 Geographic Distribution", className="mb-4"),
            dcc.Graph(figure=fig)
        ])
    
    def run(self, debug=True, host="0.0.0.0", port=8050):
        """Run the application."""
        self.app.run_server(debug=debug, host=host, port=port)


if __name__ == "__main__":
    print("Starting Minimal AI Adoption Dashboard...")
    app = MinimalDashboardApp()
    app.run()