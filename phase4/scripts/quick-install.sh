#!/bin/bash
# Quick installation of Minikube and Helm

echo "Installing Minikube..."
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64
echo "✓ Minikube installed"

echo ""
echo "Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
echo "✓ Helm installed"

echo ""
echo "Verifying installations..."
minikube version
helm version

echo ""
echo "✅ All tools installed!"
echo ""
echo "Next: Run ./quick-start.sh to deploy the app"
