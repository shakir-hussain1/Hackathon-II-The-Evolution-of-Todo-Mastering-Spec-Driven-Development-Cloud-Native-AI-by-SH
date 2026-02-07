# Kubernetes Deployment: Technical Decisions Summary

## Quick Reference for Implementation

### 1. Docker Image Structure
**DECISION: Multi-Stage Builds**

```dockerfile
# Next.js Multi-Stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/public ./public
CMD ["npm", "start"]

# FastAPI Multi-Stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why:** 75% image size reduction (1.2GB→300MB for Next.js), better caching, production best practice

**Expected Image Sizes:**
- Next.js: 200-300MB
- FastAPI: 120-180MB

---

### 2. Helm Chart Layout
**DECISION: Umbrella Chart with Sub-Charts**

**Structure:**
```
helm/
└── todo-app/                 # Parent chart
    ├── Chart.yaml
    ├── values.yaml
    ├── Chart.lock
    └── charts/
        ├── frontend/         # Sub-chart
        └── backend/          # Sub-chart
```

**Deployment:**
```bash
helm install todo-app ./helm/todo-app
# Deploys frontend + backend together
```

**Why:** Single deployment command, unified versioning, shared configuration, clear for learning

---

### 3. Service Configuration
**DECISION: NodePort (Frontend) + ClusterIP (Backend)**

**Frontend (Next.js):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: NodePort
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30080
  selector:
    app: frontend
```

**Access:** `http://<minikube-ip>:30080` or `minikube service frontend --url`

**Backend (FastAPI):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: backend
```

**Access from Frontend:** `http://backend.default.svc.cluster.local:8000`

**Why:** Frontend needs external access (NodePort), backend stays internal (ClusterIP = more secure)

---

### 4. Resource Limits
**DECISION: Conservative Allocation with Headroom**

**Frontend (Next.js):**
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

**Backend (FastAPI):**
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

**Minikube Startup:**
```bash
minikube start \
  --memory=6144 \      # 6GB to cluster (leave 2GB for host)
  --cpus=4 \           # 4 cores (leave 4 for host)
  --disk-size=40g
```

**Cluster Math:**
- Frontend limit: 256Mi
- Backend limit: 512Mi
- System overhead: 512Mi
- **Total used:** ~1.3Gi out of 6Gi = 22% (healthy headroom)

**Why:** Safe for 8GB laptop, prevents pod crashes, teaches resource management

---

### 5. Storage Strategy
**DECISION: Ephemeral (SQLite + emptyDir)**

**SQLite Configuration:**
```yaml
# In deployment template
volumeMounts:
- name: db-volume
  mountPath: /app/db

volumes:
- name: db-volume
  emptyDir: {}  # Data lost on pod restart, OK for learning
```

**Logs Configuration:**
```python
# FastAPI
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Outputs to stdout → Kubernetes captures automatically
# Access: kubectl logs -f deployment/backend
```

**Static Assets:**
- Built into Next.js image during multi-stage build
- Served from `/public` directory
- No separate storage needed

**Why:** Zero additional setup, teaches containerization philosophy, can upgrade to PVC in Week 3

**Upgrade Path (Week 3+):**
- Replace emptyDir with PersistentVolumeClaim
- Add PostgreSQL with persistent volume
- Teach storage abstraction in Kubernetes

---

### 6. Minikube Driver
**DECISION: Docker Driver (Primary) with VirtualBox Fallback**

**Docker Driver (Recommended):**
```bash
# Prerequisites
1. Docker Desktop for Windows (4.1.0+)
2. WSL2 enabled
3. Windows 10 21H2 or later

# Start cluster
minikube start --driver=docker --memory=6144 --cpus=4

# Resource usage: ~500MB, startup: 15-20 seconds
```

**Why:** Lowest overhead, fastest startup, already have Docker Desktop

**VirtualBox Fallback (if Docker fails):**
```bash
# Prerequisites
1. VirtualBox 6.0+
2. CPU with VT-X support

# Start cluster
minikube start --driver=virtualbox --memory=6144 --cpus=4

# Resource usage: ~2-3GB, startup: 45-60 seconds
```

**Why:** Works on any Windows version, no WSL2 requirement, educational value

**Do NOT use HyperV:** Requires Windows Pro, no advantage, steeper setup

---

## Implementation Checklist

### Phase 1: Setup (Week 1)
- [ ] Create multi-stage Dockerfiles for both services
- [ ] Create umbrella Helm chart structure
- [ ] Define NodePort service for frontend
- [ ] Define ClusterIP service for backend
- [ ] Set resource requests and limits
- [ ] Use emptyDir for database storage
- [ ] Configure logging to stdout
- [ ] Test deployment: `helm install todo-app ./helm/todo-app`

### Phase 2: Service Communication (Week 2)
- [ ] Configure frontend to discover backend via DNS
- [ ] Set backend URL: `http://backend.default.svc.cluster.local:8000`
- [ ] Test inter-service communication
- [ ] Add port-forward debugging capability
- [ ] Document log access patterns

### Phase 3: Persistence (Week 3+)
- [ ] Add PersistentVolumeClaim for database
- [ ] Upgrade to PostgreSQL
- [ ] Demonstrate data persistence across pod restarts
- [ ] Teach storage abstraction

### Phase 4: Production Patterns (Week 4+)
- [ ] Separate independent charts
- [ ] Add Ingress controller
- [ ] Implement horizontal pod autoscaling
- [ ] Add NetworkPolicies
- [ ] Security hardening

---

## Testing Commands

```bash
# Verify Minikube is running
minikube status

# Deploy
helm install todo-app ./helm/todo-app

# Check deployments
kubectl get deployments
kubectl get pods
kubectl get services

# Verify frontend access
minikube service frontend --url

# Test backend from cluster
kubectl port-forward svc/backend 8000:8000

# View logs
kubectl logs -f deployment/frontend
kubectl logs -f deployment/backend

# Describe resources for troubleshooting
kubectl describe pod <pod-name>
kubectl describe service frontend
```

---

## Rationale Summary

| Decision | Primary Rationale | Secondary Benefits | Trade-offs |
|----------|------------------|-------------------|-----------|
| Multi-stage Docker | 75% size reduction | Better caching, prod practice | Slightly slower first build |
| Umbrella Chart | Single deployment | Unified versioning | Less service independence |
| NodePort + ClusterIP | UI access + security | Clear architecture | NodePort port limit 30000-32767 |
| Resource Limits | Safe for 8GB laptop | Prevents pod crashes | Tight constraints force efficiency |
| Ephemeral Storage | Zero setup overhead | Educational progression | Data lost on restart (OK for learning) |
| Docker Driver | Lowest overhead | Fastest, simplest | Requires WSL2 |

---

## Key Learnings for Students

1. **Containerization:** Why multi-stage builds and optimized images matter
2. **Kubernetes Services:** Different patterns for internal vs external access
3. **Resource Management:** How to allocate resources responsibly
4. **Stateless Design:** Why containers are ephemeral and how to handle state
5. **Service Discovery:** How Kubernetes DNS enables service-to-service communication
6. **Local Development:** How to develop locally before going to production

---

## Production Differences

When moving to production, these change:

| Area | Development | Production |
|------|-------------|-----------|
| **Service Type** | NodePort | Ingress + LoadBalancer |
| **Resources** | Generous limits | Tight limits forcing efficiency |
| **Storage** | ephemeral | Cloud-managed PersistentVolumes |
| **Logging** | stdout | Central logging system (ELK, Datadog) |
| **Replicas** | 1 | 3+ for high availability |
| **Driver** | Docker local | Managed Kubernetes (EKS, GKE, AKS) |

---

## Next Steps

1. **Create Dockerfiles:** Implement multi-stage builds
2. **Create Helm Chart:** Implement umbrella structure
3. **Deploy:** Test on Minikube with these configurations
4. **Iterate:** Add complexity gradually (persistence, logging, etc.)
5. **Document:** Create runbooks for deployment and troubleshooting
