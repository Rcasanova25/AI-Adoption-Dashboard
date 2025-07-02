#!/usr/bin/env python3
"""
Test Execution Script for AI Adoption Dashboard
Easy-to-use script for running all automated tests
"""

import sys
import os
import subprocess
from pathlib import Path
import argparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if testing dependencies are installed"""
    required_packages = [
        'pytest',
        'pytest-cov', 
        'pytest-html',
        'pytest-json-report'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.error(f"Missing testing dependencies: {', '.join(missing)}")
        logger.info("Install them with: pip install pytest pytest-cov pytest-html pytest-json-report")
        return False
    
    return True


def run_quick_tests():
    """Run quick unit tests only"""
    logger.info("🚀 Running quick tests (unit tests only)...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/automated/",
        "-m", "not slow",
        "-v",
        "--tb=short"
    ]
    
    return subprocess.run(cmd).returncode


def run_full_tests():
    """Run full test suite with coverage"""
    logger.info("🔬 Running full test suite with coverage...")
    
    # Ensure test results directory exists
    Path("test_results").mkdir(exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--cov=data",
        "--cov=views",
        "--cov=business",
        "--cov=Utils",
        "--cov-report=html:test_results/coverage_html",
        "--cov-report=term-missing",
        "--html=test_results/test_report.html",
        "--self-contained-html",
        "--json-report=--file=test_results/test_results.json",
        "-v"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        logger.info("✅ All tests passed!")
        logger.info("📄 Reports generated:")
        logger.info("  - HTML Test Report: test_results/test_report.html")
        logger.info("  - Coverage Report: test_results/coverage_html/index.html")
        logger.info("  - JSON Results: test_results/test_results.json")
    else:
        logger.error("❌ Some tests failed. Check the reports for details.")
    
    return result.returncode


def run_specific_suite(suite_name):
    """Run a specific test suite"""
    logger.info(f"🎯 Running {suite_name} test suite...")
    
    suite_paths = {
        'data': 'tests/automated/test_data_validation_enhanced.py',
        'views': 'tests/automated/test_view_rendering.py', 
        'integration': 'tests/integration/',
        'unit': 'tests/unit/',
        'performance': 'tests/ -m performance'
    }
    
    if suite_name not in suite_paths:
        logger.error(f"Unknown test suite: {suite_name}")
        logger.info(f"Available suites: {', '.join(suite_paths.keys())}")
        return 1
    
    test_path = suite_paths[suite_name]
    
    cmd = [sys.executable, "-m", "pytest"] + test_path.split() + ["-v"]
    
    return subprocess.run(cmd).returncode


def run_automated_pipeline():
    """Run the automated test pipeline"""
    logger.info("🤖 Running automated test pipeline...")
    
    try:
        from tests.automated.test_runner_automated import AutomatedTestRunner
        
        runner = AutomatedTestRunner()
        results = runner.run_all_tests()
        
        success_rate = results['summary']['success_rate']
        
        if success_rate == 100:
            logger.info("🎉 Automated pipeline completed successfully!")
            return 0
        elif success_rate >= 80:
            logger.warning("⚠️ Automated pipeline completed with warnings")
            return 0
        else:
            logger.error("❌ Automated pipeline failed")
            return 1
    
    except Exception as e:
        logger.error(f"Failed to run automated pipeline: {e}")
        return 1


def run_ci_tests():
    """Run tests in CI/CD mode"""
    logger.info("🔄 Running tests in CI/CD mode...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--tb=short",
        "--maxfail=5",
        "-q"
    ]
    
    return subprocess.run(cmd).returncode


def validate_dashboard():
    """Run dashboard validation tests"""
    logger.info("🏠 Running dashboard validation...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/automated/test_data_validation_enhanced.py",
        "tests/automated/test_view_rendering.py",
        "-v"
    ]
    
    return subprocess.run(cmd).returncode


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run tests for AI Adoption Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --quick          # Run quick unit tests
  python run_tests.py --full           # Run full test suite with coverage
  python run_tests.py --suite data     # Run data validation tests only
  python run_tests.py --automated      # Run automated test pipeline
  python run_tests.py --validate       # Run dashboard validation
  python run_tests.py --ci             # Run in CI/CD mode
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--quick', action='store_true', 
                      help='Run quick unit tests only (fast)')
    group.add_argument('--full', action='store_true',
                      help='Run full test suite with coverage reports')
    group.add_argument('--suite', choices=['data', 'views', 'integration', 'unit', 'performance'],
                      help='Run specific test suite')
    group.add_argument('--automated', action='store_true',
                      help='Run automated test pipeline')
    group.add_argument('--validate', action='store_true',
                      help='Run dashboard validation tests')
    group.add_argument('--ci', action='store_true',
                      help='Run tests in CI/CD mode')
    
    parser.add_argument('--check-deps', action='store_true',
                       help='Check if testing dependencies are installed')
    
    args = parser.parse_args()
    
    # Check dependencies first
    if args.check_deps or not check_dependencies():
        if not check_dependencies():
            return 1
        else:
            logger.info("✅ All testing dependencies are installed")
            return 0
    
    # Run selected test mode
    if args.quick:
        return run_quick_tests()
    elif args.full:
        return run_full_tests()
    elif args.suite:
        return run_specific_suite(args.suite)
    elif args.automated:
        return run_automated_pipeline()
    elif args.validate:
        return validate_dashboard()
    elif args.ci:
        return run_ci_tests()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Tests interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)