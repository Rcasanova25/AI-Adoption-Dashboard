"""Example usage of ViewRegistry with existing views.

This demonstrates how the ViewRegistry works with both function-based
and class-based views while maintaining backward compatibility.
"""

# Example of how app.py uses ViewRegistry

# Import the registry and existing views
from views import VIEW_REGISTRY, ViewRegistry, BaseView, ViewMetadata

# Initialize the registry
view_registry = ViewRegistry()

# Register all existing function-based views
for view_name, view_func in VIEW_REGISTRY.items():
    view_registry.register(view_name, view_func)

# Example of creating a class-based view
class CustomAnalysisView(BaseView):
    """Example class-based view."""
    
    def __init__(self):
        metadata = ViewMetadata(
            name="Custom Analysis",
            category="Advanced",
            description="Custom analysis view with enhanced features",
            required_data=["historical_data", "sector_2025"],
            tags={"custom", "analysis", "advanced"},
            icon="🔬",
            order=50
        )
        super().__init__(metadata)
    
    def render(self, data):
        """Render the custom analysis view."""
        # Validate required data
        if not self.validate_data(data):
            print("Missing required data")
            return
        
        print(f"Rendering {self.metadata.name} view")
        
        # Show source info
        self.show_source_info([
            "Custom data source 1",
            "Custom data source 2"
        ])

# Register a class-based view
custom_view = CustomAnalysisView()
view_registry.register("Custom Analysis", custom_view)

# Example usage patterns
print("=" * 50)
print("ViewRegistry Usage Examples")
print("=" * 50)

# List all views
print("\nAll registered views:")
for view_name in view_registry.list_views():
    print(f"  - {view_name}")

# List views by category
print("\nViews by category:")
for category in view_registry.list_categories():
    print(f"\n{category}:")
    for view_name in view_registry.list_views(category=category):
        print(f"  - {view_name}")

# Get view metadata
print("\nView metadata example:")
metadata = view_registry.get_metadata("Custom Analysis")
if metadata:
    print(f"  Name: {metadata.name}")
    print(f"  Category: {metadata.category}")
    print(f"  Description: {metadata.description}")
    print(f"  Required data: {metadata.required_data}")
    print(f"  Tags: {metadata.tags}")
    print(f"  Icon: {metadata.icon}")

# Get views by tag
print("\nViews with 'custom' tag:")
for view_name in view_registry.get_views_by_tag("custom"):
    print(f"  - {view_name}")

# Demonstrate rendering (in actual app, data would be real dashboard data)
print("\nRendering example:")
sample_data = {
    "historical_data": {"sample": "data"},
    "sector_2025": {"sample": "data"}
}

# This would be called in app.py like:
# view_registry.render("Custom Analysis", data)
print(f"Would render 'Custom Analysis' view with data: {list(sample_data.keys())}")

print("\n" + "=" * 50)
print("ViewRegistry is fully backward compatible!")
print("Existing function-based views work without changes.")
print("=" * 50)