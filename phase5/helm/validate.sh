#!/bin/bash
# Validation script for Phase 5 deployment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NAMESPACE=${1:-phase5}
RELEASE=${2:-phase5}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 5 Deployment Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Namespace: ${GREEN}${NAMESPACE}${NC}"
echo -e "Release: ${GREEN}${RELEASE}${NC}"
echo ""

# Track results
PASSED=0
FAILED=0
WARNINGS=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# 1. Check namespace exists
echo -e "\n${YELLOW}1. Checking namespace...${NC}"
if kubectl get namespace "$NAMESPACE" &> /dev/null; then
    check_pass "Namespace '$NAMESPACE' exists"
else
    check_fail "Namespace '$NAMESPACE' not found"
    exit 1
fi

# 2. Check Helm release
echo -e "\n${YELLOW}2. Checking Helm release...${NC}"
if helm list -n "$NAMESPACE" | grep -q "$RELEASE"; then
    RELEASE_STATUS=$(helm list -n "$NAMESPACE" | grep "$RELEASE" | awk '{print $8}')
    if [ "$RELEASE_STATUS" == "deployed" ]; then
        check_pass "Helm release '$RELEASE' is deployed"
    else
        check_warn "Helm release status: $RELEASE_STATUS"
    fi
else
    check_fail "Helm release '$RELEASE' not found"
fi

# 3. Check Dapr installation
echo -e "\n${YELLOW}3. Checking Dapr...${NC}"
if kubectl get namespace dapr-system &> /dev/null; then
    check_pass "Dapr namespace exists"

    DAPR_PODS=$(kubectl get pods -n dapr-system --no-headers 2>/dev/null | wc -l)
    if [ "$DAPR_PODS" -gt 0 ]; then
        check_pass "Dapr pods running ($DAPR_PODS pods)"
    else
        check_fail "No Dapr pods found"
    fi
else
    check_fail "Dapr not installed"
fi

# 4. Check Dapr components
echo -e "\n${YELLOW}4. Checking Dapr components...${NC}"
EXPECTED_COMPONENTS=("pubsub-kafka" "statestore" "secretstore" "cron-recurring-tasks" "cron-reminders")

for component in "${EXPECTED_COMPONENTS[@]}"; do
    if kubectl get component "$component" -n "$NAMESPACE" &> /dev/null; then
        check_pass "Component '$component' exists"
    else
        check_fail "Component '$component' not found"
    fi
done

# Check Dapr configuration
if kubectl get configuration dapr-config -n "$NAMESPACE" &> /dev/null; then
    check_pass "Dapr configuration exists"
else
    check_warn "Dapr configuration not found"
fi

# 5. Check pods
echo -e "\n${YELLOW}5. Checking pods...${NC}"
EXPECTED_SERVICES=("chat-api" "notification-service" "recurring-task-service" "audit-service" "websocket-sync-service" "frontend")

for service in "${EXPECTED_SERVICES[@]}"; do
    POD_COUNT=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=$service" --no-headers 2>/dev/null | wc -l)

    if [ "$POD_COUNT" -gt 0 ]; then
        RUNNING_COUNT=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=$service" --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)

        if [ "$RUNNING_COUNT" -eq "$POD_COUNT" ]; then
            # Check ready status
            READY_COUNT=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=$service" -o jsonpath='{range .items[*]}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}' | grep -c "True" || true)

            if [ "$READY_COUNT" -eq "$POD_COUNT" ]; then
                check_pass "$service: $POD_COUNT/$POD_COUNT pods ready"
            else
                check_warn "$service: $READY_COUNT/$POD_COUNT pods ready"
            fi
        else
            check_fail "$service: Only $RUNNING_COUNT/$POD_COUNT pods running"
        fi
    else
        check_fail "$service: No pods found"
    fi
done

# Check infrastructure pods
echo -e "\n${YELLOW}6. Checking infrastructure...${NC}"

# PostgreSQL
if kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=postgresql" --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q .; then
    check_pass "PostgreSQL is running"
else
    check_fail "PostgreSQL is not running"
fi

# Kafka
if kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=kafka" --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q .; then
    KAFKA_PODS=$(kubectl get pods -n "$NAMESPACE" -l "app.kubernetes.io/name=kafka" --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
    check_pass "Kafka is running ($KAFKA_PODS brokers)"
else
    check_fail "Kafka is not running"
fi

# 7. Check services
echo -e "\n${YELLOW}7. Checking services...${NC}"
for service in "${EXPECTED_SERVICES[@]}"; do
    if kubectl get svc "${RELEASE}-${service}" -n "$NAMESPACE" &> /dev/null; then
        check_pass "Service '$service' exists"
    else
        check_fail "Service '$service' not found"
    fi
done

# 8. Check secrets
echo -e "\n${YELLOW}8. Checking secrets...${NC}"
EXPECTED_SECRETS=("postgres-secret" "jwt-secret" "openai-secret")

for secret in "${EXPECTED_SECRETS[@]}"; do
    if kubectl get secret "$secret" -n "$NAMESPACE" &> /dev/null; then
        check_pass "Secret '$secret' exists"
    else
        check_fail "Secret '$secret' not found"
    fi
done

# 9. Check ingress
echo -e "\n${YELLOW}9. Checking ingress...${NC}"
if kubectl get ingress -n "$NAMESPACE" &> /dev/null; then
    INGRESS_COUNT=$(kubectl get ingress -n "$NAMESPACE" --no-headers | wc -l)
    if [ "$INGRESS_COUNT" -gt 0 ]; then
        check_pass "Ingress configured ($INGRESS_COUNT ingresses)"

        # Check if ingress has address
        if kubectl get ingress -n "$NAMESPACE" -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}' 2>/dev/null | grep -q .; then
            LB_IP=$(kubectl get ingress -n "$NAMESPACE" -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}')
            echo -e "  Load Balancer IP: ${GREEN}${LB_IP}${NC}"
        else
            check_warn "No Load Balancer IP assigned yet"
        fi
    else
        check_warn "No ingress found"
    fi
else
    check_warn "Ingress not configured"
fi

# 10. Check HPA
echo -e "\n${YELLOW}10. Checking autoscaling...${NC}"
HPA_COUNT=$(kubectl get hpa -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$HPA_COUNT" -gt 0 ]; then
    check_pass "HPA configured ($HPA_COUNT HPAs)"
else
    check_warn "No HPA configured"
fi

# 11. Test health endpoints
echo -e "\n${YELLOW}11. Testing health endpoints...${NC}"
for service in "chat-api" "notification-service" "audit-service"; do
    POD=$(kubectl get pod -n "$NAMESPACE" -l "app.kubernetes.io/name=$service" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -n "$POD" ]; then
        if kubectl exec -n "$NAMESPACE" "$POD" -c "$service" -- curl -sf http://localhost:${service#*:}/health &> /dev/null; then
            check_pass "$service health endpoint responds"
        else
            check_warn "$service health endpoint not responding"
        fi
    fi
done

# 12. Check PVCs
echo -e "\n${YELLOW}12. Checking persistent volumes...${NC}"
PVC_COUNT=$(kubectl get pvc -n "$NAMESPACE" --no-headers 2>/dev/null | wc -l)
if [ "$PVC_COUNT" -gt 0 ]; then
    BOUND_COUNT=$(kubectl get pvc -n "$NAMESPACE" --field-selector=status.phase=Bound --no-headers 2>/dev/null | wc -l)
    if [ "$BOUND_COUNT" -eq "$PVC_COUNT" ]; then
        check_pass "All PVCs bound ($BOUND_COUNT/$PVC_COUNT)"
    else
        check_warn "Only $BOUND_COUNT/$PVC_COUNT PVCs bound"
    fi
else
    check_warn "No PVCs found"
fi

# Summary
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"

if [ "$FAILED" -eq 0 ]; then
    echo -e "\n${GREEN}✓ Deployment validation successful!${NC}"

    # Show access info
    echo -e "\n${YELLOW}Access Information:${NC}"
    echo -e "Frontend: ${GREEN}kubectl port-forward -n $NAMESPACE svc/${RELEASE}-frontend 3000:3000${NC}"
    echo -e "Then open: ${GREEN}http://localhost:3000${NC}"

    echo -e "\n${YELLOW}Logs:${NC}"
    echo -e "${GREEN}kubectl logs -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE -f --all-containers=true${NC}"

    exit 0
else
    echo -e "\n${RED}✗ Deployment validation failed!${NC}"
    echo -e "Please check the failed items above."
    exit 1
fi
