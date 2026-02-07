# START HERE: Kubernetes Deployment Research Documentation

Welcome! This directory contains comprehensive research and specifications for deploying a Next.js frontend and FastAPI backend to Minikube using Helm charts.

**Total Documentation:** 3,328 lines across 8 markdown files | ~120KB

---

## What You Get

A complete, research-backed guide covering:

1. **Docker Image Structure** - Multi-stage vs single-stage builds
2. **Helm Chart Layout** - Umbrella vs separate charts
3. **Service Types** - NodePort vs ClusterIP for Minikube
4. **Resource Limits** - Proper allocation for 8GB laptops
5. **Storage Strategy** - Ephemeral vs persistent storage
6. **Minikube Driver** - Docker vs VirtualBox on Windows

Each decision includes:
- Detailed rationale with empirical data
- Alternatives considered and why they were rejected
- Trade-offs analysis
- Implementation examples
- Week-by-week learning progression

---

## Quick Navigation

### I have 5 minutes
Read this page, then go to [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) and skim the decision boxes.

**Key takeaways:**
- Multi-stage Docker builds: 75% smaller images
- Umbrella Helm chart: Single deployment for both services
- Frontend: NodePort (external), Backend: ClusterIP (internal)
- Resources: Frontend 128/256Mi, Backend 256/512Mi
- Storage: Ephemeral SQLite with emptyDir
- Driver: Docker (or VirtualBox fallback)

### I have 30 minutes
1. Read [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md) - Visual diagrams and flows
2. Skim [research.md](./research.md) - Section summaries
3. Review [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) - Implementation details

### I have 2 hours
This is the recommended approach:
1. **Start:** [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md) (15 min)
   - Understand the complete architecture
   - See how components connect
   - Visualize data flows

2. **Learn:** [research.md](./research.md) (45 min)
   - Deep dive into each decision area
   - Understand the rationale
   - Review alternatives and trade-offs

3. **Plan:** [plan.md](./plan.md) & [README.md](./README.md) (15 min)
   - Understand implementation phases
   - Review 4-week learning progression
   - See production differences

4. **Implement:** [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) (15 min)
   - Copy YAML examples
   - Follow implementation checklist
   - Reference verification commands

5. **Navigate:** [INDEX.md](./INDEX.md) (10 min)
   - Understand document structure
   - Learn how to find information
   - Know where to go for specific topics

### I want to implement right now
1. Go to [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md)
2. Follow the implementation checklist
3. Copy YAML snippets for your Helm chart
4. Run testing commands to verify
5. Return to [research.md](./research.md) for any "why" questions

### I need to understand the "why"
1. Go to [research.md](./research.md)
2. Find your topic in the table of contents
3. Read the detailed section
4. Check "Decision Rationale" and "Alternatives Considered"
5. Review trade-offs table

### I'm teaching students
1. Use [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md) for diagrams
2. Use [research.md](./research.md) for explaining decisions
3. Use [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) for code examples
4. Follow 4-week progression in [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md)
5. Use [spec.md](./spec.md) for acceptance criteria

---

## Document Overview

### [research.md](./research.md) - 1,350 lines | The Authority
Comprehensive technical research covering all six decision areas with:
- Empirical performance data
- Detailed alternatives analysis
- Trade-offs tables
- Production best practices
- References and sources

**Read when:** You need to understand WHY each decision was made

---

### [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) - 344 lines | Quick Reference
Practical guide with:
- Copy-paste ready Dockerfiles
- YAML configuration examples
- Installation commands
- Implementation checklist
- Verification commands
- One-page reference tables

**Read when:** You're implementing and need code examples

---

### [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md) - 525 lines | Visual Design
Complete architecture with:
- ASCII art diagrams
- Resource topology
- Service communication flows
- Data flow architecture
- Deployment sequence
- Week-by-week timeline
- Success metrics

**Read when:** You want to understand the complete system design

---

### [README.md](./README.md) - 288 lines | Navigation Guide
Overview of entire documentation:
- Document structure explanation
- Usage patterns for different roles
- How to use each document
- Implementation progression
- Research methodology
- Common questions with answers

**Read when:** You're new to this documentation and need guidance

---

### [INDEX.md](./INDEX.md) - 482 lines | Complete Index
Comprehensive index with:
- Content by technical topic
- Content by audience level
- Navigation maps
- File statistics
- Cross-references
- Document maintenance guidelines

**Read when:** You're looking for specific information

---

### [spec.md](./spec.md) - 190 lines | Formal Specification
SDD-formatted requirements:
- Scope and constraints
- Acceptance criteria
- Non-functional requirements
- Dependencies and risks

**Read when:** You need formal requirements or project management

---

### [plan.md](./plan.md) - 104 lines | Implementation Plan
Phase-based plan:
- Phase breakdown
- Milestone definitions
- Task allocation
- Timeline

**Read when:** You're planning the project timeline

---

### [checklists/requirements.md](./checklists/requirements.md) - 45 lines | Validation
Detailed verification checklist for acceptance testing.

**Read when:** You're validating the implementation

---

## The Six Key Decisions

### 1. Docker Image Structure: Multi-Stage Builds
```
Result: 75% smaller images
Next.js: 200-300MB (vs 1.2GB single-stage)
FastAPI: 120-180MB (vs 500MB single-stage)
Why: Better caching, faster CI/CD, production best practice
```
[Read in research.md →](./research.md)

### 2. Helm Chart Layout: Umbrella with Sub-Charts
```
Result: Single deployment command
helm install todo-app ./helm/todo-app
Deploys: Frontend + Backend together
Why: Clear for learning, unified versioning, coordinated deployment
```
[Read in research.md →](./research.md)

### 3. Service Types: NodePort + ClusterIP
```
Frontend: NodePort 30080 (external access for UI)
Backend: ClusterIP 8000 (internal only, more secure)
Why: UI needs external access, API stays internal
```
[Read in research.md →](./research.md)

### 4. Resource Limits: Conservative with Headroom
```
Frontend: 128Mi request / 256Mi limit
Backend: 256Mi request / 512Mi limit
Minikube: 6GB allocated to cluster
Total utilization: 43% (57% buffer for spikes)
Why: Safe for 8GB laptop, prevents crashes, teaches responsibility
```
[Read in research.md →](./research.md)

### 5. Storage Strategy: Ephemeral SQLite
```
Database: Embedded SQLite with emptyDir
Logs: stdout/stderr captured by Kubernetes
Static: Built into Next.js image
Why: Zero setup, teaches containerization, can upgrade in Week 3
```
[Read in research.md →](./research.md)

### 6. Minikube Driver: Docker (Primary) + VirtualBox (Fallback)
```
Recommended: Docker driver
- Lowest overhead (~500MB)
- Fastest startup (15-20 sec)
- Requires: Docker Desktop + WSL2

Fallback: VirtualBox driver
- Works on any Windows version
- Acceptable overhead (~2-3GB)
- Slower startup (45-60 sec)
```
[Read in research.md →](./research.md)

---

## Decision Summary Table

| Area | Decision | Benefit | Trade-off |
|------|----------|---------|-----------|
| Docker | Multi-stage | 75% smaller images | Slightly slower first build |
| Helm | Umbrella chart | Single deployment | Less service independence |
| Services | NodePort + ClusterIP | UI access + security | Standard port range limits |
| Resources | Conservative | Safe for 8GB laptop | Tight constraints require efficiency |
| Storage | Ephemeral | Zero setup, learning focus | Data lost on restart (OK for Week 1-2) |
| Driver | Docker primary | Lowest overhead, fastest | Requires Docker Desktop + WSL2 |

---

## Learning Progression (4 Weeks)

### Week 1: Core Deployment
- Create multi-stage Dockerfiles
- Create umbrella Helm chart
- Deploy to Minikube
- Verify frontend and backend running

### Week 2: Service Integration
- Configure service discovery
- Test frontend ↔ backend communication
- Learn logging with kubectl logs
- Debug with port-forward

### Week 3: Advanced Topics
- Add PersistentVolumeClaim
- Upgrade to PostgreSQL
- Create ConfigMaps and Secrets
- Optional: NetworkPolicies

### Week 4: Production Patterns
- Separate charts for services
- Add Ingress Controller
- Horizontal pod autoscaling
- Security hardening

---

## Implementation Checklist

Quick verification that you're ready:

### Before You Start
- [ ] Understand the 6 decisions (read DECISIONS_SUMMARY.md)
- [ ] Have 8GB RAM laptop available
- [ ] Have Docker Desktop installed (or VirtualBox)
- [ ] Have Minikube installed
- [ ] Have Helm 3.13+ installed

### Week 1: Build & Deploy
- [ ] Create multi-stage Dockerfile for frontend
- [ ] Create multi-stage Dockerfile for backend
- [ ] Build and test images locally
- [ ] Create umbrella Helm chart
- [ ] Deploy to Minikube
- [ ] Verify pods are running
- [ ] Test external access to frontend
- [ ] Verify resource allocation

### Week 2: Integration & Debugging
- [ ] Configure environment variables
- [ ] Test backend API from frontend
- [ ] Set up logging
- [ ] Test port-forward debugging
- [ ] Document troubleshooting commands
- [ ] Load test and monitor resources

### Week 3: Persistence
- [ ] Add PersistentVolumeClaim
- [ ] Upgrade to PostgreSQL
- [ ] Test data persistence
- [ ] Create ConfigMap and Secret

### Week 4: Production
- [ ] Separate frontend and backend charts
- [ ] Add Ingress Controller
- [ ] Test Ingress routing
- [ ] Add horizontal pod autoscaling
- [ ] Document production migration path

---

## Testing & Verification

After deploying, run these commands to verify:

```bash
# Check Minikube status
minikube status

# Verify deployments
kubectl get deployments
kubectl get pods
kubectl get services

# Test frontend access
minikube service frontend --url

# View logs
kubectl logs -f deployment/frontend
kubectl logs -f deployment/backend

# Check resources
kubectl top pods
kubectl top nodes

# Describe for debugging
kubectl describe pod <pod-name>
```

---

## Production Deployment

When ready to move to production, these change:

| Aspect | Development | Production |
|--------|-------------|-----------|
| Service Type | NodePort | Ingress + LoadBalancer |
| Resources | Generous | Tight, forces efficiency |
| Storage | ephemeral | Cloud-managed PersistentVolumes |
| Logging | stdout | Central system (ELK, Datadog) |
| Replicas | 1 | 3+ for high availability |
| Database | SQLite embedded | Managed service (RDS, Cloud SQL) |
| Platform | Minikube local | Cloud Kubernetes (EKS, GKE, AKS) |

---

## Recommended Reading Order

### Path A: Visual Learner
1. ARCHITECTURE_OVERVIEW.md (visual understanding)
2. DECISIONS_SUMMARY.md (implementation details)
3. research.md (deep dive on interesting topics)

### Path B: Details-First
1. research.md (understand all decisions)
2. ARCHITECTURE_OVERVIEW.md (see connections)
3. DECISIONS_SUMMARY.md (implement)

### Path C: Practitioner (Just Build)
1. DECISIONS_SUMMARY.md (copy examples)
2. ARCHITECTURE_OVERVIEW.md (understand flows)
3. research.md (reference as needed)

### Path D: Educator/Manager
1. README.md (understand structure)
2. ARCHITECTURE_OVERVIEW.md (explain to others)
3. research.md (answer "why" questions)
4. spec.md (formal requirements)

---

## Document Statistics

```
Total Lines:   3,328
Total Size:    ~120KB
Read Time:     1.5-2 hours (complete)
Sections:      32 major sections
Examples:      50+ code examples
Diagrams:      15+ ASCII diagrams
Tables:        25+ reference tables
```

---

## Troubleshooting This Documentation

**I'm confused about Docker vs Helm**
→ Read ARCHITECTURE_OVERVIEW.md - Visual Architecture Diagram

**I don't understand why this decision was made**
→ Read research.md for "Decision Rationale" and "Alternatives Considered"

**I need code examples**
→ Go to DECISIONS_SUMMARY.md - it's all YAML and configuration examples

**I want to know how long this takes to implement**
→ See ARCHITECTURE_OVERVIEW.md - Week-by-Week Implementation Timeline

**I need to teach this to students**
→ See README.md - "For Student Teaching" section

**I'm ready to implement but not sure what to do first**
→ Go to DECISIONS_SUMMARY.md and follow the Implementation Checklist

---

## Key Files Referenced in This Documentation

### From Your Project
- `phase3/backend/Dockerfile` - Will be upgraded to multi-stage
- `phase3/frontend/` - Next.js application
- `phase3/backend/` - FastAPI application
- `./.claude/agents/k8s-minikube-helm.md` - K8s agent specifications

### To Create
- `helm/todo-app/Chart.yaml` - Umbrella chart manifest
- `helm/todo-app/values.yaml` - Chart configuration
- `helm/todo-app/charts/frontend/` - Frontend sub-chart
- `helm/todo-app/charts/backend/` - Backend sub-chart
- Updated Dockerfiles with multi-stage builds

---

## Support & Questions

**General navigation?** → Read INDEX.md

**Quick reference needed?** → Use DECISIONS_SUMMARY.md

**Want to understand decisions?** → Read research.md

**Need diagrams?** → See ARCHITECTURE_OVERVIEW.md

**Planning the project?** → Review plan.md and spec.md

**Teaching others?** → Use README.md "For Student Teaching" section

---

## Next Steps

1. **Right now (5 min):** Skim DECISIONS_SUMMARY.md to understand what you'll build
2. **Next (15 min):** Read ARCHITECTURE_OVERVIEW.md to see how it all connects
3. **Then (30 min):** Read research.md sections relevant to your interests
4. **Finally:** Follow DECISIONS_SUMMARY.md implementation checklist to build

---

## About This Documentation

Created: January 30, 2026

These specifications are designed for:
- Student learning on resource-constrained laptops (8GB RAM)
- Educational progression (4 weeks, increasing complexity)
- Real-world applicable architecture (can scale to production)
- Clear decision documentation with alternatives analyzed
- Comprehensive examples and verification steps

All recommendations are based on:
- Empirical performance data
- Industry best practices
- Student learning objectives
- Resource constraints (8GB RAM)
- Production applicability

---

## Quick Decision Reference

### Dockerfile
```dockerfile
# Use multi-stage builds
# FROM ... AS builder
# RUN compile/build
# FROM ... (final)
# COPY --from=builder (artifacts only)
```

### Helm Chart
```
helm/todo-app/              (umbrella)
├── charts/frontend/        (sub-chart)
└── charts/backend/         (sub-chart)
helm install todo-app ./helm/todo-app
```

### Services
```yaml
# Frontend
type: NodePort
nodePort: 30080

# Backend
type: ClusterIP
port: 8000
```

### Resources
```yaml
# Frontend
requests: {cpu: 100m, memory: 128Mi}
limits: {cpu: 500m, memory: 256Mi}

# Backend
requests: {cpu: 100m, memory: 256Mi}
limits: {cpu: 1000m, memory: 512Mi}
```

### Storage
```yaml
volume: emptyDir  # Ephemeral
mountPath: /app/db
```

### Minikube
```bash
minikube start \
  --driver=docker \
  --memory=6144 \
  --cpus=4 \
  --disk-size=40g
```

---

## You're All Set!

You now have:
- Complete technical research on all 6 decision areas
- Detailed rationale for each choice
- Implementation examples and checklists
- Visual architecture diagrams
- Week-by-week learning progression
- Production migration guidance

**Pick your path above and start reading!**

---

**Next:** [README.md](./README.md) or [ARCHITECTURE_OVERVIEW.md](./ARCHITECTURE_OVERVIEW.md)
