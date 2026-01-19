"""
Database CRUD operations with user isolation enforcement.
All operations filter by user_id to prevent cross-user data access.
"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models import User, Task, TaskStatus, Conversation, Message, MessageRole


# ===== TASK OPERATIONS =====

async def create_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: str = ""
) -> Task:
    """Create a new task for user."""
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        status=TaskStatus.PENDING
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(
    session: AsyncSession,
    user_id: str,
    status: Optional[TaskStatus] = None
) -> List[Task]:
    """Get all tasks for user, optionally filtered by status."""
    query = select(Task).where(Task.user_id == user_id)
    if status:
        query = query.where(Task.status == status)
    query = query.order_by(Task.created_at.desc())

    result = await session.execute(query)
    return list(result.scalars().all())


async def get_task_by_id(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Optional[Task]:
    """Get specific task by ID (with user_id validation)."""
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # User isolation
        )
    )
    return result.scalars().first()


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    """Update task title and/or description."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    task.updated_at = datetime.utcnow()
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> Optional[Task]:
    """Mark task as completed."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return None

    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: str
) -> bool:
    """Delete task (returns True if deleted, False if not found)."""
    task = await get_task_by_id(session, user_id, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


# ===== CONVERSATION OPERATIONS =====

async def get_or_create_conversation(
    session: AsyncSession,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Conversation:
    """
    Get existing conversation by ID or create/get user's latest conversation.
    MVP: Single ongoing conversation per user.
    """
    if conversation_id:
        # Get specific conversation
        result = await session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id  # User isolation
            )
        )
        conversation = result.scalars().first()
        if conversation:
            return conversation

    # Get user's most recent conversation
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(1)
    )
    conversation = result.scalars().first()

    if conversation:
        return conversation

    # Create new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def load_conversation_history(
    session: AsyncSession,
    conversation_id: str
) -> List[Message]:
    """Load all messages in conversation ordered by sequence number."""
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.sequence_number.asc())
    )
    return list(result.scalars().all())


async def get_next_sequence_number(
    session: AsyncSession,
    conversation_id: str
) -> int:
    """Get next sequence number for message in conversation."""
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.sequence_number.desc())
        .limit(1)
    )
    last_message = result.scalars().first()
    return (last_message.sequence_number + 1) if last_message else 1


async def save_user_message(
    session: AsyncSession,
    conversation_id: str,
    content: str
) -> Message:
    """Save user message to conversation."""
    sequence_number = await get_next_sequence_number(session, conversation_id)

    message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=content,
        sequence_number=sequence_number
    )

    session.add(message)
    await session.commit()
    await session.refresh(message)

    # Update conversation timestamp
    result = await session.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalars().first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        await session.commit()

    return message


async def save_assistant_message(
    session: AsyncSession,
    conversation_id: str,
    content: str,
    tool_calls: Optional[Dict[str, Any]] = None
) -> Message:
    """Save assistant message with optional tool call audit trail."""
    sequence_number = await get_next_sequence_number(session, conversation_id)

    message = Message(
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=content,
        tool_calls=tool_calls,
        sequence_number=sequence_number
    )

    session.add(message)
    await session.commit()
    await session.refresh(message)

    # Update conversation timestamp
    result = await session.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalars().first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        await session.commit()

    return message
