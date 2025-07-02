"""
Visualization Callbacks for Dash AI Adoption Dashboard
Handle main content visualization and view routing
"""

from dash import callback, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

@callback(
    Output('main-content-area', 'children'),
    [Input('view-type-selector', 'value'),
     Input('data-year-selector', 'value'),
     Input('persona-selector', 'value'),
     Input('year-range-slider', 'value'),
     Input('data-store', 'data')]
)
def update_main_content(view_type, data_year, persona, year_range, mckinsey_data):
    """Main content router - converts Streamlit view_type logic to Dash"""
    
    if mckinsey_data is None:
        return dbc.Spinner(html.Div("Loading dashboard data..."), color="primary")
    
    # Convert data from dict format back to DataFrames
    dashboard_data = {}
    for key, value in mckinsey_data.items():
        if isinstance(value, list):
            dashboard_data[key] = pd.DataFrame(value)
        else:
            dashboard_data[key] = value
    
    # Route to appropriate view function
    if view_type == "Historical Trends":
        return create_historical_trends_view(dashboard_data, year_range, persona)
    elif view_type == "Industry Analysis":
        return create_industry_analysis_view(dashboard_data, data_year)
    elif view_type == "Financial Impact":
        return create_financial_impact_view(dashboard_data)
    elif view_type == "Investment Trends":
        return create_investment_trends_view(dashboard_data)
    elif view_type == "Geographic Distribution":
        return create_geographic_distribution_view(dashboard_data)
    elif view_type == "AI Chart Generator":
        return create_ai_chart_generator_view(dashboard_data)
    else:
        return create_default_view(view_type, dashboard_data)

def create_historical_trends_view(dashboard_data, year_range, persona):
    """Create Historical Trends view - converts Streamlit Historical Trends section"""
    
    # Get historical data
    historical_data = dashboard_data.get('historical_data', pd.DataFrame())
    
    if historical_data.empty:
        return dbc.Alert("Historical data not available", color="warning")
    
    # Filter data by year range
    filtered_data = historical_data[
        (historical_data['year'] >= year_range[0]) & 
        (historical_data['year'] <= year_range[1])
    ]
    
    # Create the same Plotly figure as in Streamlit
    fig = go.Figure()
    
    # Add overall AI use line
    fig.add_trace(go.Scatter(
        x=filtered_data['year'], 
        y=filtered_data['ai_use'], 
        mode='lines+markers', 
        name='Overall AI Use', 
        line=dict(width=4, color='#1f77b4'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Adoption: %{y}%<br>Source: AI Index & McKinsey<extra></extra>'
    ))
    
    # Add GenAI use line
    fig.add_trace(go.Scatter(
        x=filtered_data['year'], 
        y=filtered_data['genai_use'], 
        mode='lines+markers', 
        name='GenAI Use', 
        line=dict(width=4, color='#ff7f0e'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Adoption: %{y}%<br>Source: AI Index 2025<extra></extra>'
    ))
    
    # Add annotations
    if 2022 in filtered_data['year'].values:
        fig.add_annotation(
            x=2022, y=33,
            text="<b>ChatGPT Launch</b><br>GenAI Era Begins<br><i>Source: Stanford AI Index</i>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#ff7f0e",
            ax=-50,
            ay=-40,
            bgcolor="rgba(255,127,14,0.1)",
            bordercolor="#ff7f0e",
            borderwidth=2,
            font=dict(color="#ff7f0e", size=11, family="Arial")
        )
    
    fig.update_layout(
        title="AI Adoption Trends: The GenAI Revolution", 
        xaxis_title="Year", 
        yaxis_title="Adoption Rate (%)",
        height=500,
        hovermode='x unified'
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H3("📈 Historical Trends: AI Adoption Evolution", className="mb-0"),
            html.Small("Data Sources: AI Index Report 2025, McKinsey Global Survey", className="text-muted")
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, id='historical-trends-chart'),
            dbc.Alert([
                html.Strong("Key Insight: "),
                "The GenAI revolution (2022-2025) accelerated AI adoption by 23 percentage points, ",
                "with generative AI adoption jumping from 33% to 71% in just two years."
            ], color="info", className="mt-3")
        ])
    ])

def create_industry_analysis_view(dashboard_data, data_year):
    """Create Industry Analysis view"""
    
    industry_data = dashboard_data.get('industry_data', pd.DataFrame())
    
    if industry_data.empty:
        return dbc.Alert("Industry data not available", color="warning")
    
    # Create sector comparison chart (adoption rate)
    adoption_fig = px.bar(
        industry_data,
        x='sector',
        y='adoption_rate',
        color='adoption_rate',
        color_continuous_scale='Blues',
        title='AI Adoption Rate by Industry Sector',
        text_auto=True
    )
    adoption_fig.update_layout(
        title_font_size=18,
        xaxis_title="Industry Sector",
        yaxis_title="Adoption Rate (%)",
        height=400
    )
    
    # ROI comparison
    roi_fig = px.bar(
        industry_data,
        x='sector',
        y='roi_percentage',
        color='roi_percentage',
        color_continuous_scale='Greens',
        title='ROI (%) by Industry Sector',
        text_auto=True
    )
    roi_fig.update_layout(
        title_font_size=18,
        xaxis_title="Industry Sector",
        yaxis_title="ROI (%)",
        height=400
    )
    
    # Productivity comparison
    prod_fig = px.bar(
        industry_data,
        x='sector',
        y='productivity_gain',
        color='productivity_gain',
        color_continuous_scale='Purples',
        title='Productivity Gain by Industry Sector',
        text_auto=True
    )
    prod_fig.update_layout(
        title_font_size=18,
        xaxis_title="Industry Sector",
        yaxis_title="Productivity Gain (Index)",
        height=400
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H3("🏭 Industry Analysis: Sector Comparison", className="mb-0"),
            html.Small("Data Sources: McKinsey Global Survey, Industry Reports", className="text-muted")
        ]),
        dbc.CardBody([
            html.H5("AI Adoption Rate by Sector", className="mb-3"),
            dcc.Graph(figure=adoption_fig, id='industry-adoption-chart'),
            html.H5("ROI by Sector", className="mb-3 mt-4"),
            dcc.Graph(figure=roi_fig, id='industry-roi-chart'),
            html.H5("Productivity Gain by Sector", className="mb-3 mt-4"),
            dcc.Graph(figure=prod_fig, id='industry-productivity-chart'),
            dbc.Alert([
                html.Strong("Key Insights: "),
                html.Ul([
                    html.Li("Technology (91%) and Finance (85%) lead AI adoption, with the highest ROI and productivity gains."),
                    html.Li("Manufacturing and Retail show significant growth potential but lag in ROI."),
                    html.Li("Sector-specific strategies are critical for maximizing AI value.")
                ])
            ], color="info", className="mt-3"),
            html.Div([
                html.Small([
                    "Source: McKinsey Global Survey on AI, AI Index Report 2025, Industry Reports. "
                    "All metrics reflect latest available data as of 2025."
                ], className="text-muted")
            ], className="mt-2")
        ])
    ])

def create_financial_impact_view(dashboard_data):
    """Create Financial Impact view"""
    
    historical_data = dashboard_data.get('historical_data', pd.DataFrame())
    
    if historical_data.empty:
        return dbc.Alert("Financial data not available", color="warning")
    
    # Create investment trends line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical_data['year'],
        y=historical_data['investment_billions'],
        mode='lines+markers',
        name='AI Investment (Billions $)',
        line=dict(width=4, color='#2ca02c'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Investment: $%{y}B<extra></extra>'
    ))
    fig.update_layout(
        title="AI Investment Trends: 2018-2025",
        xaxis_title="Year",
        yaxis_title="Investment (Billions USD)",
        height=500,
        hovermode='x unified',
        title_font_size=18
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H3("💰 Financial Impact: Investment Trends", className="mb-0"),
            html.Small("Data Sources: CB Insights, PitchBook, Industry Reports", className="text-muted")
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, id='financial-impact-chart'),
            dbc.Alert([
                html.Strong("Investment Surge: "),
                "AI investment reached $252.3B in 2024, a 44.5% year-over-year increase, ",
                "driven by GenAI adoption and enterprise AI initiatives."
            ], color="warning", className="mt-3"),
            html.Div([
                html.Small([
                    "Source: CB Insights, PitchBook, AI Index Report 2025. "
                    "All investment figures are inflation-adjusted and reflect latest available data as of 2025."
                ], className="text-muted")
            ], className="mt-2")
        ])
    ])

def create_investment_trends_view(dashboard_data):
    """Create Investment Trends view"""
    return dbc.Alert("Investment Trends view - Coming Soon", color="info")

def create_geographic_distribution_view(dashboard_data):
    """Create Geographic Distribution view"""
    
    geographic_data = dashboard_data.get('geographic_data', pd.DataFrame())
    
    if geographic_data.empty:
        return dbc.Alert("Geographic data not available", color="warning")
    
    # Create geographic chart
    fig = px.bar(
        geographic_data,
        x='country',
        y='adoption_rate',
        color='gdp_impact',
        title='AI Adoption by Country',
        color_continuous_scale='plasma',
        hover_data=['gdp_impact']
    )
    
    fig.update_layout(
        title_font_size=18,
        xaxis_title="Country",
        yaxis_title="Adoption Rate (%)",
        height=500
    )
    
    return dbc.Card([
        dbc.CardHeader([
            html.H3("🌍 Geographic Distribution: Global AI Adoption", className="mb-0"),
            html.Small("Data Sources: OECD, World Bank, National Surveys", className="text-muted")
        ]),
        dbc.CardBody([
            dcc.Graph(figure=fig, id='geographic-distribution-chart'),
            dbc.Alert([
                html.Strong("Global Leaders: "),
                "USA (78%) and China (72%) lead global AI adoption, ",
                "with significant economic impact across all regions."
            ], color="primary", className="mt-3")
        ])
    ])

def create_ai_chart_generator_view(dashboard_data):
    """Create AI Chart Generator view"""
    return dbc.Card([
        dbc.CardHeader([
            html.H3("🤖 AI Chart Generator", className="mb-0"),
            html.Small("Powered by Vizro-AI", className="text-muted")
        ]),
        dbc.CardBody([
            dbc.Alert([
                html.Strong("Coming Soon: "),
                "AI-powered chart generation feature will be available in the next update."
            ], color="info")
        ])
    ])

def create_default_view(view_type, dashboard_data):
    """Create default view for unimplemented view types"""
    return dbc.Card([
        dbc.CardHeader([
            html.H3(f"📊 {view_type}", className="mb-0"),
            html.Small("View under development", className="text-muted")
        ]),
        dbc.CardBody([
            dbc.Alert([
                html.Strong("Feature in Progress: "),
                f"The {view_type} view is being migrated from Streamlit to Dash. ",
                "Please check back soon for the complete implementation."
            ], color="warning")
        ])
    ])

def register_visualization_callbacks(app):
    """Register all visualization callbacks with the Dash app"""
    
    @app.callback(
        Output('chart-container', 'children'),
        [Input('chart-type-selector', 'value'),
         Input('data-store', 'data')]
    )
    def update_chart(chart_type, data):
        """Update chart based on selected type and data"""
        if data is None or chart_type is None:
            return html.Div("Select chart type and ensure data is loaded", className="text-center")
        
        try:
            if chart_type == 'adoption_trends':
                return create_adoption_trends_chart(data)
            elif chart_type == 'industry_comparison':
                return create_industry_comparison_chart(data)
            elif chart_type == 'investment_analysis':
                return create_investment_analysis_chart(data)
            else:
                return html.Div("Chart type not implemented", className="text-center")
        except Exception as e:
            return html.Div(f"Error creating chart: {str(e)}", className="text-center text-danger")

    def create_adoption_trends_chart(data):
        """Create adoption trends line chart"""
        try:
            if 'historical_data' in data:
                df = pd.DataFrame(data['historical_data'])
                fig = px.line(df, x='year', y='ai_use', 
                            title='AI Adoption Trends (2018-2025)',
                            labels={'year': 'Year', 'ai_use': 'AI Adoption Rate (%)'})
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="AI Adoption Rate (%)",
                    hovermode='x unified'
                )
                return dcc.Graph(figure=fig)
            else:
                return html.Div("Historical data not available", className="text-center")
        except Exception as e:
            return html.Div(f"Error creating adoption trends chart: {str(e)}", className="text-center text-danger")

    def create_industry_comparison_chart(data):
        """Create industry comparison bar chart"""
        try:
            if 'industry_data' in data:
                df = pd.DataFrame(data['industry_data'])
                fig = px.bar(df, x='sector', y='adoption_rate',
                           title='AI Adoption by Industry Sector',
                           labels={'sector': 'Industry Sector', 'adoption_rate': 'Adoption Rate (%)'})
                fig.update_layout(
                    xaxis_title="Industry Sector",
                    yaxis_title="Adoption Rate (%)"
                )
                return dcc.Graph(figure=fig)
            else:
                return html.Div("Industry data not available", className="text-center")
        except Exception as e:
            return html.Div(f"Error creating industry comparison chart: {str(e)}", className="text-center text-danger")

    def create_investment_analysis_chart(data):
        """Create investment analysis chart"""
        try:
            if 'historical_data' in data:
                df = pd.DataFrame(data['historical_data'])
                fig = px.line(df, x='year', y='investment_billions',
                           title='AI Investment Trends (2018-2025)',
                           labels={'year': 'Year', 'investment_billions': 'Investment ($B)'})
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Investment ($B)",
                    hovermode='x unified'
                )
                return dcc.Graph(figure=fig)
            else:
                return html.Div("Investment data not available", className="text-center")
        except Exception as e:
            return html.Div(f"Error creating investment analysis chart: {str(e)}", className="text-center text-danger")

    @app.callback(
        Output('chart-options', 'children'),
        [Input('data-store', 'data')]
    )
    def update_chart_options(data):
        """Update available chart options based on loaded data"""
        if data is None:
            return html.Div("No data loaded", className="text-center")
        
        available_charts = []
        if 'historical_data' in data:
            available_charts.extend(['adoption_trends', 'investment_analysis'])
        if 'industry_data' in data:
            available_charts.append('industry_comparison')
        
        if available_charts:
            return html.Div([
                html.Label("Select Chart Type:", className="form-label"),
                dcc.Dropdown(
                    id='chart-type-selector',
                    options=[{'label': chart.replace('_', ' ').title(), 'value': chart} 
                            for chart in available_charts],
                    value=available_charts[0] if available_charts else None,
                    className="form-select"
                )
            ])
        else:
            return html.Div("No compatible data for charts", className="text-center") 