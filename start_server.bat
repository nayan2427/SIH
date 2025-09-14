@echo off
echo Starting InternshipHub Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create necessary directories
if not exist "static" mkdir static
if not exist "templates" mkdir templates
if not exist "data" mkdir data

REM Start the Flask application
echo.
echo Starting Flask application...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
