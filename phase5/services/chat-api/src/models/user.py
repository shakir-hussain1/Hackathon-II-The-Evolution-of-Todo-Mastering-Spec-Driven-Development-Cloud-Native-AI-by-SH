"""User model for authentication and profile"""

import uuid
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User entity with authentication and notification preferences"""

    __tablename__ = "users"
    __table_args__ = {"schema": "chat_api"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    notification_preferences = Column(
        JSON,
        default={"email": True, "push": False},
        nullable=False
    )
    timezone = Column(String(50), default="UTC", nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)"""
        return {
            "id": str(self.id),
            "email": self.email,
            "full_name": self.full_name,
            "notification_preferences": self.notification_preferences,
            "timezone": self.timezone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
