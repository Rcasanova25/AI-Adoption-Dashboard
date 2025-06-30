# UI Components Module for AI Adoption Dashboard

A professional, reusable UI component library designed specifically for AI adoption dashboards and strategic decision support applications.

## 🎯 Overview

This module provides advanced UI components with:
- **Executive-friendly visualizations** for leadership presentations
- **Interactive features** and animations
- **Responsive design** principles
- **Accessibility compliance**
- **Professional theming** with consistent styling
- **Modular architecture** for easy integration

## 📦 Installation

The components are part of the AI Adoption Dashboard project. Simply import them in your Streamlit application:

```python
from components.charts import MetricCard, TrendChart
from components.layouts import ExecutiveDashboard
from components.widgets import SmartFilter
from components.themes import apply_custom_theme
```

## 🏗️ Architecture

The module is organized into four main categories:

### 1. Charts (`charts.py`)
Professional chart components for data visualization:

- **MetricCard**: Executive-style metric cards with trends
- **TrendChart**: Professional line charts with annotations
- **ComparisonChart**: Bar/column charts for comparisons
- **ROIChart**: Specialized ROI visualization with business context
- **GeographicChart**: Map-based visualizations
- **IndustryChart**: Industry-specific analysis charts

### 2. Layouts (`layouts.py`)
Layout components for dashboard structure:

- **ExecutiveDashboard**: Leadership-focused dashboard layouts
- **AnalyticalDashboard**: Detailed analysis layouts
- **ResponsiveGrid**: Responsive grid system
- **TabContainer**: Professional tab containers

### 3. Widgets (`widgets.py`)
Interactive widget components:

- **SmartFilter**: Advanced filtering capabilities
- **ActionButton**: Professional action buttons with feedback
- **ProgressIndicator**: Progress and status indicators
- **AlertBox**: Alert and notification boxes
- **DataTable**: Professional data tables

### 4. Themes (`themes.py`)
Theming and styling capabilities:

- **ExecutiveTheme**: Leadership presentation theme
- **AnalystTheme**: Detailed analysis theme
- **apply_custom_theme**: Custom theme application

## 🚀 Quick Start

### Basic Usage

```python
import streamlit as st
from components.themes import apply_custom_theme
from components.charts import MetricCard
from components.layouts import ExecutiveDashboard

# Apply executive theme
apply_custom_theme("executive")

# Create executive dashboard
dashboard = ExecutiveDashboard()

# Render header with metrics
metrics = [
    {"value": "78%", "label": "Market Adoption"},
    {"value": "280x", "label": "Cost Reduction"},
    {"value": "3.2x", "label": "Average ROI"}
]

dashboard.render_header(
    title="AI Adoption Intelligence",
    subtitle="Strategic decision support",
    metrics=metrics
)

# Create metric cards
metric_card = MetricCard()
metric_card.render(
    label="Market Adoption",
    value="78%",
    delta="+23pp vs 2023",
    insight="Competitive table stakes",
    trend="up"
)
```

### Advanced Usage

```python
from components.charts import IndustryChart, ChartConfig
from components.widgets import SmartFilter, AlertBox
from components.layouts import ResponsiveGrid

# Configure chart styling
config = ChartConfig(
    theme="executive",
    height=500,
    title_font_size=16
)

# Create industry analysis chart
industry_chart = IndustryChart(config)
industry_chart.render(
    data=adoption_data,
    sector_column='sector',
    adoption_column='adoption_rate',
    genai_column='genai_adoption',
    roi_column='avg_roi'
)

# Create smart filters
smart_filter = SmartFilter()
selected_sectors = smart_filter.render_multi_select(
    label="Select Sectors",
    options=['Technology', 'Finance', 'Healthcare'],
    key="sector_filter"
)

# Create responsive grid
responsive_grid = ResponsiveGrid()
responsive_grid.render_metric_row(metrics, columns=4, responsive=True)
```

## 🎨 Theming

### Executive Theme
Professional theme designed for leadership presentations:

```python
from components.themes import apply_custom_theme

# Apply executive theme
apply_custom_theme("executive")

# Or with custom colors
apply_custom_theme("executive", {
    "primary_color": "#1e3c72",
    "accent_color": "#3498db"
})
```

### Analyst Theme
Clean theme designed for detailed analysis:

```python
apply_custom_theme("analyst")
```

### Custom Themes
Create your own theme configuration:

```python
from components.themes import create_custom_theme

custom_theme = create_custom_theme(
    name="corporate",
    primary_color="#2c3e50",
    secondary_color="#34495e",
    accent_color="#3498db",
    font_family="'Arial', sans-serif"
)
```

## 📊 Chart Components

### MetricCard
Professional metric cards with trend indicators:

```python
metric_card = MetricCard()
metric_card.render(
    label="Market Adoption",
    value="78%",
    delta="+23pp vs 2023",
    insight="Competitive table stakes",
    trend="up",  # up, down, neutral
    help_text="Business AI adoption rate"
)
```

### TrendChart
Professional trend line charts:

```python
trend_chart = TrendChart()
trend_chart.render(
    data=historical_data,
    x_column='year',
    y_column='adoption_rate',
    title="AI Adoption Trends",
    color="#1f77b4",
    show_points=True,
    annotations=[
        {
            'x': 2022,
            'y': 33,
            'text': 'ChatGPT Launch',
            'showarrow': True
        }
    ]
)
```

### IndustryChart
Specialized industry analysis charts:

```python
industry_chart = IndustryChart()
industry_chart.render(
    data=sector_data,
    sector_column='sector',
    adoption_column='adoption_rate',
    genai_column='genai_adoption',
    roi_column='avg_roi',
    title="Industry AI Adoption Analysis"
)
```

## 🔧 Widget Components

### SmartFilter
Advanced filtering capabilities:

```python
smart_filter = SmartFilter()

# Date range filter
start_date, end_date = smart_filter.render_date_range(
    label="Select Date Range",
    key="date_filter"
)

# Multi-select filter
selected_items = smart_filter.render_multi_select(
    label="Select Items",
    options=['Option 1', 'Option 2', 'Option 3'],
    key="multi_filter"
)

# Slider filter
value_range = smart_filter.render_slider(
    label="Value Range",
    min_value=0,
    max_value=100,
    key="slider_filter",
    default_value=(25, 75)
)
```

### ActionButton
Professional action buttons:

```python
action_button = ActionButton()

def my_action():
    st.success("Action completed!")

action_button.render(
    label="Execute Action",
    action_func=my_action,
    button_type="primary",
    confirm=True,
    confirm_message="Are you sure?"
)
```

### AlertBox
Professional alert boxes:

```python
alert_box = AlertBox()

alert_box.render_success(
    title="Success",
    message="Operation completed successfully"
)

alert_box.render_warning(
    title="Warning",
    message="Please review the data quality"
)

alert_box.render_error(
    title="Error",
    message="An error occurred during processing"
)
```

## 📐 Layout Components

### ExecutiveDashboard
Leadership-focused dashboard layouts:

```python
dashboard = ExecutiveDashboard()

# Render header with metrics
dashboard.render_header(
    title="Strategic Intelligence",
    subtitle="Executive decision support",
    metrics=metrics
)

# Render insight cards
dashboard.render_insight_card(
    title="Competitive Threat",
    content="78% of businesses now use AI.",
    insight_type="warning",
    icon="⚠️"
)
```

### ResponsiveGrid
Responsive grid system:

```python
responsive_grid = ResponsiveGrid()

# Render metric row
responsive_grid.render_metric_row(metrics, columns=4, responsive=True)

# Render card grid
responsive_grid.render_card_grid(cards, columns=3, card_height="300px")
```

### TabContainer
Professional tab containers:

```python
tab_container = TabContainer()

def tab1_content():
    st.write("Content for tab 1")

tabs = [
    {"label": "Overview", "content": tab1_content},
    {"label": "Analysis", "content": "Static content"},
    {"label": "Settings", "content": lambda: st.write("Settings content")}
]

selected_tab = tab_container.render(tabs, default_tab=0, tab_style="executive")
```

## 🎯 Best Practices

### 1. Theme Consistency
Always apply a theme at the beginning of your application:

```python
# Apply theme first
apply_custom_theme("executive")

# Then use components
dashboard = ExecutiveDashboard()
```

### 2. Configuration Objects
Use configuration objects for consistent styling:

```python
config = ChartConfig(
    theme="executive",
    height=500,
    title_font_size=16,
    axis_font_size=12
)

chart = TrendChart(config)
```

### 3. Responsive Design
Use responsive components for better mobile experience:

```python
responsive_grid.render_metric_row(metrics, responsive=True)
```

### 4. Error Handling
Always handle data validation:

```python
if data is not None and not data.empty:
    chart.render(data=data, ...)
else:
    st.warning("No data available")
```

## 🔧 Configuration

### ChartConfig
Configure chart appearance and behavior:

```python
@dataclass
class ChartConfig:
    theme: str = "executive"
    height: int = 500
    width: Optional[int] = None
    show_legend: bool = True
    responsive: bool = True
    animate: bool = True
    color_scheme: str = "viridis"
    font_family: str = "Arial, sans-serif"
    title_font_size: int = 16
    axis_font_size: int = 12
```

### LayoutConfig
Configure layout behavior:

```python
@dataclass
class LayoutConfig:
    theme: str = "executive"
    max_width: int = 1200
    padding: int = 20
    responsive: bool = True
    show_borders: bool = False
    background_color: str = "transparent"
    accent_color: str = "#1f77b4"
```

### WidgetConfig
Configure widget behavior:

```python
@dataclass
class WidgetConfig:
    theme: str = "executive"
    size: str = "medium"  # small, medium, large
    color_scheme: str = "blue"
    animate: bool = True
    responsive: bool = True
    show_help: bool = True
```

## 🧪 Testing

Run the example demo to see all components in action:

```bash
streamlit run components/example_usage.py
```

## 📝 Examples

See `example_usage.py` for comprehensive examples of all components.

## 🤝 Contributing

When contributing to the components module:

1. Follow the existing code style and patterns
2. Add comprehensive docstrings
3. Include type hints
4. Test your components thoroughly
5. Update the example usage file
6. Update this README if adding new features

## 📄 License

This module is part of the AI Adoption Dashboard project.

## 🆘 Support

For issues or questions about the UI components:

1. Check the example usage file
2. Review the component docstrings
3. Test with the demo application
4. Create an issue in the project repository

---

**Version:** 1.0.0  
**Author:** AI Dashboard Team  
**Description:** Professional UI components for strategic AI dashboards 