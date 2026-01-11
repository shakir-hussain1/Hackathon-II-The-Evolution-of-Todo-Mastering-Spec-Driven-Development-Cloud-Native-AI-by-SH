"""
Pydantic schemas for Task requests and responses.

Used for request validation and response serialization in API endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title (required, max 255 chars)",
    )
    description: Optional[str] = Field(
        None,
        max_length=10000,
        description="Task description (optional, max 10000 chars)",
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_trimmed(cls, v: Optional[str]) -> Optional[str]:
        """Trim whitespace from description."""
        return v.strip() if v else v


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title (optional, max 255 chars)",
    )
    description: Optional[str] = Field(
        None,
        max_length=10000,
        description="Updated description (optional, max 10000 chars)",
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("description")
    @classmethod
    def description_trimmed(cls, v: Optional[str]) -> Optional[str]:
        """Trim whitespace from description."""
        return v.strip() if v else v


class TaskRead(BaseModel):
    """Schema for task response (read-only fields)."""

    id: int = Field(..., description="Unique task identifier")
    user_id: str = Field(..., description="Task owner's user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field(
        ...,
        description='Task status: "incomplete" or "complete"',
    )
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
