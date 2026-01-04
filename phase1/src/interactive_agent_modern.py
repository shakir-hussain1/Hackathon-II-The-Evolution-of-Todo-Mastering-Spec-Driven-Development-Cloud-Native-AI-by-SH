"""Modern, stylish interactive CLI for Todo Application with Agent System.

Uses Rich library for beautiful, colorful terminal UI with:
- Colored output and panels
- Beautiful tables for task listing
- Progress indicators
- Modern formatting
- Interactive experience
"""

import sys
import asyncio
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule

# Add parent directory to path
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

# Initialize Rich console
console = Console()


def print_banner():
    """Print beautiful banner."""
    banner = Panel(
        "[bold cyan]AGENT-POWERED TODO APPLICATION[/bold cyan]\n"
        "[yellow]Phase 1 - Intelligent Task Management[/yellow]",
        border_style="cyan",
        padding=(2, 4),
        title="[bold green]Welcome[/bold green]",
    )
    console.print(banner)


def print_welcome():
    """Print welcome message."""
    welcome = Panel(
        "[bold yellow]Ready to manage your tasks![/bold yellow]\n"
        "[cyan]Type 'help' for commands | 'exit' to quit[/cyan]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(welcome)


def print_help():
    """Print help text."""
    help_text = """
[bold cyan]TASK COMMANDS[/bold cyan]
[green]add <title>[/green]              - Create new task
[green]add <title> | <desc>[/green]     - Create with description
[green]list[/green]                     - Show all tasks
[green]list json[/green]                - Show tasks as JSON
[green]complete <id>[/green]            - Mark task as done
[green]incomplete <id>[/green]          - Mark task as pending
[green]update <id> -t <title>[/green]   - Update task title
[green]update <id> -d <desc>[/green]    - Update description
[green]delete <id>[/green]              - Remove task

[bold cyan]SYSTEM COMMANDS[/bold cyan]
[green]analytics[/green]                - Show task statistics
[green]registry[/green]                 - Show agent/skill info
[green]history[/green]                  - Show execution log
[green]clear-history[/green]            - Clear execution log
[green]help[/green]                     - Show this help
[green]exit[/green]                     - Quit application

[bold cyan]EXAMPLES[/bold cyan]
[yellow]add Shopping[/yellow]
[yellow]add Buy milk | For breakfast[/yellow]
[yellow]list[/yellow]
[yellow]complete 1[/yellow]
[yellow]analytics[/yellow]
"""
    console.print(help_text)


def create_task_table(tasks):
    """Create a beautiful table for tasks."""
    table = Table(
        title="[bold cyan]Your Tasks[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        padding=(0, 1),
    )

    table.add_column("ID", style="cyan", width=5)
    table.add_column("Task", style="white")
    table.add_column("Description", style="gray50")
    table.add_column("Status", style="magenta", width=12)

    if not tasks:
        table.add_row("--", "[dim]No tasks yet[/dim]", "", "")
    else:
        for task in tasks:
            status_badge = (
                "[bold green][DONE][/bold green]"
                if task["status"] == "complete"
                else "[bold yellow][TODO][/bold yellow]"
            )

            table.add_row(
                str(task["id"]),
                task["title"][:40],
                (task["description"][:25] + "...") if task["description"] else "--",
                status_badge,
            )

    return table


def create_metrics_panel(metrics):
    """Create a beautiful metrics panel."""
    total = metrics["total_tasks"]
    completed = metrics["completed_tasks"]
    incomplete = metrics["incomplete_tasks"]
    rate = metrics["completion_rate"]

    # Create progress bar visualization
    bar_length = 25
    filled = int((rate / 100) * bar_length)
    bar = "[green]" + "=" * filled + "[/green]" + "[dim]" + "-" * (bar_length - filled) + "[/dim]"

    metrics_text = f"""
[bold cyan]Total Tasks:[/bold cyan]      {total}
[bold green]Completed:[/bold green]      {completed}
[bold yellow]Pending:[/bold yellow]       {incomplete}

[bold magenta]Progress:[/bold magenta]
{bar} {rate}%
"""

    panel = Panel(
        metrics_text,
        title="[bold green]Task Analytics[/bold green]",
        border_style="green",
        padding=(1, 2),
    )

    return panel


async def run_modern_cli():
    """Run modern interactive CLI."""
    print_banner()

    # Initialize agent system
    with console.status("[bold green]Initializing agent system...[/bold green]"):
        task_manager = TaskManager()
        registry = AgentFactory.create_agent_system()
        orchestrator = AgentOrchestrator(registry, task_manager)

    console.print("[green]Agent system ready![/green]\n")
    print_welcome()

    while True:
        try:
            # Get user input
            user_input = console.input("\n[bold cyan]todo[/bold cyan] [bold magenta]>[/bold magenta] ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            # ===== EXIT =====
            if command in ("exit", "quit"):
                farewell = Panel(
                    "[bold yellow]See you soon![/bold yellow]",
                    border_style="cyan",
                    padding=(1, 2),
                )
                console.print(farewell)
                break

            # ===== HELP =====
            elif command == "help":
                print_help()

            # ===== ADD =====
            elif command == "add":
                if len(parts) < 2:
                    console.print("[bold red]Error:[/bold red] Title required")
                    continue

                title_and_desc = " ".join(parts[1:])

                with console.status("[bold cyan]Adding task...[/bold cyan]"):
                    result = await orchestrator.execute_skill(
                        skill_name="create_task", user_input=title_and_desc
                    )

                if result["success"]:
                    task_data = result["data"]
                    task_panel = Panel(
                        f"[bold green]Task created![/bold green]\n\n"
                        f"[cyan]ID:[/cyan] {task_data['task_id']}\n"
                        f"[cyan]Title:[/cyan] {task_data['title']}\n"
                        f"[cyan]Description:[/cyan] {task_data['description'] or '(none)'}",
                        border_style="green",
                        padding=(1, 2),
                    )
                    console.print(task_panel)
                else:
                    console.print(f"[bold red]Error:[/bold red] {result['message']}")

            # ===== LIST =====
            elif command == "list":
                format_type = "human"
                if len(parts) > 1 and parts[1].lower() == "json":
                    format_type = "json"

                with console.status("[bold cyan]Loading tasks...[/bold cyan]"):
                    result = await orchestrator.execute_skill(
                        skill_name="list_tasks", user_input="list"
                    )

                if result["success"]:
                    tasks = result["data"]["tasks"]
                    if format_type == "json":
                        console.print_json(data=tasks)
                    else:
                        table = create_task_table(tasks)
                        console.print(table)
                        console.print(f"[cyan]Total: {len(tasks)} task(s)[/cyan]\n")
                else:
                    console.print(f"[bold red]Error:[/bold red] {result['message']}")

            # ===== COMPLETE =====
            elif command == "complete":
                if len(parts) < 2:
                    console.print("[bold red]Error:[/bold red] Task ID required")
                    continue
                try:
                    task_id = int(parts[1])

                    with console.status("[bold cyan]Marking task complete...[/bold cyan]"):
                        result = await orchestrator.execute_skill(
                            skill_name="toggle_task_status", user_input=str(task_id)
                        )

                    if result["success"]:
                        console.print(f"[bold green]Task {task_id} marked as {result['data']['new_status']}![/bold green]")
                    else:
                        console.print(f"[bold red]Error:[/bold red] {result['message']}")
                except ValueError:
                    console.print("[bold red]Error:[/bold red] Invalid task ID")

            # ===== INCOMPLETE =====
            elif command == "incomplete":
                if len(parts) < 2:
                    console.print("[bold red]Error:[/bold red] Task ID required")
                    continue
                try:
                    task_id = int(parts[1])

                    with console.status("[bold cyan]Marking task incomplete...[/bold cyan]"):
                        result = await orchestrator.execute_skill(
                            skill_name="toggle_task_status", user_input=str(task_id)
                        )

                    if result["success"]:
                        console.print(f"[bold green]Task {task_id} marked as {result['data']['new_status']}![/bold green]")
                    else:
                        console.print(f"[bold red]Error:[/bold red] {result['message']}")
                except ValueError:
                    console.print("[bold red]Error:[/bold red] Invalid task ID")

            # ===== UPDATE =====
            elif command == "update":
                if len(parts) < 2:
                    console.print("[bold red]Error:[/bold red] Task ID required")
                    continue
                try:
                    task_id = int(parts[1])
                    title = None
                    description = None

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
                        console.print("[bold red]Error:[/bold red] At least title or description required")
                        continue

                    update_input = f"{task_id}|{title or ''}|{description or ''}"

                    with console.status("[bold cyan]Updating task...[/bold cyan]"):
                        result = await orchestrator.execute_skill(
                            skill_name="update_task", user_input=update_input
                        )

                    if result["success"]:
                        console.print(f"[bold green]Task {task_id} updated![/bold green]")
                    else:
                        console.print(f"[bold red]Error:[/bold red] {result['message']}")
                except ValueError:
                    console.print("[bold red]Error:[/bold red] Invalid task ID")

            # ===== DELETE =====
            elif command == "delete":
                if len(parts) < 2:
                    console.print("[bold red]Error:[/bold red] Task ID required")
                    continue
                try:
                    task_id = int(parts[1])

                    with console.status("[bold cyan]Deleting task...[/bold cyan]"):
                        result = await orchestrator.execute_skill(
                            skill_name="delete_task", user_input=str(task_id)
                        )

                    if result["success"]:
                        console.print(f"[bold green]Task {task_id} deleted![/bold green]")
                    else:
                        console.print(f"[bold red]Error:[/bold red] {result['message']}")
                except ValueError:
                    console.print("[bold red]Error:[/bold red] Invalid task ID")

            # ===== ANALYTICS =====
            elif command in ("analytics", "stats"):
                with console.status("[bold cyan]Computing metrics...[/bold cyan]"):
                    result = await orchestrator.execute_agent(
                        agent_name="AnalyticsAgent", user_input="compute metrics"
                    )

                if result["success"]:
                    metrics_panel = create_metrics_panel(result["data"])
                    console.print(metrics_panel)
                else:
                    console.print(f"[bold red]Error:[/bold red] {result['message']}")

            # ===== REGISTRY =====
            elif command == "registry":
                info = orchestrator.get_registry_info()

                registry_table = Table(title="[bold cyan]System Registry[/bold cyan]")
                registry_table.add_column("Type", style="magenta")
                registry_table.add_column("Name", style="cyan")

                for agent in info["agents"]:
                    registry_table.add_row("Agent", agent)

                for skill in info["skills"]:
                    registry_table.add_row("Skill", skill)

                console.print(registry_table)

            # ===== HISTORY =====
            elif command == "history":
                history = orchestrator.get_execution_history()
                if not history:
                    console.print("[yellow]No execution history yet[/yellow]")
                else:
                    history_table = Table(title="[bold cyan]Execution History[/bold cyan]")
                    history_table.add_column("#", style="cyan", width=3)
                    history_table.add_column("Agent/Skill", style="magenta")
                    history_table.add_column("Message", style="white")
                    history_table.add_column("Status", style="magenta")

                    for i, entry in enumerate(history, 1):
                        agent_or_skill = entry.get("agent") or entry.get("skill")
                        success = entry["result"]["success"]
                        status = "[bold green]OK[/bold green]" if success else "[bold red]FAIL[/bold red]"

                        history_table.add_row(
                            str(i),
                            agent_or_skill,
                            entry["result"]["message"][:40],
                            status,
                        )

                    console.print(history_table)

            # ===== CLEAR-HISTORY =====
            elif command == "clear-history":
                orchestrator.clear_history()
                console.print("[bold green]Execution history cleared![/bold green]")

            else:
                console.print(f"[bold red]Unknown command:[/bold red] [yellow]{command}[/yellow]")
                console.print("[cyan]Type 'help' for available commands[/cyan]")

        except KeyboardInterrupt:
            farewell = Panel(
                "[bold yellow]Interrupted. Goodbye![/bold yellow]",
                border_style="cyan",
                padding=(1, 2),
            )
            console.print(farewell)
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")


def main():
    """Main entry point."""
    asyncio.run(run_modern_cli())


if __name__ == "__main__":
    main()
