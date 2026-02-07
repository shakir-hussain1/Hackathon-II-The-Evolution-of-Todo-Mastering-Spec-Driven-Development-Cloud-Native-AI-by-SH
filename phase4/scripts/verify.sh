#!/bin/bash
# Verify Todo App deployment health and connectivity

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Todo App Deployment Verification${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration
RELEASE_NAME="todo-app"
NAMESPACE="default"

# Check if deployment exists
echo -e "\n${YELLOW}[1/6] Checking if deployment exists...${NC}"
if ! helm list -n "$NAMESPACE" | grep -q "^$RELEASE_NAME"; then
    echo -e "${RED}✗ No deployment found with name: $RELEASE_NAME${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Deployment found${NC}"

# Check pod status
echo -e "\n${YELLOW}[2/6] Checking pod status...${NC}"
BACKEND_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME,app.kubernetes.io/component=backend --no-headers 2>/dev/null)
FRONTEND_PODS=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME,app.kubernetes.io/component=frontend --no-headers 2>/dev/null)

echo -e "${BLUE}Backend pods:${NC}"
echo "$BACKEND_PODS"
echo -e "${BLUE}Frontend pods:${NC}"
echo "$FRONTEND_PODS"

# Count running pods
BACKEND_RUNNING=$(echo "$BACKEND_PODS" | grep -c "Running" || true)
FRONTEND_RUNNING=$(echo "$FRONTEND_PODS" | grep -c "Running" || true)

if [ "$BACKEND_RUNNING" -gt 0 ] && [ "$FRONTEND_RUNNING" -gt 0 ]; then
    echo -e "${GREEN}✓ All pods are running${NC}"
else
    echo -e "${RED}✗ Some pods are not running${NC}"
    exit 1
fi

# Check service endpoints
echo -e "\n${YELLOW}[3/6] Checking service endpoints...${NC}"
BACKEND_ENDPOINTS=$(kubectl get endpoints -n "$NAMESPACE" "${RELEASE_NAME}-backend" -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)
FRONTEND_ENDPOINTS=$(kubectl get endpoints -n "$NAMESPACE" "${RELEASE_NAME}-frontend" -o jsonpath='{.subsets[*].addresses[*].ip}' 2>/dev/null)

if [ -n "$BACKEND_ENDPOINTS" ] && [ -n "$FRONTEND_ENDPOINTS" ]; then
    echo -e "${GREEN}✓ Service endpoints are available${NC}"
    echo -e "${BLUE}Backend endpoints: $BACKEND_ENDPOINTS${NC}"
    echo -e "${BLUE}Frontend endpoints: $FRONTEND_ENDPOINTS${NC}"
else
    echo -e "${RED}✗ Service endpoints not available${NC}"
    exit 1
fi

# Check persistent volume claims
echo -e "\n${YELLOW}[4/6] Checking persistent volume claims...${NC}"
PVC_STATUS=$(kubectl get pvc -n "$NAMESPACE" "${RELEASE_NAME}-backend-pvc" -o jsonpath='{.status.phase}' 2>/dev/null || echo "NotFound")

if [ "$PVC_STATUS" = "Bound" ]; then
    echo -e "${GREEN}✓ PVC is bound${NC}"
else
    echo -e "${YELLOW}! PVC status: $PVC_STATUS${NC}"
fi

# Test backend health endpoint
echo -e "\n${YELLOW}[5/6] Testing backend health endpoint...${NC}"
BACKEND_POD=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME,app.kubernetes.io/component=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$BACKEND_POD" ]; then
    HEALTH_RESPONSE=$(kubectl exec -n "$NAMESPACE" "$BACKEND_POD" -- wget -q -O- http://localhost:7860/health 2>/dev/null || echo "Failed")

    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        echo -e "${GREEN}✓ Backend health check passed${NC}"
        echo -e "${BLUE}Response: $HEALTH_RESPONSE${NC}"
    else
        echo -e "${RED}✗ Backend health check failed${NC}"
        echo -e "${RED}Response: $HEALTH_RESPONSE${NC}"
    fi
else
    echo -e "${YELLOW}! Could not find backend pod for health check${NC}"
fi

# Test frontend connectivity
echo -e "\n${YELLOW}[6/6] Testing frontend connectivity...${NC}"
FRONTEND_POD=$(kubectl get pods -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME,app.kubernetes.io/component=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$FRONTEND_POD" ]; then
    FRONTEND_STATUS=$(kubectl exec -n "$NAMESPACE" "$FRONTEND_POD" -- wget -q -O- http://localhost:3000 2>/dev/null | head -c 50 || echo "Failed")

    if [ "$FRONTEND_STATUS" != "Failed" ]; then
        echo -e "${GREEN}✓ Frontend is responding${NC}"
    else
        echo -e "${RED}✗ Frontend connectivity test failed${NC}"
    fi
else
    echo -e "${YELLOW}! Could not find frontend pod for connectivity test${NC}"
fi

# Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Verification Summary${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${BLUE}Resource Status:${NC}"
kubectl get all -n "$NAMESPACE" -l app.kubernetes.io/instance=$RELEASE_NAME

echo -e "\n${YELLOW}Access Instructions:${NC}"
echo -e "Frontend: ${GREEN}minikube service ${RELEASE_NAME}-frontend --url${NC}"
echo -e "Backend: ${GREEN}kubectl port-forward -n $NAMESPACE svc/${RELEASE_NAME}-backend 8000:8000${NC}"

echo -e "\n${GREEN}Verification completed!${NC}"
