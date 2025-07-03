#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Cleanup Script
Removes remaining redundant files while preserving essential functionality
"""

import os
import shutil

def final_cleanup():
    """Remove remaining redundant files"""
    
    # Files to remove (redundant or obsolete)
    files_to_remove = [
        'simple_dashboard.py',
        'clean_dashboard.py', 
        'cleanup_project.py',
        'diagnose_data_loading.py',
        'pytest.ini',
        'requirements-test.txt',
        '.coverage',
        '.Rhistory',
        'Makefile',
        'pyproject.toml',
        '.coveragerc'
    ]
    
    # Directories to remove (if they exist and are empty)
    dirs_to_remove = [
        '.mypy_cache',
        '.pytest_cache', 
        '.hypothesis',
        '.benchmarks',
        '__pycache__',
        '.venv',
        '.devcontainer',
        '.github'
    ]
    
    print("🧹 Final cleanup of remaining redundant files...")
    
    removed_files = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
                removed_files += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
    
    removed_dirs = 0
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed directory: {dir_path}")
                removed_dirs += 1
            except Exception as e:
                print(f"❌ Failed to remove {dir_path}: {e}")
    
    print(f"🎉 Final cleanup complete! Removed {removed_files} files and {removed_dirs} directories")
    print("🚀 Your sophisticated dashboard is now clean and ready!")

if __name__ == '__main__':
    final_cleanup()
