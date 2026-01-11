@echo off
cls
echo ============================================
echo    STARTING PHASE 2 TODO FRONTEND
echo ============================================
echo.
echo Increasing Node.js memory to 4GB...
set NODE_OPTIONS=--max-old-space-size=4096

echo Changing to frontend directory...
cd /d E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend

echo.
echo Starting Next.js development server...
echo This may take 30-60 seconds on first run...
echo.
npm run dev

pause
