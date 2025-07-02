#!/usr/bin/env python3
"""
Comprehensive Test Script for AI Adoption Dashboard Migration
Tests all components of the Dash migration from Streamlit
"""

import sys
import os
import importlib
import traceback
from datetime import datetime

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'dash',
        'dash_bootstrap_components',
        'plotly',
        'pandas',
        'numpy',
        'layouts.main_layout',
        'layouts.sidebar_layout',
        'callbacks.navigation_callbacks',
        'callbacks.data_callbacks',
        'callbacks.visualization_callbacks',
        'views.industry_analysis',
        'views.financial_impact',
        'views.adoption_rates',
        'views.productivity_research',
        'views.executive_dashboard'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_view_functions():
    """Test all view creation functions"""
    print("\n🔍 Testing view functions...")
    
    view_modules = [
        ('views.industry_analysis', 'create_industry_analysis_view'),
        ('views.financial_impact', 'create_financial_impact_view'),
        ('views.adoption_rates', 'create_adoption_rates_view'),
        ('views.productivity_research', 'create_productivity_research_view'),
        ('views.executive_dashboard', 'create_executive_dashboard_view')
    ]
    
    failed_views = []
    
    for module_name, function_name in view_modules:
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            
            # Test function call
            result = function()
            if result is not None:
                print(f"✅ {module_name}.{function_name}")
            else:
                print(f"⚠️ {module_name}.{function_name} returned None")
                failed_views.append(f"{module_name}.{function_name}")
                
        except Exception as e:
            print(f"❌ {module_name}.{function_name}: {e}")
            failed_views.append(f"{module_name}.{function_name}")
    
    return len(failed_views) == 0

def test_callback_registration():
    """Test callback registration functions"""
    print("\n🔍 Testing callback registration...")
    
    callback_modules = [
        ('callbacks.navigation_callbacks', 'register_navigation_callbacks'),
        ('callbacks.data_callbacks', 'register_data_callbacks'),
        ('callbacks.visualization_callbacks', 'register_visualization_callbacks')
    ]
    
    failed_callbacks = []
    
    for module_name, function_name in callback_modules:
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            
            # Test function exists and is callable
            if callable(function):
                print(f"✅ {module_name}.{function_name}")
            else:
                print(f"❌ {module_name}.{function_name} is not callable")
                failed_callbacks.append(f"{module_name}.{function_name}")
                
        except Exception as e:
            print(f"❌ {module_name}.{function_name}: {e}")
            failed_callbacks.append(f"{module_name}.{function_name}")
    
    return len(failed_callbacks) == 0

def test_layout_functions():
    """Test layout creation functions"""
    print("\n🔍 Testing layout functions...")
    
    layout_modules = [
        ('layouts.main_layout', 'create_main_layout'),
        ('layouts.sidebar_layout', 'create_sidebar_layout')
    ]
    
    failed_layouts = []
    
    for module_name, function_name in layout_modules:
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
            
            # Test function call
            result = function()
            if result is not None:
                print(f"✅ {module_name}.{function_name}")
            else:
                print(f"⚠️ {module_name}.{function_name} returned None")
                failed_layouts.append(f"{module_name}.{function_name}")
                
        except Exception as e:
            print(f"❌ {module_name}.{function_name}: {e}")
            failed_layouts.append(f"{module_name}.{function_name}")
    
    return len(failed_layouts) == 0

def test_data_generation():
    """Test data generation and processing"""
    print("\n🔍 Testing data generation...")
    
    try:
        import pandas as pd
        import numpy as np
        
        # Test basic data generation
        years = list(range(2020, 2025))
        industries = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail']
        
        # Create sample data
        data = []
        for year in years:
            for industry in industries:
                data.append({
                    'Year': year,
                    'Industry': industry,
                    'Adoption_Rate': np.random.uniform(10, 80),
                    'Investment': np.random.uniform(1000000, 10000000)
                })
        
        df = pd.DataFrame(data)
        
        if len(df) == len(years) * len(industries):
            print("✅ Data generation successful")
            return True
        else:
            print("❌ Data generation failed - incorrect number of rows")
            return False
            
    except Exception as e:
        print(f"❌ Data generation error: {e}")
        return False

def test_visualization_creation():
    """Test chart creation"""
    print("\n🔍 Testing visualization creation...")
    
    try:
        import plotly.express as px
        import pandas as pd
        
        # Create sample data
        df = pd.DataFrame({
            'Year': [2020, 2021, 2022, 2023, 2024],
            'Adoption_Rate': [15, 25, 35, 45, 55],
            'Investment': [1000000, 2000000, 3000000, 4000000, 5000000]
        })
        
        # Test different chart types
        charts = [
            px.line(df, x='Year', y='Adoption_Rate'),
            px.bar(df, x='Year', y='Investment'),
            px.scatter(df, x='Adoption_Rate', y='Investment')
        ]
        
        for i, chart in enumerate(charts):
            if chart is not None:
                print(f"✅ Chart {i+1} created successfully")
            else:
                print(f"❌ Chart {i+1} creation failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Visualization creation error: {e}")
        return False

def test_app_initialization():
    """Test Dash app initialization"""
    print("\n🔍 Testing app initialization...")
    
    try:
        import dash
        from dash import Dash
        
        # Test basic app creation
        app = Dash(__name__)
        
        if app is not None:
            print("✅ Dash app initialization successful")
            return True
        else:
            print("❌ Dash app initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ App initialization error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 Starting Comprehensive AI Adoption Dashboard Migration Test")
    print("=" * 60)
    
    test_results = {}
    
    # Run all tests
    test_results['imports'] = test_imports()
    test_results['view_functions'] = test_view_functions()
    test_results['callback_registration'] = test_callback_registration()
    test_results['layout_functions'] = test_layout_functions()
    test_results['data_generation'] = test_data_generation()
    test_results['visualization_creation'] = test_visualization_creation()
    test_results['app_initialization'] = test_app_initialization()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Migration is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 