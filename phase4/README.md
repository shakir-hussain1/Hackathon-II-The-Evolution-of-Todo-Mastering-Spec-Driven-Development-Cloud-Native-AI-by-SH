# Phase 4: Kubernetes Deployment with Helm

Production-ready Kubernetes deployment for the Phase 3 Todo Chatbot application using Helm charts optimized for Minikube.

## Quick Start

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and JWT_SECRET

# 3. Deploy (Linux/macOS)
chmod +x scripts/*.sh
./scripts/deploy.sh

# 3. Deploy (Windows)
scripts\deploy.bat
```

## What You Get

- **Frontend**: Next.js application with 2 replicas
- **Backend**: FastAPI application with 2 replicas
- **Database**: Persistent SQLite database (1Gi PVC)
- **Load Balancing**: Kubernetes service load balancing
- **Health Checks**: Automatic liveness and readiness probes
- **Resource Limits**: CPU and memory limits for stability

## Directory Structure

```
phase4/
├── helm/
│   └── todo-app/              # Helm chart
│       ├── Chart.yaml          # Chart metadata
│       ├── values.yaml         # Configuration values
│       ├── templates/          # Kubernetes templates
│       │   ├── backend-deployment.yaml
│       │   ├── backend-service.yaml
│       │   ├── backend-pvc.yaml
│       │   ├── frontend-deployment.yaml
│       │   ├── frontend-service.yaml
│       │   ├── ingress.yaml
│       │   ├── secrets.yaml
│       │   ├── _helpers.tpl
│       │   └── NOTES.txt
│       └── .helmignore
├── docker/
│   ├── backend.Dockerfile      # Multi-stage backend build
│   └── frontend.Dockerfile     # Multi-stage frontend build
├── scripts/
│   ├── build-images.sh         # Build Docker images (Linux/macOS)
│   ├── build-images.bat        # Build Docker images (Windows)
│   ├── deploy.sh               # Deploy to Minikube (Linux/macOS)
│   ├── deploy.bat              # Deploy to Minikube (Windows)
│   ├── verify.sh               # Verify deployment health
│   └── cleanup.sh              # Clean up deployment
├── DEPLOYMENT.md               # Comprehensive deployment guide
├── README.md                   # This file
└── .env.example                # Environment variables template
```

## Prerequisites

- **Minikube** v1.30+ ([Install](https://minikube.sigs.k8s.io/docs/start/))
- **kubectl** v1.27+ ([Install](https://kubernetes.io/docs/tasks/tools/))
- **Helm** v3.12+ ([Install](https://helm.sh/docs/intro/install/))
- **Docker** v20.10+ ([Install](https://docs.docker.com/get-docker/))
- **System**: 4GB RAM, 2 CPU cores minimum

## Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)**: Complete deployment guide with troubleshooting
- **[Helm Chart Values](./helm/todo-app/values.yaml)**: Configuration reference
- **[Phase 3 Application](../phase3/README.md)**: Application documentation

## Common Commands

### Deployment

```bash
# Deploy
./scripts/deploy.sh

# Verify deployment
./scripts/verify.sh

# Check pod status
kubectl get pods -l app.kubernetes.io/instance=todo-app

# View logs
kubectl logs -l app.kubernetes.io/component=backend -f
kubectl logs -l app.kubernetes.io/component=frontend -f
```

### Access

```bash
# Frontend
minikube service todo-app-frontend --url

# Backend (port forward)
kubectl port-forward svc/todo-app-backend 8000:8000
# Then open: http://localhost:8000/docs
```

### Maintenance

```bash
# Scale replicas
kubectl scale deployment/todo-app-backend --replicas=3

# Restart pods
kubectl rollout restart deployment/todo-app-backend

# Upgrade deployment
helm upgrade todo-app ./helm/todo-app --reuse-values

# Backup database
BACKEND_POD=$(kubectl get pods -l app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}')
kubectl cp $BACKEND_POD:/app/data/todos.db ./backup.db
```

### Cleanup

```bash
# Remove deployment
./scripts/cleanup.sh

# Or manually
helm uninstall todo-app
kubectl delete pvc todo-app-backend-pvc
```

## Architecture

```
┌─────────────────────────────────────┐
│         Minikube Cluster            │
│                                     │
│  ┌───────────────────────────────┐ │
│  │     Frontend Service          │ │
│  │     (NodePort: 30080)         │ │
│  └───────────┬───────────────────┘ │
│              │                      │
│  ┌───────────▼───────────────────┐ │
│  │  Frontend Pods (2 replicas)   │ │
│  │  Next.js on port 3000         │ │
│  └───────────────────────────────┘ │
│              │                      │
│              │ Calls API            │
│              │                      │
│  ┌───────────▼───────────────────┐ │
│  │     Backend Service           │ │
│  │     (ClusterIP: 8000)         │ │
│  └───────────┬───────────────────┘ │
│              │                      │
│  ┌───────────▼───────────────────┐ │
│  │  Backend Pods (2 replicas)    │ │
│  │  FastAPI on port 7860         │ │
│  └───────────┬───────────────────┘ │
│              │                      │
│  ┌───────────▼───────────────────┐ │
│  │  PersistentVolume (1Gi)       │ │
│  │  SQLite Database              │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## Configuration

Key configuration options in `values.yaml`:

```yaml
# Replica counts
backend.replicaCount: 2
frontend.replicaCount: 2

# Resource limits
backend.resources.limits.memory: 512Mi
backend.resources.limits.cpu: 500m

# Service configuration
frontend.service.type: NodePort
frontend.service.nodePort: 30080

# Storage
backend.persistence.enabled: true
backend.persistence.size: 1Gi
```

Override during installation:

```bash
helm install todo-app ./helm/todo-app \
  --set backend.replicaCount=3 \
  --set backend.resources.limits.memory=1Gi
```

## Troubleshooting

### Pods not starting?

```bash
# Check pod status
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Common fix: Rebuild images in Minikube's Docker
eval $(minikube docker-env)
./scripts/build-images.sh
```

### Can't access frontend?

```bash
# Get URL
minikube service todo-app-frontend --url

# Or check NodePort
kubectl get svc todo-app-frontend
```

### Backend health check failing?

```bash
# Check logs
kubectl logs -l app.kubernetes.io/component=backend

# Verify secrets
kubectl get secret todo-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d
```

For more troubleshooting, see [DEPLOYMENT.md](./DEPLOYMENT.md#troubleshooting).

## Features

- **High Availability**: Multiple replicas for zero-downtime deployments
- **Auto-healing**: Kubernetes automatically restarts failed pods
- **Resource Management**: CPU and memory limits prevent resource exhaustion
- **Health Monitoring**: Liveness and readiness probes ensure healthy pods
- **Persistent Storage**: Database survives pod restarts
- **Secure Secrets**: API keys and JWT secrets stored in Kubernetes secrets
- **Easy Scaling**: Scale up/down with a single command
- **Rolling Updates**: Update application with zero downtime

## Development vs Production

This deployment is optimized for **local development with Minikube**. For production:

1. Use managed Kubernetes (EKS, GKS, AKS)
2. Replace SQLite with PostgreSQL/MySQL
3. Enable Horizontal Pod Autoscaler (HPA)
4. Add monitoring (Prometheus, Grafana)
5. Configure Ingress with TLS
6. Use external secrets manager (AWS Secrets Manager, HashiCorp Vault)
7. Implement backup and disaster recovery

## Support

- **Issues**: See [Troubleshooting](./DEPLOYMENT.md#troubleshooting)
- **Logs**: `kubectl logs -l app.kubernetes.io/instance=todo-app`
- **Status**: `helm status todo-app`
- **Documentation**: [DEPLOYMENT.md](./DEPLOYMENT.md)

## License

Same as main project

---

**Phase**: 4
**Status**: Production Ready
**Last Updated**: 2026-02-01
