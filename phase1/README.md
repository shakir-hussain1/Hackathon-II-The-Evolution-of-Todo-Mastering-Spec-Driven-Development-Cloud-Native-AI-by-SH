# Phase I – In-Memory Python Todo CLI

A command-line todo application built with Spec-Driven Development principles.

## Setup & Installation

### Requirements

- Python 3.13+
- UV package manager

### Installation

```bash
# Clone the repository
cd Hackathon-II-Todo

# Install dependencies
uv sync

# Run the application
python src/main.py --help
```

## Usage

### Add a Task

```bash
python src/main.py add "Buy groceries"
python src/main.py add "Call mom" --description "This weekend"
```

### List All Tasks

```bash
python src/main.py list
python src/main.py list --format json
```

### Update a Task

```bash
python src/main.py update 1 --title "New title"
python src/main.py update 1 --description "New description"
python src/main.py update 1 --title "New title" --description "New description"
```

### Complete a Task

```bash
python src/main.py complete 1
```

### Mark Task Incomplete

```bash
python src/main.py incomplete 1
```

### Delete a Task

```bash
python src/main.py delete 1
```

### Get Help

```bash
python src/main.py help
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_task_model.py -v
```

## Project Structure

```
.
├── src/
│   ├── main.py                 # Entry point and CLI routing
│   ├── models/
│   │   └── task.py             # Task data model
│   ├── services/
│   │   └── task_manager.py     # TaskManager CRUD service
│   └── cli/
│       └── commands.py         # Command handlers
├── tests/
│   ├── test_task_model.py      # Unit tests for Task model
│   ├── test_task_manager.py    # Unit tests for TaskManager
│   ├── test_cli_commands.py    # Integration tests for CLI
│   └── test_acceptance.py      # Acceptance tests (all spec scenarios)
├── pyproject.toml              # Project metadata and dependencies
└── README.md                   # This file
```

## Features

### User Story 1: Add Task (Priority: P1)
- Create a new task with title (required) and description (optional)
- Task receives unique sequential ID
- Default status: incomplete

### User Story 2: View Task List (Priority: P1)
- Display all tasks
- Show ID, title, and completion status indicator
- Handle empty list gracefully

### User Story 3: Mark Task Complete (Priority: P1)
- Toggle task completion status
- Status change reflected immediately in list

### User Story 4: Update Task (Priority: P2)
- Modify task title and/or description by ID
- Clear error message for non-existent IDs

### User Story 5: Delete Task (Priority: P2)
- Remove task by ID
- Graceful error handling for invalid IDs

## Architecture

### Task Model
Immutable data class representing a single todo item:
- `id`: Unique sequential integer
- `title`: Required string (max 256 chars)
- `description`: Optional string (max 1024 chars)
- `status`: Enum ('incomplete' or 'complete')
- `created_at`: Datetime in ISO 8601 format

### TaskManager Service
In-memory CRUD operations:
- `add_task(title, description="")`: Create and store task
- `list_tasks()`: Return all tasks
- `get_task(task_id)`: Fetch task by ID
- `update_task(task_id, title, description)`: Modify task
- `delete_task(task_id)`: Remove task
- `toggle_task_status(task_id)`: Toggle complete/incomplete

### CLI Layer
Command-based interface using argparse:
- `add`: Create new task
- `list`: Display all tasks
- `update`: Modify task
- `delete`: Remove task
- `complete`: Mark task complete
- `incomplete`: Mark task incomplete
- `help`: Display available commands

## Notes

- **In-Memory Only**: All data is stored in memory. Tasks are lost when the application exits.
- **Single-User**: Designed for single-user local execution.
- **No Database**: No external storage or persistence.
- **CLI Only**: Command-line interface without GUI or web UI.

## Testing

Phase I enforces strict TDD discipline:
- Tests written BEFORE implementation (RED phase)
- Tests fail before code is generated (confirmed before GREEN phase)
- Implementation makes tests pass (GREEN phase)
- Code refactored while tests stay passing (REFACTOR phase)

### Test Coverage Goals
- Unit tests: ≥95% (models + services)
- Integration tests: ≥90% (CLI layer)
- Acceptance tests: 100% (all spec scenarios)

## Phase II Evolution

Phase I code is designed to enable clean transition to Phase II (Full-Stack Web App):
- Task model and TaskManager service are reusable
- CLI layer cleanly separated from business logic
- No hardcoded assumptions preventing database persistence
- Structure supports future API endpoint creation

---

**Status**: Phase I Complete - Ready for Phase II Planning
**Version**: 1.0.0
**Date**: 2026-01-01
