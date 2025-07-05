# Streamlit Deployment Fix

## Issue Fixed

The Streamlit deployment was failing due to a dependency conflict:

- **causalnex>=0.12.1** requires `pandas>=1.0,<2.0`
- Our app requires `pandas>=2.0.0`
- These requirements are incompatible

## Solution Applied

1. **Removed unused dependencies** from `requirements.txt`:
   - `causalnex>=0.12.1` - Not used in the codebase
   - `kedro>=0.19.14` - Not used in the codebase
   - `pytest>=6.0.0` - Already in requirements-dev.txt
   - `black>=22.0.0` - Already in requirements-dev.txt
   - `flake8>=4.0.0` - Already in requirements-dev.txt

2. **Kept only production dependencies** in `requirements.txt`

## Verification

- Confirmed `causalnex` is not imported anywhere in the code
- Confirmed `kedro` is only mentioned in Feedback.md, not used in code
- Development tools are properly placed in `requirements-dev.txt`

## Next Steps

1. Commit and push the updated requirements.txt
2. Streamlit will automatically redeploy with the fixed dependencies
3. The deployment should now succeed

## Additional Notes

The deployment uses Python 3.13.5, which is very recent. All remaining dependencies in requirements.txt are compatible with this Python version.