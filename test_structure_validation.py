#!/usr/bin/env python3
"""
Simple Structure Validation Test
Tests our authentic data integration structure without requiring external dependencies
"""

import sys
import os
from pathlib import Path

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    project_root = Path(__file__).parent
    
    required_files = [
        'data/research_integration.py',
        'data/loaders.py',
        'data/models.py',
        'main.py',
        'config/constants.py',
        'config/settings.py'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - NOT FOUND")
    
    print(f"\n📊 File structure: {len(existing_files)}/{len(required_files)} files found")
    
    return len(missing_files) == 0, missing_files

def test_research_integration_content():
    """Test research integration file content"""
    print("\n🔍 Testing research_integration.py content...")
    
    try:
        research_file = Path(__file__).parent / 'data' / 'research_integration.py'
        
        if not research_file.exists():
            print("❌ research_integration.py not found")
            return False
            
        content = research_file.read_text()
        
        # Check for key components
        checks = [
            ('ResearchDataIntegrator class', 'class ResearchDataIntegrator'),
            ('Stanford AI Index method', 'get_authentic_historical_data'),
            ('McKinsey Survey method', 'get_authentic_sector_data_2025'),
            ('Goldman Sachs method', 'get_authentic_gdp_impact_data'),
            ('Federal Reserve method', 'get_authentic_productivity_data'),
            ('Data source attribution', 'data_source'),
            ('Credibility metrics', 'get_data_lineage_report'),
            ('Source mapping', 'data_sources')
        ]
        
        passed_checks = 0
        
        for check_name, search_string in checks:
            if search_string in content:
                print(f"✅ {check_name}")
                passed_checks += 1
            else:
                print(f"❌ {check_name} - NOT FOUND")
        
        print(f"\n📊 Content validation: {passed_checks}/{len(checks)} checks passed")
        
        return passed_checks == len(checks)
        
    except Exception as e:
        print(f"❌ Error reading research_integration.py: {e}")
        return False

def test_loaders_integration():
    """Test that loaders.py has been updated with authentic data integration"""
    print("\n🔍 Testing loaders.py integration...")
    
    try:
        loaders_file = Path(__file__).parent / 'data' / 'loaders.py'
        
        if not loaders_file.exists():
            print("❌ loaders.py not found")
            return False
            
        content = loaders_file.read_text()
        
        # Check for authentic data integration
        checks = [
            ('Research integration import', 'from .research_integration import'),
            ('Authentic historical data', 'research_integrator.get_authentic_historical_data'),
            ('Authentic sector data', 'research_integrator.get_authentic_sector_data_2025'),
            ('Stanford AI Index attribution', 'Stanford AI Index 2025'),
            ('McKinsey attribution', 'McKinsey Global Survey'),
            ('Fallback system', 'fallback_data'),
            ('Source transparency', 'data_source')
        ]
        
        passed_checks = 0
        
        for check_name, search_string in checks:
            if search_string in content:
                print(f"✅ {check_name}")
                passed_checks += 1
            else:
                print(f"❌ {check_name} - NOT FOUND")
        
        print(f"\n📊 Loaders integration: {passed_checks}/{len(checks)} checks passed")
        
        return passed_checks == len(checks)
        
    except Exception as e:
        print(f"❌ Error reading loaders.py: {e}")
        return False

def test_main_integration():
    """Test that main.py has been updated for authentic data"""
    print("\n🔍 Testing main.py integration...")
    
    try:
        main_file = Path(__file__).parent / 'main.py'
        
        if not main_file.exists():
            print("❌ main.py not found")
            return False
            
        content = main_file.read_text()
        
        # Check for authentic data integration
        checks = [
            ('Research integration import', 'from data.research_integration import'),
            ('Authentic data loading', 'load_authentic_research_datasets'),
            ('Credibility metrics', 'get_data_credibility_metrics'),
            ('Authenticity dashboard', 'display_data_authenticity_dashboard'),
            ('Authentic research data loading', 'load_authentic_dashboard_data'),
            ('Source attribution UI', 'authentic research data from Stanford'),
            ('Data authenticity verification', 'Data Authenticity Verification')
        ]
        
        passed_checks = 0
        
        for check_name, search_string in checks:
            if search_string in content:
                print(f"✅ {check_name}")
                passed_checks += 1
            else:
                print(f"❌ {check_name} - NOT FOUND")
        
        print(f"\n📊 Main.py integration: {passed_checks}/{len(checks)} checks passed")
        
        return passed_checks == len(checks)
        
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

def test_data_source_documentation():
    """Test that data sources are properly documented"""
    print("\n🔍 Testing data source documentation...")
    
    try:
        research_file = Path(__file__).parent / 'data' / 'research_integration.py'
        content = research_file.read_text()
        
        # Check for authoritative sources
        sources = [
            ('Stanford AI Index Report 2025', 'Stanford HAI'),
            ('McKinsey Global Survey', 'McKinsey & Company'),
            ('Goldman Sachs Research', 'Goldman Sachs'),
            ('Federal Reserve Research', 'Federal Reserve Bank of Richmond')
        ]
        
        documented_sources = 0
        
        for source_name, authority in sources:
            if source_name in content and authority in content:
                print(f"✅ {authority}: {source_name}")
                documented_sources += 1
            else:
                print(f"❌ {authority}: {source_name} - NOT DOCUMENTED")
        
        print(f"\n📊 Source documentation: {documented_sources}/{len(sources)} sources documented")
        
        return documented_sources == len(sources)
        
    except Exception as e:
        print(f"❌ Error checking source documentation: {e}")
        return False

def run_structure_tests():
    """Run all structure validation tests"""
    print("🚀 Starting Structure Validation Test Suite")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Research Integration Content", test_research_integration_content),
        ("Loaders Integration", test_loaders_integration),
        ("Main.py Integration", test_main_integration),
        ("Data Source Documentation", test_data_source_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            # Handle tuple return from test_file_structure
            if isinstance(result, tuple):
                result = result[0]
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 STRUCTURE VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({(passed/total)*100:.0f}%)")
    
    if passed == total:
        print("🎉 ALL STRUCTURE TESTS PASSED!")
        print("\n✅ Authentic data integration structure is complete")
        print("✅ File structure is correct") 
        print("✅ Integration points are implemented")
        print("✅ Source attribution is documented")
        print("\n🚀 READY FOR DASHBOARD TESTING:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run dashboard: streamlit run main.py")
        print("   3. Verify authentic data loading and source attribution")
    else:
        print("⚠️ Structure validation failed - fix issues before dashboard testing")
        print("\n🔧 Next steps:")
        print("   1. Review failed tests above")
        print("   2. Fix missing files or integration points")
        print("   3. Re-run this validation script")
    
    return passed == total

if __name__ == "__main__":
    success = run_structure_tests()
    sys.exit(0 if success else 1)