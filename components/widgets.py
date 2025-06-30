"""
Professional Widget Components for AI Adoption Dashboard

This module provides advanced interactive widgets with:
- Smart filtering capabilities
- Action buttons with feedback
- Progress indicators
- Alert boxes
- Data tables
- Professional styling
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List, Callable, Union
from dataclasses import dataclass
import numpy as np
import time


@dataclass
class WidgetConfig:
    """Configuration for widget styling and behavior"""
    theme: str = "executive"
    size: str = "medium"  # small, medium, large
    color_scheme: str = "blue"
    animate: bool = True
    responsive: bool = True
    show_help: bool = True


class SmartFilter:
    """Advanced filtering widget with multiple filter types"""
    
    def __init__(self):
        self.filters = {}
        
    def add_date_filter(self, 
                       key: str, 
                       label: str, 
                       min_date, 
                       max_date, 
                       default_range: Optional[tuple] = None):
        """Add date range filter"""
        if default_range is None:
            default_range = (min_date, max_date)
            
        date_range = st.date_input(
            label,
            value=default_range,
            min_value=min_date,
            max_value=max_date,
            key=key
        )
        
        self.filters[key] = date_range
        return date_range
    
    def add_multiselect_filter(self,
                              key: str,
                              label: str, 
                              options: List[str],
                              default: Optional[List[str]] = None):
        """Add multiselect filter"""
        if default is None:
            default = options
            
        selected = st.multiselect(
            label,
            options=options,
            default=default,
            key=key
        )
        
        self.filters[key] = selected
        return selected
    
    def add_range_filter(self,
                        key: str,
                        label: str,
                        min_value: float,
                        max_value: float,
                        step: float = 1.0,
                        format_str: str = "%d"):
        """Add numeric range filter"""
        range_values = st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
            step=step,
            format=format_str,
            key=key
        )
        
        self.filters[key] = range_values
        return range_values
    
    def get_filtered_data(self, data: pd.DataFrame, filter_configs: Dict[str, Dict]) -> pd.DataFrame:
        """Apply all filters to dataframe"""
        filtered_data = data.copy()
        
        for filter_key, config in filter_configs.items():
            if filter_key not in self.filters:
                continue
                
            filter_value = self.filters[filter_key]
            column = config.get('column')
            filter_type = config.get('type')
            
            if not column or column not in filtered_data.columns:
                continue
            
            if filter_type == 'date_range' and len(filter_value) == 2:
                start_date, end_date = filter_value
                filtered_data = filtered_data[
                    (pd.to_datetime(filtered_data[column]) >= pd.to_datetime(start_date)) &
                    (pd.to_datetime(filtered_data[column]) <= pd.to_datetime(end_date))
                ]
            
            elif filter_type == 'multiselect':
                filtered_data = filtered_data[filtered_data[column].isin(filter_value)]
            
            elif filter_type == 'range' and len(filter_value) == 2:
                min_val, max_val = filter_value
                filtered_data = filtered_data[
                    (filtered_data[column] >= min_val) & 
                    (filtered_data[column] <= max_val)
                ]
        
        return filtered_data


class ActionButton:
    """Enhanced action button with loading states and callbacks"""
    
    @staticmethod
    def render(label: str,
               callback: Callable,
               button_type: str = "primary",
               loading_text: str = "Processing...",
               success_text: str = "Complete!",
               icon: str = "",
               disabled: bool = False,
               help_text: str = "") -> bool:
        """
        Render action button with enhanced UX
        
        Args:
            label: Button text
            callback: Function to execute on click
            button_type: primary, secondary, success, warning, error
            loading_text: Text to show during processing
            success_text: Text to show on success
            icon: Icon to display (emoji or Unicode)
            disabled: Whether button is disabled
            help_text: Tooltip text
        """
        
        # Create unique key for this button
        button_key = f"action_btn_{label.lower().replace(' ', '_')}"
        
        # Initialize session state for this button
        if f"{button_key}_state" not in st.session_state:
            st.session_state[f"{button_key}_state"] = "ready"
        
        state = st.session_state[f"{button_key}_state"]
        
        # Determine button appearance based on state
        if state == "loading":
            display_label = f"{icon} {loading_text}" if icon else loading_text
            button_disabled = True
        elif state == "success":
            display_label = f"✅ {success_text}"
            button_disabled = True
        else:
            display_label = f"{icon} {label}" if icon else label
            button_disabled = disabled
        
        # Render button with appropriate styling
        button_clicked = st.button(
            display_label,
            key=button_key,
            disabled=button_disabled,
            type=button_type,
            help=help_text,
            use_container_width=True
        )
        
        # Handle button click
        if button_clicked and state == "ready":
            st.session_state[f"{button_key}_state"] = "loading"
            st.rerun()
        
        # Execute callback if in loading state
        if state == "loading":
            try:
                result = callback()
                st.session_state[f"{button_key}_state"] = "success"
                
                # Reset to ready after showing success briefly
                time.sleep(1)
                st.session_state[f"{button_key}_state"] = "ready"
                st.rerun()
                
                return True
                
            except Exception as e:
                st.session_state[f"{button_key}_state"] = "ready"
                st.error(f"Action failed: {str(e)}")
                return False
        
        return False


class ProgressIndicator:
    """Advanced progress indicator with multiple visualization types"""
    
    @staticmethod
    def render_circular(value: float, 
                       max_value: float = 100,
                       title: str = "Progress",
                       color: str = "#1f77b4",
                       size: int = 100):
        """Render circular progress indicator"""
        
        percentage = min(100, (value / max_value) * 100)
        
        # Create SVG circular progress
        svg_html = f"""
        <div style="text-align: center; margin: 1rem 0;">
            <div style="position: relative; display: inline-block;">
                <svg width="{size}" height="{size}" style="transform: rotate(-90deg);">
                    <circle cx="{size//2}" cy="{size//2}" r="{size//2 - 10}" 
                            fill="none" stroke="#e0e0e0" stroke-width="8"/>
                    <circle cx="{size//2}" cy="{size//2}" r="{size//2 - 10}" 
                            fill="none" stroke="{color}" stroke-width="8"
                            stroke-linecap="round"
                            stroke-dasharray="{2 * 3.14159 * (size//2 - 10)}"
                            stroke-dashoffset="{2 * 3.14159 * (size//2 - 10) * (1 - percentage/100)}"
                            style="transition: stroke-dashoffset 0.5s ease;"/>
                </svg>
                <div style="
                    position: absolute; 
                    top: 50%; 
                    left: 50%; 
                    transform: translate(-50%, -50%);
                    font-weight: bold;
                    font-size: {size//8}px;
                    color: {color};
                ">
                    {percentage:.1f}%
                </div>
            </div>
            <div style="margin-top: 0.5rem; font-weight: 500; color: #333;">{title}</div>
            <div style="font-size: 0.9rem; color: #666;">{value} / {max_value}</div>
        </div>
        """
        
        st.markdown(svg_html, unsafe_allow_html=True)
    
    @staticmethod
    def render_linear(value: float,
                     max_value: float = 100,
                     title: str = "Progress",
                     color: str = "#1f77b4",
                     height: int = 20,
                     show_percentage: bool = True):
        """Render linear progress bar"""
        
        percentage = min(100, (value / max_value) * 100)
        
        bar_html = f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 500; color: #333;">{title}</span>
                {f'<span style="color: #666;">{percentage:.1f}%</span>' if show_percentage else ''}
            </div>
            <div style="
                width: 100%; 
                height: {height}px; 
                background-color: #e0e0e0; 
                border-radius: {height//2}px;
                overflow: hidden;
            ">
                <div style="
                    width: {percentage}%; 
                    height: 100%; 
                    background: linear-gradient(90deg, {color} 0%, {color}CC 100%);
                    border-radius: {height//2}px;
                    transition: width 0.5s ease;
                "></div>
            </div>
            <div style="
                display: flex; 
                justify-content: space-between; 
                margin-top: 0.25rem; 
                font-size: 0.8rem; 
                color: #666;
            ">
                <span>{value}</span>
                <span>{max_value}</span>
            </div>
        </div>
        """
        
        st.markdown(bar_html, unsafe_allow_html=True)


class AlertBox:
    """Professional alert/notification system"""
    
    @staticmethod
    def render_alert(message: str,
                    alert_type: str = "info",
                    title: Optional[str] = None,
                    dismissible: bool = False,
                    actions: Optional[List[Dict]] = None):
        """
        Render professional alert box
        
        Args:
            message: Alert message
            alert_type: info, success, warning, error
            title: Optional alert title
            dismissible: Whether alert can be dismissed
            actions: List of action buttons
        """
        
        # Alert styling
        alert_styles = {
            'info': {
                'bg': 'rgba(13, 110, 253, 0.1)',
                'border': '#0d6efd',
                'icon': 'ℹ️',
                'color': '#0d6efd'
            },
            'success': {
                'bg': 'rgba(25, 135, 84, 0.1)', 
                'border': '#198754',
                'icon': '✅',
                'color': '#198754'
            },
            'warning': {
                'bg': 'rgba(255, 193, 7, 0.1)',
                'border': '#ffc107',
                'icon': '⚠️',
                'color': '#856404'
            },
            'error': {
                'bg': 'rgba(220, 53, 69, 0.1)',
                'border': '#dc3545',
                'icon': '❌',
                'color': '#dc3545'
            }
        }
        
        style = alert_styles.get(alert_type, alert_styles['info'])
        
        # Create alert HTML
        alert_html = f"""
        <div style="
            background: {style['bg']};
            border-left: 4px solid {style['border']};
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            position: relative;
        ">
            <div style="display: flex; align-items: flex-start;">
                <div style="margin-right: 0.75rem; font-size: 1.2rem;">
                    {style['icon']}
                </div>
                <div style="flex: 1;">
                    {f'<h4 style="margin: 0 0 0.5rem 0; color: {style["color"]}; font-weight: 600;">{title}</h4>' if title else ''}
                    <div style="color: #333; line-height: 1.5;">
                        {message}
                    </div>
                    {AlertBox._render_actions(actions) if actions else ''}
                </div>
                {AlertBox._render_dismiss_button() if dismissible else ''}
            </div>
        </div>
        """
        
        st.markdown(alert_html, unsafe_allow_html=True)
    
    @staticmethod
    def _render_actions(actions: List[Dict]) -> str:
        """Render action buttons for alert"""
        if not actions:
            return ""
        
        actions_html = '<div style="margin-top: 1rem;">'
        for action in actions:
            label = action.get('label', 'Action')
            style_type = action.get('type', 'secondary')
            
            button_style = "background: #007bff; color: white;" if style_type == 'primary' else "background: #6c757d; color: white;"
            
            actions_html += f'''
            <button style="
                {button_style}
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                margin-right: 0.5rem;
                cursor: pointer;
                font-size: 0.9rem;
            ">{label}</button>
            '''
        
        actions_html += '</div>'
        return actions_html
    
    @staticmethod
    def _render_dismiss_button() -> str:
        """Render dismiss button for alert"""
        return '''
        <button style="
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            color: #666;
            padding: 0.25rem;
        " onclick="this.parentElement.parentElement.style.display='none';">
            ×
        </button>
        '''


class DataTable:
    """Professional data table with advanced features"""
    
    def __init__(self, config: Optional[WidgetConfig] = None):
        self.config = config or WidgetConfig()
    
    def render(self,
               data: pd.DataFrame,
               title: str = "Data Table",
               show_summary: bool = True,
               show_filters: bool = True,
               max_rows: int = 100,
               key: str = None) -> None:
        """
        Render a professional data table
        
        Args:
            data: DataFrame to display
            title: Table title
            show_summary: Whether to show data summary
            show_filters: Whether to show filtering options
            max_rows: Maximum rows to display
            key: Unique key for the widget
        """
        
        if data is None or data.empty:
            st.warning("No data available to display")
            return
        
        st.markdown(f"### {title}")
        
        # Show summary if requested
        if show_summary:
            self._render_summary(data)
        
        # Show filters if requested
        if show_filters:
            self._render_filters(data, key)
        
        # Display data
        if len(data) > max_rows:
            st.info(f"Showing first {max_rows} rows of {len(data)} total rows")
            st.dataframe(data.head(max_rows), use_container_width=True)
        else:
            st.dataframe(data, use_container_width=True)
    
    def _render_summary(self, data: pd.DataFrame) -> None:
        """Render data summary"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows", len(data))
        
        with col2:
            st.metric("Columns", len(data.columns))
        
        with col3:
            memory_kb = data.memory_usage(deep=True).sum() / 1024
            st.metric("Memory", f"{memory_kb:.1f} KB")
        
        with col4:
            missing_count = data.isnull().sum().sum()
            st.metric("Missing Values", missing_count)
    
    def _render_filters(self, data: pd.DataFrame, key: str = None) -> None:
        """Render data filters"""
        
        st.markdown("**Filters:**")
        
        # Column filter
        if len(data.columns) > 1:
            selected_columns = st.multiselect(
                "Select Columns",
                options=data.columns.tolist(),
                default=data.columns.tolist(),
                key=f"{key}_columns" if key else "columns"
            )
            
            if selected_columns:
                data = data[selected_columns]
        
        # Row filter
        if len(data) > 10:
            row_filter = st.slider(
                "Show Rows",
                min_value=1,
                max_value=len(data),
                value=min(50, len(data)),
                key=f"{key}_rows" if key else "rows"
            )
            
            data = data.head(row_filter)
        
        return data 


# Demo function
def demo_widgets():
    """Demo function for widgets"""
    st.title("🎛️ Advanced Widgets Demo")
    
    # Smart Filter Demo
    st.header("Smart Filtering System")
    
    smart_filter = SmartFilter()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        industries = smart_filter.add_multiselect_filter(
            "industries",
            "Select Industries",
            ["Technology", "Finance", "Healthcare", "Manufacturing", "Retail"]
        )
    
    with col2:
        roi_range = smart_filter.add_range_filter(
            "roi_range",
            "ROI Range",
            1.0, 5.0, 0.1, "%.1fx"
        )
    
    with col3:
        adoption_range = smart_filter.add_range_filter(
            "adoption",
            "Adoption Rate %",
            0, 100, 5, "%d%%"
        )
    
    st.write(f"Selected filters: Industries: {industries}, ROI: {roi_range}, Adoption: {adoption_range}")
    
    # Action Button Demo
    st.header("Enhanced Action Buttons")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        def generate_report():
            time.sleep(2)  # Simulate processing
            return "Report generated successfully!"
        
        ActionButton.render(
            label="Generate Report",
            callback=generate_report,
            button_type="primary",
            icon="📊",
            help_text="Generate comprehensive AI analysis report"
        )
    
    with col2:
        def export_data():
            time.sleep(1)
            return "Data exported!"
        
        ActionButton.render(
            label="Export Data",
            callback=export_data,
            button_type="secondary",
            icon="📥"
        )
    
    with col3:
        ActionButton.render(
            label="Disabled Action",
            callback=lambda: None,
            disabled=True,
            icon="🔒"
        )
    
    # Progress Indicators Demo
    st.header("Progress Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Circular Progress")
        ProgressIndicator.render_circular(
            value=75,
            max_value=100,
            title="AI Implementation",
            color="#28a745"
        )
    
    with col2:
        st.subheader("Linear Progress")
        ProgressIndicator.render_linear(
            value=68,
            max_value=100,
            title="Market Penetration",
            color="#007bff"
        )
    
    # Alert Box Demo
    st.header("Professional Alert System")
    
    AlertBox.render_alert(
        title="Success",
        message="Your AI strategy assessment has been completed successfully.",
        alert_type="success",
        dismissible=True
    )
    
    AlertBox.render_alert(
        title="Important Update",
        message="New AI regulations require compliance review by Q3 2025.",
        alert_type="warning",
        actions=[
            {"label": "Review Now", "type": "primary"},
            {"label": "Remind Later", "type": "secondary"}
        ]
    )


if __name__ == "__main__":
    demo_widgets() 