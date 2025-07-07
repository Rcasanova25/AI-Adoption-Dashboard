#!/usr/bin/env python3
"""
Simple script to run the Dash app with proper error handling.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the Dash application."""
    print("Starting AI Adoption Dashboard (Dash version)...")
    print("-" * 60)
    
    # Check for required packages
    required_packages = ['dash', 'dash_bootstrap_components', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("\nPlease install them with:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    # Try to import and run the app
    try:
        from app_dash import DashboardApp
        
        print("✅ Successfully imported DashboardApp")
        print("\nInitializing application...")
        
        app_instance = DashboardApp()
        
        print("✅ Application initialized")
        print("\n" + "=" * 60)
        print("🚀 Starting Dash server...")
        print("=" * 60)
        print("\n📊 Access the dashboard at: http://localhost:8050")
        print("Press Ctrl+C to stop the server\n")
        
        # Run the app
        app_instance.run(debug=True, host="0.0.0.0", port=8050)
        
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()