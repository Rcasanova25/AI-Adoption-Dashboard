"""Dashboard customization API endpoints.

This module provides API endpoints for dashboard customization features
including themes, layouts, and saved views.
"""

import logging
from typing import Dict, List, Optional, Any
from fastapi import Depends, HTTPException

from utils.dashboard_customization import (
    dashboard_customizer,
    Theme,
    Layout,
    Widget,
    SavedView,
    ThemeType,
    LayoutType,
    WidgetType,
    ColorScheme
)
from .endpoints import APIResponse, log_api_call, validate_request
from .auth_endpoints import get_current_user, TokenData

logger = logging.getLogger(__name__)


class CustomizationAPI:
    """API endpoints for dashboard customization."""
    
    @staticmethod
    @log_api_call("customization/themes")
    def get_themes(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get available themes for user."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            themes = dashboard_customizer.get_available_themes(user_id)
            
            # Convert to dict format
            themes_data = []
            for theme in themes:
                theme_dict = {
                    "id": theme.id,
                    "name": theme.name,
                    "type": theme.type.value,
                    "colors": {
                        "primary": theme.colors.primary,
                        "secondary": theme.colors.secondary,
                        "background": theme.colors.background,
                        "text_primary": theme.colors.text_primary
                    },
                    "is_custom": theme.type == ThemeType.CUSTOM
                }
                themes_data.append(theme_dict)
            
            return APIResponse.success({
                "themes": themes_data,
                "count": len(themes_data)
            })
            
        except Exception as e:
            logger.error(f"Get themes error: {e}")
            return APIResponse.error("Failed to get themes", 500)
    
    @staticmethod
    @log_api_call("customization/themes/create")
    @validate_request(["name", "colors"])
    def create_theme(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Create custom theme.
        
        Request:
            {
                "name": "My Theme",
                "colors": {
                    "primary": "#2196F3",
                    "secondary": "#FF4081",
                    "background": "#FFFFFF",
                    "text_primary": "#212121"
                },
                "font_family": "Roboto, sans-serif",
                "font_size_base": 14
            }
        """
        try:
            user_id = current_user.username if current_user else "anonymous"
            
            # Create color scheme
            color_data = request_data["colors"]
            colors = ColorScheme(
                primary=color_data.get("primary", "#1E88E5"),
                secondary=color_data.get("secondary", "#424242"),
                success=color_data.get("success", "#4CAF50"),
                warning=color_data.get("warning", "#FF9800"),
                error=color_data.get("error", "#F44336"),
                background=color_data.get("background", "#FFFFFF"),
                surface=color_data.get("surface", "#F5F5F5"),
                text_primary=color_data.get("text_primary", "#212121"),
                text_secondary=color_data.get("text_secondary", "#757575"),
                border=color_data.get("border", "#E0E0E0")
            )
            
            # Create theme
            theme = Theme(
                name=request_data["name"],
                type=ThemeType.CUSTOM,
                colors=colors,
                font_family=request_data.get("font_family", "Arial, sans-serif"),
                font_size_base=request_data.get("font_size_base", 14),
                border_radius=request_data.get("border_radius", 4),
                spacing_unit=request_data.get("spacing_unit", 8)
            )
            
            created_theme = dashboard_customizer.create_custom_theme(user_id, theme)
            
            return APIResponse.success({
                "theme": {
                    "id": created_theme.id,
                    "name": created_theme.name,
                    "type": created_theme.type.value
                }
            }, "Theme created successfully")
            
        except Exception as e:
            logger.error(f"Create theme error: {e}")
            return APIResponse.error("Failed to create theme", 500)
    
    @staticmethod
    @log_api_call("customization/layouts")
    def get_layouts(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get available layouts for user."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            layouts = dashboard_customizer.get_available_layouts(user_id)
            
            # Convert to dict format
            layouts_data = []
            for layout in layouts:
                layout_dict = {
                    "id": layout.id,
                    "name": layout.name,
                    "type": layout.type.value,
                    "widgets_count": len(layout.widgets),
                    "columns": layout.columns,
                    "is_custom": layout.id.startswith("custom-")
                }
                layouts_data.append(layout_dict)
            
            return APIResponse.success({
                "layouts": layouts_data,
                "count": len(layouts_data)
            })
            
        except Exception as e:
            logger.error(f"Get layouts error: {e}")
            return APIResponse.error("Failed to get layouts", 500)
    
    @staticmethod
    @log_api_call("customization/layouts/create")
    @validate_request(["name", "widgets"])
    def create_layout(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Create custom layout.
        
        Request:
            {
                "name": "My Layout",
                "type": "dashboard",
                "columns": 12,
                "widgets": [
                    {
                        "type": "metric",
                        "title": "NPV",
                        "position": {"x": 0, "y": 0, "w": 3, "h": 2},
                        "data_source": "npv_calculation"
                    }
                ]
            }
        """
        try:
            user_id = current_user.username if current_user else "anonymous"
            
            # Create layout
            layout = Layout(
                name=request_data["name"],
                type=LayoutType(request_data.get("type", "dashboard")),
                columns=request_data.get("columns", 12),
                row_height=request_data.get("row_height", 80),
                spacing=request_data.get("spacing", 10)
            )
            
            # Add widgets
            for widget_data in request_data["widgets"]:
                widget = Widget(
                    type=WidgetType(widget_data["type"]),
                    title=widget_data.get("title", ""),
                    config=widget_data.get("config", {}),
                    position=widget_data.get("position", {"x": 0, "y": 0, "w": 4, "h": 3}),
                    data_source=widget_data.get("data_source"),
                    refresh_interval=widget_data.get("refresh_interval"),
                    visible=widget_data.get("visible", True)
                )
                
                if not layout.add_widget(widget):
                    return APIResponse.error(f"Invalid widget position: {widget.title}", 400)
            
            # Optimize layout
            layout.optimize_layout()
            
            created_layout = dashboard_customizer.create_custom_layout(user_id, layout)
            
            return APIResponse.success({
                "layout": {
                    "id": created_layout.id,
                    "name": created_layout.name,
                    "widgets_count": len(created_layout.widgets)
                }
            }, "Layout created successfully")
            
        except Exception as e:
            logger.error(f"Create layout error: {e}")
            return APIResponse.error("Failed to create layout", 500)
    
    @staticmethod
    @log_api_call("customization/views/save")
    @validate_request(["name", "layout_id", "theme_id"])
    def save_view(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Save current dashboard view.
        
        Request:
            {
                "name": "Q4 Analysis",
                "description": "Financial analysis for Q4",
                "layout_id": "layout-financial",
                "theme_id": "theme-dark",
                "filters": {
                    "date_range": "2024-Q4",
                    "department": "finance"
                },
                "is_public": false
            }
        """
        try:
            user_id = current_user.username if current_user else "anonymous"
            
            view = dashboard_customizer.create_saved_view(
                user_id=user_id,
                name=request_data["name"],
                layout_id=request_data["layout_id"],
                theme_id=request_data["theme_id"],
                filters=request_data.get("filters", {}),
                description=request_data.get("description", ""),
                is_public=request_data.get("is_public", False)
            )
            
            return APIResponse.success({
                "view": {
                    "id": view.id,
                    "name": view.name,
                    "created_at": view.created_at.isoformat()
                }
            }, "View saved successfully")
            
        except Exception as e:
            logger.error(f"Save view error: {e}")
            return APIResponse.error("Failed to save view", 500)
    
    @staticmethod
    @log_api_call("customization/views")
    def get_saved_views(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get user's saved views."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            prefs = dashboard_customizer.get_user_preferences(user_id)
            
            views_data = []
            for view in prefs.saved_views:
                views_data.append({
                    "id": view.id,
                    "name": view.name,
                    "description": view.description,
                    "created_at": view.created_at.isoformat(),
                    "updated_at": view.updated_at.isoformat(),
                    "is_default": view.is_default,
                    "is_public": view.is_public,
                    "tags": view.tags
                })
            
            return APIResponse.success({
                "views": views_data,
                "count": len(views_data),
                "recent_views": prefs.recent_views[:5]
            })
            
        except Exception as e:
            logger.error(f"Get saved views error: {e}")
            return APIResponse.error("Failed to get saved views", 500)
    
    @staticmethod
    @log_api_call("customization/views/apply")
    @validate_request(["view_id"])
    def apply_view(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Apply a saved view."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            view_id = request_data["view_id"]
            
            config = dashboard_customizer.apply_saved_view(user_id, view_id)
            
            if not config:
                return APIResponse.error("View not found", 404)
            
            return APIResponse.success({
                "configuration": config
            }, "View applied successfully")
            
        except Exception as e:
            logger.error(f"Apply view error: {e}")
            return APIResponse.error("Failed to apply view", 500)
    
    @staticmethod
    @log_api_call("customization/views/delete")
    @validate_request(["view_id"])
    def delete_view(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Delete a saved view."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            view_id = request_data["view_id"]
            
            prefs = dashboard_customizer.get_user_preferences(user_id)
            if prefs.delete_saved_view(view_id):
                dashboard_customizer.save_user_preferences(prefs)
                return APIResponse.success({}, "View deleted successfully")
            else:
                return APIResponse.error("View not found", 404)
                
        except Exception as e:
            logger.error(f"Delete view error: {e}")
            return APIResponse.error("Failed to delete view", 500)
    
    @staticmethod
    @log_api_call("customization/preferences")
    def get_preferences(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get user preferences."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            prefs = dashboard_customizer.get_user_preferences(user_id)
            
            return APIResponse.success({
                "preferences": {
                    "default_theme_id": prefs.default_theme_id,
                    "default_layout_id": prefs.default_layout_id,
                    "favorite_widgets": prefs.favorite_widgets,
                    "settings": prefs.settings
                }
            })
            
        except Exception as e:
            logger.error(f"Get preferences error: {e}")
            return APIResponse.error("Failed to get preferences", 500)
    
    @staticmethod
    @log_api_call("customization/preferences/update")
    def update_preferences(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Update user preferences."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            prefs = dashboard_customizer.get_user_preferences(user_id)
            
            # Update allowed fields
            if "default_theme_id" in request_data:
                prefs.default_theme_id = request_data["default_theme_id"]
            if "default_layout_id" in request_data:
                prefs.default_layout_id = request_data["default_layout_id"]
            if "favorite_widgets" in request_data:
                prefs.favorite_widgets = request_data["favorite_widgets"]
            if "settings" in request_data:
                prefs.settings.update(request_data["settings"])
            
            dashboard_customizer.save_user_preferences(prefs)
            
            return APIResponse.success({}, "Preferences updated successfully")
            
        except Exception as e:
            logger.error(f"Update preferences error: {e}")
            return APIResponse.error("Failed to update preferences", 500)
    
    @staticmethod
    @log_api_call("customization/export")
    def export_configuration(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Export user's customization configuration."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            config = dashboard_customizer.export_configuration(user_id)
            
            return APIResponse.success({
                "configuration": config,
                "export_format": "json"
            }, "Configuration exported successfully")
            
        except Exception as e:
            logger.error(f"Export configuration error: {e}")
            return APIResponse.error("Failed to export configuration", 500)
    
    @staticmethod
    @log_api_call("customization/import")
    @validate_request(["configuration"])
    def import_configuration(
        request_data: Dict,
        current_user: TokenData = None
    ) -> Dict:
        """Import customization configuration."""
        try:
            user_id = current_user.username if current_user else "anonymous"
            config = request_data["configuration"]
            
            if dashboard_customizer.import_configuration(user_id, config):
                return APIResponse.success({}, "Configuration imported successfully")
            else:
                return APIResponse.error("Invalid configuration format", 400)
                
        except Exception as e:
            logger.error(f"Import configuration error: {e}")
            return APIResponse.error("Failed to import configuration", 500)
    
    @staticmethod
    @log_api_call("customization/widgets/types")
    def get_widget_types(
        request_data: Dict = None,
        current_user: TokenData = None
    ) -> Dict:
        """Get available widget types."""
        try:
            widget_types = [
                {
                    "type": "chart",
                    "name": "Chart",
                    "description": "Display data visualizations",
                    "config_options": ["chart_type", "show_legend", "show_grid"]
                },
                {
                    "type": "metric",
                    "name": "Metric",
                    "description": "Display single metric value",
                    "config_options": ["format", "show_trend", "comparison"]
                },
                {
                    "type": "table",
                    "name": "Table",
                    "description": "Display tabular data",
                    "config_options": ["sortable", "filterable", "pagination"]
                },
                {
                    "type": "text",
                    "name": "Text",
                    "description": "Display formatted text content",
                    "config_options": ["template", "markdown"]
                },
                {
                    "type": "filter",
                    "name": "Filter",
                    "description": "Interactive filter controls",
                    "config_options": ["filter_type", "options", "default_value"]
                },
                {
                    "type": "calculator",
                    "name": "Calculator",
                    "description": "Interactive calculation widget",
                    "config_options": ["calculation_type", "inputs"]
                }
            ]
            
            return APIResponse.success({
                "widget_types": widget_types
            })
            
        except Exception as e:
            logger.error(f"Get widget types error: {e}")
            return APIResponse.error("Failed to get widget types", 500)


# Initialize customization API instance
customization_api = CustomizationAPI()