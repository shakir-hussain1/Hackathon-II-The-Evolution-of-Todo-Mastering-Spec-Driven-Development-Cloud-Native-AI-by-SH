# Local Deployment Guide - Todo App on Kubernetes

## Pre-requisites Check

Run these commands in WSL2 Ubuntu terminal:

```bash
# Check all tools
docker --version          # Should show 24+
minikube version         # Should show 1.32+
kubectl version --client # Should show 1.28+
helm version            # Should show 3.13+
```

## Step-by-Step Deployment

### Step 1: Start Docker Desktop
- Open Docker Desktop on Windows
- Ensure it's running (whale icon in system tray)
- Wait until "Docker Desktop is running" appears

### Step 2: Start Minikube Cluster

```bash
# Open WSL2 Ubuntu terminal
cd /mnt/e/Hackathon-II-The-Evolution-of-Todo

# Start Minikube with enough resources
minikube start --driver=docker --cpus=4 --memory=8192 --disk-size=20g

# Verify cluster is running
minikube status
kubectl get nodes
```

### Step 3: Configure Environment Variables

```bash
cd phase4

# Copy example env file
cp .env.example .env

# Edit .env file (use nano or vim)
nano .env
```

Add these values:
```
OPENAI_API_KEY=your-openai-api-key-here
JWT_SECRET=your-secret-key-here
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 4: Build Docker Images in Minikube

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest -f docker/backend.Dockerfile ../phase3/backend/

# Build frontend image
docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../phase3/frontend/

# Verify images
docker images | grep todo
```

### Step 5: Create Kubernetes Secrets

```bash
# Create secret from .env file
kubectl create secret generic todo-app-secrets \
  --from-env-file=.env \
  --dry-run=client -o yaml | kubectl apply -f -

# Verify secret created
kubectl get secrets
```

### Step 6: Deploy with Helm

```bash
# Install the Helm chart
helm install todo-app ./helm/todo-app \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --set backend.image.pullPolicy=Never \
  --set frontend.image.pullPolicy=Never

# Watch deployment progress
kubectl get pods -w
```

Wait until all pods show `Running` status (Press Ctrl+C to stop watching)

### Step 7: Access the Application

```bash
# Get the frontend URL
minikube service todo-app-frontend --url
```

This will output something like: `http://127.0.0.1:xxxxx`

Open this URL in your browser!

### Step 8: Access Backend API (Optional)

```bash
# In a new terminal, port-forward backend
kubectl port-forward svc/todo-app-backend 8000:8000

# Access API docs at:
# http://localhost:8000/docs
```

## Quick Commands Reference

```bash
# Check pod status
kubectl get pods

# Check services
kubectl get svc

# View logs
kubectl logs -f <pod-name>

# Restart deployment
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend

# Delete and redeploy
helm uninstall todo-app
# Then repeat Step 6
```

## Troubleshooting

### Pods stuck in ImagePullBackOff
```bash
# Make sure you're using Minikube's Docker
eval $(minikube docker-env)
# Rebuild images and set pullPolicy=Never
```

### Frontend can't reach backend
```bash
# Port forward backend manually
kubectl port-forward svc/todo-app-backend 8000:8000
# Update frontend env to use localhost:8000
```

### Out of memory errors
```bash
# Delete and restart with more memory
minikube delete
minikube start --cpus=4 --memory=10240
```

## Cleanup

```bash
# Uninstall app
helm uninstall todo-app

# Stop Minikube
minikube stop

# Delete cluster (careful!)
minikube delete
```

## Next Steps

1. Test all features in the app
2. Check logs for any errors
3. Try creating, updating, deleting todos
4. Test the AI chat feature

Enjoy your locally running Todo App on Kubernetes! 🎉
