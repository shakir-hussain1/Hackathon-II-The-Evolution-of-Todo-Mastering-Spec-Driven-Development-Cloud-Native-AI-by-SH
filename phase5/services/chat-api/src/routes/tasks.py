"""Task routes for CRUD operations and search"""

from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from ..database import get_db
from ..services.task_service import TaskService
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from ..middleware.auth import get_current_user
from ..models.user import User
from ..utils.dapr_client import get_dapr_client, DaprClientWrapper

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: pending, completed, archived"),
    priority: Optional[str] = Query(None, description="Filter by priority: high, medium, low"),
    tags: Optional[str] = Query(None, description="Comma-separated list of tags to filter by"),
    due_before: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    due_after: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    sort: str = Query("created_desc", description="Sort field: created_asc, created_desc, due_asc, due_desc, priority_asc, priority_desc, title_asc, title_desc"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    List all tasks for the authenticated user with filtering and pagination.

    **Filters:**
    - status: Filter by task status
    - priority: Filter by priority level
    - tags: Filter by tags (comma-separated)
    - due_before/due_after: Filter by due date range

    **Sorting:**
    - created_asc/created_desc: Sort by creation date
    - due_asc/due_desc: Sort by due date
    - priority_asc/priority_desc: Sort by priority
    - title_asc/title_desc: Sort by title alphabetically

    **Pagination:**
    - limit: Number of results per page (max 100)
    - offset: Number of results to skip
    """
    task_service = TaskService(db, dapr_client)

    # Parse sort parameter
    sort_parts = sort.split("_")
    sort_field = "_".join(sort_parts[:-1]) if len(sort_parts) > 1 else "created_at"
    sort_order = sort_parts[-1] if sort_parts[-1] in ["asc", "desc"] else "desc"

    # Parse tags if provided
    tags_list = tags.split(",") if tags else None

    # Fetch tasks
    tasks, total = task_service.list_tasks(
        user=current_user,
        status=status_filter,
        priority=priority,
        tags=tags_list,
        due_before=due_before,
        due_after=due_after,
        sort=sort_field,
        order=sort_order,
        limit=limit,
        offset=offset
    )

    # Convert to response models
    task_responses = [TaskResponse(**task.to_dict()) for task in tasks]

    return TaskListResponse(
        tasks=task_responses,
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Create a new task.

    **Required:**
    - title: Task title (max 200 characters)

    **Optional:**
    - description: Detailed description
    - priority: high, medium (default), or low
    - due_date: ISO 8601 datetime with timezone
    - tags: Array of tag strings
    - recurrence_pattern: Recurrence configuration for recurring tasks
    """
    task_service = TaskService(db, dapr_client)

    try:
        task = await task_service.create_task(current_user, task_data)
        return TaskResponse(**task.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/search", response_model=TaskListResponse)
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search query for full-text search"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Full-text search across task titles and descriptions.

    Uses PostgreSQL full-text search (GIN index) for fast searching.

    **Parameters:**
    - q: Search query (searches in title and description)
    - limit: Maximum number of results (max 100)
    """
    task_service = TaskService(db, dapr_client)

    tasks = task_service.search_tasks(current_user, q, limit)

    task_responses = [TaskResponse(**task.to_dict()) for task in tasks]

    return TaskListResponse(
        tasks=task_responses,
        total=len(task_responses),
        limit=limit,
        offset=0
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Get a single task by ID.

    Returns 404 if task doesn't exist or doesn't belong to the current user.
    """
    task_service = TaskService(db, dapr_client)

    task = task_service.get_task(task_id, current_user)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    return TaskResponse(**task.to_dict())


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    update_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Update a task (partial update).

    **Optimistic Locking:**
    - Must provide current version number
    - Returns 409 Conflict if version doesn't match (task was modified)

    **Updatable Fields:**
    - title, description, status, priority, due_date, tags, recurrence_pattern

    **Status Values:**
    - pending, completed, archived
    """
    task_service = TaskService(db, dapr_client)

    try:
        task = await task_service.update_task(task_id, current_user, update_data)
        return TaskResponse(**task.to_dict())
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "version conflict" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "VersionConflict",
                    "message": "Task was modified by another process. Please refresh and try again.",
                    "details": error_msg
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Soft delete a task.

    The task is marked as deleted but remains in the database for audit purposes.
    Returns 404 if task doesn't exist or doesn't belong to the current user.
    """
    task_service = TaskService(db, dapr_client)

    success = await task_service.delete_task(task_id, current_user)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Mark a task as completed.

    This is a convenience endpoint that sets status to 'completed' and records completion timestamp.
    """
    task_service = TaskService(db, dapr_client)

    try:
        task = await task_service.complete_task(task_id, current_user)
        return TaskResponse(**task.to_dict())
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
