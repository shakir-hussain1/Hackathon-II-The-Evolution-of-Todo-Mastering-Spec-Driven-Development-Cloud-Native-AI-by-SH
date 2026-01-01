"""Integration tests for CLI command handlers."""

import pytest
import json
from io import StringIO
import sys
from src.services.task_manager import TaskManager
from src.cli.commands import (
    add_command,
    list_command,
    update_command,
    delete_command,
    complete_command,
    incomplete_command,
)


class MockArgs:
    """Mock argparse Namespace for testing."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def capture_output(func, *args, **kwargs):
    """Capture stdout from function execution."""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return output


class TestAddCommand:
    """Test add_command CLI handler."""

    def test_add_command_creates_task(self):
        """add_command should create task and confirm with message."""
        tm = TaskManager()
        args = MockArgs(title="Buy groceries", description="")
        output = capture_output(add_command, tm, args)

        assert "Task 1 added: Buy groceries" in output
        assert tm.get_task(1) is not None

    def test_add_command_with_description(self):
        """add_command should accept description parameter."""
        tm = TaskManager()
        args = MockArgs(title="Call mom", description="This weekend")
        output = capture_output(add_command, tm, args)

        assert "Task 1 added: Call mom" in output
        task = tm.get_task(1)
        assert task.description == "This weekend"

    def test_add_command_empty_title_rejected(self):
        """add_command should reject empty title."""
        tm = TaskManager()
        args = MockArgs(title="", description="")
        output = capture_output(add_command, tm, args)

        assert "Error: Title is required" in output
        assert len(tm.list_tasks()) == 0

    def test_add_command_whitespace_title_rejected(self):
        """add_command should reject whitespace-only title."""
        tm = TaskManager()
        args = MockArgs(title="   ", description="")
        output = capture_output(add_command, tm, args)

        assert "Error: Title is required" in output
        assert len(tm.list_tasks()) == 0


class TestListCommand:
    """Test list_command CLI handler."""

    def test_list_command_human_format(self):
        """list_command should display tasks in human-readable format."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "1. [ ] Task 1" in output
        assert "2. [ ] Task 2" in output

    def test_list_command_json_format(self):
        """list_command should output valid JSON when format='json'."""
        tm = TaskManager()
        tm.add_task("Task 1", "Description 1")
        tm.add_task("Task 2")

        args = MockArgs(format="json")
        output = capture_output(list_command, tm, args)

        data = json.loads(output)
        assert "tasks" in data
        assert len(data["tasks"]) == 2
        assert data["tasks"][0]["title"] == "Task 1"
        assert data["tasks"][0]["description"] == "Description 1"
        assert data["tasks"][0]["status"] == "incomplete"

    def test_list_command_empty_list(self):
        """list_command should show 'No tasks' when list is empty."""
        tm = TaskManager()

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "No tasks" in output

    def test_list_command_default_format_human(self):
        """list_command without format attribute should default to human format."""
        tm = TaskManager()
        tm.add_task("Task 1")

        args = MockArgs()
        # Don't set format attribute
        output = capture_output(list_command, tm, args)

        assert "1. [ ] Task 1" in output


class TestUpdateCommand:
    """Test update_command CLI handler."""

    def test_update_command_changes_title(self):
        """update_command should update task title."""
        tm = TaskManager()
        tm.add_task("Old title")

        args = MockArgs(id=1, title="New title", description=None)
        output = capture_output(update_command, tm, args)

        assert "Task 1 updated: New title" in output
        assert tm.get_task(1).title == "New title"

    def test_update_command_invalid_id_format(self):
        """update_command should reject non-numeric ID."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id="invalid", title="New", description=None)
        output = capture_output(update_command, tm, args)

        assert "Error: Invalid ID format" in output

    def test_update_command_nonexistent_id(self):
        """update_command should show available IDs when task not found."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        args = MockArgs(id=999, title="New", description=None)
        output = capture_output(update_command, tm, args)

        assert "Error: Task ID 999 not found" in output
        assert "1" in output or "2" in output

    def test_update_command_requires_title_or_description(self):
        """update_command should require at least title or description."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id=1, title=None, description=None)
        output = capture_output(update_command, tm, args)

        assert "Error: At least one of --title or --description must be provided" in output

    def test_update_command_rejects_empty_title(self):
        """update_command should reject empty title."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id=1, title="", description=None)
        output = capture_output(update_command, tm, args)

        assert "Error: Title cannot be empty" in output


class TestDeleteCommand:
    """Test delete_command CLI handler."""

    def test_delete_command_removes_task(self):
        """delete_command should remove task and confirm."""
        tm = TaskManager()
        tm.add_task("Task to delete")

        args = MockArgs(id=1)
        output = capture_output(delete_command, tm, args)

        assert "Task 1 deleted" in output
        assert tm.get_task(1) is None

    def test_delete_command_invalid_id_format(self):
        """delete_command should reject non-numeric ID."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id="invalid")
        output = capture_output(delete_command, tm, args)

        assert "Error: Invalid ID format" in output

    def test_delete_command_nonexistent_id(self):
        """delete_command should show available IDs when task not found."""
        tm = TaskManager()
        tm.add_task("Task 1")

        args = MockArgs(id=999)
        output = capture_output(delete_command, tm, args)

        assert "Error: Task ID 999 not found" in output


class TestCompleteCommand:
    """Test complete_command CLI handler."""

    def test_complete_command_marks_complete(self):
        """complete_command should mark task as complete."""
        tm = TaskManager()
        tm.add_task("Task to complete")

        args = MockArgs(id=1)
        output = capture_output(complete_command, tm, args)

        assert "Task 1 marked complete: Task to complete" in output
        assert tm.get_task(1).status.value == "complete"

    def test_complete_command_invalid_id_format(self):
        """complete_command should reject non-numeric ID."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id="invalid")
        output = capture_output(complete_command, tm, args)

        assert "Error: Invalid ID format" in output

    def test_complete_command_nonexistent_id(self):
        """complete_command should show available IDs when task not found."""
        tm = TaskManager()
        tm.add_task("Task 1")

        args = MockArgs(id=999)
        output = capture_output(complete_command, tm, args)

        assert "Error: Task ID 999 not found" in output


class TestIncompleteCommand:
    """Test incomplete_command CLI handler."""

    def test_incomplete_command_marks_incomplete(self):
        """incomplete_command should mark complete task as incomplete."""
        tm = TaskManager()
        task = tm.add_task("Task")
        tm.toggle_task_status(1)  # Mark complete

        args = MockArgs(id=1)
        output = capture_output(incomplete_command, tm, args)

        assert "Task 1 marked incomplete: Task" in output
        assert tm.get_task(1).status.value == "incomplete"

    def test_incomplete_command_invalid_id_format(self):
        """incomplete_command should reject non-numeric ID."""
        tm = TaskManager()
        tm.add_task("Task")

        args = MockArgs(id="invalid")
        output = capture_output(incomplete_command, tm, args)

        assert "Error: Invalid ID format" in output

    def test_incomplete_command_nonexistent_id(self):
        """incomplete_command should show available IDs when task not found."""
        tm = TaskManager()
        tm.add_task("Task 1")

        args = MockArgs(id=999)
        output = capture_output(incomplete_command, tm, args)

        assert "Error: Task ID 999 not found" in output
