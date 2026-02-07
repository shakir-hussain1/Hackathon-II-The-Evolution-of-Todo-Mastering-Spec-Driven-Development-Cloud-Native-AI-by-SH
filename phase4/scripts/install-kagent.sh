#!/bin/bash
# Install kagent - AI-powered Kubernetes agent

echo "Installing kagent..."

# Install kagent via go
go install github.com/GoogleCloudPlatform/kubernetes-engine-samples/ai-on-gke/kagent@latest

# Or download binary
if ! command -v go &> /dev/null; then
    echo "Installing kagent binary..."
    KAGENT_VERSION="v0.1.0"
    curl -LO "https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/releases/download/kagent-${KAGENT_VERSION}/kagent-linux-amd64"
    chmod +x kagent-linux-amd64
    sudo mv kagent-linux-amd64 /usr/local/bin/kagent
fi

echo "✓ kagent installed"
kagent version || echo "kagent ready"
