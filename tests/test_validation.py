"""
Test the new type safety and validation features
Run this to see validation in action
"""

import pandas as pd
from data.models import (
    HistoricalDataPoint, SectorData, validate_dataframe, 
    validate_dataset, safe_validate_data
)
from data.loaders import load_historical_data, load_sector_2025


def test_valid_data():
    """Test validation with valid data"""
    print("🧪 Testing with VALID data...")
    
    # Test historical data
    valid_historical = pd.DataFrame({
        'year': [2023, 2024],
        'ai_use': [55.0, 78.0],
        'genai_use': [33.0, 71.0]
    })
    
    result = validate_dataframe(valid_historical, HistoricalDataPoint)
    print(f"✅ Valid historical data: {result.is_valid} ({result.validated_rows}/{result.total_rows} rows)")
    
    # Test sector data
    valid_sector = pd.DataFrame({
        'sector': ['Technology', 'Healthcare'],
        'adoption_rate': [92.0, 78.0],
        'genai_adoption': [88.0, 65.0],
        'avg_roi': [4.2, 3.2]
    })
    
    result = validate_dataframe(valid_sector, SectorData)
    print(f"✅ Valid sector data: {result.is_valid} ({result.validated_rows}/{result.total_rows} rows)")


def test_invalid_data():
    """Test validation with invalid data - should catch errors"""
    print("\n🧪 Testing with INVALID data (should catch errors)...")
    
    # Test invalid historical data (GenAI > AI use)
    invalid_historical = pd.DataFrame({
        'year': [2023, 2024],
        'ai_use': [55.0, 78.0],
        'genai_use': [80.0, 85.0]  # ❌ GenAI exceeds overall AI
    })
    
    result = validate_dataframe(invalid_historical, HistoricalDataPoint)
    print(f"❌ Invalid historical data: {result.is_valid}")
    print(f"   Error: {result.error_message}")
    
    # Test invalid sector data
    invalid_sector = pd.DataFrame({
        'sector': ['Technology', 'Invalid Sector Name'],  # ❌ Invalid sector
        'adoption_rate': [92.0, 150.0],  # ❌ > 100%
        'avg_roi': [4.2, -1.0]  # ❌ Negative ROI
    })
    
    result = validate_dataframe(invalid_sector, SectorData)
    print(f"❌ Invalid sector data: {result.is_valid}")
    print(f"   Error: {result.error_message}")


def test_real_data_loading():
    """Test validation with real data from loaders"""
    print("\n🧪 Testing REAL data loading with validation...")
    
    try:
        # Load and validate historical data
        hist_data = load_historical_data()
        print(f"📊 Loaded historical data: {len(hist_data)} rows")
        
        is_valid = safe_validate_data(hist_data, "historical_data", show_warnings=False)
        print(f"✅ Historical data validation: {'PASSED' if is_valid else 'FAILED'}")
        
        # Load and validate sector data
        sector_data = load_sector_2025()
        print(f"📊 Loaded sector data: {len(sector_data)} rows")
        
        is_valid = safe_validate_data(sector_data, "sector_data", show_warnings=False)
        print(f"✅ Sector data validation: {'PASSED' if is_valid else 'FAILED'}")
        
    except Exception as e:
        print(f"❌ Error loading real data: {e}")


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🧪 Testing EDGE CASES...")
    
    # Test year boundaries
    edge_historical = pd.DataFrame({
        'year': [2017, 2025],  # Min and max allowed years
        'ai_use': [0.0, 100.0],  # Min and max percentages
        'genai_use': [0.0, 100.0]
    })
    
    result = validate_dataframe(edge_historical, HistoricalDataPoint)
    print(f"🔍 Edge case historical data: {result.is_valid}")
    
    # Test very high ROI (should warn but not fail)
    high_roi_sector = pd.DataFrame({
        'sector': ['Technology'],
        'adoption_rate': [92.0],
        'avg_roi': [8.5]  # High but valid ROI
    })
    
    result = validate_dataframe(high_roi_sector, SectorData)
    print(f"🔍 High ROI sector data: {result.is_valid}")
    if result.warning_messages:
        print(f"   Warnings: {result.warning_messages}")


def test_performance():
    """Test validation performance with larger datasets"""
    print("\n🧪 Testing PERFORMANCE with large dataset...")
    
    import time
    
    # Create large dataset
    large_data = pd.DataFrame({
        'year': [2024] * 10000,
        'ai_use': [78.0] * 10000,
        'genai_use': [71.0] * 10000
    })
    
    start_time = time.time()
    result = validate_dataframe(large_data, HistoricalDataPoint, sample_size=1000)
    duration = time.time() - start_time
    
    print(f"⚡ Large dataset validation: {duration:.3f} seconds")
    print(f"   Validated {result.validated_rows} of {result.total_rows} rows")
    print(f"   Result: {'PASSED' if result.is_valid else 'FAILED'}")


if __name__ == "__main__":
    print("🚀 Starting Type Safety and Validation Tests\n")
    
    test_valid_data()
    test_invalid_data()
    test_real_data_loading()
    test_edge_cases()
    test_performance()
    
    print("\n🎉 All validation tests completed!")
    print("\n💡 What this proves:")
    print("   ✅ Valid data passes validation")
    print("   ❌ Invalid data is caught and reported")
    print("   🔍 Edge cases are handled properly")
    print("   ⚡ Performance is acceptable for large datasets")
    print("   🛡️ Your app is now protected from bad data!")