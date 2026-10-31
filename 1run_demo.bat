@echo off
cd /d "%~dp0"

echo ====================================================
echo Checking and installing required dependencies...
echo ====================================================
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    pip install streamlit fastapi uvicorn
)

echo.
echo ====================================================
echo Starting Backend Server (app.py)...
echo ====================================================
start cmd /k "python app.py"

echo Waiting 4 seconds for the backend to initialize...
timeout /t 4 /nobreak > nul

echo.
echo ====================================================
echo Starting Streamlit Dashboard (dashboard.py)...
echo ====================================================
start cmd /k "python -m streamlit run dashboard.py"

echo Setup complete! You can close this window.
pause