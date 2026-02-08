"""Chat schemas for AI assistant interactions"""

from typing import Optional, List, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Schema for chat message request"""

    message: str = Field(..., min_length=1, description="User message to AI assistant")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for context")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Create a task to review the project proposal by Friday",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class ChatAction(BaseModel):
    """Schema for action taken by AI assistant"""

    type: str = Field(..., description="Action type: task_created, task_updated, task_deleted, search_performed")
    task_id: Optional[str] = Field(None, description="Task ID if action involves a task")
    details: dict = Field(default_factory=dict, description="Additional action details")

    class Config:
        json_schema_extra = {
            "example": {
                "type": "task_created",
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "details": {
                    "title": "Review project proposal",
                    "priority": "high",
                    "due_date": "2026-02-14T17:00:00Z"
                }
            }
        }


class ChatResponse(BaseModel):
    """Schema for chat response from AI assistant"""

    response: str = Field(..., description="AI assistant's text response")
    actions: List[ChatAction] = Field(default_factory=list, description="Actions performed by assistant")
    conversation_id: str = Field(..., description="Conversation ID for context continuity")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "I've created a task to review the project proposal by Friday. It's marked as high priority and due on February 14th at 5 PM.",
                "actions": [
                    {
                        "type": "task_created",
                        "task_id": "550e8400-e29b-41d4-a716-446655440000",
                        "details": {
                            "title": "Review project proposal",
                            "priority": "high",
                            "due_date": "2026-02-14T17:00:00Z"
                        }
                    }
                ],
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
