# Feature Specification: Phase I – In-Memory Python Todo CLI

**Feature Branch**: `001-core-todos`
**Created**: 2026-01-01
**Status**: Draft
**Input**: Phase I – Todo In-Memory Python Console App specification for Hackathon II

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a Task to Todo List (Priority: P1)

As a user, I want to create a new task with a title and optional description so that I can track what I need to do.

**Why this priority**: Creating tasks is the fundamental MVP feature—without it, the todo app has no purpose. This is the absolute foundation.

**Independent Test**: Can be fully tested by: running the app, executing an "add" command with a title, and verifying the task appears in the task list with a unique ID and incomplete status.

**Acceptance Scenarios**:

1. **Given** the todo app is running and empty, **When** user adds task with title "Buy groceries", **Then** task is created with a unique ID (e.g., 1), title stored, status is incomplete, and system confirms success
2. **Given** a task exists, **When** user adds a second task with title "Call mom", **Then** new task receives unique ID (e.g., 2) and both tasks coexist in memory
3. **Given** the app is running, **When** user adds task with title "Fix bug" and description "Resolve login timeout issue", **Then** task is created with both title and description stored correctly
4. **Given** a task is being added, **When** title is empty or whitespace-only, **Then** system rejects with clear error message "Title is required"

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I want to see all my tasks in a clear list format so that I can review what I need to do.

**Why this priority**: Viewing tasks is equally critical as adding them—users must be able to see what they created. These two features together form the MVP.

**Independent Test**: Can be fully tested by: adding 2–3 tasks, running the "list" command, and verifying all tasks display with ID, title, and completion status indicator (✔ or ✘).

**Acceptance Scenarios**:

1. **Given** multiple tasks exist in memory, **When** user runs "list" or "view" command, **Then** all tasks display with ID, title, and status indicator
2. **Given** a task with incomplete status, **When** displayed in list, **Then** shows incomplete indicator (e.g., ✘ or "[ ]")
3. **Given** a task with complete status, **When** displayed in list, **Then** shows complete indicator (e.g., ✔ or "[x]")
4. **Given** no tasks exist, **When** user runs "list" command, **Then** system displays "No tasks" message clearly instead of empty output
5. **Given** 10+ tasks exist, **When** user runs "list" command, **Then** all tasks display in numbered or ID-based order, readable and organized

---

### User Story 3 - Mark Task as Complete (Priority: P1)

As a user, I want to mark a task as complete so that I can track my progress and distinguish finished work from pending work.

**Why this priority**: Completion tracking is essential for the MVP—without it, users cannot mark progress. Together with Add and View, this completes the minimum viable feature set.

**Independent Test**: Can be fully tested by: creating a task, marking it complete using a "complete" or "done" command with task ID, and verifying the status changes in the list view.

**Acceptance Scenarios**:

1. **Given** a task with incomplete status exists, **When** user marks it complete by ID, **Then** status changes to complete immediately and list shows updated indicator
2. **Given** a completed task, **When** user marks it incomplete again, **Then** status toggles back to incomplete
3. **Given** a task with ID 1 exists, **When** user tries to complete a non-existent ID (e.g., 99), **Then** system returns "Task not found" error
4. **Given** multiple tasks exist, **When** user completes one task, **Then** other tasks remain unchanged

---

### User Story 4 - Update Task Details (Priority: P2)

As a user, I want to edit a task's title or description so that I can correct mistakes or add more information later.

**Why this priority**: Essential for usability but secondary to core CRUD—users can delete and re-add if needed, but edit improves experience.

**Independent Test**: Can be fully tested by: creating a task, updating its title/description using an "update" or "edit" command, and verifying changes persist in the list.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy groceries", **When** user updates it to "Buy groceries and cook dinner", **Then** title is updated and list shows new title
2. **Given** a task exists, **When** user updates only the description, **Then** title remains unchanged and description is added/updated
3. **Given** a task with ID 5 exists, **When** user tries to update non-existent task, **Then** system returns "Task not found" error
4. **Given** task update with empty title, **When** attempted, **Then** system rejects with "Title cannot be empty" error

---

### User Story 5 - Delete a Task (Priority: P2)

As a user, I want to delete a task so that I can remove outdated or irrelevant tasks from my list.

**Why this priority**: Useful for cleanup but secondary to core MVP—users can ignore completed tasks if deletion is unavailable.

**Independent Test**: Can be fully tested by: creating a task, deleting it by ID, and verifying it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** multiple tasks exist, **When** user deletes a task by ID, **Then** task is removed from memory and no longer appears in list
2. **Given** a non-existent task ID, **When** user attempts to delete it, **Then** system returns "Task not found" error gracefully
3. **Given** 3 tasks exist with IDs 1, 2, 3, **When** user deletes task 2, **Then** tasks 1 and 3 remain, IDs do not shift

---

### Edge Cases

- What happens when user enters invalid command (e.g., "todo foobar")? System MUST display helpful error message and list available commands.
- What happens when user provides non-numeric ID to a command that requires numeric ID? System MUST reject with "Invalid ID format" error.
- What happens when user runs the app and immediately exits? All tasks must be lost (in-memory only, no persistence expected).
- What happens when user adds 1000+ tasks? System MUST handle gracefully without crashing or significant slowdown.
- What happens when user runs commands with extra whitespace or mixed case (e.g., "  LIST  ", "List", "LiSt")? System SHOULD be forgiving and execute command (case-insensitive, trim whitespace).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a task with a required title and optional description
- **FR-002**: System MUST assign a unique sequential ID to each task upon creation
- **FR-003**: System MUST display all tasks in a list view showing ID, title, and completion status indicator
- **FR-004**: System MUST allow users to mark a task as complete or incomplete by ID
- **FR-005**: System MUST allow users to update a task's title and/or description by ID
- **FR-006**: System MUST allow users to delete a task by ID
- **FR-007**: System MUST validate that task IDs exist before allowing update/delete/complete operations
- **FR-008**: System MUST provide clear error messages for invalid commands, missing inputs, or non-existent tasks
- **FR-009**: System MUST accept case-insensitive commands and trim whitespace from user input
- **FR-010**: System MUST store all task data in memory only (no database or file persistence)
- **FR-011**: System MUST initialize with an empty task list upon startup
- **FR-012**: System MUST provide an interactive CLI interface with clear prompts and feedback messages
- **FR-013**: System MUST support JSON output format for scripting (in addition to human-readable output)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a single todo item
  - **id** (integer): Unique sequential identifier, auto-generated, immutable
  - **title** (string): Required, max 256 characters, user-provided
  - **description** (string): Optional, max 1024 characters, defaults to empty string
  - **status** (enum): One of `incomplete` or `complete`, defaults to `incomplete`
  - **created_at** (timestamp): When task was created (ISO 8601 format)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All five core features (add, list, update, delete, toggle-complete) MUST work without errors when used in sequence
- **SC-002**: User can create, list, and complete tasks in under 10 seconds for a typical 3-task workflow
- **SC-003**: Error messages MUST be clear and actionable (e.g., "Task ID 99 not found. Valid IDs: 1, 2, 3")
- **SC-004**: System MUST handle edge cases gracefully: invalid IDs, empty input, non-existent tasks, and malformed commands
- **SC-005**: All generated code MUST be directly runnable via Claude Code without manual edits or adjustments
- **SC-006**: TDD cycle MUST be strictly followed: tests written first and fail before implementation begins

## Acceptance Criteria

### Feature Completeness

- [ ] All five user stories (P1 and P2) are implemented
- [ ] Edge cases are handled with clear error messages
- [ ] Task creation with unique IDs works correctly
- [ ] List view displays all tasks with status indicators
- [ ] Complete/incomplete toggling works bidirectionally
- [ ] Update and delete operations validate task existence
- [ ] JSON output format is available for scripting
- [ ] Case-insensitive command handling is implemented
- [ ] Input whitespace is trimmed consistently

### Code Quality

- [ ] Code is structured with clear separation of concerns (CLI vs. task logic)
- [ ] Function names are descriptive and self-documenting
- [ ] Error handling is explicit and user-friendly
- [ ] No hardcoded values or magic numbers
- [ ] Code follows PEP 8 style guidelines

### Testing (TDD)

- [ ] Unit tests written first and fail before implementation
- [ ] All acceptance scenarios from user stories have corresponding tests
- [ ] Integration tests verify CLI interaction end-to-end
- [ ] Edge case tests cover invalid input and boundary conditions
- [ ] Test coverage MUST be ≥ 85%

## Assumptions

- Users are expected to use the CLI interface, not a GUI or web app
- Tasks persist only during the current session (loss upon app exit is acceptable)
- Single-user execution; no multi-user concurrency needed
- Unique IDs are sequential integers starting from 1
- Timestamps are optional but recommended for task creation time tracking
- CLI prompts can be simple (e.g., `> `) without elaborate UI styling
- JSON output is a secondary output format; human-readable is primary

## Constraints

- **No database or file storage**: All data is in-memory only
- **No web server**: CLI-only application
- **No external dependencies beyond standard Python 3.13+ library**: Use built-in modules (argparse, json, datetime, etc.)
- **No manual coding**: All code must be generated by Claude Code from this spec
- **Single-user only**: No authentication, authorization, or multi-user support needed
- **Python 3.13+ required**: Must be compatible with latest Python version
- **UV environment**: Project must be set up with UV package manager

## Glossary

| Term | Definition |
|------|-----------|
| Task | A single todo item with title, description, and completion status |
| CLI | Command-Line Interface for text-based user interaction |
| Status | Task state: either `incomplete` or `complete` |
| In-memory | Data stored in RAM only, lost when app exits |
| Unique ID | Sequential integer assigned to each task, immutable |
| Acceptance Scenario | A given-when-then test case that validates user story requirements |
