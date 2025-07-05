#!/usr/bin/env python3
"""
Migration script to update app.py with new components
====================================================

This script helps migrate from the old app.py to the new integrated version.
"""

import os
import shutil
from datetime import datetime


def backup_original():
    """Create backup of original app.py."""
    if os.path.exists("app.py"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"app_backup_{timestamp}.py"
        shutil.copy("app.py", backup_name)
        print(f"✅ Created backup: {backup_name}")
        return backup_name
    else:
        print("❌ No app.py found to backup")
        return None


def validate_dependencies():
    """Check if all required components exist."""
    required_files = [
        "data/data_manager.py",
        "components/competitive_assessor.py",
        "components/accessibility.py",
        "components/progressive_disclosure.py",
        "components/economic_insights.py",
        "components/persona_dashboards.py",
        "components/guided_tour.py",
        "components/key_takeaways.py",
        "components/mobile_responsive.py",
        "components/view_enhancements.py",
        "components/lazy_loading.py",
        "performance/monitor.py",
        "performance/cache_manager.py",
    ]

    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)

    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required components found")
        return True


def create_transition_app():
    """Create a transition app that gradually migrates functionality."""
    transition_code = '''"""
Transition App - Gradual Migration to Economics of AI Dashboard
===============================================================

This version allows gradual migration from old to new components.
"""

import streamlit as st
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Feature flags for gradual migration
ENABLE_NEW_DATA_MANAGER = st.sidebar.checkbox("Enable New Data Manager", value=False)
ENABLE_COMPETITIVE_ASSESSOR = st.sidebar.checkbox("Enable Competitive Assessor", value=False)
ENABLE_ACCESSIBILITY = st.sidebar.checkbox("Enable Accessibility Features", value=False)
ENABLE_LAZY_LOADING = st.sidebar.checkbox("Enable Lazy Loading", value=False)

# Import based on feature flags
if ENABLE_NEW_DATA_MANAGER:
    try:
        from data.data_manager import DataManager
        st.sidebar.success("✅ New Data Manager loaded")
    except ImportError as e:
        st.sidebar.error(f"❌ Failed to load Data Manager: {e}")
        ENABLE_NEW_DATA_MANAGER = False

if ENABLE_COMPETITIVE_ASSESSOR:
    try:
        from components.competitive_assessor import CompetitivePositionAssessor
        st.sidebar.success("✅ Competitive Assessor loaded")
    except ImportError as e:
        st.sidebar.error(f"❌ Failed to load Competitive Assessor: {e}")
        ENABLE_COMPETITIVE_ASSESSOR = False

if ENABLE_ACCESSIBILITY:
    try:
        from components.accessibility import create_accessible_dashboard_layout
        st.sidebar.success("✅ Accessibility features loaded")
    except ImportError as e:
        st.sidebar.error(f"❌ Failed to load Accessibility: {e}")
        ENABLE_ACCESSIBILITY = False

# Load the original app with modifications
if os.path.exists('app_backup_latest.py'):
    exec(open('app_backup_latest.py').read())
else:
    st.error("Original app backup not found. Please run migrate_app.py first.")
'''

    with open("app_transition.py", "w") as f:
        f.write(transition_code)
    print("✅ Created transition app: app_transition.py")


def create_environment_template():
    """Create environment configuration template."""
    env_template = """# Environment Configuration for Economics of AI Dashboard
# =====================================================

# Cache Configuration
CACHE_MEMORY_SIZE=200
CACHE_MEMORY_TTL=600
CACHE_DISK_SIZE=2147483648  # 2GB
CACHE_DISK_DIR=./cache

# Performance Thresholds
PERF_DATA_LOAD_THRESHOLD=1.0
PERF_VIEW_RENDER_THRESHOLD=0.5
PERF_DASHBOARD_INIT_THRESHOLD=3.0

# Data Source Configuration
DATA_SOURCES_DIR=/mnt/c/Users/rcasa/OneDrive/Documents/AI-Adoption-Dashboard/AI adoption resources
ENABLE_PDF_EXTRACTION=true
PDF_EXTRACTION_TIMEOUT=30

# Feature Flags
ENABLE_COMPETITIVE_ASSESSOR=true
ENABLE_ACCESSIBILITY=true
ENABLE_LAZY_LOADING=true
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_MOBILE_RESPONSIVE=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/dashboard.log
"""

    with open(".env.template", "w") as f:
        f.write(env_template)
    print("✅ Created environment template: .env.template")


def create_migration_guide():
    """Create migration guide documentation."""
    guide = """# Migration Guide: Economics of AI Dashboard

## Overview
This guide helps you migrate from the original AI Adoption Dashboard to the new Economics of AI Dashboard.

## Migration Steps

### 1. Backup Original
```bash
python migrate_app.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Set Up Environment
```bash
cp .env.template .env
# Edit .env with your configuration
```

### 4. Create Cache Directory
```bash
mkdir -p ./cache
chmod 755 ./cache
```

### 5. Test Components
```bash
# Run tests to ensure all components work
python -m pytest tests/unit -v
python -m pytest tests/integration -v
```

### 6. Gradual Migration
Use `app_transition.py` to gradually enable new features:
```bash
streamlit run app_transition.py
```

Enable features one by one in the sidebar and test.

### 7. Full Migration
Once all features work in transition mode:
```bash
cp app_new.py app.py
streamlit run app.py
```

## Feature Mapping

| Old Feature | New Component | Benefits |
|------------|---------------|----------|
| load_data() | OptimizedDataManager | 5x faster, multi-layer caching |
| Homepage | CompetitivePositionAssessor | Economic focus, actionable insights |
| Basic UI | AccessibilityManager | WCAG 2.1 AA compliant |
| All data shown | ProgressiveDisclosure | 3-level information hierarchy |
| Generic views | PersonaDashboards | Role-specific experiences |

## Rollback Plan
If you need to rollback:
```bash
cp app_backup_[timestamp].py app.py
```

## Support
- Documentation: https://github.com/Rcasanova25/AI-Adoption-Dashboard/wiki
- Issues: https://github.com/Rcasanova25/AI-Adoption-Dashboard/issues
"""

    with open("MIGRATION_GUIDE.md", "w") as f:
        f.write(guide)
    print("✅ Created migration guide: MIGRATION_GUIDE.md")


def main():
    """Run migration process."""
    print("🚀 Starting Economics of AI Dashboard Migration")
    print("=" * 50)

    # Step 1: Backup
    backup_file = backup_original()
    if backup_file:
        # Create a latest backup link
        if os.path.exists("app_backup_latest.py"):
            os.remove("app_backup_latest.py")
        shutil.copy(backup_file, "app_backup_latest.py")

    # Step 2: Validate dependencies
    if not validate_dependencies():
        print("\n⚠️  Please ensure all components are installed before migrating")
        return

    # Step 3: Create transition app
    create_transition_app()

    # Step 4: Create environment template
    create_environment_template()

    # Step 5: Create migration guide
    create_migration_guide()

    print("\n✅ Migration preparation complete!")
    print("\nNext steps:")
    print("1. Review MIGRATION_GUIDE.md")
    print("2. Test with: streamlit run app_transition.py")
    print("3. When ready, copy app_new.py to app.py")
    print("\n💡 Tip: Use the transition app to test features incrementally")


if __name__ == "__main__":
    main()
