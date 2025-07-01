"""
Image Export System for AI Adoption Dashboard

High-resolution image export capabilities supporting PNG, SVG formats
with professional quality, custom branding, and batch processing.
"""

import os
import io
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Tuple, Union
from pathlib import Path
import logging

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from PIL.ImageColor import getrgb

from .core import ExportSettings, ExportFormat
from .templates import TemplateManager

logger = logging.getLogger(__name__)


class ImageExporter:
    """
    Professional image export system for AI Adoption Dashboard
    
    Features:
    - High-resolution PNG and SVG export
    - Custom branding and watermarks
    - Batch chart export
    - Professional layouts and styling
    - Multi-panel dashboards
    - Print-ready quality (300 DPI)
    """
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.template_manager = TemplateManager()
        
        # Configure Plotly for high-quality exports
        pio.kaleido.scope.default_width = 1200
        pio.kaleido.scope.default_height = 800
        pio.kaleido.scope.default_scale = 2
    
    def export(
        self,
        data: Dict[str, Any],
        persona: Optional[str] = None,
        view: Optional[str] = None,
        settings: ExportSettings = None,
        progress_callback: Optional[Callable] = None,
        format: ExportFormat = ExportFormat.PNG,
        **options
    ) -> Path:
        """
        Export dashboard content as high-resolution images
        
        Args:
            data: Dashboard data to export
            persona: Target persona
            view: Specific view to export
            settings: Export settings
            progress_callback: Progress update callback
            format: Export format (PNG, SVG)
            **options: Additional export options
            
        Returns:
            Path to generated image file or directory
        """
        if settings is None:
            settings = ExportSettings()
            
        if progress_callback:
            progress_callback(0.1)
        
        export_type = options.get('export_type', 'dashboard')  # dashboard, charts, or single
        
        if export_type == 'dashboard':
            return self._export_dashboard_image(data, persona, view, settings, format, progress_callback, **options)
        elif export_type == 'charts':
            return self._export_charts_batch(data, persona, view, settings, format, progress_callback, **options)
        else:
            return self._export_single_chart(data, view, settings, format, progress_callback, **options)
    
    def _export_dashboard_image(
        self,
        data: Dict[str, Any],
        persona: Optional[str],
        view: Optional[str],
        settings: ExportSettings,
        format: ExportFormat,
        progress_callback: Optional[Callable],
        **options
    ) -> Path:
        """Export complete dashboard as single high-resolution image"""
        
        # Generate filename
        filename = self._generate_filename(persona, view, format, 'dashboard')
        output_path = self.output_dir / filename
        
        if progress_callback:
            progress_callback(0.2)
        
        # Create dashboard layout
        if format == ExportFormat.SVG:
            return self._create_svg_dashboard(data, persona, output_path, settings, **options)
        else:
            return self._create_png_dashboard(data, persona, output_path, settings, progress_callback, **options)
    
    def _create_png_dashboard(
        self,
        data: Dict[str, Any],
        persona: Optional[str],
        output_path: Path,
        settings: ExportSettings,
        progress_callback: Optional[Callable],
        **options
    ) -> Path:
        """Create high-resolution PNG dashboard"""
        
        # Dashboard dimensions (300 DPI for print quality)
        width = options.get('width', 3300)  # 11 inches at 300 DPI
        height = options.get('height', 2550)  # 8.5 inches at 300 DPI
        
        # Create base image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        if progress_callback:
            progress_callback(0.3)
        
        # Add header
        self._add_header(img, draw, persona, settings, width)
        
        if progress_callback:
            progress_callback(0.4)
        
        # Generate and add charts
        charts = self._generate_charts(data, persona, settings)
        
        if progress_callback:
            progress_callback(0.6)
        
        # Layout charts in grid
        self._layout_charts_grid(img, charts, width, height, settings)
        
        if progress_callback:
            progress_callback(0.8)
        
        # Add branding and watermarks
        self._add_branding(img, draw, settings, width, height)
        
        # Add footer
        self._add_footer(img, draw, settings, width, height)
        
        if progress_callback:
            progress_callback(0.9)
        
        # Save image
        img.save(output_path, 'PNG', dpi=(300, 300), optimize=True)
        
        if progress_callback:
            progress_callback(1.0)
        
        logger.info(f"Generated dashboard PNG: {output_path}")
        return output_path
    
    def _create_svg_dashboard(
        self,
        data: Dict[str, Any],
        persona: Optional[str],
        output_path: Path,
        settings: ExportSettings,
        **options
    ) -> Path:
        """Create scalable SVG dashboard"""
        
        # Generate charts as SVG
        charts = self._generate_charts(data, persona, settings, format='svg')
        
        # Create SVG document
        svg_content = self._create_svg_layout(charts, persona, settings, **options)
        
        # Save SVG
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        logger.info(f"Generated dashboard SVG: {output_path}")
        return output_path
    
    def _export_charts_batch(
        self,
        data: Dict[str, Any],
        persona: Optional[str],
        view: Optional[str],
        settings: ExportSettings,
        format: ExportFormat,
        progress_callback: Optional[Callable],
        **options
    ) -> Path:
        """Export all charts as separate image files"""
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = self.output_dir / f"charts_{timestamp}"
        output_dir.mkdir(exist_ok=True)
        
        if progress_callback:
            progress_callback(0.1)
        
        # Generate charts
        charts = self._generate_charts(data, persona, settings)
        
        total_charts = len(charts)
        for i, (chart_name, fig) in enumerate(charts.items()):
            # Generate filename for each chart
            chart_filename = f"{chart_name.replace(' ', '_').lower()}.{format.value}"
            chart_path = output_dir / chart_filename
            
            # Export chart
            if format == ExportFormat.SVG:
                fig.write_image(
                    str(chart_path),
                    format='svg',
                    width=settings.chart_width,
                    height=settings.chart_height
                )
            else:
                fig.write_image(
                    str(chart_path),
                    format='png',
                    width=settings.chart_width,
                    height=settings.chart_height,
                    scale=2
                )
            
            if progress_callback:
                progress_callback(0.1 + (0.8 * (i + 1) / total_charts))
        
        # Create index file
        self._create_chart_index(output_dir, charts.keys(), format)
        
        if progress_callback:
            progress_callback(1.0)
        
        logger.info(f"Generated chart batch export: {output_dir}")
        return output_dir
    
    def _export_single_chart(
        self,
        data: Dict[str, Any],
        chart_name: Optional[str],
        settings: ExportSettings,
        format: ExportFormat,
        progress_callback: Optional[Callable],
        **options
    ) -> Path:
        """Export single chart as high-resolution image"""
        
        if not chart_name:
            raise ValueError("Chart name required for single chart export")
        
        if progress_callback:
            progress_callback(0.2)
        
        # Generate chart
        fig = self._create_specific_chart(data, chart_name, settings)
        
        if progress_callback:
            progress_callback(0.6)
        
        # Generate filename
        filename = self._generate_filename(None, chart_name, format, 'chart')
        output_path = self.output_dir / filename
        
        # Export chart
        if format == ExportFormat.SVG:
            fig.write_image(
                str(output_path),
                format='svg',
                width=settings.chart_width,
                height=settings.chart_height
            )
        else:
            fig.write_image(
                str(output_path),
                format='png',
                width=settings.chart_width,
                height=settings.chart_height,
                scale=2
            )
        
        if progress_callback:
            progress_callback(1.0)
        
        logger.info(f"Generated single chart: {output_path}")
        return output_path
    
    def _generate_filename(self, persona: Optional[str], view: Optional[str], format: ExportFormat, export_type: str) -> str:
        """Generate appropriate filename for image export"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if persona and persona != "General":
            base_name = f"AI_Dashboard_{persona.replace(' ', '_')}_{export_type}"
        elif view:
            base_name = f"AI_Dashboard_{view.replace(' ', '_')}_{export_type}"
        else:
            base_name = f"AI_Dashboard_{export_type}"
        
        return f"{base_name}_{timestamp}.{format.value}"
    
    def _generate_charts(self, data: Dict[str, Any], persona: Optional[str], settings: ExportSettings, format: str = 'png') -> Dict[str, go.Figure]:
        """Generate all relevant charts for the dashboard"""
        charts = {}
        
        # Historical trends chart
        if 'historical_trends' in data and not data['historical_trends'].empty:
            charts['Historical Trends'] = self._create_trends_chart(data['historical_trends'], settings)
        
        # Geographic distribution chart
        if 'geographic_data' in data and not data['geographic_data'].empty:
            charts['Geographic Distribution'] = self._create_geographic_chart(data['geographic_data'], settings)
        
        # ROI analysis chart
        if 'roi_data' in data and data['roi_data']:
            charts['ROI Analysis'] = self._create_roi_chart(data['roi_data'], settings)
        
        # Competitive position chart
        if 'competitive_data' in data and data['competitive_data']:
            charts['Competitive Position'] = self._create_competitive_chart(data['competitive_data'], settings)
        
        # Persona-specific charts
        if persona == "Business Leader":
            charts.update(self._create_business_charts(data, settings))
        elif persona == "Policymaker":
            charts.update(self._create_policy_charts(data, settings))
        elif persona == "Researcher":
            charts.update(self._create_research_charts(data, settings))
        
        return charts
    
    def _create_trends_chart(self, df: pd.DataFrame, settings: ExportSettings) -> go.Figure:
        """Create historical trends chart"""
        fig = go.Figure()
        
        # Primary trend line
        if 'ai_use' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['year'],
                y=df['ai_use'],
                mode='lines+markers',
                name='AI Adoption',
                line=dict(color=settings.brand_colors['primary'], width=3),
                marker=dict(size=8)
            ))
        
        # Secondary trend line
        if 'genai_use' in df.columns:
            fig.add_trace(go.Scatter(
                x=df['year'],
                y=df['genai_use'],
                mode='lines+markers',
                name='GenAI Adoption',
                line=dict(color=settings.brand_colors['secondary'], width=3),
                marker=dict(size=8)
            ))
        
        # Style the chart
        fig.update_layout(
            title=dict(
                text='AI Adoption Trends Over Time',
                font=dict(size=24, color=settings.brand_colors['text']),
                x=0.5
            ),
            xaxis=dict(
                title='Year',
                titlefont=dict(size=16),
                tickfont=dict(size=14),
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Adoption Rate (%)',
                titlefont=dict(size=16),
                tickfont=dict(size=14),
                gridcolor='lightgray'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=60, r=60, t=100, b=60)
        )
        
        return fig
    
    def _create_geographic_chart(self, df: pd.DataFrame, settings: ExportSettings) -> go.Figure:
        """Create geographic distribution chart"""
        if 'country' in df.columns and 'ai_use' in df.columns:
            # Top 10 countries
            top_df = df.nlargest(10, 'ai_use')
            
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
                    )
                )
            ])
            
            fig.update_layout(
                title=dict(
                    text='AI Adoption by Country (Top 10)',
                    font=dict(size=24, color=settings.brand_colors['text']),
                    x=0.5
                ),
                xaxis=dict(
                    title='Adoption Rate (%)',
                    titlefont=dict(size=16),
                    tickfont=dict(size=14)
                ),
                yaxis=dict(
                    titlefont=dict(size=16),
                    tickfont=dict(size=14)
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial'),
                margin=dict(l=150, r=60, t=100, b=60)
            )
        else:
            # Fallback simple chart
            fig = go.Figure()
            fig.add_annotation(
                text="Geographic data not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=20)
            )
        
        return fig
    
    def _create_roi_chart(self, roi_data: Dict[str, Any], settings: ExportSettings) -> go.Figure:
        """Create ROI analysis chart"""
        scenarios = ['Conservative', 'Expected', 'Optimistic']
        
        if isinstance(roi_data, dict) and 'total_roi' in roi_data:
            base_roi = roi_data['total_roi']
            values = [base_roi * 0.8, base_roi, base_roi * 1.2]
        else:
            values = [15, 25, 35]  # Default values
        
        fig = go.Figure(data=[
            go.Bar(
                x=scenarios,
                y=values,
                marker=dict(
                    color=[settings.brand_colors['secondary'], 
                           settings.brand_colors['primary'], 
                           settings.brand_colors['accent']],
                    line=dict(color='black', width=1)
                ),
                text=[f"{v:.1f}%" for v in values],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='ROI Analysis Scenarios',
                font=dict(size=24, color=settings.brand_colors['text']),
                x=0.5
            ),
            xaxis=dict(
                title='Scenario',
                titlefont=dict(size=16),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title='ROI (%)',
                titlefont=dict(size=16),
                tickfont=dict(size=14)
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial'),
            margin=dict(l=60, r=60, t=100, b=60)
        )
        
        return fig
    
    def _create_competitive_chart(self, comp_data: Any, settings: ExportSettings) -> go.Figure:
        """Create competitive position chart"""
        # Sample competitive data
        companies = ['Leaders', 'Challengers', 'Followers', 'Laggards']
        adoption_rates = [75, 55, 35, 15]
        market_share = [35, 30, 25, 10]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=adoption_rates,
            y=market_share,
            mode='markers+text',
            marker=dict(
                size=[40, 35, 30, 25],
                color=[settings.brand_colors['primary'], settings.brand_colors['secondary'],
                       settings.brand_colors['accent'], '#cccccc'],
                opacity=0.8
            ),
            text=companies,
            textposition="middle center",
            textfont=dict(color='white', size=12)
        ))
        
        fig.update_layout(
            title=dict(
                text='Competitive Position Matrix',
                font=dict(size=24, color=settings.brand_colors['text']),
                x=0.5
            ),
            xaxis=dict(
                title='AI Adoption Rate (%)',
                titlefont=dict(size=16),
                tickfont=dict(size=14),
                range=[0, 100]
            ),
            yaxis=dict(
                title='Market Share (%)',
                titlefont=dict(size=16),
                tickfont=dict(size=14),
                range=[0, 50]
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial'),
            margin=dict(l=60, r=60, t=100, b=60)
        )
        
        return fig
    
    def _create_business_charts(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, go.Figure]:
        """Create business leader specific charts"""
        charts = {}
        
        # Investment timeline chart
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
        investment = [2.5, 3.2, 4.1, 5.8]
        returns = [1.8, 3.5, 6.2, 10.1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quarters, y=investment, mode='lines+markers',
            name='Investment ($M)', line=dict(color=settings.brand_colors['primary'])
        ))
        fig.add_trace(go.Scatter(
            x=quarters, y=returns, mode='lines+markers',
            name='Returns ($M)', line=dict(color=settings.brand_colors['accent'])
        ))
        
        fig.update_layout(
            title='Investment vs Returns Timeline',
            xaxis_title='Quarter',
            yaxis_title='Amount ($M)',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        charts['Investment Timeline'] = fig
        return charts
    
    def _create_policy_charts(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, go.Figure]:
        """Create policymaker specific charts"""
        charts = {}
        
        # Labor impact chart
        sectors = ['Manufacturing', 'Healthcare', 'Finance', 'Education', 'Government']
        job_creation = [15, 25, 30, 20, 10]
        job_displacement = [-10, -5, -8, -3, -2]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Job Creation', x=sectors, y=job_creation,
            marker_color=settings.brand_colors['accent']
        ))
        fig.add_trace(go.Bar(
            name='Job Displacement', x=sectors, y=job_displacement,
            marker_color=settings.brand_colors['secondary']
        ))
        
        fig.update_layout(
            title='Labor Market Impact by Sector',
            xaxis_title='Sector',
            yaxis_title='Jobs (thousands)',
            barmode='relative',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        charts['Labor Impact'] = fig
        return charts
    
    def _create_research_charts(self, data: Dict[str, Any], settings: ExportSettings) -> Dict[str, go.Figure]:
        """Create researcher specific charts"""
        charts = {}
        
        # Technology maturity chart
        technologies = ['NLP', 'Computer Vision', 'ML Platforms', 'Robotics', 'GenAI']
        maturity = [85, 75, 90, 45, 60]
        adoption = [70, 65, 80, 25, 50]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=maturity, y=adoption, mode='markers+text',
            text=technologies, textposition="top center",
            marker=dict(size=15, color=settings.brand_colors['primary'])
        ))
        
        fig.update_layout(
            title='Technology Maturity vs Adoption',
            xaxis_title='Technology Maturity (%)',
            yaxis_title='Market Adoption (%)',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        charts['Technology Maturity'] = fig
        return charts
    
    def _create_specific_chart(self, data: Dict[str, Any], chart_name: str, settings: ExportSettings) -> go.Figure:
        """Create a specific named chart"""
        chart_creators = {
            'historical_trends': lambda: self._create_trends_chart(data.get('historical_trends', pd.DataFrame()), settings),
            'geographic_distribution': lambda: self._create_geographic_chart(data.get('geographic_data', pd.DataFrame()), settings),
            'roi_analysis': lambda: self._create_roi_chart(data.get('roi_data', {}), settings),
            'competitive_position': lambda: self._create_competitive_chart(data.get('competitive_data', {}), settings)
        }
        
        creator = chart_creators.get(chart_name.lower().replace(' ', '_'))
        if creator:
            return creator()
        else:
            # Default empty chart
            fig = go.Figure()
            fig.add_annotation(
                text=f"Chart '{chart_name}' not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                font=dict(size=20)
            )
            return fig
    
    def _add_header(self, img: Image.Image, draw: ImageDraw.Draw, persona: Optional[str], settings: ExportSettings, width: int):
        """Add header to dashboard image"""
        header_height = 150
        
        # Header background
        draw.rectangle([0, 0, width, header_height], fill=settings.brand_colors['primary'])
        
        # Title text
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        title = "AI Adoption Dashboard"
        if persona and persona != "General":
            title += f" - {persona} Perspective"
        
        # Calculate text position
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        draw.text((title_x, 30), title, fill='white', font=title_font)
        
        # Subtitle
        subtitle = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (width - subtitle_width) // 2
        
        draw.text((subtitle_x, 90), subtitle, fill='white', font=subtitle_font)
    
    def _layout_charts_grid(self, img: Image.Image, charts: Dict[str, go.Figure], width: int, height: int, settings: ExportSettings):
        """Layout charts in a grid on the dashboard"""
        if not charts:
            return
        
        # Calculate grid dimensions
        chart_count = len(charts)
        if chart_count <= 2:
            grid_cols, grid_rows = chart_count, 1
        elif chart_count <= 4:
            grid_cols, grid_rows = 2, 2
        else:
            grid_cols, grid_rows = 3, (chart_count + 2) // 3
        
        # Chart dimensions
        margin = 50
        header_height = 150
        footer_height = 100
        available_height = height - header_height - footer_height - (margin * 2)
        available_width = width - (margin * 2)
        
        chart_width = (available_width - (margin * (grid_cols - 1))) // grid_cols
        chart_height = (available_height - (margin * (grid_rows - 1))) // grid_rows
        
        # Place charts
        for i, (chart_name, fig) in enumerate(charts.items()):
            row = i // grid_cols
            col = i % grid_cols
            
            x = margin + col * (chart_width + margin)
            y = header_height + margin + row * (chart_height + margin)
            
            # Convert Plotly figure to PIL Image
            chart_img = self._plotly_to_pil(fig, chart_width, chart_height)
            
            # Paste chart onto main image
            img.paste(chart_img, (x, y))
    
    def _plotly_to_pil(self, fig: go.Figure, width: int, height: int) -> Image.Image:
        """Convert Plotly figure to PIL Image"""
        img_bytes = pio.to_image(fig, format="png", width=width, height=height, scale=1)
        return Image.open(io.BytesIO(img_bytes))
    
    def _add_branding(self, img: Image.Image, draw: ImageDraw.Draw, settings: ExportSettings, width: int, height: int):
        """Add branding elements to the image"""
        if settings.watermark:
            # Add watermark
            try:
                watermark_font = ImageFont.truetype("arial.ttf", 36)
            except:
                watermark_font = ImageFont.load_default()
            
            # Create semi-transparent watermark
            watermark_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
            watermark_draw = ImageDraw.Draw(watermark_img)
            
            watermark_text = settings.watermark
            bbox = watermark_draw.textbbox((0, 0), watermark_text, font=watermark_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position at bottom right
            x = width - text_width - 50
            y = height - text_height - 50
            
            watermark_draw.text((x, y), watermark_text, fill=(128, 128, 128, 128), font=watermark_font)
            
            # Composite watermark onto main image
            img.paste(watermark_img, (0, 0), watermark_img)
    
    def _add_footer(self, img: Image.Image, draw: ImageDraw.Draw, settings: ExportSettings, width: int, height: int):
        """Add footer to dashboard image"""
        footer_height = 100
        footer_y = height - footer_height
        
        # Footer background
        draw.rectangle([0, footer_y, width, height], fill='#f8f9fa')
        
        # Footer text
        try:
            footer_font = ImageFont.truetype("arial.ttf", 16)
        except:
            footer_font = ImageFont.load_default()
        
        footer_text = f"© {datetime.now().year} {settings.company_name} | AI Adoption Dashboard v2.0"
        
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        
        draw.text((text_x, footer_y + 25), footer_text, fill=settings.brand_colors['text'], font=footer_font)
    
    def _create_svg_layout(self, charts: Dict[str, go.Figure], persona: Optional[str], settings: ExportSettings, **options) -> str:
        """Create SVG layout for dashboard"""
        width = options.get('width', 1200)
        height = options.get('height', 800)
        
        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="white"/>',
            
            # Header
            f'<rect width="{width}" height="100" fill="{settings.brand_colors["primary"]}"/>',
            f'<text x="{width//2}" y="40" text-anchor="middle" fill="white" font-size="24" font-family="Arial">',
            f'AI Adoption Dashboard',
            '</text>',
            f'<text x="{width//2}" y="70" text-anchor="middle" fill="white" font-size="14" font-family="Arial">',
            f'Generated on {datetime.now().strftime("%B %d, %Y")}',
            '</text>'
        ]
        
        # Add charts as embedded SVGs
        chart_y = 120
        for chart_name, fig in charts.items():
            chart_svg = pio.to_image(fig, format="svg", width=400, height=300).decode('utf-8')
            # Extract the inner SVG content (remove outer SVG tags)
            inner_svg = chart_svg[chart_svg.find('>')+1:chart_svg.rfind('</svg>')]
            
            svg_parts.extend([
                f'<g transform="translate(50, {chart_y})">',
                inner_svg,
                '</g>'
            ])
            chart_y += 320
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _create_chart_index(self, output_dir: Path, chart_names: List[str], format: ExportFormat):
        """Create index file for batch chart export"""
        index_content = [
            "# AI Adoption Dashboard - Chart Export",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Charts Included:",
            ""
        ]
        
        for chart_name in chart_names:
            filename = f"{chart_name.replace(' ', '_').lower()}.{format.value}"
            index_content.append(f"- [{chart_name}](./{filename})")
        
        index_path = output_dir / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(index_content))