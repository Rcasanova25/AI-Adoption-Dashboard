@echo off
echo ========================================
echo Restarting Dash App with Clean Cache
echo ========================================
echo.

REM Remove Python cache
echo Removing Python cache...
rmdir /s /q callbacks\__pycache__ 2>nul
rmdir /s /q data\__pycache__ 2>nul
rmdir /s /q data\loaders\__pycache__ 2>nul
rmdir /s /q __pycache__ 2>nul

REM Set environment to suppress Streamlit warnings
set STREAMLIT_SERVER_HEADLESS=true
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

REM Kill any existing Python processes running app_dash.py
echo Stopping existing dashboard processes...
taskkill /f /im python.exe /fi "WINDOWTITLE eq app_dash*" 2>nul

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Run the Dash app
echo Starting fresh dashboard instance...
python app_dash.py

pause