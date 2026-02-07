# Phase 4: Kubernetes Deployment Guide

Complete guide for deploying the Phase 3 Todo Chatbot application to Minikube using Helm charts.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Detailed Installation](#detailed-installation)
- [Configuration](#configuration)
- [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [Cleanup](#cleanup)

## Overview

This deployment configuration packages the Phase 3 Todo application (FastAPI backend + Next.js frontend) into a production-ready Kubernetes deployment using Helm charts optimized for Minikube.

### What's Included

- **Helm Chart**: Complete chart with templates for all Kubernetes resources
- **Docker Images**: Multi-stage Dockerfiles for optimized builds
- **Deployment Scripts**: Automated deployment and verification scripts
- **Documentation**: Comprehensive guides and troubleshooting tips

### Key Features

- **High Availability**: 2 replicas each for frontend and backend
- **Health Checks**: Liveness and readiness probes for all services
- **Persistent Storage**: SQLite database persisted across pod restarts
- **Resource Management**: CPU and memory limits to prevent resource exhaustion
- **Secret Management**: Secure handling of API keys and JWT secrets

## Prerequisites

### Required Software

1. **Minikube** (v1.30.0 or later)
   ```bash
   # Install Minikube
   # macOS
   brew install minikube

   # Windows (using Chocolatey)
   choco install minikube

   # Linux
   curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
   sudo install minikube-linux-amd64 /usr/local/bin/minikube
   ```

2. **kubectl** (v1.27.0 or later)
   ```bash
   # Install kubectl
   # macOS
   brew install kubectl

   # Windows (using Chocolatey)
   choco install kubernetes-cli

   # Linux
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   sudo install kubectl /usr/local/bin/kubectl
   ```

3. **Helm** (v3.12.0 or later)
   ```bash
   # Install Helm
   # macOS
   brew install helm

   # Windows (using Chocolatey)
   choco install kubernetes-helm

   # Linux
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

4. **Docker** (v20.10.0 or later)
   - Docker Desktop for macOS/Windows
   - Docker Engine for Linux

### System Requirements

- **CPU**: 2 cores minimum, 4 cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 20GB free space

### Environment Setup

1. Start Minikube with recommended resources:
   ```bash
   minikube start --cpus=4 --memory=8192 --disk-size=20g
   ```

2. Verify Minikube is running:
   ```bash
   minikube status
   ```

3. Enable Ingress addon (optional):
   ```bash
   minikube addons enable ingress
   ```

## Quick Start

### Automated Deployment

The fastest way to deploy is using the automated deployment script:

**Linux/macOS:**
```bash
# Navigate to phase4
cd phase4

# Make scripts executable
chmod +x scripts/*.sh

# Deploy (includes building images)
./scripts/deploy.sh
```

**Windows:**
```cmd
REM Navigate to phase4
cd phase4

REM Deploy
scripts\deploy.bat
```

### Manual Deployment

If you prefer manual control:

1. **Set up secrets**:
   ```bash
   # Create .env file in phase4 directory
   cat > phase4/.env << EOF
   OPENAI_API_KEY=your-openai-api-key-here
   JWT_SECRET=your-jwt-secret-here
   EOF
   ```

2. **Build Docker images**:
   ```bash
   # Linux/macOS
   ./scripts/build-images.sh

   # Windows
   scripts\build-images.bat
   ```

3. **Install with Helm**:
   ```bash
   # Source environment variables
   source phase4/.env

   # Install the chart
   helm install todo-app ./helm/todo-app \
     --set secrets.openaiApiKey="$OPENAI_API_KEY" \
     --set secrets.jwtSecret="$JWT_SECRET" \
     --wait
   ```

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Minikube Cluster                      │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   Ingress                         │   │
│  │          (todo-app.local)                        │   │
│  └────────────┬──────────────────┬──────────────────┘   │
│               │                  │                        │
│       /api/* │                  │ /*                     │
│               ▼                  ▼                        │
│  ┌─────────────────┐   ┌─────────────────┐              │
│  │  Backend Svc    │   │  Frontend Svc   │              │
│  │  (ClusterIP)    │   │  (NodePort)     │              │
│  │  Port: 8000     │   │  Port: 3000     │              │
│  └────────┬────────┘   └────────┬────────┘              │
│           │                     │                        │
│  ┌────────▼────────┐   ┌────────▼────────┐              │
│  │  Backend Pod    │   │  Frontend Pod   │              │
│  │  (2 replicas)   │   │  (2 replicas)   │              │
│  │  FastAPI        │   │  Next.js        │              │
│  │  Port: 7860     │   │  Port: 3000     │              │
│  └────────┬────────┘   └─────────────────┘              │
│           │                                              │
│  ┌────────▼────────┐                                     │
│  │  PVC (1Gi)      │                                     │
│  │  SQLite DB      │                                     │
│  └─────────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

### Resource Specifications

#### Backend (FastAPI)
- **Replicas**: 2
- **Image**: `todo-backend:latest`
- **Port**: 7860 (container), 8000 (service)
- **Resources**:
  - Requests: 256Mi RAM, 250m CPU
  - Limits: 512Mi RAM, 500m CPU
- **Storage**: 1Gi PersistentVolume for SQLite database
- **Health Checks**:
  - Liveness: `/health` endpoint, 30s initial delay
  - Readiness: `/health` endpoint, 10s initial delay

#### Frontend (Next.js)
- **Replicas**: 2
- **Image**: `todo-frontend:latest`
- **Port**: 3000
- **Service Type**: NodePort (30080)
- **Resources**:
  - Requests: 128Mi RAM, 100m CPU
  - Limits: 256Mi RAM, 250m CPU
- **Health Checks**:
  - Liveness: `/` endpoint, 30s initial delay
  - Readiness: `/` endpoint, 10s initial delay

### Networking

- **Backend Service**: ClusterIP (internal only)
  - Accessible within cluster at `todo-app-backend:8000`
  - External access via `kubectl port-forward`

- **Frontend Service**: NodePort
  - Accessible externally via `minikube service` command
  - NodePort: 30080

- **Ingress** (optional):
  - Host: `todo-app.local`
  - Paths:
    - `/api/*` → Backend
    - `/*` → Frontend

## Detailed Installation

### Step 1: Prepare Environment

1. **Start Minikube**:
   ```bash
   minikube start --cpus=4 --memory=8192
   ```

2. **Verify cluster**:
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

3. **Configure Docker environment** (for building images):
   ```bash
   eval $(minikube docker-env)
   ```

### Step 2: Configure Secrets

Create a `.env` file in the `phase4` directory:

```bash
# phase4/.env
OPENAI_API_KEY=sk-your-actual-openai-api-key
JWT_SECRET=your-secure-random-jwt-secret-at-least-32-chars
```

**Generate a secure JWT secret**:
```bash
# Linux/macOS
openssl rand -hex 32

# Or use any long random string
```

### Step 3: Build Docker Images

```bash
# Navigate to project root
cd /path/to/Hackathon-II-The-Evolution-of-Todo

# Make build script executable (Linux/macOS)
chmod +x phase4/scripts/build-images.sh

# Build images
./phase4/scripts/build-images.sh

# Verify images
docker images | grep todo-
```

**Expected output**:
```
todo-backend     latest    abc123def456   2 minutes ago   245MB
todo-frontend    latest    def456abc123   1 minute ago    178MB
```

### Step 4: Deploy with Helm

```bash
# Load environment variables
source phase4/.env

# Deploy
helm install todo-app ./phase4/helm/todo-app \
  --set secrets.openaiApiKey="$OPENAI_API_KEY" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  --wait \
  --timeout 5m
```

**Monitor deployment**:
```bash
# Watch pods
kubectl get pods -w

# Check deployment status
kubectl rollout status deployment/todo-app-backend
kubectl rollout status deployment/todo-app-frontend
```

### Step 5: Verify Deployment

Run the verification script:

```bash
./phase4/scripts/verify.sh
```

Or manually verify:

```bash
# Check all resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Check pods are running
kubectl get pods -l app.kubernetes.io/instance=todo-app

# Check services
kubectl get services -l app.kubernetes.io/instance=todo-app

# Check PVC
kubectl get pvc

# Test backend health
kubectl exec -it deployment/todo-app-backend -- wget -q -O- http://localhost:7860/health
```

## Configuration

### Helm Values

The deployment is configured via `values.yaml`. Key configuration options:

#### Backend Configuration

```yaml
backend:
  replicaCount: 2  # Number of backend replicas

  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent

  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"

  env:
    - name: ENVIRONMENT
      value: "production"
    - name: CORS_ORIGINS
      value: "http://localhost:3000,http://localhost:30080"
```

#### Frontend Configuration

```yaml
frontend:
  replicaCount: 2  # Number of frontend replicas

  image:
    repository: todo-frontend
    tag: latest

  service:
    type: NodePort
    nodePort: 30080  # External access port

  env:
    - name: NEXT_PUBLIC_API_URL
      value: "http://todo-backend:8000"
```

### Customizing Deployment

Override values during installation:

```bash
# Change replica counts
helm install todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=3

# Change resource limits
helm install todo-app ./helm/todo-app \
  --set backend.resources.limits.memory=1Gi \
  --set backend.resources.limits.cpu=1000m

# Use custom values file
helm install todo-app ./helm/todo-app \
  -f custom-values.yaml
```

### Environment Variables

#### Backend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `production` | Environment name |
| `DEBUG` | `false` | Enable debug mode |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRATION_HOURS` | `24` | JWT token expiration |
| `CORS_ORIGINS` | Various | Allowed CORS origins |
| `DATABASE_URL` | `sqlite:///app/data/todos.db` | Database connection |
| `OPENAI_API_KEY` | (from secret) | OpenAI API key |
| `JWT_SECRET` | (from secret) | JWT signing secret |

#### Frontend Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_ENV` | `production` | Node environment |
| `NEXT_PUBLIC_API_URL` | `http://todo-backend:8000` | Backend API URL |

## Accessing the Application

### Frontend Access

**Method 1: Minikube Service (Recommended for local dev)**

```bash
# Get URL and open in browser
minikube service todo-app-frontend --url

# Or automatically open in browser
minikube service todo-app-frontend
```

**Method 2: NodePort**

```bash
# Get Minikube IP
minikube ip

# Access at: http://<minikube-ip>:30080
```

**Method 3: Port Forwarding**

```bash
kubectl port-forward svc/todo-app-frontend 3000:3000

# Access at: http://localhost:3000
```

### Backend API Access

The backend is not exposed externally by default. Use port forwarding:

```bash
# Forward backend port
kubectl port-forward svc/todo-app-backend 8000:8000

# Access API at: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

### Ingress Access (Optional)

If you enabled ingress:

1. **Get Minikube IP**:
   ```bash
   minikube ip
   ```

2. **Add to hosts file**:
   ```bash
   # Linux/macOS
   echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts

   # Windows (as Administrator)
   echo %minikube ip% todo-app.local >> C:\Windows\System32\drivers\etc\hosts
   ```

3. **Access**:
   - Frontend: http://todo-app.local
   - Backend API: http://todo-app.local/api

## Troubleshooting

### Common Issues

#### 1. Pods Not Starting

**Symptoms**: Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`

**Diagnosis**:
```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/instance=todo-app

# Get detailed pod info
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>
```

**Solutions**:

- **ImagePullBackOff**: Ensure images are built in Minikube's Docker daemon
  ```bash
  eval $(minikube docker-env)
  ./phase4/scripts/build-images.sh
  ```

- **CrashLoopBackOff**: Check logs for application errors
  ```bash
  kubectl logs <pod-name> --previous  # View logs from crashed container
  ```

- **Pending**: Check resource availability
  ```bash
  kubectl describe node
  kubectl top nodes
  ```

#### 2. Backend Health Check Failures

**Symptoms**: Backend pods restarting frequently

**Diagnosis**:
```bash
# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend -f

# Check health endpoint manually
kubectl exec -it deployment/todo-app-backend -- wget -q -O- http://localhost:7860/health
```

**Solutions**:

- Verify OpenAI API key is set correctly:
  ```bash
  kubectl get secret todo-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d
  ```

- Check database initialization:
  ```bash
  kubectl exec -it deployment/todo-app-backend -- ls -la /app/data
  ```

#### 3. Frontend Cannot Connect to Backend

**Symptoms**: Frontend loads but API calls fail

**Diagnosis**:
```bash
# Check frontend environment variables
kubectl exec -it deployment/todo-app-frontend -- env | grep API

# Test backend connectivity from frontend pod
kubectl exec -it deployment/todo-app-frontend -- wget -q -O- http://todo-app-backend:8000/health
```

**Solutions**:

- Verify service DNS resolution:
  ```bash
  kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup todo-app-backend
  ```

- Check service endpoints:
  ```bash
  kubectl get endpoints todo-app-backend
  ```

#### 4. PVC Not Binding

**Symptoms**: Backend pod stuck in `Pending` with PVC mount error

**Diagnosis**:
```bash
# Check PVC status
kubectl get pvc

# Check PV availability
kubectl get pv
```

**Solutions**:

- Verify storage class exists:
  ```bash
  kubectl get storageclass
  ```

- Manually create PV if needed (Minikube usually auto-provisions)

#### 5. Out of Memory Errors

**Symptoms**: Pods killed with `OOMKilled` status

**Diagnosis**:
```bash
# Check resource usage
kubectl top pods

# View pod events
kubectl get events --sort-by='.lastTimestamp'
```

**Solutions**:

- Increase memory limits:
  ```bash
  helm upgrade todo-app ./helm/todo-app \
    --set backend.resources.limits.memory=1Gi \
    --reuse-values
  ```

### Debugging Commands

```bash
# Get all resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Describe deployment
kubectl describe deployment todo-app-backend
kubectl describe deployment todo-app-frontend

# View events
kubectl get events --sort-by='.lastTimestamp' | tail -20

# Check resource usage
kubectl top pods -l app.kubernetes.io/instance=todo-app
kubectl top nodes

# Access pod shell
kubectl exec -it deployment/todo-app-backend -- /bin/bash
kubectl exec -it deployment/todo-app-frontend -- /bin/sh

# View logs with timestamps
kubectl logs -l app.kubernetes.io/component=backend --timestamps=true -f

# Check ConfigMaps and Secrets
kubectl get configmaps
kubectl get secrets
kubectl describe secret todo-secrets
```

### Logs Collection

Collect logs for debugging:

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend --tail=100 > backend.log

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend --tail=100 > frontend.log

# All pod logs
kubectl logs -l app.kubernetes.io/instance=todo-app --all-containers=true > all-logs.log

# Previous instance logs (after crash)
kubectl logs <pod-name> --previous > crashed-pod.log
```

## Maintenance

### Upgrading the Deployment

```bash
# Pull latest code
git pull origin main

# Rebuild images
eval $(minikube docker-env)
./phase4/scripts/build-images.sh

# Upgrade Helm release
helm upgrade todo-app ./helm/todo-app \
  --reuse-values \
  --wait
```

### Scaling

```bash
# Scale backend
kubectl scale deployment/todo-app-backend --replicas=3

# Scale frontend
kubectl scale deployment/todo-app-frontend --replicas=3

# Or use Helm
helm upgrade todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=3 \
  --reuse-values
```

### Rolling Updates

```bash
# Update image tag
helm upgrade todo-app ./helm/todo-app \
  --set backend.image.tag=v1.1.0 \
  --reuse-values

# Force pod restart
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend

# Monitor rollout
kubectl rollout status deployment/todo-app-backend
```

### Backup Database

```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')

# Copy database file
kubectl cp $BACKEND_POD:/app/data/todos.db ./backup-$(date +%Y%m%d).db

# Verify backup
ls -lh backup-*.db
```

### Restore Database

```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')

# Copy database to pod
kubectl cp ./backup-20260201.db $BACKEND_POD:/app/data/todos.db

# Restart pods to pick up new database
kubectl rollout restart deployment/todo-app-backend
```

### Monitoring

```bash
# Watch pods
kubectl get pods -w -l app.kubernetes.io/instance=todo-app

# Monitor resource usage
watch kubectl top pods

# Stream logs
kubectl logs -f -l app.kubernetes.io/component=backend
```

## Cleanup

### Remove Deployment

**Using cleanup script**:
```bash
./phase4/scripts/cleanup.sh
```

**Manual cleanup**:
```bash
# Uninstall Helm release
helm uninstall todo-app

# Delete PVC
kubectl delete pvc todo-app-backend-pvc

# Delete secrets
kubectl delete secret todo-secrets

# Verify cleanup
kubectl get all -l app.kubernetes.io/instance=todo-app
```

### Remove Docker Images

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Remove images
docker rmi todo-backend:latest todo-frontend:latest

# Clean up unused images
docker image prune -f
```

### Stop Minikube

```bash
# Stop cluster
minikube stop

# Delete cluster (removes all data)
minikube delete
```

## Advanced Topics

### Using External Database

To use PostgreSQL instead of SQLite:

1. **Deploy PostgreSQL**:
   ```bash
   helm install postgres bitnami/postgresql \
     --set auth.username=todouser \
     --set auth.password=todopass \
     --set auth.database=tododb
   ```

2. **Update backend DATABASE_URL**:
   ```bash
   helm upgrade todo-app ./helm/todo-app \
     --set backend.env[6].value="postgresql+asyncpg://todouser:todopass@postgres-postgresql:5432/tododb" \
     --set backend.persistence.enabled=false \
     --reuse-values
   ```

### Custom Domain

1. **Update Ingress configuration**:
   ```yaml
   # custom-values.yaml
   ingress:
     enabled: true
     hosts:
       - host: mytodo.example.com
         paths: [...]
   ```

2. **Deploy with custom values**:
   ```bash
   helm upgrade todo-app ./helm/todo-app -f custom-values.yaml
   ```

### Enable TLS

1. **Create TLS secret**:
   ```bash
   kubectl create secret tls todo-tls \
     --cert=path/to/tls.crt \
     --key=path/to/tls.key
   ```

2. **Update Ingress**:
   ```yaml
   ingress:
     tls:
       - secretName: todo-tls
         hosts:
           - todo-app.local
   ```

## Support

For issues or questions:

1. Check logs: `kubectl logs -l app.kubernetes.io/instance=todo-app`
2. Run verification: `./phase4/scripts/verify.sh`
3. Review Helm status: `helm status todo-app`
4. Check cluster events: `kubectl get events --sort-by='.lastTimestamp'`

---

**Last Updated**: 2026-02-01
**Version**: 1.0.0
