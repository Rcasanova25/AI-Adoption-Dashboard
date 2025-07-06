"""Base view components for AI Adoption Dashboard.

This module provides the ViewRegistry system and base classes for managing views.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

import pandas as pd
import streamlit as st

from data.services import get_data_service, show_data_error


@dataclass
class ViewMetadata:
    """Metadata for a view."""

    name: str
    category: str = "General"
    description: str = ""
    required_data: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    icon: str = "📊"
    order: int = 100


class BaseView(ABC):
    """Abstract base class for views."""

    def __init__(self, metadata: Optional[ViewMetadata] = None):
        """Initialize the view with metadata.

        Args:
            metadata: Optional metadata for the view
        """
        self.metadata = metadata or ViewMetadata(name=self.__class__.__name__)

    @abstractmethod
    def render(self, data: Dict[str, Any]) -> None:
        """Render the view.

        Args:
            data: Dictionary containing all dashboard data
        """
        pass

    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate that required data is present and valid.

        Args:
            data: Dictionary containing dashboard data

        Returns:
            True if all required data is present and valid, False otherwise
        """
        if not self.metadata.required_data:
            return True

        missing_data = []
        invalid_data = []
        
        for required_key in self.metadata.required_data:
            if required_key not in data or data[required_key] is None:
                missing_data.append(required_key)
            elif isinstance(data[required_key], pd.DataFrame) and data[required_key].empty:
                invalid_data.append(f"{required_key} (empty DataFrame)")
            elif isinstance(data[required_key], dict) and not data[required_key]:
                invalid_data.append(f"{required_key} (empty dict)")
            elif isinstance(data[required_key], list) and not data[required_key]:
                invalid_data.append(f"{required_key} (empty list)")
        
        if missing_data or invalid_data:
            error_msg = f"❌ Data Validation Failed for view '{self.metadata.name}'\n\n"
            
            if missing_data:
                error_msg += f"**Missing data**: {', '.join(missing_data)}\n"
            if invalid_data:
                error_msg += f"**Invalid data**: {', '.join(invalid_data)}\n"
            
            show_data_error(
                error_msg,
                recovery_suggestions=[
                    "Ensure all required PDF files are in the resources directory",
                    "Check that PDF extraction completed successfully",
                    "Verify data source configuration in data_service.py",
                    "Run data availability diagnostic: Settings → Data Status"
                ]
            )
            return False
            
        return True

    def show_source_info(self, sources: List[str]) -> None:
        """Display source information.

        Args:
            sources: List of data source descriptions
        """
        with st.expander("📚 Data Sources"):
            for source in sources:
                st.write(f"• {source}")


class ViewRegistry:
    """Registry for managing dashboard views."""

    def __init__(self):
        """Initialize the view registry."""
        self._views: Dict[str, Any] = {}
        self._metadata: Dict[str, ViewMetadata] = {}
        self._categories: Dict[str, List[str]] = {}

    def register(self, name: str, view: Any, metadata: Optional[ViewMetadata] = None) -> None:
        """Register a view.

        Args:
            name: Name of the view
            view: View instance or callable function
            metadata: Optional metadata for the view
        """
        self._views[name] = view

        # Handle metadata
        if metadata:
            self._metadata[name] = metadata
        elif isinstance(view, BaseView):
            self._metadata[name] = view.metadata
        else:
            # Create default metadata for function-based views
            self._metadata[name] = ViewMetadata(
                name=name, category="General", description=f"{name} view"
            )

        # Update categories
        category = self._metadata[name].category
        if category not in self._categories:
            self._categories[category] = []
        if name not in self._categories[category]:
            self._categories[category].append(name)

    def unregister(self, name: str) -> None:
        """Unregister a view.

        Args:
            name: Name of the view to unregister
        """
        if name in self._views:
            # Remove from views
            del self._views[name]

            # Remove from metadata
            if name in self._metadata:
                category = self._metadata[name].category
                del self._metadata[name]

                # Update categories
                if category in self._categories and name in self._categories[category]:
                    self._categories[category].remove(name)
                    if not self._categories[category]:
                        del self._categories[category]

    def get_view(self, name: str) -> Optional[Any]:
        """Get a view by name.

        Args:
            name: Name of the view

        Returns:
            View instance or callable, or None if not found
        """
        return self._views.get(name)

    def get_metadata(self, name: str) -> Optional[ViewMetadata]:
        """Get metadata for a view.

        Args:
            name: Name of the view

        Returns:
            ViewMetadata or None if not found
        """
        return self._metadata.get(name)

    def list_views(self, category: Optional[str] = None) -> List[str]:
        """List all registered view names.

        Args:
            category: Optional category filter

        Returns:
            List of view names
        """
        if category:
            return self._categories.get(category, [])
        return list(self._views.keys())

    def list_categories(self) -> List[str]:
        """List all view categories.

        Returns:
            List of category names
        """
        return list(self._categories.keys())

    def render(self, name: str, data: Dict[str, Any]) -> None:
        """Render a view by name with strict validation.

        Args:
            name: Name of the view to render
            data: Data to pass to the view
        """
        view = self._views.get(name)
        if not view:
            show_data_error(
                f"❌ View Configuration Error: View '{name}' not found",
                recovery_suggestions=[
                    f"Available views: {', '.join(self.list_views())}",
                    "Check view registration in views/__init__.py",
                    "Verify view name spelling"
                ]
            )
            return

        try:
            # Check if it's a class-based view
            if isinstance(view, BaseView):
                # Validate data - this will show error and stop if validation fails
                if not view.validate_data(data):
                    return

                # Render the view
                view.render(data)

            # Check if it's a callable (function-based view)
            elif callable(view):
                # For function-based views, perform basic validation
                if hasattr(view, '__module__'):
                    # Check if any data is completely empty
                    empty_datasets = []
                    for key, value in data.items():
                        if isinstance(value, pd.DataFrame) and value.empty:
                            empty_datasets.append(key)
                        elif isinstance(value, (dict, list)) and not value:
                            empty_datasets.append(key)
                    
                    if empty_datasets:
                        st.warning(
                            f"⚠️ Warning: The following datasets are empty: {', '.join(empty_datasets)}. "
                            "Some visualizations may not display correctly."
                        )
                
                # Render the view
                view(data)

            else:
                show_data_error(
                    f"❌ View Type Error: View '{name}' is not a valid view type",
                    recovery_suggestions=[
                        "View must be either a BaseView instance or a callable function",
                        "Check view implementation"
                    ]
                )
                
        except Exception as e:
            # Catch any rendering errors and display them clearly
            show_data_error(
                f"❌ View Rendering Error in '{name}': {str(e)}",
                recovery_suggestions=[
                    "Check that all required data columns exist",
                    "Verify data types match expected formats",
                    "Review view implementation for errors",
                    "Check application logs for detailed error trace"
                ]
            )

    def get_views_by_tag(self, tag: str) -> List[str]:
        """Get all views with a specific tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of view names with the tag
        """
        matching_views = []
        for name, metadata in self._metadata.items():
            if tag in metadata.tags:
                matching_views.append(name)
        return matching_views

    def get_sorted_views(self) -> List[str]:
        """Get all views sorted by their order attribute.

        Returns:
            List of view names sorted by order
        """
        return sorted(
            self._views.keys(),
            key=lambda name: self._metadata.get(name, ViewMetadata(name=name)).order,
        )

    def validate_all_views_data(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Validate data availability for all registered views.
        
        Args:
            data: Dictionary containing dashboard data
            
        Returns:
            Dictionary mapping view names to validation status
        """
        validation_results = {}
        
        for view_name in self._views:
            view = self._views[view_name]
            
            if isinstance(view, BaseView):
                # Don't show errors during bulk validation, just collect status
                try:
                    # Temporarily suppress error display
                    is_valid = True
                    if view.metadata.required_data:
                        for required_key in view.metadata.required_data:
                            if required_key not in data or data[required_key] is None:
                                is_valid = False
                                break
                            elif isinstance(data[required_key], pd.DataFrame) and data[required_key].empty:
                                is_valid = False
                                break
                    validation_results[view_name] = is_valid
                except Exception:
                    validation_results[view_name] = False
            else:
                # Function-based views - assume valid if callable
                validation_results[view_name] = callable(view)
                
        return validation_results
    
    # Enforce CLAUDE.md compliance: no demo/sample logic, only real, validated data.
