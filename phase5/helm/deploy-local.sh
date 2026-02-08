#!/bin/bash
# Deploy Phase 5 to local Kubernetes (Minikube/kind/Docker Desktop)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Phase 5 - Local Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Check prerequisites
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl not found. Please install kubectl.${NC}"
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo -e "${RED}helm not found. Please install Helm 3.${NC}"
    exit 1
fi

if ! command -v dapr &> /dev/null; then
    echo -e "${RED}dapr CLI not found. Please install Dapr CLI.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"

# Check if Dapr is initialized in cluster
echo -e "\n${YELLOW}Checking Dapr installation...${NC}"
if ! kubectl get namespace dapr-system &> /dev/null; then
    echo -e "${YELLOW}Dapr not found. Installing Dapr...${NC}"
    dapr init -k
    echo -e "${GREEN}✓ Dapr installed${NC}"
else
    echo -e "${GREEN}✓ Dapr already installed${NC}"
fi

# Add Bitnami repo
echo -e "\n${YELLOW}Adding Helm repositories...${NC}"
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
echo -e "${GREEN}✓ Helm repos updated${NC}"

# Create namespace
echo -e "\n${YELLOW}Creating namespace...${NC}"
kubectl create namespace phase5 --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespace created${NC}"

# Get secrets from user
echo -e "\n${YELLOW}Setting up secrets...${NC}"
read -sp "Enter PostgreSQL password (or press Enter for default 'phase5_pass'): " POSTGRES_PASS
echo
POSTGRES_PASS=${POSTGRES_PASS:-phase5_pass}

read -sp "Enter JWT secret (or press Enter to generate): " JWT_SECRET
echo
if [ -z "$JWT_SECRET" ]; then
    JWT_SECRET=$(openssl rand -base64 32)
    echo "Generated JWT secret: $JWT_SECRET"
fi

read -p "Enter OpenAI API key (or press Enter to skip): " OPENAI_KEY
OPENAI_KEY=${OPENAI_KEY:-REPLACE_ME_WITH_ACTUAL_OPENAI_API_KEY}

# Install chart
echo -e "\n${YELLOW}Installing Phase 5 chart...${NC}"
helm upgrade --install phase5 ./phase5 \
    --namespace phase5 \
    --set postgresql.auth.password="$POSTGRES_PASS" \
    --set jwtSecret="$JWT_SECRET" \
    --set openaiApiKey="$OPENAI_KEY" \
    --set global.domain="phase5.local" \
    --wait \
    --timeout 10m

echo -e "${GREEN}✓ Chart installed${NC}"

# Wait for pods
echo -e "\n${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=phase5 -n phase5 --timeout=5m

# Show status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Pod Status:${NC}"
kubectl get pods -n phase5

echo -e "\n${YELLOW}Services:${NC}"
kubectl get svc -n phase5

echo -e "\n${YELLOW}Access the application:${NC}"
echo -e "Frontend: ${GREEN}kubectl port-forward -n phase5 svc/phase5-frontend 3000:3000${NC}"
echo -e "Then open: ${GREEN}http://localhost:3000${NC}"

echo -e "\n${YELLOW}View logs:${NC}"
echo -e "${GREEN}kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f --all-containers=true${NC}"

echo -e "\n${YELLOW}Uninstall:${NC}"
echo -e "${GREEN}helm uninstall phase5 -n phase5${NC}"
