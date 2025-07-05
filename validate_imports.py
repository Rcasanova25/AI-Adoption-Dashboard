#!/usr/bin/env python3
"""Validate that all critical imports work correctly."""

import sys

def test_import(module_path, item=None):
    """Test importing a module or specific item from a module."""
    try:
        if item:
            exec(f"from {module_path} import {item}")
            print(f"✓ Successfully imported {item} from {module_path}")
        else:
            exec(f"import {module_path}")
            print(f"✓ Successfully imported {module_path}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import {'%s from %s' % (item, module_path) if item else module_path}: {e}")
        return False
    except Exception as e:
        print(f"✗ Error importing {'%s from %s' % (item, module_path) if item else module_path}: {e}")
        return False

def main():
    """Main validation function."""
    print("Validating critical imports for AI Adoption Dashboard...\n")
    
    # Critical imports from app.py
    critical_imports = [
        # UI Components
        ("components.ui.metric_card", "render_metric_card"),
        ("components.ui.theme", "ThemeManager"),
        
        # Utils
        ("utils.error_handler", "ErrorHandler"),
        ("utils.error_handler", "handle_errors"),
        ("utils.error_handler", "setup_logging"),
        ("utils.types", "DashboardData"),
        
        # Views
        ("views", "VIEW_REGISTRY"),
        ("views.base", "ViewRegistry"),
        
        # Data
        ("data.data_manager", "DataManager"),
        ("data.data_manager", "create_optimized_manager"),
        
        # Components
        ("components.accessibility", "AccessibilityManager"),
        ("components.accessibility", "create_accessible_dashboard_layout"),
        ("components.competitive_assessor", "CompetitiveAssessor"),
        ("components.economic_insights", "EconomicInsights"),
        ("components.view_enhancements", "ViewEnhancements"),
        
        # Performance
        ("performance.cache_manager", "get_cache"),
        ("performance.monitor", "get_metrics"),
        ("performance.monitor", "track_performance"),
        
        # Config
        ("config.settings", "Settings"),
    ]
    
    success_count = 0
    total_count = len(critical_imports)
    
    for module_path, item in critical_imports:
        if test_import(module_path, item):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"Import Validation Results: {success_count}/{total_count} successful")
    print(f"{'='*50}")
    
    if success_count == total_count:
        print("\n✅ All critical imports are working correctly!")
        return 0
    else:
        print(f"\n❌ {total_count - success_count} imports failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())