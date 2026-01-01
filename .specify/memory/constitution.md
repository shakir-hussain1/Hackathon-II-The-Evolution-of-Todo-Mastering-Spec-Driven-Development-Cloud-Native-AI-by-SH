# Hackathon II – The Evolution of Todo Constitution

## Core Principles

### I. Spec-Driven Development First
No implementation without an approved, written specification. Every feature MUST have a markdown spec under `/specs/features/<feature-name>/spec.md` describing user stories, acceptance criteria, edge cases, and error handling rules. Specs are the single source of truth; code generation flows from approved specs only. Scope changes MUST be updated in the spec and re-approved before implementation begins.

### II. AI-Native Engineering
Claude Code and AI agents generate ALL production code. Manual coding is prohibited. All code changes MUST be produced by Claude Code following CLAUDE.md guidance at the root, `/frontend`, and `/backend` levels. Code references MUST cite existing files with `file_path:line_number` format. Iterative refinement via spec updates is the path to correctness, not ad-hoc edits.

### III. Reusable Intelligence
Prefer agent skills, subagents, MCP tools, and reusable specs over one-off scripts. Agents must confirm actions and handle errors gracefully. MCP tools are the ONLY way agents mutate application state. Each significant decision MUST be documented via Architecture Decision Records (ADRs) under `history/adr/`. Prompt History Records (PHRs) MUST be created for every meaningful user interaction under `history/prompts/`.

### IV. Stateless & Cloud-Native Design
Backend services MUST be stateless and horizontally scalable. No server-side session state; use JWT-based authentication (Better Auth). User-level data isolation MUST be enforced on every request at the API layer. All configuration MUST use environment variables (no hardcoded secrets). Phase IV+ deployments MUST support Kubernetes with stateless pod scaling, event-driven architecture via Kafka, and infrastructure abstraction via Dapr.

### V. Security by Default
Authentication, authorization, and user isolation are non-negotiable in ALL phases. Every API endpoint MUST enforce user context on requests. Unauthorized access returns 401; cross-user data access is impossible. Secrets are never hardcoded; use `.env` and documented environment variables only. Security checks are built into acceptance criteria, not optional.

### VI. Incremental Evolution
Each phase builds cleanly on previous phases without regressions. Phase I (Python CLI) → Phase II (Next.js + FastAPI) → Phase III (AI chatbot + MCP) → Phase IV (Local K8s) → Phase V (Cloud deployment). No feature is considered complete unless all acceptance criteria pass, specs and implementation match exactly, and Claude Code produces output without manual edits.

### VII. Production Realism
Designs MUST reflect real-world, deployable architectures. APIs are RESTful with clear contracts. Data models support schema evolution. Deployment is reproducible via Helm charts, Docker images, and documented runbooks. Observability (logs, metrics, traces) is built in from the start. Horizontal scaling, feature flags, and graceful degradation are verified before marking phases complete.

## Architecture Constraints

**Phase I (Spec-Driven Foundation):**
- In-memory Python CLI only (no database, no web server)
- All commands: `todo create`, `todo list`, `todo complete`, `todo delete`
- JSON output for scripting; human-readable for direct use
- TDD mandatory; red-green-refactor cycle enforced

**Phase II (Full-Stack Web Application):**
- Frontend: Next.js + TypeScript
- Backend: FastAPI + SQLModel
- Database: Neon PostgreSQL
- Auth: Better Auth (JWT-based)
- API: RESTful, user-isolated at the request layer

**Phase III (AI-Powered Chatbot):**
- OpenAI Agents SDK for reasoning
- MCP server for todo operations (create, list, complete, delete)
- Stateless chat endpoint (no conversation history in server)
- Natural language intent parsing and task execution

**Phase IV (Local Kubernetes):**
- Docker images for frontend, backend, MCP server
- Helm charts for reproducible local deployment
- Minikube for local testing
- Pod auto-scaling based on load

**Phase V (Production Cloud Deployment):**
- Cloud Kubernetes (DOKS, GKE, or AKS)
- Kafka for event-driven communication (no tight coupling)
- Dapr for infrastructure abstraction and service-to-service calls
- Multi-region support with disaster recovery

**Monorepo Structure:**
```
hackathon-ii-todo/
├── .specify/                # Spec-Kit Plus templates, scripts, memory
├── specs/                   # Feature specs and plans
│   └── features/
│       ├── core-todos/      # Phase I & II todo management
│       ├── ai-chatbot/      # Phase III ai integration
│       └── k8s-deployment/  # Phase IV & V kubernetes & cloud
├── frontend/                # Next.js application (Phase II+)
├── backend/                 # FastAPI application (Phase II+)
├── mcp-server/              # MCP server for AI agents (Phase III+)
├── infrastructure/          # Docker, Helm, Kubernetes (Phase IV+)
├── history/                 # PHRs, ADRs, decisions
└── CLAUDE.md                # Root-level Claude Code guidance
```

## Development Workflow

**Specification Process:**
1. User describes feature in natural language
2. `/sp.specify` creates or updates spec under `/specs/features/<feature-name>/spec.md`
3. `/sp.clarify` identifies and resolves underspecified areas
4. User approves spec before any coding begins

**Planning & Architecture:**
1. `/sp.plan` generates detailed implementation plan and identifies significant decisions
2. `/sp.adr` documents architectural decisions with trade-offs and rationale
3. Plan identifies task breakdown and dependencies

**Implementation:**
1. `/sp.tasks` generates ordered, testable tasks from approved plan
2. `/sp.implement` executes tasks, generating code via Claude Code
3. All code generated must reference specs and pass acceptance criteria
4. Integration tests verify cross-service contracts and user isolation

**Quality & Validation:**
1. `/sp.analyze` performs cross-artifact consistency checks
2. `/sp.checklist` generates phase-specific quality gates
3. No feature complete until: all acceptance criteria pass, specs match code, and deployment verified

**Documentation & History:**
1. `/sp.phr` records every significant user interaction as Prompt History Record
2. `/sp.adr` creates Architecture Decision Records for significant decisions
3. All PHRs routed to `history/prompts/` under feature name or general
4. All ADRs routed to `history/adr/` with links back to specs and PRs

**Git & Delivery:**
1. `/sp.git.commit_pr` intelligently commits work and creates pull requests
2. Commits include PHR references and traceability
3. PR descriptions include spec links, acceptance criteria, and testing summary
4. All commits signed; force-push to main/master is prohibited

## Code Quality Standards

- **Testing:** TDD mandatory for all phases. Red-Green-Refactor cycle strictly enforced. Integration tests required for inter-service communication.
- **Security:** No secrets in code. JWT-based auth enforced. User isolation on every request. Unauthorized access returns 401.
- **Observability:** Structured logging required. Metrics exposed for all services. Traces capture request flow end-to-end.
- **Documentation:** CLAUDE.md at root, `/frontend`, `/backend` levels. README.md per phase with setup and run instructions. Specs preserved (no deletions).
- **Performance:** Stateless design enables horizontal scaling. Database queries optimized. API response times tracked (p95 < 200ms target).
- **Versioning:** Semantic versioning enforced. MAJOR for breaking changes, MINOR for features, PATCH for fixes. No silent contract changes.

## Governance

**Constitution as Law:**
This constitution supersedes all other practices and informal agreements. All PRs, code reviews, and architectural decisions MUST verify compliance. Deviations require explicit amendment and documentation.

**Amendment Procedure:**
1. Amendment requested via `/sp.constitution` with rationale
2. Changes to principles, phases, or constraints require approval
3. Version incremented: MAJOR (principle removal/redefinition), MINOR (new principle/section), PATCH (clarification/wording)
4. All dependent templates (spec, plan, tasks) reviewed for consistency
5. Commit message includes version bump and summary of changes
6. Previous constitution versions preserved in git history

**Compliance Review:**
- Weekly: Spec-to-code alignment verified in PRs
- Phase completion: Full checklist against phase requirements
- Quarterly: Constitution review for emerging constraints or principle conflicts

**Development Guidance:**
Runtime guidance for developers is documented in CLAUDE.md files at root, frontend, and backend levels. These documents supplement the constitution with tool usage, hook configuration, and agent-specific practices. They MUST NOT contradict constitutional principles.

**Success Metrics (Definition of Done):**
- All five phases completed using spec-driven workflow
- AI chatbot manages todos entirely via natural language
- MCP tools correctly invoked for all task operations
- Application deploys successfully on Minikube and cloud Kubernetes
- Event-driven features (Kafka + Dapr) function correctly in Phase V
- Project is demo-ready with a <90 second walkthrough video
- Codebase is clean, reproducible, and aligned with real-world AI-native standards

---

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
