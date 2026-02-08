#!/bin/bash
# Deploy Phase 5 to Oracle OKE

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Phase 5 - Oracle OKE Deployment${NC}"
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

if ! command -v oci &> /dev/null; then
    echo -e "${RED}OCI CLI not found. Please install Oracle Cloud CLI.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"

# Get configuration from user
read -p "Enter OCI tenancy namespace: " OCI_TENANCY
read -p "Enter OCI region (e.g., iad): " OCI_REGION
read -p "Enter domain for application (e.g., phase5.oraclecloud.com): " APP_DOMAIN

# Check if kubectl is configured for OKE
echo -e "\n${YELLOW}Checking OKE cluster connection...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}kubectl not connected to OKE cluster.${NC}"
    echo -e "${YELLOW}Please configure kubectl for your OKE cluster first.${NC}"
    echo -e "Example: oci ce cluster create-kubeconfig --cluster-id <cluster-ocid>"
    exit 1
fi

echo -e "${GREEN}✓ Connected to cluster: $(kubectl config current-context)${NC}"

# Check/Install Dapr
echo -e "\n${YELLOW}Checking Dapr installation...${NC}"
if ! kubectl get namespace dapr-system &> /dev/null; then
    echo -e "${YELLOW}Installing Dapr on OKE...${NC}"
    helm repo add dapr https://dapr.github.io/helm-charts/
    helm repo update
    helm upgrade --install dapr dapr/dapr \
        --version=1.12 \
        --namespace dapr-system \
        --create-namespace \
        --wait
    echo -e "${GREEN}✓ Dapr installed${NC}"
else
    echo -e "${GREEN}✓ Dapr already installed${NC}"
fi

# Check/Install NGINX Ingress
echo -e "\n${YELLOW}Checking NGINX Ingress Controller...${NC}"
if ! kubectl get namespace ingress-nginx &> /dev/null; then
    echo -e "${YELLOW}Installing NGINX Ingress Controller...${NC}"
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx \
        --namespace ingress-nginx \
        --create-namespace \
        --set controller.service.type=LoadBalancer \
        --wait
    echo -e "${GREEN}✓ NGINX Ingress installed${NC}"
else
    echo -e "${GREEN}✓ NGINX Ingress already installed${NC}"
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

# Create OCIR pull secret
echo -e "\n${YELLOW}Creating OCIR pull secret...${NC}"
read -p "Enter OCI username (tenancy-namespace/username): " OCI_USERNAME
read -sp "Enter OCI auth token: " OCI_AUTH_TOKEN
echo

kubectl create secret docker-registry ocir-secret \
    --docker-server="${OCI_REGION}.ocir.io" \
    --docker-username="${OCI_USERNAME}" \
    --docker-password="${OCI_AUTH_TOKEN}" \
    --namespace phase5 \
    --dry-run=client -o yaml | kubectl apply -f -

echo -e "${GREEN}✓ OCIR secret created${NC}"

# Create application secrets
echo -e "\n${YELLOW}Creating application secrets...${NC}"

POSTGRES_PASS=$(openssl rand -base64 32)
echo "Generated PostgreSQL password: $POSTGRES_PASS"

JWT_SECRET=$(openssl rand -base64 32)
echo "Generated JWT secret: $JWT_SECRET"

read -p "Enter OpenAI API key: " OPENAI_KEY

# Store in Kubernetes secrets
kubectl create secret generic postgres-secret \
    --from-literal=password="$POSTGRES_PASS" \
    --namespace phase5 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic jwt-secret \
    --from-literal=secret="$JWT_SECRET" \
    --namespace phase5 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic openai-secret \
    --from-literal=api-key="$OPENAI_KEY" \
    --namespace phase5 \
    --dry-run=client -o yaml | kubectl apply -f -

echo -e "${GREEN}✓ Application secrets created${NC}"

# Install chart
echo -e "\n${YELLOW}Installing Phase 5 chart...${NC}"
helm upgrade --install phase5 ./phase5 \
    --namespace phase5 \
    -f ./phase5/values-oke.yaml \
    --set global.imageRegistry="${OCI_REGION}.ocir.io/${OCI_TENANCY}" \
    --set global.domain="${APP_DOMAIN}" \
    --set postgresql.auth.existingSecret="postgres-secret" \
    --wait \
    --timeout 15m

echo -e "${GREEN}✓ Chart installed${NC}"

# Wait for pods
echo -e "\n${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=phase5 -n phase5 --timeout=10m || true

# Show status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}Pod Status:${NC}"
kubectl get pods -n phase5

echo -e "\n${YELLOW}Services:${NC}"
kubectl get svc -n phase5

echo -e "\n${YELLOW}Ingress:${NC}"
kubectl get ingress -n phase5

# Get Load Balancer IP
echo -e "\n${YELLOW}Getting Load Balancer IP...${NC}"
LB_IP=$(kubectl get svc -n ingress-nginx nginx-ingress-ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo -e "Load Balancer IP: ${GREEN}${LB_IP}${NC}"

echo -e "\n${YELLOW}DNS Configuration:${NC}"
echo -e "Create an A record for ${GREEN}${APP_DOMAIN}${NC} pointing to ${GREEN}${LB_IP}${NC}"
echo -e "Or add to /etc/hosts for testing:"
echo -e "${GREEN}echo \"${LB_IP} ${APP_DOMAIN}\" | sudo tee -a /etc/hosts${NC}"

echo -e "\n${YELLOW}Access the application:${NC}"
echo -e "Frontend: ${GREEN}https://${APP_DOMAIN}${NC}"
echo -e "API: ${GREEN}https://api.${APP_DOMAIN}${NC}"

echo -e "\n${YELLOW}View logs:${NC}"
echo -e "${GREEN}kubectl logs -n phase5 -l app.kubernetes.io/instance=phase5 -f --all-containers=true${NC}"

echo -e "\n${YELLOW}Monitoring:${NC}"
echo -e "Dapr Dashboard: ${GREEN}dapr dashboard -k -p 9999${NC}"

echo -e "\n${YELLOW}Credentials stored in:${NC}"
echo -e "PostgreSQL: kubectl get secret postgres-secret -n phase5"
echo -e "JWT: kubectl get secret jwt-secret -n phase5"
echo -e "OpenAI: kubectl get secret openai-secret -n phase5"

echo -e "\n${YELLOW}Uninstall:${NC}"
echo -e "${GREEN}helm uninstall phase5 -n phase5${NC}"
