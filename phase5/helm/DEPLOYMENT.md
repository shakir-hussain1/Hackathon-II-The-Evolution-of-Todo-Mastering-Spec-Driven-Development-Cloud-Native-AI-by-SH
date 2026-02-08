# Phase 5 Deployment Guide

Complete guide for deploying Phase 5 to Oracle OKE or local Kubernetes.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Building Docker Images](#building-docker-images)
3. [Local Deployment](#local-deployment)
4. [Oracle OKE Deployment](#oracle-oke-deployment)
5. [Validation](#validation)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

1. **kubectl** (v1.24+)
   ```bash
   kubectl version --client
   ```

2. **Helm** (v3.8+)
   ```bash
   helm version
   ```

3. **Dapr CLI** (v1.12+)
   ```bash
   dapr version
   ```

4. **Docker** (for building images)
   ```bash
   docker version
   ```

5. **For OKE: Oracle Cloud CLI**
   ```bash
   oci --version
   ```

### Kubernetes Cluster

- **Local**: Minikube, kind, or Docker Desktop with Kubernetes enabled
- **Cloud**: Oracle OKE cluster with at least 3 worker nodes

## Building Docker Images

### 1. Build All Service Images

From the `phase5/` directory:

```bash
# Build services
docker build -t phase5/chat-api:1.0.0 ./services/chat-api
docker build -t phase5/notification-service:1.0.0 ./services/notification-service
docker build -t phase5/recurring-task-service:1.0.0 ./services/recurring-task-service
docker build -t phase5/audit-service:1.0.0 ./services/audit-service
docker build -t phase5/websocket-sync-service:1.0.0 ./services/websocket-sync-service

# Build frontend
docker build -t phase5/frontend:1.0.0 ./frontend
```

### 2. Tag for Registry

#### For Local (Minikube)

```bash
# Load images into Minikube
minikube image load phase5/chat-api:1.0.0
minikube image load phase5/notification-service:1.0.0
minikube image load phase5/recurring-task-service:1.0.0
minikube image load phase5/audit-service:1.0.0
minikube image load phase5/websocket-sync-service:1.0.0
minikube image load phase5/frontend:1.0.0
```

#### For Oracle OKE (OCIR)

```bash
# Login to OCIR
docker login iad.ocir.io -u '<tenancy-namespace>/<username>'

# Tag images
docker tag phase5/chat-api:1.0.0 iad.ocir.io/<tenancy>/phase5/chat-api:1.0.0
docker tag phase5/notification-service:1.0.0 iad.ocir.io/<tenancy>/phase5/notification-service:1.0.0
docker tag phase5/recurring-task-service:1.0.0 iad.ocir.io/<tenancy>/phase5/recurring-task-service:1.0.0
docker tag phase5/audit-service:1.0.0 iad.ocir.io/<tenancy>/phase5/audit-service:1.0.0
docker tag phase5/websocket-sync-service:1.0.0 iad.ocir.io/<tenancy>/phase5/websocket-sync-service:1.0.0
docker tag phase5/frontend:1.0.0 iad.ocir.io/<tenancy>/phase5/frontend:1.0.0

# Push to OCIR
docker push iad.ocir.io/<tenancy>/phase5/chat-api:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/notification-service:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/recurring-task-service:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/audit-service:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/websocket-sync-service:1.0.0
docker push iad.ocir.io/<tenancy>/phase5/frontend:1.0.0
```

## Local Deployment

### Automated Deployment

Use the provided script:

```bash
cd helm
./deploy-local.sh
```

### Manual Deployment

#### 1. Install Dapr

```bash
dapr init -k
```

#### 2. Add Helm Repositories

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

#### 3. Create Namespace

```bash
kubectl create namespace phase5
```

#### 4. Install Phase 5

```bash
helm install phase5 ./phase5 \
  --namespace phase5 \
  --set postgresql.auth.password="secure_password" \
  --set jwtSecret="$(openssl rand -base64 32)" \
  --set openaiApiKey="sk-your-key" \
  --wait
```

#### 5. Access the Application

```bash
# Port forward
kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000

# Open browser
open http://localhost:3000
```

## Oracle OKE Deployment

### Automated Deployment

Use the provided script:

```bash
cd helm
./deploy-oke.sh
```

The script will:
1. Check prerequisites
2. Install Dapr and NGINX Ingress
3. Create OCIR pull secret
4. Generate and store secrets
5. Deploy the application
6. Display access information

### Manual OKE Deployment

#### 1. Configure kubectl for OKE

```bash
oci ce cluster create-kubeconfig \
  --cluster-id <your-cluster-ocid> \
  --file ~/.kube/config \
  --region <your-region> \
  --token-version 2.0.0
```

Test connection:
```bash
kubectl get nodes
```

#### 2. Install Dapr

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm upgrade --install dapr dapr/dapr \
  --version=1.12 \
  --namespace dapr-system \
  --create-namespace \
  --wait
```

Verify:
```bash
kubectl get pods -n dapr-system
```

#### 3. Install NGINX Ingress Controller

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --wait
```

Get Load Balancer IP:
```bash
kubectl get svc -n ingress-nginx nginx-ingress-ingress-nginx-controller
```

#### 4. Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace phase5

# OCIR pull secret
kubectl create secret docker-registry ocir-secret \
  --docker-server=iad.ocir.io \
  --docker-username='<tenancy-namespace>/<username>' \
  --docker-password='<auth-token>' \
  --namespace phase5

# Application secrets
kubectl create secret generic postgres-secret \
  --from-literal=password=$(openssl rand -base64 32) \
  --namespace phase5

kubectl create secret generic jwt-secret \
  --from-literal=secret=$(openssl rand -base64 32) \
  --namespace phase5

kubectl create secret generic openai-secret \
  --from-literal=api-key='sk-your-actual-key' \
  --namespace phase5
```

#### 5. Deploy Application

```bash
helm install phase5 ./phase5 \
  --namespace phase5 \
  -f ./phase5/values-oke.yaml \
  --set global.imageRegistry=iad.ocir.io/<your-tenancy> \
  --set global.domain=phase5.oraclecloud.com \
  --set postgresql.auth.existingSecret=postgres-secret \
  --wait
```

#### 6. Configure DNS

Get the Load Balancer IP:
```bash
LB_IP=$(kubectl get svc -n ingress-nginx nginx-ingress-ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo $LB_IP
```

Create DNS A records:
- `phase5.oraclecloud.com` → `$LB_IP`
- `api.phase5.oraclecloud.com` → `$LB_IP`

Or for testing, add to `/etc/hosts`:
```bash
echo "$LB_IP phase5.oraclecloud.com api.phase5.oraclecloud.com" | sudo tee -a /etc/hosts
```

## Validation

### 1. Check Pod Status

```bash
# All pods should be Running
kubectl get pods -n phase5

# Expected output:
# NAME                                          READY   STATUS    RESTARTS
# phase5-chat-api-xxx                          2/2     Running   0
# phase5-notification-service-xxx              2/2     Running   0
# phase5-recurring-task-service-xxx            2/2     Running   0
# phase5-audit-service-xxx                     2/2     Running   0
# phase5-websocket-sync-service-xxx            2/2     Running   0
# phase5-frontend-xxx                          1/1     Running   0
# phase5-postgresql-0                          1/1     Running   0
# phase5-kafka-0                               1/1     Running   0
```

Note: Services with Dapr sidecars show `2/2` (app + daprd)

### 2. Verify Dapr Components

```bash
kubectl get components -n phase5

# Expected:
# pubsub-kafka
# statestore
# secretstore
# cron-recurring-tasks
# cron-reminders
```

### 3. Check Services

```bash
kubectl get svc -n phase5
```

### 4. Test Health Endpoints

```bash
# Port forward to chat-api
kubectl port-forward -n phase5 svc/phase5-chat-api 8000:8000

# Test health (in another terminal)
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

curl http://localhost:8000/ready
# Should return: {"status": "ready"}
```

### 5. Test Frontend

```bash
# Port forward
kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000

# Open browser
open http://localhost:3000
```

### 6. Check Dapr Sidecar Communication

```bash
# Exec into a pod
kubectl exec -it -n phase5 deployment/phase5-chat-api -c chat-api -- sh

# Test Dapr sidecar (from inside pod)
curl http://localhost:3500/v1.0/healthz

# Test service invocation
curl http://localhost:3500/v1.0/invoke/notification-service/method/health
```

### 7. Verify Kafka Topics

```bash
# Exec into Kafka pod
kubectl exec -it -n phase5 phase5-kafka-0 -- bash

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### 8. Check Logs

```bash
# All services
kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 --all-containers=true --tail=50

# Specific service
kubectl logs -n phase5 -l app.kubernetes.io/name=chat-api -c chat-api -f

# Dapr sidecar
kubectl logs -n phase5 -l app.kubernetes.io/name=chat-api -c daprd -f
```

## Troubleshooting

### Pods Stuck in Pending

```bash
# Check events
kubectl describe pod <pod-name> -n phase5

# Common issues:
# - Insufficient resources
# - PVC not bound
# - Image pull errors
```

### Image Pull Errors

```bash
# Check secret
kubectl get secret ocir-secret -n phase5 -o yaml

# Verify image exists in OCIR
docker pull iad.ocir.io/<tenancy>/phase5/chat-api:1.0.0

# Re-create secret if needed
kubectl delete secret ocir-secret -n phase5
kubectl create secret docker-registry ocir-secret ...
```

### Dapr Sidecar Not Injecting

```bash
# Check Dapr installation
dapr status -k

# Verify namespace has Dapr annotation
kubectl get namespace phase5 -o yaml | grep dapr

# Check pod annotations
kubectl get pod <pod-name> -n phase5 -o yaml | grep dapr.io
```

### Database Connection Issues

```bash
# Check PostgreSQL pod
kubectl get pod -n phase5 -l app.kubernetes.io/name=postgresql

# Test connection
kubectl run -it --rm psql-test --image=postgres:15 --namespace=phase5 -- \
  psql -h phase5-postgresql -U phase5_user -d phase5_db

# Check secret
kubectl get secret postgres-secret -n phase5 -o jsonpath='{.data.password}' | base64 -d
```

### Kafka Connection Issues

```bash
# Check Kafka pods
kubectl get pods -n phase5 -l app.kubernetes.io/name=kafka

# Check Kafka logs
kubectl logs -n phase5 phase5-kafka-0

# Test from inside cluster
kubectl run -it kafka-test --image=bitnami/kafka:latest --namespace=phase5 -- \
  kafka-topics.sh --list --bootstrap-server phase5-kafka:9092
```

### Ingress Not Working

```bash
# Check ingress
kubectl get ingress -n phase5
kubectl describe ingress phase5-ingress -n phase5

# Check NGINX Ingress Controller
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Test from inside cluster
kubectl run -it curl-test --image=curlimages/curl --namespace=phase5 -- \
  curl http://phase5-frontend:3000
```

### View All Events

```bash
kubectl get events -n phase5 --sort-by='.lastTimestamp'
```

## Monitoring and Observability

### Dapr Dashboard

```bash
dapr dashboard -k -p 9999
# Open http://localhost:9999
```

### Metrics

```bash
# Port forward to any service's Dapr sidecar
kubectl port-forward -n phase5 <pod-name> 9090:9090

# Scrape metrics
curl http://localhost:9090/metrics
```

### Distributed Tracing

If Zipkin is deployed:

```bash
# Port forward to Zipkin
kubectl port-forward -n default svc/zipkin 9411:9411

# Open UI
open http://localhost:9411
```

## Cleanup

### Remove Application

```bash
helm uninstall phase5 -n phase5
```

### Remove Namespace and PVCs

```bash
# Delete namespace (includes all resources)
kubectl delete namespace phase5

# Or keep namespace but delete PVCs
kubectl delete pvc -n phase5 --all
```

### Remove Infrastructure

```bash
# Remove NGINX Ingress
helm uninstall nginx-ingress -n ingress-nginx
kubectl delete namespace ingress-nginx

# Remove Dapr
helm uninstall dapr -n dapr-system
kubectl delete namespace dapr-system
```

## Advanced Configuration

### Custom Values

Create a custom `values-custom.yaml`:

```yaml
global:
  domain: my-custom-domain.com

chat-api:
  replicaCount: 5
  resources:
    limits:
      memory: 1Gi

postgresql:
  primary:
    persistence:
      size: 100Gi
```

Deploy with custom values:

```bash
helm install phase5 ./phase5 \
  -f ./phase5/values-oke.yaml \
  -f ./values-custom.yaml \
  --namespace phase5
```

### Enable Resource Quotas

```bash
kubectl create quota phase5-quota \
  --hard=cpu=10,memory=20Gi,pods=50 \
  --namespace=phase5
```

### Enable Network Policies

Create `network-policy.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: phase5-network-policy
  namespace: phase5
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: phase5
  egress:
  - to:
    - namespaceSelector: {}
```

Apply:
```bash
kubectl apply -f network-policy.yaml
```

## Production Checklist

- [ ] All secrets are externally managed (not in values files)
- [ ] TLS certificates are configured
- [ ] Resource limits are set appropriately
- [ ] Autoscaling is enabled and tested
- [ ] Backup strategy for PostgreSQL is in place
- [ ] Monitoring and alerting are configured
- [ ] Network policies are applied
- [ ] RBAC is configured
- [ ] Images are scanned for vulnerabilities
- [ ] DNS is properly configured
- [ ] Load balancer health checks are passing

## Support

For issues, check:
1. Pod logs: `kubectl logs -n phase5 <pod-name> -c <container-name>`
2. Events: `kubectl get events -n phase5`
3. Dapr status: `dapr status -k`
4. Component status: `kubectl get components -n phase5`
