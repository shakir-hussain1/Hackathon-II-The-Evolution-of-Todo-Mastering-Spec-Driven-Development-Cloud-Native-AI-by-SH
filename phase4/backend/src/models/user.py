"""
User model for authentication and ownership.
"""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class User(SQLModel, table=True):
    """User entity for authentication and task ownership."""

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique user identifier"
    )
    email: str = Field(
        unique=True,
        nullable=False,
        max_length=255,
        description="User's email address for authentication",
        index=True
    )
    password_hash: str = Field(
        nullable=False,
        max_length=255,
        description="Bcrypt hashed password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last account update timestamp"
    )

    # Relationships (defined but not loaded by default for performance)
    # conversations: List["Conversation"] = Relationship(back_populates="user")
    # tasks: List["Task"] = Relationship(back_populates="user")
