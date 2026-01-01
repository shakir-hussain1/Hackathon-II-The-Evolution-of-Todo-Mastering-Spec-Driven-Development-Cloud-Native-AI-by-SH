"""Task data model for in-memory todo application."""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone


class TaskStatus(Enum):
    """Task completion status."""

    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


@dataclass(frozen=True)
class Task:
    """Immutable task data class."""

    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime

    @classmethod
    def create(
        cls, title: str, description: str = "", auto_id: int = None
    ) -> "Task":
        """Factory method to create a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)
            auto_id: Auto-generated task ID

        Returns:
            New Task instance with INCOMPLETE status
        """
        return cls(
            id=auto_id,
            title=title,
            description=description,
            status=TaskStatus.INCOMPLETE,
            created_at=datetime.now(timezone.utc),
        )

    def __str__(self) -> str:
        """Human-readable task representation."""
        status_indicator = "[x]" if self.status == TaskStatus.COMPLETE else "[ ]"
        return f"{self.id}. {status_indicator} {self.title}"
