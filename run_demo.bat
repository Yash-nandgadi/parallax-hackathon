@echo off
cd /d %~dp0
start cmd /k "venv\Scripts\python.exe app.py"
timeout /t 2 /nobreak > nul
start cmd /k "venv\Scripts\streamlit.exe run dashboard.py"