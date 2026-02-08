"""Task model with advanced features (priority, due date, tags, recurrence)"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, ARRAY, JSON, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Task(Base, TimestampMixin):
    """Task entity with advanced task management features"""

    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'completed', 'archived')", name="check_status"),
        CheckConstraint("priority IN ('high', 'medium', 'low')", name="check_priority"),
        {"schema": "chat_api"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("chat_api.users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending", nullable=False, index=True)
    priority = Column(String(10), default="medium", nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    tags = Column(ARRAY(Text), default=[], nullable=False)
    recurrence_pattern = Column(JSON, nullable=True)
    next_occurrence = Column(DateTime(timezone=True), nullable=True, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task {self.title} ({self.status})>"

    def to_dict(self, include_user: bool = False) -> dict:
        """Convert task to dictionary"""
        data = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags or [],
            "recurrence_pattern": self.recurrence_pattern,
            "next_occurrence": self.next_occurrence.isoformat() if self.next_occurrence else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "version": self.version
        }

        if include_user and self.user:
            data["user"] = self.user.to_dict()

        return data

    def is_recurring(self) -> bool:
        """Check if task has recurrence pattern"""
        return self.recurrence_pattern is not None

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.status != "pending":
            return False
        return datetime.utcnow() > self.due_date.replace(tzinfo=None)
