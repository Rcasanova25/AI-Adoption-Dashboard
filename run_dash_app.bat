@echo off
echo ========================================
echo Running AI Adoption Dashboard (Dash)
echo ========================================
echo.

REM Set environment to suppress Streamlit warnings
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

REM Run the Dash app
python run_dash_app.py

pause