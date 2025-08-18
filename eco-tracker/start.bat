@echo off
echo Starting EcoTracker Carbon Footprint Tracker...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Create necessary directories
if not exist "data" mkdir data
if not exist "models" mkdir models
if not exist "exports" mkdir exports

:: Train models if they don't exist
if not exist "models\xgboost_model.pkl" (
    echo Training AI models...
    python src\train_model.py
)

:: Start the application
echo Starting EcoTracker...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
python -m streamlit run app.py

pause
