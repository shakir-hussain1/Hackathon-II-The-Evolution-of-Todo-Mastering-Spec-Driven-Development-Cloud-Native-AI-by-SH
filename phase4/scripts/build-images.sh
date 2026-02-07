#!/bin/bash
# Build Docker images for Todo App (Frontend + Backend)
# This script builds images and loads them into Minikube

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Building Todo App Docker Images${NC}"
echo -e "${GREEN}========================================${NC}"

# Navigate to project root
cd "$(dirname "$0")/../.."

# Check if Minikube is running
echo -e "\n${YELLOW}Checking Minikube status...${NC}"
if ! minikube status > /dev/null 2>&1; then
    echo -e "${RED}Error: Minikube is not running. Please start it with 'minikube start'${NC}"
    exit 1
fi

# Use Minikube's Docker daemon
echo -e "\n${YELLOW}Configuring Docker to use Minikube's daemon...${NC}"
eval $(minikube docker-env)

# Build Backend Image
echo -e "\n${YELLOW}Building Backend Image (FastAPI)...${NC}"
docker build \
    -f phase4/docker/backend.Dockerfile \
    -t todo-backend:latest \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend image built successfully${NC}"
else
    echo -e "${RED}✗ Backend image build failed${NC}"
    exit 1
fi

# Build Frontend Image
echo -e "\n${YELLOW}Building Frontend Image (Next.js)...${NC}"
docker build \
    -f phase4/docker/frontend.Dockerfile \
    -t todo-frontend:latest \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend image built successfully${NC}"
else
    echo -e "${RED}✗ Frontend image build failed${NC}"
    exit 1
fi

# List built images
echo -e "\n${GREEN}Built images:${NC}"
docker images | grep -E "todo-(backend|frontend)"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Image build completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Deploy to Minikube: ${GREEN}./phase4/scripts/deploy.sh${NC}"
echo -e "2. Or manually install with Helm: ${GREEN}cd phase4/helm && helm install todo-app ./todo-app${NC}"
