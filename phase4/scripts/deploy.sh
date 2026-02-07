#!/bin/bash
# Deploy Todo App to Minikube using Helm
# This script handles secrets, builds images, and deploys the Helm chart

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying Todo App to Minikube${NC}"
echo -e "${GREEN}========================================${NC}"

# Navigate to project root
SCRIPT_DIR="$(dirname "$0")"
cd "$SCRIPT_DIR/../.."

# Configuration
RELEASE_NAME="todo-app"
NAMESPACE="default"
HELM_CHART_PATH="phase4/helm/todo-app"

# Check if Minikube is running
echo -e "\n${YELLOW}Checking Minikube status...${NC}"
if ! minikube status > /dev/null 2>&1; then
    echo -e "${RED}Error: Minikube is not running. Please start it with 'minikube start'${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Minikube is running${NC}"

# Check for required secrets
echo -e "\n${YELLOW}Checking for required environment variables...${NC}"

# Load secrets from .env file if it exists
if [ -f "phase4/.env" ]; then
    echo -e "${BLUE}Loading secrets from phase4/.env${NC}"
    source phase4/.env
elif [ -f "phase3/backend/.env" ]; then
    echo -e "${BLUE}Loading secrets from phase3/backend/.env${NC}"
    source phase3/backend/.env
fi

# Validate secrets
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}Error: OPENAI_API_KEY not set${NC}"
    echo -e "${YELLOW}Please set it in phase4/.env or export it as an environment variable${NC}"
    exit 1
fi

if [ -z "$JWT_SECRET" ]; then
    echo -e "${YELLOW}Warning: JWT_SECRET not set. Generating a random one...${NC}"
    JWT_SECRET=$(openssl rand -hex 32)
    echo -e "${GREEN}Generated JWT_SECRET: $JWT_SECRET${NC}"
fi

echo -e "${GREEN}✓ Required secrets validated${NC}"

# Build Docker images
echo -e "\n${YELLOW}Building Docker images...${NC}"
bash "$SCRIPT_DIR/build-images.sh"

# Check if release already exists
echo -e "\n${YELLOW}Checking for existing deployment...${NC}"
if helm list -n "$NAMESPACE" | grep -q "^$RELEASE_NAME"; then
    echo -e "${BLUE}Existing deployment found. Upgrading...${NC}"
    HELM_COMMAND="upgrade"
else
    echo -e "${BLUE}No existing deployment. Installing...${NC}"
    HELM_COMMAND="install"
fi

# Deploy with Helm
echo -e "\n${YELLOW}Deploying with Helm...${NC}"
helm $HELM_COMMAND "$RELEASE_NAME" "$HELM_CHART_PATH" \
    --namespace "$NAMESPACE" \
    --set secrets.openaiApiKey="$OPENAI_API_KEY" \
    --set secrets.jwtSecret="$JWT_SECRET" \
    --wait \
    --timeout 5m

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Deployment successful!${NC}"
else
    echo -e "\n${RED}✗ Deployment failed${NC}"
    exit 1
fi

# Wait for pods to be ready
echo -e "\n${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod \
    -l app.kubernetes.io/instance=$RELEASE_NAME \
    -n $NAMESPACE \
    --timeout=300s

# Display deployment status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Status${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${BLUE}Pods:${NC}"
kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME

echo -e "\n${BLUE}Services:${NC}"
kubectl get services -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME

echo -e "\n${BLUE}Ingress:${NC}"
kubectl get ingress -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME 2>/dev/null || echo "No ingress configured"

# Get access URLs
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Access Information${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Frontend:${NC}"
FRONTEND_URL=$(minikube service $RELEASE_NAME-frontend -n $NAMESPACE --url 2>/dev/null)
if [ -n "$FRONTEND_URL" ]; then
    echo -e "${GREEN}URL: $FRONTEND_URL${NC}"
else
    echo -e "${YELLOW}Run: minikube service $RELEASE_NAME-frontend --url${NC}"
fi

echo -e "\n${YELLOW}Backend API:${NC}"
echo -e "${BLUE}Port-forward command:${NC}"
echo -e "kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-backend 8000:8000"
echo -e "\n${BLUE}Then access:${NC}"
echo -e "API: ${GREEN}http://localhost:8000${NC}"
echo -e "Docs: ${GREEN}http://localhost:8000/docs${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Useful commands:${NC}"
echo -e "View logs (backend): ${BLUE}kubectl logs -n $NAMESPACE -l app.kubernetes.io/component=backend -f${NC}"
echo -e "View logs (frontend): ${BLUE}kubectl logs -n $NAMESPACE -l app.kubernetes.io/component=frontend -f${NC}"
echo -e "Uninstall: ${BLUE}helm uninstall $RELEASE_NAME -n $NAMESPACE${NC}"
echo -e "Restart pods: ${BLUE}kubectl rollout restart deployment -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME${NC}"
