"""
MCP tools for task operations.
All tools are stateless and persist changes to database.
"""
from typing import Dict, Any, List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from datetime import datetime

from .server import get_mcp_server
from ..db import operations
from ..models import TaskStatus

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Note: MCP SDK decorators would normally be used here
# For this implementation, we'll create callable functions that match MCP tool signatures


async def add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = ""
) -> Dict[str, Any]:
    """
    Add a new task to the user's todo list.

    Use this tool when user wants to create a new task, using phrases like:
    - "Add [task] to my list"
    - "Create a task for [task]"
    - "Remind me to [task]"
    - "I need to [task]"

    Args:
        session: Database session
        user_id: User identifier (for data isolation)
        title: Task title/description
        description: Optional detailed description

    Returns:
        dict: Success status, created task object, and confirmation message
    """
    logger.info(f"[add_task] user_id={user_id}, title='{title}', description='{description[:50]}...'")
    try:
        task = await operations.create_task(session, user_id, title, description)
        logger.info(f"[add_task] SUCCESS: task_id={task.id}, user_id={user_id}")

        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            },
            "message": f"Added task: {title}",
            "error": None
        }
    except Exception as e:
        logger.error(f"[add_task] FAILED: user_id={user_id}, error={str(e)}")
        return {
            "success": False,
            "task": None,
            "message": f"Failed to add task: {str(e)}",
            "error": str(e)
        }


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve all tasks for a user, optionally filtered by status.

    Use this tool when user wants to view their tasks, using phrases like:
    - "Show me my tasks"
    - "What's on my todo list?"
    - "List all my tasks"
    - "Show pending tasks"
    - "Show completed tasks"

    Args:
        session: Database session
        user_id: User identifier (for data isolation)
        status: Optional status filter ("pending", "completed", or None for all)

    Returns:
        dict: Success status, task array, and message
    """
    logger.info(f"[list_tasks] user_id={user_id}, status={status}")
    try:
        # Convert status string to enum if provided
        status_enum = None
        if status:
            status_enum = TaskStatus(status.lower())

        tasks = await operations.get_tasks(session, user_id, status_enum)
        logger.info(f"[list_tasks] SUCCESS: user_id={user_id}, count={len(tasks)}")

        return {
            "success": True,
            "data": [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                }
                for task in tasks
            ],
            "message": f"Found {len(tasks)} task(s)",
            "error": None
        }
    except Exception as e:
        logger.error(f"[list_tasks] FAILED: user_id={user_id}, error={str(e)}")
        return {
            "success": False,
            "data": [],
            "message": f"Failed to list tasks: {str(e)}",
            "error": str(e)
        }


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing task's title and/or description.

    Use this tool when user wants to modify a task, using phrases like:
    - "Change [task] to [new description]"
    - "Update [task] with [details]"
    - "Edit [task] to say [new text]"

    Args:
        session: Database session
        user_id: User identifier (for data isolation)
        task_id: ID of task to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        dict: Success status, updated task object, and message
    """
    logger.info(f"[update_task] user_id={user_id}, task_id={task_id}, title={title}, description={description[:50] if description else None}...")
    try:
        task = await operations.update_task(session, user_id, task_id, title, description)

        if not task:
            logger.warning(f"[update_task] NOT FOUND: user_id={user_id}, task_id={task_id}")
            return {
                "success": False,
                "task": None,
                "message": "Task not found",
                "error": "Task not found or you don't have permission to update it"
            }

        logger.info(f"[update_task] SUCCESS: user_id={user_id}, task_id={task_id}")
        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            },
            "message": f"Updated task: {task.title}",
            "error": None
        }
    except Exception as e:
        logger.error(f"[update_task] FAILED: user_id={user_id}, task_id={task_id}, error={str(e)}")
        return {
            "success": False,
            "task": None,
            "message": f"Failed to update task: {str(e)}",
            "error": str(e)
        }


async def complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Use this tool when user wants to complete a task, using phrases like:
    - "Mark [task] as complete"
    - "Complete [task]"
    - "[task] is done"
    - "Finish [task]"

    Args:
        session: Database session
        user_id: User identifier (for data isolation)
        task_id: ID of task to complete

    Returns:
        dict: Success status, completed task object, and message
    """
    logger.info(f"[complete_task] user_id={user_id}, task_id={task_id}")
    try:
        task = await operations.complete_task(session, user_id, task_id)

        if not task:
            logger.warning(f"[complete_task] NOT FOUND: user_id={user_id}, task_id={task_id}")
            return {
                "success": False,
                "task": None,
                "message": "Task not found",
                "error": "Task not found or you don't have permission to complete it"
            }

        logger.info(f"[complete_task] SUCCESS: user_id={user_id}, task_id={task_id}")
        return {
            "success": True,
            "task": {
                "id": task.id,
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            },
            "message": f"Completed task: {task.title}",
            "error": None
        }
    except Exception as e:
        logger.error(f"[complete_task] FAILED: user_id={user_id}, task_id={task_id}, error={str(e)}")
        return {
            "success": False,
            "task": None,
            "message": f"Failed to complete task: {str(e)}",
            "error": str(e)
        }


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Delete a task from the user's todo list.

    Use this tool when user wants to remove a task, using phrases like:
    - "Delete [task]"
    - "Remove [task]"
    - "Get rid of [task]"

    Args:
        session: Database session
        user_id: User identifier (for data isolation)
        task_id: ID of task to delete

    Returns:
        dict: Success status and message
    """
    logger.info(f"[delete_task] user_id={user_id}, task_id={task_id}")
    try:
        success = await operations.delete_task(session, user_id, task_id)

        if not success:
            logger.warning(f"[delete_task] NOT FOUND: user_id={user_id}, task_id={task_id}")
            return {
                "success": False,
                "message": "Task not found",
                "error": "Task not found or you don't have permission to delete it"
            }

        logger.info(f"[delete_task] SUCCESS: user_id={user_id}, task_id={task_id}")
        return {
            "success": True,
            "message": "Task deleted successfully",
            "error": None
        }
    except Exception as e:
        logger.error(f"[delete_task] FAILED: user_id={user_id}, task_id={task_id}, error={str(e)}")
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}",
            "error": str(e)
        }


# Tool registry for easy access by agent
MCP_TOOLS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "update_task": update_task,
    "complete_task": complete_task,
    "delete_task": delete_task,
}


def register_tools():
    """Register all MCP tools with the server."""
    # In a real MCP SDK implementation, this would use decorators
    # For now, we're using a simple dictionary-based approach
    return MCP_TOOLS
