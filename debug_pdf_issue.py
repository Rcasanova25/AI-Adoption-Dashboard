#!/usr/bin/env python3
"""Debug script to identify PDF extraction permission denied issue."""

import logging
from pathlib import Path
from config.settings import settings
from data.loaders.ai_index import AIIndexLoader
from data.loaders.strategy import AIStrategyLoader

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Debug the PDF extraction issue."""
    print("=== Debugging PDF Extraction Issue ===\n")
    
    # Check settings
    print(f"Settings RESOURCES_PATH: {settings.RESOURCES_PATH}")
    resources_path = settings.get_resources_path()
    print(f"Resources path object: {resources_path}")
    print(f"Resources path exists: {resources_path.exists()}")
    print(f"Resources path is dir: {resources_path.is_dir() if resources_path.exists() else 'N/A'}")
    
    # List actual directory
    actual_dir = Path("/mnt/c/Users/rcasa/OneDrive/Documents/ai-adoption-dashboard/AI adoption resources")
    print(f"\nActual directory exists: {actual_dir.exists()}")
    print(f"Actual directory is dir: {actual_dir.is_dir() if actual_dir.exists() else 'N/A'}")
    
    # Check subdirectory
    subdir = actual_dir / "AI dashboard resources 1"
    print(f"\nSubdirectory path: {subdir}")
    print(f"Subdirectory exists: {subdir.exists()}")
    
    # List PDF files
    if subdir.exists():
        pdf_files = list(subdir.glob("*.pdf"))
        print(f"\nPDF files found: {len(pdf_files)}")
        for pdf in pdf_files[:5]:  # Show first 5
            print(f"  - {pdf.name}")
    
    # Try to load AI Index
    print("\n=== Testing AI Index Loader ===")
    try:
        loader = AIIndexLoader()
        print(f"Loader initialized: {loader}")
        print(f"Loader file path: {loader.source.file_path}")
        print(f"File exists: {loader.source.file_path.exists() if loader.source.file_path else 'None'}")
        
        # Try to load data
        data = loader.load()
        print(f"Data loaded successfully: {list(data.keys())}")
    except Exception as e:
        print(f"Error loading AI Index: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    # Try to load Strategy
    print("\n=== Testing Strategy Loader ===")
    try:
        loader = AIStrategyLoader()
        print(f"Loader initialized: {loader}")
        print(f"Loader file path: {loader.source.file_path}")
        print(f"File exists: {loader.source.file_path.exists() if loader.source.file_path else 'None'}")
    except Exception as e:
        print(f"Error loading Strategy: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()