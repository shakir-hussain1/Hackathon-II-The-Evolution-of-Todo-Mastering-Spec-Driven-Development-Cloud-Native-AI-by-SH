"""Task service with CRUD operations and event publishing"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc, asc
from ..models.task import Task
from ..models.user import User
from ..schemas.task import TaskCreate, TaskUpdate
from ..utils.dapr_client import DaprClientWrapper
from ..utils.cloudevents import create_cloudevent
from ..utils.logging import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service for managing tasks with event-driven architecture"""

    def __init__(self, db: Session, dapr_client: DaprClientWrapper):
        self.db = db
        self.dapr = dapr_client
        self.pubsub_name = "pubsub-kafka"
        self.topic_task_events = "task-events"
        self.topic_task_updates = "task-updates"

    async def create_task(self, user: User, task_data: TaskCreate) -> Task:
        """Create a new task and publish creation event"""
        # Create task entity
        task = Task(
            user_id=user.id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            tags=task_data.tags,
            recurrence_pattern=task_data.recurrence_pattern.dict() if task_data.recurrence_pattern else None
        )

        # Calculate next occurrence for recurring tasks
        if task.recurrence_pattern:
            task.next_occurrence = self._calculate_next_occurrence(task.recurrence_pattern, task.due_date)

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        logger.info(f"Task created: {task.id} by user {user.id}")

        # Publish task.created event
        await self._publish_task_event("com.todo.task.created", task, user.id)

        # Publish sync event for real-time updates
        await self._publish_sync_event("task_created", task)

        return task

    async def update_task(self, task_id: uuid.UUID, user: User, update_data: TaskUpdate) -> Task:
        """Update task with optimistic locking and publish update event"""
        # Fetch task with version check
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user.id,
            Task.deleted_at == None
        ).first()

        if not task:
            raise ValueError("Task not found")

        # Optimistic locking check
        if task.version != update_data.version:
            raise ValueError(f"Version conflict: expected {update_data.version}, got {task.version}")

        # Store old state for event
        old_state = task.to_dict()

        # Update fields
        if update_data.title is not None:
            task.title = update_data.title
        if update_data.description is not None:
            task.description = update_data.description
        if update_data.status is not None:
            task.status = update_data.status
            if update_data.status == "completed" and not task.completed_at:
                task.completed_at = datetime.utcnow()
        if update_data.priority is not None:
            task.priority = update_data.priority
        if update_data.due_date is not None:
            task.due_date = update_data.due_date
        if update_data.tags is not None:
            task.tags = update_data.tags
        if update_data.recurrence_pattern is not None:
            task.recurrence_pattern = update_data.recurrence_pattern.dict()
            task.next_occurrence = self._calculate_next_occurrence(
                task.recurrence_pattern,
                task.due_date
            )

        # Increment version
        task.version += 1
        task.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(task)

        logger.info(f"Task updated: {task.id} by user {user.id}")

        # Publish task.updated event
        await self._publish_task_event("com.todo.task.updated", task, user.id, old_state=old_state)

        # Publish sync event
        await self._publish_sync_event("task_updated", task)

        return task

    async def delete_task(self, task_id: uuid.UUID, user: User) -> bool:
        """Soft delete task and publish deletion event"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user.id,
            Task.deleted_at == None
        ).first()

        if not task:
            return False

        # Soft delete
        task.deleted_at = datetime.utcnow()
        task.version += 1
        self.db.commit()

        logger.info(f"Task deleted: {task.id} by user {user.id}")

        # Publish task.deleted event
        await self._publish_task_event("com.todo.task.deleted", task, user.id)

        # Publish sync event
        await self._publish_sync_event("task_deleted", task)

        return True

    async def complete_task(self, task_id: uuid.UUID, user: User) -> Task:
        """Mark task as completed and publish completion event"""
        task = self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user.id,
            Task.deleted_at == None
        ).first()

        if not task:
            raise ValueError("Task not found")

        task.status = "completed"
        task.completed_at = datetime.utcnow()
        task.version += 1
        self.db.commit()
        self.db.refresh(task)

        logger.info(f"Task completed: {task.id} by user {user.id}")

        # Publish task.completed event
        await self._publish_task_event("com.todo.task.completed", task, user.id)

        # Publish sync event
        await self._publish_sync_event("task_completed", task)

        return task

    def get_task(self, task_id: uuid.UUID, user: User) -> Optional[Task]:
        """Get single task by ID"""
        return self.db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user.id,
            Task.deleted_at == None
        ).first()

    def list_tasks(
        self,
        user: User,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_before: Optional[datetime] = None,
        due_after: Optional[datetime] = None,
        sort: str = "created_at",
        order: str = "desc",
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Task], int]:
        """List tasks with filters, sort, and pagination"""
        query = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.deleted_at == None
        )

        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if tags:
            query = query.filter(Task.tags.overlap(tags))
        if due_before:
            query = query.filter(Task.due_date <= due_before)
        if due_after:
            query = query.filter(Task.due_date >= due_after)

        # Get total count
        total = query.count()

        # Apply sorting
        sort_column = getattr(Task, sort, Task.created_at)
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Apply pagination
        tasks = query.limit(limit).offset(offset).all()

        return tasks, total

    def search_tasks(self, user: User, search_query: str, limit: int = 50) -> List[Task]:
        """Full-text search on task title and description"""
        # PostgreSQL full-text search
        search_vector = func.to_tsvector('english', Task.title + ' ' + func.coalesce(Task.description, ''))
        search_query_ts = func.plainto_tsquery('english', search_query)

        tasks = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.deleted_at == None,
            search_vector.op('@@')(search_query_ts)
        ).limit(limit).all()

        return tasks

    async def _publish_task_event(
        self,
        event_type: str,
        task: Task,
        user_id: uuid.UUID,
        old_state: Optional[Dict[str, Any]] = None
    ) -> None:
        """Publish task event to Kafka via Dapr"""
        event_data = {
            "task_id": str(task.id),
            "user_id": str(user_id),
            "current_state": task.to_dict(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        if old_state:
            event_data["previous_state"] = old_state

        cloudevent = create_cloudevent(
            event_type=event_type,
            source="chat-api",
            data=event_data,
            subject=f"task/{task.id}"
        )

        await self.dapr.publish_event(
            pubsub_name=self.pubsub_name,
            topic=self.topic_task_events,
            data=cloudevent
        )

    async def _publish_sync_event(self, action: str, task: Task) -> None:
        """Publish real-time sync event to task-updates topic"""
        event_data = {
            "action": action,
            "task": task.to_dict(),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        cloudevent = create_cloudevent(
            event_type="com.todo.sync.task_changed",
            source="chat-api",
            data=event_data,
            subject=f"user/{task.user_id}"
        )

        await self.dapr.publish_event(
            pubsub_name=self.pubsub_name,
            topic=self.topic_task_updates,
            data=cloudevent
        )

    def _calculate_next_occurrence(
        self,
        pattern: Dict[str, Any],
        start_date: Optional[datetime]
    ) -> Optional[datetime]:
        """Calculate next occurrence based on recurrence pattern"""
        # Simplified implementation - production would use dateutil.rrule
        if not start_date:
            start_date = datetime.utcnow()

        frequency = pattern.get("frequency")
        interval = pattern.get("interval", 1)

        # Basic calculation (simplified)
        from datetime import timedelta

        if frequency == "daily":
            return start_date + timedelta(days=interval)
        elif frequency == "weekly":
            return start_date + timedelta(weeks=interval)
        elif frequency == "monthly":
            return start_date + timedelta(days=30 * interval)  # Approximate
        elif frequency == "yearly":
            return start_date + timedelta(days=365 * interval)  # Approximate

        return None
