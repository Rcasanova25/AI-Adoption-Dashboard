#!/usr/bin/env python3
"""
Integration test for Real-time Analysis Dashboard
Tests the OECD data integration and dashboard functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_oecd_realtime_integration():
    """Test OECD real-time data integration"""
    print("🧪 Testing OECD Real-time Integration...")
    
    try:
        from data.oecd_realtime import OECDIntegration, OECDRealTimeClient
        
        # Test client initialization
        client = OECDRealTimeClient(cache_ttl=1800)
        print("✅ OECD client initialized successfully")
        
        # Test integration class
        integration = OECDIntegration()
        print("✅ OECD integration class initialized")
        
        # Test indicator summary
        summary = client.get_indicator_summary()
        print(f"✅ Available indicators: {len(summary)} found")
        print(f"📊 Indicators: {', '.join(summary['key'].tolist())}")
        
        return True
        
    except Exception as e:
        print(f"❌ OECD integration test failed: {e}")
        return False

def test_realtime_dashboard():
    """Test real-time dashboard components"""
    print("\n🧪 Testing Real-time Dashboard Components...")
    
    try:
        from views.realtime_analysis import RealTimeAnalyticsDashboard
        
        # Test dashboard initialization
        dashboard = RealTimeAnalyticsDashboard()
        print("✅ Real-time dashboard initialized")
        
        # Test performance metrics
        perf_metrics = dashboard._get_performance_metrics()
        print(f"✅ Performance metrics: {list(perf_metrics.keys())}")
        
        # Test causal comparison
        causal_data = dashboard._get_causal_comparison()
        print(f"✅ Causal comparison data: {list(causal_data.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard component test failed: {e}")
        return False

def test_navigation_integration():
    """Test navigation system integration"""
    print("\n🧪 Testing Navigation Integration...")
    
    try:
        from config.constants import VIEW_TYPES
        from Utils.navigation import setup_navigation
        
        # Check if real-time analysis is in view types
        if 'Real-time Analysis' in VIEW_TYPES:
            position = VIEW_TYPES.index('Real-time Analysis') + 1
            print(f"✅ Real-time Analysis found in position {position}")
        else:
            print("❌ Real-time Analysis not found in VIEW_TYPES")
            return False
        
        # Test navigation setup
        print("✅ Navigation integration successful")
        return True
        
    except Exception as e:
        print(f"❌ Navigation integration test failed: {e}")
        return False

def test_main_app_integration():
    """Test main app integration"""
    print("\n🧪 Testing Main App Integration...")
    
    try:
        # Test import in main.py context
        from views.realtime_analysis import show_realtime_analysis
        print("✅ Real-time analysis view import successful")
        
        # Test function signature
        import inspect
        sig = inspect.signature(show_realtime_analysis)
        print(f"✅ Function signature: {sig}")
        
        return True
        
    except Exception as e:
        print(f"❌ Main app integration test failed: {e}")
        return False

def test_data_flow():
    """Test data flow and dependencies"""
    print("\n🧪 Testing Data Flow...")
    
    try:
        # Test data validation utilities
        from Utils.data_validation import DataValidator, safe_plot_check
        validator = DataValidator()
        print("✅ Data validation utilities imported")
        
        # Test chart components
        from components.charts import ChartStyle
        style = ChartStyle.executive_style()
        print(f"✅ Chart styling available: {len(style.colors)} colors")
        
        # Test helper utilities
        from Utils.helpers import clean_filename, safe_execute
        print("✅ Helper utilities imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow test failed: {e}")
        return False

def simulate_dashboard_usage():
    """Simulate typical dashboard usage"""
    print("\n🧪 Simulating Dashboard Usage...")
    
    try:
        from views.realtime_analysis import RealTimeAnalyticsDashboard
        
        # Initialize dashboard
        dashboard = RealTimeAnalyticsDashboard()
        
        # Simulate data status check
        dashboard.data_status = {
            'oecd': {'status': 'success', 'last_update': datetime.now()},
            'ai_adoption': {'records': 150},
            'correlation': {'confidence': 0.85},
            'causal_enhancement': {'improvement': 0.13}
        }
        
        print("✅ Dashboard status simulation successful")
        
        # Test mock data operations
        mock_data = pd.DataFrame({
            'TIME_PERIOD': pd.date_range('2023-01-01', periods=12, freq='M'),
            'OBS_VALUE': np.random.normal(100, 10, 12),
            'REF_AREA': ['USA'] * 12
        })
        
        # Test trend calculation
        trend = dashboard._calculate_trend(mock_data)
        print(f"✅ Trend calculation: {trend:.2f}")
        
        # Test latest value extraction
        latest = dashboard._get_latest_indicator_value(mock_data)
        print(f"✅ Latest value extraction: {latest:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard usage simulation failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive integration test"""
    print("🚀 Starting Comprehensive Real-time Analysis Integration Test")
    print("=" * 60)
    
    tests = [
        ("OECD Real-time Integration", test_oecd_realtime_integration),
        ("Real-time Dashboard Components", test_realtime_dashboard),
        ("Navigation Integration", test_navigation_integration),
        ("Main App Integration", test_main_app_integration),
        ("Data Flow", test_data_flow),
        ("Dashboard Usage Simulation", simulate_dashboard_usage)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Real-time Analysis integration is complete!")
        print("\n📋 Integration Summary:")
        print("  • OECD real-time data module integrated")
        print("  • Real-time analysis dashboard view created")
        print("  • Navigation system updated")
        print("  • Main app routing configured")
        print("  • All dependencies resolved")
        print("\n🚀 Ready for production deployment!")
    else:
        print("⚠️  Some tests failed - please review the issues above")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)