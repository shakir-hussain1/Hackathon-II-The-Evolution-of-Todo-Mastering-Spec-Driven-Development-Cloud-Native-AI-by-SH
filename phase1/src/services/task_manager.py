"""Task management service for in-memory todo application."""

from src.models.task import Task, TaskStatus


class TaskManager:
    """In-memory CRUD service for tasks."""

    def __init__(self):
        """Initialize TaskManager with empty task list."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the list.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The newly created Task
        """
        task = Task.create(title, description, self._next_id)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[Task]:
        """Get all tasks in insertion order.

        Returns:
            Copy of all tasks (prevents external mutation)
        """
        return list(self._tasks)

    def get_task(self, task_id: int) -> Task | None:
        """Get task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self, task_id: int, title: str | None, description: str | None
    ) -> bool:
        """Update task title and/or description by ID.

        Args:
            task_id: Task ID to update
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            True if success, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        new_title = title if title is not None else task.title
        new_description = (
            description if description is not None else task.description
        )

        # Create new task (Task is immutable, replace in list)
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            status=task.status,
            created_at=task.created_at,
        )
        idx = self._tasks.index(task)
        self._tasks[idx] = updated_task
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID.

        Args:
            task_id: Task ID to delete

        Returns:
            True if success, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False
        self._tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """Toggle task completion status (incomplete <-> complete).

        Args:
            task_id: Task ID to toggle

        Returns:
            True if success, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False

        new_status = (
            TaskStatus.COMPLETE
            if task.status == TaskStatus.INCOMPLETE
            else TaskStatus.INCOMPLETE
        )

        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=new_status,
            created_at=task.created_at,
        )
        idx = self._tasks.index(task)
        self._tasks[idx] = updated_task
        return True
