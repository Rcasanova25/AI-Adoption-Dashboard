import sys
import subprocess
import argparse
import time
from pathlib import Path

class TestRunner:
    """Advanced test runner with reporting and analysis"""
    
    def __init__(self):
        self.start_time = time.time()
        self.results = {}
        
    def run_command(self, command, description):
        """Run a command and capture results"""
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(command)}")
        print(f"{'='*60}")
        
        start = time.time()
        result = subprocess.run(command, capture_output=True, text=True)
        duration = time.time() - start
        
        self.results[description] = {
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
        if result.returncode == 0:
            print(f"✅ {description} PASSED ({duration:.2f}s)")
        else:
            print(f"❌ {description} FAILED ({duration:.2f}s)")
            print(f"Error: {result.stderr}")
            
        return result.returncode == 0
    
    def run_tests(self, test_type="all", verbose=False):
        """Run specified tests"""
        success = True
        
        if test_type in ["all", "unit"]:
            success &= self.run_command(
                ["python", "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
                "Unit Tests"
            )
        
        if test_type in ["all", "integration"]:
            success &= self.run_command(
                ["python", "-m", "pytest", "tests/integration/", "-v", "--tb=short"],
                "Integration Tests"
            )
        
        if test_type in ["all", "performance"]:
            success &= self.run_command(
                ["python", "-m", "pytest", "tests/performance/", "-v", "-m", "performance and not slow"],
                "Performance Tests"
            )
        
        return success
    
    def run_quality_checks(self):
        """Run code quality checks"""
        success = True
        
        # Linting
        success &= self.run_command(
            ["python", "-m", "flake8", ".", "--max-line-length=88"],
            "Code Linting (flake8)"
        )
        
        # Type checking
        success &= self.run_command(
            ["python", "-m", "mypy", "app.py", "business/", "data/", "Utils/", "--ignore-missing-imports"],
            "Type Checking (mypy)"
        )
        
        # Security checks
        success &= self.run_command(
            ["python", "-m", "bandit", "-r", ".", "-ll"],
            "Security Check (bandit)"
        )
        
        return success
    
    def generate_report(self):
        """Generate test report"""
        total_time = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print("TEST SUMMARY REPORT")
        print(f"{'='*60}")
        print(f"Total execution time: {total_time:.2f}s")
        print()
        
        passed = sum(1 for r in self.results.values() if r['success'])
        total = len(self.results)
        
        print(f"Results: {passed}/{total} passed")
        print()
        
        for name, result in self.results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{status:<10} {name:<30} ({result['duration']:.2f}s)")
        
        if passed == total:
            print(f"\n🎉 All tests passed! Ready for deployment.")
            return True
        else:
            print(f"\n⚠️  {total-passed} test(s) failed. Please fix before deployment.")
            return False

def main():
    parser = argparse.ArgumentParser(description="Advanced test runner for AI Dashboard")
    parser.add_argument("--type", choices=["all", "unit", "integration", "performance"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--quality", action="store_true", help="Run code quality checks")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    # Run tests
    test_success = runner.run_tests(args.type, args.verbose)
    
    # Run quality checks if requested
    quality_success = True
    if args.quality:
        quality_success = runner.run_quality_checks()
    
    # Generate report
    overall_success = runner.generate_report()
    
    # Exit with appropriate code
    if test_success and quality_success and overall_success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 