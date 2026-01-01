# ADR-004: Layered Architecture (Models → Services → CLI)

**Date**: 2026-01-01
**Status**: ACCEPTED
**Context**: Phase I - Architectural Design for Scalability
**Deciders**: Clean Architecture Principles, Phase II Transition Planning

## Problem Statement

How should we organize code to maximize testability, maintainability, and readiness for future phases (web API, multiple clients)?

## Decision

Implement **three-layer architecture**:

```
┌─────────────────────────────────┐
│  CLI Layer (commands.py)        │ User Interface
│  - User input handling          │ - Command line interface
│  - Output formatting            │ - Argument parsing (main.py)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  Service Layer (task_manager.py)│ Business Logic
│  - CRUD operations              │ - Data validation
│  - State management             │ - Task orchestration
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│  Model Layer (task.py)          │ Data Representation
│  - Task entity                  │ - Immutable dataclass
│  - Status enum                  │ - Factory methods
└─────────────────────────────────┘
```

## Rationale

### 1. **Separation of Concerns**
Each layer has a single responsibility:
- **Models**: Data representation and immutability
- **Services**: Business rules and state management
- **CLI**: User interaction and I/O handling

### 2. **Testability Benefits**
- **Unit Test Models**: Test Task creation and properties (no dependencies)
- **Unit Test Services**: Test TaskManager CRUD without CLI (19 tests, 100% coverage)
- **Integration Test CLI**: Test command handlers with mocked TaskManager (9 tests)
- **Acceptance Test Workflows**: Test end-to-end scenarios (51 tests)

### 3. **Phase II Transition**
- **API Layer Addition**: Phase II adds FastAPI endpoints above Service layer
- **Database Layer Addition**: Phase II adds persistence below Service layer
- **No Refactoring Needed**: Service layer unchanged when adding new I/O layers

### 4. **Reusability**
- **Service Layer Reuse**: Same TaskManager works for CLI, API, and future GUI
- **Model Reuse**: Task entity used by all layers without modification
- **Zero Coupling**: Models don't know about services or CLI

## File Organization

```
src/
├── models/
│   ├── __init__.py
│   └── task.py             # Task, TaskStatus
├── services/
│   ├── __init__.py
│   └── task_manager.py     # TaskManager CRUD
├── cli/
│   ├── __init__.py
│   └── commands.py         # add, list, update, delete, complete, incomplete
├── main.py                 # Argparse, routing
└── __init__.py
```

## Implementation Details

### Model Layer (task.py)
```python
# No dependencies on services or CLI
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
```

### Service Layer (task_manager.py)
```python
# Depends only on models
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        # Pure business logic
        pass
```

### CLI Layer (commands.py)
```python
# Depends on models and services
def add_command(task_manager: TaskManager, args) -> None:
    # Get user input from args
    # Call service method
    # Format and print output
    pass
```

### Entry Point (main.py)
```python
# Wires everything together
def main():
    parser = argparse.ArgumentParser()
    # ... argparse setup ...
    task_manager = TaskManager()  # Instantiate service
    # ... route to CLI commands ...
```

## Dependency Graph

```
CLI Commands ──┐
               │
CLI Commands ──┼──> TaskManager ──┐
               │                  │
CLI Commands ──┘                  ├──> Task (Model)
                                  │
Entry Point (main.py) ────────────┘
```

**Key Property**: No circular dependencies. Everything flows downward.

## Consequences

### Positive
- ✓ Clean separation of concerns
- ✓ Easy to test each layer independently
- ✓ Natural transition to multi-client architecture
- ✓ Service layer reusable across interfaces (CLI, API, GUI, etc.)
- ✓ Model layer completely independent
- ✓ Straightforward to add new features
- ✓ Clear responsibility boundaries

### Negative
- ✗ More classes and files than monolithic approach
- ✗ More boilerplate for small applications
- ✗ Overhead for simple use cases (mitigated: Phase I is small)

### Scalability Notes
- **Phase I (Current)**: 4 files, 3 layers - perfect for MVP
- **Phase II**: Add API layer above Service, persistence layer below
- **Phase III+**: Scale horizontally with consistent interface

## Alternatives Considered

### 1. Monolithic Single File (rejected)
```python
# Rejected: No separation
class Task: ...
class TaskManager: ...
def add_command(): ...
def main(): ...
```
- **Problem**: Hard to test (everything coupled)
- **Problem**: Hard to extend (everything intertwined)
- **Problem**: Hard to reuse service layer

### 2. Package-Per-Feature Structure (rejected for Phase I)
```python
# Rejected: Over-engineered for Phase I
todo/
├── add_feature/
│   ├── models.py
│   ├── services.py
│   └── cli.py
├── complete_feature/
│   ├── models.py
│   ├── services.py
│   └── cli.py
```
- **Problem**: Over-complicates Phase I
- **Advantage**: Would be ideal for large Phase II
- **Plan**: Consider for Phase II restructuring

### 3. MVC Architecture (rejected)
- **Problem**: GUI-centric, not appropriate for CLI
- **Problem**: Requires View layer for CLI (over-engineered)

## Validation

- ✓ Model layer: 8 unit tests, 100% coverage, zero dependencies
- ✓ Service layer: 19 unit tests, 100% coverage, only model dependencies
- ✓ CLI layer: 9 integration tests, 96% coverage, service + model dependencies
- ✓ Entry point: Tested via integration tests and E2E validation
- ✓ 51 acceptance tests validate complete workflows

## Design Patterns Used

### Factory Pattern (Models)
```python
class Task:
    @classmethod
    def create(cls, title: str, description: str = "", auto_id: int = None):
        return cls(id=auto_id, ...)
```

### CRUD Service Pattern (Services)
```python
class TaskManager:
    def create(self, ...): ...    # add_task
    def read(self, ...): ...      # get_task, list_tasks
    def update(self, ...): ...    # update_task
    def delete(self, ...): ...    # delete_task
```

### Command Handler Pattern (CLI)
```python
def add_command(task_manager: TaskManager, args): ...
def list_command(task_manager: TaskManager, args): ...
# Easy to extend with new commands
```

## Future Extensions

### Phase II: Add API Layer
```
┌──────────────────────────┐
│  FastAPI Layer           │ (New)
│  - /tasks endpoint       │
│  - JSON serialization    │
└────────┬─────────────────┘
         │
    [Service Layer] ← Reused
    [Model Layer]   ← Reused
```

### Phase III: Add Persistence Layer
```
┌─────────────────────┐
│  CLI / API Layers   │
└────────┬────────────┘
         │
    [Service Layer]
         │
    ┌────┴─────────────┬──────────────┐
    │                  │              │
[In-Memory]     [SQLite]        [PostgreSQL]
(Phase I)       (Phase II)       (Phase III)
```

## Related ADRs

- ADR-001: Immutable Task Model (foundation for separation)
- ADR-002: In-Memory Storage (model layer doesn't know about storage)
- ADR-003: Return-Value Error Handling (enables service layer testing)
- ADR-005: Argparse CLI (entry point layer)

## Revision History

- **2026-01-01**: Initial decision - three-layer architecture for separation of concerns
