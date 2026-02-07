"""
Conversation model for chat sessions.
"""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class Conversation(SQLModel, table=True):
    """Conversation entity for chat threads."""

    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique conversation identifier"
    )
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        description="Owner of the conversation (FK to users table)",
        index=True
    )
    title: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional conversation title"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation start timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last message timestamp",
        index=True  # For sorting by recent activity
    )

    # Relationship (defined but not loaded by default)
    # user: "User" = Relationship(back_populates="conversations")
    # messages: List["Message"] = Relationship(back_populates="conversation")
