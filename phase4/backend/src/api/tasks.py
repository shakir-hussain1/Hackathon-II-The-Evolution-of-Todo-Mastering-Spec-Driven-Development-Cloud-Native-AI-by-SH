"""
Direct CRUD API endpoints for task management.
Provides REST endpoints for dashboard to fetch, update, and delete tasks.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

from ..db.connection import get_session
from ..db import operations
from ..models import TaskStatus
from .middleware import verify_jwt, verify_user_id_match, rate_limit_middleware


router = APIRouter(prefix="/api", tags=["tasks"])


class TaskResponse(BaseModel):
    """Task data transfer object."""
    id: str
    title: str
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str
    completed_at: Optional[str]


class UpdateTaskRequest(BaseModel):
    """Request to update task fields."""
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(pending|completed)$")


def task_to_response(task) -> TaskResponse:
    """Convert Task model to response format with proper UTC timestamps."""
    # Ensure ISO format includes 'Z' for UTC timezone
    # datetime.utcnow() creates naive datetimes, so we append 'Z' to indicate UTC
    created_at = task.created_at.isoformat() + 'Z' if not task.created_at.tzinfo else task.created_at.isoformat()
    updated_at = task.updated_at.isoformat() + 'Z' if not task.updated_at.tzinfo else task.updated_at.isoformat()
    completed_at = None
    if task.completed_at:
        completed_at = task.completed_at.isoformat() + 'Z' if not task.completed_at.tzinfo else task.completed_at.isoformat()

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.status.value,
        created_at=created_at,
        updated_at=updated_at,
        completed_at=completed_at
    )


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: str,
    status: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
    token_payload: Dict[str, str] = Depends(verify_jwt),
    _rate_limit: None = Depends(rate_limit_middleware)
):
    """
    Get all tasks for user, optionally filtered by status.

    Query Parameters:
    - status: Filter by 'pending' or 'completed'

    Security:
    - JWT authentication required
    - user_id must match token
    """
    try:
        # Verify user_id matches authenticated user
        verify_user_id_match(user_id, token_payload)

        # Parse status filter
        status_filter = None
        if status:
            if status not in ["pending", "completed"]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid status. Must be 'pending' or 'completed'"
                )
            status_filter = TaskStatus(status)

        # Fetch tasks
        tasks = await operations.get_tasks(session, user_id, status_filter)

        return [task_to_response(task) for task in tasks]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


@router.patch("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: str,
    request: UpdateTaskRequest,
    session: AsyncSession = Depends(get_session),
    token_payload: Dict[str, str] = Depends(verify_jwt),
    _rate_limit: None = Depends(rate_limit_middleware)
):
    """
    Update task title, description, or status.

    Supports partial updates - only send fields you want to change.

    Security:
    - JWT authentication required
    - user_id must match token
    - Can only update own tasks
    """
    try:
        # Verify user_id matches authenticated user
        verify_user_id_match(user_id, token_payload)

        # Get existing task to verify ownership
        task = await operations.get_task_by_id(session, user_id, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Handle status change
        if request.status:
            if request.status == "completed" and task.status != TaskStatus.COMPLETED:
                # Mark as completed
                task = await operations.complete_task(session, user_id, task_id)
            elif request.status == "pending" and task.status == TaskStatus.COMPLETED:
                # Reopen task
                task.status = TaskStatus.PENDING
                task.completed_at = None
                task.updated_at = datetime.utcnow()
                session.add(task)
                await session.commit()
                await session.refresh(task)

        # Update title and/or description
        if request.title is not None or request.description is not None:
            task = await operations.update_task(
                session,
                user_id,
                task_id,
                title=request.title,
                description=request.description
            )

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task_to_response(task)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update task: {str(e)}"
        )


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    session: AsyncSession = Depends(get_session),
    token_payload: Dict[str, str] = Depends(verify_jwt),
    _rate_limit: None = Depends(rate_limit_middleware)
):
    """
    Delete a task.

    Security:
    - JWT authentication required
    - user_id must match token
    - Can only delete own tasks
    """
    try:
        # Verify user_id matches authenticated user
        verify_user_id_match(user_id, token_payload)

        # Delete task
        deleted = await operations.delete_task(session, user_id, task_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"success": True, "message": "Task deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete task: {str(e)}"
        )
