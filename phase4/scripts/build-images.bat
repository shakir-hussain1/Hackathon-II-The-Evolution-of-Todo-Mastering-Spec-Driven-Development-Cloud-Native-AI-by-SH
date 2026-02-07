@echo off
REM Build Docker images for Todo App (Frontend + Backend) on Windows
REM This script builds images and loads them into Minikube

echo ========================================
echo Building Todo App Docker Images
echo ========================================

REM Navigate to project root
cd /d "%~dp0..\.."

REM Check if Minikube is running
echo.
echo Checking Minikube status...
minikube status >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Minikube is not running. Please start it with 'minikube start'
    exit /b 1
)

REM Use Minikube's Docker daemon
echo.
echo Configuring Docker to use Minikube's daemon...
@for /f "tokens=*" %%i in ('minikube docker-env --shell cmd') do @%%i

REM Build Backend Image
echo.
echo Building Backend Image (FastAPI)...
docker build -f phase4/docker/backend.Dockerfile -t todo-backend:latest .
if %errorlevel% neq 0 (
    echo Backend image build failed
    exit /b 1
)
echo Backend image built successfully

REM Build Frontend Image
echo.
echo Building Frontend Image (Next.js)...
docker build -f phase4/docker/frontend.Dockerfile -t todo-frontend:latest .
if %errorlevel% neq 0 (
    echo Frontend image build failed
    exit /b 1
)
echo Frontend image built successfully

REM List built images
echo.
echo Built images:
docker images | findstr "todo-"

echo.
echo ========================================
echo Image build completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Deploy to Minikube: phase4\scripts\deploy.bat
echo 2. Or manually install with Helm: cd phase4\helm ^&^& helm install todo-app .\todo-app

pause
