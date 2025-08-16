@echo off
echo Starting clean terminal session...
echo.

cd /d "D:\AI\DIA3"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Python version:
python --version

echo.
echo Terminal is ready! You can now run commands without control character issues.
echo.
cmd /k
