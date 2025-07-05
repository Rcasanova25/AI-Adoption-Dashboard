#!/usr/bin/env python3
"""Check Python syntax in all project files without external dependencies."""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple

class SyntaxChecker:
    """Check Python syntax in project files."""
    
    def __init__(self, root_dir: Path = None):
        """Initialize syntax checker."""
        self.root_dir = root_dir or Path.cwd()
        self.errors: List[Tuple[str, str]] = []
        self.checked_files = 0
        self.files_with_errors = 0
    
    def check_file(self, filepath: Path) -> bool:
        """Check syntax of a single Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse the file
            ast.parse(content, filename=str(filepath))
            return True
            
        except SyntaxError as e:
            self.errors.append((str(filepath), f"SyntaxError at line {e.lineno}: {e.msg}"))
            return False
        except Exception as e:
            self.errors.append((str(filepath), f"Error: {str(e)}"))
            return False
    
    def check_directory(self, directory: Path, exclude_dirs: List[str] = None) -> None:
        """Recursively check all Python files in a directory."""
        exclude_dirs = exclude_dirs or ['.venv', '__pycache__', '.git', 'venv', 'env']
        
        for item in directory.iterdir():
            if item.is_dir():
                if item.name not in exclude_dirs:
                    self.check_directory(item, exclude_dirs)
            elif item.is_file() and item.suffix == '.py':
                self.checked_files += 1
                if not self.check_file(item):
                    self.files_with_errors += 1
    
    def print_report(self) -> None:
        """Print the syntax check report."""
        print(f"\n{'='*60}")
        print(f"Syntax Check Report")
        print(f"{'='*60}")
        print(f"Files checked: {self.checked_files}")
        print(f"Files with errors: {self.files_with_errors}")
        
        if self.errors:
            print(f"\n❌ Syntax Errors Found:")
            for filepath, error in self.errors:
                print(f"\n  File: {filepath}")
                print(f"  Error: {error}")
        else:
            print(f"\n✅ All files have valid Python syntax!")
    
    def check_critical_files(self) -> bool:
        """Check syntax of critical project files."""
        critical_files = [
            "app.py",
            "utils/error_handler.py",
            "utils/types.py",
            "components/ui/metric_card.py",
            "components/ui/theme.py",
            "views/base.py",
            "config/settings.py",
            "data/data_manager.py",
        ]
        
        print("Checking critical files...")
        all_good = True
        
        for filepath in critical_files:
            full_path = self.root_dir / filepath
            if full_path.exists():
                if self.check_file(full_path):
                    print(f"✅ {filepath}")
                else:
                    print(f"❌ {filepath}")
                    all_good = False
            else:
                print(f"⚠️  {filepath} - File not found")
                all_good = False
        
        return all_good

def check_imports_structure():
    """Check if import statements are properly structured."""
    print("\nChecking import structure...")
    
    import_issues = []
    
    # Check app.py imports
    app_path = Path("app.py")
    if app_path.exists():
        with open(app_path, 'r') as f:
            content = f.read()
        
        # Check for the critical imports that were fixed
        critical_imports = [
            ("from components.ui.metric_card import render_metric_card", "components/ui/metric_card.py"),
            ("from components.ui.theme import ThemeManager", "components/ui/theme.py"),
            ("from utils.error_handler import ErrorHandler", "utils/error_handler.py"),
            ("from utils.types import DashboardData", "utils/types.py"),
            ("from views.base import ViewRegistry", "views/base.py"),
        ]
        
        for import_stmt, file_path in critical_imports:
            if import_stmt in content:
                if Path(file_path).exists():
                    print(f"✅ {import_stmt}")
                else:
                    import_issues.append(f"Import exists but file missing: {file_path}")
                    print(f"❌ {import_stmt} - file missing")
            else:
                import_issues.append(f"Expected import not found: {import_stmt}")
                print(f"⚠️  {import_stmt} - not found in app.py")
    
    return len(import_issues) == 0

def main():
    """Run syntax checks."""
    print("🔍 Python Syntax Checker for AI Adoption Dashboard\n")
    
    checker = SyntaxChecker()
    
    # Check critical files first
    critical_ok = checker.check_critical_files()
    
    # Check import structure
    imports_ok = check_imports_structure()
    
    # Check all Python files
    print("\nChecking all Python files in the project...")
    checker.check_directory(Path.cwd())
    
    # Print report
    checker.print_report()
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"{'='*60}")
    print(f"Critical files syntax: {'✅ PASS' if critical_ok else '❌ FAIL'}")
    print(f"Import structure: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Overall syntax: {'✅ PASS' if checker.files_with_errors == 0 else '❌ FAIL'}")
    
    if checker.files_with_errors == 0 and critical_ok and imports_ok:
        print("\n🎉 All syntax checks passed! The code is ready for testing.")
        print("\nNext step: Install dependencies and run tests")
        print("See INSTALLATION_GUIDE.md for instructions")
    else:
        print("\n⚠️  Some issues were found. Please fix the syntax errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())