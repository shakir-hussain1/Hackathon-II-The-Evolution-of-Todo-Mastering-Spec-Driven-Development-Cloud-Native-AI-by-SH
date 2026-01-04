"""Example of invoking agents from your application.

This file demonstrates how to use the agent system with the orchestrator.
Run this to see agents and skills in action.
"""

import asyncio
import json
from src.services.task_manager import TaskManager
from src.agents.agent_factory import AgentFactory
from src.agents.agent_orchestrator import AgentOrchestrator


async def main_with_agents():
    """Main entry point using agent system."""

    # Initialize task manager
    task_manager = TaskManager()

    # Create and initialize agent system
    print("\n" + "=" * 60)
    print("AGENT SYSTEM INITIALIZATION")
    print("=" * 60)
    registry = AgentFactory.create_agent_system()

    # Create orchestrator
    orchestrator = AgentOrchestrator(registry, task_manager)

    # Example 1: Create a task using TaskManagementAgent
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Create Task via Agent")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent",
        user_input="Buy groceries | Milk, eggs, bread",
        metadata={},
    )
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    if result["data"]:
        print(f"Data: {json.dumps(result['data'], indent=2)}")

    # Example 2: Create another task
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Create Another Task")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent",
        user_input="Call mom | This weekend",
        metadata={},
    )
    print(f"Message: {result['message']}")

    # Example 3: List all tasks
    print("\n" + "=" * 60)
    print("EXAMPLE 3: List Tasks via Agent")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent", user_input="show all tasks"
    )
    print(f"Message: {result['message']}")
    if result["data"]:
        tasks = result["data"]["tasks"]
        for task in tasks:
            print(
                f"  - Task {task['id']}: {task['title']} [{task['status']}]"
            )

    # Example 4: Toggle task status
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Toggle Task Status via Skill")
    print("=" * 60)
    result = await orchestrator.execute_skill(skill_name="toggle_task_status", user_input="1")
    print(f"Message: {result['message']}")
    if result["data"]:
        print(f"Task {result['data']['task_id']} is now {result['data']['new_status']}")

    # Example 5: Update a task
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Update Task via Agent")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent",
        user_input="Update task 2 | Call parents | This coming weekend",
    )
    print(f"Message: {result['message']}")

    # Example 6: Get analytics
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Analytics via Agent")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="AnalyticsAgent", user_input="compute metrics"
    )
    print(f"Message: {result['message']}")
    if result["data"]:
        metrics = result["data"]
        print(f"  Total Tasks: {metrics['total_tasks']}")
        print(f"  Completed: {metrics['completed_tasks']}")
        print(f"  Incomplete: {metrics['incomplete_tasks']}")
        print(f"  Completion Rate: {metrics['completion_rate']}%")

    # Example 7: View registry information
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Registry Information")
    print("=" * 60)
    registry_info = orchestrator.get_registry_info()
    print(f"Registered Agents: {registry_info['agents']}")
    print(f"Registered Skills: {registry_info['skills']}")
    print("\nAgent-Skill Mapping:")
    for agent, skills in registry_info["agent_skill_map"].items():
        print(f"  {agent}: {skills}")

    # Example 8: View execution history
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Execution History")
    print("=" * 60)
    history = orchestrator.get_execution_history()
    for i, entry in enumerate(history, 1):
        agent_or_skill = entry.get("agent") or entry.get("skill")
        success = entry["result"]["success"]
        print(f"{i}. {agent_or_skill}: {entry['result']['message']} ({'✓' if success else '✗'})")

    # Example 9: List tasks again to show final state
    print("\n" + "=" * 60)
    print("EXAMPLE 9: Final Task List")
    print("=" * 60)
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent", user_input="list all"
    )
    if result["data"]:
        tasks = result["data"]["tasks"]
        for task in tasks:
            status_symbol = "✓" if task["status"] == "complete" else "✘"
            print(f"  {task['id']}. {task['title']} {status_symbol}")

    print("\n" + "=" * 60)
    print("AGENT SYSTEM DEMO COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main_with_agents())
