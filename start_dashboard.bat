@echo off
REM Startup script for MLOPS Analytics Dashboard on Windows
REM This script will install dependencies and start the web dashboard

echo ================================================
echo   MLOPS Analytics Dashboard - Windows Launcher
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed.
)

echo.
echo [2/3] Checking data files...
if not exist customer_shopping_data.csv (
    echo Error: customer_shopping_data.csv not found!
    echo Please ensure the data file is in the current directory.
    pause
    exit /b 1
)

if not exist Region_detail_table.csv (
    echo Error: Region_detail_table.csv not found!
    echo Please ensure the data file is in the current directory.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting dashboard...
echo.
echo ================================================
echo   Dashboard will be available at:
echo   http://localhost:8000
echo.
echo   Press CTRL+C to stop the server
echo ================================================
echo.

python run_dashboard.py

pause