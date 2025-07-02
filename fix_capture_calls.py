#!/usr/bin/env python3
"""
Script to fix capture function calls in vizro_dashboard.py
"""

import re

def fix_capture_calls():
    """Fix all capture function calls in the file"""
    
    with open('visualization/vizro_dashboard.py', 'r') as f:
        content = f.read()
    
    # Pattern to match capture("name")(function_call)
    pattern = r'capture\("([^"]+)"\)\s*\(\s*([^)]+)\s*\)'
    
    # Replace with just the function call
    fixed_content = re.sub(pattern, r'\2()', content)
    
    with open('visualization/vizro_dashboard.py', 'w') as f:
        f.write(fixed_content)
    
    print("Fixed capture function calls in vizro_dashboard.py")

if __name__ == "__main__":
    fix_capture_calls() 