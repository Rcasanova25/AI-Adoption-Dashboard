#!/usr/bin/env python3
"""
Comprehensive Test Script for AI Adoption Dashboard
Tests all functionality and identifies issues with data sources and implementation
"""

import sys
import os
import traceback
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveTester:
    """Comprehensive tester for AI Adoption Dashboard"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.successes = []
        self.test_results = {}
        
    def log_error(self, test_name: str, error: str, details: str = ""):
        """Log an error"""
        self.errors.append({
            'test': test_name,
            'error': error,
            'details': details
        })
        logger.error(f"❌ {test_name}: {error}")
        if details:
            logger.error(f"   Details: {details}")
    
    def log_warning(self, test_name: str, warning: str, details: str = ""):
        """Log a warning"""
        self.warnings.append({
            'test': test_name,
            'warning': warning,
            'details': details
        })
        logger.warning(f"⚠️ {test_name}: {warning}")
        if details:
            logger.warning(f"   Details: {details}")
    
    def log_success(self, test_name: str, message: str = ""):
        """Log a success"""
        self.successes.append({
            'test': test_name,
            'message': message
        })
        logger.info(f"✅ {test_name}: {message}")
    
    def test_project_structure(self) -> bool:
        """Test project structure and file organization"""
        logger.info("🔍 Testing project structure...")
        
        required_dirs = [
            'data', 'business', 'views', 'Utils', 'components', 
            'config', 'core', 'exports', 'performance', 'realtime',
            'visualization', 'tests', 'AI adoption resources'
        ]
        
        required_files = [
            'app.py', 'main.py', 'requirements.txt', 'README.md',
            'data/loaders.py', 'data/models.py', 'data/research_integration.py',
            'business/metrics.py', 'business/roi_calculator.py',
            'Utils/data_validation.py', 'Utils/helpers.py'
        ]
        
        all_good = True
        
        # Check directories
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                self.log_error("Project Structure", f"Missing directory: {dir_name}")
                all_good = False
            else:
                self.log_success("Project Structure", f"Directory exists: {dir_name}")
        
        # Check files
        for file_name in required_files:
            if not os.path.exists(file_name):
                self.log_error("Project Structure", f"Missing file: {file_name}")
                all_good = False
            else:
                self.log_success("Project Structure", f"File exists: {file_name}")
        
        return all_good
    
    def test_ai_resources_availability(self) -> bool:
        """Test availability of AI adoption resources"""
        logger.info("🔍 Testing AI adoption resources...")
        
        resources_dir = "AI adoption resources"
        if not os.path.exists(resources_dir):
            self.log_error("AI Resources", "AI adoption resources directory not found")
            return False
        
        # Check for PDF files
        pdf_files = []
        for root, dirs, files in os.walk(resources_dir):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        if not pdf_files:
            self.log_error("AI Resources", "No PDF files found in AI adoption resources")
            return False
        
        self.log_success("AI Resources", f"Found {len(pdf_files)} PDF files")
        
        # Check specific important files
        important_files = [
            "AI adoption resources/AI dashboard resources 1/hai_ai_index_report_2025.pdf",
            "AI adoption resources/AI dashboard resources 1/the-state-of-ai-how-organizations-are-rewiring-to-capture-value_final.pdf",
            "AI adoption resources/AI Adoption Resources 3/Generative AI could raise global GDP by 7_ _ Goldman Sachs.pdf"
        ]
        
        for file_path in important_files:
            if os.path.exists(file_path):
                self.log_success("AI Resources", f"Important file found: {file_path}")
            else:
                self.log_warning("AI Resources", f"Important file missing: {file_path}")
        
        return True
    
    def test_data_loading_functionality(self) -> bool:
        """Test data loading functionality"""
        logger.info("🔍 Testing data loading functionality...")
        
        try:
            # Test import of data modules
            from data.loaders import load_all_datasets, validate_all_loaded_data
            from data.models import safe_validate_data
            from data.research_integration import research_integrator
            
            self.log_success("Data Loading", "Data modules imported successfully")
            
            # Test data loading
            try:
                datasets = load_all_datasets()
                if isinstance(datasets, dict) and len(datasets) > 0:
                    self.log_success("Data Loading", f"Loaded {len(datasets)} datasets")
                    
                    # Check for key datasets
                    key_datasets = ['historical_data', 'sector_2025', 'ai_investment_data']
                    for dataset_name in key_datasets:
                        if dataset_name in datasets:
                            df = datasets[dataset_name]
                            if isinstance(df, pd.DataFrame) and not df.empty:
                                self.log_success("Data Loading", f"Dataset '{dataset_name}' loaded with {len(df)} rows")
                            else:
                                self.log_warning("Data Loading", f"Dataset '{dataset_name}' is empty or invalid")
                        else:
                            self.log_warning("Data Loading", f"Dataset '{dataset_name}' not found")
                else:
                    self.log_error("Data Loading", "No datasets loaded or invalid format")
                    return False
                    
            except Exception as e:
                self.log_error("Data Loading", f"Failed to load datasets: {str(e)}")
                return False
            
            return True
            
        except ImportError as e:
            self.log_error("Data Loading", f"Failed to import data modules: {str(e)}")
            return False
        except Exception as e:
            self.log_error("Data Loading", f"Unexpected error in data loading: {str(e)}")
            return False
    
    def test_research_integration(self) -> bool:
        """Test research integration functionality"""
        logger.info("🔍 Testing research integration...")
        
        try:
            from data.research_integration import research_integrator
            
            # Test if research integrator is properly initialized
            if hasattr(research_integrator, 'data_sources'):
                self.log_success("Research Integration", "Research integrator initialized")
                
                # Check data sources
                sources = research_integrator.data_sources
                if isinstance(sources, dict) and len(sources) > 0:
                    self.log_success("Research Integration", f"Found {len(sources)} data sources")
                    
                    # Check for key sources
                    key_sources = ['stanford_ai_index', 'mckinsey_survey', 'goldman_sachs']
                    for source_name in key_sources:
                        if source_name in sources:
                            source_info = sources[source_name]
                            if 'file' in source_info and 'authority' in source_info:
                                self.log_success("Research Integration", f"Source '{source_name}' properly configured")
                            else:
                                self.log_warning("Research Integration", f"Source '{source_name}' missing required fields")
                        else:
                            self.log_warning("Research Integration", f"Source '{source_name}' not found")
                else:
                    self.log_error("Research Integration", "No data sources configured")
                    return False
            else:
                self.log_error("Research Integration", "Research integrator not properly initialized")
                return False
            
            return True
            
        except Exception as e:
            self.log_error("Research Integration", f"Failed to test research integration: {str(e)}")
            return False
    
    def test_pdf_extraction_capability(self) -> bool:
        """Test PDF extraction capability"""
        logger.info("🔍 Testing PDF extraction capability...")
        
        try:
            from data.pdf_extractor import PDFDataExtractor
            
            extractor = PDFDataExtractor()
            
            # Check if extractor has required methods
            required_methods = ['extract_from_pdf', '_extract_metadata', '_extract_statistics']
            for method in required_methods:
                if hasattr(extractor, method):
                    self.log_success("PDF Extraction", f"Method '{method}' available")
                else:
                    self.log_warning("PDF Extraction", f"Method '{method}' missing")
            
            # Check extraction patterns
            if hasattr(extractor, 'extraction_patterns'):
                patterns = extractor.extraction_patterns
                if isinstance(patterns, dict) and len(patterns) > 0:
                    self.log_success("PDF Extraction", f"Extraction patterns configured: {list(patterns.keys())}")
                else:
                    self.log_warning("PDF Extraction", "No extraction patterns configured")
            
            return True
            
        except Exception as e:
            self.log_error("PDF Extraction", f"Failed to test PDF extraction: {str(e)}")
            return False
    
    def test_business_logic(self) -> bool:
        """Test business logic modules"""
        logger.info("🔍 Testing business logic...")
        
        try:
            from business.metrics import business_metrics, CompetitivePosition, InvestmentRecommendation
            from business.roi_calculator import roi_calculator
            
            self.log_success("Business Logic", "Business modules imported successfully")
            
            # Test business metrics
            if callable(business_metrics):
                self.log_success("Business Logic", "business_metrics function available")
            else:
                self.log_warning("Business Logic", "business_metrics not callable")
            
            # Test ROI calculator
            if callable(roi_calculator):
                self.log_success("Business Logic", "roi_calculator function available")
            else:
                self.log_warning("Business Logic", "roi_calculator not callable")
            
            return True
            
        except Exception as e:
            self.log_error("Business Logic", f"Failed to test business logic: {str(e)}")
            return False
    
    def test_views_functionality(self) -> bool:
        """Test views functionality"""
        logger.info("🔍 Testing views functionality...")
        
        try:
            # Check views directory
            views_dir = "views"
            if not os.path.exists(views_dir):
                self.log_error("Views", "Views directory not found")
                return False
            
            # Check for key view files
            key_views = [
                'adoption_rates.py', 'ai_maturity.py', 'financial_impact.py',
                'geographic_distribution.py', 'historical_trends.py', 'industry_analysis.py'
            ]
            
            for view_file in key_views:
                view_path = os.path.join(views_dir, view_file)
                if os.path.exists(view_path):
                    self.log_success("Views", f"View file found: {view_file}")
                else:
                    self.log_warning("Views", f"View file missing: {view_file}")
            
            return True
            
        except Exception as e:
            self.log_error("Views", f"Failed to test views: {str(e)}")
            return False
    
    def test_data_validation(self) -> bool:
        """Test data validation functionality"""
        logger.info("🔍 Testing data validation...")
        
        try:
            from Utils.data_validation import DataValidator, ValidationResult, DataStatus
            
            validator = DataValidator()
            
            # Test validation with sample data
            sample_df = pd.DataFrame({
                'year': [2020, 2021, 2022],
                'value': [10, 20, 30]
            })
            
            result = validator.validate_dataframe(
                sample_df, "test_data",
                required_columns=['year', 'value']
            )
            
            if result.is_valid:
                self.log_success("Data Validation", "Sample data validation successful")
            else:
                self.log_error("Data Validation", f"Sample data validation failed: {result.message}")
                return False
            
            return True
            
        except Exception as e:
            self.log_error("Data Validation", f"Failed to test data validation: {str(e)}")
            return False
    
    def test_app_imports(self) -> bool:
        """Test app imports and basic functionality"""
        logger.info("🔍 Testing app imports...")
        
        try:
            # Test importing the main app
            import app
            
            # Check if main function exists
            if hasattr(app, 'main'):
                self.log_success("App Imports", "Main function found")
            else:
                self.log_warning("App Imports", "Main function not found")
            
            # Check if data loading function exists
            if hasattr(app, 'load_data_with_mckinsey_tools'):
                self.log_success("App Imports", "Data loading function found")
            else:
                self.log_warning("App Imports", "Data loading function not found")
            
            return True
            
        except Exception as e:
            self.log_error("App Imports", f"Failed to import app: {str(e)}")
            return False
    
    def test_data_authenticity(self) -> bool:
        """Test if data is actually sourced from AI adoption resources"""
        logger.info("🔍 Testing data authenticity...")
        
        try:
            # Load data and check source attribution
            from data.loaders import load_all_datasets
            
            datasets = load_all_datasets()
            
            # Check if datasets have source information
            authentic_sources = 0
            total_datasets = 0
            
            for name, df in datasets.items():
                total_datasets += 1
                
                # Check for data_source column
                if isinstance(df, pd.DataFrame) and 'data_source' in df.columns:
                    sources = df['data_source'].unique()
                    if any('Stanford' in str(s) or 'McKinsey' in str(s) or 'Goldman' in str(s) for s in sources):
                        authentic_sources += 1
                        self.log_success("Data Authenticity", f"Dataset '{name}' has authentic sources")
                    else:
                        self.log_warning("Data Authenticity", f"Dataset '{name}' may not have authentic sources")
                else:
                    self.log_warning("Data Authenticity", f"Dataset '{name}' missing source attribution")
            
            if total_datasets > 0:
                authenticity_rate = (authentic_sources / total_datasets) * 100
                if authenticity_rate >= 50:
                    self.log_success("Data Authenticity", f"Data authenticity rate: {authenticity_rate:.1f}%")
                else:
                    self.log_warning("Data Authenticity", f"Low data authenticity rate: {authenticity_rate:.1f}%")
            
            return True
            
        except Exception as e:
            self.log_error("Data Authenticity", f"Failed to test data authenticity: {str(e)}")
            return False
    
    def test_performance_features(self) -> bool:
        """Test performance optimization features"""
        logger.info("🔍 Testing performance features...")
        
        try:
            from performance.caching import smart_cache, performance_monitor
            
            # Check if performance modules are available
            if callable(smart_cache):
                self.log_success("Performance", "Smart cache function available")
            else:
                self.log_warning("Performance", "Smart cache function not available")
            
            if hasattr(performance_monitor, 'monitor'):
                self.log_success("Performance", "Performance monitor available")
            else:
                self.log_warning("Performance", "Performance monitor not available")
            
            return True
            
        except Exception as e:
            self.log_error("Performance", f"Failed to test performance features: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all comprehensive tests"""
        logger.info("🚀 Starting comprehensive testing...")
        
        tests = [
            ("Project Structure", self.test_project_structure),
            ("AI Resources Availability", self.test_ai_resources_availability),
            ("Data Loading Functionality", self.test_data_loading_functionality),
            ("Research Integration", self.test_research_integration),
            ("PDF Extraction Capability", self.test_pdf_extraction_capability),
            ("Business Logic", self.test_business_logic),
            ("Views Functionality", self.test_views_functionality),
            ("Data Validation", self.test_data_validation),
            ("App Imports", self.test_app_imports),
            ("Data Authenticity", self.test_data_authenticity),
            ("Performance Features", self.test_performance_features)
        ]
        
        for test_name, test_func in tests:
            try:
                logger.info(f"\n{'='*50}")
                logger.info(f"Running: {test_name}")
                logger.info(f"{'='*50}")
                
                result = test_func()
                self.test_results[test_name] = result
                
            except Exception as e:
                self.log_error(test_name, f"Test failed with exception: {str(e)}")
                self.test_results[test_name] = False
        
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'errors': self.errors,
            'warnings': self.warnings,
            'successes': self.successes,
            'test_results': self.test_results,
            'recommendations': self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check for critical issues
        if len(self.errors) > 0:
            recommendations.append("🔴 CRITICAL: Fix all errors before deployment")
        
        # Check data authenticity
        if any('Data Authenticity' in error['test'] for error in self.errors):
            recommendations.append("🔴 CRITICAL: Implement proper data extraction from PDF resources")
        
        # Check for missing dependencies
        if any('import' in error['error'].lower() for error in self.errors):
            recommendations.append("🟡 WARNING: Install missing dependencies")
        
        # Check for performance issues
        if any('Performance' in warning['test'] for warning in self.warnings):
            recommendations.append("🟡 WARNING: Optimize performance features")
        
        # Check for data source issues
        if any('Research Integration' in error['test'] for error in self.errors):
            recommendations.append("🔴 CRITICAL: Fix research integration to use actual PDF data")
        
        if not recommendations:
            recommendations.append("✅ All systems operational - ready for deployment")
        
        return recommendations
    
    def print_report(self, report: Dict[str, Any]):
        """Print the test report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        # Summary
        summary = report['summary']
        print(f"\n📊 SUMMARY:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed_tests']}")
        print(f"   Failed: {summary['failed_tests']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        
        # Errors
        if report['errors']:
            print(f"\n❌ ERRORS ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"   • {error['test']}: {error['error']}")
                if error['details']:
                    print(f"     Details: {error['details']}")
        
        # Warnings
        if report['warnings']:
            print(f"\n⚠️ WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"   • {warning['test']}: {warning['warning']}")
                if warning['details']:
                    print(f"     Details: {warning['details']}")
        
        # Recommendations
        if report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"   {rec}")
        
        print("\n" + "="*80)

def main():
    """Main function to run comprehensive testing"""
    tester = ComprehensiveTester()
    report = tester.run_all_tests()
    tester.print_report(report)
    
    # Return exit code based on success rate
    success_rate = report['summary']['success_rate']
    if success_rate >= 80:
        print("\n🎉 Overall Status: GOOD - Ready for deployment with minor fixes")
        return 0
    elif success_rate >= 60:
        print("\n⚠️ Overall Status: FAIR - Needs significant improvements")
        return 1
    else:
        print("\n🚨 Overall Status: POOR - Major issues need to be addressed")
        return 2

if __name__ == "__main__":
    sys.exit(main()) 