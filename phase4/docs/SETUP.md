# Phase IV Environment Setup Guide

**Target**: Complete installation and configuration of all required tools for local Kubernetes deployment

**Time**: 30-60 minutes (depending on download speeds and system)

---

## Prerequisites

- **Operating System**: Windows 10/11, macOS, or Linux
- **RAM**: Minimum 8GB (Minikube will use 6GB)
- **CPU**: Minimum 2 cores
- **Disk Space**: 20GB free
- **Internet**: Required for downloading tools and Docker images

---

## Installation Steps

### 1. Docker Desktop (REQUIRED)

Docker Desktop provides the container runtime needed for building images and running Minikube.

#### Windows

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Run the installer
3. **Enable WSL2** when prompted (recommended for better performance)
4. Restart your computer if required
5. Start Docker Desktop from Start Menu
6. Wait for Docker to fully start (whale icon in system tray should be steady)

**Verify Installation:**
```bash
docker --version
# Expected: Docker version 24.0.0 or higher

docker ps
# Expected: Empty list (no containers running yet)
```

#### macOS

1. Download Docker Desktop for Mac from: https://www.docker.com/products/docker-desktop
2. Open the `.dmg` file and drag Docker to Applications
3. Launch Docker from Applications
4. Grant necessary permissions when prompted
5. Wait for Docker to start (whale icon in menu bar should be steady)

**Verify Installation:**
```bash
docker --version
# Expected: Docker version 24.0.0 or higher
```

#### Linux

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and log back in for group changes to take effect

# Verify
docker --version
```

---

### 2. Minikube (REQUIRED)

Minikube creates a local Kubernetes cluster for development and testing.

#### Windows (PowerShell as Administrator)

```powershell
# Using Chocolatey (recommended)
choco install minikube

# OR download manually from:
# https://minikube.sigs.k8s.io/docs/start/
```

#### macOS

```bash
# Using Homebrew (recommended)
brew install minikube

# OR using curl
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

#### Linux

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Verify Installation:**
```bash
minikube version
# Expected: minikube version: v1.32.0 or higher
```

---

### 3. kubectl (REQUIRED)

kubectl is the command-line tool for interacting with Kubernetes clusters.

#### Windows

```powershell
# Using Chocolatey
choco install kubernetes-cli

# OR download manually from:
# https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

**Note**: kubectl is included with Docker Desktop on Windows/Mac, so you may already have it.

#### macOS

```bash
# Using Homebrew
brew install kubectl

# OR using curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

#### Linux

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Verify Installation:**
```bash
kubectl version --client
# Expected: Client Version: v1.28.0 or higher
```

---

### 4. Helm (REQUIRED)

Helm is the package manager for Kubernetes, used to deploy applications via charts.

#### Windows

```powershell
# Using Chocolatey
choco install kubernetes-helm
```

#### macOS

```bash
# Using Homebrew
brew install helm
```

#### Linux

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Verify Installation:**
```bash
helm version
# Expected: version.BuildInfo{Version:"v3.13.0" or higher}
```

---

### 5. kubectl-ai (OPTIONAL)

kubectl-ai provides natural language commands for Kubernetes operations.

#### Installation

```bash
# Install via kubectl plugin manager (krew)
# First install krew: https://krew.sigs.k8s.io/docs/user-guide/setup/install/

kubectl krew install ai

# OR follow instructions at:
# https://github.com/sozercan/kubectl-ai
```

**Verify Installation:**
```bash
kubectl ai --version
```

**Fallback**: If kubectl-ai is not available, we'll use standard kubectl commands with Claude Code assistance.

---

### 6. Kagent (OPTIONAL)

Kagent provides AI-powered cluster health analysis and optimization.

#### Installation

```bash
# Follow instructions at:
# https://github.com/GoogleCloudPlatform/kagent

# Typically:
pip install kagent
# OR
brew install kagent  # macOS
```

**Verify Installation:**
```bash
kagent --version
```

**Fallback**: If Kagent is not available, we'll use `kubectl top` and manual analysis.

---

### 7. Docker AI Agent - Gordon (OPTIONAL)

Gordon provides AI-assisted Dockerfile generation and optimization.

#### Installation

```bash
# Enable Docker AI features in Docker Desktop
# Go to: Settings → Features in Development → Enable AI
# OR follow: https://docs.docker.com/ai/

# Verify
docker ai --version
```

**Fallback**: If Gordon is not available, we'll use Claude Code to generate Dockerfiles.

---

## Post-Installation Verification

Run this complete verification script:

```bash
echo "=== Docker ==="
docker --version
docker ps

echo "=== Minikube ==="
minikube version

echo "=== kubectl ==="
kubectl version --client

echo "=== Helm ==="
helm version

echo "=== Optional: kubectl-ai ==="
kubectl ai --version || echo "Not installed (using fallback)"

echo "=== Optional: Kagent ==="
kagent --version || echo "Not installed (using fallback)"

echo "=== Optional: Docker AI (Gordon) ==="
docker ai --version || echo "Not installed (using fallback)"
```

**Expected Result**: All REQUIRED tools should show version numbers. Optional tools can show "Not installed" and we'll use fallbacks.

---

## Starting Minikube

Once all tools are installed, start your Minikube cluster:

```bash
# Start Minikube with appropriate resources
minikube start --memory=6144 --cpus=2 --driver=docker

# Verify cluster is running
minikube status

# Verify kubectl can connect
kubectl cluster-info
```

**Expected Output**:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
```

---

## Troubleshooting

### Docker Desktop not starting

- **Windows**: Enable WSL2 in Windows Features
- **Mac**: Grant necessary permissions in System Preferences → Security
- **All**: Ensure virtualization is enabled in BIOS/UEFI

### Minikube fails to start

```bash
# Try different driver
minikube start --memory=6144 --cpus=2 --driver=virtualbox

# Check available drivers
minikube start --help | grep driver

# Delete and recreate
minikube delete
minikube start --memory=6144 --cpus=2 --driver=docker
```

### Insufficient memory

- Close other applications to free up RAM
- Reduce Minikube memory allocation (minimum 4GB):
  ```bash
  minikube start --memory=4096 --cpus=2
  ```

### kubectl connection refused

```bash
# Reset kubectl context
minikube update-context

# Verify context
kubectl config current-context
# Should show: minikube
```

---

## Next Steps

Once all tools are installed and verified:

1. **Configure Environment**: Copy `.env.example` to `.env` and fill in your secrets
2. **Read Phase III Source**: Familiarize yourself with `phase3/frontend/` and `phase3/backend/`
3. **Ready for Phase 2**: Proceed to containerization and deployment

---

## Additional Resources

- **Docker**: https://docs.docker.com/
- **Minikube**: https://minikube.sigs.k8s.io/docs/
- **kubectl**: https://kubernetes.io/docs/reference/kubectl/
- **Helm**: https://helm.sh/docs/
- **Kubernetes Basics**: https://kubernetes.io/docs/tutorials/kubernetes-basics/

---

**Estimated Setup Time**: 30-60 minutes
**Next Phase**: Containerization (Building Docker images)
