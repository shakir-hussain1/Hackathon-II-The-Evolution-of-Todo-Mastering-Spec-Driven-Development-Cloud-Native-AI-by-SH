# ADR-001: Immutable Task Model Using Frozen Dataclass

**Date**: 2026-01-01
**Status**: ACCEPTED
**Context**: Phase I - In-Memory Python Todo CLI
**Deciders**: AI Architecture + TDD Discipline

## Problem Statement

How should we represent the Task entity to ensure data consistency, enable easy testing, and prepare for Phase II database persistence?

## Decision

Use a **frozen (immutable) Python dataclass** to represent the Task model:

```python
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
```

## Rationale

### 1. **Immutability Benefits**
- **Thread-safe by design**: No synchronization needed for concurrent access
- **Predictable behavior**: Once created, a Task never changes unexpectedly
- **Easier debugging**: State transitions are explicit via task replacement, not mutation

### 2. **Dataclass Advantages**
- **Automatic __init__, __repr__, __eq__**: Reduces boilerplate
- **Type hints support**: IDE autocomplete and type checking
- **Factory method pattern**: Task.create() provides a clean constructor alternative

### 3. **Phase II Readiness**
- **ORM-friendly**: Immutable entities map naturally to database rows
- **Audit trail support**: Immutability encourages event sourcing patterns
- **Snapshot semantics**: Easy to implement versioning and undo features

### 4. **Testing Benefits**
- **Deterministic equality**: Frozen dataclasses implement __eq__ automatically
- **No hidden side effects**: Tests can safely reuse Task instances
- **Clear test expectations**: Assertions on immutable values are more reliable

## Implementation

```python
# Create with factory method
task = Task.create("Buy groceries", "At store", auto_id=1)

# Cannot mutate
task.title = "New title"  # Raises FrozenInstanceError

# Update by replacement
updated_task = Task(
    id=task.id,
    title="New title",
    description=task.description,
    status=task.status,
    created_at=task.created_at,
)
```

## Consequences

### Positive
- ✓ Safe concurrent access without locks
- ✓ Transparent state management (all changes are explicit)
- ✓ Natural transition to database entities
- ✓ Enhanced testability with automatic equality
- ✓ Supports undo/redo implementation in future phases

### Negative
- ✗ Cannot modify Task in-place (requires replacement)
- ✗ Slightly higher memory usage (creating new objects instead of mutating)
- ✗ Developers must adapt to functional thinking style

### Trade-offs Accepted
- Memory overhead is acceptable for Phase I (in-memory only, small datasets)
- Replacement pattern is explicit and clear, aiding code comprehension
- Immutability cost pays off in Phase II with database integration

## Alternatives Considered

### 1. Mutable Dataclass (rejected)
- **Advantage**: Direct mutation (slightly faster)
- **Disadvantage**: Harder to track state changes, less testable, harder to add audit logging

### 2. Regular Class with Properties (rejected)
- **Advantage**: Fine-grained control over mutations
- **Disadvantage**: More boilerplate, harder to implement __eq__, no type hints support

### 3. Named Tuple (rejected)
- **Advantage**: Built-in immutability
- **Disadvantage**: Less flexible (can't add methods easily), less readable in code

## Validation

- ✓ All 8 unit tests for Task model pass
- ✓ Immutability verified (FrozenInstanceError on mutation attempt)
- ✓ Equality semantics tested (same fields = equal objects)
- ✓ String representation tested ([ ] and [x] status indicators)
- ✓ 87 total tests validate integration with TaskManager

## Related ADRs

- ADR-003: Return-Value Error Handling (relates to update semantics)
- ADR-004: Layered Architecture (Task model as foundational layer)

## Revision History

- **2026-01-01**: Initial decision - frozen dataclass pattern selected
