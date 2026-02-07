# Quickstart Guide: Kubernetes Deployment

**Feature**: Local Kubernetes Deployment
**Date**: 2026-01-30
**Target**: 5-minute experienced users, 30-minute learners

## 5-Minute Quick Start (Experienced Users)

### Prerequisites
- Docker Desktop installed and running
- Minikube installed
- kubectl installed
- Helm 3 installed
- Phase III application in `../phase3/`

### Steps

```bash
# 1. Start Minikube
minikube start --memory=6144 --cpus=2 --driver=docker

# 2. Build and load images
docker build -t todo-frontend:v1.0.0 -f docker/frontend.Dockerfile ../phase3/frontend
docker build -t todo-backend:v1.0.0 -f docker/backend.Dockerfile ../phase3/backend
minikube image load todo-frontend:v1.0.0
minikube image load todo-backend:v1.0.0

# 3. Install Helm chart
helm install todo-app ./helm/todo-app \
  --set backend.secrets.jwtSecret=your-secret \
  --set backend.secrets.openaiApiKey=sk-your-key

# 4. Verify deployment
kubectl get pods
kubectl get services

# 5. Access application
minikube service todo-frontend-service --url
# Open URL in browser
```

## 30-Minute Guided Tutorial (Learners)

### Step 1: Install Prerequisites (10 minutes)

**Docker Desktop:**
- Download from https://docker.com/products/docker-desktop
- Install and start Docker Desktop
- Verify: `docker --version`

**Minikube:**
```bash
# Windows (PowerShell as Admin)
choco install minikube

# macOS
brew install minikube

# Verify
minikube version
```

**kubectl:**
```bash
# Included with Docker Desktop on Windows/Mac
kubectl version --client
```

**Helm:**
```bash
# Windows
choco install kubernetes-helm

# macOS
brew install helm

# Verify
helm version
```

### Step 2: Start Minikube (5 minutes)

```bash
# Start Minikube with appropriate resources
minikube start --memory=6144 --cpus=2 --driver=docker

# Verify cluster is running
minikube status
kubectl cluster-info
```

Expected output:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
```

### Step 3: Build Docker Images (10 minutes)

```bash
# Navigate to phase4
cd phase4

# Build frontend image
docker build -t todo-frontend:v1.0.0 \
  -f docker/frontend.Dockerfile \
  ../phase3/frontend

# Build backend image
docker build -t todo-backend:v1.0.0 \
  -f docker/backend.Dockerfile \
  ../phase3/backend

# Load images into Minikube
minikube image load todo-frontend:v1.0.0
minikube image load todo-backend:v1.0.0

# Verify images loaded
minikube image ls | grep todo
```

### Step 4: Deploy with Helm (3 minutes)

```bash
# Install Helm chart
helm install todo-app ./helm/todo-app \
  --set backend.secrets.jwtSecret=dev-secret-123 \
  --set backend.secrets.openaiApiKey=sk-test-key

# Watch pods start
kubectl get pods -w

# Wait until all pods show Running (press Ctrl+C to stop watching)
```

### Step 5: Verify and Access (2 minutes)

```bash
# Check all resources
kubectl get all

# Get frontend service URL
minikube service todo-frontend-service --url

# Open the URL in your browser
# Example: http://192.168.49.2:30080
```

## Troubleshooting

### Pods not starting
```bash
# Check pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>
```

### Images not found
```bash
# Verify images in Minikube
minikube image ls | grep todo

# Reload if needed
minikube image load todo-frontend:v1.0.0
```

### Service not accessible
```bash
# Get service URL
minikube service todo-frontend-service --url

# Check if Minikube tunnel is needed
minikube tunnel  # Run in separate terminal
```

## Cleanup

```bash
# Uninstall Helm release
helm uninstall todo-app

# Stop Minikube
minikube stop

# Delete cluster (optional)
minikube delete
```

## Next Steps

- Read `ARCHITECTURE_OVERVIEW.md` for system design
- Review `research.md` for technical decisions
- Run `/sp.tasks` to see implementation task breakdown
- Explore AI-assisted operations with kubectl-ai and Kagent
