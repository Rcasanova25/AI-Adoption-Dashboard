#!/usr/bin/env python3
"""
Project Cleanup Script
Removes redundant files and organizes the AI Adoption Dashboard project
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up the project by removing redundant files and organizing structure"""
    
    # Files to remove (redundant or obsolete)
    files_to_remove = [
        # Old app files
        'app.py',  # Old Streamlit app
        'app_dash.py',  # Messy Dash app
        'app_simple.py',
        'app_test_minimal.py',
        'main.py',  # Old main file
        
        # Test files
        'comprehensive_test_script.py',
        'comprehensive_test.py',
        'diagnostic_test.py',
        'final_test_runner_optimized.py',
        'quick_integration_test.py',
        'test_authentic_data_integration.py',
        'test_causal_confidence.py',
        'test_chart_optimization.py',
        'test_memory_import.py',
        'test_memory_management.py',
        'test_oecd_integration.py',
        'test_performance_integration.py',
        'test_performance.py',
        'test_productivity_gain.py',
        'test_realtime_integration.py',
        'test_standard_approach.py',
        'test_streamlit.py',
        'test_structure_validation.py',
        
        # Demo files
        'chart_optimization_demo.py',
        'memory_management_demo.py',
        'performance_demo.py',
        'performance_integration_demo.py',
        'phase_2a_integration_demo.py',
        'simple_integration_demo.py',
        'simple_vizro_demo.py',
        'ui_integration_example.py',
        'working_vizro_dashboard.py',
        
        # Fix scripts
        'fix_capture_calls.py',
        'fix_imports.py',
        'setup_automation.py',
        'setup_test_environment.py',
        
        # Report files
        'FULL_TEST_RESULTS.md',
        'integration_progress_report.md',
        'phase_2b_integration_report.md',
        'phase_2c_integration_report.md',
        'stakeholder_implementation_summary.md',
        'STANDARD_APPROACH_IMPLEMENTATION_SUMMARY.md',
        'SUCCESS_REPORT_95_PERCENT.md',
        'VALIDATION_FIX_SUMMARY.md',
        'CRITICAL_FIXES_SUMMARY.md',
        'DEBUG_BROADCASTING_OPERATIONS.md',
        'DATA_INTEGRATION_STATUS.md',
        'PERFORMANCE_INTEGRATION_STATUS.md',
        'REALTIME_INTEGRATION_SUMMARY.md',
        'REFACTORING_SUMMARY.md',
        'OECD_INTEGRATION_SUMMARY.md',
        'MISSING_ANALYSES_INTEGRATION.md',
        'MCKINSEY_INTEGRATION.md',
        'ANALYST_VIEWS_STATUS.md',
        'ADOPTION_RATES_IMPLEMENTATION.md',
        'AUTOMATED_RESEARCH_INTEGRATION_GUIDE.md',
        'REALTIME_ANALYSIS_GUIDE.md',
        'ROADMAP_TO_95_PERCENT.md',
        'STANDARD_APPROACH.md',
        'STREAMLIT_CLOUD_SETUP.md',
        'TESTING_GUIDE.md',
        'DEPLOYMENT.md',
        'PRODUCTION_CHECKLIST.md',
        
        # Other files
        'changes.diff',
        'investment_case_section.py',
        'run_accessibility_audit.py',
        'run_tests.py',
        'run_vizro_dashboard.py',
        
        # Migration notes
        '# 🚀 Streamlit to Plotly Dash Migration.txt',
        'Back up AI dashboard (detailed data analysis).txt'
    ]
    
    # Directories to remove (redundant or obsolete)
    dirs_to_remove = [
        # Complex nested structures
        'accessibility/',
        'business/',
        'cache/',
        'callbacks/',
        'components/',
        'config/',
        'core/',
        'data/',
        'exports/',
        'layouts/',
        'performance/',
        'realtime/',
        'reports/',
        'scripts/',
        'tests/',
        'Utils/',
        'views/',
        'visualization/',
        
        # Resource directories
        'AI adoption resources/',
        'assets/',
        'docs/',
        'UI/'
    ]
    
    print("🧹 Starting project cleanup...")
    print("=" * 50)
    
    # Remove files
    removed_files = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed file: {file_path}")
                removed_files += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
    
    # Remove directories
    removed_dirs = 0
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removed directory: {dir_path}")
                removed_dirs += 1
            except Exception as e:
                print(f"❌ Failed to remove {dir_path}: {e}")
    
    print("=" * 50)
    print(f"🎉 Cleanup complete!")
    print(f"📁 Removed {removed_files} files")
    print(f"📂 Removed {removed_dirs} directories")
    
    # Create new clean structure
    print("\n📋 Creating clean project structure...")
    
    # Create requirements file
    requirements_content = """dash==2.14.2
dash-bootstrap-components==1.5.0
pandas==2.1.4
plotly==5.17.0
numpy==1.24.3
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("✅ Created clean requirements.txt")
    
    # Create README
    readme_content = """# AI Adoption Dashboard

A clean, modern dashboard for analyzing AI adoption trends from 2018 to 2025.

## Features

- 📊 **Overview**: Key metrics and trends
- 🏭 **Industry Analysis**: Sector-by-sector comparison
- 🌍 **Geographic Analysis**: Regional adoption patterns
- 💡 **Strategic Insights**: Key findings and recommendations

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   python clean_dashboard.py
   ```

3. Open your browser to: http://127.0.0.1:8050

## Data Sources

- AI Index Report 2025
- McKinsey Global Survey
- Goldman Sachs Economics Analysis
- Federal Reserve Research

## Technology Stack

- **Frontend**: Dash (Plotly)
- **Styling**: Bootstrap 5
- **Charts**: Plotly Express & Graph Objects
- **Data**: Pandas & NumPy

## Project Structure

```
AI-Adoption-Dashboard/
├── clean_dashboard.py      # Main dashboard application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── cleanup_project.py     # Cleanup script (can be removed)
```

## Contributing

This is a streamlined version focused on clean, maintainable code. The dashboard provides essential AI adoption analytics without unnecessary complexity.
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✅ Created clean README.md")
    
    print("\n🎯 Project cleanup complete!")
    print("🚀 You can now run: python clean_dashboard.py")

if __name__ == '__main__':
    cleanup_project() 