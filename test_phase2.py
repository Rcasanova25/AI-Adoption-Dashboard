"""Test script for Phase 2 components."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
try:
    from components.economic_insights import EconomicInsights, CompetitiveIntelligence
    print("✓ Economic insights module imported successfully")
except Exception as e:
    print(f"✗ Error importing economic insights: {e}")

try:
    from components.competitive_assessor import CompetitivePositionAssessor
    print("✓ Competitive assessor module imported successfully")
except Exception as e:
    print(f"✗ Error importing competitive assessor: {e}")

try:
    from components.view_enhancements import ViewEnhancer
    print("✓ View enhancements module imported successfully")
except Exception as e:
    print(f"✗ Error importing view enhancements: {e}")

# Test basic functionality
try:
    import pandas as pd
    
    # Create test data
    test_adoption = pd.DataFrame({
        'year': [2023, 2024, 2025],
        'overall_adoption': [60, 75, 87.3],
        'genai_adoption': [40, 55, 70.5]
    })
    
    # Test insight generation
    insights = EconomicInsights()
    result = insights.generate_adoption_insights(test_adoption)
    print(f"✓ Generated adoption insights: {len(result['key_points'])} key points")
    
    # Test cost calculation
    costs = insights.calculate_cost_of_inaction("Large", "Technology", 6, 50)
    print(f"✓ Calculated cost of inaction: ${costs['total_cost']:,.0f}")
    
except Exception as e:
    print(f"✗ Error testing functionality: {e}")

print("\nPhase 2 component validation complete!")