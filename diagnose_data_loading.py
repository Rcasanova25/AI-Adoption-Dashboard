#!/usr/bin/env python3
"""
Data Loading Diagnostics Script
Run this script to diagnose any data loading issues in the AI Adoption Dashboard
"""

import streamlit as st
import os
import sys

def main():
    st.title("🔍 Data Loading Diagnostics")
    st.markdown("This script helps diagnose data loading issues in the AI Adoption Dashboard")
    
    # Diagnostic 1: Check if imports are working
    st.header("📦 Import Diagnostics")
    
    try:
        from data.loaders import load_all_datasets, get_dynamic_metrics, load_complete_datasets
        st.success("✅ Successfully imported data.loaders functions")
    except ImportError as e:
        st.error(f"❌ Import error: {e}")
        st.info("Check if data/loaders.py exists and is properly structured")
    
    try:
        from data.models import safe_validate_data, ValidationResult
        st.success("✅ Successfully imported data.models")
    except ImportError as e:
        st.error(f"❌ Import error for data.models: {e}")
    
    # Diagnostic 2: Check if data directory exists
    st.header("📁 Directory Structure")
    
    if os.path.exists("data"):
        st.success("✅ data/ directory exists")
        data_files = os.listdir("data")
        st.write(f"Files in data/: {data_files}")
    else:
        st.error("❌ data/ directory not found")
    
    # Diagnostic 3: Test the actual data loading function
    st.header("🔄 Data Loading Test")
    
    try:
        st.write("Testing load_all_datasets()...")
        test_result = load_all_datasets()
        if test_result is None:
            st.error("❌ load_all_datasets() returned None")
        elif isinstance(test_result, dict):
            st.success(f"✅ load_all_datasets() returned dict with {len(test_result)} keys")
            st.write("Available datasets:", list(test_result.keys()))
            
            # Check if datasets have data
            for key, value in test_result.items():
                if value is None:
                    st.warning(f"⚠️ {key}: None")
                elif hasattr(value, 'shape'):
                    st.info(f"📊 {key}: {value.shape[0]} rows × {value.shape[1]} cols")
                else:
                    st.info(f"📊 {key}: {type(value)}")
        else:
            st.warning(f"⚠️ load_all_datasets() returned unexpected type: {type(test_result)}")
            
    except Exception as e:
        st.error(f"❌ Error calling load_all_datasets(): {e}")
        st.write("Full error:", str(e))
    
    # Diagnostic 4: Check specific data files
    st.header("📄 Expected Data Files")
    
    expected_files = [
        "ai_adoption_historical.csv",
        "sector_adoption_2025.csv", 
        "firm_size_adoption.csv",
        "financial_impact.csv",
        "barriers_support.csv"
    ]
    
    for file in expected_files:
        if os.path.exists(f"data/{file}"):
            st.success(f"✅ Found: data/{file}")
        else:
            st.error(f"❌ Missing: data/{file}")
    
    # Diagnostic 5: Test direct data creation
    st.header("🎯 Direct Data Creation Test")
    
    try:
        from app import create_comprehensive_datasets
        st.write("Testing create_comprehensive_datasets()...")
        direct_data = create_comprehensive_datasets()
        
        if direct_data and isinstance(direct_data, dict):
            st.success(f"✅ Direct data creation successful: {len(direct_data)} datasets")
            
            # Show dataset details
            for key, value in direct_data.items():
                if value is not None and hasattr(value, 'shape'):
                    st.info(f"📊 {key}: {value.shape[0]} rows × {value.shape[1]} cols")
                elif value is None:
                    st.warning(f"⚠️ {key}: None (optional dataset)")
                else:
                    st.info(f"📊 {key}: {type(value)}")
        else:
            st.error("❌ Direct data creation failed")
            
    except Exception as e:
        st.error(f"❌ Error in direct data creation: {e}")
    
    # Diagnostic 6: Environment check
    st.header("🔧 Environment Check")
    
    st.write(f"Python version: {sys.version}")
    st.write(f"Working directory: {os.getcwd()}")
    
    # Check for required packages
    required_packages = ['pandas', 'streamlit', 'plotly', 'numpy']
    for package in required_packages:
        try:
            __import__(package)
            st.success(f"✅ {package} available")
        except ImportError:
            st.error(f"❌ {package} not available")
    
    st.markdown("---")
    st.info("💡 **Note:** If external data loading is failing, the dashboard now uses direct data creation in app.py")

if __name__ == "__main__":
    main() 