"""
Dash View Manager - Handles view routing and management for the dashboard.
Converts the Streamlit ViewManager to work with Dash.
"""
from typing import Dict, List, Any, Optional
import importlib
import logging
from dash import html, dcc
import dash_bootstrap_components as dbc

logger = logging.getLogger(__name__)

class DashViewManager:
    """Manages view routing and persona-based recommendations for Dash."""
    
    def __init__(self):
        """Initialize the view manager with all available views."""
        # Map view IDs to their modules and metadata
        self.all_views = {
            # Adoption Views
            "adoption_rates": {
                "label": "📈 Adoption Rates", 
                "module": "views.adoption.adoption_rates_dash",
                "category": "adoption",
                "personas": ["General", "Business Leader", "Policymaker"],
                "description": "Track AI adoption rates across industries and time"
            },
            "historical_trends": {
                "label": "📊 Historical Trends",
                "module": "views.adoption.historical_trends_dash", 
                "category": "adoption",
                "personas": ["General", "Researcher", "Policymaker"],
                "description": "Analyze AI adoption trends from 2018 to 2025"
            },
            "industry_analysis": {
                "label": "🏭 Industry Analysis",
                "module": "views.adoption.industry_analysis_dash",
                "category": "adoption", 
                "personas": ["Business Leader", "Researcher"],
                "description": "Deep dive into industry-specific AI adoption"
            },
            "firm_size_analysis": {
                "label": "🏢 Firm Size Analysis",
                "module": "views.adoption.firm_size_analysis_dash",
                "category": "adoption",
                "personas": ["Business Leader", "Policymaker"],
                "description": "AI adoption patterns by company size"
            },
            "technology_stack": {
                "label": "🔧 Technology Stack",
                "module": "views.adoption.technology_stack_dash",
                "category": "adoption",
                "personas": ["Researcher", "Business Leader"],
                "description": "Most adopted AI technologies and tools"
            },
            "ai_technology_maturity": {
                "label": "🎯 Technology Maturity",
                "module": "views.adoption.ai_technology_maturity_dash",
                "category": "adoption",
                "personas": ["Researcher", "Business Leader"],
                "description": "AI technology maturity curve analysis"
            },
            
            # Economic Views
            "investment_trends": {
                "label": "💰 Investment Trends",
                "module": "views.economic.investment_trends_dash",
                "category": "economic",
                "personas": ["General", "Business Leader", "Policymaker"],
                "description": "AI investment patterns and projections"
            },
            "financial_impact": {
                "label": "💵 Financial Impact",
                "module": "views.economic.financial_impact_dash",
                "category": "economic",
                "personas": ["Business Leader", "Policymaker"],
                "description": "Quantify financial benefits of AI adoption"
            },
            "roi_analysis": {
                "label": "📊 ROI Analysis",
                "module": "views.economic.roi_analysis_dash",
                "category": "economic",
                "personas": ["Business Leader"],
                "description": "Calculate and analyze AI investment returns"
            },
            "ai_cost_trends": {
                "label": "📉 AI Cost Trends",
                "module": "views.adoption.ai_cost_trends_dash",
                "category": "economic",
                "personas": ["Business Leader", "Researcher"],
                "description": "Track AI implementation cost evolution"
            },
            
            # Geographic Views
            "geographic_distribution": {
                "label": "🗺️ Geographic Distribution",
                "module": "views.geographic.geographic_distribution_dash",
                "category": "geographic",
                "personas": ["Policymaker", "Researcher"],
                "description": "Global AI adoption by region"
            },
            "regional_growth": {
                "label": "🌍 Regional Growth",
                "module": "views.geographic.regional_growth_dash",
                "category": "geographic",
                "personas": ["Policymaker", "Researcher"],
                "description": "Regional AI growth patterns and forecasts"
            },
            
            # Research & Analysis Views
            "productivity_research": {
                "label": "🔬 Productivity Research",
                "module": "views.adoption.productivity_research_dash",
                "category": "research",
                "personas": ["Researcher", "Business Leader"],
                "description": "Latest research on AI productivity gains"
            },
            "labor_impact": {
                "label": "👥 Labor Impact",
                "module": "views.adoption.labor_impact_dash",
                "category": "research",
                "personas": ["General", "Policymaker", "Researcher"],
                "description": "AI's impact on employment and workforce"
            },
            "skill_gap_analysis": {
                "label": "🎓 Skill Gap Analysis",
                "module": "views.adoption.skill_gap_analysis_dash",
                "category": "research",
                "personas": ["Policymaker", "Business Leader"],
                "description": "Identify and analyze AI skill gaps"
            },
            "oecd_2025_findings": {
                "label": "📋 OECD 2025 Findings",
                "module": "views.adoption.oecd_2025_findings_dash",
                "category": "research",
                "personas": ["Policymaker", "Researcher"],
                "description": "Key findings from OECD AI report 2025"
            },
            
            # Other Views
            "ai_governance": {
                "label": "⚖️ AI Governance",
                "module": "views.other.ai_governance_dash",
                "category": "other",
                "personas": ["Policymaker", "Business Leader"],
                "description": "AI governance frameworks and policies"
            },
            "environmental_impact": {
                "label": "🌱 Environmental Impact",
                "module": "views.other.environmental_impact_dash",
                "category": "other",
                "personas": ["Policymaker", "Researcher"],
                "description": "Environmental implications of AI adoption"
            },
            "token_economics": {
                "label": "🪙 Token Economics",
                "module": "views.other.token_economics_dash",
                "category": "other",
                "personas": ["Researcher", "Business Leader"],
                "description": "Economics of AI token usage and pricing"
            },
            "barriers_support": {
                "label": "🚧 Barriers & Support",
                "module": "views.adoption.barriers_support_dash",
                "category": "other",
                "personas": ["Business Leader", "Policymaker"],
                "description": "AI adoption barriers and support mechanisms"
            },
            "bibliography_sources": {
                "label": "📚 Bibliography & Sources",
                "module": "views.other.bibliography_sources_dash",
                "category": "other",
                "personas": ["General", "Researcher"],
                "description": "Data sources and references"
            }
        }
        
        # Define persona-based view recommendations
        self.persona_views = {
            "General": [
                "adoption_rates", "historical_trends", "investment_trends", 
                "labor_impact", "bibliography_sources"
            ],
            "Business Leader": [
                "adoption_rates", "industry_analysis", "financial_impact", 
                "roi_analysis", "firm_size_analysis", "ai_cost_trends",
                "technology_stack", "barriers_support"
            ],
            "Policymaker": [
                "adoption_rates", "geographic_distribution", "oecd_2025_findings", 
                "regional_growth", "ai_governance", "labor_impact", 
                "environmental_impact", "skill_gap_analysis"
            ],
            "Researcher": [
                "historical_trends", "productivity_research", "technology_stack",
                "ai_technology_maturity", "environmental_impact", "labor_impact",
                "token_economics", "bibliography_sources"
            ]
        }
        
        # Category metadata
        self.categories = {
            "adoption": {"label": "AI Adoption", "icon": "fas fa-chart-line"},
            "economic": {"label": "Economic Impact", "icon": "fas fa-dollar-sign"},
            "geographic": {"label": "Geographic Analysis", "icon": "fas fa-globe"},
            "research": {"label": "Research & Insights", "icon": "fas fa-microscope"},
            "other": {"label": "Additional Analysis", "icon": "fas fa-ellipsis-h"}
        }
    
    def create_sidebar_layout(self) -> html.Div:
        """Create the sidebar layout with persona and view selection."""
        return html.Div([
            html.H4([
                html.I(className="fas fa-cog me-2"),
                "Dashboard Controls"
            ], className="mb-4"),
            
            # Persona selector
            html.Div([
                html.Label("Select Your Role:", className="form-label fw-bold"),
                dcc.Dropdown(
                    id="persona-selector",
                    options=[
                        {"label": "👤 General User", "value": "General"},
                        {"label": "💼 Business Leader", "value": "Business Leader"},
                        {"label": "🏛️ Policymaker", "value": "Policymaker"},
                        {"label": "🔬 Researcher", "value": "Researcher"}
                    ],
                    value="General",
                    className="mb-3",
                    clearable=False
                )
            ]),
            
            # Persona recommendations card
            html.Div(id="persona-recommendations", className="mb-4"),
            
            # View selector
            html.Div([
                html.Label("Analysis View:", className="form-label fw-bold"),
                dcc.Dropdown(
                    id="view-selector",
                    className="mb-3",
                    clearable=False,
                    searchable=True
                )
            ]),
            
            # View description
            html.Div(id="view-description", className="mb-4"),
            
            # Quick filters
            html.Div([
                html.Label("Quick Filters:", className="form-label fw-bold"),
                dcc.Checklist(
                    id="category-filter",
                    options=[
                        {"label": " Show recommended only", "value": "recommended"}
                    ],
                    value=[],
                    className="mb-3"
                )
            ]),
            
            # Data controls
            html.Hr(className="my-4"),
            html.Div([
                html.H6([
                    html.I(className="fas fa-database me-2"),
                    "Data Controls"
                ], className="mb-3"),
                
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className="fas fa-sync-alt me-2"), "Refresh"], 
                        id="refresh-data-btn", 
                        color="primary", 
                        size="sm",
                        outline=True
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-download me-2"), "Export"], 
                        id="export-data-btn", 
                        color="secondary", 
                        size="sm",
                        outline=True
                    )
                ], className="w-100")
            ]),
            
            # Data status
            html.Div(id="data-status", className="mt-3")
        ])
    
    def get_view_options(self, persona: str, recommended_only: bool = False) -> List[Dict[str, str]]:
        """Get view options based on selected persona."""
        if recommended_only and persona != "General":
            # Show only recommended views for this persona
            view_ids = self.persona_views.get(persona, [])
        else:
            # Show all views
            view_ids = list(self.all_views.keys())
        
        # Group by category
        options = []
        for category_id, category_info in self.categories.items():
            category_views = [
                vid for vid in view_ids 
                if self.all_views[vid]["category"] == category_id
            ]
            
            if category_views:
                # Add category header
                options.append({
                    "label": f"━━━ {category_info['label']} ━━━",
                    "value": f"_category_{category_id}",
                    "disabled": True
                })
                
                # Add views in this category
                for view_id in category_views:
                    view = self.all_views[view_id]
                    is_recommended = persona in view["personas"]
                    label = view["label"]
                    if is_recommended and persona != "General":
                        label += " ⭐"
                    
                    options.append({
                        "label": f"   {label}",
                        "value": view_id
                    })
        
        return options
    
    def create_persona_recommendations(self, persona: str) -> html.Div:
        """Create persona-specific recommendations card."""
        if persona == "General":
            return html.Div()
        
        recommended_views = self.persona_views.get(persona, [])
        
        return dbc.Alert([
            html.H6([
                html.I(className="fas fa-lightbulb me-2"),
                f"Recommended for {persona}:"
            ], className="alert-heading mb-3"),
            html.Div([
                dbc.Badge(
                    self.all_views[view_id]["label"], 
                    color="primary", 
                    className="me-2 mb-2",
                    pill=True
                )
                for view_id in recommended_views[:6]  # Show top 6
            ])
        ], color="info", className="py-3")
    
    def create_view_description(self, view_id: str) -> html.Div:
        """Create description card for selected view."""
        if not view_id or view_id not in self.all_views:
            return html.Div()
        
        view = self.all_views[view_id]
        
        return dbc.Card([
            dbc.CardBody([
                html.H6(view["label"], className="card-title mb-2"),
                html.P(view["description"], className="card-text small text-muted"),
                html.Div([
                    dbc.Badge(
                        f"For: {persona}", 
                        color="secondary", 
                        className="me-1 small"
                    )
                    for persona in view["personas"]
                ])
            ])
        ], className="mb-3")
    
    def load_view_module(self, view_id: str) -> Optional[Any]:
        """Dynamically load a view module."""
        if view_id not in self.all_views:
            logger.error(f"View '{view_id}' not found in registry")
            return None
        
        try:
            module_path = self.all_views[view_id]["module"]
            module = importlib.import_module(module_path)
            return module
        except ImportError as e:
            logger.error(f"Failed to import view module '{module_path}': {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error loading view '{view_id}': {str(e)}")
            return None