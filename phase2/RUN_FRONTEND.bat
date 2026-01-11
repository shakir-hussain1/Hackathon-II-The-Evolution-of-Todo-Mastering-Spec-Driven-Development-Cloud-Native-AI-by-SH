@echo off
REM Start Phase 2 Frontend Server with 4GB Memory
echo ========================================
echo Starting Phase 2 Todo Frontend Server...
echo ========================================
echo.
echo Frontend will run on: http://localhost:3000
echo Make sure Backend is running on: http://localhost:8000
echo.
echo Setting Node.js memory to 4GB to prevent crashes...
echo.

cd /d "E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend"

REM Set Node.js memory limit to 4GB
set NODE_OPTIONS=--max-old-space-size=4096

REM Start Next.js development server with Webpack (not Turbopack)
npm run dev

pause
