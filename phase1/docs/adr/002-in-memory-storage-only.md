# ADR-002: In-Memory Storage Only (No Persistence)

**Date**: 2026-01-01
**Status**: ACCEPTED
**Context**: Phase I - MVP Development
**Deciders**: Specification Requirements, Phase I Scope

## Problem Statement

Should Phase I implement data persistence to a database or file system, or use in-memory storage only?

## Decision

Implement **in-memory storage only** with NO persistence to database, file system, or any external store.

Storage is managed by a simple Python list in TaskManager:

```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1
```

## Rationale

### 1. **Phase I Scope Clarity**
- **MVP Focus**: Validate core business logic and CLI interface
- **Specification Requirement**: Explicitly states "in-memory only" in Phase I
- **Time to Market**: Eliminates database setup, schema, migrations, ORM complexity

### 2. **Testing Benefits**
- **Test Isolation**: Each test gets a fresh TaskManager instance, no cleanup needed
- **Deterministic Tests**: No race conditions or database state pollution
- **Fast Tests**: 87 tests execute in <1 second with in-memory storage

### 3. **Phase II Transition Plan**
- **Clean Extraction**: TaskManager interface doesn't depend on storage implementation
- **Dependency Injection**: Future phases can inject different storage backends
- **Zero Lock-In**: No hardcoded database assumptions or ORM bindings

### 4. **Specification Alignment**
- Matches Phase I requirements exactly: "in-memory, single-user, no persistence"
- Explicitly documented in README.md
- Expected behavior: "Tasks are lost when the application exits"

## Implementation

```python
class TaskManager:
    def __init__(self):
        self._tasks: list[Task] = []        # In-memory storage
        self._next_id: int = 1

    def add_task(self, title, description="") -> Task:
        """Create task and store in memory list"""
        task = Task.create(title, description, self._next_id)
        self._tasks.append(task)             # Direct list append
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """Return copy to prevent external mutation"""
        return list(self._tasks)             # Defensive copy
```

## Consequences

### Positive
- ✓ Zero external dependencies (no database, no file system)
- ✓ Simplest possible implementation
- ✓ Fast, deterministic tests
- ✓ Easy to understand code
- ✓ Perfect for MVP validation
- ✓ Natural transition to Phase II persistence

### Negative
- ✗ No data persistence (tasks lost on app exit)
- ✗ Single-process only (no multi-process support)
- ✗ Single-user only (no multi-user scenarios)
- ✗ Limited to available RAM (no scalability)

### Explicit Trade-offs
- **Usability** vs **Functionality**: Phase I trades persistence for fast delivery
- **Scale** vs **Simplicity**: Accepts in-memory limits for ease of implementation
- **Data Loss** vs **Focus**: Explicitly accepts data loss to focus on core logic

## Alternatives Considered

### 1. SQLite File-Based (rejected)
- **Advantage**: Data persists, supports multi-process
- **Disadvantage**: Adds complexity, testing headache, out of scope for Phase I
- **Decision**: Deferred to Phase II

### 2. JSON File Storage (rejected)
- **Advantage**: Simple, human-readable
- **Disadvantage**: Race conditions, manual serialization, out of scope
- **Decision**: Deferred to Phase II

### 3. In-Memory with JSON Export (partial - rejected for Phase I)
- **Advantage**: Persistence option without DB
- **Disadvantage**: Adds complexity, not required by Phase I spec
- **Decision**: Consider for Phase II

## Validation

- ✓ All 19 TaskManager tests pass with in-memory storage
- ✓ Defensive copy pattern tested (list_tasks returns copy, not reference)
- ✓ Edge case tested: 1000+ tasks handled without issue
- ✓ Specification conformance: "in-memory only" explicitly tested

## Phase II Plan

In Phase II, the TaskManager interface remains the same, but storage is abstracted:

```python
# Future Phase II design (not implemented)
class TaskManager:
    def __init__(self, storage_backend=InMemoryStorage()):
        self._storage = storage_backend
```

This allows Phase II to inject DatabaseStorage or FileStorage without changing TaskManager logic.

## Related ADRs

- ADR-004: Layered Architecture (TaskManager as service layer)
- ADR-005: Argparse CLI (stateless commands, reset between invocations)

## Revision History

- **2026-01-01**: Initial decision - in-memory only for Phase I, database deferred to Phase II
