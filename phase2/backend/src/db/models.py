"""
SQLModel table definitions for User and Task entities.

Defines the database schema using SQLModel which provides both
ORM functionality and Pydantic validation.
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class User(SQLModel, table=True):
    """
    User table (managed by Better Auth).

    Represents a user account in the system.
    """

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique user identifier (UUID)",
    )
    email: str = Field(
        unique=True,
        index=True,
        description="User's email address (must be unique)",
    )
    password_hash: str = Field(
        description="Hashed password (managed by Better Auth)",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Account creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    # Relationship
    tasks: List["Task"] = Relationship(
        back_populates="user",
        cascade_delete=True,
    )


class Task(SQLModel, table=True):
    """
    Task table for user's todo items.

    Represents a single task owned by a user.
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier (auto-increment)",
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of the task (foreign key to users.id)",
    )
    title: str = Field(
        max_length=255,
        description="Task title (required, max 255 characters)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=10000,
        description="Task description (optional, max 10000 characters)",
    )
    status: str = Field(
        default="incomplete",
        description='Task status: "incomplete" or "complete"',
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Task creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    # Relationship
    user: Optional[User] = Relationship(
        back_populates="tasks",
    )
