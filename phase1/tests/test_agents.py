"""Unit tests for agents and skills."""

import pytest
import asyncio
from src.services.task_manager import TaskManager
from src.agents.task_management_agent import TaskManagementAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.agent_registry import AgentRegistry
from src.agents.agent_factory import AgentFactory
from src.agents.agent_orchestrator import AgentOrchestrator
from src.agents.base_agent import AgentContext
from src.skills.task_skills import (
    CreateTaskSkill,
    ListTasksSkill,
    DeleteTaskSkill,
    ToggleTaskStatusSkill,
    UpdateTaskSkill,
)
from src.skills.analytics_skills import ComputeMetricsSkill
from src.models.task import TaskStatus


class TestAgentRegistry:
    """Test agent registry functionality."""

    def test_register_agent(self):
        """Test registering an agent."""
        registry = AgentRegistry()
        agent = TaskManagementAgent()
        registry.register_agent(agent)

        assert "TaskManagementAgent" in registry.list_all_agents()
        assert registry.get_agent("TaskManagementAgent") is agent

    def test_register_skill_for_agent(self):
        """Test registering skills for an agent."""
        registry = AgentRegistry()
        agent = TaskManagementAgent()
        skill = CreateTaskSkill()

        registry.register_agent(agent)
        registry.register_skill_for_agent("TaskManagementAgent", skill)

        assert "create_task" in registry.get_agent_skills("TaskManagementAgent")
        assert registry.get_skill("create_task") is skill

    def test_list_all_agents(self):
        """Test listing all registered agents."""
        registry = AgentRegistry()
        agent1 = TaskManagementAgent()
        agent2 = AnalyticsAgent()

        registry.register_agent(agent1)
        registry.register_agent(agent2)

        agents = registry.list_all_agents()
        assert len(agents) == 2
        assert "TaskManagementAgent" in agents
        assert "AnalyticsAgent" in agents

    def test_get_registry_summary(self):
        """Test getting registry summary."""
        registry = AgentRegistry()
        agent = TaskManagementAgent()
        skill = CreateTaskSkill()

        registry.register_agent(agent)
        registry.register_skill_for_agent("TaskManagementAgent", skill)

        summary = registry.get_registry_summary()
        assert "agents" in summary
        assert "skills" in summary
        assert "agent_skill_map" in summary


class TestTaskManagementAgent:
    """Test TaskManagementAgent functionality."""

    @pytest.mark.asyncio
    async def test_agent_execute_with_create_intent(self):
        """Test agent execution with create intent."""
        agent = TaskManagementAgent()
        agent.register_skill(CreateTaskSkill())

        task_manager = TaskManager()
        context = AgentContext(
            task_manager=task_manager, user_input="add Buy milk | For coffee"
        )

        result = await agent.execute(context)

        assert result["success"] is True
        assert "created successfully" in result["message"]

    @pytest.mark.asyncio
    async def test_agent_execute_with_retrieve_intent(self):
        """Test agent execution with retrieve intent."""
        agent = TaskManagementAgent()
        agent.register_skill(ListTasksSkill())

        task_manager = TaskManager()
        task_manager.add_task("Task 1")

        context = AgentContext(task_manager=task_manager, user_input="show all tasks")

        result = await agent.execute(context)

        assert result["success"] is True
        assert result["data"]["tasks"] is not None

    @pytest.mark.asyncio
    async def test_agent_execute_with_unknown_intent(self):
        """Test agent with unknown intent."""
        agent = TaskManagementAgent()
        agent.register_skill(CreateTaskSkill())

        task_manager = TaskManager()
        context = AgentContext(
            task_manager=task_manager, user_input="unknown command"
        )

        result = await agent.execute(context)

        assert result["success"] is False
        assert "Unknown operation" in result["message"]


class TestCreateTaskSkill:
    """Test CreateTaskSkill functionality."""

    @pytest.mark.asyncio
    async def test_create_task_skill_execution(self):
        """Test creating a task through skill."""
        skill = CreateTaskSkill()
        task_manager = TaskManager()

        context = AgentContext(
            task_manager=task_manager, user_input="Buy groceries | Fresh vegetables"
        )

        result = await skill.execute(context)

        assert result["success"] is True
        assert result["data"]["title"] == "Buy groceries"
        assert result["data"]["description"] == "Fresh vegetables"

    @pytest.mark.asyncio
    async def test_create_task_skill_without_description(self):
        """Test creating task without description."""
        skill = CreateTaskSkill()
        task_manager = TaskManager()

        context = AgentContext(task_manager=task_manager, user_input="Buy milk")

        result = await skill.execute(context)

        assert result["success"] is True
        assert result["data"]["title"] == "Buy milk"
        assert result["data"]["description"] == ""

    @pytest.mark.asyncio
    async def test_create_task_skill_without_title(self):
        """Test creating task without title."""
        skill = CreateTaskSkill()
        task_manager = TaskManager()

        context = AgentContext(task_manager=task_manager, user_input="")

        result = await skill.execute(context)

        assert result["success"] is False
        assert "Title is required" in result["message"]


class TestListTasksSkill:
    """Test ListTasksSkill functionality."""

    @pytest.mark.asyncio
    async def test_list_tasks_skill(self):
        """Test listing tasks through skill."""
        skill = ListTasksSkill()
        task_manager = TaskManager()

        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")

        context = AgentContext(task_manager=task_manager, user_input="list tasks")

        result = await skill.execute(context)

        assert result["success"] is True
        assert len(result["data"]["tasks"]) == 2

    @pytest.mark.asyncio
    async def test_list_tasks_skill_empty(self):
        """Test listing tasks when none exist."""
        skill = ListTasksSkill()
        task_manager = TaskManager()

        context = AgentContext(task_manager=task_manager, user_input="list tasks")

        result = await skill.execute(context)

        assert result["success"] is True
        assert len(result["data"]["tasks"]) == 0


class TestDeleteTaskSkill:
    """Test DeleteTaskSkill functionality."""

    @pytest.mark.asyncio
    async def test_delete_task_skill(self):
        """Test deleting a task through skill."""
        skill = DeleteTaskSkill()
        task_manager = TaskManager()

        task = task_manager.add_task("Task to delete")

        context = AgentContext(task_manager=task_manager, user_input=str(task.id))

        result = await skill.execute(context)

        assert result["success"] is True
        assert task_manager.get_task(task.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self):
        """Test deleting a non-existent task."""
        skill = DeleteTaskSkill()
        task_manager = TaskManager()

        context = AgentContext(task_manager=task_manager, user_input="999")

        result = await skill.execute(context)

        assert result["success"] is False
        assert "not found" in result["message"]


class TestToggleTaskStatusSkill:
    """Test ToggleTaskStatusSkill functionality."""

    @pytest.mark.asyncio
    async def test_toggle_task_status_skill(self):
        """Test toggling task status through skill."""
        skill = ToggleTaskStatusSkill()
        task_manager = TaskManager()

        task = task_manager.add_task("Task to toggle")
        assert task.status == TaskStatus.INCOMPLETE

        context = AgentContext(task_manager=task_manager, user_input=str(task.id))

        result = await skill.execute(context)

        assert result["success"] is True
        assert result["data"]["new_status"] == "complete"


class TestComputeMetricsSkill:
    """Test ComputeMetricsSkill functionality."""

    @pytest.mark.asyncio
    async def test_compute_metrics_skill(self):
        """Test computing metrics through skill."""
        skill = ComputeMetricsSkill()
        task_manager = TaskManager()

        task1 = task_manager.add_task("Task 1")
        task2 = task_manager.add_task("Task 2")
        task_manager.toggle_task_status(task1.id)

        context = AgentContext(task_manager=task_manager, user_input="metrics")

        result = await skill.execute(context)

        assert result["success"] is True
        assert result["data"]["total_tasks"] == 2
        assert result["data"]["completed_tasks"] == 1
        assert result["data"]["incomplete_tasks"] == 1
        assert result["data"]["completion_rate"] == 50.0


class TestAgentOrchestrator:
    """Test AgentOrchestrator functionality."""

    @pytest.mark.asyncio
    async def test_orchestrator_execute_agent(self):
        """Test orchestrator executing an agent."""
        task_manager = TaskManager()
        registry = AgentFactory.create_agent_system()
        orchestrator = AgentOrchestrator(registry, task_manager)

        result = await orchestrator.execute_agent(
            agent_name="TaskManagementAgent", user_input="add New task | Description"
        )

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_orchestrator_execute_skill(self):
        """Test orchestrator executing a skill."""
        task_manager = TaskManager()
        registry = AgentFactory.create_agent_system()
        orchestrator = AgentOrchestrator(registry, task_manager)

        task = task_manager.add_task("Task to complete")

        result = await orchestrator.execute_skill(
            skill_name="toggle_task_status", user_input=str(task.id)
        )

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_orchestrator_execution_history(self):
        """Test orchestrator tracks execution history."""
        task_manager = TaskManager()
        registry = AgentFactory.create_agent_system()
        orchestrator = AgentOrchestrator(registry, task_manager)

        await orchestrator.execute_agent(
            agent_name="TaskManagementAgent", user_input="add Test task"
        )

        history = orchestrator.get_execution_history()
        assert len(history) == 1
        assert history[0]["agent"] == "TaskManagementAgent"

    @pytest.mark.asyncio
    async def test_orchestrator_nonexistent_agent(self):
        """Test orchestrator with non-existent agent."""
        task_manager = TaskManager()
        registry = AgentFactory.create_agent_system()
        orchestrator = AgentOrchestrator(registry, task_manager)

        result = await orchestrator.execute_agent(
            agent_name="NonexistentAgent", user_input="test"
        )

        assert result["success"] is False
        assert "not found" in result["message"]


class TestAgentFactory:
    """Test AgentFactory functionality."""

    def test_create_agent_system(self):
        """Test creating a complete agent system."""
        registry = AgentFactory.create_agent_system()

        # Verify agents are registered
        assert "TaskManagementAgent" in registry.list_all_agents()
        assert "AnalyticsAgent" in registry.list_all_agents()

        # Verify skills are registered
        assert "create_task" in registry.list_all_skills()
        assert "list_tasks" in registry.list_all_skills()
        assert "delete_task" in registry.list_all_skills()
        assert "toggle_task_status" in registry.list_all_skills()
        assert "update_task" in registry.list_all_skills()
        assert "compute_metrics" in registry.list_all_skills()

    def test_agent_has_all_skills(self):
        """Test that TaskManagementAgent has all required skills."""
        registry = AgentFactory.create_agent_system()
        agent = registry.get_agent("TaskManagementAgent")

        skills = agent.list_skills()
        assert "create_task" in skills
        assert "list_tasks" in skills
        assert "delete_task" in skills
        assert "toggle_task_status" in skills
        assert "update_task" in skills
