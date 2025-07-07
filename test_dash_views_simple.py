#!/usr/bin/env python3
"""
Simple test script to verify Dash views work.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_views():
    """Test a few key views."""
    print("Testing Dash views...")
    print("=" * 60)
    
    # Mock data
    mock_data = {
        "_metadata": {"loaded_at": "2025-01-01", "successful_loads": 25}
    }
    
    # Test views
    test_cases = [
        ("views.adoption.adoption_rates_dash", "Adoption Rates"),
        ("views.adoption.historical_trends_dash", "Historical Trends"),
        ("views.economic.financial_impact_dash", "Financial Impact"),
        ("views.geographic.geographic_distribution_dash", "Geographic Distribution")
    ]
    
    passed = 0
    total = len(test_cases)
    
    for module_path, name in test_cases:
        try:
            # Import module
            module = __import__(module_path, fromlist=['create_layout'])
            
            # Test create_layout
            layout = module.create_layout(mock_data, "General")
            
            if layout is not None:
                print(f"✅ {name:30} - Success")
                passed += 1
            else:
                print(f"❌ {name:30} - create_layout returned None")
                
        except Exception as e:
            print(f"❌ {name:30} - Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} views passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = test_views()
    sys.exit(0 if success else 1)