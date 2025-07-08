#!/usr/bin/env python3
"""Test script to verify PDF loading works correctly."""

import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Test PDF loading."""
    print("=== Testing PDF Loading ===\n")
    
    # Import settings
    from config.settings import settings
    
    print(f"Resources path from settings: {settings.RESOURCES_PATH}")
    resources_path = settings.get_resources_path()
    print(f"Resources path object: {resources_path}")
    print(f"Resources path exists: {resources_path.exists()}")
    
    # Check subdirectory
    subdir = resources_path / "AI dashboard resources 1"
    print(f"\nSubdirectory path: {subdir}")
    print(f"Subdirectory exists: {subdir.exists()}")
    
    # List PDF files
    if subdir.exists():
        pdf_files = list(subdir.glob("*.pdf"))
        print(f"\nPDF files found: {len(pdf_files)}")
        for pdf in pdf_files[:5]:
            print(f"  - {pdf.name}")
    
    # Test AI Index loader
    print("\n=== Testing AI Index Loader ===")
    try:
        from data.loaders.ai_index import AIIndexLoader
        loader = AIIndexLoader()
        print(f"Loader initialized: {loader}")
        print(f"Loader file path: {loader.source.file_path}")
        print(f"File exists: {loader.source.file_path.exists() if loader.source.file_path else 'None'}")
        print(f"Has extractor: {loader.extractor is not None}")
        
        # Try to load data
        data = loader.load()
        print(f"Data loaded successfully! Datasets: {list(data.keys())}")
        
        # Show sample data
        for key, df in data.items():
            if not df.empty:
                print(f"\n{key}: {len(df)} rows")
                print(df.head(2))
                break
                
    except Exception as e:
        print(f"Error loading AI Index: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    # Test data manager
    print("\n=== Testing Data Manager ===")
    try:
        from data.data_manager_dash import DataManagerDash as DataManager
        dm = DataManager()
        print("DataManager initialized")
        
        # Try to load all data
        all_data = dm.load_all_data()
        print(f"Loaded {len(all_data)} datasets")
        
        for key in list(all_data.keys())[:3]:
            print(f"  - {key}")
            
    except Exception as e:
        print(f"Error with DataManager: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()