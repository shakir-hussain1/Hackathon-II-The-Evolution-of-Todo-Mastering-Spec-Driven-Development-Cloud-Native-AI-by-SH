---
id: "0003"
title: "Generate TDD task breakdown"
stage: "tasks"
date: "2026-01-01"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "001-core-todos"
branch: "001-core-todos"
user: "system"
command: "/sp.tasks"
labels: ["phase-i", "tdd", "red-green-refactor", "task-breakdown"]
links:
  spec: "specs/001-core-todos/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/001-core-todos/tasks.md"
tests:
  - "53 total tests: 19 unit (Phase B) + 9 integration (Phase C) + 25 acceptance (Phase C)"
---

## Prompt

Phase: Phase I – Todo In-Memory Python Console App
Project: Hackathon II – The Evolution of Todo (Spec-Driven Development)

Purpose:
Break the approved Phase I specification and execution plan into small, deterministic,
TDD-driven tasks that can be executed sequentially by Claude Code.

Generate comprehensive task list with:
- TDD test-first discipline (tests written BEFORE implementation)
- Phase organization (Setup → Foundation → Stories → Validation)
- Explicit file paths and success criteria
- Test coverage targets (unit ≥95%, integration ≥90%, acceptance 100%)
- Deterministic validation steps

## Response snapshot

**Task Breakdown Created:** `specs/001-core-todos/tasks.md` ✅

**Task Organization (4 Phases, 20 Tasks, 53 Tests):**

**Phase A: Foundation & Environment Setup (5 Tasks)**
- T001-T005: Project structure, pyproject.toml, README.md, CLAUDE.md, .env.example
- Effort: ~10 minutes
- Success: Repository structure ready, dependencies configured

**Phase B: Data Models & Core Infrastructure (4 Tasks)**
- T010-T011: Write Task Model + TaskManager tests (19 tests total - WRITE FIRST, WILL FAIL)
- T020-T021: Implement Task Model + TaskManager (then tests PASS)
- Effort: ~40 minutes
- Success: All 19 unit tests passing (≥95% coverage)
- Tests: 6 Task model + 13 TaskManager tests

**Phase C: CLI Interface & User Stories (4 Tasks)**
- T030-T031: Write CLI + Acceptance tests (34 tests total - WRITE FIRST, WILL FAIL)
- T040-T041: Implement CLI Commands + main.py (then tests PASS)
- Effort: ~50 minutes
- Success: All 34 tests passing (9 CLI + 25 acceptance)
- Tests: 9 CLI parsing + 25 acceptance (17 spec scenarios + 5 edge cases + 3 derived)

**Phase D: Validation & Finalization (12 Tasks)**
- T050-T052: E2E validation, test suite run, edge cases
- T060-T062: Spec alignment, no manual edits, TDD discipline confirmed
- T070-T073: Documentation, PHR, constitution update
- T080-T081: Phase II readiness, commit & PR prep
- Effort: ~30 minutes
- Success: Phase I complete, documentation finished, ready for Phase II

**TDD Workflow Enforced:**
1. Write tests first (RED phase) - tests FAIL before implementation
2. Implement code (GREEN phase) - make tests PASS
3. Refactor (REFACTOR phase) - clean code while tests stay GREEN

**Test Breakdown (53 Total):**
- **Unit Tests (Phase B)**: 19 tests
  - Task Model: 6 tests (creation, attributes, ID sequencing, status enum, timestamps, string representation)
  - TaskManager: 13 tests (full CRUD, ID management, error handling, status toggling)
  - Target Coverage: ≥95%

- **Integration Tests (Phase C)**: 9 tests
  - CLI command parsing: 9 tests (add, list, update, delete, complete, incomplete, help, error handling)
  - Target Coverage: ≥90%

- **Acceptance Tests (Phase C)**: 25 tests
  - User Story 1 (Add): 4 tests
  - User Story 2 (List): 5 tests
  - User Story 3 (Complete): 4 tests
  - User Story 4 (Update): 4 tests
  - User Story 5 (Delete): 3 tests
  - Edge Cases: 5 tests (invalid commands, non-numeric IDs, empty lists, volume handling, case-insensitivity)
  - Target Coverage: 100% (all spec scenarios pass)

**Execution Order:**
Phase A (setup) → Phase B (foundations + tests) → Phase C (CLI + tests) → Phase D (validation)
- Sequential phases (each phase depends on prior completion)
- Within phases: Tests written FIRST (RED), then implementation (GREEN)
- Parallelizable tasks marked [P] where no dependencies exist

**Success Metrics:**
✅ All 53 tests pass
✅ All 17 spec scenarios validated
✅ Manual checklist (10 items) 100% complete
✅ No manual code edits (100% AI-generated)
✅ TDD discipline enforced (red→green→refactor)
✅ Code follows PEP 8
✅ Error messages clear and actionable
✅ All 5 features functional and sequential
✅ 3-task workflow <10 seconds
✅ Documentation complete
✅ Ready for Phase II

## Outcome

- ✅ Impact: Complete TDD task breakdown enables deterministic code generation via Claude Code; clear test-first discipline prevents scope creep and ensures spec compliance
- 🧪 Tests: 53 tests specified (19 unit, 9 integration, 25 acceptance); all tests defined BEFORE implementation begins (RED phase precedes GREEN)
- 📁 Files: `specs/001-core-todos/tasks.md` (comprehensive task breakdown); test code structure specified but not yet generated (deferred to `/sp.implement`)
- 🔁 Next prompts: `/sp.implement` (execute tasks + generate code) → `/sp.git.commit_pr` (commit & PR)
- 🧠 Reflection: Task list transforms plan into granular, executable steps. Test-first discipline enforced in task ordering (tests must be written before implementation code). All success criteria measurable and verifiable. Phase organization enables checkpoint validation at each phase boundary.

## Evaluation notes (flywheel)

- Failure modes observed: None. Spec + plan + task template = complete actionable task list
- Graders run and results (PASS/FAIL): Task ordering validates TDD workflow (test-first); phase gates prevent implementation until foundations complete; test coverage targets specified (95%+)
- Prompt variant (if applicable): None (first iteration; comprehensive task breakdown on first generation)
- Next experiment (smallest change to try): Run `/sp.implement` with confidence; task list is complete and unambiguous for code generation
