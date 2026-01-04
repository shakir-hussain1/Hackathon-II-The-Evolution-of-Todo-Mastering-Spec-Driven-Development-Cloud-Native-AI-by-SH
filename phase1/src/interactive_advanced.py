"""Advanced Interactive CLI for Todo Application - Phase 1 with Rich UI."""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to allow imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.align import Align
    from rich.text import Text
except ImportError:
    print("Error: rich library not found. Run: pip install rich")
    sys.exit(1)

try:
    from src.services.task_manager import TaskManager
    from src.cli.commands import (
        add_command,
        list_command,
        update_command,
        delete_command,
        complete_command,
        incomplete_command,
    )
except ImportError:
    from services.task_manager import TaskManager
    from cli.commands import (
        add_command,
        list_command,
        update_command,
        delete_command,
        complete_command,
        incomplete_command,
    )


class AdvancedArgs:
    """Mock args object for commands."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class TodoCLI:
    """Advanced Todo CLI with Rich styling."""

    def __init__(self):
        self.console = Console()
        self.task_manager = TaskManager()
        self.running = True

    def show_welcome(self):
        """Display welcome banner."""
        title = Text("[TODO] IN-MEMORY CLI APPLICATION", style="bold cyan")
        subtitle = Text("Phase 1 - Advanced Interactive Edition", style="italic magenta")

        panel = Panel(
            f"{title}\n{subtitle}",
            border_style="cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        self.console.print("Type [bold yellow]'help'[/] for commands | [bold yellow]'exit'[/] to quit\n")

    def show_stats(self):
        """Display task statistics."""
        tasks = self.task_manager.list_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status.value == "complete")
        incomplete = total - completed

        if total == 0:
            return

        progress = f"[green]{completed}[/]/[cyan]{total}[/]"
        stats_text = f"[STATS] {progress} completed | [yellow]{incomplete}[/] pending"
        self.console.print(stats_text)

    def show_help(self):
        """Display help with nice formatting."""
        help_table = Table(title="[HELP] Available Commands", border_style="cyan", title_style="bold cyan")
        help_table.add_column("Command", style="bold yellow", width=30)
        help_table.add_column("Description", style="white")

        commands = [
            ("add <title>", "Add a new task"),
            ("add <title> -d <desc>", "Add task with description"),
            ("list", "List all tasks"),
            ("list json", "Export tasks as JSON"),
            ("list completed", "Show only completed tasks"),
            ("list pending", "Show only pending tasks"),
            ("search <keyword>", "Search tasks by title"),
            ("complete <id>", "Mark task as complete"),
            ("incomplete <id>", "Mark task as incomplete"),
            ("update <id> -t <title>", "Update task title"),
            ("update <id> -d <desc>", "Update task description"),
            ("delete <id>", "Delete a task"),
            ("stats", "Show task statistics"),
            ("help", "Show this help"),
            ("exit", "Exit application"),
        ]

        for cmd, desc in commands:
            help_table.add_row(cmd, desc)

        self.console.print(help_table)
        self.console.print()

    def show_tasks(self, format_type="human", filter_type=None, search_query=None):
        """Display tasks with rich formatting."""
        tasks = self.task_manager.list_tasks()

        # Filter tasks
        if filter_type == "completed":
            tasks = [t for t in tasks if t.status.value == "complete"]
        elif filter_type == "pending":
            tasks = [t for t in tasks if t.status.value == "incomplete"]

        # Search tasks
        if search_query:
            search_query = search_query.lower()
            tasks = [t for t in tasks if search_query in t.title.lower() or search_query in t.description.lower()]

        if not tasks:
            self.console.print("[yellow][EMPTY] No tasks found[/]\n")
            return

        if format_type == "json":
            self._show_json_format(tasks)
        else:
            self._show_table_format(tasks)

    def _show_table_format(self, tasks):
        """Display tasks in table format."""
        table = Table(title="[TASKS] Active Tasks", border_style="cyan", title_style="bold cyan")
        table.add_column("ID", style="bold yellow", width=5)
        table.add_column("Status", width=10)
        table.add_column("Title", style="bold white")
        table.add_column("Description", style="dim white")

        for task in tasks:
            status_icon = "[green][x][/]" if task.status.value == "complete" else "[yellow][ ][/]"
            status_text = "Complete" if task.status.value == "complete" else "Pending"
            style = "dim white" if task.status.value == "complete" else "white"

            table.add_row(
                str(task.id),
                status_icon,
                Text(task.title, style=style),
                task.description or "[dim]-[/]"
            )

        self.console.print(table)
        self.console.print()

    def _show_json_format(self, tasks):
        """Display tasks in JSON format."""
        import json
        tasks_data = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]
        json_str = json.dumps({"tasks": tasks_data}, indent=2)
        self.console.print("[dim]" + json_str + "[/]")
        self.console.print()

    def handle_command(self, user_input):
        """Parse and handle user commands."""
        if not user_input.strip():
            return

        parts = user_input.split()
        command = parts[0].lower()

        try:
            if command == "exit" or command == "quit":
                self.console.print("[cyan][BYE] Goodbye! Task data saved in memory.[/]")
                self.running = False

            elif command == "help":
                self.show_help()

            elif command == "stats":
                self.show_stats()

            elif command == "add":
                self._handle_add(parts)

            elif command == "list":
                self._handle_list(parts)

            elif command == "search":
                self._handle_search(parts)

            elif command == "complete":
                self._handle_complete(parts)

            elif command == "incomplete":
                self._handle_incomplete(parts)

            elif command == "update":
                self._handle_update(parts)

            elif command == "delete":
                self._handle_delete(parts)

            else:
                self.console.print(f"[red][ERROR] Unknown command: {command}[/] Type [yellow]'help'[/] for available commands\n")

        except Exception as e:
            self.console.print(f"[red][ERROR] {str(e)}[/]\n")

    def _handle_add(self, parts):
        """Handle add command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Title required[/] Usage: [yellow]add <title> [-d description][/]\n")
            return

        title = ""
        description = ""

        if "-d" in parts:
            d_index = parts.index("-d")
            title = " ".join(parts[1:d_index])
            description = " ".join(parts[d_index+1:])
        else:
            title = " ".join(parts[1:])

        args = AdvancedArgs(title=title, description=description)
        add_command(self.task_manager, args)
        self.console.print()

    def _handle_list(self, parts):
        """Handle list command."""
        format_type = "human"
        filter_type = None

        if len(parts) > 1:
            if parts[1] == "json":
                format_type = "json"
            elif parts[1] in ["completed", "pending"]:
                filter_type = parts[1]

        self.show_tasks(format_type=format_type, filter_type=filter_type)

    def _handle_search(self, parts):
        """Handle search command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Search query required[/] Usage: [yellow]search <keyword>[/]\n")
            return

        query = " ".join(parts[1:])
        self.console.print(f"[SEARCH] Searching for: [yellow]{query}[/]\n")
        self.show_tasks(search_query=query)

    def _handle_complete(self, parts):
        """Handle complete command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Task ID required[/] Usage: [yellow]complete <id>[/]\n")
            return

        try:
            task_id = int(parts[1])
            args = AdvancedArgs(id=task_id)
            complete_command(self.task_manager, args)
            self.console.print()
        except ValueError:
            self.console.print("[red][ERROR] Invalid task ID[/]\n")

    def _handle_incomplete(self, parts):
        """Handle incomplete command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Task ID required[/] Usage: [yellow]incomplete <id>[/]\n")
            return

        try:
            task_id = int(parts[1])
            args = AdvancedArgs(id=task_id)
            incomplete_command(self.task_manager, args)
            self.console.print()
        except ValueError:
            self.console.print("[red][ERROR] Invalid task ID[/]\n")

    def _handle_update(self, parts):
        """Handle update command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Task ID required[/] Usage: [yellow]update <id> [-t title] [-d description][/]\n")
            return

        try:
            task_id = int(parts[1])
            title = None
            description = None

            if "-t" in parts:
                t_index = parts.index("-t")
                if "-d" in parts:
                    d_index = parts.index("-d")
                    if t_index < d_index:
                        title = " ".join(parts[t_index+1:d_index])
                        description = " ".join(parts[d_index+1:])
                    else:
                        description = " ".join(parts[d_index+1:t_index])
                        title = " ".join(parts[t_index+1:])
                else:
                    title = " ".join(parts[t_index+1:])
            elif "-d" in parts:
                d_index = parts.index("-d")
                description = " ".join(parts[d_index+1:])

            args = AdvancedArgs(id=task_id, title=title, description=description)
            update_command(self.task_manager, args)
            self.console.print()
        except ValueError:
            self.console.print("[red][ERROR] Invalid task ID[/]\n")

    def _handle_delete(self, parts):
        """Handle delete command."""
        if len(parts) < 2:
            self.console.print("[red][ERROR] Task ID required[/] Usage: [yellow]delete <id>[/]\n")
            return

        try:
            task_id = int(parts[1])
            args = AdvancedArgs(id=task_id)
            delete_command(self.task_manager, args)
            self.console.print()
        except ValueError:
            self.console.print("[red][ERROR] Invalid task ID[/]\n")

    def run(self):
        """Run the interactive CLI."""
        self.show_welcome()

        while self.running:
            try:
                user_input = self.console.input("[bold cyan]todo>[/] ").strip()
                self.handle_command(user_input)
            except KeyboardInterrupt:
                self.console.print("\n[cyan]👋 Goodbye![/]")
                break
            except EOFError:
                break


def main():
    """Entry point for advanced interactive CLI."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
