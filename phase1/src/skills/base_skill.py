"""Base skill class for composable agent capabilities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class SkillConfig:
    """Configuration for a skill."""

    name: str
    description: str
    version: str = "1.0.0"
    tags: list = field(default_factory=list)


class Skill(ABC):
    """Abstract base class for all skills."""

    def __init__(self, config: SkillConfig):
        self.config = config
        self.name = config.name
        self.description = config.description
        self.version = config.version
        self.tags = config.tags
        self.execution_count = 0
        self.last_executed: Optional[datetime] = None

    @abstractmethod
    async def execute(self, context: Any) -> dict:
        """Execute the skill.

        Args:
            context: AgentContext or similar context object

        Returns:
            dict with keys: 'success', 'message', 'data'
        """
        pass

    @abstractmethod
    def validate(self, context: Any) -> bool:
        """Validate that the skill can be executed with given context."""
        pass

    def get_metadata(self) -> dict:
        """Get skill metadata."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "tags": self.tags,
            "execution_count": self.execution_count,
            "last_executed": self.last_executed.isoformat() if self.last_executed else None,
        }
