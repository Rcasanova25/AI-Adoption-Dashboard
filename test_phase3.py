"""Test script for Phase 3 UI/UX components."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
print("Testing Phase 3 component imports...\n")

try:
    from components.progressive_disclosure import ProgressiveDisclosure, DisclosureLevel
    print("✓ Progressive disclosure module imported successfully")
except Exception as e:
    print(f"✗ Error importing progressive disclosure: {e}")

try:
    from components.guided_tour import GuidedTour, UserLevel
    print("✓ Guided tour module imported successfully")
except Exception as e:
    print(f"✗ Error importing guided tour: {e}")

try:
    from components.persona_dashboards import PersonaDashboards
    print("✓ Persona dashboards module imported successfully")
except Exception as e:
    print(f"✗ Error importing persona dashboards: {e}")

try:
    from components.key_takeaways import KeyTakeawaysGenerator, Takeaway
    print("✓ Key takeaways module imported successfully")
except Exception as e:
    print(f"✗ Error importing key takeaways: {e}")

try:
    from components.mobile_responsive import ResponsiveUI
    print("✓ Mobile responsive module imported successfully")
except Exception as e:
    print(f"✗ Error importing mobile responsive: {e}")

# Test basic functionality
print("\nTesting basic functionality...\n")

try:
    # Test takeaway generation
    generator = KeyTakeawaysGenerator()
    test_data = {
        'current_adoption': 75,
        'yoy_growth': 15,
        'industry_average': 80
    }
    takeaways = generator.generate_takeaways('adoption_rates', test_data)
    print(f"✓ Generated {len(takeaways)} takeaways")
    
    # Test persona config
    personas = PersonaDashboards()
    executive = personas.personas['Executive']
    print(f"✓ Executive persona configured with {len(executive.primary_metrics)} primary metrics")
    
except Exception as e:
    print(f"✗ Error testing functionality: {e}")

print("\nPhase 3 component validation complete!")