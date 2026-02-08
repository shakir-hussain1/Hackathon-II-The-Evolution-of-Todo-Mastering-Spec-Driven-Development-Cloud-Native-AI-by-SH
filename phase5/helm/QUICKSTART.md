# Phase 5 - Quick Start Guide

Get Phase 5 running in under 10 minutes.

## 🚀 Quick Deploy (Local)

```bash
# 1. Prerequisites
minikube start --cpus=4 --memory=8192
dapr init -k

# 2. Build images
cd phase5
docker build -t phase5/chat-api:latest ./services/chat-api
docker build -t phase5/notification-service:latest ./services/notification-service
docker build -t phase5/recurring-task-service:latest ./services/recurring-task-service
docker build -t phase5/audit-service:latest ./services/audit-service
docker build -t phase5/websocket-sync-service:latest ./services/websocket-sync-service
docker build -t phase5/frontend:latest ./frontend

# 3. Load images into Minikube
minikube image load phase5/chat-api:latest
minikube image load phase5/notification-service:latest
minikube image load phase5/recurring-task-service:latest
minikube image load phase5/audit-service:latest
minikube image load phase5/websocket-sync-service:latest
minikube image load phase5/frontend:latest

# 4. Deploy
cd helm
./deploy-local.sh

# 5. Access
kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000
# Open http://localhost:3000
```

## 🔍 Verify Deployment

```bash
cd helm
./validate.sh phase5 phase5
```

## 📊 Monitor

```bash
# View all logs
kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f --all-containers=true

# Dapr dashboard
dapr dashboard -k -p 9999
# Open http://localhost:9999

# Check pods
kubectl get pods -n phase5

# Check services
kubectl get svc -n phase5
```

## 🛠️ Common Commands

```bash
# Restart a service
kubectl rollout restart deployment/phase5-chat-api -n phase5

# Scale a service
kubectl scale deployment/phase5-chat-api --replicas=3 -n phase5

# Get logs for specific service
kubectl logs -n phase5 -l app.kubernetes.io/name=chat-api -c chat-api -f

# Get Dapr sidecar logs
kubectl logs -n phase5 -l app.kubernetes.io/name=chat-api -c daprd -f

# Exec into pod
kubectl exec -it -n phase5 deployment/phase5-chat-api -c chat-api -- sh

# Port forward to API
kubectl port-forward -n phase5 svc/phase5-chat-api 8000:8000

# Test API
curl http://localhost:8000/health
```

## 🧪 Test Endpoints

Once port-forwarded to localhost:

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/ready

# Create user (example)
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com"}'

# Get tasks (example)
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>"
```

## 🔥 Troubleshooting

### Pods not starting?

```bash
kubectl describe pod <pod-name> -n phase5
kubectl logs <pod-name> -n phase5 -c <container>
```

### Dapr issues?

```bash
dapr status -k
kubectl get components -n phase5
kubectl logs <pod-name> -n phase5 -c daprd
```

### Database issues?

```bash
# Check PostgreSQL
kubectl get pods -n phase5 -l app.kubernetes.io/name=postgresql

# Connect to database
kubectl run -it --rm psql-test --image=postgres:15 -n phase5 -- \
  psql -h phase5-postgresql -U phase5_user -d phase5_db
```

### Kafka issues?

```bash
# Check Kafka
kubectl get pods -n phase5 -l app.kubernetes.io/name=kafka

# List topics
kubectl exec -it -n phase5 phase5-kafka-0 -- \
  kafka-topics.sh --list --bootstrap-server localhost:9092
```

## 🧹 Cleanup

```bash
# Remove application
helm uninstall phase5 -n phase5

# Delete namespace and PVCs
kubectl delete namespace phase5

# Stop Minikube
minikube stop
```

## 📚 Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [phase5/README.md](phase5/README.md) for full documentation
- Check [values.yaml](phase5/values.yaml) for configuration options
- Check [values-oke.yaml](phase5/values-oke.yaml) for OKE-specific settings

## 🐛 Common Issues

**Issue**: Pods stuck in `ImagePullBackOff`
**Fix**: Make sure images are loaded into Minikube:
```bash
minikube image load phase5/chat-api:latest
```

**Issue**: Dapr sidecar not injecting
**Fix**: Verify Dapr is installed:
```bash
dapr status -k
```

**Issue**: PVCs stuck in `Pending`
**Fix**: Check storage class:
```bash
kubectl get storageclass
minikube addons enable default-storageclass
```

**Issue**: Port forward fails
**Fix**: Check pod is running:
```bash
kubectl get pods -n phase5
```

## 💡 Tips

- Use `kubectl get events -n phase5 --sort-by='.lastTimestamp'` to debug issues
- Set `imagePullPolicy: Never` in values.yaml for local development
- Use `helm upgrade` instead of `install` to update deployments
- Enable Minikube dashboard: `minikube dashboard`

## 🎯 Success Criteria

After deployment, you should see:

- ✅ 10+ pods running (services + infrastructure)
- ✅ All Dapr components created
- ✅ Health endpoints responding
- ✅ Frontend accessible via port-forward
- ✅ All HPAs active

Run `./validate.sh` to check!
