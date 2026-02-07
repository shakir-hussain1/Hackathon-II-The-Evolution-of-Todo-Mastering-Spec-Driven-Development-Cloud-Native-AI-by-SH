# Implementation Plan: Local Kubernetes Deployment

**Branch**: `001-k8s-deployment` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-k8s-deployment/spec.md`

## Summary

Deploy Phase III AI-Powered Todo Chatbot to local Kubernetes using Minikube, Docker, and Helm with AI-assisted DevOps tools (Gordon, kubectl-ai, Kagent). Enable students to learn cloud-native deployment patterns on standard laptops while maintaining production-applicable architecture.

**Key Approach**: Multi-stage Docker builds + Umbrella Helm chart + AI-first tooling + Progressive learning path (ephemeral→persistent storage over 4 weeks)

## Technical Context

**Language/Version**:
- Frontend: TypeScript/JavaScript (Next.js 16+, React 19+, Node.js 18+)
- Backend: Python 3.10+ (FastAPI, SQLModel)

**Primary Dependencies**:
- **Containerization**: Docker Desktop 24+, Gordon AI plugin
- **Orchestration**: Minikube 1.32+, kubectl 1.28+
- **Package Management**: Helm 3.13+
- **AI DevOps**: kubectl-ai, Kagent (optional with fallbacks)
- **Phase III App**: Full-stack Next.js + FastAPI todo chatbot

**Storage**: SQLite (embedded, ephemeral) with emptyDir volumes. Week 3-4 progression to PostgreSQL + PersistentVolumeClaim for advanced students.

**Testing**: Manual validation via browser access, kubectl commands, pod logs, Helm dry-run. Future: Automated integration tests with pytest/jest.

**Target Platform**: Minikube on Windows/macOS/Linux (Docker driver primary, VirtualBox fallback), 8GB RAM student laptops

**Project Type**: Web application (frontend + backend microservices)

**Performance Goals**:
- Deployment completes in <5 minutes
- Frontend loads in <3 seconds
- Backend responds to health checks in <1 second
- Supports 2+ replicas per service

**Constraints**:
- Maximum 6GB RAM allocated to Minikube (leave 2GB for host OS)
- Maximum 2 CPU cores per service
- No cloud deployment (local only)
- No manual YAML/Dockerfile writing (AI-generated)
- Must follow Spec-Driven Development workflow

**Scale/Scope**: 2 services (frontend + backend), ~10 Kubernetes resources, 2-4 week learning timeline

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on Phase IV Kubernetes Deployment Constitution v1.0.0:

### ✅ Principle I: Cloud-Native Correctness
- Resource limits and requests defined for all containers
- Health checks (liveness/readiness probes) configured
- Secrets and ConfigMaps for configuration
- Services exposed via proper Kubernetes Service objects
- Namespaces used (default namespace acceptable for learning, optional custom namespace)

### ✅ Principle II: Reproducible Local Deployments
- All steps documented with exact commands
- Resource requirements specified (6GB RAM, 2 CPU cores)
- No cloud-specific features
- Version-pinned dependencies
- Setup scripts provided

### ✅ Principle III: AI-First DevOps Automation
- Dockerfiles generated via Gordon (or documented Claude Code fallback)
- kubectl-ai for Kubernetes operations
- Kagent for cluster health analysis
- Helm charts AI-assisted (helm create + Claude Code customization)

### ✅ Principle IV: Spec-Driven Development Workflow
- Spec created (/sp.specify) ✅
- Plan in progress (/sp.plan) - this document
- Tasks next (/sp.tasks)
- Implementation last (/sp.implement)

### ✅ Principle V: Zero Manual Infrastructure Coding
- All Dockerfiles AI-generated
- All Kubernetes YAML AI-generated
- Helm charts scaffolded then AI-customized
- Manual edits only for debugging (temporary)

### ✅ Principle VI: Observable and Validated Deployments
- Pods must reach Running state
- No CrashLoopBackOff permitted
- Services accessible via browser
- Logs must show healthy startup
- Resource usage within limits

### ✅ Principle VII: Security-First Configuration
- No secrets in images or Git
- Kubernetes Secrets for JWT/API keys
- Non-root containers where possible
- Network policies (optional, Phase 4 enhancement)

**Constitution Check Status**: ✅ PASSED - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-k8s-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (COMPLETED by research agent)
├── data-model.md        # Phase 1 output (this planning phase)
├── quickstart.md        # Phase 1 output (this planning phase)
├── contracts/           # Phase 1 output (this planning phase)
│   ├── docker-builds.md # Docker image build contracts
│   ├── helm-values.md   # Helm values.yaml schema
│   └── k8s-resources.md # Kubernetes resource specifications
├── DECISIONS_SUMMARY.md # Quick reference (created by research)
├── ARCHITECTURE_OVERVIEW.md # Diagrams (created by research)
└── spec.md              # Feature specification (completed)
```

### Source Code (phase4 root - infrastructure only, app in phase3/)

```text
phase4/
├── helm/                        # Helm charts
│   └── todo-app/                # Umbrella chart
│       ├── Chart.yaml           # Chart metadata
│       ├── values.yaml          # Default configuration values
│       ├── templates/           # Kubernetes manifest templates
│       │   ├── _helpers.tpl     # Template helpers
│       │   ├── NOTES.txt        # Post-install instructions
│       │   └── namespace.yaml   # Optional custom namespace
│       └── charts/              # Sub-charts
│           ├── frontend/        # Next.js frontend chart
│           │   ├── Chart.yaml
│           │   ├── values.yaml
│           │   └── templates/
│           │       ├── deployment.yaml
│           │       ├── service.yaml
│           │       ├── configmap.yaml
│           │       └── hpa.yaml # Optional autoscaling
│           └── backend/         # FastAPI backend chart
│               ├── Chart.yaml
│               ├── values.yaml
│               └── templates/
│                   ├── deployment.yaml
│                   ├── service.yaml
│                   ├── secret.yaml
│                   └── hpa.yaml
│
├── docker/                      # Dockerfiles (AI-generated)
│   ├── frontend.Dockerfile      # Multi-stage Next.js build
│   └── backend.Dockerfile       # Multi-stage FastAPI build
│
├── scripts/                     # Automation scripts
│   ├── setup-minikube.sh        # Initialize Minikube cluster
│   ├── build-images.sh          # Build Docker images locally
│   ├── deploy-all.sh            # Full deployment automation
│   ├── cleanup.sh               # Teardown resources
│   └── ai-commands.log          # Log of all AI tool commands
│
├── .env.example                 # Environment variable template
├── README.md                    # Setup and deployment guide
└── QUICKSTART.md                # 5-minute getting started guide
```

**Structure Decision**: Web application structure (frontend + backend) with infrastructure-as-code in phase4/ and application source in phase3/. Helm umbrella chart pattern with sub-charts for frontend and backend enables independent versioning while maintaining coordinated deployment.

## Complexity Tracking

> **No constitution violations requiring justification**

All complexity is essential and justified:
- **Helm umbrella chart**: Required for coordinated multi-service deployment per FR-010
- **Multi-stage Docker builds**: Required for production-ready image optimization per FR-003
- **AI tools (Gordon, kubectl-ai, Kagent)**: Required per Constitution Principle III (AI-First DevOps)
- **Kubernetes resources (Deployment, Service, ConfigMap, Secret)**: Minimum viable set for cloud-native deployment per FR-005, FR-006, FR-008, FR-009

## Architectural Decisions Requiring ADRs

The following decisions are architecturally significant and should be documented with `/sp.adr`:

1. **Multi-Stage Docker Builds**: Long-term impact on CI/CD, image size, build caching
2. **Helm Umbrella Chart Pattern**: Affects versioning strategy, release coordination, dependency management
3. **Ephemeral-First Storage Strategy**: Impacts data persistence, backup strategy, production migration path

Suggested command: `/sp.adr multi-stage-docker-builds`

## Success Criteria Mapping

| Success Criterion | Implementation Approach | Validation Method |
|------------------|------------------------|-------------------|
| SC-001: Deployment <5 min | Optimized images, resource pre-allocation | Time deployment from helm install to all pods Running |
| SC-002: Frontend loads <3s | Multi-stage build, nginx serving static assets | Browser DevTools Network tab |
| SC-003: Backend health check <1s | FastAPI health endpoint, optimized startup | kubectl exec curl timing |
| SC-004: Support 2+ replicas | HorizontalPodAutoscaler, LoadBalancer services | kubectl scale and test functionality |
| SC-005: Helm install succeeds | helm lint, dry-run validation | helm install on clean cluster |
| SC-006: Scaling maintains functionality | Stateless design, shared ConfigMap/Secrets | Scale up/down and run integration tests |
| SC-007: Reproducible <30 min | Automated scripts, clear documentation | Fresh VM deployment test |
| SC-008: Zero secrets in images | Multi-stage builds, .dockerignore | docker history inspection |
| SC-009: kubectl-ai operations | Natural language command execution | Document 5+ successful operations |
| SC-010: Kagent analysis | Cluster health scan | Review Kagent output report |
| SC-011: Operates within 4GB/2CPU | Resource limits, requests, monitoring | kubectl top verification |
| SC-012: Instructor verification <15 min | Verification checklist, QUICKSTART.md | Instructor feedback form |

## Next Steps

1. **Generate data-model.md**: Document Kubernetes resource entities (completed below)
2. **Generate contracts/**: Docker, Helm, K8s resource contracts (completed below)
3. **Generate quickstart.md**: 5-minute and 30-minute setup guides (completed below)
4. **Run `/sp.tasks`**: Break down into actionable TDD tasks
5. **Run `/sp.implement`**: Execute implementation via Claude Code
