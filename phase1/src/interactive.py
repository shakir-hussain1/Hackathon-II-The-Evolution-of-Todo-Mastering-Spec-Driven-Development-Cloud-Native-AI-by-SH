"""Interactive CLI for Todo Application - Phase 1."""

import sys
from pathlib import Path

# Add parent directory to path to allow imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.services.task_manager import TaskManager
    from src.cli.commands import (
        add_command,
        list_command,
        update_command,
        delete_command,
        complete_command,
        incomplete_command,
    )
except ImportError:
    from services.task_manager import TaskManager
    from cli.commands import (
        add_command,
        list_command,
        update_command,
        delete_command,
        complete_command,
        incomplete_command,
    )


class Args:
    """Mock args object for commands."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def print_help():
    """Print available commands."""
    print("""
========================================
       TODO CLI - AVAILABLE COMMANDS
========================================
  add <title>                 - Add new task
  add <title> -d <desc>       - Add task with description
  list                        - List all tasks
  list json                   - List tasks as JSON
  complete <id>               - Mark task complete
  incomplete <id>             - Mark task incomplete
  update <id> -t <title>      - Update task title
  update <id> -d <desc>       - Update task description
  delete <id>                 - Delete task
  help                        - Show this help
  exit                        - Exit application
========================================
""")


def main():
    """Run interactive CLI."""
    task_manager = TaskManager()

    print("\n" + "="*50)
    print("   PHASE 1 - TODO IN-MEMORY CLI APPLICATION")
    print("="*50)
    print("Type 'help' for commands, 'exit' to quit\n")

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command == "exit" or command == "quit":
                print("Goodbye!")
                break

            elif command == "help":
                print_help()

            elif command == "add":
                if len(parts) < 2:
                    print("Error: Title required. Usage: add <title>")
                    continue

                # Check for description flag
                title = ""
                description = ""

                if "-d" in parts:
                    d_index = parts.index("-d")
                    title = " ".join(parts[1:d_index])
                    description = " ".join(parts[d_index+1:])
                else:
                    title = " ".join(parts[1:])

                args = Args(title=title, description=description)
                add_command(task_manager, args)

            elif command == "list":
                format_type = "human"
                if len(parts) > 1 and parts[1].lower() == "json":
                    format_type = "json"
                args = Args(format=format_type)
                list_command(task_manager, args)

            elif command == "complete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: complete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    args = Args(id=task_id)
                    complete_command(task_manager, args)
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "incomplete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: incomplete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    args = Args(id=task_id)
                    incomplete_command(task_manager, args)
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "update":
                if len(parts) < 4:
                    print("Error: Usage: update <id> -t <title> OR update <id> -d <desc>")
                    continue
                try:
                    task_id = int(parts[1])
                    title = None
                    description = None

                    if "-t" in parts:
                        t_index = parts.index("-t")
                        # Find where description starts (if any)
                        if "-d" in parts:
                            d_index = parts.index("-d")
                            title = " ".join(parts[t_index+1:d_index])
                            description = " ".join(parts[d_index+1:])
                        else:
                            title = " ".join(parts[t_index+1:])
                    elif "-d" in parts:
                        d_index = parts.index("-d")
                        description = " ".join(parts[d_index+1:])

                    args = Args(id=task_id, title=title, description=description)
                    update_command(task_manager, args)
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "delete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: delete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    args = Args(id=task_id)
                    delete_command(task_manager, args)
                except ValueError:
                    print("Error: Invalid ID format")

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
