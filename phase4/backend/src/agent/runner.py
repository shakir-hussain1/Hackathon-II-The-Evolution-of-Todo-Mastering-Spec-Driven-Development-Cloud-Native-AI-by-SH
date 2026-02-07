"""
OpenAI Agent runner with MCP tool integration.
Provides stateless agent execution for natural language task management.
"""
from typing import List, Dict, Any, Optional
import json
import logging
import re
from openai import AsyncOpenAI
from sqlmodel.ext.asyncio.session import AsyncSession

from ..config import settings
from ..mcp.tools import MCP_TOOLS
from .prompts import SYSTEM_PROMPT

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def detect_operation_intent(user_message: str) -> tuple[str, str]:
    """
    Detect what operation user wants and extract task reference.

    Returns:
        (operation, task_reference) tuple
        operation: 'complete', 'update', 'delete', 'add', 'list', None
        task_reference: the task name/description
    """
    msg_lower = user_message.lower()

    # Update (check FIRST because it might contain "complete" in the new title)
    if any(word in msg_lower for word in ['update', 'change', 'edit', 'modify', 'rename']):
        # Extract old and new
        patterns = [
            r'change\s+(.+?)\s+to\s+(.+)',
            r'update\s+(.+?)\s+to\s+(.+)',
            r'rename\s+(.+?)\s+to\s+(.+)',
            r'edit\s+(.+?)\s+to\s+(.+)',
            r'modify\s+(.+?)\s+to\s+(.+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, msg_lower)
            if match:
                return ('update', match.group(1).strip() + '|' + match.group(2).strip())
        return ('update', '')

    # Delete (check SECOND)
    if any(word in msg_lower for word in ['delete', 'remove', 'get rid of']):
        patterns = [
            r'delete\s+(.+)',
            r'remove\s+(.+)',
            r'get\s+rid\s+of\s+(.+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, msg_lower)
            if match:
                return ('delete', match.group(1).strip())
        return ('delete', '')

    # Complete (check LAST to avoid conflicts)
    if any(word in msg_lower for word in ['complete', 'done', 'finish', 'mark as done', 'mark as complete']):
        # Extract task reference
        patterns = [
            r'complete\s+(.+)',
            r'mark\s+(.+?)\s+as\s+done',
            r'mark\s+(.+?)\s+as\s+complete',
            r'done\s+with\s+(.+)',
            r'finish\s+(.+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, msg_lower)
            if match:
                return ('complete', match.group(1).strip())
        return ('complete', '')

    return (None, '')


def find_matching_task(tasks: List[Dict], reference: str) -> Optional[str]:
    """Find task ID by matching reference string."""
    if not tasks or not reference:
        return None

    reference_lower = reference.lower().strip()

    # Position references
    if reference_lower in ['first', 'first task', '1st', 'one']:
        return tasks[0]['id'] if tasks else None
    if reference_lower in ['last', 'last task', 'final']:
        return tasks[-1]['id'] if tasks else None

    # Number references
    num_match = re.match(r'(\d+)(st|nd|rd|th)?\s*task?', reference_lower)
    if num_match:
        num = int(num_match.group(1))
        if 1 <= num <= len(tasks):
            return tasks[num - 1]['id']

    # Title matching
    for task in tasks:
        title_lower = task['title'].lower()
        # Exact match
        if reference_lower == title_lower:
            return task['id']
        # Substring match
        if reference_lower in title_lower or title_lower in reference_lower:
            return task['id']

    # Word matching
    ref_words = reference_lower.split()
    for task in tasks:
        title_lower = task['title'].lower()
        if any(word in title_lower for word in ref_words if len(word) > 2):
            return task['id']

    return None


async def run_agent(
    session: AsyncSession,
    user_id: str,
    user_message: str,
    conversation_history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Run OpenAI agent with MCP tool access for task management.
    """
    try:
        # Detect operation intent BEFORE calling agent
        operation, task_reference = detect_operation_intent(user_message)
        logger.info(f"[AGENT] Detected operation: {operation}, reference: {task_reference}")

        # For multi-step operations, handle them directly
        if operation in ['complete', 'update', 'delete']:
            logger.info(f"[AGENT] Multi-step operation detected: {operation}")

            # STEP 1: Get all tasks
            list_result = await MCP_TOOLS['list_tasks'](
                session=session,
                user_id=user_id
            )

            if not list_result.get('success'):
                return {
                    "content": "I couldn't retrieve your tasks. Please try again.",
                    "tool_calls": None,
                    "model": "gpt-4o-mini",
                    "finish_reason": "error"
                }

            tasks = list_result.get('data', [])

            if not tasks:
                return {
                    "content": "You don't have any tasks yet. Add one first!",
                    "tool_calls": {"calls": [{"tool": "list_tasks", "result": list_result}]},
                    "model": "gpt-4o-mini",
                    "finish_reason": "no_tasks"
                }

            # STEP 2: Find matching task
            task_id = find_matching_task(tasks, task_reference)

            if not task_id:
                # Show available tasks
                task_list = "\n".join([f"{i+1}. {t['title']}" for i, t in enumerate(tasks)])
                return {
                    "content": f"I couldn't find a task matching '{task_reference}'. Here are your tasks:\n\n{task_list}\n\nWhich one did you mean?",
                    "tool_calls": {"calls": [{"tool": "list_tasks", "result": list_result}]},
                    "model": "gpt-4o-mini",
                    "finish_reason": "task_not_found"
                }

            # Find the task object
            task = next((t for t in tasks if t['id'] == task_id), None)
            task_title = task['title'] if task else 'the task'

            # STEP 3: Execute the operation
            tool_calls_audit = [{"tool": "list_tasks", "arguments": {}, "result": list_result}]

            if operation == 'complete':
                result = await MCP_TOOLS['complete_task'](
                    session=session,
                    user_id=user_id,
                    task_id=task_id
                )
                tool_calls_audit.append({"tool": "complete_task", "arguments": {"task_id": task_id}, "result": result})

                if result.get('success'):
                    return {
                        "content": f"✅ Done! I've completed '{task_title}'.",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "success"
                    }
                else:
                    return {
                        "content": f"I couldn't complete '{task_title}'. {result.get('message', '')}",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "tool_error"
                    }

            elif operation == 'update':
                # Extract new title from reference
                parts = task_reference.split('|')
                if len(parts) == 2:
                    new_title = parts[1].strip()
                else:
                    new_title = task_reference.strip()

                result = await MCP_TOOLS['update_task'](
                    session=session,
                    user_id=user_id,
                    task_id=task_id,
                    title=new_title
                )
                tool_calls_audit.append({"tool": "update_task", "arguments": {"task_id": task_id, "title": new_title}, "result": result})

                if result.get('success'):
                    return {
                        "content": f"✏️ Updated! I've changed the task to '{new_title}'.",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "success"
                    }
                else:
                    return {
                        "content": f"I couldn't update '{task_title}'. {result.get('message', '')}",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "tool_error"
                    }

            elif operation == 'delete':
                result = await MCP_TOOLS['delete_task'](
                    session=session,
                    user_id=user_id,
                    task_id=task_id
                )
                tool_calls_audit.append({"tool": "delete_task", "arguments": {"task_id": task_id}, "result": result})

                if result.get('success'):
                    return {
                        "content": f"🗑️ Deleted! I've removed '{task_title}' from your list.",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "success"
                    }
                else:
                    return {
                        "content": f"I couldn't delete '{task_title}'. {result.get('message', '')}",
                        "tool_calls": {"calls": tool_calls_audit},
                        "model": "gpt-4o-mini",
                        "finish_reason": "tool_error"
                    }

        # For other operations (add, list), use standard agent flow
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a NEW task. Use when user wants to add/create a task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Optional description"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Get all tasks. Use when user wants to see their tasks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["pending", "completed"]}
                        }
                    }
                }
            }
        ]

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=1000
        )

        message = response.choices[0].message
        tool_calls_audit = []

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in MCP_TOOLS:
                    tool_result = await MCP_TOOLS[function_name](
                        session=session,
                        user_id=user_id,
                        **function_args
                    )

                    tool_calls_audit.append({
                        "tool": function_name,
                        "arguments": function_args,
                        "result": tool_result
                    })

                    if not tool_result.get("success"):
                        return {
                            "content": f"Error: {tool_result.get('message', 'Unknown error')}",
                            "tool_calls": {"calls": tool_calls_audit},
                            "model": response.model,
                            "finish_reason": "tool_error"
                        }

            # Get natural language response
            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    }
                    for tc in message.tool_calls
                ]
            })

            for i, tool_call in enumerate(message.tool_calls):
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_calls_audit[i]["result"])
                })

            followup = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )

            return {
                "content": followup.choices[0].message.content,
                "tool_calls": {"calls": tool_calls_audit},
                "model": followup.model,
                "finish_reason": followup.choices[0].finish_reason
            }

        return {
            "content": message.content or "I'm ready to help with your tasks!",
            "tool_calls": None,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason
        }

    except Exception as e:
        logger.error(f"[AGENT] ERROR: {str(e)}", exc_info=True)
        return {
            "content": f"I'm sorry, I encountered an error: {str(e)}",
            "tool_calls": None,
            "model": "error",
            "finish_reason": "error"
        }
