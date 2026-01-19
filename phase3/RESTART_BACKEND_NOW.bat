@echo off
echo ========================================
echo RESTARTING BACKEND WITH FIXES
echo ========================================
echo.

cd backend

echo Clearing Python cache...
python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; print('Cache cleared')"

echo.
echo Starting backend server...
echo Backend URL: http://127.0.0.1:8000
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop
echo.

python -m uvicorn src.main:app --reload --port 8000
