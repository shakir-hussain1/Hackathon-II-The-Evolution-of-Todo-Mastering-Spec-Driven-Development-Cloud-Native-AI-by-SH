"""
Message model for conversation history.
"""
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum as PyEnum
import uuid


class MessageRole(str, PyEnum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message entity for chat turns in conversations."""

    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique message identifier"
    )
    conversation_id: str = Field(
        foreign_key="conversations.id",
        nullable=False,
        description="Parent conversation (FK to conversations table)",
        index=True
    )
    role: MessageRole = Field(
        nullable=False,
        description="Message sender role (user or assistant)"
    )
    content: str = Field(
        nullable=False,
        description="Message content (user input or agent response)"
    )
    tool_calls: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Audit trail of MCP tool invocations (JSONB)"
    )
    sequence_number: int = Field(
        nullable=False,
        description="Message order within conversation"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message timestamp",
        index=True
    )

    # Relationship (defined but not loaded by default)
    # conversation: "Conversation" = Relationship(back_populates="messages")

    class Config:
        """SQLModel configuration."""
        arbitrary_types_allowed = True
