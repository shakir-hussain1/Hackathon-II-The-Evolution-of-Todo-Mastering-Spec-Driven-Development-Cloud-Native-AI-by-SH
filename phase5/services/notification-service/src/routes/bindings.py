"""Dapr input binding handlers for cron-reminders"""

from fastapi import APIRouter, Request
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
bindings_router = APIRouter()


@bindings_router.post("/cron-reminders")
async def handle_cron_reminders(request: Request):
    """
    Dapr input binding handler for cron-reminders
    Triggered every minute to check and send pending reminders
    """
    logger.info("Cron reminder check triggered")

    # TODO: Implementation
    # 1. Query reminders with scheduled_at <= now and status='pending'
    # 2. Send notifications (email/in-app)
    # 3. Update reminder status to 'sent'
    # 4. Publish reminder.sent events

    return {"status": "success", "processed": 0}


@bindings_router.post("/task-events")
async def handle_task_events(request: Request):
    """
    Dapr subscription handler for task-events topic
    Auto-creates reminders when tasks are created with due_date
    """
    data = await request.json()
    logger.info(f"Task event received: {data.get('type')}")

    # TODO: Implementation
    # 1. Parse CloudEvent
    # 2. If task.created with due_date, create reminders (24h, 1h, 0h before due)
    # 3. Store reminders in database
    # 4. Publish reminder.scheduled events

    return {"status": "success"}
