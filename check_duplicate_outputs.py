#!/usr/bin/env python3
"""
Check for duplicate callback outputs in the Dash app.
"""
import ast
import re
from pathlib import Path
from collections import defaultdict

def extract_outputs(node):
    """Extract output IDs from a callback decorator."""
    outputs = []
    
    for decorator in node.decorator_list:
        # Check if it's an app.callback decorator
        if (isinstance(decorator, ast.Call) and 
            isinstance(decorator.func, ast.Attribute) and
            decorator.func.attr == 'callback'):
            
            # Find Output arguments
            for arg in decorator.args:
                if isinstance(arg, ast.Call) and getattr(arg.func, 'id', None) == 'Output':
                    # Single output
                    if len(arg.args) >= 2:
                        component_id = ast.literal_eval(arg.args[0])
                        prop = ast.literal_eval(arg.args[1])
                        outputs.append(f"{component_id}.{prop}")
                elif isinstance(arg, ast.List):
                    # Multiple outputs
                    for item in arg.elts:
                        if isinstance(item, ast.Call) and getattr(item.func, 'id', None) == 'Output':
                            if len(item.args) >= 2:
                                component_id = ast.literal_eval(item.args[0])
                                prop = ast.literal_eval(item.args[1])
                                outputs.append(f"{component_id}.{prop}")
    
    return outputs

def check_duplicate_outputs(directory):
    """Check all Python files in directory for duplicate outputs."""
    all_outputs = defaultdict(list)
    
    # Check all Python files
    for py_file in Path(directory).rglob("*.py"):
        # Skip test files and __pycache__
        if "__pycache__" in str(py_file) or "test_" in py_file.name:
            continue
            
        try:
            with open(py_file, 'r') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Find all callbacks
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    outputs = extract_outputs(node)
                    for output in outputs:
                        all_outputs[output].append({
                            'file': str(py_file),
                            'function': node.name,
                            'line': node.lineno
                        })
        except Exception as e:
            print(f"Error parsing {py_file}: {e}")
    
    # Find duplicates
    duplicates = {k: v for k, v in all_outputs.items() if len(v) > 1}
    
    return duplicates

def main():
    print("=" * 60)
    print("Checking for Duplicate Callback Outputs")
    print("=" * 60)
    
    # Check callbacks directory and app_dash.py
    duplicates = check_duplicate_outputs(".")
    
    if duplicates:
        print("\n❌ Found duplicate outputs:\n")
        for output_id, locations in duplicates.items():
            print(f"Output: {output_id}")
            for loc in locations:
                print(f"  - {loc['file']}:{loc['line']} in {loc['function']}()")
            print()
    else:
        print("\n✅ No duplicate outputs found!")
    
    # Summary
    print("=" * 60)
    if duplicates:
        print(f"Found {len(duplicates)} duplicate output(s) that need to be fixed.")
    else:
        print("All callbacks have unique outputs. The app should run without errors.")

if __name__ == "__main__":
    main()