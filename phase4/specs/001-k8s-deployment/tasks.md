# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/001-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only included if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Infrastructure (phase4)**: `phase4/` at repository root
- **Application source**: `phase3/frontend/`, `phase3/backend/`
- **Helm charts**: `phase4/helm/`
- **Docker files**: `phase4/docker/`
- **Scripts**: `phase4/scripts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, environment validation, and prerequisite installation

- [X] T001 Create phase4 project directory structure (docker/, helm/, scripts/)
- [ ] T002 Verify Docker Desktop installed and running (version 24+) - **REQUIRES USER INSTALLATION**
- [ ] T003 [P] Install Minikube (version 1.32+) and verify installation - **REQUIRES USER INSTALLATION**
- [ ] T004 [P] Install kubectl (version 1.28+) and verify installation - **REQUIRES USER INSTALLATION**
- [ ] T005 [P] Install Helm (version 3.13+) and verify installation - **REQUIRES USER INSTALLATION**
- [ ] T006 [P] Install kubectl-ai plugin (optional, with fallback documentation) - **OPTIONAL**
- [ ] T007 [P] Install Kagent for cluster analysis (optional, with fallback documentation) - **OPTIONAL**
- [ ] T008 [P] Enable Docker AI Agent (Gordon) if available - **OPTIONAL**
- [X] T009 Create .env.example template in phase4/ with required variables
- [X] T010 Create .gitignore in phase4/ to exclude secrets and build artifacts
- [X] T011 Document environment setup steps in phase4/docs/SETUP.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T012 Start Minikube cluster with 6GB RAM and 2 CPU allocation
- [ ] T013 Verify Minikube status (all components Running)
- [ ] T014 Configure kubectl context to use Minikube cluster
- [ ] T015 Create phase4/scripts/setup-minikube.sh automation script
- [ ] T016 Test Minikube cluster connectivity with kubectl cluster-info
- [ ] T017 Document Minikube driver selection (Docker primary, VirtualBox fallback) in phase4/docs/MINIKUBE.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Containerize Applications (Priority: P1) 🎯 MVP

**Goal**: Build Docker images for frontend and backend that can run in any container environment

**Independent Test**: Run `docker run` for both images locally and verify they serve traffic without Kubernetes

### Implementation for User Story 1

- [ ] T018 [P] [US1] Analyze Phase III frontend structure in phase3/frontend/
- [ ] T019 [P] [US1] Analyze Phase III backend structure in phase3/backend/
- [ ] T020 [P] [US1] Create .dockerignore for frontend in phase3/frontend/.dockerignore
- [ ] T021 [P] [US1] Create .dockerignore for backend in phase3/backend/.dockerignore
- [ ] T022 [US1] Generate frontend Dockerfile using Gordon AI in phase4/docker/frontend.Dockerfile
- [ ] T023 [US1] Generate backend Dockerfile using Gordon AI in phase4/docker/backend.Dockerfile
- [ ] T024 [US1] Create fallback frontend Dockerfile using Claude Code if Gordon unavailable
- [ ] T025 [US1] Create fallback backend Dockerfile using Claude Code if Gordon unavailable
- [ ] T026 [US1] Build frontend Docker image (todo-frontend:v1.0.0)
- [ ] T027 [US1] Build backend Docker image (todo-backend:v1.0.0)
- [ ] T028 [US1] Validate frontend image size (<300MB) using docker images command
- [ ] T029 [US1] Validate backend image size (<200MB) using docker images command
- [ ] T030 [US1] Inspect frontend image for secrets using docker history
- [ ] T031 [US1] Inspect backend image for secrets using docker history
- [ ] T032 [US1] Test frontend container locally with docker run on port 3000
- [ ] T033 [US1] Test backend container locally with docker run on port 8000
- [ ] T034 [US1] Verify frontend health endpoint responds (http://localhost:3000/health)
- [ ] T035 [US1] Verify backend health endpoint responds (http://localhost:8000/health)
- [ ] T036 [US1] Load frontend image into Minikube using minikube image load
- [ ] T037 [US1] Load backend image into Minikube using minikube image load
- [ ] T038 [US1] Verify images available in Minikube with minikube image ls
- [ ] T039 [US1] Create phase4/scripts/build-images.sh automation script
- [ ] T040 [US1] Document Docker build process in phase4/docker/README.md
- [ ] T041 [US1] Log all Gordon AI commands in phase4/scripts/ai-commands.log

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - Docker images built and validated locally

---

## Phase 4: User Story 2 - Deploy to Local Kubernetes (Priority: P2)

**Goal**: Deploy containerized applications to Minikube and verify pods reach Running state

**Independent Test**: Start Minikube, apply manifests, verify all pods Running and services accessible

### Implementation for User Story 2

- [ ] T042 [P] [US2] Create namespace for todo-app in phase4/k8s/namespace.yaml (optional, can use default)
- [ ] T043 [P] [US2] Create frontend ConfigMap in phase4/k8s/frontend-configmap.yaml
- [ ] T044 [P] [US2] Create backend ConfigMap in phase4/k8s/backend-configmap.yaml
- [ ] T045 [P] [US2] Create backend Secret in phase4/k8s/backend-secret.yaml
- [ ] T046 [US2] Generate frontend Deployment manifest using kubectl-ai or Claude Code in phase4/k8s/frontend-deployment.yaml
- [ ] T047 [US2] Generate backend Deployment manifest using kubectl-ai or Claude Code in phase4/k8s/backend-deployment.yaml
- [ ] T048 [P] [US2] Generate frontend Service manifest (NodePort 30080) in phase4/k8s/frontend-service.yaml
- [ ] T049 [P] [US2] Generate backend Service manifest (ClusterIP 8000) in phase4/k8s/backend-service.yaml
- [ ] T050 [US2] Add resource limits to frontend deployment (128Mi request, 256Mi limit)
- [ ] T051 [US2] Add resource limits to backend deployment (256Mi request, 512Mi limit)
- [ ] T052 [P] [US2] Add liveness probe to frontend deployment (/health endpoint)
- [ ] T053 [P] [US2] Add readiness probe to frontend deployment (/health endpoint)
- [ ] T054 [P] [US2] Add liveness probe to backend deployment (/health endpoint)
- [ ] T055 [P] [US2] Add readiness probe to backend deployment (/health endpoint)
- [ ] T056 [US2] Apply namespace if created using kubectl apply -f
- [ ] T057 [US2] Apply ConfigMaps using kubectl apply -f
- [ ] T058 [US2] Apply Secrets using kubectl apply -f
- [ ] T059 [US2] Apply frontend Deployment using kubectl apply -f
- [ ] T060 [US2] Apply backend Deployment using kubectl apply -f
- [ ] T061 [US2] Apply frontend Service using kubectl apply -f
- [ ] T062 [US2] Apply backend Service using kubectl apply -f
- [ ] T063 [US2] Verify all pods reach Running state using kubectl get pods
- [ ] T064 [US2] Verify no CrashLoopBackOff errors using kubectl get pods
- [ ] T065 [US2] Check frontend pod logs for errors using kubectl logs
- [ ] T066 [US2] Check backend pod logs for errors using kubectl logs
- [ ] T067 [US2] Get frontend service URL using minikube service todo-frontend-service --url
- [ ] T068 [US2] Access frontend in browser and verify app loads
- [ ] T069 [US2] Test frontend-to-backend API connectivity (check network requests in browser)
- [ ] T070 [US2] Scale frontend to 2 replicas using kubectl scale
- [ ] T071 [US2] Scale backend to 2 replicas using kubectl scale
- [ ] T072 [US2] Verify application still functions with multiple replicas
- [ ] T073 [US2] Create phase4/scripts/deploy-all.sh automation script
- [ ] T074 [US2] Document Kubernetes deployment in phase4/k8s/README.md
- [ ] T075 [US2] Log all kubectl-ai commands in phase4/scripts/ai-commands.log

**Checkpoint**: All pods Running, services accessible, application fully functional on Kubernetes

---

## Phase 5: User Story 3 - Package with Helm Charts (Priority: P3)

**Goal**: Package Kubernetes manifests as reusable Helm charts with parameterized configuration

**Independent Test**: Install/uninstall Helm charts multiple times, test with custom values

### Implementation for User Story 3

- [ ] T076 [US3] Create Helm umbrella chart structure using helm create in phase4/helm/todo-app/
- [ ] T077 [P] [US3] Create frontend sub-chart directory in phase4/helm/todo-app/charts/frontend/
- [ ] T078 [P] [US3] Create backend sub-chart directory in phase4/helm/todo-app/charts/backend/
- [ ] T079 [P] [US3] Create frontend Chart.yaml in phase4/helm/todo-app/charts/frontend/Chart.yaml
- [ ] T080 [P] [US3] Create backend Chart.yaml in phase4/helm/todo-app/charts/backend/Chart.yaml
- [ ] T081 [US3] Create umbrella Chart.yaml with sub-chart dependencies in phase4/helm/todo-app/Chart.yaml
- [ ] T082 [US3] Create umbrella values.yaml with global config in phase4/helm/todo-app/values.yaml
- [ ] T083 [P] [US3] Create frontend values.yaml in phase4/helm/todo-app/charts/frontend/values.yaml
- [ ] T084 [P] [US3] Create backend values.yaml in phase4/helm/todo-app/charts/backend/values.yaml
- [ ] T085 [US3] Convert frontend Deployment to Helm template in phase4/helm/todo-app/charts/frontend/templates/deployment.yaml
- [ ] T086 [US3] Convert backend Deployment to Helm template in phase4/helm/todo-app/charts/backend/templates/deployment.yaml
- [ ] T087 [P] [US3] Convert frontend Service to Helm template in phase4/helm/todo-app/charts/frontend/templates/service.yaml
- [ ] T088 [P] [US3] Convert backend Service to Helm template in phase4/helm/todo-app/charts/backend/templates/service.yaml
- [ ] T089 [P] [US3] Convert frontend ConfigMap to Helm template in phase4/helm/todo-app/charts/frontend/templates/configmap.yaml
- [ ] T090 [P] [US3] Convert backend ConfigMap to Helm template in phase4/helm/todo-app/charts/backend/templates/configmap.yaml
- [ ] T091 [P] [US3] Convert backend Secret to Helm template in phase4/helm/todo-app/charts/backend/templates/secret.yaml
- [ ] T092 [US3] Parameterize replica counts in values.yaml
- [ ] T093 [US3] Parameterize resource limits in values.yaml
- [ ] T094 [US3] Parameterize image tags in values.yaml
- [ ] T095 [US3] Create _helpers.tpl with common labels in phase4/helm/todo-app/charts/frontend/templates/_helpers.tpl
- [ ] T096 [US3] Create _helpers.tpl with common labels in phase4/helm/todo-app/charts/backend/templates/_helpers.tpl
- [ ] T097 [US3] Create NOTES.txt with post-install instructions in phase4/helm/todo-app/templates/NOTES.txt
- [ ] T098 [US3] Validate frontend chart using helm lint
- [ ] T099 [US3] Validate backend chart using helm lint
- [ ] T100 [US3] Validate umbrella chart using helm lint
- [ ] T101 [US3] Test Helm install dry-run using helm install --dry-run --debug
- [ ] T102 [US3] Uninstall raw Kubernetes manifests if present
- [ ] T103 [US3] Install Helm chart using helm install todo-app ./helm/todo-app
- [ ] T104 [US3] Verify all resources created by Helm using helm list
- [ ] T105 [US3] Verify pods and services match previous deployment
- [ ] T106 [US3] Test Helm upgrade with different replica count
- [ ] T107 [US3] Verify rolling update completes without downtime
- [ ] T108 [US3] Test Helm uninstall and verify clean resource removal
- [ ] T109 [US3] Reinstall Helm chart to verify reproducibility
- [ ] T110 [US3] Test with custom values file (custom-values.yaml)
- [ ] T111 [US3] Document Helm chart usage in phase4/helm/todo-app/README.md

**Checkpoint**: Helm charts installable, configurable, and reusable for any environment

---

## Phase 6: User Story 4 - AI-Assisted Operations (Priority: P4)

**Goal**: Demonstrate AI-powered cluster management with kubectl-ai and Kagent

**Independent Test**: Execute 5+ kubectl-ai commands and run Kagent analysis, document all operations

### Implementation for User Story 4

- [ ] T112 [P] [US4] Test kubectl-ai installation with kubectl-ai --version
- [ ] T113 [P] [US4] Test Kagent installation (if available) or document fallback
- [ ] T114 [US4] Use kubectl-ai to describe frontend deployment
- [ ] T115 [US4] Use kubectl-ai to describe backend deployment
- [ ] T116 [US4] Use kubectl-ai to scale frontend deployment to 3 replicas
- [ ] T117 [US4] Use kubectl-ai to get pod resource usage
- [ ] T118 [US4] Use kubectl-ai to check service endpoints
- [ ] T119 [US4] Run Kagent cluster health analysis
- [ ] T120 [US4] Review Kagent optimization recommendations
- [ ] T121 [US4] Apply at least one Kagent recommendation
- [ ] T122 [US4] Use kubectl-ai to rollback deployment if needed
- [ ] T123 [US4] Document all kubectl-ai commands in phase4/scripts/ai-commands.log
- [ ] T124 [US4] Document Kagent analysis results in phase4/docs/KAGENT_ANALYSIS.md
- [ ] T125 [US4] Compare kubectl-ai output with traditional kubectl commands
- [ ] T126 [US4] Create examples of AI commands in phase4/docs/AI_OPERATIONS.md

**Checkpoint**: AI tools demonstrated, all operations logged, learning value captured

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final documentation

- [ ] T127 [P] Create comprehensive README.md in phase4/ with complete setup guide
- [ ] T128 [P] Create QUICKSTART.md in phase4/ with 5-minute guide
- [ ] T129 [P] Document troubleshooting steps in phase4/docs/TROUBLESHOOTING.md
- [ ] T130 [P] Create verification checklist in phase4/docs/VERIFICATION.md
- [ ] T131 Create phase4/scripts/cleanup.sh to teardown all resources
- [ ] T132 Test cleanup script and re-deploy from scratch
- [ ] T133 Verify deployment reproducible on clean Minikube cluster
- [ ] T134 [P] Monitor resource usage with kubectl top nodes
- [ ] T135 [P] Monitor resource usage with kubectl top pods
- [ ] T136 Verify total resource usage within 6GB RAM / 2 CPU limits
- [ ] T137 Test pod restart scenario (delete pod, verify recreation)
- [ ] T138 Test crash recovery (simulate crash, verify restart)
- [ ] T139 Simulate resource exhaustion and document behavior
- [ ] T140 Update root README.md with Phase IV information
- [ ] T141 Create architecture diagram in phase4/docs/ARCHITECTURE.md
- [ ] T142 Document AI tool usage patterns in phase4/docs/AI_TOOLS.md
- [ ] T143 Run quickstart.md validation (follow guide end-to-end)
- [ ] T144 Create demo checklist for instructor evaluation in phase4/docs/DEMO.md
- [ ] T145 Organize repository structure for submission

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (Containerization): Can start after Foundational
  - User Story 2 (Kubernetes): Depends on User Story 1 (needs Docker images)
  - User Story 3 (Helm): Depends on User Story 2 (needs K8s manifests)
  - User Story 4 (AI Operations): Depends on User Story 2 or 3 (needs deployed cluster)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: DEPENDS on User Story 1 (needs Docker images)
- **User Story 3 (P3)**: DEPENDS on User Story 2 (needs K8s manifests to convert)
- **User Story 4 (P4)**: DEPENDS on User Story 2 OR 3 (needs running cluster)

### Within Each User Story

- **User Story 1**: Dockerfiles before builds, builds before validation, validation before loading to Minikube
- **User Story 2**: Images loaded before deployments, ConfigMaps/Secrets before deployments, deployments before services
- **User Story 3**: K8s manifests exist before conversion, chart structure before templates, templates before testing
- **User Story 4**: Cluster deployed before AI operations, AI tools installed before usage

### Parallel Opportunities

- **Setup (Phase 1)**: Tasks T003-T010 can run in parallel (different tools, no dependencies)
- **User Story 1**: Tasks T018-T021 (analysis and .dockerignore) can run in parallel
- **User Story 1**: Tasks T026-T027 (image builds) can run in parallel
- **User Story 1**: Tasks T028-T031 (validations) can run in parallel
- **User Story 2**: Tasks T042-T045 (ConfigMaps/Secrets) can run in parallel
- **User Story 2**: Tasks T048-T049 (Service manifests) can run in parallel
- **User Story 2**: Tasks T052-T055 (health probes) can run in parallel
- **User Story 3**: Tasks T077-T078 (sub-chart directories) can run in parallel
- **User Story 3**: Tasks T079-T080 (Chart.yaml files) can run in parallel
- **User Story 3**: Tasks T083-T084 (values.yaml files) can run in parallel
- **User Story 3**: Tasks T087-T091 (template conversions) can run in parallel
- **User Story 4**: Tasks T112-T113 (AI tool testing) can run in parallel
- **Polish (Phase 7)**: Tasks T127-T130 (documentation) can run in parallel
- **Polish (Phase 7)**: Tasks T134-T135 (monitoring) can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Containerization)
4. Complete Phase 4: User Story 2 (Kubernetes Deployment)
5. **STOP and VALIDATE**: Test deployment end-to-end
6. Deploy/demo if ready (working Kubernetes deployment)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently (Docker images work) → Milestone 1
3. Add User Story 2 → Test independently (K8s deployment works) → Deploy/Demo (MVP!)
4. Add User Story 3 → Test independently (Helm works) → Deploy/Demo (Production-ready)
5. Add User Story 4 → Test independently (AI tools work) → Deploy/Demo (Full feature set)
6. Each story adds value without breaking previous stories

### Sequential Team Strategy

With single developer (recommended for learning):

1. Week 1: Setup + Foundational + User Story 1 (Containerization)
2. Week 2: User Story 2 (Kubernetes Deployment) + MVP validation
3. Week 3: User Story 3 (Helm Charts) + User Story 4 (AI Operations)
4. Week 4: Polish, documentation, demo preparation

---

## Task Statistics

**Total Tasks**: 145
**Setup Tasks**: 11 (Phase 1)
**Foundational Tasks**: 6 (Phase 2)
**User Story 1 Tasks**: 24 (Phase 3)
**User Story 2 Tasks**: 34 (Phase 4)
**User Story 3 Tasks**: 36 (Phase 5)
**User Story 4 Tasks**: 15 (Phase 6)
**Polish Tasks**: 19 (Phase 7)

**Parallel Opportunities**: 45+ tasks marked [P]

**MVP Scope** (Minimum for demo):
- Phase 1: Setup (11 tasks)
- Phase 2: Foundational (6 tasks)
- Phase 3: User Story 1 (24 tasks)
- Phase 4: User Story 2 (34 tasks)
- **Total MVP**: 75 tasks

**Full Feature Set**:
- All 145 tasks completed

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- AI-generated configs preferred (Gordon, kubectl-ai, Claude Code)
- All AI commands logged in scripts/ai-commands.log
- Commit after each completed user story or logical milestone
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, blocking dependencies, manual coding
- Constitution compliance: AI-first, no manual YAML/Dockerfiles, reproducible, secure
