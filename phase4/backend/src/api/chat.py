"""
Chat API endpoint for natural language task management.
Handles message exchange with AI agent using MCP tools.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession

from ..db.connection import get_session
from ..db import operations
from ..agent.runner import run_agent
from .middleware import verify_jwt, verify_user_id_match, rate_limit_middleware


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """User message to agent."""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue")


class ChatResponse(BaseModel):
    """Agent response with conversation metadata."""
    response: str = Field(..., description="Agent's response text")
    conversation_id: str = Field(..., description="Conversation ID")
    message_id: str = Field(..., description="Assistant message ID")
    tool_calls: Optional[Dict[str, Any]] = Field(None, description="Tool calls made (audit trail)")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    token_payload: Dict[str, str] = Depends(verify_jwt),
    _rate_limit: None = Depends(rate_limit_middleware)
):
    """
    Send message to AI agent and get response.

    Flow:
    1. Verify user_id matches JWT token
    2. Get or create conversation
    3. Load conversation history
    4. Save user message
    5. Run agent with MCP tools
    6. Save assistant response
    7. Return response

    Security:
    - JWT authentication required
    - user_id must match token
    - All operations scoped to user_id
    """
    try:
        # Verify user_id matches authenticated user
        verify_user_id_match(user_id, token_payload)

        # Get or create conversation
        conversation = await operations.get_or_create_conversation(
            session,
            user_id,
            request.conversation_id
        )

        # Load conversation history for context
        history_messages = await operations.load_conversation_history(
            session,
            conversation.id
        )

        # Convert history to format expected by agent
        conversation_history = [
            {
                "role": msg.role.value,
                "content": msg.content
            }
            for msg in history_messages
        ]

        # Save user message
        user_msg = await operations.save_user_message(
            session,
            conversation.id,
            request.message
        )

        # Run agent with conversation context
        agent_response = await run_agent(
            session=session,
            user_id=user_id,
            user_message=request.message,
            conversation_history=conversation_history
        )

        # Save assistant response with tool calls audit
        assistant_msg = await operations.save_assistant_message(
            session,
            conversation.id,
            agent_response["content"],
            agent_response.get("tool_calls")
        )

        # Return response
        return ChatResponse(
            response=agent_response["content"],
            conversation_id=conversation.id,
            message_id=assistant_msg.id,
            tool_calls=agent_response.get("tool_calls")
        )

    except HTTPException:
        # Re-raise HTTP exceptions (auth errors)
        raise
    except Exception as e:
        # Log error and return user-friendly message
        error_detail = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {error_detail}"
        )


@router.get("/{user_id}/conversations/{conversation_id}/history")
async def get_conversation_history(
    user_id: str,
    conversation_id: str,
    session: AsyncSession = Depends(get_session),
    token_payload: Dict[str, str] = Depends(verify_jwt)
):
    """
    Retrieve conversation history.

    Useful for:
    - Loading conversation on frontend mount
    - Displaying message history
    - Debugging/auditing
    """
    try:
        # Verify user_id matches authenticated user
        verify_user_id_match(user_id, token_payload)

        # Verify conversation belongs to user
        conversation = await operations.get_or_create_conversation(
            session,
            user_id,
            conversation_id
        )

        if conversation.id != conversation_id:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or access denied"
            )

        # Load messages
        messages = await operations.load_conversation_history(
            session,
            conversation_id
        )

        # Format response
        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role.value,
                    "content": msg.content,
                    "tool_calls": msg.tool_calls,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load conversation history: {str(e)}"
        )
