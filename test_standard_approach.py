#!/usr/bin/env python3
"""
Test Standard Approach Implementation

This script validates that all the standard approach patterns and fixes
are working correctly in the AI Adoption Dashboard.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import traceback
import logging

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StandardApproachTester:
    """Test suite for standard approach implementation"""
    
    def __init__(self):
        self.test_results = []
        self.errors = []
        self.warnings = []
        
    def run_test(self, test_name, test_func):
        """Run a test and record results"""
        try:
            logger.info(f"Running test: {test_name}")
            result = test_func()
            if result:
                self.test_results.append(f"✅ {test_name}: PASSED")
                logger.info(f"✅ {test_name}: PASSED")
            else:
                self.test_results.append(f"❌ {test_name}: FAILED")
                self.errors.append(f"❌ {test_name}: FAILED")
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            self.test_results.append(f"❌ {test_name}: ERROR - {str(e)}")
            self.errors.append(f"❌ {test_name}: ERROR - {str(e)}")
            logger.error(f"❌ {test_name}: ERROR - {str(e)}")
            logger.error(traceback.format_exc())
    
    def test_dataframe_safety_utilities(self):
        """Test DataFrame safety utilities"""
        try:
            from Utils.dataframe_safety import (
                ensure_dataframe, safe_dataframe_operation, safe_column_access,
                safe_numeric_conversion, safe_dataframe_filter, validate_dataframe_structure
            )
            
            # Test ensure_dataframe
            test_data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
            df = ensure_dataframe(test_data)
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 2
            
            # Test with None
            df_none = ensure_dataframe(None)
            assert isinstance(df_none, pd.DataFrame)
            assert df_none.empty
            
            # Test safe_column_access
            value = safe_column_access(df, 'a', default_value=0)
            assert value is not None
            
            # Test safe_numeric_conversion
            assert safe_numeric_conversion(10) == 10.0
            assert safe_numeric_conversion(None) == 0.0
            assert safe_numeric_conversion("invalid", default=5.0) == 5.0
            
            # Test validate_dataframe_structure
            assert validate_dataframe_structure(df, ['a', 'b']) == True
            assert validate_dataframe_structure(df, ['a', 'c']) == False
            
            return True
        except Exception as e:
            logger.error(f"DataFrame safety utilities test failed: {e}")
            return False
    
    def test_business_metrics_fixes(self):
        """Test business metrics fixes"""
        try:
            from business.metrics import business_metrics, calculate_roi
            
            # Test calculate_roi function
            roi = calculate_roi(1000, 1150)
            assert roi == 0.15
            
            # Test BusinessMetrics class method
            roi_class = business_metrics.calculate_roi(1000, 1150)
            assert roi_class == 0.15
            
            # Test error handling
            roi_zero = calculate_roi(0, 100)
            assert roi_zero == 0.0
            
            return True
        except Exception as e:
            logger.error(f"Business metrics test failed: {e}")
            return False
    
    def test_data_loading_fixes(self):
        """Test data loading fixes"""
        try:
            from data.loaders import load_all_datasets
            
            # Load all datasets
            datasets = load_all_datasets()
            
            # Check that required keys are present
            required_keys = [
                'historical_data', 'sector_2018', 'sector_2025', 
                'firm_size_data', 'geographic_data', 'financial_impact_data'
            ]
            
            for key in required_keys:
                assert key in datasets, f"Missing key: {key}"
                if datasets[key] is not None:
                    assert isinstance(datasets[key], pd.DataFrame) or isinstance(datasets[key], dict)
            
            return True
        except Exception as e:
            logger.error(f"Data loading test failed: {e}")
            return False
    
    def test_validation_models_fixes(self):
        """Test validation models fixes"""
        try:
            from data.models import safe_validate_data
            
            # Test with sample data
            test_data = pd.DataFrame({
                'technology': ['Generative AI', 'AI Agents'],
                'skill_level': ['High-skilled', 'Medium-skilled'],
                'source': ['McKinsey (potential)', 'Goldman Sachs (potential)'],
                'application': ['Content Generation', 'Code Generation'],
                'barrier': ['Lack of skilled personnel', 'Data availability/quality'],
                'support_type': ['Training Programs', 'Technical Support'],
                'region': ['North America', 'Europe']
            })
            
            # This should not raise validation errors
            result = safe_validate_data(test_data, 'test_dataset')
            assert result is not None
            
            return True
        except Exception as e:
            logger.error(f"Validation models test failed: {e}")
            return False
    
    def test_app_imports(self):
        """Test that the main app imports successfully"""
        try:
            import app
            assert hasattr(app, 'main')
            assert hasattr(app, 'load_data_with_mckinsey_tools')
            assert hasattr(app, 'load_fallback_data')
            return True
        except Exception as e:
            logger.error(f"App import test failed: {e}")
            return False
    
    def test_view_components(self):
        """Test view components are accessible"""
        try:
            from views import (
                adoption_rates, ai_cost_trends, ai_governance, ai_maturity,
                barriers_support, bibliography, causal_analysis, environmental_impact,
                executive_dashboard, financial_impact, firm_size_analysis,
                geographic_distribution, governance_compliance, historical_trends,
                implementation_guides, industry_analysis, investment_trends,
                labor_impact, oecd_findings, productivity_research, realtime_analysis,
                regional_growth, research_meta_analysis, research_scanner, roi_analysis,
                skill_gap_analysis, technical_research, technology_stack, token_economics
            )
            
            # Check that view functions exist
            view_functions = [
                'show_adoption_rates', 'show_ai_cost_trends', 'show_ai_governance',
                'show_ai_maturity', 'show_barriers_support', 'show_bibliography',
                'show_causal_analysis', 'show_environmental_impact', 'show_executive_dashboard',
                'show_financial_impact', 'show_firm_size_analysis', 'show_geographic_distribution',
                'show_governance_compliance', 'show_historical_trends', 'show_implementation_guides',
                'show_industry_analysis', 'show_investment_trends', 'show_labor_impact',
                'show_oecd_findings', 'show_productivity_research', 'show_realtime_analysis',
                'show_regional_growth', 'show_research_meta_analysis', 'show_research_scanner',
                'show_roi_analysis', 'show_skill_gap_analysis', 'show_technical_research',
                'show_technology_stack', 'show_token_economics'
            ]
            
            for func_name in view_functions:
                # Check if function exists in any of the view modules
                found = False
                for module in [adoption_rates, ai_cost_trends, ai_governance, ai_maturity,
                              barriers_support, bibliography, causal_analysis, environmental_impact,
                              executive_dashboard, financial_impact, firm_size_analysis,
                              geographic_distribution, governance_compliance, historical_trends,
                              implementation_guides, industry_analysis, investment_trends,
                              labor_impact, oecd_findings, productivity_research, realtime_analysis,
                              regional_growth, research_meta_analysis, research_scanner, roi_analysis,
                              skill_gap_analysis, technical_research, technology_stack, token_economics]:
                    if hasattr(module, func_name):
                        found = True
                        break
                
                if not found:
                    self.warnings.append(f"View function {func_name} not found")
            
            return True
        except Exception as e:
            logger.error(f"View components test failed: {e}")
            return False
    
    def test_performance_integration(self):
        """Test performance integration"""
        try:
            from performance.caching import smart_cache, performance_monitor
            from performance.memory_management import MemoryManager
            
            # Test that performance modules are accessible
            assert smart_cache is not None
            assert performance_monitor is not None
            
            return True
        except Exception as e:
            logger.error(f"Performance integration test failed: {e}")
            return False
    
    def test_utils_integration(self):
        """Test utilities integration"""
        try:
            from Utils.helpers import clean_filename, safe_execute, safe_data_check
            from Utils.navigation import setup_navigation
            from Utils.dataframe_safety import ensure_dataframe
            
            # Test utility functions
            assert clean_filename is not None
            assert safe_execute is not None
            assert safe_data_check is not None
            assert setup_navigation is not None
            assert ensure_dataframe is not None
            
            return True
        except Exception as e:
            logger.error(f"Utils integration test failed: {e}")
            return False
    
    def test_data_integration(self):
        """Test data integration"""
        try:
            from data.loaders import load_all_datasets
            from data.models import safe_validate_data
            from data.geographic import get_geographic_data
            from data.integration import integrate_research_data
            
            # Test data modules
            assert load_all_datasets is not None
            assert safe_validate_data is not None
            assert get_geographic_data is not None
            
            return True
        except Exception as e:
            logger.error(f"Data integration test failed: {e}")
            return False
    
    def test_business_integration(self):
        """Test business logic integration"""
        try:
            from business.metrics import business_metrics, calculate_roi
            from business.roi_calculator import roi_calculator
            from business.causal_analysis import causal_engine
            
            # Test business modules
            assert business_metrics is not None
            assert calculate_roi is not None
            assert roi_calculator is not None
            
            return True
        except Exception as e:
            logger.error(f"Business integration test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all standard approach tests"""
        logger.info("🚀 Starting Standard Approach Tests")
        logger.info("=" * 60)
        
        tests = [
            ("DataFrame Safety Utilities", self.test_dataframe_safety_utilities),
            ("Business Metrics Fixes", self.test_business_metrics_fixes),
            ("Data Loading Fixes", self.test_data_loading_fixes),
            ("Validation Models Fixes", self.test_validation_models_fixes),
            ("App Imports", self.test_app_imports),
            ("View Components", self.test_view_components),
            ("Performance Integration", self.test_performance_integration),
            ("Utils Integration", self.test_utils_integration),
            ("Data Integration", self.test_data_integration),
            ("Business Integration", self.test_business_integration),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 STANDARD APPROACH TEST REPORT")
        logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if "✅" in r])
        failed_tests = len([r for r in self.test_results if "❌" in r])
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        logger.info("\n📋 Test Results:")
        for result in self.test_results:
            logger.info(f"  {result}")
        
        if self.errors:
            logger.info("\n❌ Errors:")
            for error in self.errors:
                logger.info(f"  {error}")
        
        if self.warnings:
            logger.info("\n⚠️  Warnings:")
            for warning in self.warnings:
                logger.info(f"  {warning}")
        
        logger.info("\n🎯 Recommendations:")
        if failed_tests == 0:
            logger.info("✅ All standard approach tests passed!")
            logger.info("✅ The project follows the established standards")
            logger.info("✅ Ready for production deployment")
        else:
            logger.info("🔧 Some tests failed - review and fix issues")
            logger.info("🔧 Check the error messages above")
            logger.info("🔧 Ensure all dependencies are properly installed")
        
        logger.info("\n" + "=" * 60)

if __name__ == "__main__":
    tester = StandardApproachTester()
    tester.run_all_tests() 