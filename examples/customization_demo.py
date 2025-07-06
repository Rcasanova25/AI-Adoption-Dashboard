"""Demonstration of dashboard customization features.

This script shows how to use the dashboard customization API.
"""

import requests
import json
from typing import Dict, Any, List


class CustomizationClient:
    """Client for dashboard customization API."""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str = None):
        """Initialize customization client."""
        self.base_url = base_url
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}
        
    def get_themes(self) -> List[Dict]:
        """Get available themes."""
        response = requests.get(
            f"{self.base_url}/api/customization/themes",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["data"]["themes"]
        return []
    
    def create_theme(self, name: str, colors: Dict[str, str]) -> Dict:
        """Create custom theme."""
        data = {
            "name": name,
            "colors": colors,
            "font_family": "Roboto, sans-serif",
            "font_size_base": 14
        }
        
        response = requests.post(
            f"{self.base_url}/api/customization/themes/create",
            json=data,
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()["data"]["theme"]
        else:
            print(f"Error creating theme: {response.json()}")
            return None
    
    def get_layouts(self) -> List[Dict]:
        """Get available layouts."""
        response = requests.get(
            f"{self.base_url}/api/customization/layouts",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["data"]["layouts"]
        return []
    
    def create_layout(self, name: str, widgets: List[Dict]) -> Dict:
        """Create custom layout."""
        data = {
            "name": name,
            "type": "dashboard",
            "columns": 12,
            "widgets": widgets
        }
        
        response = requests.post(
            f"{self.base_url}/api/customization/layouts/create",
            json=data,
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()["data"]["layout"]
        else:
            print(f"Error creating layout: {response.json()}")
            return None
    
    def save_view(self, name: str, layout_id: str, theme_id: str, filters: Dict = None) -> Dict:
        """Save dashboard view."""
        data = {
            "name": name,
            "layout_id": layout_id,
            "theme_id": theme_id,
            "filters": filters or {},
            "description": f"Custom view: {name}"
        }
        
        response = requests.post(
            f"{self.base_url}/api/customization/views/save",
            json=data,
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()["data"]["view"]
        else:
            print(f"Error saving view: {response.json()}")
            return None
    
    def get_saved_views(self) -> List[Dict]:
        """Get saved views."""
        response = requests.get(
            f"{self.base_url}/api/customization/views",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["data"]["views"]
        return []
    
    def apply_view(self, view_id: str) -> Dict:
        """Apply saved view."""
        response = requests.post(
            f"{self.base_url}/api/customization/views/apply",
            json={"view_id": view_id},
            headers=self.headers
        )
        
        if response.status_code == 200:
            return response.json()["data"]["configuration"]
        return None
    
    def get_preferences(self) -> Dict:
        """Get user preferences."""
        response = requests.get(
            f"{self.base_url}/api/customization/preferences",
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()["data"]["preferences"]
        return {}
    
    def update_preferences(self, updates: Dict) -> bool:
        """Update user preferences."""
        response = requests.put(
            f"{self.base_url}/api/customization/preferences/update",
            json=updates,
            headers=self.headers
        )
        return response.status_code == 200


def main():
    """Demonstrate customization features."""
    print("=== AI Adoption Dashboard Customization Demo ===\n")
    
    # First, login to get token
    print("1. Logging in...")
    auth_response = requests.post(
        "http://localhost:8000/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    
    if auth_response.status_code != 200:
        print("❌ Failed to login. Make sure the API server is running.")
        return
    
    token = auth_response.json()["data"]["access_token"]
    client = CustomizationClient(token=token)
    print("✅ Logged in successfully\n")
    
    # Get available themes
    print("2. Getting available themes...")
    themes = client.get_themes()
    print(f"   Found {len(themes)} themes:")
    for theme in themes[:3]:
        print(f"   - {theme['name']} ({theme['type']})")
    
    # Create custom theme
    print("\n3. Creating custom theme...")
    custom_theme = client.create_theme(
        name="Ocean Blue",
        colors={
            "primary": "#006994",
            "secondary": "#00ACC1",
            "background": "#E8F5E9",
            "text_primary": "#263238",
            "success": "#00897B",
            "warning": "#FFB300",
            "error": "#E53935"
        }
    )
    if custom_theme:
        print(f"   ✅ Created theme: {custom_theme['name']} (ID: {custom_theme['id']})")
    
    # Get available layouts
    print("\n4. Getting available layouts...")
    layouts = client.get_layouts()
    print(f"   Found {len(layouts)} layouts:")
    for layout in layouts:
        print(f"   - {layout['name']} ({layout['widgets_count']} widgets)")
    
    # Create custom layout
    print("\n5. Creating custom layout...")
    custom_widgets = [
        {
            "type": "metric",
            "title": "Total Investment",
            "position": {"x": 0, "y": 0, "w": 3, "h": 2},
            "data_source": "total_investment"
        },
        {
            "type": "metric",
            "title": "Current NPV",
            "position": {"x": 3, "y": 0, "w": 3, "h": 2},
            "data_source": "npv_calculation"
        },
        {
            "type": "chart",
            "title": "ROI Trend",
            "position": {"x": 6, "y": 0, "w": 6, "h": 3},
            "config": {"chart_type": "line"},
            "data_source": "roi_trend"
        },
        {
            "type": "table",
            "title": "Recent Calculations",
            "position": {"x": 0, "y": 3, "w": 6, "h": 4},
            "data_source": "recent_calculations"
        },
        {
            "type": "calculator",
            "title": "Quick NPV Calculator",
            "position": {"x": 6, "y": 3, "w": 6, "h": 4},
            "config": {"calculation_type": "npv"}
        }
    ]
    
    custom_layout = client.create_layout("Executive Overview", custom_widgets)
    if custom_layout:
        print(f"   ✅ Created layout: {custom_layout['name']} with {custom_layout['widgets_count']} widgets")
    
    # Save a view
    print("\n6. Saving dashboard view...")
    if custom_theme and custom_layout:
        saved_view = client.save_view(
            name="Q4 Financial Review",
            layout_id=custom_layout['id'],
            theme_id=custom_theme['id'],
            filters={
                "date_range": "2024-Q4",
                "department": "finance"
            }
        )
        if saved_view:
            print(f"   ✅ Saved view: {saved_view['name']} (ID: {saved_view['id']})")
    
    # Get saved views
    print("\n7. Getting saved views...")
    views = client.get_saved_views()
    print(f"   Found {len(views)} saved views:")
    for view in views:
        print(f"   - {view['name']} (Created: {view['created_at']})")
    
    # Get preferences
    print("\n8. Getting user preferences...")
    prefs = client.get_preferences()
    print(f"   Default theme: {prefs.get('default_theme_id')}")
    print(f"   Default layout: {prefs.get('default_layout_id', 'None')}")
    print(f"   Favorite widgets: {len(prefs.get('favorite_widgets', []))}")
    
    # Update preferences
    print("\n9. Updating preferences...")
    if custom_theme:
        success = client.update_preferences({
            "default_theme_id": custom_theme['id'],
            "settings": {
                "auto_refresh": True,
                "refresh_interval": 300
            }
        })
        if success:
            print("   ✅ Preferences updated")
    
    # Apply a saved view
    print("\n10. Applying saved view...")
    if views:
        config = client.apply_view(views[0]['id'])
        if config:
            print(f"   ✅ Applied view: {config['view']['name']}")
            print(f"   Theme: {config['theme']['name']}")
            print(f"   Layout: {config['layout']['name']}")
            print(f"   Widgets: {len(config['layout']['widgets'])}")
    
    print("\n=== Demo Complete ===")
    print("\nCustomization features allow users to:")
    print("- Create custom themes with brand colors")
    print("- Design personalized dashboard layouts")
    print("- Save and share dashboard views")
    print("- Set personal preferences")
    print("- Export/import configurations")


if __name__ == "__main__":
    main()