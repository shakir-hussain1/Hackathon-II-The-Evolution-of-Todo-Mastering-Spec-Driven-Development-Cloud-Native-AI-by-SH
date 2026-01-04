# ADR-005: Argparse Subparser CLI with Command Handlers

**Date**: 2026-01-01
**Status**: ACCEPTED
**Context**: Phase I - CLI Interface Design
**Deciders**: Python Standard Library, Command-Based Interface

## Problem Statement

What is the best approach for implementing a command-line interface that is:
- Easy to extend with new commands?
- Provides built-in help?
- Validates arguments cleanly?
- Separates CLI concerns from business logic?

## Decision

Use **Python's argparse with subparsers** to create a command-based CLI:

```python
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# Each command gets its own parser
add_parser = subparsers.add_parser("add", help="Add a new task")
list_parser = subparsers.add_parser("list", help="List all tasks")
# ... more commands ...

# Parse and route
args = parser.parse_args()
if args.command == "add":
    add_command(task_manager, args)
elif args.command == "list":
    list_command(task_manager, args)
```

## Rationale

### 1. **Standard Library**
- No external dependencies (zero additional imports)
- Part of Python since 2.7, very stable
- Familiar to Python developers
- Well-documented with extensive examples

### 2. **Command Structure Benefits**
- **Intuitive**: `python src/main.py add "task"` mirrors system commands
- **Extensible**: Easy to add new commands without changing core logic
- **Discoverable**: Built-in `-h` and `--help` shows all commands
- **Namespace Isolation**: Each command has own argument namespace

### 3. **Help System**
```bash
$ python src/main.py -h
usage: todo [-h] {add,list,update,delete,complete,incomplete,help} ...

$ python src/main.py add -h
usage: todo add [-h] title [-d DESCRIPTION]
```
Automatically generates help from parser configuration.

### 4. **Argument Validation**
```python
# Type conversion built-in
update_parser.add_argument("id", type=int, help="Task ID")
# Positional vs optional args clearly defined
add_parser.add_argument("title", help="Task title (required)")
add_parser.add_argument("--description", "-d", help="Description (optional)")
```

### 5. **Separation of Concerns**
- **main.py**: Parses arguments, instantiates TaskManager, routes to handlers
- **commands.py**: Receives clean args namespace, executes command
- **task_manager.py**: Zero knowledge of CLI, pure business logic

## Implementation

### Full Example
```python
def main():
    parser = argparse.ArgumentParser(
        prog="todo",
        description="In-memory Python todo application"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (required)")
    add_parser.add_argument("--description", "-d", default="")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--format", "-f",
        choices=["human", "json"],
        default="human"
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--title", "-t")
    update_parser.add_argument("--description", "-d")

    # ... more commands ...

    args = parser.parse_args()

    # Instantiate service
    task_manager = TaskManager()

    # Route to handler
    if args.command == "add":
        add_command(task_manager, args)
    elif args.command == "list":
        list_command(task_manager, args)
    # ... more routing ...
```

### Command Handler (Separation of Concerns)
```python
def add_command(task_manager: TaskManager, args) -> None:
    """Handle 'add' command - handler receives clean args"""
    title = args.title
    description = args.description or ""

    if not title or not title.strip():
        print("Error: Title is required")
        return

    task = task_manager.add_task(title, description)
    print(f"Task {task.id} added: {task.title}")
```

## Consequences

### Positive
- ✓ Zero external dependencies
- ✓ Built-in argument validation and type conversion
- ✓ Automatic help system
- ✓ Easy to extend with new commands
- ✓ Clean separation from business logic
- ✓ Familiar to Python developers
- ✓ Positional and optional arguments
- ✓ Mutually exclusive argument groups supported

### Negative
- ✗ Slightly more verbose than Click or Typer
- ✗ Manual command routing (if args.command == "add": ...)
- ✗ Subparser registration is declarative (can't introspect for automatic routing)
- ✗ Less stylish than modern alternatives

### Mitigations
- **Verbosity**: Worth it for zero dependencies and standard library
- **Routing**: Could use decorator pattern in Phase II, acceptable for Phase I

## Alternatives Considered

### 1. Click (rejected)
```python
# Click example (rejected)
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('title')
def add(title):
    pass
```
- **Advantage**: More elegant, less boilerplate
- **Disadvantage**: External dependency, over-engineered for Phase I
- **Decision**: Keep dependencies minimal for Phase I

### 2. Typer (rejected)
```python
# Typer example (rejected - too modern)
import typer
app = typer.Typer()

@app.command()
def add(title: str):
    pass
```
- **Advantage**: Very modern, type-hint based
- **Disadvantage**: External dependency, requires Python 3.6+
- **Decision**: argparse is more widely available

### 3. Manual sys.argv Parsing (rejected)
```python
# Rejected: error-prone, no validation
if len(sys.argv) > 1:
    if sys.argv[1] == "add":
        # ... parse manually ...
```
- **Problem**: No validation, no help system
- **Problem**: Duplicated error handling
- **Problem**: Hard to maintain

### 4. Docopt (rejected)
```python
# Rejected: obscure syntax
Usage: todo add <title> [--description <desc>]
```
- **Problem**: Learning curve for developers
- **Problem**: External dependency

## Validation

- ✓ All 6 commands implemented (add, list, update, delete, complete, incomplete)
- ✓ Help system works: `python src/main.py -h`
- ✓ Per-command help works: `python src/main.py add -h`
- ✓ Argument validation tested (invalid ID format, empty title, etc.)
- ✓ Type conversion tested (string ID converted to int)
- ✓ 9 integration tests validate CLI commands
- ✓ 51 acceptance tests validate complete workflows

## Feature Support

### Implemented
- ✓ Subparsers for commands
- ✓ Positional arguments (title, id)
- ✓ Optional arguments (--description, --title, --format)
- ✓ Short flags (-d for --description, -f for --format)
- ✓ Type conversion (string → int for IDs)
- ✓ Choices validation (format: human/json)
- ✓ Default values
- ✓ Help text

### Could Add (Phase II)
- Mutually exclusive groups (`-t` and `-d` together)
- Action='store_true' for flags
- Argument groups for organization
- Epilog with examples (partially implemented)

## Future Considerations

### Phase II: API Layer
When adding FastAPI endpoints, argparse remains for CLI:
```
┌────────────────────────────┐
│  FastAPI (API routes)      │
└────────────────────────────┘
┌────────────────────────────┐
│  Argparse (CLI routes)     │ ← Unchanged
└────────────────────────────┘
```

### Phase II: Command Routing Improvement
Consider decorator pattern for auto-registration:
```python
@register_command("add")
def add_command(task_manager: TaskManager, args):
    pass

# Auto-routes based on registration
```

## Related ADRs

- ADR-004: Layered Architecture (argparse at CLI layer, separate from service)
- ADR-003: Return-Value Error Handling (handlers return None, print errors)

## Revision History

- **2026-01-01**: Initial decision - argparse with subparsers for extensible CLI
