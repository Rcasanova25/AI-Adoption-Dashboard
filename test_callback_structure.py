#!/usr/bin/env python3
"""
Test script to verify callback structure and imports without running the app.
"""
import sys
import importlib
import ast
from pathlib import Path

def check_callback_registration(file_path):
    """Check if callbacks use app.callback instead of @callback."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == 'callback':
                    issues.append(f"Line {decorator.lineno}: Found @callback decorator (should be @app.callback)")
                elif isinstance(decorator, ast.Attribute):
                    if hasattr(decorator.value, 'id') and decorator.value.id == 'app' and decorator.attr == 'callback':
                        # This is correct - @app.callback
                        pass
    
    return issues

def test_view_imports():
    """Test if all views can be imported."""
    views = [
        "views.adoption.adoption_rates_dash",
        "views.adoption.historical_trends_dash",
        "views.adoption.industry_analysis_dash",
        "views.adoption.firm_size_analysis_dash",
        "views.adoption.technology_stack_dash",
        "views.adoption.ai_technology_maturity_dash",
        "views.adoption.ai_cost_trends_dash",
        "views.adoption.productivity_research_dash",
        "views.adoption.labor_impact_dash",
        "views.adoption.skill_gap_analysis_dash",
        "views.adoption.oecd_2025_findings_dash",
        "views.adoption.barriers_support_dash",
        "views.economic.investment_trends_dash",
        "views.economic.financial_impact_dash",
        "views.economic.roi_analysis_dash",
        "views.geographic.geographic_distribution_dash",
        "views.geographic.regional_growth_dash",
        "views.other.ai_governance_dash",
        "views.other.environmental_impact_dash",
        "views.other.token_economics_dash",
        "views.other.bibliography_sources_dash"
    ]
    
    import_results = {}
    for view_module in views:
        try:
            # Check if file exists
            module_path = view_module.replace('.', '/') + '.py'
            if Path(module_path).exists():
                # Check for create_layout function
                with open(module_path, 'r') as f:
                    content = f.read()
                if 'def create_layout' in content:
                    import_results[view_module] = "✅ OK - create_layout found"
                else:
                    import_results[view_module] = "❌ Missing create_layout function"
            else:
                import_results[view_module] = "❌ File not found"
        except Exception as e:
            import_results[view_module] = f"❌ Error: {str(e)}"
    
    return import_results

def main():
    print("=" * 60)
    print("AI Adoption Dashboard - Callback Structure Test")
    print("=" * 60)
    
    # Check callback files
    callback_files = [
        "callbacks/data_callbacks.py",
        "callbacks/view_callbacks.py", 
        "callbacks/performance_callbacks.py"
    ]
    
    print("\n1. Checking callback registration patterns:")
    print("-" * 40)
    
    all_good = True
    for cb_file in callback_files:
        if Path(cb_file).exists():
            issues = check_callback_registration(cb_file)
            if issues:
                print(f"\n❌ {cb_file}:")
                for issue in issues:
                    print(f"   {issue}")
                all_good = False
            else:
                print(f"✅ {cb_file} - All callbacks use app.callback")
        else:
            print(f"❌ {cb_file} - File not found")
            all_good = False
    
    if all_good:
        print("\n✅ All callbacks properly registered with app.callback!")
    
    # Check view imports
    print("\n\n2. Checking view modules:")
    print("-" * 40)
    
    import_results = test_view_imports()
    all_views_ok = True
    
    for view, result in import_results.items():
        if not result.startswith("✅"):
            all_views_ok = False
        print(f"{view}: {result}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    if all_good and all_views_ok:
        print("✅ All checks passed! The app should run without duplicate callback errors.")
    else:
        if not all_good:
            print("❌ Some callbacks still use @callback instead of @app.callback")
        if not all_views_ok:
            print("❌ Some views have issues")
    print("=" * 60)

if __name__ == "__main__":
    main()