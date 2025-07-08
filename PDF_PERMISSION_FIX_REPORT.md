# PDF Permission Denied Error Fix Report

## Root Cause Analysis

The error `ERROR:data.extractors.pdf_extractor:Error finding pages with keyword 'adoption rate': [Errno 13] Permission denied: 'AI adoption resources'` was caused by two issues:

### 1. Case Sensitivity Mismatch
- **Actual directory name**: `AI adoption resources` (lowercase 'a')
- **Settings configuration**: `AI Adoption Resources` (capital 'A')
- **Location**: `/config/settings.py` line 26

### 2. Missing PDF Filename in IMFLoader
- **Issue**: The IMFLoader was initializing with just `settings.get_resources_path()` without appending a PDF filename
- **Effect**: This caused the PDFExtractor to try opening the directory "AI adoption resources" as if it were a file
- **Location**: `/data/loaders/academic.py` line 1007

### 3. Incorrect Subdirectory Reference
- **Issue**: AcademicPapersLoader referenced non-existent `"AI Adoption Resources 4"` subdirectory
- **Actual subdirectory**: `"AI dashboard resources 1"`
- **Location**: `/data/loaders/academic.py` line 26

## Fixes Applied

### 1. Fixed Case Sensitivity in settings.py
```python
# OLD:
str(BASE_DIR / "AI Adoption Resources")  # FIXED: Capital "A" in "Adoption"

# NEW:
str(BASE_DIR / "AI adoption resources")  # FIXED: lowercase 'a' in "adoption"
```

### 2. Fixed IMFLoader to Include PDF Filename
```python
# OLD:
file_path = settings.get_resources_path()

# NEW:
file_path = settings.get_resources_path() / "AI dashboard resources 1/wpiea2024231-print-pdf.pdf"
```

### 3. Fixed AcademicPapersLoader Subdirectory Reference
```python
# OLD:
papers_dir = settings.get_resources_path() / "AI Adoption Resources 4"

# NEW:
papers_dir = settings.get_resources_path() / "AI dashboard resources 1"
```

## Verification

The fixes ensure that:
1. The resources path matches the actual directory name on the file system
2. All PDF extractors are initialized with actual PDF file paths, not directory paths
3. All referenced subdirectories actually exist

## Prevention

To prevent similar issues in the future:
1. Always verify that file paths point to actual files, not directories
2. Use consistent casing for directory names across the codebase
3. Validate that referenced paths exist before passing them to file operations
4. Consider adding path validation in the PDFExtractor constructor to provide clearer error messages

## Files Modified
- `/config/settings.py`
- `/data/loaders/academic.py`