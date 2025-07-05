#!/usr/bin/env python3
"""Comprehensive verification of all critical fixes."""

import ast
import os
from pathlib import Path

def check_file_exists(filepath):
    """Check if a file exists and return status."""
    exists = Path(filepath).exists()
    return exists, f"{'✅' if exists else '❌'} {filepath}"

def check_class_exists(filepath, classname):
    """Check if a class exists in a file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == classname:
                return True, f"✅ {classname} found in {filepath}"
        return False, f"❌ {classname} NOT found in {filepath}"
    except Exception as e:
        return False, f"❌ Error checking {filepath}: {e}"

def check_function_exists(filepath, funcname):
    """Check if a function exists in a file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == funcname:
                return True, f"✅ {funcname} found in {filepath}"
        return False, f"❌ {funcname} NOT found in {filepath}"
    except Exception as e:
        return False, f"❌ Error checking {filepath}: {e}"

def check_import_exists(filepath, module, item=None):
    """Check if an import exists in a file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        if item:
            import_line = f"from {module} import {item}"
        else:
            import_line = f"import {module}"
        
        if import_line in content or (item and f"from {module} import" in content and item in content):
            return True, f"✅ Import '{import_line}' found in {filepath}"
        return False, f"❌ Import '{import_line}' NOT found in {filepath}"
    except Exception as e:
        return False, f"❌ Error checking import in {filepath}: {e}"

def main():
    """Run all verification checks."""
    print("🔍 Verifying Critical Fixes for AI Adoption Dashboard\n")
    
    all_checks = []
    
    # 1. Check critical files exist
    print("1️⃣ Checking Critical Files Exist:")
    files_to_check = [
        "components/ui/__init__.py",
        "components/ui/metric_card.py",
        "components/ui/theme.py",
        "utils/__init__.py",
        "utils/error_handler.py",
        "utils/types.py",
        "views/base.py",
        "config/__init__.py",
        "config/settings.py",
        ".env.example",
        "app.py",
    ]
    
    for filepath in files_to_check:
        status, msg = check_file_exists(filepath)
        all_checks.append(status)
        print(f"   {msg}")
    
    # 2. Check critical classes exist
    print("\n2️⃣ Checking Critical Classes:")
    classes_to_check = [
        ("utils/error_handler.py", "ErrorHandler"),
        ("components/ui/theme.py", "ThemeManager"),
        ("views/base.py", "ViewRegistry"),
        ("config/settings.py", "Settings"),
        ("data/data_manager.py", "DataManager"),
    ]
    
    for filepath, classname in classes_to_check:
        status, msg = check_class_exists(filepath, classname)
        all_checks.append(status)
        print(f"   {msg}")
    
    # 3. Check critical functions exist
    print("\n3️⃣ Checking Critical Functions:")
    functions_to_check = [
        ("utils/error_handler.py", "handle_errors"),
        ("utils/error_handler.py", "setup_logging"),
        ("components/ui/metric_card.py", "render_metric_card"),
        ("data/data_manager.py", "get_data"),
    ]
    
    for filepath, funcname in functions_to_check:
        status, msg = check_function_exists(filepath, funcname)
        all_checks.append(status)
        print(f"   {msg}")
    
    # 4. Check critical type definitions
    print("\n4️⃣ Checking Type Definitions:")
    with open("utils/types.py", 'r') as f:
        content = f.read()
    
    if "DashboardData" in content and "TypedDict" in content:
        all_checks.append(True)
        print("   ✅ DashboardData TypedDict found in utils/types.py")
    else:
        all_checks.append(False)
        print("   ❌ DashboardData TypedDict NOT found in utils/types.py")
    
    # 5. Check hardcoded paths are removed
    print("\n5️⃣ Checking Hardcoded Paths Removed:")
    with open("data/data_manager.py", 'r') as f:
        content = f.read()
    
    if "/mnt/c/Users/rcasa/OneDrive" in content:
        all_checks.append(False)
        print("   ❌ Hardcoded path still exists in data_manager.py")
    else:
        all_checks.append(True)
        print("   ✅ Hardcoded paths removed from data_manager.py")
    
    # 6. Check settings import in data_manager
    status, msg = check_import_exists("data/data_manager.py", "config.settings", "settings")
    all_checks.append(status)
    print(f"   {msg}")
    
    # 7. Check directory structure
    print("\n6️⃣ Checking Directory Structure:")
    if Path("utils").exists() and Path("utils").is_dir():
        all_checks.append(True)
        print("   ✅ utils/ directory exists (lowercase)")
    else:
        all_checks.append(False)
        print("   ❌ utils/ directory missing")
    
    if Path("Utils").exists():
        all_checks.append(False)
        print("   ❌ Utils/ directory still exists (should be lowercase)")
    else:
        all_checks.append(True)
        print("   ✅ Utils/ directory removed (correct)")
    
    # Summary
    print("\n" + "="*60)
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🎉 All critical fixes have been successfully implemented!")
        print("The application structure is ready for dependency installation and testing.")
    else:
        print(f"❌ SOME CHECKS FAILED ({passed}/{total} passed)")
        print("\n⚠️  Please review the failed checks above.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())