"""
Automated Test Runner for AI Adoption Dashboard
Comprehensive test execution with detailed reporting and CI/CD integration
"""

import pytest
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import logging
from datetime import datetime
import coverage

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class AutomatedTestRunner:
    """
    Comprehensive test runner with reporting and CI/CD integration
    """
    
    def __init__(self, test_dir: str = "tests/automated"):
        self.test_dir = Path(test_dir)
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run_data_validation_tests(self) -> Dict[str, Any]:
        """Run data validation tests"""
        logger.info("Running data validation tests...")
        
        test_file = self.test_dir / "test_data_validation_enhanced.py"
        if not test_file.exists():
            return {'status': 'skipped', 'reason': 'Test file not found'}
        
        result = self._run_pytest_with_coverage(
            str(test_file),
            "data_validation",
            markers="-m 'not slow'"
        )
        
        return result
    
    def run_view_rendering_tests(self) -> Dict[str, Any]:
        """Run view rendering tests"""
        logger.info("Running view rendering tests...")
        
        test_file = self.test_dir / "test_view_rendering.py"
        if not test_file.exists():
            return {'status': 'skipped', 'reason': 'Test file not found'}
        
        result = self._run_pytest_with_coverage(
            str(test_file),
            "view_rendering",
            markers="-m 'not slow'"
        )
        
        return result
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests"""
        logger.info("Running integration tests...")
        
        integration_dir = Path("tests/integration")
        if not integration_dir.exists():
            return {'status': 'skipped', 'reason': 'Integration test directory not found'}
        
        result = self._run_pytest_with_coverage(
            str(integration_dir),
            "integration",
            markers="-k 'not performance'"
        )
        
        return result
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests"""
        logger.info("Running performance tests...")
        
        result = self._run_pytest_with_coverage(
            str(self.test_dir),
            "performance",
            markers="-m 'slow' -k 'performance'"
        )
        
        return result
    
    def run_accessibility_tests(self) -> Dict[str, Any]:
        """Run accessibility tests"""
        logger.info("Running accessibility tests...")
        
        result = self._run_pytest_with_coverage(
            str(self.test_dir),
            "accessibility",
            markers="-k 'accessibility'"
        )
        
        return result
    
    def _run_pytest_with_coverage(self, test_path: str, suite_name: str, 
                                 markers: str = "") -> Dict[str, Any]:
        """Run pytest with coverage reporting"""
        
        # Prepare output files
        html_report = self.results_dir / f"{suite_name}_{self.timestamp}.html"
        json_report = self.results_dir / f"{suite_name}_{self.timestamp}.json"
        coverage_report = self.results_dir / f"coverage_{suite_name}_{self.timestamp}.html"
        
        # Build pytest command
        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
            f"--html={html_report}",
            "--self-contained-html",
            f"--json-report=--file={json_report}",
            "--tb=short",
            "-v"
        ]
        
        if markers:
            cmd.extend(markers.split())
        
        # Add coverage if available
        try:
            import coverage
            cmd.extend([
                "--cov=data",
                "--cov=views", 
                "--cov=business",
                f"--cov-report=html:{coverage_report}",
                "--cov-report=term-missing"
            ])
        except ImportError:
            logger.warning("Coverage not available, running without coverage reporting")
        
        # Run tests
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Parse results
            test_result = {
                'suite_name': suite_name,
                'status': 'passed' if result.returncode == 0 else 'failed',
                'return_code': result.returncode,
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'timestamp': self.timestamp,
                'reports': {
                    'html': str(html_report) if html_report.exists() else None,
                    'json': str(json_report) if json_report.exists() else None,
                    'coverage': str(coverage_report) if coverage_report.exists() else None
                }
            }
            
            # Try to parse JSON report for detailed results
            if json_report.exists():
                try:
                    with open(json_report, 'r') as f:
                        json_data = json.load(f)
                        test_result['summary'] = json_data.get('summary', {})
                        test_result['tests'] = json_data.get('tests', [])
                except Exception as e:
                    logger.warning(f"Failed to parse JSON report: {e}")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            return {
                'suite_name': suite_name,
                'status': 'timeout',
                'duration': 600,
                'error': 'Test suite timed out after 10 minutes'
            }
        except Exception as e:
            return {
                'suite_name': suite_name,
                'status': 'error',
                'error': str(e)
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all automated tests"""
        logger.info("🚀 Starting automated test suite execution")
        
        overall_start = time.time()
        results = {
            'execution_info': {
                'timestamp': self.timestamp,
                'start_time': datetime.now().isoformat(),
                'test_directory': str(self.test_dir),
                'results_directory': str(self.results_dir)
            },
            'test_suites': {},
            'summary': {}
        }
        
        # Define test suites to run
        test_suites = [
            ('data_validation', self.run_data_validation_tests),
            ('view_rendering', self.run_view_rendering_tests),
            ('integration', self.run_integration_tests),
            ('performance', self.run_performance_tests),
            ('accessibility', self.run_accessibility_tests)
        ]
        
        # Run each test suite
        passed_suites = 0
        failed_suites = 0
        total_duration = 0
        
        for suite_name, suite_runner in test_suites:
            logger.info(f"📋 Running {suite_name} test suite...")
            
            try:
                suite_result = suite_runner()
                results['test_suites'][suite_name] = suite_result
                
                if suite_result.get('status') == 'passed':
                    passed_suites += 1
                    logger.info(f"✅ {suite_name} tests passed")
                elif suite_result.get('status') == 'skipped':
                    logger.info(f"⏭️ {suite_name} tests skipped: {suite_result.get('reason')}")
                else:
                    failed_suites += 1
                    logger.error(f"❌ {suite_name} tests failed")
                
                total_duration += suite_result.get('duration', 0)
                
            except Exception as e:
                logger.error(f"❌ Error running {suite_name} tests: {e}")
                results['test_suites'][suite_name] = {
                    'status': 'error',
                    'error': str(e)
                }
                failed_suites += 1
        
        overall_end = time.time()
        overall_duration = overall_end - overall_start
        
        # Generate summary
        results['summary'] = {
            'total_suites': len(test_suites),
            'passed_suites': passed_suites,
            'failed_suites': failed_suites,
            'skipped_suites': len(test_suites) - passed_suites - failed_suites,
            'success_rate': (passed_suites / len(test_suites)) * 100,
            'total_duration': overall_duration,
            'test_duration': total_duration,
            'end_time': datetime.now().isoformat()
        }
        
        # Save overall results
        self._save_results(results)
        
        # Log summary
        self._log_summary(results)
        
        return results
    
    def _save_results(self, results: Dict[str, Any]):
        """Save test results to file"""
        results_file = self.results_dir / f"test_results_{self.timestamp}.json"
        
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"📄 Test results saved to: {results_file}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    def _log_summary(self, results: Dict[str, Any]):
        """Log test execution summary"""
        summary = results['summary']
        
        logger.info("=" * 60)
        logger.info("🏁 AUTOMATED TEST EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Test Suites: {summary['total_suites']}")
        logger.info(f"Passed: {summary['passed_suites']}")
        logger.info(f"Failed: {summary['failed_suites']}")
        logger.info(f"Skipped: {summary['skipped_suites']}")
        logger.info(f"Success Rate: {summary['success_rate']:.1f}%")
        logger.info(f"Total Duration: {summary['total_duration']:.2f} seconds")
        logger.info("=" * 60)
        
        # Detailed results per suite
        for suite_name, suite_result in results['test_suites'].items():
            status = suite_result.get('status', 'unknown')
            duration = suite_result.get('duration', 0)
            
            status_emoji = {
                'passed': '✅',
                'failed': '❌', 
                'skipped': '⏭️',
                'error': '💥',
                'timeout': '⏰'
            }.get(status, '❓')
            
            logger.info(f"{status_emoji} {suite_name}: {status} ({duration:.2f}s)")
            
            # Log test counts if available
            if 'summary' in suite_result:
                test_summary = suite_result['summary']
                if 'total' in test_summary:
                    passed = test_summary.get('passed', 0)
                    failed = test_summary.get('failed', 0)
                    total = test_summary.get('total', 0)
                    logger.info(f"    Tests: {passed}/{total} passed, {failed} failed")
        
        logger.info("=" * 60)
        
        if summary['success_rate'] == 100:
            logger.info("🎉 All test suites passed!")
        elif summary['success_rate'] >= 80:
            logger.info("⚠️ Most test suites passed, but some issues detected")
        else:
            logger.error("🚨 Multiple test suites failed - review required")
    
    def run_ci_mode(self) -> int:
        """Run tests in CI/CD mode with appropriate exit codes"""
        results = self.run_all_tests()
        
        # Return appropriate exit code for CI/CD
        if results['summary']['failed_suites'] == 0:
            return 0  # Success
        else:
            return 1  # Failure
    
    def generate_badge_data(self, results: Dict[str, Any]) -> Dict[str, str]:
        """Generate badge data for CI/CD integration"""
        summary = results['summary']
        success_rate = summary['success_rate']
        
        if success_rate == 100:
            color = "brightgreen"
            message = "passing"
        elif success_rate >= 80:
            color = "yellow" 
            message = f"{success_rate:.0f}% passing"
        else:
            color = "red"
            message = f"{success_rate:.0f}% passing"
        
        return {
            'schemaVersion': 1,
            'label': 'tests',
            'message': message,
            'color': color
        }


def main():
    """Main entry point for automated test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run automated tests for AI Adoption Dashboard')
    parser.add_argument('--ci', action='store_true', help='Run in CI/CD mode')
    parser.add_argument('--suite', choices=['data', 'views', 'integration', 'performance', 'accessibility'], 
                       help='Run specific test suite only')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage reports')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create test runner
    runner = AutomatedTestRunner()
    
    # Run specific suite or all tests
    if args.suite:
        suite_runners = {
            'data': runner.run_data_validation_tests,
            'views': runner.run_view_rendering_tests,
            'integration': runner.run_integration_tests,
            'performance': runner.run_performance_tests,
            'accessibility': runner.run_accessibility_tests
        }
        
        result = suite_runners[args.suite]()
        print(json.dumps(result, indent=2))
        
        return 0 if result.get('status') == 'passed' else 1
    
    elif args.ci:
        # CI/CD mode
        return runner.run_ci_mode()
    
    else:
        # Interactive mode
        results = runner.run_all_tests()
        
        # Return exit code based on success rate
        return 0 if results['summary']['success_rate'] >= 80 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)