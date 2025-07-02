#!/usr/bin/env python3
"""
Setup script for automated PDF data extraction
Installs dependencies and validates the automation system
"""

import subprocess
import sys
import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def install_pdf_dependencies():
    """Install PDF processing dependencies"""
    logger.info("Installing PDF processing dependencies...")
    
    dependencies = [
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0"
    ]
    
    for dep in dependencies:
        try:
            logger.info(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            logger.info(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install {dep}: {e}")
            return False
    
    return True


def validate_pdf_libraries():
    """Validate that PDF libraries are working"""
    logger.info("Validating PDF processing libraries...")
    
    try:
        import PyPDF2
        logger.info("✅ PyPDF2 imported successfully")
    except ImportError as e:
        logger.error(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import pdfplumber
        logger.info("✅ pdfplumber imported successfully")
    except ImportError as e:
        logger.error(f"❌ pdfplumber import failed: {e}")
        return False
    
    return True


def check_resources_folder():
    """Check if AI adoption resources folder exists"""
    logger.info("Checking for AI adoption resources folder...")
    
    resources_path = Path("AI adoption resources")
    if not resources_path.exists():
        logger.warning(f"❌ Resources folder not found: {resources_path}")
        logger.info("Creating empty resources folder...")
        resources_path.mkdir(parents=True, exist_ok=True)
        logger.info("✅ Resources folder created")
        return False
    
    # Check for PDF files
    pdf_files = list(resources_path.rglob("*.pdf"))
    if not pdf_files:
        logger.warning("⚠️ No PDF files found in resources folder")
        logger.info("Place your research PDFs in the 'AI adoption resources' folder to enable automation")
        return False
    
    logger.info(f"✅ Found {len(pdf_files)} PDF files in resources folder")
    for pdf in pdf_files[:5]:  # Show first 5
        logger.info(f"  - {pdf.name}")
    if len(pdf_files) > 5:
        logger.info(f"  - ... and {len(pdf_files) - 5} more")
    
    return True


def create_data_directory():
    """Create data directory for caching"""
    logger.info("Creating data directory for caching...")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Test write permissions
    test_file = data_dir / "test_write.tmp"
    try:
        test_file.write_text("test")
        test_file.unlink()
        logger.info("✅ Data directory created with write permissions")
        return True
    except Exception as e:
        logger.error(f"❌ Cannot write to data directory: {e}")
        return False


def test_automation_pipeline():
    """Test the automation pipeline"""
    logger.info("Testing automation pipeline...")
    
    try:
        from data.pipeline_integration import integration_manager
        
        # Get system status
        status = integration_manager.get_system_status()
        
        if status['automation_enabled']:
            logger.info("✅ Automation pipeline is enabled and ready")
            return True
        else:
            logger.warning("⚠️ Automation pipeline is disabled")
            missing = [k for k, v in status['prerequisites'].items() if not v]
            logger.info(f"Missing prerequisites: {missing}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Failed to test automation pipeline: {e}")
        return False


def main():
    """Main setup function"""
    logger.info("🚀 Setting up automated PDF data extraction for AI Adoption Dashboard")
    logger.info("=" * 70)
    
    success_count = 0
    total_steps = 5
    
    # Step 1: Install dependencies
    if install_pdf_dependencies():
        success_count += 1
    
    # Step 2: Validate libraries
    if validate_pdf_libraries():
        success_count += 1
    
    # Step 3: Check resources folder
    if check_resources_folder():
        success_count += 1
    
    # Step 4: Create data directory
    if create_data_directory():
        success_count += 1
    
    # Step 5: Test pipeline
    if test_automation_pipeline():
        success_count += 1
    
    # Summary
    logger.info("=" * 70)
    logger.info(f"Setup completed: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        logger.info("🎉 Automated PDF extraction is fully set up and ready!")
        logger.info("The dashboard will now automatically extract data from PDFs in the resources folder.")
    elif success_count >= 3:
        logger.info("⚠️ Partial setup completed. Some features may not work optimally.")
        logger.info("Please address the issues above for full automation capability.")
    else:
        logger.error("❌ Setup failed. Please install dependencies manually:")
        logger.error("  pip install PyPDF2>=3.0.0 pdfplumber>=0.9.0")
    
    # Next steps
    logger.info("\n📋 Next steps:")
    logger.info("1. Place research PDFs in the 'AI adoption resources' folder")
    logger.info("2. Run the dashboard: streamlit run app.py")
    logger.info("3. Check the sidebar for automation status")


if __name__ == "__main__":
    main()