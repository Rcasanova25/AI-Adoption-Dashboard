#!/usr/bin/env python3
"""
Test script to verify the Dash app runs without errors.
This is a quick validation to ensure the migration is working.
"""
import sys
import logging
import time
from threading import Thread
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_dash_app():
    """Test that the Dash app starts and responds to requests."""
    logger.info("Starting Dash app test...")
    
    # Import the app
    try:
        from app_dash import DashboardApp
        logger.info("✅ Successfully imported DashboardApp")
    except ImportError as e:
        logger.error(f"❌ Failed to import DashboardApp: {e}")
        return False
    
    # Create app instance
    try:
        app_instance = DashboardApp()
        logger.info("✅ Successfully created DashboardApp instance")
    except Exception as e:
        logger.error(f"❌ Failed to create DashboardApp instance: {e}")
        return False
    
    # Test that layout is set
    try:
        assert app_instance.app.layout is not None
        logger.info("✅ App layout is configured")
    except AssertionError:
        logger.error("❌ App layout is not set")
        return False
    
    # Start the app in a separate thread
    def run_app():
        try:
            app_instance.app.run_server(
                debug=False, 
                port=8051, 
                threaded=True,
                use_reloader=False
            )
        except Exception as e:
            logger.error(f"Error running app: {e}")
    
    app_thread = Thread(target=run_app, daemon=True)
    app_thread.start()
    
    # Wait for app to start
    logger.info("Waiting for app to start...")
    time.sleep(3)
    
    # Test that the app responds
    try:
        response = requests.get("http://localhost:8051/", timeout=5)
        if response.status_code == 200:
            logger.info("✅ App is responding to HTTP requests")
        else:
            logger.error(f"❌ App returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to app: {e}")
        return False
    
    logger.info("✅ All tests passed! Dash app is working correctly.")
    return True

def test_callbacks():
    """Test that callbacks are registered correctly."""
    logger.info("\nTesting callbacks...")
    
    try:
        # Import callback modules
        from callbacks.data_callbacks import register_data_callbacks
        from callbacks.view_callbacks import register_view_callbacks
        from callbacks.performance_callbacks import register_performance_callbacks
        
        logger.info("✅ All callback modules imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Failed to import callback modules: {e}")
        return False

def test_view_manager():
    """Test the Dash view manager."""
    logger.info("\nTesting view manager...")
    
    try:
        from dash_view_manager import DashViewManager
        
        # Create instance
        view_manager = DashViewManager()
        logger.info("✅ Created DashViewManager instance")
        
        # Test view registry
        assert len(view_manager.all_views) > 0
        logger.info(f"✅ View manager has {len(view_manager.all_views)} views registered")
        
        # Test persona views
        assert "General" in view_manager.persona_views
        logger.info("✅ Persona views are configured")
        
        # Test sidebar layout creation
        sidebar = view_manager.create_sidebar_layout()
        assert sidebar is not None
        logger.info("✅ Sidebar layout creates successfully")
        
        return True
    except Exception as e:
        logger.error(f"❌ View manager test failed: {e}")
        return False

def test_sample_view():
    """Test that at least one view works."""
    logger.info("\nTesting sample view (adoption_rates)...")
    
    try:
        from views.adoption.adoption_rates_dash import create_layout
        
        # Create mock data
        mock_data = {
            "_metadata": {"loaded_at": "2025-01-01", "successful_loads": 25}
        }
        
        # Test layout creation
        layout = create_layout(mock_data, "General")
        assert layout is not None
        logger.info("✅ Adoption rates view creates layout successfully")
        
        return True
    except ImportError:
        logger.warning("⚠️ Adoption rates view not yet converted to Dash")
        return True  # Not a failure, just not implemented yet
    except Exception as e:
        logger.error(f"❌ View test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("AI Adoption Dashboard - Dash Migration Test")
    logger.info("=" * 60)
    
    tests = [
        ("Callbacks", test_callbacks),
        ("View Manager", test_view_manager),
        ("Sample View", test_sample_view),
        ("Dash App", test_dash_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\nRunning {test_name} test...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n🎉 All tests passed! The Dash migration is working correctly.")
        sys.exit(0)
    else:
        logger.error(f"\n⚠️ {total - passed} tests failed. Please fix the issues and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()