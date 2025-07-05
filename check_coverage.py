"""Script to check and establish code coverage baseline."""

import os
import subprocess
import sys
from pathlib import Path


def run_coverage_check():
    """Run coverage check and generate report."""
    print("=" * 60)
    print("Economics of AI Dashboard - Code Coverage Report")
    print("=" * 60)

    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Run pytest with coverage
    print("\nRunning tests with coverage analysis...")
    print("-" * 60)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=json",
        "--cov-config=.coveragerc",
        "-v",
        "--tb=short",
    ]

    # Execute coverage command
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Print output
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)

    # Parse coverage results
    if result.returncode == 0:
        parse_coverage_results()
    else:
        print("\n❌ Tests failed. Fix failing tests before checking coverage.")
        return False

    return True


def parse_coverage_results():
    """Parse and display coverage results."""
    try:
        import json

        # Read coverage JSON report
        with open("coverage.json", "r") as f:
            coverage_data = json.load(f)

        total_coverage = coverage_data["totals"]["percent_covered"]

        print("\n" + "=" * 60)
        print("COVERAGE SUMMARY")
        print("=" * 60)
        print(f"Total Coverage: {total_coverage:.1f}%")
        print(f"Target Coverage: 80.0% (per APPDEV.md)")

        if total_coverage >= 80:
            print("✅ Coverage target ACHIEVED!")
        else:
            print(f"❌ Coverage target NOT MET (need {80 - total_coverage:.1f}% more)")

        # Show uncovered files
        print("\n" + "-" * 60)
        print("Files with Low Coverage (<80%):")
        print("-" * 60)

        files = coverage_data["files"]
        low_coverage_files = []

        for file_path, file_data in files.items():
            coverage_percent = file_data["summary"]["percent_covered"]
            if coverage_percent < 80:
                low_coverage_files.append((file_path, coverage_percent))

        # Sort by coverage (lowest first)
        low_coverage_files.sort(key=lambda x: x[1])

        for file_path, coverage in low_coverage_files[:10]:  # Show top 10
            print(f"{coverage:5.1f}% - {file_path}")

        if len(low_coverage_files) > 10:
            print(f"... and {len(low_coverage_files) - 10} more files")

        # Module breakdown
        print("\n" + "-" * 60)
        print("Coverage by Module:")
        print("-" * 60)

        module_coverage = {}
        for file_path, file_data in files.items():
            if file_path.startswith("data/"):
                module = "data"
            elif file_path.startswith("components/"):
                module = "components"
            elif file_path.startswith("tests/"):
                continue  # Skip test files
            else:
                module = "other"

            if module not in module_coverage:
                module_coverage[module] = {"lines": 0, "covered": 0}

            module_coverage[module]["lines"] += file_data["summary"]["num_statements"]
            module_coverage[module]["covered"] += file_data["summary"]["covered_statements"]

        for module, stats in module_coverage.items():
            if stats["lines"] > 0:
                coverage = (stats["covered"] / stats["lines"]) * 100
                print(f"{module:15} {coverage:5.1f}%")

        # Generate recommendations
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS TO IMPROVE COVERAGE:")
        print("=" * 60)

        if total_coverage < 80:
            print("1. Focus on testing these areas:")
            for file_path, coverage in low_coverage_files[:5]:
                if coverage < 50:
                    print(f"   - {file_path} (currently {coverage:.1f}%)")

            print("\n2. Add tests for:")
            print("   - Error handling paths")
            print("   - Edge cases in data loaders")
            print("   - Component rendering variations")
            print("   - Integration scenarios")

            print("\n3. Quick wins:")
            print("   - Test utility functions")
            print("   - Add unit tests for data models")
            print("   - Test accessibility features")

        # Report location
        print("\n" + "-" * 60)
        print("📊 Detailed coverage report: htmlcov/index.html")
        print("📄 Coverage data: coverage.json")

    except FileNotFoundError:
        print("\n❌ Coverage report not found. Make sure tests ran successfully.")
    except Exception as e:
        print(f"\n❌ Error parsing coverage results: {e}")


def create_coverage_config():
    """Create .coveragerc configuration file."""
    coverage_config = """# Coverage.py configuration for Economics of AI Dashboard

[run]
source = .
omit = 
    */tests/*
    */test_*.py
    setup.py
    run_tests.py
    check_coverage.py
    */venv/*
    */env/*
    */__pycache__/*
    */site-packages/*

[report]
precision = 1
show_missing = True
skip_covered = False
skip_empty = True

# Exclude lines from coverage
exclude_lines =
    # Standard pragma
    pragma: no cover
    
    # Don't complain about missing debug-only code
    def __repr__
    if self\\.debug
    
    # Don't complain if tests don't hit defensive assertion code
    raise AssertionError
    raise NotImplementedError
    
    # Don't complain if non-runnable code isn't run
    if 0:
    if __name__ == .__main__.:
    
    # Type checking
    if TYPE_CHECKING:
    @overload

[html]
directory = htmlcov

[json]
output = coverage.json
"""

    with open(".coveragerc", "w") as f:
        f.write(coverage_config)
    print("✅ Created .coveragerc configuration file")


def main():
    """Main function to check coverage."""
    # Create coverage config if it doesn't exist
    if not os.path.exists(".coveragerc"):
        create_coverage_config()

    # Run coverage check
    success = run_coverage_check()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
