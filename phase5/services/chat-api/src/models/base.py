"""Base SQLAlchemy models with common fields"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TimestampMixin:
    """Mixin for timestamp fields"""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1, nullable=False)

    @property
    def is_deleted(self) -> bool:
        """Check if entity is soft deleted"""
        return self.deleted_at is not None
