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

# Cross-persona comparison components
try:
    from .persona_comparison import (
        PersonaType,
        PersonaComparisonFramework,
        PersonaComparisonChart,
        PersonaInsightGenerator
    )
    from .persona_navigation import (
        PersonaNavigationInterface,
        PersonaComparisonNavigation
    )
    from .integrated_comparison_view import (
        IntegratedComparisonView
    )
    PERSONA_COMPARISON_AVAILABLE = True
except ImportError:
    PERSONA_COMPARISON_AVAILABLE = False

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

# Add persona comparison components to __all__ if available
if PERSONA_COMPARISON_AVAILABLE:
    __all__.extend([
        'PersonaType',
        'PersonaComparisonFramework', 
        'PersonaComparisonChart',
        'PersonaInsightGenerator',
        'PersonaNavigationInterface',
        'PersonaComparisonNavigation',
        'IntegratedComparisonView'
    ])

# Version and metadata
__version__ = "1.0.0"
__author__ = "AI Dashboard Team"
__description__ = "Professional UI components for strategic AI dashboards"

"""
Components module for Dash AI Adoption Dashboard
Contains reusable UI components
"""

from .charts import *
from .metrics import *
from .tables import *

__all__ = [
    # Chart components
    'create_adoption_trends_chart',
    'create_sector_comparison_chart',
    'create_roi_analysis_chart',
    'create_productivity_trends_chart',
    'create_geographic_chart',
    
    # Metric components
    'create_metric_card',
    'create_metric_row',
    
    # Table components
    'create_data_table',
    'create_summary_table'
] 