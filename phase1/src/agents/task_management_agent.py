"""Subagent specialized in task management operations."""

from src.agents.base_agent import BaseAgent, AgentContext
from src.models.task import TaskStatus


class TaskManagementAgent(BaseAgent):
    """Handles all task creation, retrieval, update, and deletion operations."""

    def __init__(self):
        super().__init__(
            name="TaskManagementAgent",
            description="Manages task lifecycle: create, read, update, delete",
        )
        self.operation_count = 0

    async def execute(self, context: AgentContext) -> dict:
        """Execute task management operations."""
        try:
            # Parse intent from user input
            intent = self._parse_intent(context.user_input)

            if intent == "create":
                return await self._handle_create(context)
            elif intent == "retrieve":
                return await self._handle_retrieve(context)
            elif intent == "delete":
                return await self._handle_delete(context)
            elif intent == "update":
                return await self._handle_update(context)
            elif intent == "toggle":
                return await self._handle_toggle(context)
            else:
                return {
                    "success": False,
                    "message": f"Unknown operation: {intent}",
                    "data": None,
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in TaskManagementAgent: {str(e)}",
                "data": None,
            }

    def _parse_intent(self, user_input: str) -> str:
        """Parse user intent from input."""
        user_input_lower = user_input.lower()
        if any(word in user_input_lower for word in ["add", "create", "new"]):
            return "create"
        elif any(word in user_input_lower for word in ["get", "show", "list"]):
            return "retrieve"
        elif any(word in user_input_lower for word in ["delete", "remove"]):
            return "delete"
        elif any(word in user_input_lower for word in ["update", "edit", "change"]):
            return "update"
        elif any(word in user_input_lower for word in ["complete", "toggle", "mark"]):
            return "toggle"
        return "unknown"

    async def _handle_create(self, context: AgentContext) -> dict:
        """Handle task creation."""
        skill = self.get_skill("create_task")
        if not skill:
            return {
                "success": False,
                "message": "Create skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        self.operation_count += 1
        return result

    async def _handle_retrieve(self, context: AgentContext) -> dict:
        """Handle task retrieval."""
        skill = self.get_skill("list_tasks")
        if not skill:
            return {
                "success": False,
                "message": "List skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        return result

    async def _handle_delete(self, context: AgentContext) -> dict:
        """Handle task deletion."""
        skill = self.get_skill("delete_task")
        if not skill:
            return {
                "success": False,
                "message": "Delete skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        self.operation_count += 1
        return result

    async def _handle_update(self, context: AgentContext) -> dict:
        """Handle task update."""
        skill = self.get_skill("update_task")
        if not skill:
            return {
                "success": False,
                "message": "Update skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        self.operation_count += 1
        return result

    async def _handle_toggle(self, context: AgentContext) -> dict:
        """Handle task status toggle."""
        skill = self.get_skill("toggle_task_status")
        if not skill:
            return {
                "success": False,
                "message": "Toggle skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        self.operation_count += 1
        return result
