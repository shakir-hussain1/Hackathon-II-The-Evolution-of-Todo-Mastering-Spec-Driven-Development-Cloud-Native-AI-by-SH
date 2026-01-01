---
id: "001"
title: "Initialize Hackathon II Constitution"
stage: "constitution"
date: "2026-01-01"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "master"
user: "system"
command: "/sp.constitution"
labels: ["spec-driven", "governance", "phase-planning", "ai-native"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests: []
---

## Prompt

Project: Hackathon II – The Evolution of Todo (Spec-Driven, AI-Native, Cloud-Native Application)

Objective:
Build a production-grade Todo application that evolves across five phases—from an in-memory CLI app to a distributed, AI-powered, cloud-native system—using strict Spec-Driven Development with Claude Code and Spec-Kit Plus. The developer acts as a system architect, not a manual code writer.

Core Principles:
- Spec-Driven Development First: No implementation without an approved, written spec
- AI-Native Engineering: Claude Code must generate all code; manual coding is prohibited
- Reusable Intelligence: Prefer agent skills, subagents, MCP tools, and reusable specs
- Stateless & Cloud-Native Design: Backend services must be stateless and horizontally scalable
- Security by Default: Authentication, authorization, and user isolation enforced in all phases
- Incremental Evolution: Each phase must build cleanly on previous phases without regressions
- Production Realism: Designs must reflect real-world, deployable architectures

Key Standards:
- Every feature MUST have:
  - A written Markdown Constitution (project-level)
  - A feature spec under `/specs/features`
  - Supporting API, DB, UI, or MCP specs where applicable
- Claude Code must:
  - Read specs via @specs references
  - Follow CLAUDE.md instructions at root, frontend, and backend levels
- Spec format must include:
  - User stories
  - Acceptance criteria
  - Edge cases
  - Error handling rules
- API standards:
  - RESTful design
  - JWT-based authentication (Better Auth)
  - User-level data isolation enforced on every request
- AI standards:
  - OpenAI Agents SDK for reasoning
  - MCP tools as the ONLY way agents mutate application state
  - Agents must confirm actions and handle errors gracefully

Architecture Constraints:
- Phase I: In-memory Python CLI only (no DB, no web)
- Phase II: Full-stack web app (Next.js + FastAPI + SQLModel + Neon)
- Phase III: AI chatbot with MCP server and stateless chat endpoint
- Phase IV: Local Kubernetes deployment using Docker, Helm, Minikube
- Phase V: Production-grade cloud deployment with Kafka + Dapr on DOKS/GKE/AKS
- Monorepo structure is mandatory
- Spec-Kit folder conventions must be followed exactly

Tooling Constraints:
- Claude Code + Spec-Kit Plus are mandatory
- Code generation must be iterative via spec refinement
- kubectl-ai, kagent, and Docker AI (Gordon) should be used where applicable
- Kafka must be event-driven (no tight coupling)
- Dapr must abstract infrastructure concerns in Phase V

Quality & Validation Rules:
- No feature is considered complete unless:
  - All acceptance criteria pass
  - Specs and implementation match exactly
  - Claude Code produces the output without manual edits
- Statelessness must be verifiable (server restarts must not lose state)
- Security checks:
  - Unauthorized access returns 401
  - Cross-user data access is impossible
- Cloud readiness:
  - Horizontal scaling supported
  - Environment variables used for secrets
  - Helm charts must be reproducible

Documentation Requirements:
- README.md with setup and run instructions per phase
- CLAUDE.md files at:
  - Root
  - /frontend
  - /backend
- Specs history must be preserved (no deletion of prior specs)
- Architecture decisions must be reflected in specs, not ad-hoc code

Success Criteria:
- All five phases completed using spec-driven workflow
- AI chatbot can manage todos entirely via natural language
- MCP tools correctly invoked for all task operations
- Application deploys successfully on:
  - Minikube (local)
  - Cloud Kubernetes (DOKS/GKE/AKS)
- Event-driven features (Kafka + Dapr) function correctly
- Project is demo-ready with a <90 second walkthrough video
- Codebase is clean, reproducible, and aligned with real-world AI-native standards

## Response snapshot

Created comprehensive constitution (v1.0.0) at `.specify/memory/constitution.md` with:

**7 Core Principles:**
1. Spec-Driven Development First (no code without approved spec)
2. AI-Native Engineering (Claude Code generates all code)
3. Reusable Intelligence (agent skills, MCP tools, ADRs, PHRs)
4. Stateless & Cloud-Native Design (JWT auth, user isolation, K8s-ready)
5. Security by Default (auth, authz, no hardcoded secrets)
6. Incremental Evolution (clean phase progression, no regressions)
7. Production Realism (RESTful APIs, schema evolution, observable, scalable)

**Architecture Sections:**
- Phase I–V constraints with tech stacks
- Monorepo structure with feature organization
- Development Workflow (spec → plan → ADR → tasks → implement → PHR)
- Code Quality Standards (testing, security, observability, versioning)
- Governance (amendment procedure, compliance, success metrics)

**Template Validation:**
✅ spec-template.md – Aligns with principle-driven user stories, acceptance criteria structure
✅ plan-template.md – Supports "Constitution Check" gate; structure matches phase progression
✅ tasks-template.md – Task organization by user story matches spec-driven workflow

All placeholders filled; no bracketed tokens remain. Version 1.0.0 (baseline ratification). Dates ISO format (2026-01-01).

## Outcome

- ✅ Impact: Constitution established as governance foundation for all five phases; unambiguous principles enable architecture decisions without re-negotiation
- 🧪 Tests: No code generated; governance artifact only. Constitution serves as acceptance criteria for all spec, plan, task, and implementation workflows.
- 📁 Files: `.specify/memory/constitution.md` (v1.0.0); history record created at `history/prompts/constitution/001-initialize-hackathon-constitution.constitution.prompt.md`
- 🔁 Next prompts: `/sp.specify` for Phase I feature specs; `/sp.plan` for architecture decisions; `/sp.tasks` for implementation task breakdown
- 🧠 Reflection: Constitution consolidates all five phases and tooling constraints into testable, auditable principles. Provides clear contract for code generation agents and human architects.

## Evaluation notes (flywheel)

- Failure modes observed: None; constitution is declarative governance, not executable code.
- Graders run and results (PASS/FAIL): Constitution check embedded in plan/tasks templates—future specs/plans will gate against these principles.
- Prompt variant (if applicable): None
- Next experiment: Create Phase I feature spec for `core-todos` to validate principle enforcement in spec-driven workflow

