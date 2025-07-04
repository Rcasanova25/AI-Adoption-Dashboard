"""Test runner script for the Economics of AI Dashboard."""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type='all', verbose=False, coverage=False):
    """Run tests with specified options.
    
    Args:
        test_type: Type of tests to run ('unit', 'integration', 'e2e', 'all')
        verbose: Enable verbose output
        coverage: Generate coverage report
    """
    # Base pytest command
    cmd = ['pytest']
    
    # Add verbosity
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    # Add coverage
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=html', '--cov-report=term'])
    
    # Select test directory
    if test_type == 'unit':
        cmd.append('tests/unit')
    elif test_type == 'integration':
        cmd.append('tests/integration')
    elif test_type == 'e2e':
        cmd.append('tests/e2e')
    elif test_type == 'performance':
        cmd.append('tests/performance')
    elif test_type == 'all':
        cmd.append('tests/')
    
    # Add additional options
    cmd.extend([
        '--tb=short',  # Shorter traceback
        '-p', 'no:warnings',  # Disable warnings
        '--maxfail=5',  # Stop after 5 failures
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run tests
    result = subprocess.run(cmd, capture_output=False)
    
    return result.returncode


def run_linting():
    """Run code quality checks."""
    print("Running code quality checks...")
    print("-" * 50)
    
    # Run black
    print("Running black...")
    black_result = subprocess.run(['black', '--check', '.'], capture_output=True)
    if black_result.returncode != 0:
        print("❌ Black found formatting issues")
        print(black_result.stdout.decode())
    else:
        print("✅ Black: All files formatted correctly")
    
    # Run flake8
    print("\nRunning flake8...")
    flake8_result = subprocess.run(
        ['flake8', '--max-line-length=100', '--exclude=tests'],
        capture_output=True
    )
    if flake8_result.returncode != 0:
        print("❌ Flake8 found issues")
        print(flake8_result.stdout.decode())
    else:
        print("✅ Flake8: No issues found")
    
    return black_result.returncode == 0 and flake8_result.returncode == 0


def run_type_checking():
    """Run type checking with mypy."""
    print("\nRunning type checking...")
    print("-" * 50)
    
    mypy_result = subprocess.run(
        ['python', '-m', 'mypy', '--ignore-missing-imports', '.'],
        capture_output=True
    )
    
    if mypy_result.returncode != 0:
        print("❌ MyPy found type issues")
        print(mypy_result.stdout.decode())
    else:
        print("✅ MyPy: No type issues found")
    
    return mypy_result.returncode == 0


def generate_test_report():
    """Generate a comprehensive test report."""
    print("\nGenerating test report...")
    print("-" * 50)
    
    # Run tests with junit output
    subprocess.run([
        'pytest',
        '--junit-xml=test-results.xml',
        '--cov=.',
        '--cov-report=html',
        '--cov-report=term',
        'tests/'
    ])
    
    print("\n📊 Test report generated:")
    print("   - Coverage HTML report: htmlcov/index.html")
    print("   - JUnit XML report: test-results.xml")


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description='Run tests for Economics of AI Dashboard')
    parser.add_argument(
        'test_type',
        nargs='?',
        default='all',
        choices=['unit', 'integration', 'e2e', 'performance', 'all'],
        help='Type of tests to run'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-c', '--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('-l', '--lint', action='store_true', help='Run linting checks')
    parser.add_argument('-t', '--typecheck', action='store_true', help='Run type checking')
    parser.add_argument('-r', '--report', action='store_true', help='Generate test report')
    parser.add_argument('-a', '--all-checks', action='store_true', help='Run all checks')
    
    args = parser.parse_args()
    
    # Track overall success
    success = True
    
    # Run linting if requested
    if args.lint or args.all_checks:
        if not run_linting():
            success = False
    
    # Run type checking if requested
    if args.typecheck or args.all_checks:
        if not run_type_checking():
            success = False
    
    # Run tests
    print(f"\nRunning {args.test_type} tests...")
    print("-" * 50)
    
    test_result = run_tests(
        test_type=args.test_type,
        verbose=args.verbose,
        coverage=args.coverage or args.all_checks
    )
    
    if test_result != 0:
        success = False
    
    # Generate report if requested
    if args.report or args.all_checks:
        generate_test_report()
    
    # Summary
    print("\n" + "=" * 50)
    if success:
        print("✅ All checks passed!")
    else:
        print("❌ Some checks failed. Please review the output above.")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())