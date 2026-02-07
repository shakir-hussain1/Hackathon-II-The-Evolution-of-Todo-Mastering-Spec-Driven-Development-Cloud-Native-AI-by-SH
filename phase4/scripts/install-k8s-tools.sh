#!/bin/bash
# Phase IV Kubernetes Tools Installation Script
# Target: WSL2 Ubuntu 22.04
# Run as: bash install-k8s-tools.sh

set -e  # Exit on any error

echo "========================================"
echo "Phase IV Kubernetes Tools Installation"
echo "Target: WSL2 Ubuntu 22.04"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log function
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in WSL2
log_info "Checking WSL2 environment..."
if grep -qi microsoft /proc/version; then
    log_info "✓ Running in WSL2"
else
    log_warn "Not running in WSL2. Script optimized for WSL2 Ubuntu."
fi

# Check virtualization support
log_info "Checking virtualization support..."
if egrep -q 'vmx|svm' /proc/cpuinfo; then
    log_info "✓ Virtualization supported"
else
    log_error "✗ Virtualization not supported or not enabled in BIOS"
fi

echo ""
echo "========================================"
echo "1. CHECKING EXISTING INSTALLATIONS"
echo "========================================"

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    log_info "Docker already installed: $DOCKER_VERSION"
else
    log_warn "Docker not found - will be installed via Docker Desktop"
fi

# Check Minikube
if command -v minikube &> /dev/null; then
    MINIKUBE_VERSION=$(minikube version --short)
    log_info "Minikube already installed: $MINIKUBE_VERSION"
else
    log_warn "Minikube not found - will be installed"
fi

# Check kubectl
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | awk '{print $3}')
    log_info "kubectl already installed: $KUBECTL_VERSION"
else
    log_warn "kubectl not found - will be installed"
fi

# Check Helm
if command -v helm &> /dev/null; then
    HELM_VERSION=$(helm version --short)
    log_info "Helm already installed: $HELM_VERSION"
else
    log_warn "Helm not found - will be installed"
fi

echo ""
echo "========================================"
echo "2. DOCKER DESKTOP NOTE"
echo "========================================"
log_warn "Docker Desktop must be installed on Windows host"
log_warn "Download from: https://www.docker.com/products/docker-desktop"
log_warn "Ensure WSL2 integration is enabled in Docker Desktop settings"
echo ""
read -p "Press Enter once Docker Desktop is installed and running..."

# Verify Docker Desktop integration
if command -v docker &> /dev/null; then
    log_info "✓ Docker command available in WSL2"
    docker --version
else
    log_error "✗ Docker command not found. Check Docker Desktop WSL2 integration"
    exit 1
fi

echo ""
echo "========================================"
echo "3. INSTALLING MINIKUBE"
echo "========================================"

if command -v minikube &> /dev/null && [[ $(minikube version --short | cut -d'v' -f2) > "1.32" ]]; then
    log_info "✓ Minikube 1.32+ already installed"
else
    log_info "Installing Minikube..."
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    rm minikube-linux-amd64
    log_info "✓ Minikube installed"
fi

minikube version

echo ""
echo "========================================"
echo "4. INSTALLING KUBECTL"
echo "========================================"

if command -v kubectl &> /dev/null && [[ $(kubectl version --client -o json 2>/dev/null | grep -o '"gitVersion":"v[0-9.]*"' | cut -d'v' -f3 | cut -d'"' -f1 | cut -d'.' -f2) -ge 28 ]]; then
    log_info "✓ kubectl 1.28+ already installed"
else
    log_info "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
    log_info "✓ kubectl installed"
fi

kubectl version --client

echo ""
echo "========================================"
echo "5. INSTALLING HELM"
echo "========================================"

if command -v helm &> /dev/null && [[ $(helm version --short | cut -d'v' -f2 | cut -d'.' -f2) -ge 13 ]]; then
    log_info "✓ Helm 3.13+ already installed"
else
    log_info "Installing Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    log_info "✓ Helm installed"
fi

helm version

echo ""
echo "========================================"
echo "6. STARTING MINIKUBE CLUSTER"
echo "========================================"

log_info "Starting Minikube with Docker driver..."
log_info "Allocating 6GB RAM and 2 CPUs..."

# Stop existing cluster if running
minikube delete 2>/dev/null || true

# Start new cluster
minikube start --driver=docker --memory=6144 --cpus=2

log_info "✓ Minikube cluster started"

echo ""
echo "========================================"
echo "7. VERIFYING MINIKUBE STATUS"
echo "========================================"

minikube status

echo ""
echo "========================================"
echo "8. CONFIGURING KUBECTL"
echo "========================================"

log_info "Configuring kubectl context..."
kubectl config use-context minikube
log_info "✓ kubectl configured for Minikube"

echo ""
echo "========================================"
echo "9. VERIFYING CLUSTER CONNECTIVITY"
echo "========================================"

log_info "Testing cluster connectivity..."
kubectl cluster-info
kubectl get nodes

echo ""
echo "========================================"
echo "10. ADDING HELM REPOSITORIES"
echo "========================================"

log_info "Adding Helm stable repository..."
helm repo add stable https://charts.helm.sh/stable 2>/dev/null || log_warn "Stable repo already added"
helm repo update

echo ""
echo "========================================"
echo "11. TEST DEPLOYMENT"
echo "========================================"

log_info "Deploying test nginx pod..."
kubectl run test-nginx --image=nginx:alpine --restart=Never 2>/dev/null || log_warn "Test pod may already exist"

log_info "Waiting for pod to be ready..."
kubectl wait --for=condition=Ready pod/test-nginx --timeout=60s

log_info "✓ Test pod running successfully"

# Show pod status
kubectl get pod test-nginx

# Cleanup test pod
log_info "Cleaning up test pod..."
kubectl delete pod test-nginx --ignore-not-found=true

echo ""
echo "========================================"
echo "12. FINAL VERIFICATION"
echo "========================================"

echo ""
echo "Installed Versions:"
echo "-------------------"
echo -n "Docker:    "; docker --version
echo -n "Minikube:  "; minikube version --short
echo -n "kubectl:   "; kubectl version --client --short 2>/dev/null || kubectl version --client
echo -n "Helm:      "; helm version --short

echo ""
echo "Cluster Status:"
echo "---------------"
minikube status

echo ""
echo "========================================"
echo "✓ INSTALLATION COMPLETE"
echo "========================================"
echo ""
log_info "All tools installed and verified successfully!"
log_info "Minikube cluster is running and ready for deployment"
echo ""
log_info "Next steps:"
log_info "  1. Return to Claude Code"
log_info "  2. Say 'Tools installed' to continue Phase 2"
echo ""
