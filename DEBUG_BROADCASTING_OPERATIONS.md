# Debug Output for Broadcasting Operations

This document lists all the debug output I've added to help diagnose broadcasting errors in the AI Adoption Dashboard codebase.

## Overview

Broadcasting errors occur when numpy/pandas arrays have incompatible shapes for element-wise operations. The debug output will help identify:
- Array shapes and types
- Data types and compatibility
- Length mismatches
- NaN or invalid values
- Broadcasting compatibility

## Files Modified with Debug Output

### 1. ui_integration_example.py

**Location:** Lines 335-365 (Risk Score Calculation)
**Debug Output Added:**
- sector_data shape and columns
- num_sectors count
- adoption_rate column type and values
- base_adjustments array details
- risk_adjustments after resize
- adoption_values type, shape, and content
- NaN/inf checks
- Broadcasting compatibility test
- Step-by-step calculation with error handling
- Fallback calculation details

**Purpose:** Diagnose the specific broadcasting error in risk score calculation where `sector_data['adoption_rate'].values + risk_adjustments` fails.

### 2. app.py

**Location:** Lines 144-200 (get_dynamic_metrics function)
**Debug Output Added:**
- Historical data operations debug
- Cost reduction operations debug
- Investment operations debug
- ROI operations debug
- Each operation includes:
  - DataFrame shape and columns
  - Individual value extraction and types
  - Calculation results
  - Error handling with fallback values

**Purpose:** Diagnose potential broadcasting issues in dynamic metrics calculations.

### 3. data/loaders.py

**Location:** Lines 350-450 (get_dynamic_metrics function)
**Debug Output Added:**
- Historical data operations debug (print statements)
- Investment operations debug (print statements)
- ROI operations debug (print statements)
- Each operation includes:
  - DataFrame shape and columns
  - Individual value extraction and types
  - Calculation results
  - Error handling with fallback values

**Purpose:** Diagnose potential broadcasting issues in data loader calculations.

### 4. components/charts.py

**Location:** Lines 540-580 (demo_charts function)
**Debug Output Added:**
- trend_data creation debug
- industry_data creation debug
- Array shape and type information
- Broadcasting test operations
- Test calculations with numpy arrays
- Shape compatibility checks

**Purpose:** Diagnose potential broadcasting issues in chart component data operations.

### 5. app_backup.py

**Location:** Lines 1435-1460 (Milestone Operations)
**Debug Output Added:**
- filtered_data shape and columns
- year column type and values
- Milestone year checking process
- Individual milestone processing with error handling

**Purpose:** Diagnose potential broadcasting issues in milestone data operations.

## How to Use the Debug Output

1. **Run the application** and navigate to the section causing the broadcasting error
2. **Look for debug output** starting with "🔍 DEBUG:"
3. **Check array shapes** to identify mismatches
4. **Verify data types** for compatibility
5. **Look for error messages** with detailed exception information
6. **Use the debug information** to fix the broadcasting issue

## Common Broadcasting Issues to Look For

1. **Shape Mismatches:**
   - Arrays with different lengths
   - 1D vs 2D array operations
   - Missing or extra dimensions

2. **Data Type Issues:**
   - Mixed numeric and string types
   - NaN or infinite values
   - Incompatible dtypes

3. **Index Problems:**
   - DataFrame vs Series operations
   - .values vs .iloc operations
   - Reset index issues

## Example Debug Output Interpretation

```
🔍 DEBUG: Risk Score Calculation
• sector_data shape: (8, 3)
• adoption_rate length: 8
• risk_adjustments length: 8
• adoption_rate: [92, 85, 78, 75, 72, 68, 65, 58]
• risk_adjustments: [5, -5, 10, 15, 0, -10, 8, -3]
```

This shows that both arrays have length 8, so the broadcasting should work. If there's still an error, check for:
- Data types (int vs float)
- NaN values
- Array vs Series operations

## Next Steps

1. Run the application with debug output enabled
2. Identify the specific broadcasting error location
3. Use the debug information to fix the array operation
4. Remove debug output once the issue is resolved
5. Add proper error handling for future robustness

## Files to Test

1. `ui_integration_example.py` - Main broadcasting error location
2. `app.py` - Dynamic metrics calculations
3. `components/charts.py` - Chart data operations
4. `data/loaders.py` - Data loading operations
5. `app_backup.py` - Milestone operations

Each file now has comprehensive debug output to help identify and resolve broadcasting errors. 