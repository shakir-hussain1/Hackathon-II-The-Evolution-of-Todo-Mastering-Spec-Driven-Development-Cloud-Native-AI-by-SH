"""Orchestrates agent and skill execution in workflows."""

from typing import Optional, Dict, Any
from src.agents.base_agent import BaseAgent, AgentContext
from src.agents.agent_registry import AgentRegistry
from src.services.task_manager import TaskManager


class AgentOrchestrator:
    """Orchestrates execution of agents and skills."""

    def __init__(self, registry: AgentRegistry, task_manager: TaskManager):
        self.registry = registry
        self.task_manager = task_manager
        self.execution_history = []

    async def execute_agent(
        self,
        agent_name: str,
        user_input: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """Execute a specific agent with given input.

        Args:
            agent_name: Name of the agent to execute
            user_input: User's input/request
            metadata: Optional metadata to pass to the agent

        Returns:
            Execution result dictionary
        """
        agent = self.registry.get_agent(agent_name)
        if not agent:
            return {
                "success": False,
                "message": f"Agent '{agent_name}' not found",
                "data": None,
            }

        context = AgentContext(
            task_manager=self.task_manager, user_input=user_input, metadata=metadata or {}
        )

        result = await agent.execute(context)

        # Record execution in history
        self.execution_history.append(
            {"agent": agent_name, "user_input": user_input, "result": result}
        )

        return result

    async def execute_skill(
        self,
        skill_name: str,
        user_input: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """Execute a specific skill directly.

        Args:
            skill_name: Name of the skill to execute
            user_input: User's input/request
            metadata: Optional metadata to pass to the skill

        Returns:
            Execution result dictionary
        """
        skill = self.registry.get_skill(skill_name)
        if not skill:
            return {
                "success": False,
                "message": f"Skill '{skill_name}' not found",
                "data": None,
            }

        context = AgentContext(
            task_manager=self.task_manager, user_input=user_input, metadata=metadata or {}
        )

        if not skill.validate(context):
            return {
                "success": False,
                "message": f"Skill '{skill_name}' validation failed",
                "data": None,
            }

        result = await skill.execute(context)

        # Record execution in history
        self.execution_history.append(
            {"skill": skill_name, "user_input": user_input, "result": result}
        )

        return result

    def get_execution_history(self) -> list:
        """Get execution history."""
        return self.execution_history

    def get_registry_info(self) -> dict:
        """Get information about registered agents and skills."""
        return self.registry.get_registry_summary()

    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
