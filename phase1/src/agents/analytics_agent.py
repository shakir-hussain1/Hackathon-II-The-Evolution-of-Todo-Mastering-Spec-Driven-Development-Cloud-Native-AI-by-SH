"""Subagent specialized in task analytics and insights."""

from src.agents.base_agent import BaseAgent, AgentContext
from src.models.task import TaskStatus
from datetime import datetime


class AnalyticsAgent(BaseAgent):
    """Provides insights and analytics about tasks."""

    def __init__(self):
        super().__init__(
            name="AnalyticsAgent",
            description="Provides task completion metrics and insights",
        )

    async def execute(self, context: AgentContext) -> dict:
        """Execute analytics operations."""
        try:
            intent = self._parse_intent(context.user_input)

            if intent == "metrics":
                return await self._handle_metrics(context)
            else:
                return {
                    "success": False,
                    "message": f"Unknown analytics operation: {intent}",
                    "data": None,
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error in AnalyticsAgent: {str(e)}",
                "data": None,
            }

    def _parse_intent(self, user_input: str) -> str:
        """Parse analytics intent from input."""
        user_input_lower = user_input.lower()
        if any(
            word in user_input_lower
            for word in ["metric", "analytics", "stats", "report", "summary"]
        ):
            return "metrics"
        return "unknown"

    async def _handle_metrics(self, context: AgentContext) -> dict:
        """Handle metrics computation."""
        skill = self.get_skill("compute_metrics")
        if not skill:
            return {
                "success": False,
                "message": "Compute metrics skill not available",
                "data": None,
            }

        result = await skill.execute(context)
        return result
