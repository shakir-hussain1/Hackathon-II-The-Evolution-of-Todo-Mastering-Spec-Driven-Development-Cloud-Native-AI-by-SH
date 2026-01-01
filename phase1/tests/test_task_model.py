"""Unit tests for Task model."""

import pytest
from datetime import datetime, timezone
from src.models.task import Task, TaskStatus


class TestTaskCreation:
    """Test Task model creation and factory method."""

    def test_task_create_with_title_only(self):
        """Task.create() should create task with title, default description, and INCOMPLETE status."""
        task = Task.create("Buy groceries", auto_id=1)

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.status == TaskStatus.INCOMPLETE
        assert isinstance(task.created_at, datetime)

    def test_task_create_with_title_and_description(self):
        """Task.create() should accept optional description parameter."""
        task = Task.create("Call mom", "This weekend", auto_id=2)

        assert task.id == 2
        assert task.title == "Call mom"
        assert task.description == "This weekend"
        assert task.status == TaskStatus.INCOMPLETE

    def test_task_create_preserves_timezone_utc(self):
        """Task.create() should set created_at in UTC timezone."""
        task = Task.create("Test task", auto_id=1)

        assert task.created_at.tzinfo == timezone.utc

    def test_task_is_immutable(self):
        """Task dataclass should be frozen (immutable)."""
        task = Task.create("Immutable test", auto_id=1)

        with pytest.raises(AttributeError):
            task.title = "Changed title"

    def test_task_equality_compares_all_fields(self):
        """Two Task objects with same fields should be equal."""
        now = datetime.now(timezone.utc)
        task1 = Task(id=1, title="Test", description="", status=TaskStatus.INCOMPLETE, created_at=now)
        task2 = Task(id=1, title="Test", description="", status=TaskStatus.INCOMPLETE, created_at=now)

        assert task1 == task2

    def test_task_string_representation_incomplete(self):
        """Task.__str__() should display title with incomplete indicator [ ]."""
        task = Task.create("Buy groceries", auto_id=1)

        assert str(task) == "1. [ ] Buy groceries"

    def test_task_string_representation_complete(self):
        """Task.__str__() should display title with complete indicator [x]."""
        now = datetime.now(timezone.utc)
        task = Task(id=1, title="Buy groceries", description="", status=TaskStatus.COMPLETE, created_at=now)

        assert str(task) == "1. [x] Buy groceries"


class TestTaskStatus:
    """Test TaskStatus enum."""

    def test_taskstatus_incomplete_value(self):
        """TaskStatus.INCOMPLETE should have value 'incomplete'."""
        assert TaskStatus.INCOMPLETE.value == "incomplete"

    def test_taskstatus_complete_value(self):
        """TaskStatus.COMPLETE should have value 'complete'."""
        assert TaskStatus.COMPLETE.value == "complete"
