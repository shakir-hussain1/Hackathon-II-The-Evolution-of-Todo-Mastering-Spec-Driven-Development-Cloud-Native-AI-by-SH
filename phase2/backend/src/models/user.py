"""
User model for Phase II.

Re-exports User from database models for convenience.
"""

from src.db.models import User

__all__ = ["User"]
