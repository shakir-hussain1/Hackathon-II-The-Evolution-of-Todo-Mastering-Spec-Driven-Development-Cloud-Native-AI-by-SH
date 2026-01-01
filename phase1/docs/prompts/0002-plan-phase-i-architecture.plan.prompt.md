---
id: "0002"
title: "Plan Phase I architecture"
stage: "plan"
date: "2026-01-01"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "001-core-todos"
branch: "001-core-todos"
user: "system"
command: "/sp.plan"
labels: ["phase-i", "architecture", "layered-design", "cli", "tdd"]
links:
  spec: "specs/001-core-todos/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-core-todos/plan.md"
tests:
  - "TDD tests to be written in /sp.tasks phase"
---

## Prompt

Phase: Phase I – Todo In-Memory Python Console App
Project: Hackathon II – The Evolution of Todo (Spec-Driven Development)

Purpose:
Create a complete execution plan for Phase I using the Agentic Dev Stack workflow:
Write spec → Generate plan → Break into tasks → Implement via Claude Code.
This plan must ensure that Claude Code can generate a clean, working CLI Todo app
without any manual coding.

Requirements:
1. Architecture Sketch - High-level structure, core components, data flow
2. Section / File Structure Plan - Project layout, separation of concerns, documentation
3. Planning Approach - Spec-first workflow, iterative refinement
4. Decisions Needing Documentation - 5 key architectural decisions with options/tradeoffs
5. Testing & Validation Strategy - TDD workflow, manual validation checklist
6. Phase Organization - 4 phases (Foundation, Core Behavior, Implementation, Validation)

## Response snapshot

**Implementation Plan Created:** `specs/001-core-todos/plan.md` ✅

**Plan Components:**

**1. Architecture Sketch:**
- Layered architecture: CLI → Command Handlers → TaskManager Service → Task Model
- In-memory data flow: User Input → CLI Parsing → Service Logic → Output Formatting
- Separation of concerns: models (Task), services (TaskManager), cli (commands)
- Stateless single-invocation design for Phase I; enables scaling in Phase IV

**2. Project Structure:**
- Single-project CLI application (Option 1)
- Directory layout: src/ (main, models/, services/, cli/), tests/ (unit/integration/acceptance)
- Clear separation: models → services → CLI prevents tight coupling
- Documentation: specs/001-core-todos/ contains spec, plan, tasks, checklists

**3. Key Architectural Decisions (5 ADRs to document):**

| Decision | Selected Option | Rationale |
|----------|-----------------|-----------|
| **ADR-001: Task ID Generation** | Sequential integers (1,2,3...) | Simple, testable, spec-aligned; migration to UUID in Phase II |
| **ADR-002: In-Memory Storage** | List of Task objects (O(n) search) | Simplicity for ~10K tasks; upgrade indexing in Phase IV |
| **ADR-003: CLI Style** | Command-based (`todo add ...`) | Scriptable, git-like, automatable; aligns with Phase II API |
| **ADR-004: Error Handling** | Return values + messages (no exceptions) | Clean user experience; CLI controls output; no stack traces |
| **ADR-005: Status Representation** | Python Enum (INCOMPLETE, COMPLETE) | Type-safe, testable, schema-evolution ready for Phase II |

**4. Core Components:**
- **Task Model**: Immutable data class with id, title, description, status (Enum), created_at
- **TaskManager Service**: In-memory CRUD (add, list, get, update, delete, toggle_status)
- **CLI Layer**: argparse-based command routing (add, list, update, delete, complete, incomplete)
- **Entry Point**: main.py bootstraps TaskManager and routes commands

**5. Implementation Workflow (4 Phases):**

| Phase | Objective | Effort | Success Criteria |
|-------|-----------|--------|------------------|
| **A: Foundation** | Environment setup, directory structure, pyproject.toml | 5-10 min | Python 3.13+, UV, empty src/tests/ |
| **B: Core Logic** | Task model, TaskManager service, unit tests | 30-45 min | Full CRUD, unique IDs, 95%+ coverage |
| **C: CLI Interface** | Command parsing, handlers, integration tests | 45-60 min | All 6 commands functional, acceptance tests pass |
| **D: Validation** | Manual testing, documentation, commit prep | 15-30 min | All tests pass, manual checklist 100%, ready for Phase II |

**6. Testing & Validation Strategy:**
- **TDD Discipline**: Write tests first (RED), implement (GREEN), refactor (while GREEN)
- **Unit Tests**: Task model + TaskManager service (≥95% coverage)
- **Integration Tests**: CLI command parsing and routing (≥90% coverage)
- **Acceptance Tests**: All 17 scenarios from spec (100% pass rate)
- **Manual Validation**: 10-point checklist covering all features and edge cases

**7. Constitution Alignment:**
✅ All 7 principles validated against plan:
- Spec-Driven Development First ✅ (spec complete before planning)
- AI-Native Engineering ✅ (100% Claude Code generation, no manual coding)
- Reusable Intelligence ✅ (ADRs document decisions, future MCP integration ready)
- Stateless & Cloud-Native Design ✅ (stateless CLI; future persistence in Phase II)
- Security by Default ✅ (error handling explicit, user isolation via single-user)
- Incremental Evolution ✅ (Phase I isolated, cleanly builds to Phase II)
- Production Realism ✅ (clear contracts, observable behavior, error handling)

**Plan Quality:**
- Comprehensive: 517 lines covering architecture, decisions, workflow, testing, risks
- Unambiguous: All 5 architectural decisions have options table with selected rationale
- Actionable: 4-phase workflow maps to `/sp.tasks` task breakdown
- Governance-compliant: Validates against all 7 constitutional principles

## Outcome

- ✅ Impact: Comprehensive implementation plan establishes clear path from spec to working code; unambiguous architecture enables Claude Code to generate correct implementation on first iteration
- 🧪 Tests: No tests in this stage (TDD tests generated in `/sp.tasks` phase); plan includes detailed testing strategy with coverage targets
- 📁 Files: `specs/001-core-todos/plan.md` (517 lines, complete plan); no code generated yet (deferred to `/sp.tasks` → `/sp.implement`)
- 🔁 Next prompts: `/sp.tasks` (TDD task breakdown) → `/sp.implement` (code generation) → `/sp.adr` (document decisions) → `/sp.git.commit_pr` (commit & PR)
- 🧠 Reflection: Plan transforms spec into actionable, phased implementation roadmap. Clear separation of concerns (models → services → CLI) enables parallel development. Architectural decisions documented for future review. All risks identified and mitigated.

## Evaluation notes (flywheel)

- Failure modes observed: None. Spec + plan template + comprehensive user input = complete plan on first iteration
- Graders run and results (PASS/FAIL): Constitution check passes 7/7 principles; project structure aligns with template; architectural decisions have clear tradeoffs documented
- Prompt variant (if applicable): None (first iteration; template + clear requirements = complete plan)
- Next experiment (smallest change to try): Proceed to `/sp.tasks` with confidence; plan is actionable and comprehensive
