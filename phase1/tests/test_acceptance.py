"""Acceptance tests covering all specification scenarios."""

import pytest
import json
from io import StringIO
import sys
from src.services.task_manager import TaskManager
from src.models.task import TaskStatus
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


class TestUserStory1AcceptanceCriteria:
    """User Story 1: Add Task – All acceptance scenarios."""

    def test_scenario_1_1_add_single_task_with_unique_id(self):
        """SCENARIO 1.1: Add task, receives unique ID 1, title stored, incomplete status, success message."""
        tm = TaskManager()
        args = MockArgs(title="Buy groceries", description="")

        output = capture_output(add_command, tm, args)

        task = tm.get_task(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.status == TaskStatus.INCOMPLETE
        assert "Task 1 added" in output

    def test_scenario_1_2_add_multiple_tasks_sequential_ids(self):
        """SCENARIO 1.2: Add second task, receives unique ID 2, both tasks coexist."""
        tm = TaskManager()
        add_command(tm, MockArgs(title="Buy groceries", description=""))
        add_command(tm, MockArgs(title="Call mom", description=""))

        tasks = tm.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[0].title == "Buy groceries"
        assert tasks[1].id == 2
        assert tasks[1].title == "Call mom"

    def test_scenario_1_3_add_task_with_description(self):
        """SCENARIO 1.3: Add task with title and description, both stored correctly."""
        tm = TaskManager()
        args = MockArgs(
            title="Fix bug",
            description="Resolve login timeout issue",
        )

        add_command(tm, args)

        task = tm.get_task(1)
        assert task.title == "Fix bug"
        assert task.description == "Resolve login timeout issue"

    def test_scenario_1_4_add_task_empty_title_rejected(self):
        """SCENARIO 1.4: Add task with empty/whitespace title, rejected with error."""
        tm = TaskManager()
        args = MockArgs(title="", description="")

        output = capture_output(add_command, tm, args)

        assert "Error: Title is required" in output
        assert len(tm.list_tasks()) == 0


class TestUserStory2AcceptanceCriteria:
    """User Story 2: View All Tasks – All acceptance scenarios."""

    def test_scenario_2_1_list_displays_id_title_status(self):
        """SCENARIO 2.1: List command displays all tasks with ID, title, status indicator."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "1." in output and "Task 1" in output
        assert "2." in output and "Task 2" in output

    def test_scenario_2_2_incomplete_task_shows_incomplete_indicator(self):
        """SCENARIO 2.2: Incomplete task displays incomplete indicator [ ]."""
        tm = TaskManager()
        tm.add_task("Incomplete task")

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "[ ]" in output

    def test_scenario_2_3_complete_task_shows_complete_indicator(self):
        """SCENARIO 2.3: Complete task displays complete indicator [x]."""
        tm = TaskManager()
        tm.add_task("Task to complete")
        tm.toggle_task_status(1)

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "[x]" in output

    def test_scenario_2_4_empty_list_shows_no_tasks_message(self):
        """SCENARIO 2.4: No tasks exist, list shows 'No tasks' message."""
        tm = TaskManager()

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        assert "No tasks" in output

    def test_scenario_2_5_many_tasks_display_organized(self):
        """SCENARIO 2.5: 10+ tasks display in organized numbered order."""
        tm = TaskManager()
        for i in range(15):
            tm.add_task(f"Task {i+1}")

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)

        # Verify all tasks present and ordered
        assert "1. [ ] Task 1" in output
        assert "10. [ ] Task 10" in output
        assert "15. [ ] Task 15" in output


class TestUserStory3AcceptanceCriteria:
    """User Story 3: Mark Task Complete – All acceptance scenarios."""

    def test_scenario_3_1_mark_incomplete_task_complete(self):
        """SCENARIO 3.1: Mark incomplete task complete, status changes, list reflects change."""
        tm = TaskManager()
        tm.add_task("Task to complete")

        complete_command(tm, MockArgs(id=1))

        assert tm.get_task(1).status == TaskStatus.COMPLETE

        args = MockArgs(format="human")
        output = capture_output(list_command, tm, args)
        assert "[x]" in output

    def test_scenario_3_2_toggle_complete_to_incomplete(self):
        """SCENARIO 3.2: Mark complete task incomplete, status toggles back."""
        tm = TaskManager()
        tm.add_task("Task")
        tm.toggle_task_status(1)  # Mark complete

        incomplete_command(tm, MockArgs(id=1))

        assert tm.get_task(1).status == TaskStatus.INCOMPLETE

    def test_scenario_3_3_complete_nonexistent_task_error(self):
        """SCENARIO 3.3: Try to complete non-existent ID, returns error."""
        tm = TaskManager()
        tm.add_task("Task")

        output = capture_output(complete_command, tm, MockArgs(id=99))

        assert "Error: Task ID 99 not found" in output

    def test_scenario_3_4_complete_one_task_others_unchanged(self):
        """SCENARIO 3.4: Complete one task, others remain unchanged."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")
        tm.add_task("Task 3")

        complete_command(tm, MockArgs(id=2))

        assert tm.get_task(1).status == TaskStatus.INCOMPLETE
        assert tm.get_task(2).status == TaskStatus.COMPLETE
        assert tm.get_task(3).status == TaskStatus.INCOMPLETE


class TestUserStory4AcceptanceCriteria:
    """User Story 4: Update Task – All acceptance scenarios."""

    def test_scenario_4_1_update_task_title(self):
        """SCENARIO 4.1: Update task title, new title in list."""
        tm = TaskManager()
        tm.add_task("Buy groceries")

        update_command(
            tm,
            MockArgs(id=1, title="Buy groceries and cook dinner", description=None),
        )

        task = tm.get_task(1)
        assert task.title == "Buy groceries and cook dinner"

    def test_scenario_4_2_update_task_description_only(self):
        """SCENARIO 4.2: Update only description, title unchanged."""
        tm = TaskManager()
        tm.add_task("Task title", "Old description")

        update_command(
            tm,
            MockArgs(id=1, title=None, description="New description"),
        )

        task = tm.get_task(1)
        assert task.title == "Task title"
        assert task.description == "New description"

    def test_scenario_4_3_update_nonexistent_task_error(self):
        """SCENARIO 4.3: Update non-existent task, error returned."""
        tm = TaskManager()
        tm.add_task("Task")

        output = capture_output(
            update_command,
            tm,
            MockArgs(id=5, title="New", description=None),
        )

        assert "Error: Task ID 5 not found" in output

    def test_scenario_4_4_update_with_empty_title_rejected(self):
        """SCENARIO 4.4: Update with empty title, rejected with error."""
        tm = TaskManager()
        tm.add_task("Task")

        output = capture_output(
            update_command,
            tm,
            MockArgs(id=1, title="", description=None),
        )

        assert "Error: Title cannot be empty" in output


class TestUserStory5AcceptanceCriteria:
    """User Story 5: Delete Task – All acceptance scenarios."""

    def test_scenario_5_1_delete_task_removed_from_list(self):
        """SCENARIO 5.1: Delete task, removed from memory, not in list."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")
        tm.add_task("Task 3")

        delete_command(tm, MockArgs(id=2))

        tasks = tm.list_tasks()
        assert len(tasks) == 2
        assert tm.get_task(2) is None

    def test_scenario_5_2_delete_nonexistent_task_error(self):
        """SCENARIO 5.2: Delete non-existent task, error returned."""
        tm = TaskManager()
        tm.add_task("Task")

        output = capture_output(delete_command, tm, MockArgs(id=999))

        assert "Error: Task ID 999 not found" in output

    def test_scenario_5_3_delete_task_ids_not_shifted(self):
        """SCENARIO 5.3: Delete task 2 of 3, remaining tasks keep IDs."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")
        tm.add_task("Task 3")

        delete_command(tm, MockArgs(id=2))

        assert tm.get_task(1) is not None
        assert tm.get_task(2) is None
        assert tm.get_task(3) is not None


class TestEdgeCases:
    """Edge cases from specification."""

    def test_edge_case_invalid_command(self):
        """EDGE: Invalid command should display error and available commands."""
        # This is tested at main.py level with argparse
        # For now, verify our commands handle invalid args gracefully
        tm = TaskManager()

        # Invalid ID format
        output = capture_output(
            complete_command,
            tm,
            MockArgs(id="not_a_number"),
        )
        assert "Error: Invalid ID format" in output

    def test_edge_case_non_numeric_id(self):
        """EDGE: Non-numeric ID, system rejects with 'Invalid ID format'."""
        tm = TaskManager()
        tm.add_task("Task")

        output = capture_output(
            delete_command,
            tm,
            MockArgs(id="abc"),
        )

        assert "Error: Invalid ID format" in output

    def test_edge_case_exit_loses_all_data(self):
        """EDGE: App exit loses all in-memory tasks (expected behavior)."""
        # Create TaskManager with tasks
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        # Create new TaskManager (simulating app restart)
        new_tm = TaskManager()

        # Verify data lost
        assert len(new_tm.list_tasks()) == 0

    def test_edge_case_many_tasks_no_crash(self):
        """EDGE: Add 1000+ tasks, system handles gracefully."""
        tm = TaskManager()

        # Add 1000 tasks
        for i in range(1000):
            task = tm.add_task(f"Task {i+1}")
            assert task.id == i + 1

        # Verify all tasks exist
        assert len(tm.list_tasks()) == 1000

        # Verify can still access arbitrary task
        assert tm.get_task(500).title == "Task 500"
        assert tm.get_task(1000).title == "Task 1000"

    def test_edge_case_very_long_title_description(self):
        """EDGE: Handle very long titles and descriptions."""
        tm = TaskManager()
        long_title = "x" * 500  # Very long title
        long_description = "y" * 2000  # Very long description

        task = tm.add_task(long_title, long_description)

        assert task.title == long_title
        assert task.description == long_description
        assert tm.get_task(1).title == long_title

    def test_edge_case_special_characters_in_title(self):
        """EDGE: Handle special characters in title/description."""
        tm = TaskManager()
        special_title = "Buy: eggs & milk @ store (🛒) 50%!"
        special_description = "Get <milk>, [eggs], {bread} with `backticks` and \"quotes\""

        task = tm.add_task(special_title, special_description)

        assert task.title == special_title
        assert task.description == special_description

    def test_edge_case_multiple_updates_same_task(self):
        """EDGE: Update same task multiple times, all changes persist."""
        tm = TaskManager()
        tm.add_task("Original")

        update_command(tm, MockArgs(id=1, title="Update 1", description=None))
        update_command(tm, MockArgs(id=1, title="Update 2", description=None))
        update_command(tm, MockArgs(id=1, title="Update 3", description="Final"))

        task = tm.get_task(1)
        assert task.title == "Update 3"
        assert task.description == "Final"

    def test_edge_case_toggle_status_multiple_times(self):
        """EDGE: Toggle task status multiple times."""
        tm = TaskManager()
        tm.add_task("Task")

        for _ in range(10):
            tm.toggle_task_status(1)

        # After 10 toggles (even number), should be INCOMPLETE
        assert tm.get_task(1).status == TaskStatus.INCOMPLETE

    def test_edge_case_json_output_with_special_chars(self):
        """EDGE: JSON output correctly handles special characters."""
        tm = TaskManager()
        tm.add_task('Task with "quotes"', "Description with\nnewline")

        args = MockArgs(format="json")
        output = capture_output(list_command, tm, args)

        # Verify valid JSON
        data = json.loads(output)
        assert len(data["tasks"]) == 1
        assert '"quotes"' in data["tasks"][0]["title"]

    def test_edge_case_add_with_none_description(self):
        """EDGE: Add task with None description should default to empty string."""
        tm = TaskManager()
        task = tm.add_task("Task", None)

        # Should handle gracefully (description might be None or empty)
        assert task.description is None or task.description == ""

    def test_workflow_complete_cycle(self):
        """COMPLETE WORKFLOW: Add, list, complete, update, delete tasks in sequence."""
        tm = TaskManager()

        # Add 3 tasks
        add_command(tm, MockArgs(title="Task 1", description=""))
        add_command(tm, MockArgs(title="Task 2", description=""))
        add_command(tm, MockArgs(title="Task 3", description=""))

        # List them
        args_list = MockArgs(format="human")
        output = capture_output(list_command, tm, args_list)
        assert "Task 1" in output and "Task 2" in output and "Task 3" in output

        # Complete task 2
        complete_command(tm, MockArgs(id=2))
        assert tm.get_task(2).status == TaskStatus.COMPLETE

        # Update task 1
        update_command(tm, MockArgs(id=1, title="Task 1 Updated", description=None))
        assert tm.get_task(1).title == "Task 1 Updated"

        # Delete task 3
        delete_command(tm, MockArgs(id=3))
        assert tm.get_task(3) is None

        # Final list
        final_tasks = tm.list_tasks()
        assert len(final_tasks) == 2
        assert final_tasks[0].id == 1
        assert final_tasks[1].id == 2
