#!/usr/bin/env python3
"""
Test script to verify all Dash views are working correctly.
"""

import sys
import os
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class ViewTester:
    """Test all converted Dash views."""
    
    def __init__(self):
        self.test_results = []
        self.mock_data = self.create_mock_data()
        
    def create_mock_data(self) -> Dict:
        """Create mock data for testing views."""
        return {
            "_metadata": {
                "loaded_at": "2025-01-01T00:00:00",
                "successful_loads": 25,
                "total_datasets": 25
            },
            "ai_index_adoption_rates": {
                "data": None,
                "metadata": {"source": "Mock Data"}
            },
            "mckinsey_financial_impact": {
                "data": None,
                "metadata": {"source": "Mock Data"}
            }
        }
    
    def test_single_view(self, view_name: str, module_path: str) -> Tuple[bool, str]:
        """Test a single view."""
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Check if create_layout function exists
            if not hasattr(module, 'create_layout'):
                return False, "Missing create_layout function"
            
            # Try to create layout
            layout = module.create_layout(self.mock_data, "General")
            
            # Check if layout is not None
            if layout is None:
                return False, "create_layout returned None"
            
            return True, "Success"
            
        except ImportError as e:
            return False, f"Import error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_all_views(self):
        """Test all views in the view manager."""
        try:
            from dash_view_manager import DashViewManager
            view_manager = DashViewManager()
        except ImportError:
            logger.error("❌ Could not import DashViewManager")
            return
        
        logger.info("Testing all Dash views...")
        logger.info("=" * 60)
        
        # Group by category for organized output
        categories = {}
        for view_id, view_info in view_manager.all_views.items():
            category = view_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((view_id, view_info))
        
        # Test each category
        total_views = 0
        passed_views = 0
        
        for category, views in sorted(categories.items()):
            logger.info(f"\n{category.upper()} Views:")
            logger.info("-" * 40)
            
            for view_id, view_info in views:
                total_views += 1
                module_path = view_info["module"]
                label = view_info["label"]
                
                # Test the view
                success, message = self.test_single_view(view_id, module_path)
                
                if success:
                    logger.info(f"✅ {label:30} - {message}")
                    passed_views += 1
                else:
                    logger.info(f"❌ {label:30} - {message}")
                
                self.test_results.append({
                    "view_id": view_id,
                    "label": label,
                    "module": module_path,
                    "success": success,
                    "message": message
                })
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("TEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total views tested: {total_views}")
        logger.info(f"Passed: {passed_views}")
        logger.info(f"Failed: {total_views - passed_views}")
        logger.info(f"Success rate: {(passed_views/total_views*100):.1f}%")
        
        # List failed views
        failed = [r for r in self.test_results if not r["success"]]
        if failed:
            logger.info("\nFailed views:")
            for result in failed:
                logger.info(f"  - {result['label']}: {result['message']}")
        
        return passed_views == total_views
    
    def generate_report(self):
        """Generate a detailed test report."""
        report_path = Path("VIEW_TEST_REPORT.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Dash View Test Report\n\n")
            f.write("## Summary\n\n")
            
            total = len(self.test_results)
            if total == 0:
                f.write("No views were tested due to import errors.\n")
                return
                
            passed = sum(1 for r in self.test_results if r["success"])
            
            f.write(f"- Total views: {total}\n")
            f.write(f"- Passed: {passed}\n")
            f.write(f"- Failed: {total - passed}\n")
            f.write(f"- Success rate: {(passed/total*100):.1f}%\n\n")
            
            f.write("## Detailed Results\n\n")
            
            # Group by success/failure
            f.write("### ✅ Passed Views\n\n")
            for result in self.test_results:
                if result["success"]:
                    f.write(f"- {result['label']} (`{result['module']}`)\n")
            
            f.write("\n### ❌ Failed Views\n\n")
            for result in self.test_results:
                if not result["success"]:
                    f.write(f"- {result['label']} (`{result['module']}`)\n")
                    f.write(f"  - Error: {result['message']}\n")
            
            f.write("\n## Next Steps\n\n")
            if passed < total:
                f.write("1. Fix the failed views by checking their imports and syntax\n")
                f.write("2. Ensure all views have a `create_layout` function\n")
                f.write("3. Test views individually with real data\n")
            else:
                f.write("1. All views passed basic tests!\n")
                f.write("2. Test with real data to ensure full functionality\n")
                f.write("3. Customize each view with specific logic from originals\n")
        
        logger.info(f"\n📄 Test report saved to: {report_path}")


def main():
    """Run the view tests."""
    tester = ViewTester()
    
    # Test all views
    all_passed = tester.test_all_views()
    
    # Generate report
    tester.generate_report()
    
    if all_passed:
        logger.info("\n🎉 All views passed basic tests!")
        logger.info("The Dash migration is ready for further customization.")
    else:
        logger.info("\n⚠️ Some views need fixes. Check the report for details.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())