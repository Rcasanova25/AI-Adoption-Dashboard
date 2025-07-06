# Phase 1: Data Integrity & CLAUDE.md Compliance - Implementation Plan

## Overview
This plan addresses the removal of all fallback/sample data logic and enforcement of CLAUDE.md compliance, ensuring only real, validated data is used throughout the application.

## Current State Analysis
- **9 TODO comments** in views need to be connected to real data sources
- **Fallback data logic** exists in all data loaders (ai_index.py, mckinsey.py, etc.)
- **Empty DataFrames** in views instead of proper data loading
- **No visible failure** when data is missing or invalid

## Implementation Steps

### Step 1: Remove Fallback Data Logic from Loaders
1. **Remove from each loader**:
   - `_get_fallback_datasets()` methods
   - Fallback logic in `load()` methods
   - Replace with proper error propagation

2. **Files to modify**:
   - `data/loaders/ai_index.py`
   - `data/loaders/mckinsey.py`
   - `data/loaders/goldman_sachs.py`
   - `data/loaders/oecd.py`
   - `data/loaders/imf.py`
   - `data/loaders/academic.py`
   - `data/loaders/nvidia.py`
   - `data/loaders/fed_data.py`

### Step 2: Create Data Service Layer
1. **Create `data/services/data_service.py`**:
   - Central service for all data access
   - Maps view requirements to data sources
   - Validates data completeness
   - Handles errors uniformly

2. **Data mapping structure**:
   ```python
   DATA_MAPPING = {
       "historical_trends": {
           "milestones": ("ai_index", "milestones"),
           "convergence_factors": ("academic", "convergence_analysis"),
       },
       "roi_analysis": {
           "roi_data": ("mckinsey", "roi_metrics"),
           "payback_data": ("mckinsey", "payback_analysis"),
       },
       # ... etc
   }
   ```

### Step 3: Connect Views to Real Data
1. **Replace TODOs in each view**:
   - Remove empty DataFrame assignments
   - Call data service with proper error handling
   - Implement visible failure on missing data

2. **Example transformation**:
   ```python
   # Before:
   # TODO: Load ROI data from actual data source
   roi_data = pd.DataFrame()
   
   # After:
   roi_data = data_service.get_required_data("roi_analysis", "roi_data")
   if roi_data.empty:
       st.error("❌ Critical Error: ROI data not available. Please ensure data sources are properly configured.")
       st.stop()
   ```

### Step 4: Implement Strict Data Validation
1. **Update `views/base.py`**:
   - Enhance `validate_data()` to be more strict
   - Add schema validation using Pydantic models
   - Fail visibly with detailed error messages

2. **Create validation utilities**:
   - Schema validators for each data type
   - Completeness checks
   - Data quality metrics

### Step 5: Update app.py for Data Enforcement
1. **Modify data loading**:
   - Remove any try-catch that hides failures
   - Add startup data validation
   - Show clear error page if critical data missing

2. **Add data status dashboard**:
   - Show which data sources are available
   - Display data freshness
   - Provide troubleshooting guidance

### Step 6: Remove All Remaining TODOs
1. **Search and eliminate**:
   - All TODO comments in production code
   - Replace with proper implementations
   - Document any deferred work in separate tracking

### Step 7: Enforce CLAUDE.md Compliance
1. **Run compliance checks**:
   - No interface{} or any{} (Python equivalent: no untyped data)
   - No sleep or busy waits
   - No placeholder functions
   - All code must be production-ready

2. **Add pre-commit hooks**:
   - TODO detection
   - Fallback data detection
   - Type checking enforcement

## Success Criteria
- ✅ Zero TODO comments in production code
- ✅ No fallback or sample data anywhere
- ✅ All views fail visibly when data is missing
- ✅ All data validated against Pydantic models
- ✅ Clear error messages guide users to resolution
- ✅ All linters and tests pass

## Testing Strategy
1. **Unit tests**: Verify each component fails appropriately without data
2. **Integration tests**: Test data flow from sources to views
3. **Error scenario tests**: Ensure proper error messages and handling
4. **No mock data in tests**: Use real data or proper test fixtures

## Rollback Plan
- Git branching strategy for safe implementation
- Feature flags for gradual rollout
- Backup of current working state

## Timeline Estimate
- Step 1-2: 2 days (Remove fallbacks, create service layer)
- Step 3-4: 3 days (Connect views, implement validation)
- Step 5-6: 2 days (Update app.py, remove TODOs)
- Step 7: 1 day (Compliance enforcement)
- Testing: 2 days

**Total: ~10 days**