"""
Reusable UI components - Stop repeating yourself!
Extract common UI patterns from your app.py
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Optional

from config.settings import DashboardConfig


class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def metric_card(
        title: str, 
        value: str, 
        delta: str = "", 
        help_text: str = "",
        color: str = "primary"
    ) -> None:
        """
        Create a styled metric card
        
        Use this instead of repeating st.metric() everywhere
        """
        color_map = {
            "primary": "#1f77b4",
            "success": "#2ecc71", 
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        
        bg_color = color_map.get(color, color_map["primary"])
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {bg_color}20 0%, {bg_color}10 100%);
            border-left: 4px solid {bg_color};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        '>
            <h3 style='margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #666;'>{title}</h3>
            <h2 style='margin: 0 0 0.25rem 0; font-size: 1.8rem; color: #333;'>{value}</h2>
            <p style='margin: 0; font-size: 0.9rem; color: {bg_color};'>{delta}</p>
            <small style='color: #888;'>{help_text}</small>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def insight_box(
        title: str, 
        content: str, 
        box_type: str = "info"
    ) -> None:
        """
        Create styled insight boxes
        
        Replace your repeated markdown patterns with this
        """
        type_styles = {
            "info": {"color": "#2E86AB", "bg": "rgba(46, 134, 171, 0.1)"},
            "success": {"color": "#2ecc71", "bg": "rgba(46, 204, 113, 0.1)"},
            "warning": {"color": "#f39c12", "bg": "rgba(243, 156, 18, 0.1)"},
            "error": {"color": "#e74c3c", "bg": "rgba(231, 76, 60, 0.1)"}
        }
        
        style = type_styles.get(box_type, type_styles["info"])
        
        st.markdown(f"""
        <div style='
            border-left: 4px solid {style["color"]};
            background: {style["bg"]};
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 8px 8px 0;
        '>
            <h4 style='color: {style["color"]}; margin-top: 0;'>{title}</h4>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_metric_grid(metrics: Dict[str, Dict[str, str]], columns: int = 4) -> None:
        """
        Create a grid of metrics
        
        Usage:
        metrics_data = {
            "Market Adoption": {"value": "78%", "delta": "+23pp", "help": "Explanation"},
            "Cost Reduction": {"value": "280x", "delta": "Since 2022", "help": "Details"}
        }
        UIComponents.create_metric_grid(metrics_data)
        """
        metric_names = list(metrics.keys())
        cols = st.columns(columns)
        
        for i, metric_name in enumerate(metric_names):
            col_idx = i % columns
            metric_data = metrics[metric_name]
            
            with cols[col_idx]:
                st.metric(
                    label=metric_name,
                    value=metric_data.get("value", "N/A"),
                    delta=metric_data.get("delta", ""),
                    help=metric_data.get("help", "")
                )
    
    @staticmethod
    def apply_custom_css() -> None:
        """Apply custom CSS styling - call this once in your app"""
        st.markdown("""
        <style>
        .metric-card {
            background-color: transparent;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .insight-box {
            border-left: 4px solid #2E86AB;
            background: rgba(46, 134, 171, 0.1);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0.25rem;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .metric-card {
                padding: 1rem;
                font-size: 0.9rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)


class ChartFactory:
    """Factory for creating standardized charts"""
    
    @staticmethod
    def create_adoption_trend_chart(data: pd.DataFrame, title: str = "AI Adoption Trends") -> go.Figure:
        """
        Create standardized adoption trend chart
        
        Use this instead of repeating chart creation code
        """
        fig = go.Figure()
        
        # Add AI adoption line
        fig.add_trace(go.Scatter(
            x=data['year'],
            y=data['ai_use'],
            mode='lines+markers',
            name='Overall AI Use',
            line=dict(width=4, color='#1f77b4'),
            marker=dict(size=8),
            hovertemplate='Year: %{x}<br>Adoption: %{y}%<extra></extra>'
        ))
        
        # Add GenAI line if available
        if 'genai_use' in data.columns:
            fig.add_trace(go.Scatter(
                x=data['year'],
                y=data['genai_use'],
                mode='lines+markers',
                name='GenAI Use',
                line=dict(width=4, color='#ff7f0e'),
                marker=dict(size=8),
                hovertemplate='Year: %{x}<br>GenAI Adoption: %{y}%<extra></extra>'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Year",
            yaxis_title="Adoption Rate (%)",
            height=DashboardConfig.UI.CHART_HEIGHT,
            hovermode='x unified'
        )
        
        return fig


# Create instances for easy import
ui = UIComponents()
charts = ChartFactory()