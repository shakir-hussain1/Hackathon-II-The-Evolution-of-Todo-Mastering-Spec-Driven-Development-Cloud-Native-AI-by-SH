"""Analytics skills for task insights."""

from src.skills.base_skill import Skill, SkillConfig
from src.agents.base_agent import AgentContext
from src.models.task import TaskStatus
from datetime import datetime


class ComputeMetricsSkill(Skill):
    """Skill for computing task metrics and statistics."""

    def __init__(self):
        config = SkillConfig(
            name="compute_metrics",
            description="Computes task completion metrics and statistics",
            tags=["analytics", "metrics", "reporting"],
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        """Validate task_manager availability."""
        return hasattr(context, "task_manager") and context.task_manager is not None

    async def execute(self, context: AgentContext) -> dict:
        """Compute metrics."""
        if not self.validate(context):
            return {
                "success": False,
                "message": "Invalid context: task_manager not available",
                "data": None,
            }

        try:
            tasks = context.task_manager.list_tasks()

            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETE])
            incomplete_tasks = total_tasks - completed_tasks
            completion_rate = (
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            )

            self.execution_count += 1
            self.last_executed = datetime.now()

            return {
                "success": True,
                "message": "Metrics computed successfully",
                "data": {
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "incomplete_tasks": incomplete_tasks,
                    "completion_rate": round(completion_rate, 2),
                    "computed_at": datetime.now().isoformat(),
                },
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to compute metrics: {str(e)}",
                "data": None,
            }
