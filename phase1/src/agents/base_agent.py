"""Base agent class for all specialized agents in the Todo system."""

from dataclasses import dataclass, field
from typing import Any, Optional
from abc import ABC, abstractmethod


@dataclass
class AgentContext:
    """Context passed to agents during execution."""
    task_manager: Any
    user_input: str
    metadata: dict = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all subagents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.skills: list = []

    def register_skill(self, skill: "Skill") -> None:
        """Register a skill with this agent."""
        self.skills.append(skill)
        print(f"[{self.name}] Registered skill: {skill.name}")

    @abstractmethod
    async def execute(self, context: AgentContext) -> dict:
        """Execute the agent's primary responsibility.

        Returns:
            dict with keys: 'success', 'message', 'data'
        """
        pass

    def get_skill(self, skill_name: str) -> Optional["Skill"]:
        """Retrieve a registered skill by name."""
        for skill in self.skills:
            if skill.name == skill_name:
                return skill
        return None

    def list_skills(self) -> list[str]:
        """List all registered skills."""
        return [skill.name for skill in self.skills]
