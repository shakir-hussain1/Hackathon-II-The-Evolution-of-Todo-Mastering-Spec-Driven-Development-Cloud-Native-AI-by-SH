"""Unit tests for TaskManager service."""

import pytest
from src.services.task_manager import TaskManager
from src.models.task import Task, TaskStatus


class TestTaskManagerAddTask:
    """Test add_task functionality."""

    def test_add_task_returns_task_with_id(self):
        """add_task() should return Task object with auto-incremented ID."""
        tm = TaskManager()
        task = tm.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_increments_ids_sequentially(self):
        """Multiple add_task() calls should generate sequential IDs."""
        tm = TaskManager()
        task1 = tm.add_task("Task 1")
        task2 = tm.add_task("Task 2")
        task3 = tm.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_description(self):
        """add_task() should accept optional description parameter."""
        tm = TaskManager()
        task = tm.add_task("Call mom", "This weekend")

        assert task.title == "Call mom"
        assert task.description == "This weekend"

    def test_add_task_default_description_empty_string(self):
        """add_task() without description should default to empty string."""
        tm = TaskManager()
        task = tm.add_task("Buy groceries")

        assert task.description == ""


class TestTaskManagerListTasks:
    """Test list_tasks functionality."""

    def test_list_tasks_empty_returns_empty_list(self):
        """list_tasks() on empty TaskManager should return empty list."""
        tm = TaskManager()
        tasks = tm.list_tasks()

        assert tasks == []

    def test_list_tasks_returns_all_tasks(self):
        """list_tasks() should return all added tasks."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")
        tm.add_task("Task 3")

        tasks = tm.list_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_list_tasks_returns_copy_not_reference(self):
        """list_tasks() should return independent copy, not reference to internal list."""
        tm = TaskManager()
        tm.add_task("Original task")

        tasks1 = tm.list_tasks()
        original_length = len(tasks1)

        # Modify returned list
        tasks1.append(Task.create("Fake task", auto_id=999))

        # Verify internal list unchanged
        tasks2 = tm.list_tasks()
        assert len(tasks2) == original_length


class TestTaskManagerGetTask:
    """Test get_task functionality."""

    def test_get_task_returns_task_by_id(self):
        """get_task() should return Task with matching ID."""
        tm = TaskManager()
        task = tm.add_task("Buy groceries")

        retrieved = tm.get_task(1)

        assert retrieved is not None
        assert retrieved.id == 1
        assert retrieved.title == "Buy groceries"

    def test_get_task_nonexistent_returns_none(self):
        """get_task() should return None for non-existent ID."""
        tm = TaskManager()
        tm.add_task("Buy groceries")

        result = tm.get_task(999)

        assert result is None

    def test_get_task_empty_returns_none(self):
        """get_task() on empty TaskManager should return None."""
        tm = TaskManager()

        result = tm.get_task(1)

        assert result is None


class TestTaskManagerUpdateTask:
    """Test update_task functionality."""

    def test_update_task_changes_title(self):
        """update_task() should change task title and return True."""
        tm = TaskManager()
        tm.add_task("Old title")

        success = tm.update_task(1, "New title", None)

        assert success is True
        assert tm.get_task(1).title == "New title"

    def test_update_task_changes_description(self):
        """update_task() should change task description and return True."""
        tm = TaskManager()
        tm.add_task("Task", "Old description")

        success = tm.update_task(1, None, "New description")

        assert success is True
        assert tm.get_task(1).description == "New description"

    def test_update_task_changes_both_fields(self):
        """update_task() should change both title and description if provided."""
        tm = TaskManager()
        tm.add_task("Old title", "Old description")

        success = tm.update_task(1, "New title", "New description")

        assert success is True
        assert tm.get_task(1).title == "New title"
        assert tm.get_task(1).description == "New description"

    def test_update_task_preserves_unchanged_fields(self):
        """update_task() should keep status and created_at unchanged."""
        tm = TaskManager()
        original_task = tm.add_task("Title", "Description")
        original_status = original_task.status
        original_created_at = original_task.created_at

        tm.update_task(1, "New title", None)
        updated_task = tm.get_task(1)

        assert updated_task.status == original_status
        assert updated_task.created_at == original_created_at

    def test_update_task_nonexistent_returns_false(self):
        """update_task() should return False for non-existent ID."""
        tm = TaskManager()
        tm.add_task("Task")

        success = tm.update_task(999, "New title", None)

        assert success is False

    def test_update_task_does_not_affect_other_tasks(self):
        """update_task() should only modify target task."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        tm.update_task(1, "Updated", None)

        assert tm.get_task(1).title == "Updated"
        assert tm.get_task(2).title == "Task 2"


class TestTaskManagerDeleteTask:
    """Test delete_task functionality."""

    def test_delete_task_removes_task(self):
        """delete_task() should remove task and return True."""
        tm = TaskManager()
        tm.add_task("Buy groceries")

        success = tm.delete_task(1)

        assert success is True
        assert tm.get_task(1) is None

    def test_delete_task_nonexistent_returns_false(self):
        """delete_task() should return False for non-existent ID."""
        tm = TaskManager()
        tm.add_task("Task")

        success = tm.delete_task(999)

        assert success is False

    def test_delete_task_does_not_affect_other_tasks(self):
        """delete_task() should only remove target task."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")
        tm.add_task("Task 3")

        tm.delete_task(2)

        assert tm.get_task(1) is not None
        assert tm.get_task(2) is None
        assert tm.get_task(3) is not None

    def test_delete_task_list_length_decreases(self):
        """delete_task() should decrease task list length by 1."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        initial_count = len(tm.list_tasks())
        tm.delete_task(1)
        final_count = len(tm.list_tasks())

        assert final_count == initial_count - 1


class TestTaskManagerToggleStatus:
    """Test toggle_task_status functionality."""

    def test_toggle_task_status_incomplete_to_complete(self):
        """toggle_task_status() should change INCOMPLETE to COMPLETE."""
        tm = TaskManager()
        tm.add_task("Task")

        success = tm.toggle_task_status(1)

        assert success is True
        assert tm.get_task(1).status == TaskStatus.COMPLETE

    def test_toggle_task_status_complete_to_incomplete(self):
        """toggle_task_status() on complete task should change to INCOMPLETE."""
        tm = TaskManager()
        task = tm.add_task("Task")
        tm.toggle_task_status(1)

        # Now toggle again
        success = tm.toggle_task_status(1)

        assert success is True
        assert tm.get_task(1).status == TaskStatus.INCOMPLETE

    def test_toggle_task_status_nonexistent_returns_false(self):
        """toggle_task_status() should return False for non-existent ID."""
        tm = TaskManager()
        tm.add_task("Task")

        success = tm.toggle_task_status(999)

        assert success is False

    def test_toggle_task_status_does_not_affect_other_tasks(self):
        """toggle_task_status() should only modify target task status."""
        tm = TaskManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        tm.toggle_task_status(1)

        assert tm.get_task(1).status == TaskStatus.COMPLETE
        assert tm.get_task(2).status == TaskStatus.INCOMPLETE

    def test_toggle_task_status_preserves_other_fields(self):
        """toggle_task_status() should keep title, description, id, created_at unchanged."""
        tm = TaskManager()
        original_task = tm.add_task("Title", "Description")
        original_title = original_task.title
        original_description = original_task.description
        original_id = original_task.id
        original_created_at = original_task.created_at

        tm.toggle_task_status(1)
        updated_task = tm.get_task(1)

        assert updated_task.title == original_title
        assert updated_task.description == original_description
        assert updated_task.id == original_id
        assert updated_task.created_at == original_created_at
