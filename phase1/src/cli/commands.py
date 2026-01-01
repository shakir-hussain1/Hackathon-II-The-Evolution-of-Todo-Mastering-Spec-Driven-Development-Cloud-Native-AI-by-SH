"""CLI command handlers for todo application."""

import json
from src.services.task_manager import TaskManager


def add_command(task_manager: TaskManager, args) -> None:
    """Handle 'add' command: create a new task.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with 'title' and 'description'
    """
    title = args.title
    description = args.description or ""

    if not title or not title.strip():
        print("Error: Title is required")
        return

    task = task_manager.add_task(title, description)
    print(f"Task {task.id} added: {task.title}")


def list_command(task_manager: TaskManager, args) -> None:
    """Handle 'list' command: display all tasks.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with optional 'format'
    """
    tasks = task_manager.list_tasks()

    if not tasks:
        print("No tasks")
        return

    format_type = getattr(args, "format", "human")

    if format_type == "json":
        tasks_data = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]
        print(json.dumps({"tasks": tasks_data}, indent=2))
    else:
        # Human-readable format
        for task in tasks:
            print(task)


def update_command(task_manager: TaskManager, args) -> None:
    """Handle 'update' command: modify task title and/or description.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with 'id', 'title', 'description'
    """
    task_id = args.id
    title = getattr(args, "title", None)
    description = getattr(args, "description", None)

    if not isinstance(task_id, int):
        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            print("Error: Invalid ID format")
            return

    if not task_manager.get_task(task_id):
        tasks = task_manager.list_tasks()
        valid_ids = [str(t.id) for t in tasks]
        valid_ids_str = ", ".join(valid_ids) if valid_ids else "none"
        print(
            f"Error: Task ID {task_id} not found. Valid IDs: {valid_ids_str}"
        )
        return

    if title is not None and not title.strip():
        print("Error: Title cannot be empty")
        return

    if title is None and description is None:
        print("Error: At least one of --title or --description must be provided")
        return

    success = task_manager.update_task(task_id, title, description)

    if success:
        task = task_manager.get_task(task_id)
        print(f"Task {task_id} updated: {task.title}")
    else:
        print(f"Error: Could not update task {task_id}")


def delete_command(task_manager: TaskManager, args) -> None:
    """Handle 'delete' command: remove task by ID.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with 'id'
    """
    task_id = args.id

    if not isinstance(task_id, int):
        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            print("Error: Invalid ID format")
            return

    if not task_manager.get_task(task_id):
        tasks = task_manager.list_tasks()
        valid_ids = [str(t.id) for t in tasks]
        valid_ids_str = ", ".join(valid_ids) if valid_ids else "none"
        print(
            f"Error: Task ID {task_id} not found. Valid IDs: {valid_ids_str}"
        )
        return

    success = task_manager.delete_task(task_id)

    if success:
        print(f"Task {task_id} deleted")
    else:
        print(f"Error: Could not delete task {task_id}")


def complete_command(task_manager: TaskManager, args) -> None:
    """Handle 'complete' command: mark task as complete.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with 'id'
    """
    task_id = args.id

    if not isinstance(task_id, int):
        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            print("Error: Invalid ID format")
            return

    if not task_manager.get_task(task_id):
        tasks = task_manager.list_tasks()
        valid_ids = [str(t.id) for t in tasks]
        valid_ids_str = ", ".join(valid_ids) if valid_ids else "none"
        print(
            f"Error: Task ID {task_id} not found. Valid IDs: {valid_ids_str}"
        )
        return

    success = task_manager.toggle_task_status(task_id)

    if success:
        task = task_manager.get_task(task_id)
        print(f"Task {task_id} marked complete: {task.title}")
    else:
        print(f"Error: Could not complete task {task_id}")


def incomplete_command(task_manager: TaskManager, args) -> None:
    """Handle 'incomplete' command: mark task as incomplete.

    Args:
        task_manager: TaskManager instance
        args: Parsed arguments with 'id'
    """
    task_id = args.id

    if not isinstance(task_id, int):
        try:
            task_id = int(task_id)
        except (ValueError, TypeError):
            print("Error: Invalid ID format")
            return

    if not task_manager.get_task(task_id):
        tasks = task_manager.list_tasks()
        valid_ids = [str(t.id) for t in tasks]
        valid_ids_str = ", ".join(valid_ids) if valid_ids else "none"
        print(
            f"Error: Task ID {task_id} not found. Valid IDs: {valid_ids_str}"
        )
        return

    success = task_manager.toggle_task_status(task_id)

    if success:
        task = task_manager.get_task(task_id)
        print(f"Task {task_id} marked incomplete: {task.title}")
    else:
        print(f"Error: Could not mark task incomplete {task_id}")
