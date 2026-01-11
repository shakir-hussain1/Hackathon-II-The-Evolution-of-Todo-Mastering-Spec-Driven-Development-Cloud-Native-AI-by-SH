"""
Pydantic schemas for User requests and responses.

Used for request validation and response serialization in API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base User schema with common fields."""

    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for user signup request."""

    password: str = Field(..., min_length=8, description="User's password (min 8 chars)")


class UserLogin(UserBase):
    """Schema for user login request."""

    password: str = Field(..., description="User's password")


class UserRead(UserBase):
    """Schema for user response (read-only fields)."""

    id: str = Field(..., description="Unique user identifier (UUID)")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
