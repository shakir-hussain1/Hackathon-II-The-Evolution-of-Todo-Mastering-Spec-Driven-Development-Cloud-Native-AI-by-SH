"""Chat routes for AI-powered task management"""

import os
import uuid
import json
from typing import List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from openai import AsyncOpenAI
from ..database import get_db
from ..services.task_service import TaskService
from ..schemas.chat import ChatRequest, ChatResponse, ChatAction
from ..schemas.task import TaskCreate
from ..middleware.auth import get_current_user
from ..models.user import User
from ..utils.dapr_client import get_dapr_client, DaprClientWrapper
from ..utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# System prompt for AI assistant
SYSTEM_PROMPT = """You are an AI assistant for a todo management application. Your role is to help users manage their tasks through natural language.

You can:
1. Create new tasks with titles, descriptions, priorities, due dates, and tags
2. Search for existing tasks
3. Answer questions about task management

When creating tasks:
- Extract the task title from the user's message
- Identify priority (high, medium, low) if mentioned
- Parse due dates in natural language (e.g., "tomorrow", "next Friday", "in 2 days")
- Extract tags from context (e.g., "work", "personal", "urgent")

Respond in a friendly, helpful manner. When you create or search for tasks, explain what you did.

IMPORTANT: You can only respond with text and ONE function call per message. Format your function calls as JSON with this structure:
{
  "function": "create_task" | "search_tasks",
  "parameters": {...}
}

For create_task:
{
  "function": "create_task",
  "parameters": {
    "title": "Task title",
    "description": "Optional description",
    "priority": "medium",
    "due_date": "2026-02-10T15:00:00Z",
    "tags": ["work", "urgent"]
  }
}

For search_tasks:
{
  "function": "search_tasks",
  "parameters": {
    "query": "search terms"
  }
}
"""


async def parse_ai_response(response_text: str) -> tuple[str, Dict[str, Any] | None]:
    """Parse AI response to extract text and function call"""
    # Try to find JSON function call in response
    try:
        # Look for JSON blocks
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            function_call = json.loads(json_str)

            # Extract text (everything except the JSON)
            text_response = response_text[:start_idx].strip() + response_text[end_idx:].strip()
            text_response = text_response.strip()

            return text_response, function_call
    except json.JSONDecodeError:
        pass

    return response_text, None


async def execute_function_call(
    function_call: Dict[str, Any],
    user: User,
    task_service: TaskService
) -> tuple[List[ChatAction], str]:
    """Execute function call and return actions and result description"""
    actions = []
    result_text = ""

    function_name = function_call.get("function")
    parameters = function_call.get("parameters", {})

    if function_name == "create_task":
        # Create task
        try:
            # Parse due_date if present
            due_date = parameters.get("due_date")
            if due_date and isinstance(due_date, str):
                try:
                    due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                except ValueError:
                    due_date = None

            task_data = TaskCreate(
                title=parameters.get("title", "New Task"),
                description=parameters.get("description"),
                priority=parameters.get("priority", "medium"),
                due_date=due_date,
                tags=parameters.get("tags", [])
            )

            task = await task_service.create_task(user, task_data)

            actions.append(ChatAction(
                type="task_created",
                task_id=str(task.id),
                details={
                    "title": task.title,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "tags": task.tags
                }
            ))

            result_text = f"Created task: {task.title}"
            logger.info(f"AI created task {task.id} for user {user.id}")

        except Exception as e:
            logger.error(f"Error creating task via AI: {e}")
            result_text = f"Error creating task: {str(e)}"

    elif function_name == "search_tasks":
        # Search tasks
        try:
            query = parameters.get("query", "")
            tasks = task_service.search_tasks(user, query, limit=10)

            actions.append(ChatAction(
                type="search_performed",
                details={
                    "query": query,
                    "results_count": len(tasks),
                    "tasks": [
                        {
                            "id": str(task.id),
                            "title": task.title,
                            "status": task.status,
                            "priority": task.priority
                        }
                        for task in tasks
                    ]
                }
            ))

            if tasks:
                result_text = f"Found {len(tasks)} task(s) matching '{query}'"
            else:
                result_text = f"No tasks found matching '{query}'"

            logger.info(f"AI searched tasks for user {user.id}: {query}")

        except Exception as e:
            logger.error(f"Error searching tasks via AI: {e}")
            result_text = f"Error searching tasks: {str(e)}"

    return actions, result_text


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    dapr_client: DaprClientWrapper = Depends(get_dapr_client)
):
    """
    Send a message to the AI chat assistant.

    The AI assistant can:
    - Create tasks from natural language
    - Search for existing tasks
    - Answer questions about task management

    **Examples:**
    - "Create a task to review the budget report by next Friday"
    - "Add a high priority task for the team meeting tomorrow"
    - "Find all tasks tagged with 'work'"
    - "What tasks do I have due this week?"

    **Parameters:**
    - message: Your message to the AI assistant
    - conversation_id: Optional ID to maintain conversation context
    """
    task_service = TaskService(db, dapr_client)

    # Generate conversation ID if not provided
    conversation_id = request.conversation_id or str(uuid.uuid4())

    try:
        # Call OpenAI API
        completion = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=500
        )

        ai_response = completion.choices[0].message.content

        # Parse response for function calls
        text_response, function_call = await parse_ai_response(ai_response)

        actions = []

        # Execute function call if present
        if function_call:
            function_actions, result_text = await execute_function_call(
                function_call,
                current_user,
                task_service
            )
            actions.extend(function_actions)

            # Append result to response if text is empty
            if not text_response:
                text_response = result_text

        # Default response if empty
        if not text_response:
            text_response = "I'm here to help you manage your tasks. You can ask me to create tasks, search for tasks, or answer questions about task management."

        logger.info(f"Chat request processed for user {current_user.id}: {len(actions)} actions")

        return ChatResponse(
            response=text_response,
            actions=actions,
            conversation_id=conversation_id
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )
