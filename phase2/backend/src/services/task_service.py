"""
Task service for business logic and database operations.

Handles all task-related operations with user isolation enforcement.
"""

from sqlmodel import Session, select
from datetime import datetime
from typing import Optional, List

from src.db.models import Task
from src.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """Service class for task operations."""

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_data: TaskCreate,
    ) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: ID of task owner
            task_data: Task creation data (title, description)

        Returns:
            Created Task object

        Raises:
            ValueError: If validation fails
        """
        # Create task with user_id ownership
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status="incomplete",
        )

        # Persist to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def get_user_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None,
    ) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by status.

        IMPORTANT: Query is always filtered by user_id for security.

        Args:
            session: Database session
            user_id: ID of task owner
            status: Optional status filter ("incomplete" or "complete")

        Returns:
            List of Task objects
        """
        # Build query with user_id filter (CRITICAL for security)
        query = select(Task).where(Task.user_id == user_id)

        # Optional status filter
        if status:
            query = query.where(Task.status == status)

        # Order by creation time (newest first)
        query = query.order_by(Task.created_at.desc())

        return session.exec(query).all()

    @staticmethod
    def get_task(
        session: Session,
        task_id: int,
        user_id: str,
    ) -> Optional[Task]:
        """
        Get a single task by ID, verifying ownership.

        IMPORTANT: Query includes user_id filter to prevent cross-user access.

        Args:
            session: Database session
            task_id: ID of task to retrieve
            user_id: ID of authenticated user (must own task)

        Returns:
            Task object or None if not found or not owned by user
        """
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,  # CRITICAL: Verify ownership
        )

        return session.exec(query).first()

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        user_id: str,
        task_data: TaskUpdate,
    ) -> Optional[Task]:
        """
        Update a task, verifying ownership.

        Only updates provided fields. Status cannot be updated via this method.

        Args:
            session: Database session
            task_id: ID of task to update
            user_id: ID of authenticated user (must own task)
            task_data: Update data (title, description)

        Returns:
            Updated Task object or None if not found or not owned by user
        """
        # Get task and verify ownership
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return None

        # Update fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Persist to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(
        session: Session,
        task_id: int,
        user_id: str,
    ) -> bool:
        """
        Delete a task, verifying ownership.

        Args:
            session: Database session
            task_id: ID of task to delete
            user_id: ID of authenticated user (must own task)

        Returns:
            True if deleted, False if not found or not owned by user
        """
        # Get task and verify ownership
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return False

        # Delete from database
        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_status(
        session: Session,
        task_id: int,
        user_id: str,
    ) -> Optional[Task]:
        """
        Toggle task completion status, verifying ownership.

        Flips status between "incomplete" and "complete".

        Args:
            session: Database session
            task_id: ID of task to toggle
            user_id: ID of authenticated user (must own task)

        Returns:
            Updated Task object or None if not found or not owned by user
        """
        # Get task and verify ownership
        task = TaskService.get_task(session, task_id, user_id)
        if not task:
            return None

        # Toggle status
        task.status = "complete" if task.status == "incomplete" else "incomplete"

        # Update timestamp
        task.updated_at = datetime.utcnow()

        # Persist to database
        session.add(task)
        session.commit()
        session.refresh(task)

        return task
