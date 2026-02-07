# Complete Installation Guide

Step-by-step guide to deploy the Todo App on Minikube from scratch.

## Prerequisites Check

Before starting, ensure you have:

- [ ] **Minikube** installed and working
- [ ] **kubectl** installed and working
- [ ] **Helm** v3.12+ installed
- [ ] **Docker** installed and running
- [ ] **Git** (to clone the repository)
- [ ] **4GB+ RAM** available for Minikube
- [ ] **20GB+ disk space** available

### Verify Prerequisites

```bash
# Check Minikube
minikube version
# Expected: minikube version: v1.30.0 or later

# Check kubectl
kubectl version --client
# Expected: Client Version: v1.27.0 or later

# Check Helm
helm version
# Expected: version.BuildInfo{Version:"v3.12.0" or later}

# Check Docker
docker --version
# Expected: Docker version 20.10.0 or later

# Check available resources
free -h  # Linux
# or
vm_stat # macOS
# Ensure at least 4GB free RAM
```

## Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd Hackathon-II-The-Evolution-of-Todo

# Navigate to Phase 4
cd phase4
```

## Step 2: Start Minikube

### Option A: Default Configuration
```bash
minikube start --cpus=4 --memory=8192
```

### Option B: Custom Configuration
```bash
# For systems with limited resources
minikube start --cpus=2 --memory=4096 --disk-size=20g

# For systems with more resources
minikube start --cpus=6 --memory=12288 --disk-size=30g
```

### Verify Minikube Started
```bash
minikube status
# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

### Enable Required Addons
```bash
# Enable storage provisioner (usually enabled by default)
minikube addons enable storage-provisioner

# Optional: Enable ingress if you want to use Ingress
minikube addons enable ingress

# Optional: Enable metrics for resource monitoring
minikube addons enable metrics-server

# Verify addons
minikube addons list
```

## Step 3: Configure Environment

### Create Environment File

```bash
# Copy the example file
cp .env.example .env

# Edit the file
nano .env  # or use your preferred editor
```

### Required Configuration

Add the following to `.env`:

```bash
# OpenAI API Key (REQUIRED)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# JWT Secret (REQUIRED)
# Generate with: openssl rand -hex 32
JWT_SECRET=your-secure-random-jwt-secret-minimum-32-characters
```

### Generate JWT Secret

```bash
# Generate a secure JWT secret
openssl rand -hex 32

# Or on Windows (PowerShell)
# [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### Verify Configuration

```bash
# Source the environment file
source .env  # Linux/macOS
# or
# In PowerShell: Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }

# Verify variables are set
echo $OPENAI_API_KEY
echo $JWT_SECRET
```

## Step 4: Build Docker Images

### Configure Docker to Use Minikube

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify connection
docker ps
# Should show containers running in Minikube
```

### Build Images

**Linux/macOS:**
```bash
# Make script executable
chmod +x scripts/build-images.sh

# Run build script
./scripts/build-images.sh
```

**Windows:**
```cmd
REM Run build script
scripts\build-images.bat
```

### Verify Images

```bash
# List images
docker images | grep todo-

# Expected output:
# todo-backend     latest    <image-id>   X minutes ago   ~245MB
# todo-frontend    latest    <image-id>   X minutes ago   ~178MB
```

## Step 5: Deploy with Helm

### Option A: Automated Deployment (Recommended)

**Linux/macOS:**
```bash
# Make deploy script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

**Windows:**
```cmd
scripts\deploy.bat
```

The script will:
1. Check Minikube status
2. Validate environment variables
3. Build Docker images
4. Install/upgrade Helm release
5. Wait for pods to be ready
6. Display access information

### Option B: Manual Deployment

```bash
# Ensure environment variables are loaded
source .env

# Install Helm chart
helm install todo-app ./helm/todo-app \
  --set secrets.openaiApiKey="$OPENAI_API_KEY" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  --wait \
  --timeout 5m

# Verify installation
helm list
```

## Step 6: Verify Deployment

### Run Verification Script

```bash
# Make script executable
chmod +x scripts/verify.sh

# Run verification
./scripts/verify.sh
```

### Manual Verification

```bash
# Check all resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Expected output:
# NAME                                      READY   STATUS    RESTARTS   AGE
# pod/todo-app-backend-xxxxx-xxxxx          1/1     Running   0          2m
# pod/todo-app-backend-xxxxx-yyyyy          1/1     Running   0          2m
# pod/todo-app-frontend-xxxxx-xxxxx         1/1     Running   0          2m
# pod/todo-app-frontend-xxxxx-yyyyy         1/1     Running   0          2m
#
# NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# service/todo-app-backend       ClusterIP   10.96.xxx.xxx   <none>        8000/TCP         2m
# service/todo-app-frontend      NodePort    10.96.xxx.xxx   <none>        3000:30080/TCP   2m
#
# NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/todo-app-backend    2/2     2            2           2m
# deployment.apps/todo-app-frontend   2/2     2            2           2m

# Check pod logs
kubectl logs -l app.kubernetes.io/component=backend --tail=20
kubectl logs -l app.kubernetes.io/component=frontend --tail=20
```

### Health Checks

```bash
# Test backend health endpoint
kubectl exec deployment/todo-app-backend -- wget -q -O- http://localhost:7860/health

# Expected output: {"status":"healthy","environment":"production"}

# Test frontend
kubectl exec deployment/todo-app-frontend -- wget -q -O- http://localhost:3000 | head -c 100
```

## Step 7: Access the Application

### Frontend Access

**Method 1: Minikube Service (Recommended)**
```bash
# Get URL
minikube service todo-app-frontend --url

# Output example: http://192.168.49.2:30080

# Open in browser automatically
minikube service todo-app-frontend
```

**Method 2: Port Forwarding**
```bash
# Forward port
kubectl port-forward svc/todo-app-frontend 3000:3000

# Access at: http://localhost:3000
```

### Backend API Access

```bash
# Forward backend port
kubectl port-forward svc/todo-app-backend 8000:8000

# Access in browser:
# API: http://localhost:8000
# Interactive docs: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API docs (open in browser)
open http://localhost:8000/docs  # macOS
xdg-open http://localhost:8000/docs  # Linux
start http://localhost:8000/docs  # Windows
```

## Step 8: Post-Deployment Verification

### Create Test User and Todo

```bash
# 1. Open frontend in browser
minikube service todo-app-frontend

# 2. Register a new user
# 3. Login
# 4. Create a todo item
# 5. Verify it persists after pod restart

# Test persistence
kubectl delete pod -l app.kubernetes.io/component=backend
kubectl wait --for=condition=ready pod -l app.kubernetes.io/component=backend --timeout=60s

# Refresh frontend - todos should still be there
```

### Monitor Resources

```bash
# Watch pods
kubectl get pods -w

# Check resource usage
kubectl top pods

# View events
kubectl get events --sort-by='.lastTimestamp' | tail -20
```

## Troubleshooting

### Issue: Pods Not Starting

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/instance=todo-app

# Describe problematic pod
kubectl describe pod <pod-name>

# Common fixes:
# 1. Ensure images are in Minikube's Docker
eval $(minikube docker-env)
./scripts/build-images.sh

# 2. Check secrets
kubectl get secret todo-secrets

# 3. Restart deployment
kubectl rollout restart deployment/todo-app-backend
```

### Issue: ImagePullBackOff

```bash
# This means Docker can't find the image
# Solution: Rebuild in Minikube's Docker daemon

eval $(minikube docker-env)
./scripts/build-images.sh
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend
```

### Issue: Can't Access Frontend

```bash
# Check service
kubectl get svc todo-app-frontend

# Get Minikube IP
minikube ip

# Manually construct URL
echo "http://$(minikube ip):$(kubectl get svc todo-app-frontend -o jsonpath='{.spec.ports[0].nodePort}')"
```

### Full Troubleshooting Guide

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for comprehensive troubleshooting.

## Cleanup (When Done Testing)

### Remove Deployment

```bash
# Option 1: Use cleanup script
./scripts/cleanup.sh

# Option 2: Manual cleanup
helm uninstall todo-app
kubectl delete pvc todo-app-backend-pvc
kubectl delete secret todo-secrets
```

### Stop Minikube

```bash
# Stop (keeps data)
minikube stop

# Delete (removes everything)
minikube delete
```

## Next Steps

After successful installation:

1. **Explore the Application**
   - Create user accounts
   - Add/edit/delete todos
   - Test the chatbot functionality

2. **Monitor Performance**
   ```bash
   kubectl top pods
   kubectl logs -f -l app.kubernetes.io/component=backend
   ```

3. **Experiment with Scaling**
   ```bash
   kubectl scale deployment/todo-app-backend --replicas=3
   ```

4. **Customize Configuration**
   - Edit `helm/todo-app/values.yaml`
   - Run `helm upgrade todo-app ./helm/todo-app`

5. **Read Documentation**
   - [DEPLOYMENT.md](../DEPLOYMENT.md) - Complete guide
   - [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Command reference
   - [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Problem solving

## Common Commands Reference

```bash
# Status
kubectl get all -l app.kubernetes.io/instance=todo-app
helm status todo-app

# Logs
kubectl logs -f -l app.kubernetes.io/component=backend
kubectl logs -f -l app.kubernetes.io/component=frontend

# Restart
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend

# Scale
kubectl scale deployment/todo-app-backend --replicas=3

# Access
minikube service todo-app-frontend --url
kubectl port-forward svc/todo-app-backend 8000:8000

# Cleanup
helm uninstall todo-app
./scripts/cleanup.sh
```

## Support

If you encounter issues:

1. Run verification: `./scripts/verify.sh`
2. Check logs: `kubectl logs <pod-name>`
3. Review troubleshooting: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
4. Check Helm status: `helm status todo-app`

---

**Installation Complete!** 🎉

You now have a fully functional Todo application running on Kubernetes with:
- High availability (2 replicas each)
- Persistent storage for todos
- Health monitoring
- Auto-recovery
- Production-ready configuration

Enjoy exploring the application!
