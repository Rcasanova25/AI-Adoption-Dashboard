"""
Template Management System for AI Adoption Dashboard Exports

Professional template management for consistent branding, formatting,
and styling across all export formats.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging

from .core import ExportSettings

logger = logging.getLogger(__name__)


class TemplateManager:
    """
    Centralized template management system
    
    Features:
    - Professional report templates for each persona
    - Consistent branding and styling
    - Customizable layouts and themes
    - Template validation and versioning
    - Multi-format template support
    """
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        self._create_default_templates()
    
    def get_template(self, template_type: str, persona: Optional[str] = None, format: str = "general") -> Dict[str, Any]:
        """Get template configuration for specific type and persona"""
        template_key = f"{template_type}_{persona or 'general'}_{format}".lower()
        
        # Try specific template first, then fallback to general
        template = self._load_template(template_key)
        if not template:
            template = self._load_template(f"{template_type}_general_{format}")
        if not template:
            template = self._get_default_template(template_type, format)
        
        return template
    
    def _load_template(self, template_key: str) -> Optional[Dict[str, Any]]:
        """Load template from file"""
        template_path = self.templates_dir / f"{template_key}.json"
        if template_path.exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load template {template_key}: {e}")
        return None
    
    def _create_default_templates(self):
        """Create default template configurations"""
        
        # Business Leader Templates
        self._create_business_leader_templates()
        
        # Policymaker Templates
        self._create_policymaker_templates()
        
        # Researcher Templates
        self._create_researcher_templates()
        
        # General Templates
        self._create_general_templates()
    
    def _create_business_leader_templates(self):
        """Create business leader specific templates"""
        
        # PDF Report Template
        business_pdf_template = {
            "template_type": "pdf_report",
            "persona": "business_leader",
            "title": "AI Adoption ROI Analysis",
            "subtitle": "Executive Business Intelligence Report",
            "sections": [
                {
                    "name": "executive_summary",
                    "title": "Executive Summary",
                    "priority": 1,
                    "content_focus": "roi_business_impact"
                },
                {
                    "name": "competitive_analysis",
                    "title": "Competitive Position Assessment",
                    "priority": 2,
                    "content_focus": "market_positioning"
                },
                {
                    "name": "roi_analysis",
                    "title": "Return on Investment Analysis",
                    "priority": 3,
                    "content_focus": "financial_metrics"
                },
                {
                    "name": "implementation_roadmap",
                    "title": "Implementation Strategy",
                    "priority": 4,
                    "content_focus": "strategic_planning"
                },
                {
                    "name": "risk_assessment",
                    "title": "Risk Assessment & Mitigation",
                    "priority": 5,
                    "content_focus": "risk_management"
                }
            ],
            "styling": {
                "primary_color": "#1f4e79",
                "secondary_color": "#2e75b6",
                "accent_color": "#70ad47",
                "font_family": "Arial",
                "executive_focus": True
            },
            "charts": [
                "roi_scenarios",
                "competitive_positioning",
                "investment_timeline",
                "market_share_analysis"
            ],
            "key_metrics": [
                "total_roi",
                "payback_period",
                "npv",
                "competitive_advantage_score"
            ]
        }
        
        self._save_template("pdf_report_business_leader_general", business_pdf_template)
        
        # PowerPoint Template
        business_ppt_template = {
            "template_type": "powerpoint",
            "persona": "business_leader",
            "slide_layouts": [
                {
                    "type": "title_slide",
                    "title": "AI Adoption Strategy",
                    "subtitle": "ROI Analysis & Competitive Positioning"
                },
                {
                    "type": "executive_summary",
                    "title": "Executive Summary",
                    "bullets": 5,
                    "focus": "business_value"
                },
                {
                    "type": "roi_analysis",
                    "title": "ROI Analysis",
                    "chart_type": "bar_chart",
                    "data_focus": "financial_metrics"
                },
                {
                    "type": "competitive_matrix",
                    "title": "Competitive Position",
                    "chart_type": "scatter_plot",
                    "axes": ["adoption_rate", "market_share"]
                },
                {
                    "type": "recommendations",
                    "title": "Strategic Recommendations",
                    "bullets": 5,
                    "action_oriented": True
                }
            ],
            "branding": {
                "logo_position": "top_right",
                "color_scheme": "professional_blue",
                "font_sizes": {
                    "title": 32,
                    "subtitle": 18,
                    "content": 16,
                    "footnote": 12
                }
            }
        }
        
        self._save_template("powerpoint_business_leader_general", business_ppt_template)
    
    def _create_policymaker_templates(self):
        """Create policymaker specific templates"""
        
        # PDF Report Template
        policy_pdf_template = {
            "template_type": "pdf_report",
            "persona": "policymaker",
            "title": "AI Adoption Policy Impact Analysis",
            "subtitle": "Regulatory and Economic Implications Report",
            "sections": [
                {
                    "name": "policy_summary",
                    "title": "Policy Summary",
                    "priority": 1,
                    "content_focus": "regulatory_landscape"
                },
                {
                    "name": "labor_impact",
                    "title": "Labor Market Impact Analysis",
                    "priority": 2,
                    "content_focus": "workforce_implications"
                },
                {
                    "name": "geographic_analysis",
                    "title": "Geographic Distribution & Disparities",
                    "priority": 3,
                    "content_focus": "regional_patterns"
                },
                {
                    "name": "regulatory_recommendations",
                    "title": "Regulatory Framework Recommendations",
                    "priority": 4,
                    "content_focus": "policy_guidance"
                },
                {
                    "name": "economic_impact",
                    "title": "Macroeconomic Impact Assessment",
                    "priority": 5,
                    "content_focus": "economic_analysis"
                }
            ],
            "styling": {
                "primary_color": "#d73027",
                "secondary_color": "#fc8d59",
                "accent_color": "#91bfdb",
                "font_family": "Times New Roman",
                "formal_style": True
            },
            "charts": [
                "geographic_heatmap",
                "labor_impact_by_sector",
                "regulatory_timeline",
                "economic_indicators"
            ],
            "key_metrics": [
                "job_displacement",
                "job_creation",
                "gdp_impact",
                "geographic_gini_coefficient"
            ]
        }
        
        self._save_template("pdf_report_policymaker_general", policy_pdf_template)
    
    def _create_researcher_templates(self):
        """Create researcher specific templates"""
        
        # PDF Report Template
        research_pdf_template = {
            "template_type": "pdf_report",
            "persona": "researcher",
            "title": "AI Adoption Research Analysis",
            "subtitle": "Comprehensive Academic Research Report",
            "sections": [
                {
                    "name": "abstract",
                    "title": "Abstract",
                    "priority": 1,
                    "content_focus": "research_summary"
                },
                {
                    "name": "methodology",
                    "title": "Research Methodology",
                    "priority": 2,
                    "content_focus": "scientific_approach"
                },
                {
                    "name": "literature_review",
                    "title": "Literature Review",
                    "priority": 3,
                    "content_focus": "academic_context"
                },
                {
                    "name": "findings",
                    "title": "Research Findings",
                    "priority": 4,
                    "content_focus": "empirical_results"
                },
                {
                    "name": "discussion",
                    "title": "Discussion & Implications",
                    "priority": 5,
                    "content_focus": "analysis_interpretation"
                },
                {
                    "name": "future_research",
                    "title": "Future Research Directions",
                    "priority": 6,
                    "content_focus": "research_opportunities"
                },
                {
                    "name": "references",
                    "title": "References",
                    "priority": 7,
                    "content_focus": "citations"
                }
            ],
            "styling": {
                "primary_color": "#2166ac",
                "secondary_color": "#5aae61",
                "accent_color": "#f7f7f7",
                "font_family": "Times New Roman",
                "academic_style": True,
                "citation_style": "apa"
            },
            "charts": [
                "trend_analysis",
                "correlation_matrix",
                "regression_analysis",
                "statistical_distributions"
            ],
            "key_metrics": [
                "correlation_coefficients",
                "confidence_intervals",
                "p_values",
                "effect_sizes"
            ]
        }
        
        self._save_template("pdf_report_researcher_general", research_pdf_template)
    
    def _create_general_templates(self):
        """Create general purpose templates"""
        
        # General PDF Template
        general_pdf_template = {
            "template_type": "pdf_report",
            "persona": "general",
            "title": "AI Adoption Dashboard Report",
            "subtitle": "Comprehensive Analysis and Insights",
            "sections": [
                {
                    "name": "overview",
                    "title": "Market Overview",
                    "priority": 1,
                    "content_focus": "general_trends"
                },
                {
                    "name": "key_findings",
                    "title": "Key Findings",
                    "priority": 2,
                    "content_focus": "main_insights"
                },
                {
                    "name": "analysis",
                    "title": "Detailed Analysis",
                    "priority": 3,
                    "content_focus": "comprehensive_review"
                },
                {
                    "name": "recommendations",
                    "title": "Recommendations",
                    "priority": 4,
                    "content_focus": "actionable_guidance"
                }
            ],
            "styling": {
                "primary_color": "#1f77b4",
                "secondary_color": "#ff7f0e",
                "accent_color": "#2ca02c",
                "font_family": "Arial",
                "balanced_design": True
            },
            "charts": [
                "historical_trends",
                "geographic_distribution",
                "sector_analysis",
                "future_projections"
            ],
            "key_metrics": [
                "overall_adoption",
                "growth_rate",
                "market_penetration",
                "regional_variance"
            ]
        }
        
        self._save_template("pdf_report_general_general", general_pdf_template)
        
        # Excel Template
        excel_template = {
            "template_type": "excel",
            "persona": "general",
            "worksheets": [
                {
                    "name": "Dashboard",
                    "type": "summary",
                    "layout": "executive_overview"
                },
                {
                    "name": "Historical_Data",
                    "type": "data_table",
                    "source": "historical_trends"
                },
                {
                    "name": "Geographic_Data",
                    "type": "data_table",
                    "source": "geographic_distribution"
                },
                {
                    "name": "Analysis",
                    "type": "calculations",
                    "formulas": True
                },
                {
                    "name": "Charts",
                    "type": "visualizations",
                    "chart_types": ["line", "bar", "pie"]
                },
                {
                    "name": "Metadata",
                    "type": "documentation",
                    "content": "data_sources_methodology"
                }
            ],
            "styling": {
                "header_color": "#1f77b4",
                "accent_color": "#ff7f0e",
                "table_style": "medium2",
                "conditional_formatting": True
            }
        }
        
        self._save_template("excel_general_general", excel_template)
        
        # HTML Template
        html_template = {
            "template_type": "html",
            "persona": "general",
            "layout": {
                "header": {
                    "include_logo": True,
                    "navigation": True,
                    "breadcrumbs": False
                },
                "content": {
                    "sidebar": True,
                    "main_content": "responsive_grid",
                    "chart_layout": "interactive"
                },
                "footer": {
                    "include_metadata": True,
                    "social_links": False
                }
            },
            "styling": {
                "theme": "professional",
                "color_scheme": "blue_gradient",
                "typography": "sans_serif",
                "responsive_breakpoints": [768, 1024, 1200]
            },
            "interactivity": {
                "chart_hover": True,
                "data_filters": True,
                "export_buttons": True,
                "print_optimization": True
            }
        }
        
        self._save_template("html_general_general", html_template)
    
    def _save_template(self, template_key: str, template_data: Dict[str, Any]):
        """Save template to file"""
        template_path = self.templates_dir / f"{template_key}.json"
        try:
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save template {template_key}: {e}")
    
    def _get_default_template(self, template_type: str, format: str) -> Dict[str, Any]:
        """Get basic default template"""
        return {
            "template_type": template_type,
            "persona": "general",
            "format": format,
            "title": "AI Adoption Dashboard",
            "subtitle": "Data Analysis Report",
            "styling": {
                "primary_color": "#1f77b4",
                "secondary_color": "#ff7f0e",
                "accent_color": "#2ca02c",
                "font_family": "Arial"
            },
            "sections": [
                {"name": "overview", "title": "Overview", "priority": 1},
                {"name": "analysis", "title": "Analysis", "priority": 2},
                {"name": "recommendations", "title": "Recommendations", "priority": 3}
            ]
        }
    
    def get_persona_insights(self, persona: str) -> List[str]:
        """Get persona-specific insights"""
        insights = {
            "Business Leader": [
                "ROI opportunities demonstrate clear value creation potential",
                "Competitive advantages accrue to early AI adopters",
                "Skills gap represents primary implementation barrier",
                "Phased deployment approach minimizes implementation risks",
                "Data quality critical for AI success and ROI realization"
            ],
            "Policymaker": [
                "Geographic disparities require targeted policy interventions",
                "Labor market impacts need proactive workforce transition support",
                "Regulatory frameworks require modernization for AI governance",
                "International competitiveness depends on national AI strategies",
                "Public-private partnerships essential for inclusive AI growth"
            ],
            "Researcher": [
                "Adoption patterns follow established technology lifecycle models",
                "Organizational factors more predictive than technical capabilities",
                "Network effects drive cluster-based adoption patterns",
                "Long-term productivity impacts require longitudinal studies",
                "Multi-dimensional measurement frameworks needed for assessment"
            ]
        }
        return insights.get(persona, [
            "AI adoption accelerating across all measured sectors",
            "Strategic implementation approaches determine success outcomes",
            "Skills development critical for realizing AI benefits",
            "Cross-sector collaboration drives best practices"
        ])
    
    def get_persona_recommendations(self, persona: str) -> List[str]:
        """Get persona-specific recommendations"""
        recommendations = {
            "Business Leader": [
                "Prioritize high-impact use cases with measurable ROI",
                "Invest in data infrastructure and governance capabilities",
                "Develop AI talent through strategic hiring and upskilling",
                "Implement phased deployment with continuous learning cycles",
                "Build strategic partnerships for technology and expertise access"
            ],
            "Policymaker": [
                "Develop national AI strategies with clear implementation roadmaps",
                "Invest in workforce transition and reskilling programs",
                "Update regulatory frameworks for AI governance and ethics",
                "Foster public-private partnerships for inclusive growth",
                "Strengthen international cooperation on AI standards"
            ],
            "Researcher": [
                "Conduct longitudinal studies on AI adoption patterns",
                "Develop standardized metrics for AI impact measurement",
                "Investigate organizational success factors in AI implementation",
                "Study human-AI collaboration models and effectiveness",
                "Research ethical implications and societal impacts"
            ]
        }
        return recommendations.get(persona, [
            "Develop comprehensive AI strategies aligned with goals",
            "Invest in foundational capabilities: data, talent, governance",
            "Implement pilot programs to validate approaches",
            "Build cross-functional teams for AI initiatives"
        ])
    
    def get_chart_preferences(self, persona: str) -> Dict[str, Any]:
        """Get persona-specific chart preferences"""
        preferences = {
            "Business Leader": {
                "primary_charts": ["roi_analysis", "competitive_positioning", "investment_timeline"],
                "chart_style": "executive",
                "color_emphasis": "financial_performance",
                "annotations": "business_insights"
            },
            "Policymaker": {
                "primary_charts": ["geographic_distribution", "labor_impact", "regulatory_timeline"],
                "chart_style": "formal",
                "color_emphasis": "geographic_regions",
                "annotations": "policy_implications"
            },
            "Researcher": {
                "primary_charts": ["trend_analysis", "correlation_analysis", "statistical_distribution"],
                "chart_style": "academic",
                "color_emphasis": "data_categories",
                "annotations": "statistical_significance"
            }
        }
        return preferences.get(persona, {
            "primary_charts": ["historical_trends", "geographic_distribution", "sector_analysis"],
            "chart_style": "balanced",
            "color_emphasis": "categories",
            "annotations": "general_insights"
        })
    
    def customize_template(self, base_template: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customizations to a base template"""
        import copy
        customized_template = copy.deepcopy(base_template)
        
        # Apply nested customizations
        for key, value in customizations.items():
            if key in customized_template and isinstance(customized_template[key], dict) and isinstance(value, dict):
                customized_template[key].update(value)
            else:
                customized_template[key] = value
        
        return customized_template
    
    def validate_template(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Validate template configuration"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        required_fields = ["template_type", "persona", "styling"]
        for field in required_fields:
            if field not in template:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False
        
        # Validate styling
        if "styling" in template:
            styling = template["styling"]
            color_fields = ["primary_color", "secondary_color"]
            for color_field in color_fields:
                if color_field in styling:
                    color_value = styling[color_field]
                    if not self._is_valid_color(color_value):
                        validation_result["warnings"].append(f"Invalid color format: {color_field} = {color_value}")
        
        # Validate sections if present
        if "sections" in template:
            sections = template["sections"]
            if not isinstance(sections, list):
                validation_result["errors"].append("Sections must be a list")
                validation_result["valid"] = False
            else:
                for i, section in enumerate(sections):
                    if not isinstance(section, dict) or "name" not in section:
                        validation_result["warnings"].append(f"Section {i} missing required 'name' field")
        
        return validation_result
    
    def _is_valid_color(self, color: str) -> bool:
        """Validate color format (hex, rgb, named)"""
        import re
        
        # Check hex format
        if re.match(r'^#[0-9A-Fa-f]{6}$', color):
            return True
        
        # Check rgb format
        if re.match(r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$', color):
            return True
        
        # Check named colors (basic validation)
        named_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'black', 'white', 'gray']
        if color.lower() in named_colors:
            return True
        
        return False
    
    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get list of available templates by type"""
        templates = {}
        
        for template_file in self.templates_dir.glob("*.json"):
            parts = template_file.stem.split("_")
            if len(parts) >= 2:
                template_type = parts[0]
                if template_type not in templates:
                    templates[template_type] = []
                templates[template_type].append(template_file.stem)
        
        return templates
    
    def create_custom_template(self, template_config: Dict[str, Any]) -> str:
        """Create and save a custom template"""
        # Generate template key
        template_type = template_config.get("template_type", "custom")
        persona = template_config.get("persona", "general")
        format_type = template_config.get("format", "general")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        template_key = f"{template_type}_{persona}_{format_type}_{timestamp}"
        
        # Validate template
        validation = self.validate_template(template_config)
        if not validation["valid"]:
            raise ValueError(f"Invalid template configuration: {validation['errors']}")
        
        # Save template
        self._save_template(template_key, template_config)
        
        logger.info(f"Created custom template: {template_key}")
        return template_key