---
description: "TDD task breakdown for Phase I in-memory Python Todo CLI"
---

# Tasks: Phase I – In-Memory Python Todo CLI

**Input**: Specifications from `/specs/001-core-todos/spec.md` and `/specs/001-core-todos/plan.md`
**Prerequisites**: spec.md (complete), plan.md (complete)
**Tests**: MANDATORY - TDD discipline enforced (tests written FIRST, before implementation)

**Organization**: Tasks organized by Phase (Setup → Foundation → User Stories → Validation). Tests are prioritized before implementation for strict TDD workflow.

## Format: `[ID] [P?] [Story/Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies between them)
- **[Story]**: Which phase/user story (US1, US2, etc.)
- **File paths**: Exact locations specified for generated code

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Structure**: src/main.py, src/models/task.py, src/services/task_manager.py, src/cli/commands.py
- **Tests**: tests/test_task_model.py, tests/test_task_manager.py, tests/test_cli_commands.py, tests/test_acceptance.py

---

## Phase A: Foundation & Environment Setup

**Purpose**: Project initialization, directory structure, and dependencies

**⚠️ CRITICAL**: Complete this phase before any code generation begins

- [ ] **T001** [P] [Setup] Create Python project structure: `src/`, `src/models/`, `src/services/`, `src/cli/`, `tests/`
- [ ] **T002** [P] [Setup] Create `pyproject.toml` with Python 3.13+ constraint, pytest dependency, UV package manager config
- [ ] **T003** [P] [Setup] Create `README.md` with setup, installation, and usage instructions
- [ ] **T004** [P] [Setup] Create `CLAUDE.md` with Claude Code guidance for Phase I module (code generation standards, conventions)
- [ ] **T005** [Setup] Create `.env.example` template (no environment variables required for Phase I, but prepared for Phase II)

**Checkpoint**: Project structure ready; dependencies configured; ready to begin Phase B

---

## Phase B: Data Models & Core Infrastructure (Foundational)

**Purpose**: Core data structures and business logic that ALL user stories depend on

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete

### B1: Tests for Task Model (TDD - WRITE FIRST)

> **IMPORTANT**: Write these tests FIRST. They will FAIL until implementation in B2 is complete.

- [ ] **T010** [P] [TaskModel] Write unit tests for Task model in `tests/test_task_model.py`
  - Test 1: Create task with title only → task has id, title, empty description, incomplete status, created_at timestamp
  - Test 2: Create task with title and description → both attributes stored correctly
  - Test 3: Task IDs are unique sequential integers (1, 2, 3, ...)
  - Test 4: Task status is Enum('incomplete', 'complete'), never invalid values
  - Test 5: Task created_at is datetime in ISO 8601 format
  - Test 6: Task.__str__() produces human-readable output including all attributes
  - **Assertion**: pytest discovers and runs these 6 tests; all FAIL before implementation

- [ ] **T011** [P] [TaskModel] Write unit tests for TaskManager in `tests/test_task_manager.py`
  - Test 1: add_task(title) creates task, returns Task object with id=1
  - Test 2: add_task() twice → ids increment (1, 2)
  - Test 3: add_task("Title", "Desc") stores both title and description
  - Test 4: list_tasks() returns list of all tasks in insertion order
  - Test 5: list_tasks() with no tasks returns empty list (not None)
  - Test 6: get_task(1) returns Task object if exists
  - Test 7: get_task(99) returns None if task doesn't exist
  - Test 8: update_task(1, "New Title", None) updates title, keeps description
  - Test 9: update_task(99, ...) returns False (invalid ID)
  - Test 10: delete_task(1) removes task; get_task(1) returns None
  - Test 11: delete_task(99) returns False (invalid ID)
  - Test 12: toggle_task_status(1) changes incomplete ↔ complete
  - Test 13: toggle_task_status(99) returns False (invalid ID)
  - **Assertion**: pytest discovers 13 tests; all FAIL before implementation

### B2: Implement Task Model (Green Phase)

- [ ] **T020** [P] [TaskModel] Implement `src/models/task.py` with Task data class
  - Attributes: `id` (int), `title` (str), `description` (str, default ""), `status` (Enum), `created_at` (datetime)
  - Create factory method: `Task.create(title, description="", auto_id=1)` → returns Task with assigned id
  - Implement `__str__()` method for human-readable output (e.g., "1. Buy groceries ✘ (created: 2026-01-01T10:00:00)")
  - Make Task immutable (use `@dataclass(frozen=True)` or `__setattr__` protection)
  - **Tests**: tests/test_task_model.py must pass (all 6 tests)

- [ ] **T021** [P] [TaskModel] Implement `src/services/task_manager.py` with TaskManager class
  - Private attributes: `_tasks: List[Task]`, `_next_id: int = 1`
  - Public methods:
    - `add_task(title: str, description: str = "") -> Task`: Create, store, return Task; increment `_next_id`
    - `list_tasks() -> List[Task]`: Return copy of all tasks (to prevent external mutation)
    - `get_task(task_id: int) -> Task | None`: Find task by id; return None if not found
    - `update_task(task_id: int, title: str | None, description: str | None) -> bool`: Update task; return True if success, False if not found
    - `delete_task(task_id: int) -> bool`: Remove task; return True if success, False if not found
    - `toggle_task_status(task_id: int) -> bool`: Toggle incomplete ↔ complete; return True if success, False if not found
  - Error handling: All methods use return values (bool/None); NO exceptions
  - **Tests**: tests/test_task_manager.py must pass (all 13 tests)

**Checkpoint**: Task model and TaskManager fully implemented and tested. All 19 unit tests passing (6 + 13).

---

## Phase C: CLI Interface & Command Handling

**Purpose**: User-facing command-line interface; all user story implementations

### C1: Tests for CLI Commands (TDD - WRITE FIRST)

> **IMPORTANT**: Write these tests FIRST. They will FAIL until implementation in C2 is complete.

- [ ] **T030** [P] [CLI] Write integration tests for CLI command parsing in `tests/test_cli_commands.py`
  - Test 1: `parse_args(["add", "Buy groceries"])` → parsed with title="Buy groceries", description=None
  - Test 2: `parse_args(["add", "Buy groceries", "--description", "Milk, eggs"])` → both parsed
  - Test 3: `parse_args(["list"])` → command="list", no arguments
  - Test 4: `parse_args(["list", "--format", "json"])` → format="json"
  - Test 5: `parse_args(["update", "1", "--title", "New title"])` → task_id=1, title="New title"
  - Test 6: `parse_args(["delete", "1"])` → task_id=1
  - Test 7: `parse_args(["complete", "1"])` → task_id=1, command="complete"
  - Test 8: `parse_args(["incomplete", "1"])` → task_id=1, command="incomplete"
  - Test 9: Invalid command raises SystemExit (argparse behavior) or returns error
  - **Assertion**: pytest discovers 9 tests; all FAIL before implementation

- [ ] **T031** [P] [CLI] Write acceptance tests for all 17 spec scenarios in `tests/test_acceptance.py`
  - **User Story 1 (Add Task)**: 4 scenarios
    - Test 1: Add task with title only → task created, id=1, status incomplete, confirmed
    - Test 2: Add second task → id=2, both coexist
    - Test 3: Add task with title + description → both stored
    - Test 4: Add task with empty title → error "Title is required"
  - **User Story 2 (View Tasks)**: 5 scenarios
    - Test 5: List with multiple tasks → all displayed with id, title, status indicator
    - Test 6: Task with incomplete status → displays ✘ or "[ ]"
    - Test 7: Task with complete status → displays ✔ or "[x]"
    - Test 8: List with no tasks → displays "No tasks" message
    - Test 9: List with 10+ tasks → all displayed in order
  - **User Story 3 (Mark Complete)**: 4 scenarios
    - Test 10: Complete task by ID → status changes, list reflects immediately
    - Test 11: Complete a completed task → status toggles back to incomplete
    - Test 12: Complete non-existent task ID 99 → error "Task ID 99 not found"
    - Test 13: Complete task → others remain unchanged
  - **User Story 4 (Update Task)**: 4 scenarios
    - Test 14: Update task title → title changed, list reflects change
    - Test 15: Update task description only → title unchanged, description added
    - Test 16: Update non-existent task → error "Task ID X not found"
    - Test 17: Update with empty title → error "Title cannot be empty"
  - **User Story 5 (Delete Task)**: 3 scenarios
    - Test 18: Delete task by ID → removed from list
    - Test 19: Delete non-existent task → error "Task ID X not found"
    - Test 20: Delete task 2 from [1,2,3] → [1,3] remain (IDs don't shift)
  - **Edge Cases**: 5 scenarios
    - Test 21: Invalid command → error "Unknown command" + help
    - Test 22: Non-numeric task ID → error "Invalid ID format"
    - Test 23: App exit → all tasks lost (in-memory expected)
    - Test 24: Add 1000+ tasks → no slowdown, all accessible
    - Test 25: Case-insensitive commands → "LIST", "list", "LiSt" all work
  - **Assertion**: pytest discovers 25 acceptance tests; all FAIL before implementation

### C2: Implement CLI Commands & Entry Point (Green Phase)

- [ ] **T040** [P] [US1-5] Implement `src/cli/commands.py` with command handlers
  - `add_command(task_manager, args)` → Parse title/description, call `task_manager.add_task()`, print confirmation (e.g., "Task 1 added: Buy groceries")
  - `list_command(task_manager, args)` → Call `task_manager.list_tasks()`, format output (human-readable by default, JSON if `--format json`)
    - Human format: `1. Buy groceries ✘` or `1. Buy groceries [✔]` (one per line)
    - JSON format: `{"tasks": [{"id": 1, "title": "Buy groceries", "status": "incomplete", "description": ""}]}`
  - `update_command(task_manager, args)` → Parse task_id, title, description; call `task_manager.update_task()`, print result
  - `delete_command(task_manager, args)` → Parse task_id, call `task_manager.delete_task()`, print result
  - `complete_command(task_manager, args)` → Parse task_id, call `task_manager.toggle_task_status()`, print result
  - `incomplete_command(task_manager, args)` → Parse task_id, call `task_manager.toggle_task_status()`, print result
  - Error messages: Clear, actionable (e.g., "Task ID 99 not found. Valid IDs: 1, 2, 3")
  - **Tests**: tests/test_cli_commands.py must pass (all 9 tests)

- [ ] **T041** [US1-5] Implement `src/main.py` entry point
  - Initialize `TaskManager()` (in-process instance)
  - Set up `argparse.ArgumentParser` with subparsers for: add, list, update, delete, complete, incomplete, help
  - Parse command-line arguments: `parse_args(sys.argv[1:])`
  - Route parsed args to appropriate command handler
  - Print results to stdout; errors to stderr
  - Exit with code 0 (success), 1 (invalid command), 2 (validation error)
  - Usage: `python src/main.py add "Buy groceries"`, `python src/main.py list`, etc.
  - **Tests**: tests/test_acceptance.py must pass (all 25 acceptance tests)

**Checkpoint**: CLI fully implemented and tested. All 34 tests passing (9 CLI + 25 acceptance).

---

## Phase D: Validation & Finalization

**Purpose**: Verify correctness, documentation, and readiness for handoff

### D1: End-to-End Validation

- [ ] **T050** [Validation] Run CLI through all 5 user stories in one session
  - Step 1: `python src/main.py add "Buy groceries"`
  - Step 2: `python src/main.py add "Call mom" --description "This weekend"`
  - Step 3: `python src/main.py list`
  - Step 4: `python src/main.py complete 1`
  - Step 5: `python src/main.py list`
  - Step 6: `python src/main.py update 1 --title "Buy groceries and cook dinner"`
  - Step 7: `python src/main.py incomplete 1`
  - Step 8: `python src/main.py delete 2`
  - Step 9: `python src/main.py list`
  - Step 10: `python src/main.py complete 99` (error case)
  - Step 11: `python src/main.py help`
  - **Success Criteria**: All steps execute without errors; output matches expectations

- [ ] **T051** [Validation] Run full test suite and verify coverage
  - Command: `pytest tests/ -v --cov=src --cov-report=term-missing`
  - **Success Criteria**:
    - All tests pass (34 unit + integration + acceptance)
    - Unit test coverage ≥ 95% (models/ + services/)
    - Integration test coverage ≥ 90% (CLI layer)
    - Acceptance test coverage 100% (all 17 spec scenarios)

- [ ] **T052** [Validation] Run all edge case tests
  - Invalid commands, non-numeric IDs, empty lists, large task volumes, case-insensitivity
  - **Success Criteria**: All 5 edge case tests pass (Test 21-25 from T031)

### D2: Spec-to-Code Alignment

- [ ] **T060** [Validation] Verify implementation matches spec.md exactly
  - Check: All 13 functional requirements (FR-001 through FR-013) implemented
  - Check: All 5 user stories (US1-US5) fully functional
  - Check: All 17 acceptance scenarios pass
  - Check: All edge cases handled as specified
  - **Success Criteria**: Zero deviations from spec

- [ ] **T061** [Validation] Confirm no manual code edits
  - Requirement: All code must be AI-generated via Claude Code
  - Verification: No hand-written code; no manual edits after generation
  - If edits discovered: Regenerate from spec updates, not manual fixes
  - **Success Criteria**: 100% AI-generated code

- [ ] **T062** [Validation] Verify TDD discipline enforced
  - Check: Tests written before implementation (RED phase)
  - Check: Tests failed before code generated (confirmed from test runs)
  - Check: Tests now pass with implementation (GREEN phase)
  - **Success Criteria**: Red-Green-Refactor cycle strictly followed

### D3: Documentation & Completion

- [ ] **T070** [P] [Validation] Complete `README.md`
  - Include: Setup instructions (Python 3.13+, UV, clone/cd/setup)
  - Include: Installation steps (`uv sync` or equivalent)
  - Include: Usage examples for all 6 commands
  - Include: Testing instructions (`pytest tests/`)
  - Include: Note on in-memory storage (data lost on exit)

- [ ] **T071** [P] [Validation] Complete `CLAUDE.md` for Phase I module
  - Include: Code generation standards and conventions
  - Include: File organization (models → services → CLI)
  - Include: Error handling patterns (return values, not exceptions)
  - Include: TDD workflow (tests first, then implementation)
  - Include: Links to spec.md and plan.md

- [ ] **T072** [Validation] Create PHR for tasks stage
  - Record: Full task breakdown, test-first discipline, implementation workflow
  - Link: spec.md, plan.md, task results

- [ ] **T073** [Validation] Update root `.specify/memory/constitution.md` with Phase I completion note
  - Reference: Phase I specs, plan, code, tests
  - Confirm: All 7 constitutional principles upheld in Phase I

### D4: Preparation for Phase II

- [ ] **T080** [Validation] Verify readiness for Phase II (database + web app)
  - Check: Task model and TaskManager are reusable (designed for extraction to backend)
  - Check: CLI code cleanly separates from business logic (enables API endpoint creation)
  - Check: No hardcoded assumptions preventing database persistence
  - **Success Criteria**: Code structure enables Phase II evolution without major refactoring

- [ ] **T081** [Validation] Create commit and prepare PR
  - Commit message: "feat: implement Phase I in-memory todo CLI (all acceptance criteria pass)"
  - Include: spec.md, plan.md, tasks.md, all source code, all tests, documentation
  - PR description: Links to spec, summary of features, test results, readiness for Phase II

**Checkpoint**: Phase I complete. All tests passing. Documentation complete. Ready for Phase II planning.

---

## Test Summary

### Unit Tests (Phase B)
- **File**: `tests/test_task_model.py` (6 tests)
- **File**: `tests/test_task_manager.py` (13 tests)
- **Total**: 19 tests
- **Coverage Target**: ≥ 95% of models/ and services/
- **Run**: `pytest tests/test_task_model.py tests/test_task_manager.py -v`

### Integration Tests (Phase C)
- **File**: `tests/test_cli_commands.py` (9 tests)
- **Coverage Target**: ≥ 90% of CLI layer
- **Run**: `pytest tests/test_cli_commands.py -v`

### Acceptance Tests (Phase C)
- **File**: `tests/test_acceptance.py` (25 tests)
- **Covers**: All 17 spec scenarios + 5 edge cases + 3 deletions
- **Coverage Target**: 100% pass rate (all spec scenarios)
- **Run**: `pytest tests/test_acceptance.py -v`

### Full Test Suite
- **Total Tests**: 53 (19 unit + 9 integration + 25 acceptance)
- **Run All**: `pytest tests/ -v --cov=src --cov-report=term-missing`
- **Success Criteria**: All 53 tests pass; unit coverage ≥95%, integration ≥90%, acceptance 100%

---

## Dependencies & Execution Order

### Phase A: Setup (Independent)
- All T001-T005 can run in parallel
- **Dependency**: None (starting point)
- **Blocks**: Phase B cannot start until Phase A complete

### Phase B: Foundation (Sequential within phase)
- **Dependency Chain**:
  - T010 (tests for Task model) - write first, will fail
  - T011 (tests for TaskManager) - write first, will fail
  - T020 (implement Task model) - depends on T010 passing afterward
  - T021 (implement TaskManager) - depends on T011 passing afterward
- **Blocks**: Phase C cannot start until Phase B complete

### Phase C: CLI & User Stories (Sequential within phase)
- **Dependency Chain**:
  - T030 (CLI tests) - write first, will fail
  - T031 (acceptance tests) - write first, will fail
  - T040 (implement CLI commands) - depends on T030 passing afterward
  - T041 (implement main.py) - depends on T031 passing afterward
- **Blocks**: Phase D cannot start until Phase C complete

### Phase D: Validation (Mostly sequential)
- **Dependency**: All phases A-C must complete
- **Order**: T050 (E2E) → T051 (tests) → T052 (edge cases) → T060-T062 (alignment) → T070-T073 (docs) → T080-T081 (Phase II prep)

---

## TDD Workflow Diagram

```
PHASE A: Setup (5 tasks)
  └─→ PHASE B: Foundation (4 tasks)
        ├─ T010: Task Model Tests (FAIL)
        ├─ T011: TaskManager Tests (FAIL)
        ├─ T020: Implement Task Model (then T010 PASSES)
        ├─ T021: Implement TaskManager (then T011 PASSES)
        └─ Checkpoint: All 19 unit tests passing
              └─→ PHASE C: CLI & Stories (4 tasks)
                    ├─ T030: CLI Tests (FAIL)
                    ├─ T031: Acceptance Tests (FAIL - all 25)
                    ├─ T040: Implement CLI Commands (then T030 PASSES)
                    ├─ T041: Implement main.py (then T031 PASSES)
                    └─ Checkpoint: All 34 tests passing (19 + 9 + 25)
                          └─→ PHASE D: Validation (12 tasks)
                                ├─ T050: End-to-End CLI
                                ├─ T051: Full Test Suite
                                ├─ T052: Edge Cases
                                ├─ T060-T062: Spec Alignment
                                ├─ T070-T073: Documentation
                                ├─ T080-T081: Phase II Prep
                                └─ Checkpoint: Phase I Complete ✅
```

---

## Manual Validation Checklist

After all tests pass, manually validate:

- [ ] `python src/main.py add "Buy groceries"` → Task created, ID 1, status incomplete
- [ ] `python src/main.py add "Call mom" --description "This weekend"` → Task created with description
- [ ] `python src/main.py list` → Both tasks displayed with IDs, titles, status indicators
- [ ] `python src/main.py complete 1` → Task 1 status changes; list reflects change
- [ ] `python src/main.py update 1 --title "Buy groceries and cook dinner"` → Title updated
- [ ] `python src/main.py incomplete 1` → Status reverts to incomplete
- [ ] `python src/main.py delete 2` → Task 2 removed; list shows only Task 1
- [ ] `python src/main.py complete 99` → Error message: "Task ID 99 not found. Valid IDs: 1"
- [ ] `python src/main.py list --format json` → JSON output with all attributes
- [ ] `python src/main.py help` → Lists available commands and usage

---

## Success Criteria

Phase I is **COMPLETE** when:

1. ✅ All 53 tests pass (unit + integration + acceptance)
2. ✅ All 17 spec scenarios validated
3. ✅ All 5 edge cases handled gracefully
4. ✅ Manual validation checklist 100% complete
5. ✅ No manual code edits (100% AI-generated)
6. ✅ TDD discipline enforced (tests written first, failed, then passed)
7. ✅ Code follows PEP 8 style guidelines
8. ✅ Error messages clear and actionable
9. ✅ All 5 features (add, list, update, delete, complete) work without errors
10. ✅ Typical 3-task workflow completes in <10 seconds
11. ✅ Documentation (README.md, CLAUDE.md) complete
12. ✅ Ready to commit and create PR
13. ✅ Ready for Phase II planning (database + web app)

---

**Task List Status**: ✅ READY FOR IMPLEMENTATION VIA CLAUDE CODE
**Total Tasks**: 20 (A: 5, B: 4, C: 4, D: 12)
**Total Tests**: 53 (B: 19, C: 9 + 25)
**Estimated Implementation Time**: 2-3 hours (all phases)
**Next Step**: Run `/sp.implement` to execute tasks and generate code
