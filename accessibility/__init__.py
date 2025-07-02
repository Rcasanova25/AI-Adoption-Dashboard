"""
Accessibility Module for AI Adoption Dashboard
WCAG 2.1 compliant components and accessibility audit tools
"""

from .accessibility_audit import accessibility_auditor, AccessibilityLevel, ColorContrastAnalyzer
from .accessible_components import (
    AccessibleChart, AccessibleMetric, AccessibleLayout, 
    AccessibleDashboard, AccessibleColorPalette, accessible_dashboard
)

__version__ = "1.0.0"
__all__ = [
    "accessibility_auditor",
    "AccessibilityLevel", 
    "ColorContrastAnalyzer",
    "AccessibleChart",
    "AccessibleMetric", 
    "AccessibleLayout",
    "AccessibleDashboard",
    "AccessibleColorPalette",
    "accessible_dashboard"
]