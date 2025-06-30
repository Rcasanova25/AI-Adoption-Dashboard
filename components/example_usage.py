"""
Example Usage of UI Components for AI Adoption Dashboard

This file demonstrates how to use the professional UI components
in your Streamlit dashboard applications.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import the UI components
from components.charts import (
    MetricCard, TrendChart, ComparisonChart, ROIChart, 
    GeographicChart, IndustryChart, ChartConfig
)
from components.layouts import (
    ExecutiveDashboard, AnalyticalDashboard, ResponsiveGrid, TabContainer
)
from components.widgets import (
    SmartFilter, ActionButton, ProgressIndicator, AlertBox, DataTable
)
from components.themes import (
    ExecutiveTheme, AnalystTheme, apply_custom_theme
)


def demo_executive_dashboard():
    """Demonstrate executive dashboard components"""
    
    st.title("🎯 Executive Dashboard Demo")
    
    # Apply executive theme
    apply_custom_theme("executive")
    
    # Create executive dashboard
    exec_dashboard = ExecutiveDashboard()
    
    # Render header with metrics
    metrics = [
        {"value": "78%", "label": "Market Adoption"},
        {"value": "280x", "label": "Cost Reduction"},
        {"value": "3.2x", "label": "Average ROI"},
        {"value": "$252B", "label": "Global Investment"}
    ]
    
    exec_dashboard.render_header(
        title="AI Adoption Strategic Intelligence",
        subtitle="Executive decision support for AI investment",
        metrics=metrics
    )
    
    # Render metric grid
    exec_dashboard.render_metric_grid(metrics, columns=4)
    
    # Render insight cards
    exec_dashboard.render_insight_card(
        title="Competitive Threat",
        content="78% of businesses now use AI. Non-adopters becoming minority position.",
        insight_type="warning",
        icon="⚠️"
    )
    
    exec_dashboard.render_insight_card(
        title="Economic Opportunity", 
        content="280x cost reduction enables mass deployment with proven 3.2x ROI.",
        insight_type="success",
        icon="💰"
    )


def demo_analytical_dashboard():
    """Demonstrate analytical dashboard components"""
    
    st.title("📊 Analytical Dashboard Demo")
    
    # Apply analyst theme
    apply_custom_theme("analyst")
    
    # Create analytical dashboard
    analyst_dashboard = AnalyticalDashboard()
    
    # Create sample data
    dates = pd.date_range('2020-01-01', '2025-01-01', freq='M')
    data = pd.DataFrame({
        'date': dates,
        'ai_adoption': np.random.normal(50, 10, len(dates)).cumsum(),
        'genai_adoption': np.random.normal(20, 5, len(dates)).cumsum(),
        'investment': np.random.normal(100, 20, len(dates)).cumsum()
    })
    
    # Render analysis section
    analyst_dashboard.render_analysis_section(
        title="AI Adoption Trends Analysis",
        description="Comprehensive analysis of AI adoption patterns and investment trends"
    )
    
    # Render data table
    analyst_dashboard.render_data_table(
        data=data.head(20),
        title="Sample Data",
        show_summary=True,
        max_rows=20
    )


def demo_charts():
    """Demonstrate chart components"""
    
    st.title("📈 Chart Components Demo")
    
    # Create sample data
    sectors = ['Technology', 'Financial Services', 'Healthcare', 'Manufacturing', 
               'Retail & E-commerce', 'Education', 'Energy & Utilities', 'Government']
    adoption_data = pd.DataFrame({
        'sector': sectors,
        'adoption_rate': [92, 85, 78, 75, 72, 65, 58, 52],
        'genai_adoption': [88, 78, 65, 58, 70, 62, 45, 38],
        'avg_roi': [4.2, 3.8, 3.2, 3.5, 3.0, 2.5, 2.8, 2.2]
    })
    
    # Create chart config
    config = ChartConfig(
        theme="executive",
        height=400,
        title_font_size=14,
        axis_font_size=10
    )
    
    # Demo MetricCard
    st.subheader("Metric Cards")
    metric_card = MetricCard(config)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card.render("Market Adoption", "78%", "+23pp vs 2023", "Competitive table stakes", "up")
    with col2:
        metric_card.render("Cost Reduction", "280x", "Since Nov 2022", "Barriers eliminated", "up")
    with col3:
        metric_card.render("ROI Range", "2.5-4.2x", "Proven returns", "Strong business case", "neutral")
    with col4:
        metric_card.render("Time to Impact", "12-18 months", "Typical payback", "Fast value creation", "neutral")
    
    # Demo IndustryChart
    st.subheader("Industry Analysis Chart")
    industry_chart = IndustryChart(config)
    industry_chart.render(
        data=adoption_data,
        sector_column='sector',
        adoption_column='adoption_rate',
        genai_column='genai_adoption',
        roi_column='avg_roi',
        title="AI Adoption by Industry Sector"
    )
    
    # Demo ROIChart
    st.subheader("ROI Analysis Chart")
    roi_chart = ROIChart(config)
    roi_chart.render(
        data=adoption_data,
        sector_column='sector',
        roi_column='avg_roi',
        adoption_column='adoption_rate',
        title="ROI vs Adoption Rate Analysis"
    )


def demo_widgets():
    """Demonstrate widget components"""
    
    st.title("🔧 Widget Components Demo")
    
    # Create widgets
    smart_filter = SmartFilter()
    action_button = ActionButton()
    progress_indicator = ProgressIndicator()
    alert_box = AlertBox()
    data_table = DataTable()
    
    # Demo SmartFilter
    st.subheader("Smart Filters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date range filter
        start_date, end_date = smart_filter.render_date_range(
            label="Select Date Range",
            key="demo_date_range",
            help_text="Choose the analysis period"
        )
        
        # Multi-select filter
        selected_sectors = smart_filter.render_multi_select(
            label="Select Sectors",
            options=['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail'],
            key="demo_sectors",
            default=['Technology', 'Finance'],
            help_text="Choose sectors to analyze"
        )
    
    with col2:
        # Slider filter
        roi_range = smart_filter.render_slider(
            label="ROI Range",
            min_value=1.0,
            max_value=5.0,
            key="demo_roi",
            default_value=(2.0, 4.0),
            step=0.1,
            help_text="Select ROI range"
        )
        
        # Search box
        search_query = smart_filter.render_search_box(
            label="Search Companies",
            key="demo_search",
            placeholder="Enter company name...",
            help_text="Search for specific companies"
        )
    
    # Demo ActionButton
    st.subheader("Action Buttons")
    
    def sample_action():
        st.success("Action executed successfully!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        action_button.render(
            label="Execute Analysis",
            action_func=sample_action,
            button_type="primary",
            help_text="Run the analysis"
        )
    
    with col2:
        action_button.render(
            label="Delete Data",
            action_func=sample_action,
            button_type="secondary",
            confirm=True,
            confirm_message="Are you sure you want to delete this data?"
        )
    
    # Demo ProgressIndicator
    st.subheader("Progress Indicators")
    
    progress_indicator.render_progress_bar(75, 100, "Analysis Progress")
    progress_indicator.render_status_indicator("Data loaded successfully", "success")
    
    # Demo AlertBox
    st.subheader("Alert Boxes")
    
    alert_box.render_success(
        title="Analysis Complete",
        message="The AI adoption analysis has been completed successfully."
    )
    
    alert_box.render_warning(
        title="Data Quality Warning",
        message="Some data points may have quality issues. Please review."
    )
    
    # Demo DataTable
    st.subheader("Data Table")
    
    sample_data = pd.DataFrame({
        'Company': ['Tech Corp', 'Finance Inc', 'Health Systems'],
        'Adoption Rate': [92, 85, 78],
        'ROI': [4.2, 3.8, 3.2],
        'Investment': [1000000, 750000, 500000]
    })
    
    data_table.render(
        data=sample_data,
        title="Company Analysis",
        show_summary=True,
        show_filters=True,
        max_rows=10
    )


def demo_layouts():
    """Demonstrate layout components"""
    
    st.title("📐 Layout Components Demo")
    
    # Demo ResponsiveGrid
    st.subheader("Responsive Grid")
    
    responsive_grid = ResponsiveGrid()
    
    # Sample metrics
    metrics = [
        {"value": "78%", "label": "Market Adoption"},
        {"value": "280x", "label": "Cost Reduction"},
        {"value": "3.2x", "label": "Average ROI"},
        {"value": "$252B", "label": "Global Investment"}
    ]
    
    responsive_grid.render_metric_row(metrics, columns=4, responsive=True)
    
    # Sample cards
    cards = [
        {
            "title": "Strategic Intelligence",
            "content": "Comprehensive analysis of AI adoption trends and competitive dynamics."
        },
        {
            "title": "Investment Case",
            "content": "Detailed ROI analysis and business case development for AI investments."
        },
        {
            "title": "Risk Assessment",
            "content": "Evaluation of implementation risks and mitigation strategies."
        }
    ]
    
    responsive_grid.render_card_grid(cards, columns=3, card_height="200px")
    
    # Demo TabContainer
    st.subheader("Tab Container")
    
    tab_container = TabContainer()
    
    def tab1_content():
        st.write("This is the content for tab 1")
        st.write("You can put any Streamlit components here")
    
    def tab2_content():
        st.write("This is the content for tab 2")
        st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C']))
    
    tabs = [
        {"label": "Overview", "content": tab1_content},
        {"label": "Analysis", "content": tab2_content},
        {"label": "About", "content": "This is a static content tab."}
    ]
    
    selected_tab = tab_container.render(tabs, default_tab=0, tab_style="executive")
    st.write(f"Selected tab: {selected_tab}")


def main():
    """Main demo function"""
    
    st.set_page_config(
        page_title="UI Components Demo",
        page_icon="🎨",
        layout="wide"
    )
    
    # Sidebar navigation
    st.sidebar.title("🎨 UI Components Demo")
    
    demo_option = st.sidebar.selectbox(
        "Choose Demo",
        [
            "Executive Dashboard",
            "Analytical Dashboard", 
            "Charts",
            "Widgets",
            "Layouts"
        ]
    )
    
    # Run selected demo
    if demo_option == "Executive Dashboard":
        demo_executive_dashboard()
    elif demo_option == "Analytical Dashboard":
        demo_analytical_dashboard()
    elif demo_option == "Charts":
        demo_charts()
    elif demo_option == "Widgets":
        demo_widgets()
    elif demo_option == "Layouts":
        demo_layouts()


if __name__ == "__main__":
    main() 