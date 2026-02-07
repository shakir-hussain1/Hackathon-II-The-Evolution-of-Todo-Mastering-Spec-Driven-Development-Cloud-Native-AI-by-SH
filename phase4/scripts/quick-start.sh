#!/bin/bash
# Quick start script for Todo App deployment

set -e

echo "=========================================="
echo "Todo App - Quick Deployment"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Start Minikube
echo -e "${GREEN}[1/6]${NC} Starting Minikube cluster..."
minikube status | grep -q "host: Running" && echo "Minikube already running" || minikube start --driver=docker --cpus=4 --memory=8192

# Configure environment
echo -e "${GREEN}[2/6]${NC} Configuring environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file and add OPENAI_API_KEY${NC}"
    read -p "Press Enter after editing .env file..."
fi

# Use Minikube Docker
echo -e "${GREEN}[3/6]${NC} Using Minikube Docker daemon..."
eval $(minikube docker-env)

# Build images
echo -e "${GREEN}[4/6]${NC} Building Docker images (this may take 5-10 minutes)..."
echo "Building backend..."
docker build -t todo-backend:latest -f docker/backend.Dockerfile ../phase3/backend/
echo "Building frontend..."
docker build -t todo-frontend:latest -f docker/frontend.Dockerfile ../phase3/frontend/

# Create secrets
echo -e "${GREEN}[5/6]${NC} Creating Kubernetes secrets..."
kubectl create secret generic todo-app-secrets \
  --from-env-file=.env \
  --dry-run=client -o yaml | kubectl apply -f -

# Deploy with Helm
echo -e "${GREEN}[6/6]${NC} Deploying with Helm..."
helm upgrade --install todo-app ./helm/todo-app \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest \
  --set backend.image.pullPolicy=Never \
  --set frontend.image.pullPolicy=Never

# Wait for pods
echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=Ready pods --all --timeout=300s || true

# Show status
echo ""
echo "=========================================="
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo "=========================================="
echo ""

# Get URL
echo "Frontend URL:"
minikube service todo-app-frontend --url

echo ""
echo "To view backend API docs, run:"
echo "  kubectl port-forward svc/todo-app-backend 8000:8000"
echo "  Then open: http://localhost:8000/docs"
echo ""
echo "To view logs:"
echo "  kubectl logs -f deployment/todo-app-backend"
echo "  kubectl logs -f deployment/todo-app-frontend"
echo ""
echo "To check pod status:"
echo "  kubectl get pods"
echo ""
