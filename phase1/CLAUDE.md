# Phase I – In-Memory Python Todo CLI – Claude Code Guidance

This document provides runtime guidance for Claude Code when implementing or extending Phase I of the Hackathon II Todo application.

## Core Principles

Phase I is built on strict **Spec-Driven Development** principles:

1. **Spec-First**: All implementation strictly follows `/specs/001-core-todos/spec.md`
2. **AI-Native**: 100% code generation via Claude Code (no manual coding)
3. **TDD Discipline**: Tests written BEFORE implementation (RED→GREEN→REFACTOR)
4. **No Persistence**: In-memory only; no database, files, or external APIs
5. **Single-User**: Local CLI only; no web, API, or authentication

## Project Structure

```
src/
├── main.py                 # CLI entry point with argparse routing
├── models/
│   └── task.py            # Task data class (immutable, frozen dataclass)
├── services/
│   └── task_manager.py    # TaskManager CRUD service
└── cli/
    └── commands.py        # Command handlers and output formatting

tests/
├── test_task_model.py     # Unit tests for Task (6 tests)
├── test_task_manager.py   # Unit tests for TaskManager (13 tests)
├── test_cli_commands.py   # Integration tests for CLI (9 tests)
└── test_acceptance.py     # Acceptance tests (25 tests covering all spec scenarios)
```

## Code Generation Standards

### Models (`src/models/task.py`)

**Use `@dataclass(frozen=True)` for immutability:**

```python
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TaskStatus(Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
```

**Factory method for safe creation:**

```python
@classmethod
def create(cls, title: str, description: str = "", auto_id: int = None) -> "Task":
    """Factory method to create a new task with auto-generated ID."""
    return cls(
        id=auto_id,
        title=title,
        description=description,
        status=TaskStatus.INCOMPLETE,
        created_at=datetime.now(timezone.utc)
    )

def __str__(self) -> str:
    """Human-readable task representation."""
    status_indicator = "✔" if self.status == TaskStatus.COMPLETE else "✘"
    return f"{self.id}. {self.title} {status_indicator}"
```

### Services (`src/services/task_manager.py`)

**Use return values, NOT exceptions:**

```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task and return it."""
        task = Task.create(title, description, self._next_id)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        """Get task by ID; return None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str | None, description: str | None) -> bool:
        """Update task; return True if success, False if not found."""
        task = self.get_task(task_id)
        if not task:
            return False

        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Replace in list (since Task is immutable)
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            status=task.status,
            created_at=task.created_at
        )
        idx = self._tasks.index(task)
        self._tasks[idx] = updated_task
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete task; return True if success, False if not found."""
        task = self.get_task(task_id)
        if not task:
            return False
        self._tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle task status; return True if success, False if not found."""
        task = self.get_task(task_id)
        if not task:
            return False

        new_status = (
            TaskStatus.COMPLETE if task.status == TaskStatus.INCOMPLETE
            else TaskStatus.INCOMPLETE
        )

        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=new_status,
            created_at=task.created_at
        )
        idx = self._tasks.index(task)
        self._tasks[idx] = updated_task
        return True
```

### CLI (`src/cli/commands.py`)

**Use argparse for command parsing:**

```python
import argparse
from src.services.task_manager import TaskManager

def add_command(task_manager: TaskManager, args) -> None:
    """Handle 'add' command."""
    title = args.title
    description = args.description or ""

    if not title or not title.strip():
        print("Error: Title is required")
        return

    task = task_manager.add_task(title, description)
    print(f"Task {task.id} added: {task.title}")

def list_command(task_manager: TaskManager, args) -> None:
    """Handle 'list' command."""
    tasks = task_manager.list_tasks()

    if not tasks:
        print("No tasks")
        return

    if args.format == "json":
        import json
        tasks_data = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
        print(json.dumps({"tasks": tasks_data}, indent=2))
    else:
        for task in tasks:
            print(task)
```

### Entry Point (`src/main.py`)

**Use argparse with subparsers:**

```python
import sys
import argparse
from src.services.task_manager import TaskManager
from src.cli import commands

def main():
    task_manager = TaskManager()

    parser = argparse.ArgumentParser(
        prog="todo",
        description="In-memory CLI Todo application"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--description", help="Task description (optional)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--format", choices=["human", "json"], default="human")

    # ... other command parsers ...

    args = parser.parse_args()

    if args.command == "add":
        commands.add_command(task_manager, args)
    elif args.command == "list":
        commands.list_command(task_manager, args)
    # ... handle other commands ...
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

## Testing Standards

### Unit Tests (models + services)

**Test structure:**

```python
import pytest
from src.models.task import Task, TaskStatus
from src.services.task_manager import TaskManager

class TestTaskModel:
    def test_create_task_with_title_only(self):
        """Test creating task with title only."""
        task = Task.create("Buy groceries", auto_id=1)
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE
        assert task.created_at is not None

class TestTaskManager:
    def test_add_task_creates_unique_ids(self):
        """Test that add_task creates tasks with unique sequential IDs."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        assert task1.id == 1
        assert task2.id == 2
```

### Integration Tests (CLI)

**Test command parsing:**

```python
def test_add_command_with_title_and_description(task_manager):
    """Test add command with both title and description."""
    # Simulate argparse Namespace
    class Args:
        title = "Buy groceries"
        description = "Milk, eggs"

    # Test command execution
    commands.add_command(task_manager, Args())

    # Verify result
    tasks = task_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy groceries"
    assert tasks[0].description == "Milk, eggs"
```

### Acceptance Tests (spec scenarios)

**Test end-to-end workflows:**

```python
def test_user_story_1_add_task_with_title_only():
    """Test User Story 1: Add task with title only."""
    manager = TaskManager()

    # Step 1: Add task
    task = manager.add_task("Buy groceries")

    # Verify
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert task.status == TaskStatus.INCOMPLETE

    # Step 2: List tasks
    tasks = manager.list_tasks()
    assert len(tasks) == 1
    assert str(task) == "1. Buy groceries ✘"
```

## Error Handling

**Never use exceptions in main flow; use return values:**

```python
# BAD
def update_task(self, task_id: int, title: str) -> None:
    task = self._get_task_or_raise(task_id)  # NO!
    task.title = title

# GOOD
def update_task(self, task_id: int, title: str) -> bool:
    task = self.get_task(task_id)
    if not task:
        return False  # Caller handles the error
    # ... update logic ...
    return True
```

**CLI messages are user-facing:**

```python
# BAD
raise ValueError("Task not found")  # Stack trace exposed!

# GOOD
if not task:
    print("Error: Task ID 99 not found. Valid IDs: 1, 2, 3")
    return  # Clean exit, no stack trace
```

## Development Workflow (TDD)

**RED Phase**: Write tests first (they will FAIL)

```bash
# Phase B: Tasks T010-T011
pytest tests/test_task_model.py -v  # All 6 tests FAIL
pytest tests/test_task_manager.py -v  # All 13 tests FAIL
```

**GREEN Phase**: Implement code (tests PASS)

```bash
# Phase B: Tasks T020-T021
# Implement src/models/task.py
# Implement src/services/task_manager.py
pytest tests/test_task_model.py -v  # All 6 tests now PASS
pytest tests/test_task_manager.py -v  # All 13 tests now PASS
```

**REFACTOR Phase**: Clean code while tests stay GREEN

```bash
# Improve readability, optimize performance
pytest tests/ -v  # All tests still PASS
```

## Validation Checklist

Before finalizing Phase I, verify:

- [ ] All 53 tests pass (19 unit + 9 integration + 25 acceptance)
- [ ] All 17 spec scenarios validated
- [ ] All 5 edge cases handled gracefully
- [ ] Manual validation checklist 100% complete
- [ ] No manual code edits (100% AI-generated)
- [ ] TDD discipline enforced (tests fail first, then pass)
- [ ] Code follows PEP 8 style guidelines
- [ ] Error messages clear and actionable
- [ ] All 5 features work without errors
- [ ] Typical 3-task workflow <10 seconds
- [ ] Documentation complete
- [ ] Ready to commit and create PR

## Running the Application

```bash
# Installation
uv sync

# Run with help
python src/main.py help

# Add tasks
python src/main.py add "Buy groceries"
python src/main.py add "Call mom" --description "This weekend"

# List tasks
python src/main.py list
python src/main.py list --format json

# Other commands
python src/main.py complete 1
python src/main.py update 1 --title "New title"
python src/main.py delete 2
python src/main.py incomplete 1
```

## References

- **Specification**: `/specs/001-core-todos/spec.md` (user stories, requirements, edge cases)
- **Implementation Plan**: `/specs/001-core-todos/plan.md` (architecture, decisions, phases)
- **Task Breakdown**: `/specs/001-core-todos/tasks.md` (20 tasks, 53 tests, TDD workflow)
- **Constitution**: `/.specify/memory/constitution.md` (project principles and governance)

---

**Phase I Status**: Implementation-ready
**Approach**: Spec-driven, AI-native, TDD-first
**Success Metric**: All acceptance criteria pass without manual edits
