@echo off
REM Start Phase 2 Backend Server
echo ========================================
echo Starting Phase 2 Todo Backend Server...
echo ========================================
echo.
echo Backend will run on: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
cd /d "E:\Hackathon-II-The-Evolution-of-Todo\phase2\backend"
call venv\Scripts\activate.bat
python main.py
pause
