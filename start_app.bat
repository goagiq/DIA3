@echo off
echo 🚀 Starting DIA3 Application...
echo ==================================================

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo.
    echo To create the virtual environment:
    echo 1. python -m venv .venv
    echo 2. .venv\Scripts\activate
    echo 3. pip install -r requirements_core.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Run the application
echo 🚀 Starting main application...
echo ==================================================
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo ❌ Application exited with error code %errorlevel%
    pause
)
