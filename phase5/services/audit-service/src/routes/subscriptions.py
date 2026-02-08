"""Dapr subscription handlers for all topics"""

from fastapi import APIRouter, Request
import logging

logger = logging.getLogger(__name__)
subscriptions_router = APIRouter()


@subscriptions_router.post("/all-events")
async def handle_all_events(request: Request):
    """
    Subscribe to all Kafka topics (task-events, reminders, task-updates)
    Log every event to audit_logs table
    """
    data = await request.json()
    logger.info(f"Audit event received: {data.get('type')}")

    # TODO: Implementation
    # 1. Parse CloudEvent
    # 2. Extract event_id, event_type, user_id, entity details
    # 3. Check idempotency (event_id uniqueness)
    # 4. Insert into audit_logs table

    return {"status": "success"}
