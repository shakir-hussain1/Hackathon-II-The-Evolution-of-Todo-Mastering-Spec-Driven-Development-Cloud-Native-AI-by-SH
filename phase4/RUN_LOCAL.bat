@echo off
REM Local Deployment Script for Todo App on Kubernetes
REM Run this from Windows Command Prompt or PowerShell

echo ========================================
echo Todo App - Local Kubernetes Deployment
echo ========================================
echo.

echo Step 1: Checking Docker Desktop...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo OK: Docker Desktop is running
echo.

echo Step 2: Starting Minikube cluster...
wsl -e bash -c "minikube status | grep -q 'host: Running' && echo 'Minikube already running' || minikube start --driver=docker --cpus=4 --memory=8192"
echo.

echo Step 3: Checking environment variables...
if not exist "phase4\.env" (
    echo Creating .env file...
    copy phase4\.env.example phase4\.env
    echo.
    echo IMPORTANT: Please edit phase4\.env and add:
    echo   - OPENAI_API_KEY=your-key-here
    echo   - JWT_SECRET=your-secret-here
    echo.
    notepad phase4\.env
    echo.
    echo Press any key after saving the file...
    pause
)
echo.

echo Step 4: Building Docker images...
echo This may take 5-10 minutes...
wsl -e bash -c "cd /mnt/e/Hackathon-II-The-Evolution-of-Todo/phase4 && eval \$(minikube docker-env) && docker build -t todo-backend:latest -f docker/backend.Dockerfile ../phase3/backend/ && docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../phase3/frontend/"
echo.

echo Step 5: Creating Kubernetes secrets...
wsl -e bash -c "cd /mnt/e/Hackathon-II-The-Evolution-of-Todo/phase4 && kubectl create secret generic todo-app-secrets --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -"
echo.

echo Step 6: Deploying with Helm...
wsl -e bash -c "cd /mnt/e/Hackathon-II-The-Evolution-of-Todo/phase4 && helm upgrade --install todo-app ./helm/todo-app --set backend.image.tag=latest --set frontend.image.tag=latest --set backend.image.pullPolicy=Never --set frontend.image.pullPolicy=Never"
echo.

echo Step 7: Waiting for pods to be ready...
wsl -e bash -c "kubectl wait --for=condition=Ready pods --all --timeout=300s"
echo.

echo Step 8: Getting application URL...
echo.
echo ========================================
echo DEPLOYMENT SUCCESSFUL!
echo ========================================
echo.
echo Your Todo App is running!
echo.
wsl -e bash -c "minikube service todo-app-frontend --url"
echo.
echo Copy the URL above and open it in your browser.
echo.
echo To access backend API docs:
echo   wsl -e bash -c "kubectl port-forward svc/todo-app-backend 8000:8000"
echo   Then open: http://localhost:8000/docs
echo.
echo To view logs:
echo   wsl -e bash -c "kubectl logs -f deployment/todo-app-backend"
echo   wsl -e bash -c "kubectl logs -f deployment/todo-app-frontend"
echo.
pause
