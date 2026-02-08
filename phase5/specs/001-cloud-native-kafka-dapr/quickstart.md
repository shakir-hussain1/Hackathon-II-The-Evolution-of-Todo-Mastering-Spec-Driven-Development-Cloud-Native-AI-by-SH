# Quickstart Guide: Phase V Local Setup

**Estimated Time**: 5 minutes ⏱️
**Prerequisites**: Docker Desktop, Minikube, Helm 3, kubectl, Dapr CLI

---

## 🚀 One-Command Setup

```bash
# Clone repository and run setup script
git clone <repo-url> && cd phase5
./scripts/quickstart.sh
```

**What it does**:
1. Starts Minikube cluster (4 CPUs, 8GB RAM)
2. Installs Dapr runtime (1.12+)
3. Deploys Redpanda (Kafka)
4. Deploys PostgreSQL
5. Installs Phase V Helm chart
6. Runs database migrations
7. Waits for all pods to be ready
8. Opens frontend in browser

---

## 📋 Manual Setup (Step-by-Step)

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster
kubectl cluster-info
```

---

### Step 2: Install Dapr

```bash
# Install Dapr runtime in Kubernetes
dapr init --kubernetes --wait

# Verify installation
dapr status -k

# Expected output:
#   NAME                   NAMESPACE    HEALTHY  STATUS   VERSION  AGE
#   dapr-sidecar-injector  dapr-system  True     Running  1.12.0   1m
#   dapr-sentry            dapr-system  True     Running  1.12.0   1m
#   dapr-operator          dapr-system  True     Running  1.12.0   1m
#   dapr-placement         dapr-system  True     Running  1.12.0   1m
```

---

### Step 3: Deploy Infrastructure (Kafka + PostgreSQL)

```bash
# Create namespace
kubectl create namespace phase5

# Install Redpanda (Kafka)
helm repo add redpanda https://charts.redpanda.com/
helm install redpanda redpanda/redpanda \
  --namespace phase5 \
  --set statefulset.replicas=3 \
  --set resources.cpu.cores=1 \
  --set resources.memory.container.max=2Gi \
  --wait --timeout=5m

# Install PostgreSQL
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres bitnami/postgresql \
  --namespace phase5 \
  --set auth.username=phase5_user \
  --set auth.password=phase5_pass \
  --set auth.database=phase5_db \
  --set primary.resources.limits.memory=1Gi \
  --wait --timeout=3m

# Verify infrastructure
kubectl get pods -n phase5
# Expected: 3 redpanda pods + 1 postgres pod (all Running)
```

---

### Step 4: Deploy Phase V Application

```bash
# Navigate to Helm chart directory
cd helm/phase5

# Install application
helm install phase5 . \
  --namespace phase5 \
  --create-namespace \
  --wait --timeout=10m

# Verify deployment
kubectl get pods -n phase5

# Expected pods (all Running):
# - frontend-xxx
# - chat-api-xxx
# - notification-service-xxx
# - recurring-task-service-xxx
# - audit-service-xxx
# - websocket-sync-service-xxx
# - postgres-0
# - redpanda-0, redpanda-1, redpanda-2
```

---

### Step 5: Run Database Migrations

```bash
# Port-forward PostgreSQL
kubectl port-forward -n phase5 svc/postgres 5432:5432 &

# Run migrations (from each service directory)
cd services/chat-api
alembic upgrade head

cd ../notification-service
alembic upgrade head

cd ../recurring-task-service
alembic upgrade head

cd ../audit-service
alembic upgrade head

# Stop port-forward
fg  # Bring to foreground
# Press Ctrl+C
```

---

### Step 6: Access Application

```bash
# Get Minikube IP
minikube ip
# Example output: 192.168.49.2

# Port-forward frontend (temporary)
kubectl port-forward -n phase5 svc/frontend 3000:3000

# Open browser
http://localhost:3000
```

**Or use Ingress** (if configured):
```bash
# Add to /etc/hosts (Windows: C:\Windows\System32\drivers\etc\hosts)
192.168.49.2 phase5.local

# Access application
http://phase5.local
```

---

## 🧪 Verify Installation

### Check All Pods

```bash
kubectl get pods -n phase5 -o wide

# All pods should show STATUS=Running and READY=2/2 (app + dapr sidecar)
```

---

### Test API Endpoints

```bash
# Health check (chat-api)
kubectl port-forward -n phase5 svc/chat-api 8000:8000 &
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status": "healthy", "checks": {"database": "ok", "kafka": "ok", "dapr": "ok"}}
```

---

### Test Event Flow

```bash
# Create a task via API
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "priority": "high",
    "due_date": "2026-02-10T18:00:00Z",
    "tags": ["test"]
  }'

# Check Kafka topic for event
kubectl exec -n phase5 redpanda-0 -- rpk topic consume task-events --num 1

# Expected: CloudEvents-formatted task.created event
```

---

### Test WebSocket Sync

```bash
# Port-forward WebSocket service
kubectl port-forward -n phase5 svc/websocket-sync-service 8080:8080 &

# Connect with wscat
npm install -g wscat
wscat -c ws://localhost:8080/ws?token=<jwt-token>

# Create a task in browser → should see real-time update in wscat
```

---

### Check Dapr Components

```bash
# List Dapr components
kubectl get components -n phase5

# Expected:
# - pubsub-kafka
# - statestore-postgresql
# - secretstore-kubernetes
# - cron-recurring-tasks
# - cron-reminders

# Check component health
dapr components -k -n phase5
```

---

### View Logs

```bash
# Chat API logs (application container)
kubectl logs -n phase5 -l app=chat-api -c chat-api --tail=50 -f

# Chat API logs (Dapr sidecar)
kubectl logs -n phase5 -l app=chat-api -c daprd --tail=50 -f

# All services logs (combined)
kubectl logs -n phase5 -l tier=backend --all-containers --tail=50 -f
```

---

### Monitor Metrics (optional)

```bash
# Install Prometheus + Grafana (if monitoring enabled)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --wait

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3001:80
# Open http://localhost:3001 (admin/prom-operator)
```

---

## 🛑 Stop and Clean Up

```bash
# Uninstall Phase V
helm uninstall phase5 -n phase5

# Uninstall infrastructure
helm uninstall redpanda -n phase5
helm uninstall postgres -n phase5

# Uninstall Dapr
dapr uninstall --kubernetes

# Stop Minikube
minikube stop

# Delete Minikube (if needed)
minikube delete
```

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod -n phase5 <pod-name>

# Check events
kubectl get events -n phase5 --sort-by='.lastTimestamp'

# Common issues:
# - Insufficient resources → increase Minikube CPUs/RAM
# - Image pull errors → check image registry/tags
# - Dapr sidecar not injected → verify namespace annotation
```

---

### Database Connection Errors

```bash
# Verify PostgreSQL secret
kubectl get secret -n phase5 postgres-secret -o yaml

# Test database connection
kubectl run -n phase5 -it --rm psql-test --image=postgres:15 --restart=Never -- \
  psql postgresql://phase5_user:phase5_pass@postgres:5432/phase5_db -c '\l'

# Expected: List of databases including phase5_db
```

---

### Kafka Events Not Flowing

```bash
# Check Redpanda health
kubectl exec -n phase5 redpanda-0 -- rpk cluster health

# List topics
kubectl exec -n phase5 redpanda-0 -- rpk topic list

# Expected: task-events, reminders, task-updates

# Check consumer groups
kubectl exec -n phase5 redpanda-0 -- rpk group list
```

---

### Dapr Sidecar Issues

```bash
# Verify Dapr injection annotation
kubectl get deployment -n phase5 chat-api -o jsonpath='{.spec.template.metadata.annotations}'

# Expected: dapr.io/enabled="true"

# Check Dapr logs
kubectl logs -n phase5 -l app=chat-api -c daprd --tail=100

# Restart deployment (if needed)
kubectl rollout restart deployment/chat-api -n phase5
```

---

## 📚 Next Steps

After successful setup:

1. **Explore Features**:
   - Create recurring tasks (daily standup, weekly review)
   - Set due dates and test reminders
   - Add tags and test full-text search
   - Test priority filtering and smart sorting

2. **Test Event Flow**:
   - Monitor Kafka topics (`rpk topic consume`)
   - Check audit logs in database
   - Verify WebSocket real-time sync

3. **Load Testing**:
   - Use `k6` or `ab` to test API performance
   - Verify HPA scaling (if enabled)
   - Monitor Prometheus metrics

4. **Cloud Deployment**:
   - Follow `docs/cloud-deployment.md` for AKS/GKE/OKE
   - Use Strimzi instead of Redpanda
   - Enable TLS/HTTPS with cert-manager

---

## 📖 Documentation

- **Architecture**: `specs/001-cloud-native-kafka-dapr/plan.md`
- **API Reference**: `specs/001-cloud-native-kafka-dapr/contracts/api-chat-service.yaml`
- **Event Schemas**: `specs/001-cloud-native-kafka-dapr/contracts/kafka-events.yaml`
- **Dapr Components**: `specs/001-cloud-native-kafka-dapr/contracts/dapr-components.yaml`
- **Data Model**: `specs/001-cloud-native-kafka-dapr/data-model.md`

---

## ✅ Success Checklist

- [ ] Minikube cluster running
- [ ] Dapr runtime installed (`dapr status -k` shows all healthy)
- [ ] Redpanda (3 pods) and PostgreSQL (1 pod) running
- [ ] All 6 Phase V services deployed (each with 2/2 containers: app + dapr)
- [ ] Database migrations completed
- [ ] Frontend accessible in browser
- [ ] API health check returns `{"status": "healthy"}`
- [ ] Task creation publishes event to Kafka (`task-events` topic)
- [ ] WebSocket receives real-time task updates
- [ ] Dapr components operational (`kubectl get components -n phase5`)

**Estimated Total Time**: ⏱️ **5-10 minutes** (depending on internet speed for image pulls)

---

🎉 **You're ready to demo Phase V!** 🎉
