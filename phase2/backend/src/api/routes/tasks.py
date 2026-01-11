"""
Task API routes for CRUD operations.

All endpoints require JWT authentication and are scoped to authenticated user.
All task queries are filtered by user_id for security.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlmodel import Session
from typing import Optional, List

from src.db.database import get_session
from src.services.task_service import TaskService
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead

router = APIRouter(prefix="/api/users", tags=["tasks"])


@router.post(
    "/{user_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    T018: Create a new task for the authenticated user.

    Required:
    - user_id in URL (verified against JWT)
    - title in request body

    Optional:
    - description in request body

    Returns:
        201 Created with task object

    Raises:
        400: Validation error (empty title, title too long)
        401: Missing or invalid JWT
        403: user_id mismatch with JWT
    """
    # Verify user_id matches authenticated user (middleware already checks this, but be explicit)
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Create task using service
        task = TaskService.create_task(session, user_id, task_data)

        return {
            "success": True,
            "data": TaskRead.from_orm(task),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task",
        )


@router.get(
    "/{user_id}/tasks",
    response_model=dict,
)
async def list_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status: incomplete or complete"),
    request: Request = None,
    session: Session = Depends(get_session),
):
    """
    T019: List all tasks for the authenticated user.

    Query Parameters:
    - status (optional): Filter by "incomplete" or "complete"

    Returns:
        200 OK with array of task objects

    Raises:
        401: Missing or invalid JWT
        403: user_id mismatch with JWT
    """
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Get tasks using service (automatically filters by user_id)
        tasks = TaskService.get_user_tasks(session, user_id, status)

        return {
            "success": True,
            "data": [TaskRead.from_orm(task) for task in tasks],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tasks",
        )


@router.get(
    "/{user_id}/tasks/{id}",
    response_model=dict,
)
async def get_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    T020: Get a single task by ID.

    Returns:
        200 OK with task object

    Raises:
        401: Missing or invalid JWT
        403: user_id mismatch with JWT (or task belongs to different user)
        404: Task not found
    """
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Get task using service (verifies ownership)
        task = TaskService.get_task(session, id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return {
            "success": True,
            "data": TaskRead.from_orm(task),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving task",
        )


@router.put(
    "/{user_id}/tasks/{id}",
    response_model=dict,
)
async def update_task(
    user_id: str,
    id: int,
    task_data: TaskUpdate,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    T021: Update a task.

    Can update: title, description
    Cannot update: status (use PATCH endpoint)

    Returns:
        200 OK with updated task object

    Raises:
        400: Validation error
        401: Missing or invalid JWT
        403: user_id mismatch with JWT (or task belongs to different user)
        404: Task not found
    """
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Update task using service (verifies ownership)
        task = TaskService.update_task(session, id, user_id, task_data)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return {
            "success": True,
            "data": TaskRead.from_orm(task),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task",
        )


@router.delete(
    "/{user_id}/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    T022: Delete a task.

    Returns:
        204 No Content (empty response)

    Raises:
        401: Missing or invalid JWT
        403: user_id mismatch with JWT (or task belongs to different user)
        404: Task not found
    """
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Delete task using service (verifies ownership)
        success = TaskService.delete_task(session, id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting task",
        )


@router.patch(
    "/{user_id}/tasks/{id}/complete",
    response_model=dict,
)
async def toggle_task(
    user_id: str,
    id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    """
    T023: Toggle task completion status.

    Flips status between "incomplete" and "complete".

    Returns:
        200 OK with updated task object

    Raises:
        401: Missing or invalid JWT
        403: user_id mismatch with JWT (or task belongs to different user)
        404: Task not found
    """
    # Verify user_id matches authenticated user
    if user_id != request.state.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch",
        )

    try:
        # Toggle task using service (verifies ownership)
        task = TaskService.toggle_task_status(session, id, user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return {
            "success": True,
            "data": TaskRead.from_orm(task),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error toggling task status",
        )
