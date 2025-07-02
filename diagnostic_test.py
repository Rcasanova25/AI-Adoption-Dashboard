#!/usr/bin/env python3
"""
Diagnostic Test for AI Adoption Dashboard
Tests the key components to identify issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all key modules can be imported"""
    print("Testing imports...")
    
    try:
        from views.realtime_analysis import show_realtime_analysis
        print("✅ realtime_analysis import successful")
    except Exception as e:
        print(f"❌ realtime_analysis import failed: {e}")
    
    try:
        from data.oecd_realtime import OECDIntegration, OECDRealTimeClient
        print("✅ oecd_realtime import successful")
    except Exception as e:
        print(f"❌ oecd_realtime import failed: {e}")
    
    try:
        from business.causal_analysis import causal_engine
        print("✅ causal_analysis import successful")
    except Exception as e:
        print(f"❌ causal_analysis import failed: {e}")
    
    try:
        from views.executive_dashboard import show_executive_dashboard
        print("✅ executive_dashboard import successful")
    except Exception as e:
        print(f"❌ executive_dashboard import failed: {e}")

def test_causal_confidence():
    """Test the causal analysis confidence calculation"""
    print("\nTesting causal confidence...")
    
    try:
        import pandas as pd
        from business.causal_analysis import causal_engine
        
        # Create sample data
        sample_adoption_data = pd.DataFrame({
            'year': [2022, 2023, 2024],
            'adoption_rate': [45, 65, 78],
            'sector': ['Technology', 'Technology', 'Technology']
        })
        
        sample_productivity_data = pd.DataFrame({
            'year': [2022, 2023, 2024],
            'revenue_per_employee': [150000, 165000, 180000],
            'sector': ['Technology', 'Technology', 'Technology']
        })
        
        # Run causal analysis
        result = causal_engine.establish_ai_productivity_causality(
            adoption_data=sample_adoption_data,
            productivity_data=sample_productivity_data,
            sector="technology"
        )
        
        print(f"✅ Causal analysis completed")
        print(f"   Confidence score: {result.confidence_score:.3f}")
        print(f"   Relationships found: {len(result.causal_relationships)}")
        print(f"   Productivity impacts: {len(result.productivity_impacts)}")
        
    except Exception as e:
        print(f"❌ Causal analysis failed: {e}")

def test_oecd_integration():
    """Test OECD integration"""
    print("\nTesting OECD integration...")
    
    try:
        from data.oecd_realtime import OECDIntegration
        
        # Initialize OECD client
        oecd = OECDIntegration()
        print("✅ OECD client initialized")
        
        # Note: We won't actually fetch data to avoid API calls
        print("   (Skipping actual API fetch to avoid rate limits)")
        
    except Exception as e:
        print(f"❌ OECD integration failed: {e}")

def test_view_types():
    """Test view types configuration"""
    print("\nTesting view types...")
    
    try:
        from config.constants import VIEW_TYPES
        
        print(f"✅ VIEW_TYPES loaded: {len(VIEW_TYPES)} views")
        
        expected_views = ["Executive Dashboard", "Real-time Analysis"]
        for view in expected_views:
            if view in VIEW_TYPES:
                print(f"   ✅ {view} found in VIEW_TYPES")
            else:
                print(f"   ❌ {view} missing from VIEW_TYPES")
                
    except Exception as e:
        print(f"❌ VIEW_TYPES test failed: {e}")

def main():
    """Run all diagnostic tests"""
    print("AI Adoption Dashboard - Diagnostic Test")
    print("=" * 40)
    
    test_imports()
    test_causal_confidence()
    test_oecd_integration()
    test_view_types()
    
    print("\n" + "=" * 40)
    print("Diagnostic complete")

if __name__ == "__main__":
    main()