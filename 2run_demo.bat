@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ====================================================
echo STEP 1: Checking Python Installation...
echo ====================================================
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python and check "Add Python to PATH" during setup.
    pause
    exit /b
)

echo.
echo ====================================================
echo STEP 2: Creating Virtual Environment (venv)...
echo ====================================================
if not exist "venv" (
    echo Creating missing virtual environment folder...
    python -m venv venv
) else (
    echo Virtual environment folder already exists.
)

echo.
echo ====================================================
echo STEP 3: Upgrading Pip and Installing Dependencies...
echo ====================================================
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1

if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Installing default requirements...
    pip install streamlit fastapi uvicorn requests pandas
)

echo.
echo ====================================================
echo STEP 4: Launching Backend Server (app.py)...
echo ====================================================
start cmd /k ""%~dp0venv\Scripts\python.exe" "%~dp0app.py""

echo Waiting 5 seconds for backend server to open on port 8000...
timeout /t 5 /nobreak > nul

echo.
echo ====================================================
echo STEP 5: Launching Streamlit Dashboard (dashboard.py)...
echo ====================================================
start cmd /k ""%~dp0venv\Scripts\python.exe" -m streamlit run "%~dp0dashboard.py""

echo Setup complete! Both servers are starting up.
pause