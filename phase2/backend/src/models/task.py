"""
Task model for Phase II.

Re-exports Task from database models for convenience.
"""

from src.db.models import Task

__all__ = ["Task"]
