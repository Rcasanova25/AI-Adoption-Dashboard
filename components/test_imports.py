"""
Test file to verify that all UI components can be imported correctly.
Run this file to check if the components module is working properly.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test importing all components"""
    
    print("Testing UI Components imports...")
    
    try:
        # Test charts imports
        from components.charts import (
            MetricCard,
            TrendChart, 
            ComparisonChart,
            ROIChart,
            GeographicChart,
            IndustryChart,
            ChartConfig
        )
        print("✅ Charts module imported successfully")
        
        # Test layouts imports
        from components.layouts import (
            ExecutiveDashboard,
            AnalyticalDashboard, 
            ResponsiveGrid,
            TabContainer,
            LayoutConfig
        )
        print("✅ Layouts module imported successfully")
        
        # Test widgets imports
        from components.widgets import (
            SmartFilter,
            ActionButton,
            ProgressIndicator,
            AlertBox,
            DataTable,
            WidgetConfig
        )
        print("✅ Widgets module imported successfully")
        
        # Test themes imports
        from components.themes import (
            ExecutiveTheme,
            AnalystTheme,
            apply_custom_theme,
            get_available_themes,
            get_theme_preview,
            create_custom_theme,
            ThemeConfig
        )
        print("✅ Themes module imported successfully")
        
        # Test main module import
        from components import (
            MetricCard,
            TrendChart,
            ComparisonChart,
            ROIChart,
            GeographicChart,
            IndustryChart,
            ExecutiveDashboard,
            AnalyticalDashboard,
            ResponsiveGrid,
            TabContainer,
            SmartFilter,
            ActionButton,
            ProgressIndicator,
            AlertBox,
            DataTable,
            ExecutiveTheme,
            AnalystTheme,
            apply_custom_theme
        )
        print("✅ Main components module imported successfully")
        
        print("\n🎉 All imports successful! The UI components module is working correctly.")
        
        # Test creating some basic objects
        print("\nTesting object creation...")
        
        # Test chart config
        config = ChartConfig(theme="executive", height=500)
        print("✅ ChartConfig created successfully")
        
        # Test metric card
        metric_card = MetricCard(config)
        print("✅ MetricCard created successfully")
        
        # Test executive dashboard
        dashboard = ExecutiveDashboard()
        print("✅ ExecutiveDashboard created successfully")
        
        # Test smart filter
        smart_filter = SmartFilter()
        print("✅ SmartFilter created successfully")
        
        # Test executive theme
        theme = ExecutiveTheme()
        print("✅ ExecutiveTheme created successfully")
        
        print("\n🎉 All object creation tests passed!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_version():
    """Test version information"""
    try:
        from components import __version__, __author__, __description__
        print(f"\n📦 Component Module Info:")
        print(f"   Version: {__version__}")
        print(f"   Author: {__author__}")
        print(f"   Description: {__description__}")
        return True
    except Exception as e:
        print(f"❌ Error getting version info: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing UI Components Module")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test version info
    version_ok = test_version()
    
    print("\n" + "=" * 50)
    if imports_ok and version_ok:
        print("🎉 All tests passed! The UI components module is ready to use.")
        print("\nTo run the demo:")
        print("   streamlit run components/example_usage.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.") 