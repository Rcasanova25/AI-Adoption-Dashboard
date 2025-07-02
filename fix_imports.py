#!/usr/bin/env python3
"""
Quick script to fix import path issues
Changes 'utils' to 'Utils' throughout the codebase
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix import statements in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace utils imports with Utils
        original_content = content
        content = re.sub(r'from utils\.', 'from Utils.', content)
        content = re.sub(r'import utils\.', 'import Utils.', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed imports in {file_path}")
            return True
        else:
            print(f"⚪ No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def fix_all_imports():
    """Fix imports throughout the project"""
    print("🔧 Fixing import statements throughout the project...")
    
    project_root = Path(__file__).parent
    
    # Directories to check
    directories_to_check = [
        project_root / "views",
        project_root / "data",
        project_root / "business",
        project_root / "core",
        project_root / "components"
    ]
    
    files_fixed = 0
    files_checked = 0
    
    for directory in directories_to_check:
        if directory.exists():
            print(f"\n📁 Checking {directory.name}/ directory...")
            
            # Find all Python files
            python_files = list(directory.glob("*.py"))
            
            for py_file in python_files:
                files_checked += 1
                if fix_imports_in_file(py_file):
                    files_fixed += 1
    
    print(f"\n📊 Summary:")
    print(f"   Files checked: {files_checked}")
    print(f"   Files fixed: {files_fixed}")
    
    if files_fixed > 0:
        print("✅ Import fixes applied successfully!")
    else:
        print("ℹ️ No import fixes needed")
    
    return files_fixed

if __name__ == "__main__":
    print("🚀 Import Fix Utility")
    print("=" * 40)
    
    fixes_applied = fix_all_imports()
    
    print("\n" + "=" * 40)
    if fixes_applied > 0:
        print("🎉 Import fixes complete!")
        print("🚀 Ready to test dashboard: streamlit run main.py")
    else:
        print("✅ No import issues found")
        print("🚀 Dashboard should run: streamlit run main.py")