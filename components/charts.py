"""
Professional Chart Components for AI Adoption Dashboard

This module provides advanced chart components with:
- Executive-friendly visualizations
- Interactive features
- Consistent theming
- Responsive design
- Accessibility features
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, Dict, Any, List, Tuple, Union
from dataclasses import dataclass
import numpy as np
from enum import Enum

# Color schemes and styling
class ChartTheme(Enum):
    EXECUTIVE = "executive"
    ANALYST = "analyst"
    PRESENTATION = "presentation"

@dataclass
class ChartStyle:
    """Chart styling configuration"""
    colors: List[str]
    font_family: str
    font_size: int
    background_color: str
    grid_color: str
    hover_color: str
    
    @classmethod
    def executive_style(cls):
        return cls(
            colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E'],
            font_family='Arial, sans-serif',
            font_size=12,
            background_color='rgba(0,0,0,0)',
            grid_color='rgba(128,128,128,0.2)',
            hover_color='rgba(46,134,171,0.8)'
        )
    
    @classmethod
    def analyst_style(cls):
        return cls(
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            font_family='Helvetica, sans-serif', 
            font_size=11,
            background_color='rgba(0,0,0,0)',
            grid_color='rgba(128,128,128,0.3)',
            hover_color='rgba(31,119,180,0.8)'
        )

class MetricCard:
    """Professional metric card with trend indicators and styling"""
    
    def __init__(self, theme: ChartTheme = ChartTheme.EXECUTIVE):
        self.theme = theme
        self.style = ChartStyle.executive_style() if theme == ChartTheme.EXECUTIVE else ChartStyle.analyst_style()
    
    def render(self, 
               title: str, 
               value: Union[str, int, float], 
               delta: Optional[str] = None,
               trend: Optional[List[float]] = None,
               insight: Optional[str] = None,
               color: Optional[str] = None,
               help_text: Optional[str] = None) -> None:
        """
        Render an advanced metric card with optional trend sparkline
        
        Args:
            title: Metric title
            value: Primary value to display
            delta: Change indicator (e.g., "+5.2%" or "-1.1pp")
            trend: List of values for sparkline trend
            insight: Brief insight text
            color: Override color (success, warning, error, info)
            help_text: Tooltip help text
        """
        
        # Determine color scheme
        if color == "success":
            bg_color = "rgba(46, 160, 67, 0.1)"
            border_color = "#2ea043"
        elif color == "warning": 
            bg_color = "rgba(255, 193, 7, 0.1)"
            border_color = "#ffc107"
        elif color == "error":
            bg_color = "rgba(220, 53, 69, 0.1)" 
            border_color = "#dc3545"
        else:
            bg_color = "rgba(46, 134, 171, 0.1)"
            border_color = self.style.colors[0]
        
        # Create container with custom styling
        container_html = f"""
        <div style="
            background: linear-gradient(135deg, {bg_color} 0%, rgba(255,255,255,0.05) 100%);
            border-left: 4px solid {border_color};
            border-radius: 8px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)'"
           onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'">
            
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <h4 style="
                        margin: 0 0 0.5rem 0; 
                        color: #333; 
                        font-size: 0.9rem; 
                        font-weight: 500;
                        opacity: 0.8;
                    ">{title}</h4>
                    
                    <h2 style="
                        margin: 0 0 0.25rem 0; 
                        color: {border_color}; 
                        font-size: 2rem; 
                        font-weight: bold;
                        line-height: 1.2;
                    ">{value}</h2>
                    
                    {f'<p style="margin: 0; font-size: 0.85rem; color: #666; font-weight: 500;">{delta}</p>' if delta else ''}
                    {f'<p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #555; font-style: italic;">{insight}</p>' if insight else ''}
                </div>
                
                {self._create_sparkline_html(trend, border_color) if trend else ''}
            </div>
        </div>
        """
        
        st.markdown(container_html, unsafe_allow_html=True)
        
        # Add help text if provided
        if help_text:
            st.caption(f"ℹ️ {help_text}")
    
    def _create_sparkline_html(self, trend: List[float], color: str) -> str:
        """Create SVG sparkline for trend visualization"""
        if not trend or len(trend) < 2:
            return ""
        
        # Normalize trend data
        min_val, max_val = min(trend), max(trend)
        if max_val == min_val:
            normalized = [50] * len(trend)  # Flat line
        else:
            normalized = [(val - min_val) / (max_val - min_val) * 40 + 10 for val in trend]
        
        # Create SVG path
        width, height = 80, 50
        step = width / (len(trend) - 1)
        
        points = " ".join([f"{i * step},{height - norm}" for i, norm in enumerate(normalized)])
        
        return f"""
        <div style="width: 80px; height: 50px; margin-left: 1rem;">
            <svg width="80" height="50" style="overflow: visible;">
                <polyline points="{points}" 
                         fill="none" 
                         stroke="{color}" 
                         stroke-width="2"
                         opacity="0.8"/>
                <circle cx="{(len(trend)-1) * step}" 
                       cy="{height - normalized[-1]}" 
                       r="3" 
                       fill="{color}"/>
            </svg>
        </div>
        """

class TrendChart:
    """Advanced trend chart with interactive features"""
    
    def __init__(self, theme: ChartTheme = ChartTheme.EXECUTIVE):
        self.theme = theme
        self.style = ChartStyle.executive_style() if theme == ChartTheme.EXECUTIVE else ChartStyle.analyst_style()
    
    def render(self,
               data: pd.DataFrame,
               x_col: str,
               y_cols: Union[str, List[str]], 
               title: str,
               subtitle: Optional[str] = None,
               annotations: Optional[List[Dict]] = None,
               height: int = 500,
               show_controls: bool = True,
               enable_zoom: bool = True) -> go.Figure:
        """
        Render an advanced trend chart with professional styling
        
        Args:
            data: DataFrame with trend data
            x_col: Column name for x-axis (typically time/year)
            y_cols: Column name(s) for y-axis (metrics)
            title: Chart title
            subtitle: Optional subtitle
            annotations: List of annotation dictionaries
            height: Chart height in pixels
            show_controls: Whether to show interactive controls
            enable_zoom: Whether to enable zoom functionality
        """
        
        if isinstance(y_cols, str):
            y_cols = [y_cols]
        
        # Create figure
        fig = go.Figure()
        
        # Add traces for each y column
        for i, y_col in enumerate(y_cols):
            if y_col not in data.columns:
                st.error(f"Column '{y_col}' not found in data")
                continue
                
            color = self.style.colors[i % len(self.style.colors)]
            
            # Add main line
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                mode='lines+markers',
                name=y_col.replace('_', ' ').title(),
                line=dict(
                    width=3,
                    color=color,
                    shape='spline',  # Smooth curves
                    smoothing=0.3
                ),
                marker=dict(
                    size=8,
                    color=color,
                    line=dict(width=2, color='white')
                ),
                hovertemplate=f'<b>{y_col.replace("_", " ").title()}</b><br>' +
                             f'{x_col.title()}: %{{x}}<br>' +
                             f'Value: %{{y}}<br>' +
                             '<extra></extra>',
                fill='tonexty' if i > 0 else None,
                fillcolor=self._hex_to_rgba(color, 0.1)
            ))
            
            # Add trend line if data has enough points
            if len(data) >= 3:
                z = np.polyfit(range(len(data)), data[y_col], 1)
                trend_line = np.poly1d(z)(range(len(data)))
                
                fig.add_trace(go.Scatter(
                    x=data[x_col],
                    y=trend_line,
                    mode='lines',
                    name=f'{y_col} Trend',
                    line=dict(
                        width=2,
                        color=color,
                        dash='dash'
                    ),
                    opacity=0.6,
                    hoverinfo='skip',
                    showlegend=False
                ))
        
        # Add annotations if provided
        if annotations:
            for ann in annotations:
                fig.add_annotation(**ann)
        
        # Update layout with professional styling
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>" + (f"<br><sub>{subtitle}</sub>" if subtitle else ""),
                x=0.02,
                font=dict(
                    family=self.style.font_family,
                    size=20,
                    color='#2c3e50'
                )
            ),
            xaxis=dict(
                title=x_col.replace('_', ' ').title(),
                showgrid=True,
                gridwidth=1,
                gridcolor=self.style.grid_color,
                tickfont=dict(size=11),
                title_font=dict(size=13, color='#555')
            ),
            yaxis=dict(
                title="Value",
                showgrid=True,
                gridwidth=1,
                gridcolor=self.style.grid_color,
                tickfont=dict(size=11),
                title_font=dict(size=13, color='#555')
            ),
            plot_bgcolor=self.style.background_color,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family=self.style.font_family),
            height=height,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right", 
                x=1,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            ),
            margin=dict(l=60, r=40, t=80, b=60)
        )
        
        # Configure interactivity
        if enable_zoom:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False)),
                dragmode='zoom'
            )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': show_controls,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'] if not show_controls else [],
            'displaylogo': False
        })
        
        return fig
    
    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        """Convert hex color to rgba format"""
        # Remove # if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex to RGB
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return f'rgba({r},{g},{b},{alpha})'

class ComparisonChart:
    """Advanced comparison chart for benchmarking and analysis"""
    
    def __init__(self, theme: ChartTheme = ChartTheme.EXECUTIVE):
        self.theme = theme
        self.style = ChartStyle.executive_style() if theme == ChartTheme.EXECUTIVE else ChartStyle.analyst_style()
    
    def render_industry_comparison(self,
                                 data: pd.DataFrame,
                                 category_col: str,
                                 value_cols: List[str],
                                 title: str,
                                 benchmark_lines: Optional[Dict[str, float]] = None,
                                 height: int = 500) -> go.Figure:
        """
        Render an industry comparison chart with benchmarks
        
        Args:
            data: DataFrame with comparison data
            category_col: Column for categories (e.g., 'industry')
            value_cols: List of value columns to compare
            title: Chart title
            benchmark_lines: Dict of benchmark names and values
            height: Chart height
        """
        
        fig = go.Figure()
        
        # Add bars for each value column
        for i, col in enumerate(value_cols):
            color = self.style.colors[i % len(self.style.colors)]
            
            fig.add_trace(go.Bar(
                name=col.replace('_', ' ').title(),
                x=data[category_col],
                y=data[col],
                marker=dict(
                    color=color,
                    opacity=0.8,
                    line=dict(color='white', width=1)
                ),
                text=[f'{val}%' if col.endswith('_rate') or col.endswith('_adoption') 
                      else f'{val}x' if 'roi' in col.lower() 
                      else str(val) for val in data[col]],
                textposition='outside',
                textfont=dict(size=10, color='#333'),
                hovertemplate=f'<b>%{{x}}</b><br>{col.replace('_', ' ').title()}: %{{y}}<extra></extra>'
            ))
        
        # Add benchmark lines
        if benchmark_lines:
            for benchmark_name, value in benchmark_lines.items():
                fig.add_hline(
                    y=value,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"{benchmark_name}: {value}",
                    annotation_position="right"
                )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.02,
                font=dict(size=18, color='#2c3e50')
            ),
            xaxis=dict(
                title=category_col.replace('_', ' ').title(),
                tickangle=45 if len(data) > 5 else 0
            ),
            yaxis=dict(title="Value"),
            barmode='group',
            height=height,
            plot_bgcolor=self.style.background_color,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=len(value_cols) > 1
        )
        
        st.plotly_chart(fig, use_container_width=True)
        return fig

class ROIChart:
    """Specialized ROI visualization with risk-return analysis"""
    
    def __init__(self, theme: ChartTheme = ChartTheme.EXECUTIVE):
        self.theme = theme
        self.style = ChartStyle.executive_style() if theme == ChartTheme.EXECUTIVE else ChartStyle.analyst_style()
    
    def render_roi_analysis(self,
                           data: pd.DataFrame,
                           roi_col: str,
                           risk_col: Optional[str] = None,
                           size_col: Optional[str] = None,
                           category_col: Optional[str] = None,
                           title: str = "ROI Analysis",
                           height: int = 500) -> go.Figure:
        """
        Render ROI analysis with risk-return scatter plot
        
        Args:
            data: DataFrame with ROI data
            roi_col: Column for ROI values
            risk_col: Optional column for risk values
            size_col: Optional column for bubble sizes
            category_col: Optional column for categories/colors
            title: Chart title
            height: Chart height
        """
        
        if risk_col and risk_col in data.columns:
            # Risk-Return scatter plot
            fig = px.scatter(
                data,
                x=risk_col,
                y=roi_col,
                size=size_col if size_col and size_col in data.columns else None,
                color=category_col if category_col and category_col in data.columns else None,
                hover_name=category_col if category_col else None,
                title=title,
                labels={
                    roi_col: 'Return on Investment (x)',
                    risk_col: 'Risk Score',
                    size_col: size_col.replace('_', ' ').title() if size_col else None
                },
                color_discrete_sequence=self.style.colors
            )
            
            # Add quadrant lines
            roi_median = data[roi_col].median()
            risk_median = data[risk_col].median()
            
            fig.add_hline(y=roi_median, line_dash="dot", line_color="gray", opacity=0.5)
            fig.add_vline(x=risk_median, line_dash="dot", line_color="gray", opacity=0.5)
            
            # Add quadrant labels
            fig.add_annotation(x=risk_median*0.5, y=roi_median*1.5, text="High Return<br>Low Risk", 
                             showarrow=False, bgcolor="rgba(0,255,0,0.1)")
            fig.add_annotation(x=risk_median*1.5, y=roi_median*1.5, text="High Return<br>High Risk", 
                             showarrow=False, bgcolor="rgba(255,255,0,0.1)")
            
        else:
            # Simple ROI bar chart
            fig = go.Figure()
            
            categories = data[category_col] if category_col and category_col in data.columns else range(len(data))
            
            fig.add_trace(go.Bar(
                x=categories,
                y=data[roi_col],
                marker=dict(
                    color=data[roi_col],
                    colorscale='RdYlGn',
                    colorbar=dict(title="ROI Multiplier")
                ),
                text=[f'{val:.1f}x' for val in data[roi_col]],
                textposition='outside'
            ))
            
            # Add ROI threshold lines
            fig.add_hline(y=2.0, line_dash="dash", line_color="orange", 
                         annotation_text="Minimum Viable ROI (2.0x)")
            fig.add_hline(y=3.0, line_dash="dash", line_color="green",
                         annotation_text="Strong ROI Threshold (3.0x)")
        
        # Update layout
        fig.update_layout(
            height=height,
            plot_bgcolor=self.style.background_color,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family=self.style.font_family)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        return fig

# Usage example and testing function
def demo_charts():
    """Demo function to showcase chart components"""
    st.title("🎨 Advanced Chart Components Demo")
    
    # Sample data
    trend_data = pd.DataFrame({
        'year': range(2020, 2026),
        'ai_adoption': [10, 25, 45, 65, 78, 85],
        'genai_adoption': [0, 2, 15, 40, 71, 82],
        'investment': [50, 75, 120, 180, 252, 320]
    })
    
    industry_data = pd.DataFrame({
        'industry': ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
                    'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government'],
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2],
        'risk_score': [25, 35, 45, 55, 40, 60, 70, 80]
    })
    
    # Demo metric cards
    st.subheader("📊 Metric Cards")
    col1, col2, col3 = st.columns(3)
    
    metric_card = MetricCard()
    
    with col1:
        metric_card.render(
            title="Market Adoption",
            value="78%",
            delta="+23pp vs 2023",
            trend=[45, 52, 58, 65, 71, 78],
            insight="Crossed majority threshold",
            color="success"
        )
    
    with col2:
        metric_card.render(
            title="Average ROI",
            value="3.2x",
            delta="+0.4x vs baseline", 
            insight="Consistent value creation",
            color="info"
        )
    
    with col3:
        metric_card.render(
            title="Investment Risk",
            value="Medium",
            delta="Stable outlook",
            insight="Balanced risk-return profile",
            color="warning"
        )
    
    # Demo trend chart
    st.subheader("📈 Trend Analysis")
    trend_chart = TrendChart()
    trend_chart.render(
        data=trend_data,
        x_col='year',
        y_cols=['ai_adoption', 'genai_adoption'],
        title="AI Adoption Trends Over Time",
        subtitle="Strategic market evolution 2020-2025",
        annotations=[
            dict(x=2022, y=45, text="GenAI Revolution", showarrow=True, arrowhead=2)
        ]
    )
    
    # Demo comparison chart
    st.subheader("🏭 Industry Comparison")
    comparison_chart = ComparisonChart()
    comparison_chart.render_industry_comparison(
        data=industry_data,
        category_col='industry',
        value_cols=['adoption_rate', 'avg_roi'],
        title="Industry Adoption vs ROI Analysis",
        benchmark_lines={"Market Average": 75, "ROI Threshold": 3.0}
    )
    
    # Demo ROI chart
    st.subheader("💰 ROI Risk Analysis")
    roi_chart = ROIChart()
    roi_chart.render_roi_analysis(
        data=industry_data,
        roi_col='avg_roi',
        risk_col='risk_score',
        size_col='adoption_rate',
        category_col='industry',
        title="Risk-Return Analysis by Industry"
    )

if __name__ == "__main__":
    demo_charts() 