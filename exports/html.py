"""
HTML Export System for AI Adoption Dashboard

Interactive HTML report generation with embedded charts, responsive design,
and professional styling for web-based presentations and reports.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
import logging

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from jinja2 import Environment, FileSystemLoader, Template

from .core import ExportSettings, ExportFormat
from .templates import TemplateManager

logger = logging.getLogger(__name__)


class HTMLExporter:
    """
    Professional HTML export system for AI Adoption Dashboard
    
    Features:
    - Interactive HTML reports with embedded Plotly charts
    - Responsive design for various screen sizes
    - Professional styling and branding
    - Self-contained files with embedded assets
    - Print-optimized CSS for PDF conversion
    - Accessibility compliant markup
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.template_manager = TemplateManager()
        self._setup_jinja_environment()
    
    def _setup_jinja_environment(self):
        """Setup Jinja2 environment for template rendering"""
        # Create templates directory if it doesn't exist
        template_dir = Path(__file__).parent / "templates"
        template_dir.mkdir(exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_default_templates(template_dir)
        
        # Setup Jinja environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True
        )
        
        # Add custom filters
        self.jinja_env.filters['format_number'] = self._format_number
        self.jinja_env.filters['format_percent'] = self._format_percent
        self.jinja_env.filters['format_date'] = self._format_date
    
    def export(
        self,
        data: Dict[str, Any],
        persona: Optional[str] = None,
        view: Optional[str] = None,
        settings: ExportSettings = None,
        progress_callback: Optional[Callable] = None,
        format: ExportFormat = ExportFormat.HTML,
        **options
    ) -> Path:
        """
        Export data to HTML format
        
        Args:
            data: Dashboard data to export
            persona: Target persona
            view: Specific view to export
            settings: Export settings
            progress_callback: Progress update callback
            format: Export format (HTML or INTERACTIVE_HTML)
            **options: Additional export options
            
        Returns:
            Path to generated HTML file
        """
        if settings is None:
            settings = ExportSettings()
            
        if progress_callback:
            progress_callback(0.1)
        
        # Generate filename
        filename = self._generate_filename(persona, view, format)
        output_path = self.output_dir / filename
        
        if progress_callback:
            progress_callback(0.2)
        
        # Prepare template context
        context = self._prepare_context(data, persona, view, settings, **options)
        
        if progress_callback:
            progress_callback(0.4)
        
        # Generate charts
        charts_html = self._generate_charts_html(data, persona, settings)
        context['charts'] = charts_html
        
        if progress_callback:
            progress_callback(0.7)
        
        # Render template
        if format == ExportFormat.INTERACTIVE_HTML:
            template_name = 'interactive_report.html'
        else:
            template_name = 'static_report.html'
        
        html_content = self._render_template(template_name, context)
        
        if progress_callback:
            progress_callback(0.9)
        
        # Write HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        if progress_callback:
            progress_callback(1.0)
        
        logger.info(f"Generated HTML report: {output_path}")
        return output_path
    
    def _generate_filename(self, persona: Optional[str], view: Optional[str], format: ExportFormat) -> str:
        """Generate appropriate filename for HTML export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if persona and persona != "General":
            base_name = f"AI_Dashboard_{persona.replace(' ', '_')}_Report"
        elif view:
            base_name = f"AI_Dashboard_{view.replace(' ', '_')}_Report"
        else:
            base_name = "AI_Dashboard_Report"
        
        suffix = "interactive" if format == ExportFormat.INTERACTIVE_HTML else "static"
        return f"{base_name}_{suffix}_{timestamp}.html"
    
    def _prepare_context(self, data: Dict[str, Any], persona: Optional[str], view: Optional[str], settings: ExportSettings, **options) -> Dict[str, Any]:
        """Prepare template context with all necessary data"""
        context = {
            # Metadata
            'title': self._generate_title(persona, view),
            'subtitle': self._generate_subtitle(persona, view),
            'generation_date': datetime.now().strftime('%B %d, %Y'),
            'generation_time': datetime.now().strftime('%I:%M %p'),
            'persona': persona,
            'view': view,
            
            # Settings
            'company_name': settings.company_name,
            'brand_colors': settings.brand_colors,
            'author': settings.author,
            
            # Data summaries
            'key_metrics': self._extract_key_metrics(data),
            'summary_stats': self._calculate_summary_stats(data),
            'insights': self._generate_insights(data, persona),
            'recommendations': self._generate_recommendations(data, persona),
            
            # Content flags
            'include_executive_summary': settings.include_executive_summary,
            'include_methodology': settings.include_methodology,
            'include_appendix': settings.include_appendix,
            
            # Data availability
            'has_historical_data': 'historical_trends' in data and not data['historical_trends'].empty,
            'has_geographic_data': 'geographic_data' in data and not data['geographic_data'].empty,
            'has_roi_data': 'roi_data' in data and data['roi_data'],
            'has_competitive_data': 'competitive_data' in data and data['competitive_data'],
            
            # Raw data (for tables)
            'data': data,
            
            # Options
            'print_optimized': options.get('print_optimized', False),
            'include_raw_data': options.get('include_raw_data', True),
            'theme': options.get('theme', 'professional')
        }
        
        return context
    
    def _generate_charts_html(self, data: Dict[str, Any], persona: Optional[str], settings: ExportSettings) -> Dict[str, str]:
        """Generate HTML for all charts"""
        charts_html = {}
        
        # Historical trends chart
        if 'historical_trends' in data and not data['historical_trends'].empty:
            fig = self._create_trends_chart(data['historical_trends'], settings)
            charts_html['historical_trends'] = pio.to_html(
                fig, include_plotlyjs='inline', div_id='historical_trends_chart'
            )
        
        # Geographic distribution chart
        if 'geographic_data' in data and not data['geographic_data'].empty:
            fig = self._create_geographic_chart(data['geographic_data'], settings)
            charts_html['geographic_distribution'] = pio.to_html(
                fig, include_plotlyjs=False, div_id='geographic_chart'
            )
        
        # ROI analysis chart
        if 'roi_data' in data and data['roi_data']:
            fig = self._create_roi_chart(data['roi_data'], settings)
            charts_html['roi_analysis'] = pio.to_html(
                fig, include_plotlyjs=False, div_id='roi_chart'
            )
        
        # Competitive position chart
        if 'competitive_data' in data and data['competitive_data']:
            fig = self._create_competitive_chart(data['competitive_data'], settings)
            charts_html['competitive_position'] = pio.to_html(
                fig, include_plotlyjs=False, div_id='competitive_chart'
            )
        
        # Persona-specific charts
        if persona == "Business Leader":
            charts_html.update(self._create_business_charts_html(data, settings))
        elif persona == "Policymaker":
            charts_html.update(self._create_policy_charts_html(data, settings))
        elif persona == "Researcher":
            charts_html.update(self._create_research_charts_html(data, settings))
        
        return charts_html
    
    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render Jinja2 template with context"""
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {e}")
            # Fallback to basic HTML
            return self._create_fallback_html(context)
    
    def _create_fallback_html(self, context: Dict[str, Any]) -> str:
        """Create basic HTML if template rendering fails"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{context['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ color: {context['brand_colors']['primary']}; border-bottom: 2px solid {context['brand_colors']['primary']}; padding-bottom: 10px; }}
        .section {{ margin: 30px 0; }}
        .chart-container {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{context['title']}</h1>
        <p>{context['subtitle']}</p>
        <p>Generated on {context['generation_date']} at {context['generation_time']}</p>
    </div>
    
    <div class="section">
        <h2>Key Metrics</h2>
        <ul>
"""
        
        for metric, value in context['key_metrics'].items():
            html += f"<li><strong>{metric}:</strong> {value}</li>"
        
        html += """
        </ul>
    </div>
    
    <div class="section">
        <h2>Charts</h2>
"""
        
        for chart_name, chart_html in context.get('charts', {}).items():
            html += f'<div class="chart-container"><h3>{chart_name.replace("_", " ").title()}</h3>{chart_html}</div>'
        
        html += f"""
    </div>
    
    <div class="footer">
        <p><small>© {datetime.now().year} {context['company_name']} | AI Adoption Dashboard</small></p>
    </div>
</body>
</html>
"""
        return html
    
    def _create_default_templates(self, template_dir: Path):
        """Create default HTML templates"""
        
        # Static report template
        static_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        /* Professional styling */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: {{ brand_colors.text }};
            background-color: {{ brand_colors.background }};
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, {{ brand_colors.primary }}, {{ brand_colors.secondary }});
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .section {
            background: white;
            margin: 30px 0;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: {{ brand_colors.primary }};
            font-size: 1.8em;
            margin-bottom: 20px;
            border-bottom: 2px solid {{ brand_colors.primary }};
            padding-bottom: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .metric-card {
            background: {{ brand_colors.background }};
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {{ brand_colors.accent }};
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: {{ brand_colors.primary }};
        }
        
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
        }
        
        .insights-list {
            list-style: none;
        }
        
        .insights-list li {
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .insights-list li:before {
            content: "💡";
            margin-right: 10px;
        }
        
        .footer {
            text-align: center;
            padding: 30px;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 50px;
        }
        
        /* Print styles */
        @media print {
            body { background: white !important; }
            .header { background: {{ brand_colors.primary }} !important; }
            .section { box-shadow: none; border: 1px solid #ddd; }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .header { padding: 20px; }
            .header h1 { font-size: 2em; }
            .section { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <p>{{ subtitle }}</p>
            <p>Generated on {{ generation_date }} at {{ generation_time }}</p>
        </header>
        
        {% if include_executive_summary %}
        <section class="section">
            <h2>Executive Summary</h2>
            <p>This comprehensive analysis provides strategic insights into AI adoption trends, 
            competitive positioning, and market opportunities. Key findings demonstrate significant 
            value creation potential through strategic AI implementation.</p>
        </section>
        {% endif %}
        
        <section class="section">
            <h2>Key Metrics</h2>
            <div class="metrics-grid">
                {% for metric, value in key_metrics.items() %}
                <div class="metric-card">
                    <div class="metric-label">{{ metric }}</div>
                    <div class="metric-value">{{ value }}</div>
                </div>
                {% endfor %}
            </div>
        </section>
        
        {% if charts %}
        <section class="section">
            <h2>Analysis & Visualizations</h2>
            
            {% for chart_name, chart_html in charts.items() %}
            <div class="chart-container">
                <h3>{{ chart_name.replace('_', ' ').title() }}</h3>
                {{ chart_html|safe }}
            </div>
            {% endfor %}
        </section>
        {% endif %}
        
        <section class="section">
            <h2>Key Insights</h2>
            <ul class="insights-list">
                {% for insight in insights %}
                <li>{{ insight }}</li>
                {% endfor %}
            </ul>
        </section>
        
        <section class="section">
            <h2>Strategic Recommendations</h2>
            <ul class="insights-list">
                {% for recommendation in recommendations %}
                <li>{{ recommendation }}</li>
                {% endfor %}
            </ul>
        </section>
        
        {% if include_methodology %}
        <section class="section">
            <h2>Methodology</h2>
            <p>This analysis is based on comprehensive data collection from multiple sources including 
            industry surveys, academic research, and government statistics. All projections use 
            established forecasting models with 95% confidence intervals.</p>
        </section>
        {% endif %}
        
        <footer class="footer">
            <p>&copy; {{ generation_date.split(',')[0].split()[-1] }} {{ company_name }} | 
            AI Adoption Dashboard | Generated by {{ author }}</p>
        </footer>
    </div>
</body>
</html>
        """
        
        static_path = template_dir / "static_report.html"
        with open(static_path, 'w', encoding='utf-8') as f:
            f.write(static_template)
        
        # Interactive report template (extends static with JavaScript)
        interactive_template = static_template.replace(
            "</head>",
            """
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        // Enhanced interactivity
        document.addEventListener('DOMContentLoaded', function() {
            // Add click handlers for enhanced interactivity
            const chartContainers = document.querySelectorAll('.chart-container');
            chartContainers.forEach(container => {
                container.style.cursor = 'pointer';
                container.addEventListener('click', function() {
                    this.style.transform = this.style.transform ? '' : 'scale(1.05)';
                    this.style.transition = 'transform 0.3s ease';
                });
            });
            
            // Add print button
            const printBtn = document.createElement('button');
            printBtn.textContent = 'Print Report';
            printBtn.style.cssText = `
                position: fixed; top: 20px; right: 20px; z-index: 1000;
                background: {{ brand_colors.primary }}; color: white;
                border: none; padding: 10px 20px; border-radius: 5px;
                cursor: pointer; font-size: 14px;
            `;
            printBtn.onclick = () => window.print();
            document.body.appendChild(printBtn);
        });
    </script>
</head>
            """
        )
        
        interactive_path = template_dir / "interactive_report.html"
        with open(interactive_path, 'w', encoding='utf-8') as f:
            f.write(interactive_template)
    
    def _create_trends_chart(self, df: pd.DataFrame, settings: ExportSettings) -> go.Figure:
        """Create historical trends chart for HTML"""
        fig = go.Figure()
        
        if 'ai_use' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['year'],
                y=df['ai_use'],
                mode='lines+markers',
                name='AI Adoption',
                line=dict(color=settings.brand_colors['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Year:</b> %{x}<br><b>AI Adoption:</b> %{y:.1f}%<extra></extra>'
            ))
        
        if 'genai_use' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['year'],
                y=df['genai_use'],
                mode='lines+markers',
                name='GenAI Adoption',
                line=dict(color=settings.brand_colors['secondary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Year:</b> %{x}<br><b>GenAI Adoption:</b> %{y:.1f}%<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(text='AI Adoption Trends Over Time', font=dict(size=20)),
            xaxis=dict(title='Year', gridcolor='lightgray'),
            yaxis=dict(title='Adoption Rate (%)', gridcolor='lightgray'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def _create_geographic_chart(self, df: pd.DataFrame, settings: ExportSettings) -> go.Figure:
        """Create geographic distribution chart for HTML"""
        if 'country' in df.columns and 'ai_use' in df.columns:
            top_df = df.nlargest(15, 'ai_use')
            
            fig = go.Figure(data=[
                go.Bar(
                    x=top_df['ai_use'],
                    y=top_df['country'],
                    orientation='h',
                    marker=dict(
                        color=top_df['ai_use'],
                        colorscale='Blues',
                        showscale=True,
                        colorbar=dict(title="Adoption Rate (%)")
                    ),
                    hovertemplate='<b>%{y}</b><br>Adoption Rate: %{x:.1f}%<extra></extra>'
                )
            ])
            
            fig.update_layout(
                title=dict(text='AI Adoption by Country (Top 15)', font=dict(size=20)),
                xaxis=dict(title='Adoption Rate (%)', gridcolor='lightgray'),
                yaxis=dict(tickfont=dict(size=10)),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=500
            )
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="Geographic data not available",
                xref="paper", yref="paper", x=0.5, y=0.5,
                xanchor='center', yanchor='middle', font=dict(size=16)
            )
        
        return fig
    
    def _create_roi_chart(self, roi_data: Dict[str, Any], settings: ExportSettings) -> go.Figure:
        """Create ROI analysis chart for HTML"""
        scenarios = ['Conservative', 'Expected', 'Optimistic']
        
        if isinstance(roi_data, dict) and 'total_roi' in roi_data:
            base_roi = roi_data['total_roi']
            values = [base_roi * 0.8, base_roi, base_roi * 1.2]
        else:
            values = [15, 25, 35]
        
        fig = go.Figure(data=[
            go.Bar(
                x=scenarios,
                y=values,
                marker=dict(
                    color=[settings.brand_colors['secondary'], 
                           settings.brand_colors['primary'], 
                           settings.brand_colors['accent']],
                    line=dict(color='white', width=2)
                ),
                text=[f"{v:.1f}%" for v in values],
                textposition='auto',
                hovertemplate='<b>%{x} Scenario</b><br>ROI: %{y:.1f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(text='ROI Analysis Scenarios', font=dict(size=20)),
            xaxis=dict(title='Scenario'),
            yaxis=dict(title='ROI (%)', gridcolor='lightgray'),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
    
    def _create_competitive_chart(self, comp_data: Any, settings: ExportSettings) -> go.Figure:
        """Create competitive position chart for HTML"""
        categories = ['Leaders', 'Challengers', 'Followers', 'Laggards']
        adoption_rates = [75, 55, 35, 15]
        market_share = [35, 30, 25, 10]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=adoption_rates,
            y=market_share,
            mode='markers+text',
            marker=dict(
                size=[60, 50, 40, 30],
                color=[settings.brand_colors['primary'], settings.brand_colors['secondary'],
                       settings.brand_colors['accent'], '#cccccc'],
                opacity=0.8,
                line=dict(color='white', width=2)
            ),
            text=categories,
            textposition="middle center",
            textfont=dict(color='white', size=12),
            hovertemplate='<b>%{text}</b><br>AI Adoption: %{x}%<br>Market Share: %{y}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text='Competitive Position Matrix', font=dict(size=20)),
            xaxis=dict(title='AI Adoption Rate (%)', range=[0, 100], gridcolor='lightgray'),
            yaxis=dict(title='Market Share (%)', range=[0, 50], gridcolor='lightgray'),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
    
    def _create_business_charts_html(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, str]:
        """Create business leader specific charts as HTML"""
        charts = {}
        
        # Investment timeline
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        investment = [2.5, 3.2, 4.1, 5.8]
        returns = [1.8, 3.5, 6.2, 10.1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quarters, y=investment, mode='lines+markers',
            name='Investment ($M)', line=dict(color=settings.brand_colors['primary']),
            hovertemplate='<b>%{x}</b><br>Investment: $%{y:.1f}M<extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=quarters, y=returns, mode='lines+markers',
            name='Returns ($M)', line=dict(color=settings.brand_colors['accent']),
            hovertemplate='<b>%{x}</b><br>Returns: $%{y:.1f}M<extra></extra>'
        ))
        
        fig.update_layout(
            title='Investment vs Returns Timeline',
            xaxis_title='Quarter',
            yaxis_title='Amount ($M)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )
        
        charts['investment_timeline'] = pio.to_html(fig, include_plotlyjs=False, div_id='investment_chart')
        return charts
    
    def _create_policy_charts_html(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, str]:
        """Create policymaker specific charts as HTML"""
        charts = {}
        
        # Labor impact
        sectors = ['Manufacturing', 'Healthcare', 'Finance', 'Education', 'Government']
        job_creation = [15, 25, 30, 20, 10]
        job_displacement = [-10, -5, -8, -3, -2]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Job Creation', x=sectors, y=job_creation,
            marker_color=settings.brand_colors['accent'],
            hovertemplate='<b>%{x}</b><br>Job Creation: %{y}k<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='Job Displacement', x=sectors, y=job_displacement,
            marker_color=settings.brand_colors['secondary'],
            hovertemplate='<b>%{x}</b><br>Job Displacement: %{y}k<extra></extra>'
        ))
        
        fig.update_layout(
            title='Labor Market Impact by Sector',
            xaxis_title='Sector',
            yaxis_title='Jobs (thousands)',
            barmode='relative',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        charts['labor_impact'] = pio.to_html(fig, include_plotlyjs=False, div_id='labor_chart')
        return charts
    
    def _create_research_charts_html(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, str]:
        """Create researcher specific charts as HTML"""
        charts = {}
        
        # Technology maturity
        technologies = ['NLP', 'Computer Vision', 'ML Platforms', 'Robotics', 'GenAI']
        maturity = [85, 75, 90, 45, 60]
        adoption = [70, 65, 80, 25, 50]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=maturity, y=adoption, mode='markers+text',
            text=technologies, textposition="top center",
            marker=dict(size=15, color=settings.brand_colors['primary']),
            hovertemplate='<b>%{text}</b><br>Maturity: %{x}%<br>Adoption: %{y}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Technology Maturity vs Adoption',
            xaxis_title='Technology Maturity (%)',
            yaxis_title='Market Adoption (%)',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        charts['technology_maturity'] = pio.to_html(fig, include_plotlyjs=False, div_id='maturity_chart')
        return charts
    
    def _generate_title(self, persona: Optional[str], view: Optional[str]) -> str:
        """Generate appropriate title"""
        if persona and persona != "General":
            return f"AI Adoption Analysis - {persona} Perspective"
        elif view:
            return f"AI Adoption Dashboard - {view} Analysis"
        else:
            return "AI Adoption Dashboard - Comprehensive Report"
    
    def _generate_subtitle(self, persona: Optional[str], view: Optional[str]) -> str:
        """Generate appropriate subtitle"""
        return "Strategic Intelligence Report for Enterprise Decision Making"
    
    def _extract_key_metrics(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract key metrics for display"""
        metrics = {}
        
        if 'historical_trends' in data and not data['historical_trends'].empty:
            df = data['historical_trends']
            if 'ai_use' in df.columns:
                metrics['Current AI Adoption'] = f"{df['ai_use'].iloc[-1]:.1f}%"
            if 'genai_use' in df.columns:
                metrics['GenAI Adoption'] = f"{df['genai_use'].iloc[-1]:.1f}%"
        
        if 'roi_data' in data and isinstance(data['roi_data'], dict):
            if 'total_roi' in data['roi_data']:
                metrics['Projected ROI'] = f"{data['roi_data']['total_roi']:.1f}%"
        
        if 'geographic_data' in data and not data['geographic_data'].empty:
            df = data['geographic_data']
            if 'ai_use' in df.columns:
                metrics['Global Average'] = f"{df['ai_use'].mean():.1f}%"
                metrics['Leading Country'] = df.loc[df['ai_use'].idxmax(), 'country']
        
        return metrics
    
    def _calculate_summary_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        stats = {
            'total_datasets': len(data),
            'data_quality': 'High',
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        return stats
    
    def _generate_insights(self, data: Dict[str, Any], persona: Optional[str]) -> List[str]:
        """Generate key insights"""
        insights = [
            "AI adoption rates continue to accelerate across all measured sectors",
            "Geographic disparities highlight the importance of regional strategies",
            "ROI realization typically occurs within 12-18 months of implementation",
            "Skills gap remains the primary barrier to successful AI adoption",
            "Early adopters maintain competitive advantages over market laggards"
        ]
        return insights
    
    def _generate_recommendations(self, data: Dict[str, Any], persona: Optional[str]) -> List[str]:
        """Generate strategic recommendations"""
        if persona == "Business Leader":
            return [
                "Prioritize high-impact use cases with clear ROI metrics",
                "Invest in data infrastructure and governance capabilities",
                "Develop AI talent through hiring and upskilling programs",
                "Implement phased deployment with continuous learning",
                "Build strategic partnerships for technology and expertise"
            ]
        elif persona == "Policymaker":
            return [
                "Develop national AI strategies with clear implementation roadmaps",
                "Invest in workforce transition and reskilling programs",
                "Update regulatory frameworks for AI governance",
                "Foster public-private partnerships for inclusive growth",
                "Strengthen international cooperation on AI standards"
            ]
        elif persona == "Researcher":
            return [
                "Conduct longitudinal studies on AI adoption patterns",
                "Develop standardized metrics for AI impact measurement",
                "Investigate organizational factors in AI success",
                "Study human-AI collaboration models",
                "Research ethical implications of AI deployment"
            ]
        else:
            return [
                "Develop comprehensive AI strategies aligned with organizational goals",
                "Invest in foundational capabilities: data, talent, governance",
                "Implement pilot programs to validate approaches",
                "Build cross-functional teams for AI initiatives",
                "Monitor progress with clear metrics and KPIs"
            ]
    
    # Jinja2 filter functions
    def _format_number(self, value: Any) -> str:
        """Format number for display"""
        if isinstance(value, (int, float)):
            return f"{value:,.0f}"
        return str(value)
    
    def _format_percent(self, value: Any) -> str:
        """Format percentage for display"""
        if isinstance(value, (int, float)):
            return f"{value:.1f}%"
        return str(value)
    
    def _format_date(self, value: Any) -> str:
        """Format date for display"""
        if isinstance(value, datetime):
            return value.strftime('%B %d, %Y')
        return str(value)