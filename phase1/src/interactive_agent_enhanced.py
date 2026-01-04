"""Interactive CLI for Todo Application - Phase 1 with Agent System.

This is an enhanced version of interactive.py that uses the agent system
for intelligent task management and analytics.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add parent directory to path to allow imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.services.task_manager import TaskManager
    from src.agents.agent_factory import AgentFactory
    from src.agents.agent_orchestrator import AgentOrchestrator
except ImportError:
    from services.task_manager import TaskManager
    from agents.agent_factory import AgentFactory
    from agents.agent_orchestrator import AgentOrchestrator


def print_help():
    """Print available commands."""
    print(
        """
================================================
   TODO CLI WITH AGENT SYSTEM - AVAILABLE COMMANDS
================================================

TASK MANAGEMENT:
  add <title>                    - Add new task
  add <title> | <description>    - Add task with description
  list                           - List all tasks
  list json                      - List tasks as JSON
  complete <id>                  - Mark task complete
  incomplete <id>                - Mark task incomplete
  update <id> -t <title>         - Update task title
  update <id> -d <description>   - Update task description
  update <id> -t <title> -d <desc> - Update both
  delete <id>                    - Delete task

ANALYTICS:
  analytics                      - Show task completion metrics
  stats                          - Show task statistics

SYSTEM:
  registry                       - Show registered agents and skills
  history                        - Show execution history
  clear-history                  - Clear execution history
  help                           - Show this help
  exit                           - Exit application

EXAMPLES:
  todo> add Buy groceries
  todo> add Buy milk | For breakfast
  todo> list
  todo> complete 1
  todo> update 1 -t New title
  todo> update 1 -d New description
  todo> delete 1
  todo> analytics
================================================
"""
    )


async def run_interactive_with_agents():
    """Run interactive CLI with agent system."""
    task_manager = TaskManager()

    # Initialize agent system
    registry = AgentFactory.create_agent_system()
    orchestrator = AgentOrchestrator(registry, task_manager)

    print("\n" + "=" * 50)
    print("   PHASE 1 - TODO WITH AGENT SYSTEM")
    print("=" * 50)
    print("Type 'help' for commands, 'exit' to quit\n")

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            if command == "exit" or command == "quit":
                print("Goodbye!")
                break

            elif command == "help":
                print_help()

            elif command == "add":
                if len(parts) < 2:
                    print("Error: Title required. Usage: add <title> [| description]")
                    continue

                # Convert input format for skill
                # Format: "Buy groceries | Fresh vegetables"
                title_and_desc = " ".join(parts[1:])
                result = await orchestrator.execute_skill(
                    skill_name="create_task", user_input=title_and_desc
                )

                if result["success"]:
                    task_data = result["data"]
                    print(f"[OK] Task {task_data['task_id']} added: {task_data['title']}")
                    if task_data["description"]:
                        print(f"     Description: {task_data['description']}")
                else:
                    print(f"[ERROR] {result['message']}")

            elif command == "list":
                format_type = "human"
                if len(parts) > 1 and parts[1].lower() == "json":
                    format_type = "json"

                result = await orchestrator.execute_skill(
                    skill_name="list_tasks", user_input="list"
                )

                if result["success"]:
                    tasks = result["data"]["tasks"]
                    if not tasks:
                        print("No tasks yet")
                    elif format_type == "json":
                        print(json.dumps({"tasks": tasks}, indent=2))
                    else:
                        for task in tasks:
                            status_symbol = "[X]" if task["status"] == "complete" else "[ ]"
                            print(f"{task['id']}. {task['title']} {status_symbol}")
                else:
                    print(f"[ERROR] {result['message']}")

            elif command == "complete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: complete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    result = await orchestrator.execute_skill(
                        skill_name="toggle_task_status", user_input=str(task_id)
                    )

                    if result["success"]:
                        print(
                            f"[OK] Task {task_id} marked as {result['data']['new_status']}"
                        )
                    else:
                        print(f"[ERROR] {result['message']}")
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "incomplete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: incomplete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    result = await orchestrator.execute_skill(
                        skill_name="toggle_task_status", user_input=str(task_id)
                    )

                    if result["success"]:
                        print(
                            f"[OK] Task {task_id} marked as {result['data']['new_status']}"
                        )
                    else:
                        print(f"[ERROR] {result['message']}")
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "update":
                if len(parts) < 2:
                    print(
                        "Error: Usage: update <id> -t <title> -d <description>"
                    )
                    continue
                try:
                    task_id = int(parts[1])
                    title = None
                    description = None

                    # Parse -t and -d flags
                    if "-t" in parts:
                        t_index = parts.index("-t")
                        if "-d" in parts:
                            d_index = parts.index("-d")
                            title = " ".join(parts[t_index + 1 : d_index])
                            description = " ".join(parts[d_index + 1 :])
                        else:
                            title = " ".join(parts[t_index + 1 :])
                    elif "-d" in parts:
                        d_index = parts.index("-d")
                        description = " ".join(parts[d_index + 1 :])

                    if not title and not description:
                        print("Error: At least title or description required")
                        continue

                    update_input = f"{task_id}|{title or ''}|{description or ''}"
                    result = await orchestrator.execute_skill(
                        skill_name="update_task", user_input=update_input
                    )

                    if result["success"]:
                        print(f"[OK] Task {task_id} updated")
                    else:
                        print(f"[ERROR] {result['message']}")
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "delete":
                if len(parts) < 2:
                    print("Error: Task ID required. Usage: delete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    result = await orchestrator.execute_skill(
                        skill_name="delete_task", user_input=str(task_id)
                    )

                    if result["success"]:
                        print(f"[OK] Task {task_id} deleted")
                    else:
                        print(f"[ERROR] {result['message']}")
                except ValueError:
                    print("Error: Invalid ID format")

            elif command == "analytics" or command == "stats":
                result = await orchestrator.execute_agent(
                    agent_name="AnalyticsAgent", user_input="compute metrics"
                )

                if result["success"]:
                    metrics = result["data"]
                    print("\n" + "=" * 40)
                    print("TASK ANALYTICS")
                    print("=" * 40)
                    print(f"Total Tasks:      {metrics['total_tasks']}")
                    print(f"Completed:        {metrics['completed_tasks']}")
                    print(f"Incomplete:       {metrics['incomplete_tasks']}")
                    print(f"Completion Rate:  {metrics['completion_rate']}%")
                    print("=" * 40 + "\n")
                else:
                    print(f"✗ {result['message']}")

            elif command == "registry":
                info = orchestrator.get_registry_info()
                print("\n" + "=" * 40)
                print("AGENT SYSTEM REGISTRY")
                print("=" * 40)
                print(f"\nRegistered Agents:")
                for agent in info["agents"]:
                    print(f"  • {agent}")

                print(f"\nRegistered Skills:")
                for skill in info["skills"]:
                    print(f"  • {skill}")

                print(f"\nAgent-Skill Mapping:")
                for agent, skills in info["agent_skill_map"].items():
                    print(f"  {agent}:")
                    for skill in skills:
                        print(f"    - {skill}")
                print("=" * 40 + "\n")

            elif command == "history":
                history = orchestrator.get_execution_history()
                if not history:
                    print("No execution history yet")
                else:
                    print("\n" + "=" * 40)
                    print("EXECUTION HISTORY")
                    print("=" * 40)
                    for i, entry in enumerate(history, 1):
                        agent_or_skill = entry.get("agent") or entry.get("skill")
                        success = entry["result"]["success"]
                        status = "OK" if success else "FAIL"
                        print(
                            f"{i}. [{status}] {agent_or_skill}: {entry['result']['message']}"
                        )
                    print("=" * 40 + "\n")

            elif command == "clear-history":
                orchestrator.clear_history()
                print("Execution history cleared")

            else:
                print(f"Unknown command: {command}")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point."""
    asyncio.run(run_interactive_with_agents())


if __name__ == "__main__":
    main()
