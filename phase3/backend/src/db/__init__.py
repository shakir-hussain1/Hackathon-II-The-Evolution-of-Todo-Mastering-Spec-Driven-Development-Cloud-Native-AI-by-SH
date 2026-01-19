"""Database package for Phase III Todo Chatbot."""
from .connection import get_session, init_db, close_db
from .operations import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    complete_task,
    delete_task,
    get_or_create_conversation,
    load_conversation_history,
    save_user_message,
    save_assistant_message,
)

__all__ = [
    "get_session",
    "init_db",
    "close_db",
    "create_task",
    "get_tasks",
    "get_task_by_id",
    "update_task",
    "complete_task",
    "delete_task",
    "get_or_create_conversation",
    "load_conversation_history",
    "save_user_message",
    "save_assistant_message",
]
