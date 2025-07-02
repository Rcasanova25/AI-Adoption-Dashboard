"""
Accessibility Integration Script
Integrates accessibility improvements into existing dashboard views
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Optional, Any, Union
import logging

from .accessible_components import (
    AccessibleChart, AccessibleMetric, AccessibleLayout, 
    AccessibleColorPalette, accessible_dashboard
)
from .accessible_themes import initialize_accessible_theme, add_accessibility_controls

logger = logging.getLogger(__name__)


class AccessibilityIntegrator:
    """Integrates accessibility features into existing dashboard components"""
    
    def __init__(self):
        self.palette = AccessibleColorPalette()
        self.chart_component = AccessibleChart("", accessibility_level="AA")
        self.metric_component = AccessibleMetric()
        self.layout_component = AccessibleLayout()
    
    def enhance_plotly_chart(self, 
                           fig: go.Figure, 
                           title: str,
                           description: str,
                           data: Optional[pd.DataFrame] = None) -> go.Figure:
        """Enhance existing Plotly chart with accessibility features"""
        
        # Apply accessible color scheme
        fig.update_layout(
            title={
                'text': title,
                'font': {'size': 18, 'color': self.palette.text_primary},
                'x': 0.5,
                'xanchor': 'center'
            },
            font={
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': self.palette.text_primary
            },
            paper_bgcolor=self.palette.background_primary,
            plot_bgcolor=self.palette.background_primary
        )
        
        # Enhance gridlines for better visibility
        fig.update_xaxes(
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            showgrid=True,
            title_font_size=14,
            tickfont_size=12
        )
        
        fig.update_yaxes(
            gridcolor='rgba(128,128,128,0.3)',
            gridwidth=1,
            showgrid=True,
            title_font_size=14,
            tickfont_size=12
        )
        
        # Update trace colors to use accessible palette
        if fig.data:
            for i, trace in enumerate(fig.data):
                color_index = i % len(self.palette.data_colors)
                color = self.palette.data_colors[color_index]
                
                # Update based on trace type
                if hasattr(trace, 'marker') and trace.marker:
                    trace.marker.color = color
                    trace.marker.line = dict(width=2, color='white')
                    if hasattr(trace.marker, 'size'):
                        trace.marker.size = max(8, trace.marker.size or 6)  # Ensure minimum size
                
                if hasattr(trace, 'line') and trace.line:
                    trace.line.color = color
                    trace.line.width = max(3, trace.line.width or 2)  # Ensure minimum width
        
        # Add accessibility metadata
        fig.update_layout(
            annotations=[
                dict(
                    text=f"Chart: {title}. {description}",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0, y=0,
                    visible=False,  # For screen readers only
                    font=dict(color=self.palette.text_primary)
                )
            ]
        )
        
        return fig
    
    def create_accessible_metric_display(self,
                                       label: str,
                                       value: Union[str, float, int],
                                       delta: Optional[str] = None,
                                       help_text: Optional[str] = None) -> None:
        """Create accessible metric display"""
        
        # Determine trend direction from delta
        trend_direction = None
        if delta:
            if '+' in delta or '↑' in delta:
                trend_direction = "up"
            elif '-' in delta or '↓' in delta:
                trend_direction = "down"
        
        self.metric_component.render(
            label=label,
            value=value,
            delta=delta,
            help_text=help_text,
            trend_direction=trend_direction
        )
    
    def add_chart_alternative_content(self,
                                    data: pd.DataFrame,
                                    chart_title: str,
                                    description: str) -> None:
        """Add alternative content for charts"""
        
        # Add descriptive text
        st.markdown(f"""
        <div class="sr-only" aria-label="Chart description">
            {description}
        </div>
        """, unsafe_allow_html=True)
        
        # Add data table alternative
        with st.expander(f"📊 Data Table: {chart_title}", expanded=False):
            st.markdown("**Alternative representation of chart data:**")
            st.dataframe(data, use_container_width=True)
            
            # Add summary if numeric data exists
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.markdown("**Summary Statistics:**")
                summary = data[numeric_cols].describe()
                st.dataframe(summary, use_container_width=True)
    
    def enhance_view_accessibility(self, view_function):
        """Decorator to enhance view accessibility"""
        
        def wrapper(*args, **kwargs):
            # Apply accessible theme if not already applied
            if 'accessibility_theme_applied' not in st.session_state:
                initialize_accessible_theme()
                st.session_state.accessibility_theme_applied = True
            
            # Add skip link
            st.markdown("""
            <a href="#main-content" class="skip-link">Skip to main content</a>
            <main id="main-content" role="main">
            """, unsafe_allow_html=True)
            
            # Call original view function
            result = view_function(*args, **kwargs)
            
            # Close main content area
            st.markdown("</main>", unsafe_allow_html=True)
            
            return result
        
        return wrapper
    
    def create_accessible_section(self,
                                title: str,
                                level: int = 2,
                                description: Optional[str] = None) -> None:
        """Create accessible section with proper heading hierarchy"""
        self.layout_component.create_section_header(title, level, description)
    
    def apply_global_accessibility_enhancements(self) -> None:
        """Apply global accessibility enhancements to the app"""
        
        # Initialize accessible theme
        initialize_accessible_theme()
        
        # Add accessibility controls to sidebar
        add_accessibility_controls()
        
        # Apply global CSS for accessibility
        accessible_dashboard.apply_accessibility_css()
        
        # Add keyboard navigation hints
        st.markdown("""
        <div class="sr-only">
            <h2>Keyboard Navigation Instructions</h2>
            <ul>
                <li>Tab key: Navigate between interactive elements</li>
                <li>Enter or Space: Activate buttons and links</li>
                <li>Arrow keys: Navigate within charts and data tables</li>
                <li>Escape: Close dialogs and dropdowns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# Global integrator instance
accessibility_integrator = AccessibilityIntegrator()


# Helper functions for easy integration
def make_chart_accessible(fig: go.Figure, 
                         title: str, 
                         description: str,
                         data: Optional[pd.DataFrame] = None) -> go.Figure:
    """Make a Plotly chart accessible"""
    enhanced_fig = accessibility_integrator.enhance_plotly_chart(fig, title, description, data)
    
    # Display enhanced chart
    st.plotly_chart(enhanced_fig, use_container_width=True)
    
    # Add alternative content if data provided
    if data is not None:
        accessibility_integrator.add_chart_alternative_content(data, title, description)
    
    return enhanced_fig


def create_accessible_metric(label: str,
                           value: Union[str, float, int],
                           delta: Optional[str] = None,
                           help_text: Optional[str] = None) -> None:
    """Create an accessible metric display"""
    accessibility_integrator.create_accessible_metric_display(label, value, delta, help_text)


def create_accessible_section(title: str, 
                            level: int = 2, 
                            description: Optional[str] = None) -> None:
    """Create an accessible section header"""
    accessibility_integrator.create_accessible_section(title, level, description)


def enable_view_accessibility(view_function):
    """Decorator to enable accessibility for a view function"""
    return accessibility_integrator.enhance_view_accessibility(view_function)


def initialize_accessibility() -> None:
    """Initialize accessibility features for the entire application"""
    accessibility_integrator.apply_global_accessibility_enhancements()


# Example usage functions for integration
def demonstrate_accessible_chart():
    """Demonstrate accessible chart creation"""
    
    # Sample data
    data = pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'ai_adoption': [45, 50, 55, 65, 78],
        'genai_adoption': [0, 0, 33, 55, 71]
    })
    
    # Create accessible chart
    fig = go.Figure()
    
    # Add traces with accessible styling
    fig.add_trace(go.Scatter(
        x=data['year'],
        y=data['ai_adoption'],
        mode='lines+markers',
        name='AI Adoption',
        line=dict(width=4),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=data['year'],
        y=data['genai_adoption'],
        mode='lines+markers',
        name='GenAI Adoption',
        line=dict(width=4, dash='dash'),
        marker=dict(size=8)
    ))
    
    # Make chart accessible
    make_chart_accessible(
        fig=fig,
        title="AI Adoption Trends Over Time",
        description="Line chart showing AI adoption percentage from 2020 to 2024, with overall AI adoption rising from 45% to 78%, and GenAI adoption starting in 2022 at 33% and reaching 71% by 2024.",
        data=data
    )


def demonstrate_accessible_metrics():
    """Demonstrate accessible metric displays"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_accessible_metric(
            label="AI Adoption Rate",
            value="78%",
            delta="+13% vs 2023",
            help_text="Percentage of organizations using AI technology"
        )
    
    with col2:
        create_accessible_metric(
            label="Average ROI",
            value="3.8x",
            delta="+0.3x vs 2023",
            help_text="Return on investment from AI initiatives"
        )
    
    with col3:
        create_accessible_metric(
            label="Market Size",
            value="$252B",
            delta="+44% YoY",
            help_text="Global AI market valuation in billions USD"
        )


# Export key functions
__all__ = [
    "AccessibilityIntegrator",
    "accessibility_integrator",
    "make_chart_accessible",
    "create_accessible_metric",
    "create_accessible_section",
    "enable_view_accessibility",
    "initialize_accessibility",
    "demonstrate_accessible_chart",
    "demonstrate_accessible_metrics"
]