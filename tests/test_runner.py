"""
Comprehensive test runner for AI Adoption Dashboard
Provides test execution, coverage reporting, and CI/CD integration
"""

import pytest
import sys
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestRunner:
    """Comprehensive test runner with coverage and reporting"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.test_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"
        self.coverage_dir = self.reports_dir / "coverage"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.coverage_dir.mkdir(exist_ok=True)
    
    def run_unit_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run unit tests with coverage"""
        print("🧪 Running Unit Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.test_dir / "unit"),
            "-v" if verbose else "-q",
            "--tb=short",
            "--cov=data",
            "--cov=Utils",
            "--cov=business",
            "--cov=views",
            f"--cov-report=html:{self.coverage_dir / 'unit'}",
            f"--cov-report=json:{self.coverage_dir / 'unit_coverage.json'}",
            "--cov-report=term",
            "-m", "unit"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "test_type": "unit",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_integration_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run integration tests"""
        print("🔗 Running Integration Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.test_dir / "integration"),
            "-v" if verbose else "-q",
            "--tb=short",
            "--cov=views",
            "--cov=data",
            f"--cov-report=html:{self.coverage_dir / 'integration'}",
            f"--cov-report=json:{self.coverage_dir / 'integration_coverage.json'}",
            "--cov-report=term",
            "-m", "integration"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "test_type": "integration",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_performance_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run performance tests"""
        print("⚡ Running Performance Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.test_dir / "performance"),
            "-v" if verbose else "-q",
            "--tb=short",
            "-m", "performance and not slow"  # Exclude slow tests by default
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "test_type": "performance",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_e2e_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run end-to-end tests"""
        print("🎯 Running End-to-End Tests...")
        
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.test_dir / "e2e"),
            "-v" if verbose else "-q",
            "--tb=short",
            "--cov=app",
            f"--cov-report=html:{self.coverage_dir / 'e2e'}",
            f"--cov-report=json:{self.coverage_dir / 'e2e_coverage.json'}",
            "--cov-report=term",
            "-m", "e2e"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "test_type": "e2e",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_all_tests(self, include_slow: bool = False, verbose: bool = True) -> Dict[str, Any]:
        """Run complete test suite"""
        print("🚀 Running Complete Test Suite...")
        
        start_time = time.time()
        
        # Build pytest command
        cmd = [
            sys.executable, "-m", "pytest",
            str(self.test_dir),
            "-v" if verbose else "-q",
            "--tb=short",
            "--cov=data",
            "--cov=Utils", 
            "--cov=business",
            "--cov=views",
            "--cov=app",
            f"--cov-report=html:{self.coverage_dir / 'complete'}",
            f"--cov-report=json:{self.coverage_dir / 'complete_coverage.json'}",
            "--cov-report=term-missing",
            "--cov-fail-under=80"  # Require 80% coverage
        ]
        
        # Add markers based on options
        if not include_slow:
            cmd.extend(["-m", "not slow"])
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            "test_type": "complete",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0,
            "execution_time": execution_time
        }
    
    def generate_coverage_report(self) -> Dict[str, Any]:
        """Generate comprehensive coverage report"""
        print("📊 Generating Coverage Report...")
        
        coverage_files = [
            self.coverage_dir / "complete_coverage.json",
            self.coverage_dir / "unit_coverage.json",
            self.coverage_dir / "integration_coverage.json",
            self.coverage_dir / "e2e_coverage.json"
        ]
        
        coverage_data = {}
        
        for coverage_file in coverage_files:
            if coverage_file.exists():
                try:
                    with open(coverage_file, 'r') as f:
                        data = json.load(f)
                        test_type = coverage_file.stem.replace('_coverage', '')
                        coverage_data[test_type] = {
                            'total_coverage': data.get('totals', {}).get('percent_covered', 0),
                            'files_covered': len(data.get('files', {})),
                            'missing_lines': data.get('totals', {}).get('missing_lines', 0)
                        }
                except Exception as e:
                    print(f"⚠️  Error reading {coverage_file}: {e}")
        
        # Generate summary report
        summary_report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'coverage_by_test_type': coverage_data,
            'overall_status': 'PASS' if all(
                data.get('total_coverage', 0) >= 80 
                for data in coverage_data.values()
            ) else 'FAIL'
        }
        
        # Save summary report
        summary_file = self.coverage_dir / "coverage_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary_report, f, indent=2)
        
        return summary_report
    
    def run_linting(self) -> Dict[str, Any]:
        """Run code linting checks"""
        print("🔍 Running Code Linting...")
        
        # Check if flake8 is available
        try:
            result = subprocess.run(
                [sys.executable, "-m", "flake8", "--version"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return {"success": False, "message": "flake8 not available"}
        except FileNotFoundError:
            return {"success": False, "message": "flake8 not installed"}
        
        # Run flake8 on main code directories
        cmd = [
            sys.executable, "-m", "flake8",
            "data/", "Utils/", "views/", "business/",
            "--max-line-length=120",
            "--extend-ignore=E203,W503",  # Ignore some style issues
            "--output-file=" + str(self.reports_dir / "flake8_report.txt")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "tool": "flake8",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_security_scan(self) -> Dict[str, Any]:
        """Run security scanning with bandit"""
        print("🔒 Running Security Scan...")
        
        # Check if bandit is available
        try:
            result = subprocess.run(
                [sys.executable, "-m", "bandit", "--version"],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return {"success": False, "message": "bandit not available"}
        except FileNotFoundError:
            return {"success": False, "message": "bandit not installed"}
        
        # Run bandit security scan
        cmd = [
            sys.executable, "-m", "bandit",
            "-r", "data/", "Utils/", "views/", "business/",
            "-f", "json",
            "-o", str(self.reports_dir / "security_report.json")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        
        return {
            "tool": "bandit",
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def generate_test_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.get('success', False))
        failed_tests = total_tests - passed_tests
        
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'total_test_suites': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'test_results': results,
            'recommendations': []
        }
        
        # Add recommendations based on results
        if failed_tests > 0:
            report['recommendations'].append("Review failed tests and fix issues before deployment")
        
        if report['summary']['success_rate'] < 95:
            report['recommendations'].append("Improve test coverage and reliability")
        
        # Save report
        report_file = self.reports_dir / "test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report


class CIIntegration:
    """CI/CD integration utilities"""
    
    @staticmethod
    def generate_github_actions_workflow() -> str:
        """Generate GitHub Actions workflow for CI/CD"""
        
        workflow = """
name: AI Dashboard CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run linting
      run: |
        flake8 data/ Utils/ views/ business/ --max-line-length=120
    
    - name: Run security scan
      run: |
        bandit -r data/ Utils/ views/ business/
    
    - name: Run unit tests
      run: |
        python -m pytest tests/unit/ -v --cov=data --cov=Utils --cov=business --cov-report=xml
    
    - name: Run integration tests
      run: |
        python -m pytest tests/integration/ -v --cov=views --cov-report=xml
    
    - name: Run end-to-end tests
      run: |
        python -m pytest tests/e2e/ -v --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Generate test report
      run: |
        python tests/test_runner.py --generate-report
    
    - name: Upload test artifacts
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-reports-${{ matrix.python-version }}
        path: reports/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Streamlit Cloud
      run: |
        echo "Deploy to production"
        # Add deployment steps here
"""
        
        return workflow
    
    @staticmethod
    def generate_pre_commit_config() -> str:
        """Generate pre-commit configuration"""
        
        config = """
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
  
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]
  
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.4
    hooks:
      - id: bandit
        args: [-r, -x, tests/]
  
  - repo: local
    hooks:
      - id: pytest-unit
        name: Run unit tests
        entry: python -m pytest tests/unit/ -x -v
        language: system
        pass_filenames: false
        always_run: true
"""
        
        return config


def main():
    """Main test runner execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Dashboard Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--include-slow", action="store_true", help="Include slow tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--generate-report", action="store_true", help="Generate test report")
    parser.add_argument("--lint", action="store_true", help="Run linting")
    parser.add_argument("--security", action="store_true", help="Run security scan")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    results = []
    
    # Run specific test types
    if args.unit:
        results.append(runner.run_unit_tests(args.verbose))
    
    if args.integration:
        results.append(runner.run_integration_tests(args.verbose))
    
    if args.performance:
        results.append(runner.run_performance_tests(args.verbose))
    
    if args.e2e:
        results.append(runner.run_e2e_tests(args.verbose))
    
    if args.all or not any([args.unit, args.integration, args.performance, args.e2e]):
        result = runner.run_all_tests(args.include_slow, args.verbose)
        results.append(result)
    
    # Run additional checks
    if args.lint:
        lint_result = runner.run_linting()
        results.append(lint_result)
    
    if args.security:
        security_result = runner.run_security_scan()
        results.append(security_result)
    
    # Generate reports
    if args.generate_report or args.all:
        coverage_report = runner.generate_coverage_report()
        test_report = runner.generate_test_report(results)
        
        print("\n📊 Test Summary:")
        print(f"Total test suites: {test_report['summary']['total_test_suites']}")
        print(f"Passed: {test_report['summary']['passed']}")
        print(f"Failed: {test_report['summary']['failed']}")
        print(f"Success rate: {test_report['summary']['success_rate']:.1f}%")
        
        if coverage_report:
            print(f"\nCoverage Status: {coverage_report['overall_status']}")
    
    # Print results
    for result in results:
        test_type = result.get('test_type', 'unknown')
        success = result.get('success', False)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_type.title()} Tests: {status}")
        
        if not success and args.verbose:
            print(f"Error output: {result.get('stderr', 'No error output')}")
    
    # Exit with appropriate code
    all_passed = all(r.get('success', False) for r in results)
    exit_code = 0 if all_passed else 1
    
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)