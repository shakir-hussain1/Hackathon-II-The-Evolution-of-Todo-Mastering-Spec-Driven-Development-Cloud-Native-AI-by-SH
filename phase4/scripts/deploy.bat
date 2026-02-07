@echo off
REM Deploy Todo App to Minikube using Helm on Windows

echo ========================================
echo Deploying Todo App to Minikube
echo ========================================

REM Navigate to project root
cd /d "%~dp0..\.."

REM Configuration
set RELEASE_NAME=todo-app
set NAMESPACE=default
set HELM_CHART_PATH=phase4\helm\todo-app

REM Check if Minikube is running
echo.
echo Checking Minikube status...
minikube status >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Minikube is not running. Please start it with 'minikube start'
    exit /b 1
)
echo Minikube is running

REM Check for required secrets
echo.
echo Checking for required environment variables...

REM Load secrets from .env file if it exists
if exist "phase4\.env" (
    echo Loading secrets from phase4\.env
    for /f "usebackq tokens=*" %%a in ("phase4\.env") do set %%a
) else if exist "phase3\backend\.env" (
    echo Loading secrets from phase3\backend\.env
    for /f "usebackq tokens=*" %%a in ("phase3\backend\.env") do set %%a
)

REM Validate secrets
if "%OPENAI_API_KEY%"=="" (
    echo Error: OPENAI_API_KEY not set
    echo Please set it in phase4\.env or as an environment variable
    exit /b 1
)

if "%JWT_SECRET%"=="" (
    echo Warning: JWT_SECRET not set. Please set it manually
    set /p JWT_SECRET="Enter JWT_SECRET (or press Enter to generate random): "
    if "!JWT_SECRET!"=="" (
        echo Generating random JWT_SECRET...
        REM Generate random string - simplified version
        set JWT_SECRET=%RANDOM%%RANDOM%%RANDOM%%RANDOM%
    )
)

echo Required secrets validated

REM Build Docker images
echo.
echo Building Docker images...
call "%~dp0build-images.bat"
if %errorlevel% neq 0 exit /b 1

REM Check if release already exists
echo.
echo Checking for existing deployment...
helm list -n %NAMESPACE% | findstr "^%RELEASE_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo Existing deployment found. Upgrading...
    set HELM_COMMAND=upgrade
) else (
    echo No existing deployment. Installing...
    set HELM_COMMAND=install
)

REM Deploy with Helm
echo.
echo Deploying with Helm...
helm %HELM_COMMAND% %RELEASE_NAME% %HELM_CHART_PATH% ^
    --namespace %NAMESPACE% ^
    --set secrets.openaiApiKey="%OPENAI_API_KEY%" ^
    --set secrets.jwtSecret="%JWT_SECRET%" ^
    --wait ^
    --timeout 5m

if %errorlevel% neq 0 (
    echo Deployment failed
    exit /b 1
)
echo Deployment successful!

REM Wait for pods to be ready
echo.
echo Waiting for pods to be ready...
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=%RELEASE_NAME% -n %NAMESPACE% --timeout=300s

REM Display deployment status
echo.
echo ========================================
echo Deployment Status
echo ========================================

echo.
echo Pods:
kubectl get pods -n %NAMESPACE% -l app.kubernetes.io/instance=%RELEASE_NAME%

echo.
echo Services:
kubectl get services -n %NAMESPACE% -l app.kubernetes.io/instance=%RELEASE_NAME%

echo.
echo Ingress:
kubectl get ingress -n %NAMESPACE% -l app.kubernetes.io/instance=%RELEASE_NAME% 2>nul

REM Get access URLs
echo.
echo ========================================
echo Access Information
echo ========================================

echo.
echo Frontend:
echo Run: minikube service %RELEASE_NAME%-frontend --url

echo.
echo Backend API:
echo Port-forward command:
echo kubectl port-forward -n %NAMESPACE% svc/%RELEASE_NAME%-backend 8000:8000
echo.
echo Then access:
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs

echo.
echo ========================================
echo Deployment completed successfully!
echo ========================================

echo.
echo Useful commands:
echo View logs (backend): kubectl logs -n %NAMESPACE% -l app.kubernetes.io/component=backend -f
echo View logs (frontend): kubectl logs -n %NAMESPACE% -l app.kubernetes.io/component=frontend -f
echo Uninstall: helm uninstall %RELEASE_NAME% -n %NAMESPACE%

pause
