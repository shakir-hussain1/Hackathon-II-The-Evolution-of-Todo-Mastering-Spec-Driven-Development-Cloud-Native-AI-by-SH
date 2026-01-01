# ADR-003: Return-Value Error Handling (No Exceptions in Main Flow)

**Date**: 2026-01-01
**Status**: ACCEPTED
**Context**: Phase I - Core Logic Error Handling Strategy
**Deciders**: TDD Discipline, Test Clarity, Explicit Control Flow

## Problem Statement

How should TaskManager and CLI commands report errors - via exceptions, return values, or result objects?

## Decision

Use **return values** for error handling in the main happy path. Exceptions are avoided for expected errors:

### TaskManager Pattern
```python
def update_task(self, task_id: int, title, description) -> bool:
    """Returns True on success, False if task not found"""
    task = self.get_task(task_id)
    if not task:
        return False  # No exception, just False
    # ... update logic ...
    return True
```

### CLI Command Pattern
```python
def update_command(task_manager: TaskManager, args) -> None:
    """Print error message on failure, return None"""
    if not isinstance(args.id, int):
        try:
            args.id = int(args.id)
        except (ValueError, TypeError):
            print("Error: Invalid ID format")
            return  # Exit on error, no exception

    # ... validation and execution ...
```

## Rationale

### 1. **Explicit Control Flow**
- **Readability**: Error paths are visible in regular code, not hidden in try/catch blocks
- **Testability**: Tests can directly assert return values without exception handling
- **Predictability**: No surprise exceptions to unwind the stack

### 2. **TDD Alignment**
- **Test Clarity**: `assert result == True` or `assert result == False` is clearer than checking exception type
- **Test Simplicity**: No need for `pytest.raises(ValueError)` for expected errors
- **Happy Path Focus**: Core logic tests focus on success cases, error cases are explicit

### 3. **CLI Appropriateness**
- **User Feedback**: Errors are printed to stdout, not thrown to console
- **Graceful Degradation**: One command failing doesn't crash the app
- **Error Messages**: Clear, actionable messages tell users exactly what went wrong

### 4. **Phase II Readiness**
- **HTTP Status Codes**: Transition to API is natural (bool → HTTP 200/404)
- **Result Monads**: Return values support future Result[T, E] pattern
- **Transaction Support**: Makes it easier to implement rollback on error

## Implementation Examples

### TaskManager
```python
# get_task returns Optional[Task]
def get_task(self, task_id: int) -> Task | None:
    for task in self._tasks:
        if task.id == task_id:
            return task
    return None  # Explicit None on not found

# update_task returns bool
def update_task(self, task_id, title, description) -> bool:
    task = self.get_task(task_id)
    if not task:
        return False  # No exception
    # ... update logic ...
    return True

# toggle_task_status returns bool
def toggle_task_status(self, task_id: int) -> bool:
    task = self.get_task(task_id)
    if not task:
        return False  # No exception
    # ... toggle logic ...
    return True
```

### CLI Commands
```python
# Validate and print error, don't raise
def update_command(tm: TaskManager, args) -> None:
    if not task_manager.get_task(task_id):
        print(f"Error: Task ID {task_id} not found")
        return  # Exit gracefully

    if not title and not description:
        print("Error: At least one field required")
        return  # Exit gracefully

    # Execute on success
    if tm.update_task(task_id, title, description):
        print(f"Task {task_id} updated")
```

## Consequences

### Positive
- ✓ Explicit error handling in code (easier to understand)
- ✓ Simpler tests (assert bool, not exception type)
- ✓ Graceful error messages for CLI users
- ✓ No exception overhead in hot paths
- ✓ Natural transition to API status codes
- ✓ Easier to implement undo/rollback
- ✓ Clearer code flow (no hidden exits via exceptions)

### Negative
- ✗ Developers must remember to check return values
- ✗ More verbose than raise statement
- ✗ Requires explicit validation at each level
- ✗ Hard to enforce return value checking at compile time

### Mitigations
- **Code Review**: Enforce checking return values
- **Type Hints**: Use bool or Optional[T] to signal error paths
- **Tests**: Comprehensive tests verify all error paths
- **Linting**: Disable unused return value warnings during code review

## Alternatives Considered

### 1. Exceptions for All Errors (rejected)
```python
# Rejected approach
def update_task(self, task_id, title, description):
    task = self.get_task(task_id)
    if not task:
        raise TaskNotFoundError(task_id)  # Exception approach
```
- **Problem**: Exceptions for expected errors (task not found) is anti-pattern
- **Problem**: Makes tests verbose and cluttered with try/catch
- **Problem**: Harder to transition to HTTP APIs

### 2. Result[T, E] Monad (rejected for Phase I)
```python
# Future Phase II consideration
def update_task(self, ...) -> Result[Task, Error]:
    if not task:
        return Err(TaskNotFoundError())
    return Ok(updated_task)
```
- **Advantage**: Type-safe error handling
- **Disadvantage**: Adds complexity not needed for Phase I
- **Plan**: Consider for Phase II with async/await

### 3. Callback/Handler Pattern (rejected)
```python
# Rejected approach
def update_task(self, ..., on_error: Callable):
    task = self.get_task(task_id)
    if not task:
        on_error(f"Task {task_id} not found")
        return
```
- **Problem**: Overly complex for Phase I
- **Problem**: Harder to test

## Validation

- ✓ All 19 TaskManager tests verify return values
- ✓ All 9 CLI tests check return values and printed output
- ✓ 51 acceptance tests validate error messages
- ✓ Integration tests verify no exceptions in normal operation

## Edge Cases Handled

- ✓ Invalid ID format: Returns False, prints "Invalid ID format"
- ✓ Task not found: Returns False/None, lists valid IDs in error message
- ✓ Empty title: Returns False, prints "Title cannot be empty"
- ✓ Missing required field: Returns None, prints error
- ✓ Multiple errors: Checks in priority order, returns at first error

## Related ADRs

- ADR-001: Immutable Task Model (why updates return new Task)
- ADR-004: Layered Architecture (responsibility separation)

## Revision History

- **2026-01-01**: Initial decision - return values for expected errors, no exceptions in main flow
