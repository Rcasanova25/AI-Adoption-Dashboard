"""UI components for the AI Adoption Dashboard.

This module provides reusable UI components with consistent styling.
"""

from .metric_card import render_metric_card
from .theme import ThemeManager

__all__ = ["render_metric_card", "ThemeManager"]