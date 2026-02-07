@echo off
echo ============================================================
echo Starting Phase 3 Backend
echo ============================================================
echo.

REM Set environment variable to prevent bytecode caching issues
set PYTHONDONTWRITEBYTECODE=1

echo Testing configuration first...
python test_simple.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Configuration test failed!
    pause
    exit /b 1
)

echo.
echo Configuration OK! Starting server...
echo.
echo Backend will be available at: http://127.0.0.1:8000
echo API docs at: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

python -m uvicorn src.main:app --reload --port 8000
