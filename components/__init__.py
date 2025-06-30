# components/__init__.py - UI Components Module
"""
Advanced UI Components for AI Adoption Dashboard

This module provides reusable, professional UI components with:
- Consistent styling and theming
- Interactive features and animations
- Responsive design principles
- Accessibility compliance
- Professional executive presentation
"""

from .charts import (
    MetricCard,
    TrendChart, 
    ComparisonChart,
    ROIChart
)

from .layouts import (
    ExecutiveDashboard,
    AnalyticalDashboard, 
    ResponsiveGrid,
    TabContainer
)

from .widgets import (
    SmartFilter,
    ActionButton,
    ProgressIndicator,
    AlertBox,
    DataTable
)

from .themes import (
    ExecutiveTheme,
    AnalystTheme,
    apply_custom_theme
)

__all__ = [
    # Charts
    'MetricCard',
    'TrendChart', 
    'ComparisonChart',
    'ROIChart',
    
    # Layouts
    'ExecutiveDashboard',
    'AnalyticalDashboard',
    'ResponsiveGrid', 
    'TabContainer',
    
    # Widgets
    'SmartFilter',
    'ActionButton',
    'ProgressIndicator',
    'AlertBox',
    'DataTable',
    
    # Themes
    'ExecutiveTheme',
    'AnalystTheme',
    'apply_custom_theme'
]

# Version and metadata
__version__ = "1.0.0"
__author__ = "AI Dashboard Team"
__description__ = "Professional UI components for strategic AI dashboards" 