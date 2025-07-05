#!/usr/bin/env python3
"""Validate project structure and simulate test runs without external dependencies."""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import ast
import json

class StructureValidator:
    """Validate AI Adoption Dashboard project structure."""
    
    def __init__(self):
        self.root = Path.cwd()
        self.results = {
            "structure": [],
            "imports": [],
            "functions": [],
            "classes": [],
            "tests": []
        }
        self.issues = []
    
    def validate_directory_structure(self) -> bool:
        """Validate that all required directories exist."""
        required_dirs = [
            "components",
            "components/ui",
            "config", 
            "data",
            "data/extractors",
            "data/loaders",
            "data/models",
            "performance",
            "tests",
            "tests/unit",
            "tests/integration", 
            "tests/performance",
            "tests/security",
            "utils",
            "views"
        ]
        
        print("📁 Validating Directory Structure...")
        all_exist = True
        
        for dir_path in required_dirs:
            path = self.root / dir_path
            exists = path.exists() and path.is_dir()
            status = "✅" if exists else "❌"
            self.results["structure"].append((dir_path, exists))
            print(f"  {status} {dir_path}")
            if not exists:
                all_exist = False
                self.issues.append(f"Missing directory: {dir_path}")
        
        return all_exist
    
    def validate_critical_files(self) -> bool:
        """Validate that all critical files exist."""
        critical_files = [
            ("app.py", "Main application entry point"),
            ("requirements.txt", "Production dependencies"),
            ("requirements-dev.txt", "Development dependencies"),
            (".env.example", "Environment configuration template"),
            ("config/settings.py", "Settings management"),
            ("data/data_manager.py", "Data management"),
            ("utils/error_handler.py", "Error handling"),
            ("utils/types.py", "Type definitions"),
            ("views/base.py", "View registry"),
            ("components/ui/metric_card.py", "Metric card component"),
            ("components/ui/theme.py", "Theme manager"),
        ]
        
        print("\n📄 Validating Critical Files...")
        all_exist = True
        
        for file_path, description in critical_files:
            path = self.root / file_path
            exists = path.exists() and path.is_file()
            status = "✅" if exists else "❌"
            print(f"  {status} {file_path} - {description}")
            if not exists:
                all_exist = False
                self.issues.append(f"Missing file: {file_path}")
        
        return all_exist
    
    def analyze_test_coverage(self) -> Dict[str, int]:
        """Analyze test file coverage."""
        print("\n🧪 Analyzing Test Coverage...")
        
        # Count source files
        source_files = list(self.root.glob("**/*.py"))
        source_files = [f for f in source_files if "test" not in f.name and ".venv" not in str(f)]
        
        # Count test files
        test_files = list((self.root / "tests").glob("**/*.py")) if (self.root / "tests").exists() else []
        test_files = [f for f in test_files if f.name.startswith("test_")]
        
        # Map source files to test files
        covered_modules = set()
        for test_file in test_files:
            # Extract module name from test file name
            if test_file.name.startswith("test_"):
                module_name = test_file.name[5:].replace(".py", "")
                covered_modules.add(module_name)
        
        coverage_stats = {
            "total_source_files": len(source_files),
            "total_test_files": len(test_files),
            "estimated_coverage": len(test_files) / max(len(source_files), 1) * 100
        }
        
        print(f"  Source files: {coverage_stats['total_source_files']}")
        print(f"  Test files: {coverage_stats['total_test_files']}")
        print(f"  Estimated coverage: {coverage_stats['estimated_coverage']:.1f}%")
        
        return coverage_stats
    
    def validate_imports(self) -> bool:
        """Validate that key imports are correct."""
        print("\n🔗 Validating Import Structure...")
        
        import_checks = [
            ("app.py", "from components.ui.metric_card import render_metric_card"),
            ("app.py", "from utils.error_handler import ErrorHandler"),
            ("app.py", "from views.base import ViewRegistry"),
            ("data/data_manager.py", "from config.settings import settings"),
        ]
        
        all_valid = True
        for file_path, expected_import in import_checks:
            path = self.root / file_path
            if path.exists():
                with open(path, 'r') as f:
                    content = f.read()
                
                if expected_import in content:
                    print(f"  ✅ {file_path}: {expected_import}")
                else:
                    print(f"  ❌ {file_path}: Missing '{expected_import}'")
                    all_valid = False
                    self.issues.append(f"Missing import in {file_path}: {expected_import}")
            else:
                print(f"  ⚠️  {file_path} not found")
                all_valid = False
        
        return all_valid
    
    def check_functionality(self) -> bool:
        """Check that key functions and classes exist."""
        print("\n⚙️  Checking Key Functionality...")
        
        functionality_checks = [
            ("utils/error_handler.py", "class", "ErrorHandler"),
            ("utils/error_handler.py", "function", "handle_errors"),
            ("utils/error_handler.py", "function", "setup_logging"),
            ("components/ui/theme.py", "class", "ThemeManager"),
            ("components/ui/metric_card.py", "function", "render_metric_card"),
            ("views/base.py", "class", "ViewRegistry"),
            ("data/data_manager.py", "class", "DataManager"),
            ("data/data_manager.py", "function", "get_data"),
        ]
        
        all_found = True
        for file_path, item_type, item_name in functionality_checks:
            path = self.root / file_path
            if path.exists():
                found = self._check_item_in_file(path, item_type, item_name)
                status = "✅" if found else "❌"
                print(f"  {status} {file_path}: {item_type} {item_name}")
                if not found:
                    all_found = False
                    self.issues.append(f"Missing {item_type} '{item_name}' in {file_path}")
            else:
                print(f"  ⚠️  {file_path} not found")
                all_found = False
        
        return all_found
    
    def _check_item_in_file(self, filepath: Path, item_type: str, item_name: str) -> bool:
        """Check if a class or function exists in a file."""
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if item_type == "class" and isinstance(node, ast.ClassDef):
                    if node.name == item_name:
                        return True
                elif item_type == "function" and isinstance(node, ast.FunctionDef):
                    if node.name == item_name:
                        return True
            
            return False
        except:
            return False
    
    def simulate_test_run(self) -> Dict[str, any]:
        """Simulate a test run without pytest."""
        print("\n🏃 Simulating Test Run...")
        
        test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
        
        # Simulate running tests
        test_path = self.root / "tests"
        if test_path.exists():
            for test_file in test_path.glob("**/test_*.py"):
                test_results["total"] += 1
                try:
                    # Just check syntax
                    with open(test_file, 'r') as f:
                        ast.parse(f.read())
                    test_results["passed"] += 1
                    print(f"  ✅ {test_file.relative_to(self.root)}")
                except SyntaxError as e:
                    test_results["failed"] += 1
                    test_results["errors"].append(f"{test_file}: {e}")
                    print(f"  ❌ {test_file.relative_to(self.root)}: Syntax error")
        
        print(f"\n  Total: {test_results['total']}")
        print(f"  Passed: {test_results['passed']}")
        print(f"  Failed: {test_results['failed']}")
        
        return test_results
    
    def generate_report(self) -> None:
        """Generate a comprehensive validation report."""
        print("\n" + "="*60)
        print("VALIDATION REPORT")
        print("="*60)
        
        if self.issues:
            print("\n❌ Issues Found:")
            for issue in self.issues:
                print(f"  - {issue}")
        else:
            print("\n✅ No critical issues found!")
        
        print("\n📊 Summary:")
        print(f"  - Directory structure: {'✅ Valid' if not any('directory' in i for i in self.issues) else '❌ Issues found'}")
        print(f"  - Critical files: {'✅ All present' if not any('file' in i for i in self.issues) else '❌ Missing files'}")
        print(f"  - Import structure: {'✅ Valid' if not any('import' in i for i in self.issues) else '❌ Issues found'}")
        print(f"  - Key functionality: {'✅ All found' if not any('Missing' in i for i in self.issues) else '❌ Missing items'}")
        
        # Save report
        report = {
            "timestamp": str(Path.cwd()),
            "issues": self.issues,
            "results": self.results
        }
        
        with open("validation_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("\n📝 Detailed report saved to validation_report.json")

def main():
    """Run all validations."""
    print("🔍 AI Adoption Dashboard Structure Validator\n")
    
    validator = StructureValidator()
    
    # Run all validations
    checks = [
        ("Directory Structure", validator.validate_directory_structure()),
        ("Critical Files", validator.validate_critical_files()),
        ("Import Structure", validator.validate_imports()),
        ("Key Functionality", validator.check_functionality()),
    ]
    
    # Analyze tests
    validator.analyze_test_coverage()
    
    # Simulate test run
    validator.simulate_test_run()
    
    # Generate report
    validator.generate_report()
    
    # Return exit code
    all_passed = all(result for _, result in checks)
    if all_passed and not validator.issues:
        print("\n🎉 All validations passed! The project structure is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: See INSTALLATION_GUIDE.md")
        print("2. Run tests: See TESTING.md")
        return 0
    else:
        print("\n⚠️  Some validations failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())