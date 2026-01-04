"""Factory for creating and initializing agents with their skills."""

from src.agents.agent_registry import AgentRegistry
from src.agents.task_management_agent import TaskManagementAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.skills.task_skills import (
    CreateTaskSkill,
    ListTasksSkill,
    DeleteTaskSkill,
    ToggleTaskStatusSkill,
    UpdateTaskSkill,
)
from src.skills.analytics_skills import ComputeMetricsSkill


class AgentFactory:
    """Factory for creating a fully configured agent system."""

    @staticmethod
    def create_agent_system() -> AgentRegistry:
        """Create and initialize all agents with their skills.

        Returns:
            Configured AgentRegistry ready for use
        """
        registry = AgentRegistry()

        # Create Task Management Agent with skills
        task_agent = TaskManagementAgent()
        registry.register_agent(task_agent)
        registry.register_skill_for_agent("TaskManagementAgent", CreateTaskSkill())
        registry.register_skill_for_agent("TaskManagementAgent", ListTasksSkill())
        registry.register_skill_for_agent("TaskManagementAgent", DeleteTaskSkill())
        registry.register_skill_for_agent("TaskManagementAgent", ToggleTaskStatusSkill())
        registry.register_skill_for_agent("TaskManagementAgent", UpdateTaskSkill())

        # Create Analytics Agent with skills
        analytics_agent = AnalyticsAgent()
        registry.register_agent(analytics_agent)
        registry.register_skill_for_agent("AnalyticsAgent", ComputeMetricsSkill())

        print("[AgentFactory] Agent system initialized successfully")
        return registry
