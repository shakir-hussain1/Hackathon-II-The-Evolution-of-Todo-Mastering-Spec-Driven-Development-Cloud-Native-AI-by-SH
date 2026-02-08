# Phase 5 Helm Chart

Production-ready Helm chart for deploying the Phase V Cloud-Native Todo Application to Kubernetes (Oracle OKE).

## Architecture

This umbrella chart deploys a complete microservices architecture with:

### Services
- **chat-api** (port 8000) - Main API with AI chat capabilities
- **notification-service** (port 8001) - Handles notifications and reminders
- **recurring-task-service** (port 8002) - Manages recurring tasks
- **audit-service** (port 8003) - Audit logging and compliance
- **websocket-sync-service** (port 8004) - Real-time WebSocket sync
- **frontend** (port 3000) - Next.js UI

### Infrastructure
- **PostgreSQL** - Primary database
- **Kafka** - Event streaming (via Bitnami chart)
- **Dapr** - Microservices runtime with sidecars

### Dapr Components
- **pubsub-kafka** - Kafka pub/sub for event-driven architecture
- **statestore-postgresql** - PostgreSQL state store
- **secretstore-kubernetes** - Kubernetes secret management
- **cron-recurring-tasks** - Cron binding (every 5 minutes)
- **cron-reminders** - Cron binding (every minute)
- **dapr-config** - Global Dapr configuration with Zipkin tracing

## Prerequisites

1. **Kubernetes Cluster** (Oracle OKE recommended)
   - Kubernetes 1.24+
   - kubectl configured

2. **Helm 3.8+**
   ```bash
   helm version
   ```

3. **Dapr installed on cluster**
   ```bash
   dapr init -k
   ```

4. **NGINX Ingress Controller**
   ```bash
   helm install nginx-ingress ingress-nginx/ingress-nginx \
     --namespace ingress-nginx --create-namespace
   ```

5. **Cert-Manager** (optional, for TLS)
   ```bash
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
   ```

## Installation

### Quick Start (Local/Minikube)

1. **Add Bitnami repository**:
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

2. **Install the chart**:
   ```bash
   helm install phase5 ./helm/phase5 \
     --namespace phase5 \
     --create-namespace \
     --set postgresql.auth.password=secure_password_here \
     --set jwtSecret=your_jwt_secret_here \
     --set openaiApiKey=sk-your-openai-key
   ```

3. **Check deployment**:
   ```bash
   kubectl get pods -n phase5
   kubectl get svc -n phase5
   ```

4. **Access the application**:
   ```bash
   # Port forward frontend
   kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000

   # Open browser
   open http://localhost:3000
   ```

### Production Deployment (Oracle OKE)

1. **Configure OKE credentials**:
   ```bash
   # Set up OCIR credentials
   kubectl create secret docker-registry ocir-secret \
     --docker-server=iad.ocir.io \
     --docker-username='<tenancy-namespace>/<username>' \
     --docker-password='<auth-token>' \
     --namespace phase5
   ```

2. **Create secrets** (do NOT use default values):
   ```bash
   # PostgreSQL password
   kubectl create secret generic postgres-secret \
     --from-literal=password=$(openssl rand -base64 32) \
     --namespace phase5

   # JWT secret
   kubectl create secret generic jwt-secret \
     --from-literal=secret=$(openssl rand -base64 32) \
     --namespace phase5

   # OpenAI API key
   kubectl create secret generic openai-secret \
     --from-literal=api-key='sk-your-actual-key' \
     --namespace phase5
   ```

3. **Deploy with OKE values**:
   ```bash
   helm install phase5 ./helm/phase5 \
     --namespace phase5 \
     --create-namespace \
     -f ./helm/phase5/values-oke.yaml \
     --set global.imageRegistry=iad.ocir.io/your-tenancy \
     --set global.domain=phase5.oraclecloud.com
   ```

4. **Verify deployment**:
   ```bash
   # Check all pods are running
   kubectl get pods -n phase5 -w

   # Check Dapr sidecars
   kubectl get pods -n phase5 -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].name}{"\n"}{end}'

   # Check services
   kubectl get svc -n phase5

   # Check ingress
   kubectl get ingress -n phase5
   ```

## Configuration

### Key Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.namespace` | Kubernetes namespace | `phase5` |
| `global.imageRegistry` | Docker registry | `docker.io` |
| `global.storageClass` | Storage class | `standard` (OKE: `oci-bv`) |
| `global.domain` | Application domain | `phase5.local` |
| `postgresql.enabled` | Enable PostgreSQL | `true` |
| `kafka.enabled` | Enable Kafka | `true` |
| `chat-api.enabled` | Enable chat-api service | `true` |
| `frontend.enabled` | Enable frontend | `true` |

### Secrets

All secrets should be created externally for production:

```bash
# Example: Create all secrets at once
kubectl create secret generic postgres-secret \
  --from-literal=connection-string='postgresql://user:pass@host:5432/db' \
  --from-literal=dapr-connection-string='host=host port=5432 user=user password=pass dbname=db' \
  --namespace phase5

kubectl create secret generic jwt-secret \
  --from-literal=secret=$(openssl rand -base64 32) \
  --namespace phase5

kubectl create secret generic openai-secret \
  --from-literal=api-key='sk-your-key' \
  --namespace phase5
```

### Resource Limits

Each service has default resource limits:

| Service | Memory Request | Memory Limit | CPU Request | CPU Limit |
|---------|----------------|--------------|-------------|-----------|
| chat-api | 256Mi | 512Mi | 100m | 500m |
| notification-service | 128Mi | 256Mi | 50m | 250m |
| recurring-task-service | 128Mi | 256Mi | 50m | 250m |
| audit-service | 128Mi | 256Mi | 50m | 250m |
| websocket-sync-service | 256Mi | 512Mi | 100m | 500m |
| frontend | 256Mi | 512Mi | 100m | 500m |

Override in values-oke.yaml for production workloads.

### Autoscaling

HPA is enabled by default:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
```

## Upgrading

```bash
helm upgrade phase5 ./helm/phase5 \
  --namespace phase5 \
  -f ./helm/phase5/values-oke.yaml
```

## Uninstalling

```bash
# Uninstall the release
helm uninstall phase5 --namespace phase5

# Delete the namespace (optional)
kubectl delete namespace phase5

# Clean up PVCs (if needed)
kubectl delete pvc -n phase5 --all
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -n phase5

# Describe pod to see events
kubectl describe pod <pod-name> -n phase5

# Check logs
kubectl logs <pod-name> -n phase5 -c <container-name>

# Check Dapr sidecar logs
kubectl logs <pod-name> -n phase5 -c daprd
```

### Dapr issues

```bash
# Verify Dapr installation
dapr status -k

# Check Dapr components
kubectl get components -n phase5

# Check Dapr configuration
kubectl get configuration -n phase5
```

### Database connection issues

```bash
# Test PostgreSQL connection
kubectl run -it --rm --image=postgres:15 --namespace=phase5 psql-test -- \
  psql -h phase5-postgresql -U phase5_user -d phase5_db

# Check secret
kubectl get secret postgres-secret -n phase5 -o yaml
```

### Kafka issues

```bash
# Check Kafka pods
kubectl get pods -n phase5 -l app.kubernetes.io/name=kafka

# Test Kafka connection
kubectl run -it --rm kafka-test --image=bitnami/kafka:latest --namespace=phase5 -- \
  kafka-topics.sh --list --bootstrap-server phase5-kafka:9092
```

## Monitoring

### Health Checks

All services expose health endpoints:

- `/health` - Liveness probe
- `/ready` - Readiness probe

### Dapr Metrics

Dapr exposes Prometheus metrics on port 9090:

```bash
# Port forward Dapr metrics
kubectl port-forward -n phase5 <pod-name> 9090:9090

# Scrape metrics
curl http://localhost:9090/metrics
```

### Logs

```bash
# Follow logs for all services
kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f --all-containers=true

# Specific service
kubectl logs -n phase5 -l app.kubernetes.io/name=chat-api -f
```

## Development

### Local Testing with Minikube

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Install Dapr
dapr init -k

# Deploy
helm install phase5 ./helm/phase5 --namespace phase5 --create-namespace

# Get ingress IP
minikube ip

# Add to /etc/hosts
echo "$(minikube ip) phase5.local" | sudo tee -a /etc/hosts
```

### Building Images

```bash
# Build all services
cd phase5

# Build and tag images
docker build -t phase5/chat-api:latest ./services/chat-api
docker build -t phase5/notification-service:latest ./services/notification-service
docker build -t phase5/recurring-task-service:latest ./services/recurring-task-service
docker build -t phase5/audit-service:latest ./services/audit-service
docker build -t phase5/websocket-sync-service:latest ./services/websocket-sync-service
docker build -t phase5/frontend:latest ./frontend

# For Minikube, load images
minikube image load phase5/chat-api:latest
minikube image load phase5/notification-service:latest
minikube image load phase5/recurring-task-service:latest
minikube image load phase5/audit-service:latest
minikube image load phase5/websocket-sync-service:latest
minikube image load phase5/frontend:latest
```

## Architecture Decisions

- **Dapr sidecars**: All services use Dapr for service invocation, pub/sub, and state management
- **PostgreSQL**: Single database instance with connection pooling
- **Kafka**: 3-node cluster for high availability
- **Horizontal Pod Autoscaling**: Automatic scaling based on CPU/memory
- **Anti-affinity**: Pods spread across nodes for resilience
- **Health probes**: Liveness and readiness checks on all services
- **Security**: Non-root users, read-only filesystem where possible

## License

MIT
