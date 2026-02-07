# Quick Reference Guide

Fast reference for common operations with the Todo App Kubernetes deployment.

## One-Line Commands

### Deployment
```bash
# Deploy everything
./scripts/deploy.sh

# Deploy with custom secrets
OPENAI_API_KEY=sk-xxx JWT_SECRET=yyy ./scripts/deploy.sh

# Manual install
helm install todo-app ./helm/todo-app --set secrets.openaiApiKey=sk-xxx --set secrets.jwtSecret=yyy
```

### Access
```bash
# Frontend URL
minikube service todo-app-frontend --url

# Backend port-forward
kubectl port-forward svc/todo-app-backend 8000:8000
```

### Monitoring
```bash
# Watch pods
kubectl get pods -w -l app.kubernetes.io/instance=todo-app

# Logs (backend)
kubectl logs -f -l app.kubernetes.io/component=backend

# Logs (frontend)
kubectl logs -f -l app.kubernetes.io/component=frontend

# Resource usage
kubectl top pods -l app.kubernetes.io/instance=todo-app
```

### Debugging
```bash
# Pod details
kubectl describe pod <pod-name>

# Shell access (backend)
kubectl exec -it deployment/todo-app-backend -- /bin/bash

# Shell access (frontend)
kubectl exec -it deployment/todo-app-frontend -- /bin/sh

# Test backend health
kubectl exec deployment/todo-app-backend -- wget -q -O- http://localhost:7860/health
```

### Maintenance
```bash
# Scale up
kubectl scale deployment/todo-app-backend --replicas=3

# Restart
kubectl rollout restart deployment/todo-app-backend

# Upgrade
helm upgrade todo-app ./helm/todo-app --reuse-values

# Rollback
helm rollback todo-app
```

### Cleanup
```bash
# Remove deployment
helm uninstall todo-app

# Remove PVC
kubectl delete pvc todo-app-backend-pvc

# Complete cleanup
./scripts/cleanup.sh
```

## Status Checks

### Quick Health Check
```bash
kubectl get pods,svc,pvc -l app.kubernetes.io/instance=todo-app
```

### Detailed Status
```bash
# Helm release status
helm status todo-app

# All resources
kubectl get all -l app.kubernetes.io/instance=todo-app

# Events (sorted by time)
kubectl get events --sort-by='.lastTimestamp' | tail -20
```

### Verify Deployment
```bash
./scripts/verify.sh
```

## Common Issues & Fixes

### ImagePullBackOff
```bash
# Fix: Rebuild images in Minikube
eval $(minikube docker-env)
./scripts/build-images.sh
kubectl rollout restart deployment/todo-app-backend
kubectl rollout restart deployment/todo-app-frontend
```

### CrashLoopBackOff
```bash
# View logs from previous crash
kubectl logs <pod-name> --previous

# Check secrets
kubectl get secret todo-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d
```

### Pending Pods
```bash
# Check node resources
kubectl describe nodes

# Check events
kubectl describe pod <pod-name>
```

### PVC Not Binding
```bash
# Check storage class
kubectl get storageclass

# Check PV
kubectl get pv
```

## Environment Variables

### Backend
```bash
# View all env vars
kubectl exec deployment/todo-app-backend -- env

# View specific var
kubectl exec deployment/todo-app-backend -- printenv DATABASE_URL
```

### Frontend
```bash
# View API URL
kubectl exec deployment/todo-app-frontend -- printenv NEXT_PUBLIC_API_URL
```

## Secrets Management

### View Secret (base64 encoded)
```bash
kubectl get secret todo-secrets -o yaml
```

### Decode Secret
```bash
# OpenAI API Key
kubectl get secret todo-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d

# JWT Secret
kubectl get secret todo-secrets -o jsonpath='{.data.jwt-secret}' | base64 -d
```

### Update Secret
```bash
# Delete old secret
kubectl delete secret todo-secrets

# Recreate with new values
kubectl create secret generic todo-secrets \
  --from-literal=openai-api-key=sk-new-key \
  --from-literal=jwt-secret=new-secret

# Restart pods to pick up new secret
kubectl rollout restart deployment/todo-app-backend
```

## Database Operations

### Backup Database
```bash
POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
kubectl cp $POD:/app/data/todos.db ./backup-$(date +%Y%m%d-%H%M%S).db
```

### Restore Database
```bash
POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
kubectl cp ./backup.db $POD:/app/data/todos.db
kubectl rollout restart deployment/todo-app-backend
```

### View Database Size
```bash
kubectl exec deployment/todo-app-backend -- ls -lh /app/data/todos.db
```

## Logs

### Stream All Logs
```bash
kubectl logs -f -l app.kubernetes.io/instance=todo-app --all-containers=true
```

### Save Logs to File
```bash
kubectl logs -l app.kubernetes.io/component=backend --tail=500 > backend.log
kubectl logs -l app.kubernetes.io/component=frontend --tail=500 > frontend.log
```

### Filter Logs
```bash
# Only errors
kubectl logs -l app.kubernetes.io/component=backend | grep -i error

# With timestamps
kubectl logs -l app.kubernetes.io/component=backend --timestamps=true
```

## Port Forwarding

### Backend API
```bash
kubectl port-forward svc/todo-app-backend 8000:8000
# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Frontend
```bash
kubectl port-forward svc/todo-app-frontend 3000:3000
# Access: http://localhost:3000
```

### Specific Pod
```bash
kubectl port-forward <pod-name> 8000:7860
```

## Helm Operations

### List Releases
```bash
helm list
```

### Get Values
```bash
# All values
helm get values todo-app

# Including defaults
helm get values todo-app --all
```

### Upgrade with New Values
```bash
helm upgrade todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --reuse-values
```

### History
```bash
helm history todo-app
```

### Rollback
```bash
# Rollback to previous version
helm rollback todo-app

# Rollback to specific revision
helm rollback todo-app 2
```

## Scaling

### Manual Scaling
```bash
# Scale backend
kubectl scale deployment/todo-app-backend --replicas=4

# Scale frontend
kubectl scale deployment/todo-app-frontend --replicas=4

# Verify
kubectl get deployments
```

### Auto-scaling (HPA)
```bash
# Enable metrics server (if not enabled)
minikube addons enable metrics-server

# Create HPA for backend
kubectl autoscale deployment todo-app-backend \
  --cpu-percent=80 \
  --min=2 \
  --max=10

# Check HPA status
kubectl get hpa
```

## Resource Management

### View Resource Usage
```bash
# Current usage
kubectl top pods

# Node usage
kubectl top nodes
```

### Update Resource Limits
```bash
helm upgrade todo-app ./helm/todo-app \
  --set backend.resources.limits.memory=1Gi \
  --set backend.resources.limits.cpu=1000m \
  --reuse-values
```

## Network Testing

### DNS Resolution
```bash
# Test from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup todo-app-backend
```

### Service Connectivity
```bash
# Test backend from frontend pod
kubectl exec -it deployment/todo-app-frontend -- wget -q -O- http://todo-app-backend:8000/health

# Test frontend from backend pod
kubectl exec -it deployment/todo-app-backend -- wget -q -O- http://todo-app-frontend:3000
```

### Curl from Pod
```bash
# Backend health endpoint
kubectl exec -it deployment/todo-app-backend -- curl http://localhost:7860/health

# Frontend
kubectl exec -it deployment/todo-app-frontend -- curl http://localhost:3000
```

## Minikube Specific

### Access Services
```bash
# Get URL
minikube service todo-app-frontend --url

# Open in browser
minikube service todo-app-frontend
```

### SSH into Minikube
```bash
minikube ssh
```

### View Dashboard
```bash
minikube dashboard
```

### Tunnel (for LoadBalancer)
```bash
# Run in separate terminal
minikube tunnel
```

## Configuration Updates

### Update Environment Variable
```bash
# Via Helm
helm upgrade todo-app ./helm/todo-app \
  --set backend.env[0].value="development" \
  --reuse-values

# Direct edit (not recommended)
kubectl edit deployment todo-app-backend
```

### Update Image
```bash
# Build new image
eval $(minikube docker-env)
docker build -t todo-backend:v2 -f phase4/docker/backend.Dockerfile .

# Update deployment
helm upgrade todo-app ./helm/todo-app \
  --set backend.image.tag=v2 \
  --reuse-values
```

## Validation

### Validate Helm Chart
```bash
# Lint chart
helm lint ./helm/todo-app

# Dry run install
helm install todo-app ./helm/todo-app --dry-run --debug

# Template rendering
helm template todo-app ./helm/todo-app
```

### Validate YAML
```bash
# Generate manifests
helm template todo-app ./helm/todo-app > manifests.yaml

# Validate with kubectl
kubectl apply --dry-run=client -f manifests.yaml
```

## Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Kubectl shortcuts
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get svc'
alias kgd='kubectl get deployments'
alias kl='kubectl logs -f'
alias kx='kubectl exec -it'
alias kpf='kubectl port-forward'

# Todo app specific
alias todo-pods='kubectl get pods -l app.kubernetes.io/instance=todo-app'
alias todo-logs-backend='kubectl logs -f -l app.kubernetes.io/component=backend'
alias todo-logs-frontend='kubectl logs -f -l app.kubernetes.io/component=frontend'
alias todo-status='kubectl get all -l app.kubernetes.io/instance=todo-app'
alias todo-frontend='minikube service todo-app-frontend'
alias todo-backend='kubectl port-forward svc/todo-app-backend 8000:8000'
```

## Emergency Procedures

### Complete Reset
```bash
# Uninstall release
helm uninstall todo-app

# Delete all resources
kubectl delete all -l app.kubernetes.io/instance=todo-app
kubectl delete pvc -l app.kubernetes.io/instance=todo-app
kubectl delete secret todo-secrets

# Rebuild and redeploy
./scripts/deploy.sh
```

### Force Delete Stuck Pod
```bash
kubectl delete pod <pod-name> --grace-period=0 --force
```

### Recreate Failed Deployment
```bash
kubectl delete deployment todo-app-backend
helm upgrade todo-app ./helm/todo-app --reuse-values
```

---

**Tip**: Bookmark this page for quick reference during development and troubleshooting!
