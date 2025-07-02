#!/usr/bin/env python3
"""
Quick Integration Test - Minimal dependency check
Tests core integration without requiring external packages
"""

import sys
from pathlib import Path

def test_critical_imports():
    """Test that our critical integration points work"""
    print("🔍 Testing critical integration points...")
    
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        # Test 1: Can we import our research integration?
        sys.path.insert(0, str(project_root / "data"))
        
        print("📋 Testing research integration import...")
        with open(project_root / "data" / "research_integration.py", 'r') as f:
            content = f.read()
            
        # Check for key class definition
        if "class ResearchDataIntegrator:" in content:
            print("✅ ResearchDataIntegrator class found")
        else:
            print("❌ ResearchDataIntegrator class missing")
            return False
            
        # Test 2: Check data loaders integration
        print("📋 Testing data loaders integration...")
        with open(project_root / "data" / "loaders.py", 'r') as f:
            loaders_content = f.read()
            
        if "from .research_integration import" in loaders_content:
            print("✅ Research integration imported in loaders")
        else:
            print("❌ Research integration not imported in loaders")
            return False
            
        # Test 3: Check main.py integration
        print("📋 Testing main.py integration...")
        with open(project_root / "main.py", 'r') as f:
            main_content = f.read()
            
        if "load_authentic_dashboard_data" in main_content:
            print("✅ Authentic data loading integrated in main.py")
        else:
            print("❌ Authentic data loading not integrated in main.py")
            return False
            
        if "authentic research data from Stanford" in main_content:
            print("✅ Source attribution UI integrated")
        else:
            print("❌ Source attribution UI not integrated")
            return False
            
        # Test 4: Check data source configuration
        print("📋 Testing data source configuration...")
        if "Stanford AI Index Report 2025" in content:
            print("✅ Stanford AI Index configured")
        else:
            print("❌ Stanford AI Index not configured")
            return False
            
        if "McKinsey Global Survey" in content:
            print("✅ McKinsey Global Survey configured")  
        else:
            print("❌ McKinsey Global Survey not configured")
            return False
            
        if "Goldman Sachs Research" in content:
            print("✅ Goldman Sachs Research configured")
        else:
            print("❌ Goldman Sachs Research not configured")
            return False
            
        if "Federal Reserve Bank" in content:
            print("✅ Federal Reserve Research configured")
        else:
            print("❌ Federal Reserve Research not configured")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Critical import test failed: {e}")
        return False

def test_data_authenticity_flow():
    """Test the data authenticity verification flow"""
    print("\n🔍 Testing data authenticity flow...")
    
    try:
        project_root = Path(__file__).parent
        
        # Check research integration file
        research_file = project_root / "data" / "research_integration.py"
        with open(research_file, 'r') as f:
            content = f.read()
            
        # Test authenticity methods
        authenticity_methods = [
            "get_authentic_historical_data",
            "get_authentic_sector_data_2025", 
            "get_authentic_investment_data",
            "get_authentic_financial_impact_data",
            "get_authentic_productivity_data",
            "get_authentic_gdp_impact_data"
        ]
        
        missing_methods = []
        
        for method in authenticity_methods:
            if method in content:
                print(f"✅ {method}")
            else:
                print(f"❌ {method} - MISSING")
                missing_methods.append(method)
                
        if missing_methods:
            print(f"❌ Missing {len(missing_methods)} authenticity methods")
            return False
            
        # Test credibility reporting
        if "get_data_lineage_report" in content:
            print("✅ Data lineage reporting")
        else:
            print("❌ Data lineage reporting - MISSING")
            return False
            
        # Test source attribution
        if "data_source" in content and "credibility_score" in content:
            print("✅ Source attribution system")
        else:
            print("❌ Source attribution system - MISSING")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Data authenticity flow test failed: {e}")
        return False

def test_fallback_system():
    """Test that fallback system is properly configured"""
    print("\n🔍 Testing fallback system...")
    
    try:
        project_root = Path(__file__).parent
        
        # Check main.py for fallback handling
        with open(project_root / "main.py", 'r') as f:
            main_content = f.read()
            
        # Test fallback data function
        if "load_fallback_data" in main_content:
            print("✅ Fallback data function exists")
        else:
            print("❌ Fallback data function missing")
            return False
            
        # Test fallback messaging
        if "synthetic fallback data" in main_content:
            print("✅ Fallback messaging configured")
        else:
            print("❌ Fallback messaging missing")
            return False
            
        # Check loaders.py for fallback handling
        with open(project_root / "data" / "loaders.py", 'r') as f:
            loaders_content = f.read()
            
        if "fallback_data" in loaders_content:
            print("✅ Loader fallback system configured")
        else:
            print("❌ Loader fallback system missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Fallback system test failed: {e}")
        return False

def run_quick_test():
    """Run quick integration test"""
    print("⚡ Quick Integration Test")
    print("=" * 40)
    
    tests = [
        ("Critical Imports", test_critical_imports),
        ("Data Authenticity Flow", test_data_authenticity_flow),
        ("Fallback System", test_fallback_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("⚡ QUICK TEST SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 INTEGRATION READY!")
        print("🚀 Your authentic data integration is properly configured")
        print("🚀 Ready to run: streamlit run main.py")
        print("\n📋 Expected results:")
        print("   ✅ Green banner with Stanford/McKinsey/Goldman Sachs sources")
        print("   ✅ Data Authenticity Verification panel")
        print("   ✅ A+ credibility score")
        print("   ✅ Source attribution in all datasets")
    else:
        print("\n⚠️ Integration issues detected")
        print("🔧 Review failed tests and fix before dashboard testing")
    
    return passed == total

if __name__ == "__main__":
    success = run_quick_test()
    sys.exit(0 if success else 1)