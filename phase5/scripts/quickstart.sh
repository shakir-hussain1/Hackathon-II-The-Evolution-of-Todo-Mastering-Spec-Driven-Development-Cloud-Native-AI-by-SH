#!/bin/bash
# Phase V Quickstart Script - 5-Minute Setup
# Based on quickstart.md

set -e  # Exit on error

echo "🚀 Phase V Quickstart - Advanced Cloud-Native Todo System"
echo "=========================================================="
echo ""

# Step 1: Start Minikube
echo "📦 Step 1: Starting Minikube cluster (4 CPUs, 8GB RAM)..."
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable addons
echo "🔧 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster
echo "✅ Verifying cluster..."
kubectl cluster-info

echo ""

# Step 2: Install Dapr
echo "📦 Step 2: Installing Dapr runtime (1.12+)..."
dapr init --kubernetes --wait

# Verify Dapr installation
echo "✅ Verifying Dapr installation..."
dapr status -k

echo ""

# Step 3: Deploy Infrastructure
echo "📦 Step 3: Deploying infrastructure (Kafka + PostgreSQL)..."

# Create namespace
kubectl create namespace phase5 || echo "Namespace phase5 already exists"

# Install Redpanda (Kafka)
echo "🔧 Installing Redpanda (Kafka)..."
helm repo add redpanda https://charts.redpanda.com/ || true
helm repo update
helm install redpanda redpanda/redpanda \
  --namespace phase5 \
  --set statefulset.replicas=3 \
  --set resources.cpu.cores=1 \
  --set resources.memory.container.max=2Gi \
  --wait --timeout=5m || echo "Redpanda already installed"

# Install PostgreSQL
echo "🔧 Installing PostgreSQL..."
helm repo add bitnami https://charts.bitnami.com/bitnami || true
helm repo update
helm install postgres bitnami/postgresql \
  --namespace phase5 \
  --set auth.username=phase5_user \
  --set auth.password=phase5_pass \
  --set auth.database=phase5_db \
  --set primary.resources.limits.memory=1Gi \
  --wait --timeout=3m || echo "PostgreSQL already installed"

# Verify infrastructure
echo "✅ Verifying infrastructure pods..."
kubectl get pods -n phase5

echo ""

# Step 4: Create Kafka Topics
echo "📦 Step 4: Creating Kafka topics..."
echo "Waiting for Redpanda pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=redpanda -n phase5 --timeout=300s

kubectl exec -n phase5 redpanda-0 -- rpk topic create task-events --partitions 3 --replicas 3 || echo "Topic task-events already exists"
kubectl exec -n phase5 redpanda-0 -- rpk topic create reminders --partitions 3 --replicas 3 || echo "Topic reminders already exists"
kubectl exec -n phase5 redpanda-0 -- rpk topic create task-updates --partitions 3 --replicas 3 || echo "Topic task-updates already exists"

# Verify topics
echo "✅ Verifying Kafka topics..."
kubectl exec -n phase5 redpanda-0 -- rpk topic list

echo ""

# Step 5: Deploy Dapr Components
echo "📦 Step 5: Deploying Dapr components..."
if [ -d "../helm/phase5/components" ]; then
  kubectl apply -f ../helm/phase5/components/ -n phase5 || echo "Dapr components already applied or not found"
else
  echo "⚠️  Dapr components directory not found. Skipping..."
fi

echo ""

# Step 6: Deploy Phase V Application (if Helm chart exists)
echo "📦 Step 6: Deploying Phase V application..."
if [ -f "../helm/phase5/Chart.yaml" ]; then
  helm install phase5 ../helm/phase5/ \
    --namespace phase5 \
    --create-namespace \
    --wait --timeout=10m || echo "Phase V application already installed"
else
  echo "⚠️  Helm chart not found. Skipping application deployment..."
  echo "Run 'helm install phase5 ./helm/phase5/ -n phase5' manually after chart is ready"
fi

echo ""

# Final status
echo "🎉 Quickstart Complete!"
echo "========================"
echo ""
echo "✅ Minikube cluster: Running"
echo "✅ Dapr runtime: Installed"
echo "✅ Redpanda (Kafka): 3 replicas"
echo "✅ PostgreSQL: Ready"
echo "✅ Kafka topics: task-events, reminders, task-updates"
echo ""
echo "📊 Check status:"
echo "  kubectl get pods -n phase5"
echo "  kubectl get components -n phase5"
echo "  dapr status -k"
echo ""
echo "🔗 Access services:"
echo "  Minikube IP: $(minikube ip)"
echo "  Frontend: kubectl port-forward -n phase5 svc/frontend 3000:3000"
echo "  Chat API: kubectl port-forward -n phase5 svc/chat-api 8000:8000"
echo ""
echo "📚 Next steps:"
echo "  1. Run database migrations"
echo "  2. Deploy application services"
echo "  3. Access frontend at http://localhost:3000"
echo ""
