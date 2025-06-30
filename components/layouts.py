"""
Professional Layout Components for AI Adoption Dashboard

This module provides advanced layout components with:
- Executive dashboard layouts
- Responsive grid systems
- Tab containers
- Professional theming
- Accessibility features
"""

import streamlit as st
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
import pandas as pd
from enum import Enum


@dataclass
class LayoutConfig:
    """Configuration for layout styling and behavior"""
    theme: str = "executive"
    max_width: int = 1200
    padding: int = 20
    responsive: bool = True
    show_borders: bool = False
    background_color: str = "transparent"
    accent_color: str = "#1f77b4"


class LayoutType(Enum):
    EXECUTIVE = "executive"
    ANALYTICAL = "analytical"
    PRESENTATION = "presentation"


@dataclass 
class GridConfig:
    """Configuration for responsive grid layouts"""
    columns: int
    gap: str = "1rem"
    min_column_width: str = "300px"
    max_width: str = "1200px"


class ExecutiveDashboard:
    """Professional executive dashboard layout"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
    
    def render_header(self, title: str, subtitle: Optional[str] = None, 
                     metrics: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Render executive dashboard header with metrics
        
        Args:
            title: Dashboard title
            subtitle: Optional subtitle
            metrics: List of metric dictionaries
        """
        
        # Apply executive styling
        st.markdown(f"""
        <style>
        .exec-header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            color: white;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }}
        
        .exec-title {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: white;
        }}
        
        .exec-subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }}
        
        .exec-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .exec-metric {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        
        .exec-metric-value {{
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 0.25rem;
        }}
        
        .exec-metric-label {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Render header
        header_html = f"""
        <div class="exec-header">
            <h1 class="exec-title">{title}</h1>
            {f'<p class="exec-subtitle">{subtitle}</p>' if subtitle else ''}
        """
        
        # Add metrics if provided
        if metrics:
            header_html += '<div class="exec-metrics">'
            for metric in metrics:
                header_html += f"""
                <div class="exec-metric">
                    <div class="exec-metric-value">{metric.get('value', 'N/A')}</div>
                    <div class="exec-metric-label">{metric.get('label', '')}</div>
                </div>
                """
            header_html += '</div>'
        
        header_html += '</div>'
        
        st.markdown(header_html, unsafe_allow_html=True)
    
    def render_metric_grid(self, metrics: List[Dict[str, Any]], columns: int = 4) -> None:
        """
        Render a grid of executive metrics
        
        Args:
            metrics: List of metric dictionaries
            columns: Number of columns in grid
        """
        
        if not metrics:
            return
        
        cols = st.columns(columns)
        
        for i, metric in enumerate(metrics):
            with cols[i % columns]:
                st.metric(
                    label=metric.get('label', ''),
                    value=metric.get('value', ''),
                    delta=metric.get('delta', None),
                    help=metric.get('help', None)
                )
    
    def render_insight_card(self, title: str, content: str, 
                          insight_type: str = "info", icon: str = "💡") -> None:
        """
        Render an executive insight card
        
        Args:
            title: Card title
            content: Card content
            insight_type: Type of insight (info, warning, success, error)
            icon: Icon to display
        """
        
        # Define insight styles
        insight_styles = {
            "info": {
                "bg": "rgba(52, 152, 219, 0.1)",
                "border": "#3498db",
                "icon": "💡"
            },
            "warning": {
                "bg": "rgba(243, 156, 18, 0.1)",
                "border": "#f39c12",
                "icon": "⚠️"
            },
            "success": {
                "bg": "rgba(46, 204, 113, 0.1)",
                "border": "#2ecc71",
                "icon": "✅"
            },
            "error": {
                "bg": "rgba(231, 76, 60, 0.1)",
                "border": "#e74c3c",
                "icon": "❌"
            }
        }
        
        style = insight_styles.get(insight_type, insight_styles["info"])
        
        card_html = f"""
        <div style="
            background: {style['bg']};
            border-left: 4px solid {style['border']};
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem;">{icon}</span>
                <h3 style="margin: 0; color: #2c3e50; font-weight: 600;">{title}</h3>
            </div>
            <p style="margin: 0; line-height: 1.6; color: #34495e;">{content}</p>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)


class AnalyticalDashboard:
    """Professional analytical dashboard layout"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
    
    def render_analysis_section(self, title: str, description: Optional[str] = None,
                               filters: Optional[List[Callable]] = None) -> None:
        """
        Render an analysis section with filters
        
        Args:
            title: Section title
            description: Optional description
            filters: List of filter functions
        """
        
        st.markdown(f"## {title}")
        
        if description:
            st.markdown(f"*{description}*")
        
        # Render filters if provided
        if filters:
            st.markdown("### Filters")
            filter_cols = st.columns(len(filters))
            
            for i, filter_func in enumerate(filters):
                with filter_cols[i]:
                    filter_func()
        
        st.markdown("---")
    
    def render_data_table(self, data: pd.DataFrame, title: str,
                         show_summary: bool = True, max_rows: int = 100) -> None:
        """
        Render a professional data table
        
        Args:
            data: DataFrame to display
            title: Table title
            show_summary: Whether to show data summary
            max_rows: Maximum rows to display
        """
        
        st.markdown(f"### {title}")
        
        if show_summary:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", len(data))
            with col2:
                st.metric("Columns", len(data.columns))
            with col3:
                st.metric("Memory", f"{data.memory_usage(deep=True).sum() / 1024:.1f} KB")
            with col4:
                st.metric("Missing Values", data.isnull().sum().sum())
        
        # Display data
        if len(data) > max_rows:
            st.info(f"Showing first {max_rows} rows of {len(data)} total rows")
            st.dataframe(data.head(max_rows), use_container_width=True)
        else:
            st.dataframe(data, use_container_width=True)
    
    def render_chart_section(self, title: str, chart_func: Callable, 
                           description: Optional[str] = None) -> None:
        """
        Render a chart section
        
        Args:
            title: Section title
            chart_func: Function that renders the chart
            description: Optional description
        """
        
        st.markdown(f"### {title}")
        
        if description:
            st.markdown(f"*{description}*")
        
        # Render chart
        chart_func()
        
        st.markdown("---")


class ResponsiveGrid:
    """Advanced responsive grid system"""
    
    def __init__(self, config: GridConfig):
        self.config = config
        
    def create_grid(self, items: List[Callable], titles: Optional[List[str]] = None):
        """Create a responsive grid of components"""
        
        # Apply custom CSS for grid
        st.markdown(f"""
        <style>
        .responsive-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax({self.config.min_column_width}, 1fr));
            gap: {self.config.gap};
            max-width: {self.config.max_width};
            margin: 0 auto;
            padding: 1rem;
        }}
        
        .grid-item {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .grid-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Create Streamlit columns for the grid
        num_cols = min(self.config.columns, len(items))
        cols = st.columns(num_cols)
        
        # Distribute items across columns
        for i, item in enumerate(items):
            with cols[i % num_cols]:
                if titles and i < len(titles):
                    st.subheader(titles[i])
                
                # Execute the component function
                if callable(item):
                    item()
                else:
                    st.write(item)


class TabContainer:
    """Professional tab container with executive styling"""
    
    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
    
    def render(self, tabs: List[Dict[str, Any]], 
               default_tab: int = 0, 
               tab_style: str = "executive") -> str:
        """
        Render a professional tab container
        
        Args:
            tabs: List of tab dictionaries with 'label' and 'content' keys
            default_tab: Index of default tab
            tab_style: Style of tabs (executive, analytical, simple)
            
        Returns:
            Selected tab label
        """
        
        if not tabs:
            return ""
        
        # Apply tab styling
        if tab_style == "executive":
            st.markdown("""
            <style>
            .exec-tabs {
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                border-radius: 8px;
                padding: 0.5rem;
                margin: 1rem 0;
            }
            
            .exec-tab {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 6px;
                margin-right: 0.5rem;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .exec-tab:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            .exec-tab.active {
                background: white;
                color: #2c3e50;
                font-weight: 600;
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Create tabs using Streamlit
        tab_labels = [tab['label'] for tab in tabs]
        selected_tab = st.tabs(tab_labels)
        
        # Render content for each tab
        for i, (tab, tab_container) in enumerate(zip(tabs, selected_tab)):
            with tab_container:
                if callable(tab['content']):
                    tab['content']()
                else:
                    st.markdown(tab['content'])
        
        return tab_labels[default_tab]
    
    def render_sidebar_tabs(self, tabs: List[Dict[str, Any]], 
                           default_tab: int = 0) -> str:
        """
        Render tabs in the sidebar
        
        Args:
            tabs: List of tab dictionaries
            default_tab: Index of default tab
            
        Returns:
            Selected tab label
        """
        
        if not tabs:
            return ""
        
        st.sidebar.markdown("### Navigation")
        
        tab_labels = [tab['label'] for tab in tabs]
        selected_tab = st.sidebar.selectbox(
            "Select View",
            tab_labels,
            index=default_tab
        )
        
        # Render content for selected tab
        for tab in tabs:
            if tab['label'] == selected_tab:
                if callable(tab['content']):
                    tab['content']()
                else:
                    st.markdown(tab['content'])
                break
        
        return selected_tab


# Demo function
def demo_layouts():
    """Demo function for layouts"""
    st.title("🎛️ Advanced Layouts Demo")
    
    # Executive Dashboard Demo
    st.header("Executive Dashboard Layout")
    
    exec_dashboard = ExecutiveDashboard()
    exec_dashboard.render_header(
        title="AI Strategic Dashboard",
        subtitle="Executive Intelligence Center"
    )
    
    # KPI Section
    kpis = [
        {"label": "Market Adoption", "value": "78%", "delta": "+23pp YoY"},
        {"label": "ROI Average", "value": "3.2x", "delta": "+0.4x vs target"},
        {"label": "Investment", "value": "$252B", "delta": "+44% YoY"},
        {"label": "Risk Level", "value": "Medium", "delta": "Stable"}
    ]
    
    exec_dashboard.render_metric_grid(kpis, columns=4)
    
    # Insights Section
    st.markdown("### 🧠 Strategic Insights")
    
    exec_dashboard.render_insight_card(
        title="Market Opportunity",
        content="AI adoption has reached majority threshold with 78% business adoption. Accelerate competitive positioning initiatives.",
        insight_type="success",
        icon="📈"
    )
    
    exec_dashboard.render_insight_card(
        title="Talent Gap Risk",
        content="68% of organizations cite talent shortage as primary barrier. Prioritize AI talent development and retention programs.",
        insight_type="warning",
        icon="⚠️"
    )


if __name__ == "__main__":
    demo_layouts() 