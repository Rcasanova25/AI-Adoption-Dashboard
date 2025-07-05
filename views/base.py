"""Base view components for AI Adoption Dashboard.

This module provides the ViewRegistry system and base classes for managing views.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

import streamlit as st


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
        """Validate that required data is present.

        Args:
            data: Dictionary containing dashboard data

        Returns:
            True if all required data is present, False otherwise
        """
        if not self.metadata.required_data:
            return True

        for required_key in self.metadata.required_data:
            if required_key not in data or data[required_key] is None:
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
        """Render a view by name.

        Args:
            name: Name of the view to render
            data: Data to pass to the view
        """
        view = self._views.get(name)
        if not view:
            st.error(f"View '{name}' not found")
            return

        # Check if it's a class-based view
        if isinstance(view, BaseView):
            # Validate data
            if not view.validate_data(data):
                st.warning(
                    f"Missing required data for view '{name}'. "
                    f"Required: {', '.join(view.metadata.required_data)}"
                )
                return

            # Render the view
            view.render(data)

        # Check if it's a callable (function-based view)
        elif callable(view):
            # For backward compatibility with function-based views
            view(data)

        else:
            st.error(f"View '{name}' is not a valid view type")

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
