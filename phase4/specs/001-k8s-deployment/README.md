# Kubernetes Deployment Specifications: Next.js + FastAPI on Minikube with Helm

## Overview

This directory contains comprehensive research and specifications for deploying a Next.js frontend and FastAPI backend to Minikube using Helm charts. The documentation is designed for educational purposes, optimized for student learning on resource-constrained laptops (8GB RAM).

## Document Structure

### 1. [research.md](./research.md) - Comprehensive Technical Research
**Length:** 1,350 lines | **Size:** 39KB

The authoritative research document covering all six technical decision areas:

#### Section 1: Docker Image Structure (175 lines)
- Multi-stage vs single-stage build analysis
- Performance implications with metrics
- Image size optimization strategies
- Build time considerations
- Production best practices
- Decision rationale and alternatives

#### Section 2: Helm Chart Layout (220 lines)
- Umbrella (mono-chart) vs separate charts comparison
- When to use each approach
- Dependency management between services
- Versioning and release strategies
- Lockstep vs independent versioning
- Trade-offs analysis

#### Section 3: Service Types & Accessibility (280 lines)
- NodePort vs ClusterIP vs LoadBalancer comparison
- Frontend service design (NodePort)
- Backend service design (ClusterIP)
- Port-forward for debugging
- Accessibility patterns for Minikube
- Security considerations with NetworkPolicy examples
- Best practices for student learning

#### Section 4: Resource Limits (200 lines)
- Kubernetes resource model (requests vs limits)
- Frontend resource allocation with rationale
- Backend resource allocation with rationale
- Minikube cluster sizing for 8GB laptops
- Detailed resource calculations and breakdown
- Multi-container scaling
- Production vs learning environment differences

#### Section 5: Storage Strategy (250 lines)
- Ephemeral storage rationale
- Embedded SQLite for development
- Logs strategy (stdout capture)
- Static assets approach
- Persistence upgrade path
- Minikube storage classes
- Storage best practices for learning

#### Section 6: Minikube Driver Selection (200 lines)
- Docker driver (recommended primary)
- VirtualBox driver (fallback)
- Hyper-V driver (not recommended)
- Driver comparison matrix
- Windows-specific considerations
- WSL2 integration details
- Installation and switching drivers
- Performance metrics for each driver

#### Additional Content
- Summary table of all decisions
- Implementation progression for learning (4-week plan)
- References and data sources
- Conclusion

### 2. [DECISIONS_SUMMARY.md](./DECISIONS_SUMMARY.md) - Quick Reference Guide
**Length:** 350 lines | **Size:** 8.4KB

Practical, implementation-focused summary with:
- Docker Dockerfile examples (Next.js and FastAPI)
- Helm chart structure diagram
- YAML configuration snippets
- Service definitions and access patterns
- Resource allocation specifications
- Storage configuration examples
- Minikube startup commands
- Testing and verification commands
- Implementation checklist (4 phases)
- Production differences table
- Key learnings for students
- Next steps

**Use this document for:**
- Quick reference during implementation
- Copy-paste ready YAML examples
- Checklists and verification steps
- When you know what you need but forgot the exact syntax

### 3. [spec.md](./spec.md) - Formal Specification
**Size:** 13KB

Formal requirements specification using SDD (Spec-Driven Development) format with:
- Scope and constraints
- Acceptance criteria
- Feature descriptions
- Non-functional requirements
- Dependencies and risks

### 4. [plan.md](./plan.md) - Implementation Plan
**Size:** 3.6KB

Architectural plan with implementation phases and task breakdown.

## Decision Summary Matrix

| Area | Decision | Key Benefit | Trade-off |
|------|----------|-----------|-----------|
| **Docker Images** | Multi-stage builds | 75% size reduction | Slightly slower first build |
| **Helm Charts** | Umbrella with sub-charts | Single deployment, unified versioning | Less service independence |
| **Services** | Frontend: NodePort, Backend: ClusterIP | UI access + security | NodePort port range limit |
| **Resources** | Conservative with headroom | Safe for 8GB laptop | Tight constraints force efficiency |
| **Storage** | Ephemeral (SQLite + emptyDir) | Zero setup, educational progression | Data lost on pod restart (acceptable for learning) |
| **Driver** | Docker (primary), VirtualBox (fallback) | Lowest overhead, fastest startup | Requires Docker Desktop + WSL2 |

## Key Specifications at a Glance

### Docker Image Sizes
- Next.js: 200-300MB (multi-stage) vs 1.2GB (single-stage)
- FastAPI: 120-180MB (multi-stage) vs 500MB (single-stage)

### Resource Allocation
- Frontend: 128Mi request / 256Mi limit (CPU: 100m request / 500m limit)
- Backend: 256Mi request / 512Mi limit (CPU: 100m request / 1000m limit)
- Minikube: 6GB allocated to cluster, 4 CPU cores

### Service Configuration
- Frontend: `type: NodePort, nodePort: 30080`
- Backend: `type: ClusterIP, port: 8000`
- Service Discovery: `http://backend.default.svc.cluster.local:8000`

### Storage
- Database: SQLite with emptyDir (ephemeral)
- Logs: stdout/stderr captured by Kubernetes
- Static Assets: Built into Next.js image

### Minikube Setup
```bash
minikube start --driver=docker --memory=6144 --cpus=4 --disk-size=40g
```

## How to Use These Documents

### For Quick Implementation
1. Start with **DECISIONS_SUMMARY.md**
2. Copy YAML snippets for your Helm chart
3. Use implementation checklist to verify
4. Reference **research.md** for rationale

### For Deep Understanding
1. Read **spec.md** for formal requirements
2. Read **research.md** section by section
3. Understand the rationale behind each decision
4. Review trade-offs and alternatives
5. Consult **DECISIONS_SUMMARY.md** for code examples

### For Student Teaching
1. Use **DECISIONS_SUMMARY.md** for Week 1 implementation
2. Reference **research.md** for explaining design choices
3. Follow 4-week implementation progression plan
4. Assign reading sections to deepen understanding

### For Production Migration
1. Review "Production Differences" section in DECISIONS_SUMMARY.md
2. Reference production changes table
3. Adapt service types (NodePort → Ingress)
4. Scale up resources and add replicas
5. Implement persistent storage and cloud databases

## Research Methodology

All recommendations in this document are based on:

1. **Empirical Data**
   - Actual memory usage measurements from Next.js and FastAPI
   - Docker image size benchmarks
   - Minikube performance metrics

2. **Industry Best Practices**
   - Kubernetes documentation
   - CNCF guidelines
   - Docker best practices
   - Helm chart design patterns

3. **Educational Considerations**
   - Appropriate complexity for learning
   - Clear progression paths
   - Production-compatible practices
   - Student resource constraints

4. **Technical Constraints**
   - 8GB RAM laptop limitation
   - Windows compatibility
   - Local Minikube capabilities
   - Container orchestration limitations

## Implementation Progression

### Week 1: Core Deployment
- Multi-stage Docker builds
- Umbrella Helm chart
- Resource requests and limits
- Basic deployment and access

### Week 2: Service Communication
- Kubernetes DNS discovery
- Environment variable configuration
- Port-forward debugging
- Log investigation

### Week 3: Persistence & Advanced
- PersistentVolumeClaim
- PostgreSQL upgrade
- ConfigMaps and Secrets
- NetworkPolicies (optional)

### Week 4: Production Patterns
- Separate charts for services
- Ingress controller
- Horizontal pod autoscaling
- Security hardening

## Verification Steps

After implementing the specifications:

```bash
# 1. Start Minikube
minikube start --driver=docker --memory=6144 --cpus=4

# 2. Deploy Helm chart
helm install todo-app ./helm/todo-app

# 3. Verify deployments
kubectl get deployments
kubectl get pods
kubectl get services

# 4. Test frontend access
minikube service frontend --url

# 5. Test service communication
kubectl logs -f deployment/frontend | grep "backend"

# 6. Verify resource allocation
kubectl describe pod <frontend-pod-name> | grep -A 5 "Limits\|Requests"
```

## Related Files in Repository

- `/phase3/backend/Dockerfile` - Existing single-stage backend Dockerfile (will be upgraded)
- `/phase3/frontend/` - Next.js application
- `/phase3/backend/` - FastAPI application
- `./.claude/agents/k8s-minikube-helm.md` - Kubernetes deployment agent specifications

## Common Questions

**Q: Can I use a single chart instead of umbrella?**
A: Yes, but you'd run two separate helm install commands instead of one. Umbrella chart is better for learning because it shows coordinated deployment.

**Q: Do I need persistent storage?**
A: Not for Week 1-2. emptyDir is fine for learning. Add PersistentVolumeClaim in Week 3 when ready to learn about Kubernetes storage abstraction.

**Q: Should I start with PostgreSQL or SQLite?**
A: Start with embedded SQLite (zero ops overhead). Upgrade to PostgreSQL in Week 3 when students understand databases better.

**Q: Is Docker driver required?**
A: No. Docker is recommended but VirtualBox works fine as a fallback. Choose based on your system.

**Q: When should I move to production?**
A: After completing Week 4 progression. Then reference "Production Differences" section for necessary changes.

## Document Maintenance

These documents should be reviewed and updated when:
- Docker or Kubernetes versions make significant changes
- New Minikube driver becomes available
- Performance characteristics change
- Student feedback suggests clarity improvements
- Production deployment occurs and patterns change

Last Updated: January 30, 2026
