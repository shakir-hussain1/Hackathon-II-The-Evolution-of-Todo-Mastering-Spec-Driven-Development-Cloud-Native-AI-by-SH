<!--
Sync Impact Report - Phase V Constitution Creation

Version Change: NONE → 1.0.0
Type: INITIAL CONSTITUTION (new phase)
Date: 2026-02-08

New Constitution Created:
- Project: Phase V – Advanced Cloud Deployment with Kafka & Dapr
- Principles Defined: 10 core principles
- Sections Added: Core Principles, Architecture Standards, Development Workflow, Governance
- Phase Context: Builds upon Phases I-IV (Console → Web → AI Chatbot → K8s → Event-Driven Cloud)

Template Updates Required:
✅ plan-template.md - Constitution Check section aligns with event-driven + Dapr principles
✅ spec-template.md - Requirements include Kafka topics, Dapr components, event flows
✅ tasks-template.md - Task categories include event testing, Dapr integration, K8s manifests

Deferred Items:
- NONE (all placeholders filled for initial version)

Notes:
- This constitution governs Phase V: Event-driven microservices with Kafka + Dapr + Kubernetes
- Inherits quality standards from Phases I-IV
- Adds event-driven, cloud-native, and distributed systems principles
- Enforces Agentic Dev Stack: Spec → Plan → Tasks → Implementation
- All implementation via Claude Code (no manual coding)
-->

# Phase V - Advanced Cloud Deployment Constitution

## Core Principles

### I. Agentic Development Stack (NON-NEGOTIABLE)

**Strict workflow enforcement:**
- ALL features MUST follow: Write Spec → Generate Plan → Break into Tasks → Implement
- NO manual coding is allowed - ALL implementation MUST be generated via Claude Code
- ALL iterations, prompts, and decisions MUST be documented in Prompt History Records (PHRs)
- System MUST be reproducible and deployable from specifications alone

**Rationale:** Ensures consistency, traceability, and reproducibility across all phases. The spec-driven approach prevents technical debt and maintains documentation accuracy.

### II. Event-Driven Architecture (NON-NEGOTIABLE)

**Event publishing rules:**
- ALL task operations (create, update, delete, complete) MUST publish events to Kafka
- Services MUST consume events independently - NO direct service-to-service calls for data sync
- NO tight coupling between event producers and consumers
- Events MUST be idempotent and include correlation IDs for traceability

**Required Kafka Topics:**
- `task-events` - All CRUD operations on tasks
- `reminders` - Due date and reminder notifications
- `task-updates` - Real-time task status changes

**Rationale:** Event-driven design enables loose coupling, independent service scaling, and real-time system-wide updates. Critical for microservices reliability and scalability.

### III. Dapr-First Integration (NON-NEGOTIABLE)

**Dapr component usage:**
- ALL external dependencies MUST go through Dapr components (Pub/Sub, State, Secrets, Bindings)
- NO direct Kafka client dependencies in application code
- NO direct database client dependencies in stateful services
- NO direct secret access - MUST use Dapr Secrets API

**Required Dapr Building Blocks:**
- **Pub/Sub**: Kafka event publishing and subscription
- **State Management**: Distributed state store for task data
- **Bindings**: External system integrations (notifications, webhooks)
- **Secrets**: Secure secret retrieval (DB passwords, API keys)
- **Service Invocation**: Inter-service communication with retries and circuit breakers

**Rationale:** Dapr provides abstraction over infrastructure, enabling portability, resilience patterns, and simplified operations. Prevents vendor lock-in and simplifies local development.

### IV. Microservices Decomposition

**Service boundaries:**
- Frontend (ChatKit UI) - User interface
- Chat API + MCP Tools - AI agent interface (FastAPI + Agents SDK)
- Notification Service - Email/SMS/Push notifications (event consumer)
- Recurring Task Service - Scheduled task creation (event publisher)
- Audit Service - Event logging and compliance (event consumer)
- WebSocket Sync Service - Real-time UI updates (event consumer)

**Service rules:**
- Each service MUST have a single responsibility
- Services MUST be independently deployable
- Services MUST communicate ONLY via events or Dapr service invocation
- NO shared databases between services
- Stateless services MUST scale horizontally

**Rationale:** Microservices enable independent scaling, deployment, and team ownership. Event-driven communication maintains loose coupling.

### V. Cloud-Native and Kubernetes-First

**Kubernetes deployment requirements:**
- ALL services MUST be containerized (Docker)
- Minikube deployment MUST work identically to cloud deployment
- Helm charts MUST be used for all Kubernetes deployments
- Services MUST declare resource limits and requests
- Health checks (liveness, readiness) MUST be implemented for all services

**Platform targets:**
- Local: Minikube (for development and validation)
- Cloud: AKS (Azure), GKE (Google Cloud), or Oracle OKE (Oracle Cloud)
- Kafka: Strimzi (K8s operator) or managed (Redpanda, Confluent Cloud)

**Rationale:** Kubernetes provides portability, declarative infrastructure, and proven scaling patterns. Minikube-first ensures local dev/test parity with production.

### VI. Test-First Development (NON-NEGOTIABLE)

**TDD enforcement:**
- Tests MUST be written and approved BEFORE implementation
- Tests MUST fail (Red) before implementation begins
- Implementation MUST make tests pass (Green)
- Code MUST be refactored for quality (Refactor)
- Integration tests MUST validate event flows end-to-end

**Required test coverage:**
- **Unit Tests**: Individual service logic
- **Integration Tests**: Event publishing and consumption
- **Contract Tests**: API contracts between services
- **Event Flow Tests**: Complete workflows (create task → notification sent)

**Rationale:** TDD ensures code correctness, prevents regressions, and serves as living documentation. Event-driven systems require rigorous integration testing.

### VII. Security and Secrets Management

**Security requirements:**
- NO secrets in code, configuration files, or Docker images
- ALL secrets MUST be managed via Dapr Secrets API
- Secrets MUST be stored in Kubernetes Secrets (sealed) or external vault (e.g., HashiCorp Vault)
- JWT tokens MUST be validated on ALL protected endpoints
- User data MUST be isolated - NO cross-user access
- Container images MUST be scanned for vulnerabilities (Trivy)

**Authentication flow:**
- Frontend → Backend: JWT tokens in Authorization header
- Service-to-Service: Dapr mTLS or service tokens
- External APIs: API keys via Dapr Secrets

**Rationale:** Security is non-negotiable for production systems. Dapr Secrets API provides abstraction and enables secret rotation without code changes.

### VIII. Observability and Monitoring

**Required observability:**
- Distributed tracing MUST be implemented (Dapr tracing + Jaeger/Zipkin)
- Metrics MUST be exported (Prometheus format)
- Structured logging MUST be used (JSON logs with correlation IDs)
- Health endpoints MUST be exposed (`/health`, `/ready`)
- Dashboards MUST be created (Grafana) for system health and business metrics

**Key metrics to track:**
- Request latency (p50, p95, p99)
- Error rates (HTTP 5xx, event processing failures)
- Event lag (Kafka consumer lag)
- Resource usage (CPU, memory, network)
- Business metrics (tasks created, completion rate)

**Rationale:** Observability is critical for debugging distributed systems. Correlation IDs enable tracing requests across services and events.

### IX. Configuration Externalization

**Configuration rules:**
- NO hardcoded configuration in code
- Environment-specific config MUST be injected via environment variables or ConfigMaps
- Dapr components MUST be configurable per environment (dev, staging, prod)
- Database URLs, Kafka brokers, service endpoints MUST be externalized
- Feature flags MUST be used for gradual rollouts

**Configuration sources (priority order):**
1. Environment variables (highest priority)
2. Kubernetes ConfigMaps
3. Dapr Configuration API
4. Default values in code (fallback only)

**Rationale:** Externalized config enables same container image across environments, simplifies deployment automation, and supports GitOps workflows.

### X. Simplicity and Pragmatism

**Complexity guidelines:**
- Start with the simplest solution that works
- Add complexity ONLY when justified by requirements
- YAGNI (You Aren't Gonna Need It) - don't over-engineer
- Prefer standard patterns over custom solutions
- Document complexity trade-offs in ADRs (Architecture Decision Records)

**Forbidden complexity (unless justified in ADR):**
- Custom messaging protocols (use Kafka via Dapr)
- Custom service meshes (use Dapr or Istio if needed)
- Custom orchestration (use Kubernetes native features)
- Over-abstraction (avoid unnecessary layers)

**Rationale:** Simplicity reduces bugs, improves maintainability, and accelerates development. Complexity must be justified and documented.

## Architecture Standards

### Technology Stack (Mandatory)

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| **Frontend** | Next.js + React | 16+/19+ | Proven in Phase II/III, server components |
| **Backend** | FastAPI + Python | 0.110+/3.11+ | Async support, OpenAPI, Pydantic validation |
| **AI Agent** | OpenAI GPT-4 | Latest | Proven in Phase III, function calling |
| **Database** | PostgreSQL | 15+ | ACID compliance, proven in Phase II/III |
| **Message Queue** | Kafka | 3.5+ | Industry standard, proven scalability |
| **Runtime** | Dapr | 1.12+ | Cloud-native, portable, resilient |
| **Orchestration** | Kubernetes | 1.28+ | Industry standard, multi-cloud support |
| **Deployment** | Helm | 3.13+ | Declarative, versioned deployments |
| **CI/CD** | GitHub Actions | Latest | Integrated with GitHub, free tier |
| **Monitoring** | Prometheus + Grafana | Latest | Cloud-native standard |
| **Tracing** | Jaeger or Zipkin | Latest | Distributed tracing standard |

### Service Communication Patterns

**Synchronous (when needed):**
- Frontend → Backend API: REST over HTTPS
- Service → Service: Dapr service invocation (with retries, circuit breakers)
- External integrations: Dapr bindings

**Asynchronous (preferred):**
- Event publishing: Dapr Pub/Sub → Kafka
- Event consumption: Dapr Pub/Sub subscriptions
- Notifications: Event-driven via notification service

### Data Management

**Database per service:**
- Tasks database: Primary task data (owned by Chat API)
- Audit database: Event logs (owned by Audit Service)
- Notification database: Notification history (owned by Notification Service)
- State store: Dapr state management for caching and session data

**Event sourcing (NOT required but consider for audit):**
- Audit Service MAY implement event sourcing for compliance
- Event log MUST be immutable
- Events MUST include timestamps, correlation IDs, and user context

### Deployment Environments

| Environment | Purpose | Kafka | Database | Dapr |
|-------------|---------|-------|----------|------|
| **Local (Minikube)** | Development | Strimzi or Redpanda | PostgreSQL in K8s | Dapr in K8s |
| **Staging (Cloud)** | Integration testing | Managed Kafka or Strimzi | Managed PostgreSQL | Dapr in K8s |
| **Production (Cloud)** | Live system | Managed Kafka (HA) | Managed PostgreSQL (HA) | Dapr in K8s (HA) |

## Development Workflow

### Phase 0: Specification (Mandatory)

**Steps:**
1. User describes feature in natural language
2. Use `/sp.specify` to create feature specification
3. Specification MUST include:
   - User stories with acceptance criteria
   - Functional requirements (FR-XXX)
   - Success criteria (measurable)
   - Event flows (if applicable)
   - Dapr components required
   - Kafka topics and message schemas

**Output:** `specs/[###-feature-name]/spec.md`

### Phase 1: Planning (Mandatory)

**Steps:**
1. Use `/sp.plan` to generate implementation plan
2. Plan MUST include:
   - Architecture decisions (with ADR references if significant)
   - Service boundaries (which services affected)
   - Event flow diagrams (if events involved)
   - Dapr component specifications
   - Database schema changes
   - API contracts
   - Kubernetes manifests required

**Output:** `specs/[###-feature-name]/plan.md`, `research.md`, `data-model.md`, `contracts/`

### Phase 2: Task Breakdown (Mandatory)

**Steps:**
1. Use `/sp.tasks` to break plan into TDD tasks
2. Tasks MUST include:
   - Test tasks (write tests FIRST)
   - Implementation tasks (grouped by service)
   - Event publishing tasks
   - Event consumption tasks
   - Dapr component configuration
   - Kubernetes manifest creation
   - Helm chart updates

**Output:** `specs/[###-feature-name]/tasks.md`

### Phase 3: Implementation (Mandatory)

**Steps:**
1. Use `/sp.implement` to execute tasks via Claude Code
2. For each task:
   - Write test (if test task)
   - Ensure test fails (Red)
   - Implement feature (Green)
   - Refactor for quality (Refactor)
   - Commit with descriptive message

**Output:** Production code, tests, Dapr components, Helm charts

### Phase 4: Validation (Mandatory)

**Steps:**
1. Run all tests locally (unit + integration)
2. Deploy to Minikube and validate end-to-end
3. Run event flow tests (verify events published and consumed)
4. Check health endpoints and observability
5. Run security scans (Trivy for container images)

**Output:** Test reports, deployment validation, security scan results

### Phase 5: Documentation (Mandatory)

**Steps:**
1. Create PHR (Prompt History Record) using `/sp.phr`
2. Update README.md with new features
3. Create ADRs for significant decisions
4. Update architecture diagrams (event flows, service dependencies)
5. Document deployment procedures

**Output:** PHRs in `history/prompts/`, ADRs in `history/adr/`, updated docs

## Governance

### Constitution Authority

This constitution supersedes all other project practices and guidelines for Phase V. Any deviation MUST be:
1. Explicitly documented in an Architecture Decision Record (ADR)
2. Justified with technical or business rationale
3. Approved by project maintainers
4. Reflected in updated constitution (version bump)

### Compliance Verification

**All PRs/implementations MUST verify:**
- [ ] Spec exists and is approved (`specs/[###-feature-name]/spec.md`)
- [ ] Plan exists and aligns with spec (`specs/[###-feature-name]/plan.md`)
- [ ] Tasks follow TDD workflow (test-first)
- [ ] Events published for state changes (if applicable)
- [ ] Dapr components used for external dependencies
- [ ] No hardcoded secrets or configuration
- [ ] Tests pass (unit + integration + event flow)
- [ ] Health checks implemented
- [ ] Observability instrumented (logs, metrics, traces)
- [ ] Documentation updated (PHR, README, ADRs)
- [ ] Minikube deployment validated
- [ ] Security scan passed (no HIGH/CRITICAL vulnerabilities)

### Amendment Process

**Minor amendments (PATCH version bump):**
- Clarifications, wording improvements, typo fixes
- No semantic changes to principles
- Approved by any maintainer

**Feature amendments (MINOR version bump):**
- New principles added
- Expanded guidance on existing principles
- New technology stack additions
- Requires maintainer consensus and ADR

**Breaking amendments (MAJOR version bump):**
- Removal of existing principles
- Redefinition of core principles
- Backward-incompatible changes
- Requires full team approval, ADR, and migration plan

### Complexity Justification

When violating simplicity principles (Principle X), create an ADR documenting:
- Problem being solved
- Alternatives considered and rejected (with reasons)
- Trade-offs accepted (complexity vs. benefits)
- Mitigation strategies (documentation, abstraction)
- Review and sunset criteria (when to revisit)

### Runtime Development Guidance

For detailed runtime development practices, refer to:
- **Project Guide**: `CLAUDE.md` (Phase V project overview)
- **SpecKit Plus Commands**: `.specify/templates/commands/*.md`
- **Agent System**: `.claude/agents/*.md` (specialized validation agents)
- **Skills**: `skills/*.md` (reusable development skills)

---

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
