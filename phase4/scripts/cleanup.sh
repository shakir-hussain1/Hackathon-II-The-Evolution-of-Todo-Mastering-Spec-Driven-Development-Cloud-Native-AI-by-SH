#!/bin/bash
# Cleanup script to remove Todo App deployment from Minikube

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Cleaning up Todo App deployment${NC}"
echo -e "${YELLOW}========================================${NC}"

# Configuration
RELEASE_NAME="todo-app"
NAMESPACE="default"

# Check if release exists
if ! helm list -n "$NAMESPACE" | grep -q "^$RELEASE_NAME"; then
    echo -e "${YELLOW}No deployment found with name: $RELEASE_NAME${NC}"
    exit 0
fi

# Confirm deletion
echo -e "\n${RED}This will delete the Todo App deployment and all associated resources.${NC}"
read -p "Are you sure you want to continue? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Cleanup cancelled${NC}"
    exit 0
fi

# Uninstall Helm release
echo -e "\n${YELLOW}Uninstalling Helm release...${NC}"
helm uninstall "$RELEASE_NAME" -n "$NAMESPACE"

# Wait for resources to be deleted
echo -e "\n${YELLOW}Waiting for resources to be deleted...${NC}"
sleep 5

# Delete PVCs if they still exist
echo -e "\n${YELLOW}Checking for remaining PVCs...${NC}"
PVC_NAME="${RELEASE_NAME}-backend-pvc"
if kubectl get pvc "$PVC_NAME" -n "$NAMESPACE" > /dev/null 2>&1; then
    echo -e "${YELLOW}Deleting PVC: $PVC_NAME${NC}"
    kubectl delete pvc "$PVC_NAME" -n "$NAMESPACE"
fi

# Delete secrets if they exist
echo -e "\n${YELLOW}Checking for remaining secrets...${NC}"
SECRET_NAME="todo-secrets"
if kubectl get secret "$SECRET_NAME" -n "$NAMESPACE" > /dev/null 2>&1; then
    echo -e "${YELLOW}Deleting secret: $SECRET_NAME${NC}"
    kubectl delete secret "$SECRET_NAME" -n "$NAMESPACE"
fi

# Verify cleanup
echo -e "\n${YELLOW}Verifying cleanup...${NC}"
REMAINING_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME --no-headers 2>/dev/null | wc -l)

if [ "$REMAINING_PODS" -eq 0 ]; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}Cleanup completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "\n${YELLOW}Warning: Some pods may still be terminating${NC}"
    kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME
fi

echo -e "\n${YELLOW}Note: Docker images are still available in Minikube's Docker daemon${NC}"
echo -e "${YELLOW}To remove them, run:${NC}"
echo -e "eval \$(minikube docker-env)"
echo -e "docker rmi todo-backend:latest todo-frontend:latest"
