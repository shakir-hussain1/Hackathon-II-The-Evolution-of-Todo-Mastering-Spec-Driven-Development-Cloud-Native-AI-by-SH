"""Registry for managing agents and skills across the application."""

from typing import Dict, Optional, List
from src.agents.base_agent import BaseAgent
from src.skills.base_skill import Skill


class AgentRegistry:
    """Centralized registry for agents and skills management."""

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._skills: Dict[str, Skill] = {}
        self._agent_skill_map: Dict[str, List[str]] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent in the registry."""
        self._agents[agent.name] = agent
        self._agent_skill_map[agent.name] = []
        print(f"[Registry] Agent registered: {agent.name}")

    def register_skill_for_agent(self, agent_name: str, skill: Skill) -> None:
        """Register a skill for a specific agent."""
        if agent_name not in self._agents:
            raise ValueError(f"Agent '{agent_name}' not found in registry")

        agent = self._agents[agent_name]
        agent.register_skill(skill)
        self._skills[skill.name] = skill
        self._agent_skill_map[agent_name].append(skill.name)
        print(f"[Registry] Skill '{skill.name}' registered for {agent_name}")

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Retrieve an agent by name."""
        return self._agents.get(agent_name)

    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Retrieve a skill by name."""
        return self._skills.get(skill_name)

    def get_agent_skills(self, agent_name: str) -> List[str]:
        """Get all skills for a specific agent."""
        return self._agent_skill_map.get(agent_name, [])

    def list_all_agents(self) -> List[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def list_all_skills(self) -> List[str]:
        """List all registered skill names."""
        return list(self._skills.keys())

    def get_registry_summary(self) -> dict:
        """Get a summary of the registry state."""
        return {
            "agents": self.list_all_agents(),
            "skills": self.list_all_skills(),
            "agent_skill_map": self._agent_skill_map,
        }
