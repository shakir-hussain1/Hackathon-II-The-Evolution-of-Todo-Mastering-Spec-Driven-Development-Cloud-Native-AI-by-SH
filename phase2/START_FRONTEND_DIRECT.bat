@echo off
REM Direct start of frontend with memory fix
echo ========================================
echo Starting Frontend (Direct Mode - 4GB Memory)
echo ========================================
echo.
echo This bypasses npm scripts and runs Next.js directly
echo Frontend will run on: http://localhost:3000
echo.

cd /d "E:\Hackathon-II-The-Evolution-of-Todo\phase2\frontend"

REM Set 4GB memory limit
set NODE_OPTIONS=--max-old-space-size=4096

REM Run Next.js directly without Turbopack
echo Starting Next.js with Webpack bundler...
echo.
npx next dev --turbo=false

pause
