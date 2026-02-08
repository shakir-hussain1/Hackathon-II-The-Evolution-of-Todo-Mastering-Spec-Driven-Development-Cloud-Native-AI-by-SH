# Oracle OKE Deployment Guide - Phase V Todo System

**Deadline**: February 9, 2026
**Goal**: Deploy Phase V to Oracle Cloud (OKE) and get a live URL for Hackathon submission

---

## Prerequisites

### 1. Oracle Cloud Account Setup

1. **Create Oracle Cloud Account** (Free Tier):
   - Visit: https://www.oracle.com/cloud/free/
   - Sign up for "Always Free" tier
   - ✅ Free includes: 2 AMD VMs (1GB RAM each), 100GB block storage

2. **Install Oracle CLI**:
   ```bash
   # Windows (PowerShell)
   Invoke-WebRequest https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.ps1 -OutFile install.ps1
   ./install.ps1

   # Or download from: https://docs.oracle.com/iaas/Content/API/SDKDocs/cliinstall.htm
   ```

3. **Configure OCI CLI**:
   ```bash
   oci setup config
   # Follow prompts to create API keys and config
   ```

### 2. Required Tools

```bash
# kubectl (Kubernetes CLI)
choco install kubernetes-cli

# helm (Package manager)
choco install kubernetes-helm

# dapr CLI
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
```

---

## Option 1: Quick Deploy to Oracle OKE (Recommended)

### Step 1: Create OKE Cluster

1. **Via OCI Console** (Easiest):
   - Login to https://cloud.oracle.com
   - Navigate to: Developer Services → Kubernetes Clusters (OKE)
   - Click "Create Cluster"
   - Choose "Quick Create"
   - Configuration:
     - Name: `phase5-oke-cluster`
     - Kubernetes Version: Latest (1.28+)
     - Node Pool: 2 nodes, VM.Standard.E2.1.Micro (Always Free tier)
     - Shape: 1 OCPU, 1GB RAM per node
   - Click "Create Cluster" (takes 10-15 minutes)

2. **Access Kubeconfig**:
   ```bash
   # After cluster creation, click "Access Cluster" button
   # Copy the kubectl config command
   oci ce cluster create-kubeconfig --cluster-id <YOUR_CLUSTER_ID> --file %USERPROFILE%\.kube\config --region us-ashburn-1

   # Verify connection
   kubectl get nodes
   ```

### Step 2: Deploy to OKE

```bash
cd helm

# Run automated OKE deployment script
./deploy-oke.sh

# Script will:
# 1. Check prerequisites
# 2. Install Dapr runtime
# 3. Deploy PostgreSQL and Kafka
# 4. Deploy all 6 microservices + frontend
# 5. Apply Dapr components
# 6. Configure ingress
# 7. Validate deployment
```

### Step 3: Get Public URL

```bash
# Wait for Load Balancer to get external IP (2-5 minutes)
kubectl get ingress -n phase5

# Output will show:
# NAME                  HOSTS              ADDRESS            PORTS
# phase5-frontend      todo.example.com   140.238.x.x        80, 443

# Your app URL: http://<EXTERNAL-IP>
# Or configure DNS: todo.yourdomain.com → <EXTERNAL-IP>
```

### Step 4: Test Deployment

```bash
# Run validation
./validate.sh phase5 phase5

# Manual test
curl http://<EXTERNAL-IP>/health

# Check all pods
kubectl get pods -n phase5

# Expected output: All pods in Running state (2/2 containers)
```

---

## Option 2: Alternative Cloud Platforms (If OKE Fails)

### Railway.app (Fastest, Simpler)

**Pros**: One-click deploy, free tier, automatic HTTPS
**Cons**: Limited to 500 MB RAM per service

```bash
# 1. Sign up: https://railway.app
# 2. Install Railway CLI
npm install -g @railway/cli

# 3. Deploy
railway login
railway init
railway up

# 4. Configure environment variables in Railway dashboard
# 5. Get URL from Railway dashboard
```

### Render.com (Good Alternative)

**Pros**: Free PostgreSQL, 750 hours/month, auto-deploy from GitHub
**Cons**: Services sleep after 15 minutes of inactivity

```bash
# 1. Sign up: https://render.com
# 2. Connect GitHub repo
# 3. Create "Blueprint" from render.yaml
# 4. Deploy all services
# 5. Get URLs from dashboard
```

### DigitalOcean Kubernetes (Paid, but Reliable)

**Cost**: $12/month for smallest cluster
**Pros**: Reliable, good documentation, managed Kubernetes

```bash
# 1. Sign up: https://www.digitalocean.com
# 2. Create Kubernetes cluster (1-click)
# 3. Download kubeconfig
doctl kubernetes cluster kubeconfig save <cluster-name>

# 4. Deploy
cd helm
./deploy-oke.sh  # Same script works on any K8s
```

---

## Option 3: Docker Compose (Local Demo)

**If cloud deployment fails, use Docker Compose for demo video:**

```bash
cd phase5

# Build all images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Access app at: http://localhost:3000
```

---

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n phase5

# Describe failing pod
kubectl describe pod <pod-name> -n phase5

# Check logs
kubectl logs <pod-name> -n phase5 -c <container-name>
```

### Dapr Issues

```bash
# Check Dapr installation
dapr status -k

# Reinstall Dapr
dapr uninstall -k
dapr init -k --wait
```

### Database Connection Errors

```bash
# Check PostgreSQL pod
kubectl get pods -n phase5 | grep postgres

# Port-forward to test connection
kubectl port-forward -n phase5 svc/postgres 5432:5432

# Test connection
psql -h localhost -U postgres -d phase5_todo
```

### Out of Memory

```bash
# Scale down replicas
kubectl scale deployment chat-api -n phase5 --replicas=1
kubectl scale deployment frontend -n phase5 --replicas=1

# Or increase node resources in OKE console
```

---

## Next Steps After Deployment

1. **Get Public URL**:
   ```bash
   kubectl get ingress -n phase5 -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}'
   ```

2. **Test App**:
   - Open browser to `http://<EXTERNAL-IP>`
   - Register account
   - Create tasks via chat
   - Verify real-time sync

3. **Record Demo Video** (see DEMO_VIDEO_GUIDE.md)

4. **Submit to Hackathon**:
   - GitHub repository URL
   - Deployed app URL: `http://<EXTERNAL-IP>`
   - YouTube demo video link

---

## Production Checklist (Optional Post-Demo)

- [ ] Configure custom domain (todo.yourdomain.com)
- [ ] Enable TLS/HTTPS with Let's Encrypt
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure alerting
- [ ] Enable backup for PostgreSQL
- [ ] Set up CI/CD pipeline
- [ ] Configure autoscaling policies
- [ ] Enable distributed tracing (Zipkin/Jaeger)

---

## Estimated Costs

**Oracle OKE (Always Free Tier)**:
- ✅ **$0/month** - 2 VMs, forever free
- ✅ 100 GB block storage included
- ✅ 10 GB outbound data/month free

**Railway.app**:
- ✅ **$0/month** - Free tier (500 MB RAM per service)
- ⚠️ Limited to 500 hours/month

**Render.com**:
- ✅ **$0/month** - Free tier
- ⚠️ Services sleep after inactivity

**DigitalOcean**:
- 💰 **$12/month** - Smallest Kubernetes cluster
- ✅ Reliable and well-documented

---

## Support

If deployment fails:
1. Check logs: `kubectl logs <pod-name> -n phase5`
2. Run validation: `./validate.sh phase5 phase5`
3. Review deployment script output for errors
4. Fall back to Docker Compose for local demo

**Remember**: The goal is to have a working demo by February 9. If cloud deployment takes too long, use Docker Compose locally and record video with localhost URLs!
