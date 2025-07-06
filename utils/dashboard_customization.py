"""Dashboard customization module for AI Adoption Dashboard.

This module provides functionality for users to customize their dashboard
experience with themes, layouts, and saved views.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid


logger = logging.getLogger(__name__)


class ThemeType(Enum):
    """Available dashboard themes."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    COLORBLIND_SAFE = "colorblind_safe"
    CUSTOM = "custom"


class LayoutType(Enum):
    """Dashboard layout options."""
    GRID = "grid"
    SINGLE_COLUMN = "single_column"
    TWO_COLUMN = "two_column"
    DASHBOARD = "dashboard"
    REPORT = "report"


class WidgetType(Enum):
    """Available widget types."""
    CHART = "chart"
    METRIC = "metric"
    TABLE = "table"
    TEXT = "text"
    FILTER = "filter"
    CALCULATOR = "calculator"


@dataclass
class ColorScheme:
    """Color scheme for themes."""
    primary: str = "#1E88E5"
    secondary: str = "#424242"
    success: str = "#4CAF50"
    warning: str = "#FF9800"
    error: str = "#F44336"
    background: str = "#FFFFFF"
    surface: str = "#F5F5F5"
    text_primary: str = "#212121"
    text_secondary: str = "#757575"
    border: str = "#E0E0E0"
    
    def to_css_variables(self) -> str:
        """Convert to CSS variables."""
        css_vars = []
        for key, value in asdict(self).items():
            css_key = key.replace('_', '-')
            css_vars.append(f"--color-{css_key}: {value};")
        return "\n".join(css_vars)


@dataclass
class Theme:
    """Dashboard theme configuration."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Custom Theme"
    type: ThemeType = ThemeType.CUSTOM
    colors: ColorScheme = field(default_factory=ColorScheme)
    font_family: str = "Arial, sans-serif"
    font_size_base: int = 14
    border_radius: int = 4
    spacing_unit: int = 8
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def get_default_themes(cls) -> Dict[str, 'Theme']:
        """Get predefined themes."""
        return {
            "light": cls(
                id="theme-light",
                name="Light",
                type=ThemeType.LIGHT,
                colors=ColorScheme()
            ),
            "dark": cls(
                id="theme-dark",
                name="Dark",
                type=ThemeType.DARK,
                colors=ColorScheme(
                    primary="#2196F3",
                    secondary="#B0BEC5",
                    background="#121212",
                    surface="#1E1E1E",
                    text_primary="#FFFFFF",
                    text_secondary="#B3B3B3",
                    border="#333333"
                )
            ),
            "high_contrast": cls(
                id="theme-high-contrast",
                name="High Contrast",
                type=ThemeType.HIGH_CONTRAST,
                colors=ColorScheme(
                    primary="#0000FF",
                    secondary="#000000",
                    background="#FFFFFF",
                    surface="#FFFFFF",
                    text_primary="#000000",
                    text_secondary="#000000",
                    border="#000000"
                )
            ),
            "colorblind_safe": cls(
                id="theme-colorblind",
                name="Colorblind Safe",
                type=ThemeType.COLORBLIND_SAFE,
                colors=ColorScheme(
                    primary="#0173B2",
                    secondary="#CC79A7",
                    success="#009E73",
                    warning="#E69F00",
                    error="#D55E00"
                )
            )
        }


@dataclass
class Widget:
    """Dashboard widget configuration."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: WidgetType = WidgetType.CHART
    title: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    position: Dict[str, int] = field(default_factory=lambda: {"x": 0, "y": 0, "w": 4, "h": 3})
    data_source: Optional[str] = None
    refresh_interval: Optional[int] = None  # seconds
    visible: bool = True
    
    def validate_position(self, max_cols: int = 12) -> bool:
        """Validate widget position."""
        pos = self.position
        return (
            0 <= pos.get("x", 0) < max_cols and
            0 <= pos.get("y", 0) and
            1 <= pos.get("w", 1) <= max_cols and
            1 <= pos.get("h", 1) and
            pos.get("x", 0) + pos.get("w", 1) <= max_cols
        )


@dataclass
class Layout:
    """Dashboard layout configuration."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Custom Layout"
    type: LayoutType = LayoutType.DASHBOARD
    widgets: List[Widget] = field(default_factory=list)
    columns: int = 12
    row_height: int = 80
    spacing: int = 10
    responsive_breakpoints: Dict[str, int] = field(
        default_factory=lambda: {"lg": 1200, "md": 996, "sm": 768, "xs": 480}
    )
    
    def add_widget(self, widget: Widget) -> bool:
        """Add widget to layout."""
        if widget.validate_position(self.columns):
            self.widgets.append(widget)
            return True
        return False
    
    def remove_widget(self, widget_id: str) -> bool:
        """Remove widget from layout."""
        initial_count = len(self.widgets)
        self.widgets = [w for w in self.widgets if w.id != widget_id]
        return len(self.widgets) < initial_count
    
    def get_widget(self, widget_id: str) -> Optional[Widget]:
        """Get widget by ID."""
        for widget in self.widgets:
            if widget.id == widget_id:
                return widget
        return None
    
    def optimize_layout(self):
        """Optimize widget positions to minimize empty space."""
        # Sort widgets by position
        self.widgets.sort(key=lambda w: (w.position["y"], w.position["x"]))
        
        # Compact vertically
        for i, widget in enumerate(self.widgets):
            if i == 0:
                widget.position["y"] = 0
            else:
                # Find the lowest available position
                min_y = 0
                for prev_widget in self.widgets[:i]:
                    if (prev_widget.position["x"] < widget.position["x"] + widget.position["w"] and
                        widget.position["x"] < prev_widget.position["x"] + prev_widget.position["w"]):
                        min_y = max(min_y, prev_widget.position["y"] + prev_widget.position["h"])
                widget.position["y"] = min_y


@dataclass
class SavedView:
    """Saved dashboard view configuration."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Saved View"
    description: str = ""
    layout_id: str = ""
    theme_id: str = ""
    filters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_default: bool = False
    is_public: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class UserPreferences:
    """User dashboard preferences."""
    user_id: str
    default_theme_id: str = "theme-light"
    default_layout_id: Optional[str] = None
    saved_views: List[SavedView] = field(default_factory=list)
    custom_themes: List[Theme] = field(default_factory=list)
    custom_layouts: List[Layout] = field(default_factory=list)
    favorite_widgets: List[str] = field(default_factory=list)
    recent_views: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def add_saved_view(self, view: SavedView):
        """Add a saved view."""
        # Limit recent views
        if view.id in self.recent_views:
            self.recent_views.remove(view.id)
        self.recent_views.insert(0, view.id)
        self.recent_views = self.recent_views[:10]
        
        # Add to saved views
        self.saved_views.append(view)
    
    def get_saved_view(self, view_id: str) -> Optional[SavedView]:
        """Get saved view by ID."""
        for view in self.saved_views:
            if view.id == view_id:
                return view
        return None
    
    def delete_saved_view(self, view_id: str) -> bool:
        """Delete a saved view."""
        initial_count = len(self.saved_views)
        self.saved_views = [v for v in self.saved_views if v.id != view_id]
        return len(self.saved_views) < initial_count


class DashboardCustomizer:
    """Main dashboard customization manager."""
    
    def __init__(self, storage_path: str = "customizations"):
        """Initialize customizer."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Cache
        self._preferences_cache: Dict[str, UserPreferences] = {}
        self._themes_cache: Dict[str, Theme] = Theme.get_default_themes()
        self._layouts_cache: Dict[str, Layout] = {}
        
        # Load default layouts
        self._load_default_layouts()
    
    def _load_default_layouts(self):
        """Load default layout configurations."""
        # Financial Overview Layout
        financial_layout = Layout(
            id="layout-financial",
            name="Financial Overview",
            type=LayoutType.DASHBOARD,
            widgets=[
                Widget(
                    id="w-npv",
                    type=WidgetType.METRIC,
                    title="Net Present Value",
                    position={"x": 0, "y": 0, "w": 3, "h": 2},
                    data_source="npv_calculation"
                ),
                Widget(
                    id="w-irr",
                    type=WidgetType.METRIC,
                    title="Internal Rate of Return",
                    position={"x": 3, "y": 0, "w": 3, "h": 2},
                    data_source="irr_calculation"
                ),
                Widget(
                    id="w-payback",
                    type=WidgetType.METRIC,
                    title="Payback Period",
                    position={"x": 6, "y": 0, "w": 3, "h": 2},
                    data_source="payback_calculation"
                ),
                Widget(
                    id="w-roi",
                    type=WidgetType.METRIC,
                    title="Return on Investment",
                    position={"x": 9, "y": 0, "w": 3, "h": 2},
                    data_source="roi_calculation"
                ),
                Widget(
                    id="w-cash-flow-chart",
                    type=WidgetType.CHART,
                    title="Cash Flow Projection",
                    position={"x": 0, "y": 2, "w": 6, "h": 4},
                    config={"chart_type": "line", "show_grid": True}
                ),
                Widget(
                    id="w-sensitivity",
                    type=WidgetType.CHART,
                    title="Sensitivity Analysis",
                    position={"x": 6, "y": 2, "w": 6, "h": 4},
                    config={"chart_type": "tornado"}
                )
            ]
        )
        self._layouts_cache["layout-financial"] = financial_layout
        
        # Executive Dashboard Layout
        executive_layout = Layout(
            id="layout-executive",
            name="Executive Dashboard",
            type=LayoutType.DASHBOARD,
            widgets=[
                Widget(
                    id="w-summary",
                    type=WidgetType.TEXT,
                    title="Executive Summary",
                    position={"x": 0, "y": 0, "w": 12, "h": 2},
                    config={"template": "executive_summary"}
                ),
                Widget(
                    id="w-key-metrics",
                    type=WidgetType.TABLE,
                    title="Key Metrics",
                    position={"x": 0, "y": 2, "w": 4, "h": 3},
                    data_source="key_metrics"
                ),
                Widget(
                    id="w-roi-gauge",
                    type=WidgetType.CHART,
                    title="ROI Performance",
                    position={"x": 4, "y": 2, "w": 4, "h": 3},
                    config={"chart_type": "gauge", "max_value": 300}
                ),
                Widget(
                    id="w-risk-matrix",
                    type=WidgetType.CHART,
                    title="Risk Assessment",
                    position={"x": 8, "y": 2, "w": 4, "h": 3},
                    config={"chart_type": "heatmap"}
                )
            ]
        )
        self._layouts_cache["layout-executive"] = executive_layout
    
    def get_user_preferences(self, user_id: str) -> UserPreferences:
        """Get user preferences."""
        if user_id in self._preferences_cache:
            return self._preferences_cache[user_id]
        
        # Try to load from storage
        pref_file = self.storage_path / f"user_{user_id}.json"
        if pref_file.exists():
            try:
                with open(pref_file, 'r') as f:
                    data = json.load(f)
                    prefs = self._deserialize_preferences(data)
                    self._preferences_cache[user_id] = prefs
                    return prefs
            except Exception as e:
                logger.error(f"Error loading preferences for {user_id}: {e}")
        
        # Create new preferences
        prefs = UserPreferences(user_id=user_id)
        self._preferences_cache[user_id] = prefs
        return prefs
    
    def save_user_preferences(self, prefs: UserPreferences):
        """Save user preferences."""
        self._preferences_cache[prefs.user_id] = prefs
        
        # Save to file
        pref_file = self.storage_path / f"user_{prefs.user_id}.json"
        try:
            with open(pref_file, 'w') as f:
                json.dump(self._serialize_preferences(prefs), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving preferences for {prefs.user_id}: {e}")
    
    def create_custom_theme(self, user_id: str, theme: Theme) -> Theme:
        """Create custom theme for user."""
        prefs = self.get_user_preferences(user_id)
        theme.created_at = datetime.utcnow()
        theme.updated_at = datetime.utcnow()
        prefs.custom_themes.append(theme)
        self.save_user_preferences(prefs)
        return theme
    
    def create_custom_layout(self, user_id: str, layout: Layout) -> Layout:
        """Create custom layout for user."""
        prefs = self.get_user_preferences(user_id)
        prefs.custom_layouts.append(layout)
        self.save_user_preferences(prefs)
        return layout
    
    def create_saved_view(
        self,
        user_id: str,
        name: str,
        layout_id: str,
        theme_id: str,
        filters: Dict[str, Any] = None,
        description: str = "",
        is_public: bool = False
    ) -> SavedView:
        """Create a saved view."""
        view = SavedView(
            name=name,
            description=description,
            layout_id=layout_id,
            theme_id=theme_id,
            filters=filters or {},
            is_public=is_public
        )
        
        prefs = self.get_user_preferences(user_id)
        prefs.add_saved_view(view)
        self.save_user_preferences(prefs)
        
        return view
    
    def get_available_themes(self, user_id: str) -> List[Theme]:
        """Get all available themes for user."""
        themes = list(self._themes_cache.values())
        
        # Add user's custom themes
        prefs = self.get_user_preferences(user_id)
        themes.extend(prefs.custom_themes)
        
        return themes
    
    def get_available_layouts(self, user_id: str) -> List[Layout]:
        """Get all available layouts for user."""
        layouts = list(self._layouts_cache.values())
        
        # Add user's custom layouts
        prefs = self.get_user_preferences(user_id)
        layouts.extend(prefs.custom_layouts)
        
        return layouts
    
    def apply_saved_view(self, user_id: str, view_id: str) -> Optional[Dict[str, Any]]:
        """Apply a saved view and return configuration."""
        prefs = self.get_user_preferences(user_id)
        view = prefs.get_saved_view(view_id)
        
        if not view:
            return None
        
        # Get theme and layout
        theme = None
        layout = None
        
        # Check default themes
        if view.theme_id in self._themes_cache:
            theme = self._themes_cache[view.theme_id]
        else:
            # Check custom themes
            for t in prefs.custom_themes:
                if t.id == view.theme_id:
                    theme = t
                    break
        
        # Check default layouts
        if view.layout_id in self._layouts_cache:
            layout = self._layouts_cache[view.layout_id]
        else:
            # Check custom layouts
            for l in prefs.custom_layouts:
                if l.id == view.layout_id:
                    layout = l
                    break
        
        if not theme or not layout:
            return None
        
        # Update recent views
        if view.id in prefs.recent_views:
            prefs.recent_views.remove(view.id)
        prefs.recent_views.insert(0, view.id)
        prefs.recent_views = prefs.recent_views[:10]
        self.save_user_preferences(prefs)
        
        return {
            "view": asdict(view),
            "theme": asdict(theme),
            "layout": asdict(layout),
            "filters": view.filters
        }
    
    def export_configuration(self, user_id: str) -> Dict[str, Any]:
        """Export user's complete configuration."""
        prefs = self.get_user_preferences(user_id)
        
        return {
            "user_id": user_id,
            "preferences": self._serialize_preferences(prefs),
            "export_date": datetime.utcnow().isoformat()
        }
    
    def import_configuration(self, user_id: str, config: Dict[str, Any]) -> bool:
        """Import configuration for user."""
        try:
            if "preferences" in config:
                prefs = self._deserialize_preferences(config["preferences"])
                prefs.user_id = user_id  # Ensure correct user ID
                self.save_user_preferences(prefs)
                return True
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
        
        return False
    
    def _serialize_preferences(self, prefs: UserPreferences) -> Dict[str, Any]:
        """Serialize preferences to JSON-compatible format."""
        return {
            "user_id": prefs.user_id,
            "default_theme_id": prefs.default_theme_id,
            "default_layout_id": prefs.default_layout_id,
            "saved_views": [asdict(v) for v in prefs.saved_views],
            "custom_themes": [asdict(t) for t in prefs.custom_themes],
            "custom_layouts": [asdict(l) for l in prefs.custom_layouts],
            "favorite_widgets": prefs.favorite_widgets,
            "recent_views": prefs.recent_views,
            "settings": prefs.settings
        }
    
    def _deserialize_preferences(self, data: Dict[str, Any]) -> UserPreferences:
        """Deserialize preferences from JSON data."""
        prefs = UserPreferences(user_id=data["user_id"])
        prefs.default_theme_id = data.get("default_theme_id", "theme-light")
        prefs.default_layout_id = data.get("default_layout_id")
        prefs.favorite_widgets = data.get("favorite_widgets", [])
        prefs.recent_views = data.get("recent_views", [])
        prefs.settings = data.get("settings", {})
        
        # Deserialize saved views
        for view_data in data.get("saved_views", []):
            view = SavedView(**view_data)
            if isinstance(view.created_at, str):
                view.created_at = datetime.fromisoformat(view.created_at)
            if isinstance(view.updated_at, str):
                view.updated_at = datetime.fromisoformat(view.updated_at)
            prefs.saved_views.append(view)
        
        # Deserialize custom themes
        for theme_data in data.get("custom_themes", []):
            theme = Theme(**theme_data)
            if isinstance(theme.type, str):
                theme.type = ThemeType(theme.type)
            if isinstance(theme.colors, dict):
                theme.colors = ColorScheme(**theme.colors)
            if isinstance(theme.created_at, str):
                theme.created_at = datetime.fromisoformat(theme.created_at)
            if isinstance(theme.updated_at, str):
                theme.updated_at = datetime.fromisoformat(theme.updated_at)
            prefs.custom_themes.append(theme)
        
        # Deserialize custom layouts
        for layout_data in data.get("custom_layouts", []):
            layout = Layout(**layout_data)
            if isinstance(layout.type, str):
                layout.type = LayoutType(layout.type)
            
            # Deserialize widgets
            widgets = []
            for widget_data in layout_data.get("widgets", []):
                widget = Widget(**widget_data)
                if isinstance(widget.type, str):
                    widget.type = WidgetType(widget.type)
                widgets.append(widget)
            layout.widgets = widgets
            
            prefs.custom_layouts.append(layout)
        
        return prefs


# Global customizer instance
dashboard_customizer = DashboardCustomizer()