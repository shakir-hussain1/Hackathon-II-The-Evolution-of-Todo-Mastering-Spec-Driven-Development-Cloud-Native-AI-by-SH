"""
Task model for todo items.
"""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum
import uuid


class TaskStatus(str, PyEnum):
    """Task status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"


class Task(SQLModel, table=True):
    """Task entity for todo items."""

    __tablename__ = "tasks"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique task identifier"
    )
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        description="Task owner (FK to users table)",
        index=True
    )
    title: str = Field(
        nullable=False,
        max_length=500,
        description="Task title/description"
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Task status (pending or completed)",
        index=True
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp",
        index=True
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last task update timestamp"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Task completion timestamp"
    )

    # Relationship (defined but not loaded by default)
    # user: "User" = Relationship(back_populates="tasks")
