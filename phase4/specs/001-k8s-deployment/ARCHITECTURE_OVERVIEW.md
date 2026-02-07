# Architecture Overview: Kubernetes Deployment for Next.js + FastAPI

## Visual Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    MINIKUBE CLUSTER (6GB)                   │
│                        Docker Driver                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            KUBERNETES NAMESPACE: default             │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │                                                        │   │
│  │  ┌─────────────┐           ┌──────────────┐          │   │
│  │  │  FRONTEND   │           │   BACKEND    │          │   │
│  │  │ (Next.js)   │           │  (FastAPI)   │          │   │
│  │  │             │           │              │          │   │
│  │  │ Deployment  │           │ Deployment   │          │   │
│  │  │ replica: 1  │           │ replica: 1   │          │   │
│  │  │ Memory:     │           │ Memory:      │          │   │
│  │  │ req 128Mi   │           │ req 256Mi    │          │   │
│  │  │ lim 256Mi   │           │ lim 512Mi    │          │   │
│  │  │             │           │              │          │   │
│  │  │ CPU:        │           │ CPU:         │          │   │
│  │  │ req 100m    │           │ req 100m     │          │   │
│  │  │ lim 500m    │           │ lim 1000m    │          │   │
│  │  └─────────────┘           └──────────────┘          │   │
│  │         ▼                            ▲                │   │
│  │         │                            │                │   │
│  │  ┌──────┴──────────┐         ┌──────┴──────────┐    │   │
│  │  │ Service: NodePort │◄──────│ Service: ClusterIP   │   │
│  │  │ port 3000        │ DNS    │ port 8000      │    │   │
│  │  │ nodePort: 30080  │service │                │    │   │
│  │  │ Type: External   │discov  │ Type: Internal │    │   │
│  │  │ Access: Host     │        │ Access: Pod    │    │   │
│  │  └──────┬──────────┘        └──────┬──────────┘    │   │
│  │         │                          │                │   │
│  │         │                    ┌─────▼──────────┐    │   │
│  │         │                    │ Storage:       │    │   │
│  │         │                    │ emptyDir       │    │   │
│  │         │                    │ /app/db/       │    │   │
│  │         │                    │ SQLite         │    │   │
│  │         │                    └────────────────┘    │   │
│  │         │                                           │   │
│  └─────────┼───────────────────────────────────────────┘   │
│            │                                                 │
├────────────┼─────────────────────────────────────────────────┤
│ HOST MACHINE (8GB RAM)                                       │
│ Windows with Docker Desktop + WSL2                          │
└────────────┼─────────────────────────────────────────────────┘
             │
             ▼
    ┌─────────────────┐
    │  Browser        │
    │ localhost:30080 │  ◄── Access Frontend
    └─────────────────┘
```

## Kubernetes Resources Topology

```
HELM RELEASE: todo-app
├── Umbrella Chart (helm/todo-app/)
│   ├── Chart.yaml (version: 1.0.0)
│   ├── values.yaml (parent config)
│   ├── Chart.lock (dependency lock)
│   │
│   └── charts/
│       ├── frontend/ (sub-chart)
│       │   ├── Chart.yaml
│       │   ├── values.yaml
│       │   ├── templates/
│       │   │   ├── deployment.yaml
│       │   │   │   └── Container (Next.js)
│       │   │   │       ├── Image: todo-frontend:latest (200-300MB)
│       │   │   │       ├── Port: 3000
│       │   │   │       ├── Env: BACKEND_URL
│       │   │   │       ├── Resources: 128Mi req / 256Mi limit
│       │   │   │       └── Logs: stdout → kubectl logs
│       │   │   │
│       │   │   ├── service.yaml
│       │   │   │   └── NodePort
│       │   │   │       ├── port: 3000
│       │   │   │       ├── nodePort: 30080
│       │   │   │       └── Selector: app=frontend
│       │   │   │
│       │   │   └── NOTES.txt (access instructions)
│       │   │
│       │   └── .helmignore
│       │
│       └── backend/ (sub-chart)
│           ├── Chart.yaml
│           ├── values.yaml
│           ├── templates/
│           │   ├── deployment.yaml
│           │   │   └── Container (FastAPI)
│           │   │       ├── Image: todo-backend:latest (120-180MB)
│           │   │       ├── Port: 8000
│           │   │       ├── Env: DATABASE_URL
│           │   │       ├── Resources: 256Mi req / 512Mi limit
│           │   │       ├── Volume: emptyDir @ /app/db
│           │   │       └── Logs: stdout → kubectl logs
│           │   │
│           │   ├── service.yaml
│           │   │   └── ClusterIP
│           │   │       ├── port: 8000
│           │   │       └── Selector: app=backend
│           │   │
│           │   └── NOTES.txt
│           │
│           └── .helmignore
```

## Service Communication Flow

```
USER BROWSER
    │
    ├─ GET http://minikube-ip:30080/
    │    ▼
    ├─► Kubernetes Node
    │    ▼
    ├─► Service frontend (NodePort 30080)
    │    ▼
    ├─► Deployment frontend
    │    ▼
    └─► Pod frontend (Next.js container)
         ▼
         Renders HTML
         Injects API URL: http://backend.default.svc.cluster.local:8000
         ▼
    USER BROWSER EXECUTES JAVASCRIPT
         ▼
    FETCH http://backend.default.svc.cluster.local:8000/api/todos
         ▼
    Kubernetes DNS Resolver
         ▼
    Service backend (ClusterIP)
         ▼
    Deployment backend
         ▼
    Pod backend (FastAPI container)
         ▼
    Returns JSON response
         ▼
    Browser receives and renders
```

## Docker Image Build Process

### Next.js (Multi-Stage)
```
Stage 1: Builder
  FROM node:18-alpine
  COPY package.json
  RUN npm install
  COPY source code
  RUN npm run build
  ▼ Creates /app/.next build artifacts

Stage 2: Runner
  FROM node:18-alpine
  COPY --from=builder /app/.next (build artifacts only)
  COPY --from=builder /app/node_modules (production deps only)
  COPY public/ (static assets)
  ▼ Final image: 200-300MB

Final Container
  ├─ OS Base: 170MB (alpine)
  ├─ Node.js Runtime: 30MB
  ├─ node_modules: 50-100MB (prod only)
  └─ App code: 5-10MB
```

### FastAPI (Multi-Stage)
```
Stage 1: Builder
  FROM python:3.11-slim
  COPY requirements.txt
  RUN pip install --user (to /root/.local)
  ▼ Creates /root/.local with dependencies

Stage 2: Runtime
  FROM python:3.11-slim
  COPY --from=builder /root/.local (only dependencies)
  COPY source code
  ▼ Final image: 120-180MB

Final Container
  ├─ OS Base: 180MB (slim)
  ├─ Python Runtime: 30MB
  ├─ Dependencies: 20-50MB
  └─ App code: 5MB
```

**Comparison:**
```
Single-Stage Next.js:    ~1.2GB  (includes build tools, node-sass, etc.)
Multi-Stage Next.js:     ~250MB  (75% smaller)

Single-Stage FastAPI:    ~500MB  (includes gcc, build tools)
Multi-Stage FastAPI:     ~150MB  (70% smaller)

Combined Total (Multi-Stage): ~400MB
```

## Resource Allocation on 8GB Laptop

```
Physical Machine (8GB = 8192MB)
│
├─ Host OS: ~2GB (Windows, system services)
│
└─ Minikube Allocation: 6GB (6144MB)
    │
    ├─ Kubernetes System: 512MB
    │  ├─ etcd (key-value store)
    │  ├─ API server
    │  ├─ Controller manager
    │  └─ kubelet
    │
    ├─ Frontend Pod: 256MB (limit)
    │  ├─ Request: 128MB (guaranteed)
    │  └─ Limit: 256MB (max)
    │
    ├─ Backend Pod: 512MB (limit)
    │  ├─ Request: 256MB (guaranteed)
    │  └─ Limit: 512MB (max)
    │
    ├─ Other Services: 50MB
    │
    └─ Buffer/Headroom: 3.5GB (57%)
        └─ Available for spikes and Minikube overhead

Utilization: ~43% (healthy, not overloaded)
```

## Data Flow Architecture

### Request Path: Frontend to Backend

```
Browser
  │
  ├─ JavaScript (React/TypeScript)
  │  fetch('http://backend.default.svc.cluster.local:8000/api/todos')
  │  │
  │  ├─ TCP/IP Stack
  │  │  │
  │  ├─ Kubernetes CoreDNS
  │  │  backend.default.svc.cluster.local → 10.0.0.x (ClusterIP)
  │  │  │
  │  ├─ Service Mesh (Networking)
  │  │  ClusterIP Routes to Pod IP
  │  │  │
  │  ├─ FastAPI Server
  │  │  @app.get("/api/todos")
  │  │  │
  │  ├─ Database Query
  │  │  sqlite3 /app/db/todo.db
  │  │  │
  │  └─ Response: JSON array
  │
  └─ Browser Renders
```

### Storage Path: Database in Pod

```
Pod: backend
  │
  ├─ FastAPI Application (/app)
  │  │
  │  ├─ src/main.py
  │  ├─ requirements.txt
  │  └─ db/ (Volume Mount: emptyDir)
  │     │
  │     └─ todo.db (SQLite Database)
  │        ├─ Created at first run
  │        ├─ Persists during pod lifetime
  │        ├─ LOST on pod restart
  │        └─ LOST on cluster shutdown
  │
  └─ Logs
     ├─ stdout (all print and logging)
     ├─ stderr (exceptions)
     └─ Captured by Docker/Kubernetes
        └─ Accessible via: kubectl logs -f deployment/backend
```

## Deployment Sequence

```
1. Developer: helm install todo-app ./helm/todo-app
   │
   ├─► Helm reads Chart.yaml
   ├─► Helm processes values.yaml
   ├─► Helm renders template files
   │   ├─ deployment.yaml (Deployment object)
   │   ├─ service.yaml (Service object)
   │   └─ NOTES.txt (instructions)
   │
   └─► Helm sends to Kubernetes API

2. Kubernetes API Server
   │
   ├─► Accepts Deployment objects
   ├─► Stores in etcd (database)
   ├─► Notifies Deployment Controller
   │
   └─► Kubernetes Scheduler

3. Scheduler
   │
   ├─► Checks resource requirements
   ├─► Checks Node capacity
   ├─► Schedules Pods to Nodes
   │
   └─► Kubelet

4. Kubelet (Node Agent)
   │
   ├─► Receives Pod spec
   ├─► Pulls Docker image
   │   ├─ frontend: todo-frontend:latest (200-300MB)
   │   └─ backend: todo-backend:latest (120-180MB)
   ├─► Starts container
   ├─► Monitors health
   │
   └─► Pod Running

5. Service Controller
   │
   ├─► Creates Virtual IP (ClusterIP)
   ├─► Routes traffic to Pod IP
   │
   └─► Service Ready

Result: Deployment Complete
├─ Frontend accessible at http://minikube-ip:30080
└─ Backend accessible at http://backend.default.svc.cluster.local:8000
```

## Week-by-Week Implementation Timeline

### Week 1: Core Infrastructure
```
Day 1-2:
  ├─ Create Dockerfile for frontend (multi-stage)
  ├─ Create Dockerfile for backend (multi-stage)
  └─ Build and test images locally

Day 3-4:
  ├─ Create Helm chart structure
  ├─ Create frontend sub-chart
  ├─ Create backend sub-chart
  └─ Write service definitions

Day 5:
  ├─ Deploy to Minikube
  ├─ Verify pods are running
  ├─ Test external access to frontend
  └─ Test internal communication
```

### Week 2: Service Integration
```
Day 1-2:
  ├─ Configure environment variables
  ├─ Set backend URL in frontend
  └─ Test frontend can reach backend

Day 3-4:
  ├─ Set up logging
  ├─ View logs with kubectl logs
  ├─ Test debugging with port-forward
  └─ Document troubleshooting commands

Day 5:
  ├─ Load test with concurrent users
  ├─ Monitor resource usage
  ├─ Verify health checks
  └─ Stress test with large data
```

### Week 3: Advanced Topics
```
Day 1-2:
  ├─ Add PersistentVolumeClaim
  ├─ Upgrade to PostgreSQL
  └─ Test data persistence

Day 3-4:
  ├─ Create ConfigMap for settings
  ├─ Create Secret for credentials
  └─ Inject into deployments

Day 5:
  ├─ Add NetworkPolicy
  ├─ Restrict traffic patterns
  └─ Document security model
```

### Week 4: Production Readiness
```
Day 1-2:
  ├─ Separate frontend and backend charts
  ├─ Version independently
  └─ Test separate deployments

Day 3-4:
  ├─ Add Ingress Controller
  ├─ Replace NodePort with Ingress
  └─ Test with custom domain

Day 5:
  ├─ Horizontal Pod Autoscaling
  ├─ Load test autoscaling
  └─ Document production migration
```

## Technology Stack Summary

```
LAYER               | TECHNOLOGY          | VERSION    | ROLE
────────────────────┼──────────────────────┼────────────┼──────────────────
Frontend            | Next.js              | 14+        | React framework
Framework           | React + TypeScript   | Latest     | UI rendering
Styling             | Tailwind CSS         | 3+         | CSS utility

Backend             | FastAPI              | 0.100+     | API framework
Runtime             | Python               | 3.11       | Runtime
Database            | SQLite               | 3+         | Development DB
Server              | Uvicorn              | 0.23+      | ASGI server

Containerization    | Docker               | 24+        | Image building
Orchestration       | Kubernetes           | 1.28+      | Container mgmt
Package Manager     | Helm                 | 3.13+      | K8s packages
Local Dev           | Minikube             | 1.32+      | Local cluster

OS (Development)    | Windows              | 10 21H2+   | Host OS
VM/Runtime          | Docker Desktop       | 4.1+       | Container runtime
Shell               | WSL2 / Git Bash      | Latest     | Terminal
Version Control     | Git                  | 2.40+      | Source control
```

## Decision Dependencies Map

```
                    ┌─────────────────────────────┐
                    │  8GB RAM Constraint         │
                    │  (Student Laptop)           │
                    └──────────────┬──────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
           ┌─────────┐      ┌──────────┐     ┌──────────────┐
           │Resource │      │ Storage  │     │ Minikube     │
           │ Limits  │      │ Strategy │     │ Driver       │
           └────┬────┘      └────┬─────┘     └──────┬───────┘
                │                │                  │
                └────────────────┼──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │ Docker Image Structure   │
                    │ (Multi-stage optimized)  │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  Helm Chart Layout       │
                    │  (Umbrella structure)    │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  Service Types           │
                    │  (NodePort + ClusterIP)  │
                    └─────────────────────────┘
                                 │
                            Deployment!
```

## Success Metrics

### Week 1 (Core Deployment)
- [ ] Dockerfile builds successfully with <40 seconds total
- [ ] Images sizes: Frontend <300MB, Backend <200MB
- [ ] Helm install completes in <2 minutes
- [ ] All pods reach Running state
- [ ] Frontend accessible at `minikube service frontend --url`

### Week 2 (Integration)
- [ ] Frontend successfully calls backend API
- [ ] Response time for API calls <500ms (local)
- [ ] Logs visible in `kubectl logs`
- [ ] Port-forward debugging works
- [ ] Database operations persist during pod lifetime

### Week 3 (Advanced)
- [ ] Data persists across pod restarts (PVC)
- [ ] ConfigMap and Secrets properly injected
- [ ] PostgreSQL connection verified
- [ ] NetworkPolicy restricts unexpected traffic

### Week 4 (Production)
- [ ] Separate charts work independently
- [ ] Ingress routes traffic correctly
- [ ] Autoscaling scales based on CPU
- [ ] Deployment to cloud provider succeeds

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Pod OOMKilled (out of memory) | Medium | High | Generous limits, resource requests |
| Docker image pulls fail | Low | High | Use IfNotPresent, local registry |
| Service discovery fails | Low | High | Document DNS format, test early |
| Storage lost on pod restart | High | Low | Document ephemeral nature, upgrade path |
| Minikube runs out of space | Low | Medium | Use --disk-size=40g, cleanup old images |
| WSL2 performance issues | Medium | Medium | Fallback to VirtualBox driver |

---

This architecture balances educational clarity with real-world best practices, making it ideal for student learning while maintaining a clear path to production deployment.
