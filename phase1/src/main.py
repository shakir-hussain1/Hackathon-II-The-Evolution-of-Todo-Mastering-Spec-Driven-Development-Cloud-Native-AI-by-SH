"""Entry point and CLI router for todo application."""

import argparse
import sys
from src.services.task_manager import TaskManager
from src.cli.commands import (
    add_command,
    list_command,
    update_command,
    delete_command,
    complete_command,
    incomplete_command,
)


def main():
    """Main entry point with argparse CLI setup and command routing."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="In-memory Python todo application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py add "Buy groceries"
  python src/main.py add "Call mom" --description "This weekend"
  python src/main.py list
  python src/main.py list --format json
  python src/main.py update 1 --title "New title"
  python src/main.py complete 1
  python src/main.py incomplete 1
  python src/main.py delete 1
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (required)")
    add_parser.add_argument(
        "--description",
        "-d",
        help="Task description (optional)",
        default="",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--format",
        "-f",
        choices=["human", "json"],
        default="human",
        help="Output format (default: human)",
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID to update")
    update_parser.add_argument(
        "--title",
        "-t",
        help="New task title",
    )
    update_parser.add_argument(
        "--description",
        "-d",
        help="New task description",
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, help="Task ID to complete")

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
    incomplete_parser.add_argument("id", type=int, help="Task ID to mark incomplete")

    # Help command (implicit via -h, but explicit for consistency)
    help_parser = subparsers.add_parser("help", help="Display help message")

    # Parse arguments
    args = parser.parse_args()

    # Handle no command case
    if not args.command:
        parser.print_help()
        return

    # Initialize task manager
    task_manager = TaskManager()

    # Route to appropriate command handler
    if args.command == "add":
        add_command(task_manager, args)
    elif args.command == "list":
        list_command(task_manager, args)
    elif args.command == "update":
        update_command(task_manager, args)
    elif args.command == "delete":
        delete_command(task_manager, args)
    elif args.command == "complete":
        complete_command(task_manager, args)
    elif args.command == "incomplete":
        incomplete_command(task_manager, args)
    elif args.command == "help":
        parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
