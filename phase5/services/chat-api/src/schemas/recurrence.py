"""Recurrence pattern schema"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class RecurrencePattern(BaseModel):
    """Schema for recurring task patterns"""

    frequency: str = Field(..., description="Recurrence frequency: daily, weekly, monthly, yearly")
    interval: int = Field(default=1, ge=1, description="Interval between occurrences (e.g., every 2 weeks)")
    days_of_week: Optional[List[int]] = Field(None, description="Days of week (0=Monday, 6=Sunday) for weekly recurrence")
    day_of_month: Optional[int] = Field(None, ge=1, le=31, description="Day of month for monthly recurrence")
    end_date: Optional[datetime] = Field(None, description="End date for recurrence")
    occurrences_count: Optional[int] = Field(None, ge=1, description="Maximum number of occurrences")

    class Config:
        json_schema_extra = {
            "example": {
                "frequency": "weekly",
                "interval": 1,
                "days_of_week": [0, 2, 4],  # Monday, Wednesday, Friday
                "end_date": "2026-12-31T23:59:59Z"
            }
        }
