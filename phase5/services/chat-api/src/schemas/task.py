"""Task schemas for request/response validation"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from .recurrence import RecurrencePattern


class TaskCreate(BaseModel):
    """Schema for creating a new task"""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: str = Field(default="medium", description="Priority: high, medium, low")
    due_date: Optional[datetime] = Field(None, description="Due date with timezone")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    recurrence_pattern: Optional[RecurrencePattern] = Field(None, description="Recurrence pattern for recurring tasks")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Weekly team standup",
                "description": "Discuss project progress and blockers",
                "priority": "high",
                "due_date": "2026-02-10T09:00:00Z",
                "tags": ["meeting", "team"],
                "recurrence_pattern": {
                    "frequency": "weekly",
                    "interval": 1,
                    "days_of_week": [0]  # Every Monday
                }
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, description="Status: pending, completed, archived")
    priority: Optional[str] = Field(None, description="Priority: high, medium, low")
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    recurrence_pattern: Optional[RecurrencePattern] = None
    version: int = Field(..., description="Current version for optimistic locking")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "version": 1
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response"""

    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    tags: List[str]
    recurrence_pattern: Optional[dict]
    next_occurrence: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    version: int

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for paginated task list response"""

    tasks: List[TaskResponse]
    total: int
    limit: int
    offset: int
