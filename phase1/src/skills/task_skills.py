"""Task-related skills for task management operations."""

from src.skills.base_skill import Skill, SkillConfig
from src.agents.base_agent import AgentContext
from src.models.task import TaskStatus
from datetime import datetime


class CreateTaskSkill(Skill):
    """Skill for creating new tasks."""

    def __init__(self):
        config = SkillConfig(
            name="create_task",
            description="Creates a new task with title and optional description",
            tags=["task", "creation", "crud"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate that task_manager is available in context."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """Create a new task from context."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            # Parse title and description from user_input
            parts = context.user_input.split("|", 1)
            title = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""

            if not title:
                return {
                    "success": False,
                    "message": "Error: Title is required",
                    "data": None,
                }

            task = context.task_manager.add_task(title, description)
            self.execution_count += 1
            self.last_executed = datetime.now()

            return {
                "success": True,
                "message": f"Task {task.id} created successfully",
                "data": {
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                },
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}",
                "data": None,
            }


class ListTasksSkill(Skill):
    """Skill for listing all tasks."""

    def __init__(self):
        config = SkillConfig(
            name="list_tasks",
            description="Lists all tasks with optional filtering by status",
            tags=["task", "retrieval", "read"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate task_manager availability."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """List all tasks, optionally filtered."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            tasks = context.task_manager.list_tasks()

            # Check for filter in metadata
            status_filter = context.metadata.get("status_filter")
            if status_filter:
                tasks = [t for t in tasks if t.status.value == status_filter]

            self.execution_count += 1
            self.last_executed = datetime.now()

            tasks_data = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                }
                for task in tasks
            ]

            return {
                "success": True,
                "message": f"Retrieved {len(tasks)} tasks",
                "data": {"tasks": tasks_data},
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to list tasks: {str(e)}",
                "data": None,
            }


class DeleteTaskSkill(Skill):
    """Skill for deleting tasks."""

    def __init__(self):
        config = SkillConfig(
            name="delete_task",
            description="Deletes a task by ID",
            tags=["task", "deletion", "crud"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate task_manager availability."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """Delete a task by ID."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            # Parse task_id from user_input
            task_id = int(context.user_input.strip())

            success = context.task_manager.delete_task(task_id)

            if success:
                self.execution_count += 1
                self.last_executed = datetime.now()
                return {
                    "success": True,
                    "message": f"Task {task_id} deleted successfully",
                    "data": {"task_id": task_id},
                }
            else:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found",
                    "data": None,
                }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid task ID format",
                "data": None,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}",
                "data": None,
            }


class ToggleTaskStatusSkill(Skill):
    """Skill for toggling task completion status."""

    def __init__(self):
        config = SkillConfig(
            name="toggle_task_status",
            description="Toggles task between complete and incomplete",
            tags=["task", "status", "update"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate task_manager availability."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """Toggle task status."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            task_id = int(context.user_input.strip())
            success = context.task_manager.toggle_task_status(task_id)

            if success:
                task = context.task_manager.get_task(task_id)
                self.execution_count += 1
                self.last_executed = datetime.now()
                return {
                    "success": True,
                    "message": f"Task {task_id} status toggled to {task.status.value}",
                    "data": {"task_id": task_id, "new_status": task.status.value},
                }
            else:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found",
                    "data": None,
                }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid task ID format",
                "data": None,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to toggle status: {str(e)}",
                "data": None,
            }


class UpdateTaskSkill(Skill):
    """Skill for updating task title and/or description."""

    def __init__(self):
        config = SkillConfig(
            name="update_task",
            description="Updates task title and/or description",
            tags=["task", "update", "crud"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate task_manager availability."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """Update a task."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            # Parse input format: task_id|title|description
            parts = context.user_input.split("|")
            if len(parts) < 2:
                return {
                    "success": False,
                    "message": "Invalid format. Use: task_id|title|description",
                    "data": None,
                }

            task_id = int(parts[0].strip())
            title = parts[1].strip() if parts[1].strip() else None
            description = parts[2].strip() if len(parts) > 2 and parts[2].strip() else None

            success = context.task_manager.update_task(task_id, title, description)

            if success:
                task = context.task_manager.get_task(task_id)
                self.execution_count += 1
                self.last_executed = datetime.now()
                return {
                    "success": True,
                    "message": f"Task {task_id} updated successfully",
                    "data": {
                        "task_id": task_id,
                        "title": task.title,
                        "description": task.description,
                    },
                }
            else:
                return {
                    "success": False,
                    "message": f"Task {task_id} not found",
                    "data": None,
                }
        except ValueError:
            return {
                "success": False,
                "message": "Invalid task ID format",
                "data": None,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}",
                "data": None,
            }
