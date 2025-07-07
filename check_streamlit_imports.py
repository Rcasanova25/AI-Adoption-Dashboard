#!/usr/bin/env python3
"""
Check for Streamlit imports in the Dash app to identify sources of warnings.
"""
import os
from pathlib import Path
import ast

def check_file_imports(filepath):
    """Check a Python file for Streamlit imports."""
    streamlit_imports = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'streamlit' in alias.name:
                        streamlit_imports.append({
                            'line': node.lineno,
                            'import': f"import {alias.name}",
                            'type': 'direct'
                        })
            elif isinstance(node, ast.ImportFrom):
                if node.module and 'streamlit' in node.module:
                    names = [alias.name for alias in node.names]
                    streamlit_imports.append({
                        'line': node.lineno,
                        'import': f"from {node.module} import {', '.join(names)}",
                        'type': 'direct'
                    })
                # Check for imports from modules that use streamlit
                elif node.module and any(mod in node.module for mod in ['data.data_manager', 'data.data_integration', 'data.services.data_service']):
                    if not 'dash' in node.module:  # Skip dash versions
                        streamlit_imports.append({
                            'line': node.lineno,
                            'import': f"from {node.module} import ...",
                            'type': 'indirect'
                        })
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return streamlit_imports

def main():
    print("=" * 70)
    print("Checking for Streamlit imports in Dash app components")
    print("=" * 70)
    
    # Files to check for the Dash app
    dash_files = [
        "app_dash.py",
        "callbacks/data_callbacks.py",
        "callbacks/view_callbacks.py",
        "callbacks/performance_callbacks.py",
        "dash_view_manager.py"
    ]
    
    # Add all converted view files
    views_dir = Path("views")
    for subdir in views_dir.iterdir():
        if subdir.is_dir():
            for file in subdir.glob("*_dash.py"):
                dash_files.append(str(file))
    
    total_issues = 0
    
    for filepath in dash_files:
        if os.path.exists(filepath):
            imports = check_file_imports(filepath)
            if imports:
                print(f"\n❌ {filepath}:")
                for imp in imports:
                    print(f"   Line {imp['line']}: {imp['import']} ({imp['type']})")
                total_issues += len(imports)
        else:
            print(f"\n⚠️  {filepath} not found")
    
    print("\n" + "=" * 70)
    print("Summary:")
    
    if total_issues == 0:
        print("✅ No Streamlit imports found in Dash app components!")
    else:
        print(f"❌ Found {total_issues} Streamlit-related imports")
        print("\nTo fix Streamlit warnings:")
        print("1. Replace 'from data.data_manager import' with 'from data.data_manager_dash import'")
        print("2. Replace 'from data.data_integration import' with 'from data.data_integration_dash import'")
        print("3. Replace 'from data.services.data_service import' with 'from data.services.data_service_dash import'")
    
    print("=" * 70)

if __name__ == "__main__":
    main()