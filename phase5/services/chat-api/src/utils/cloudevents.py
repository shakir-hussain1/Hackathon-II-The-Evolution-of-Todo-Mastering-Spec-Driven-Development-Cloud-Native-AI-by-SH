"""CloudEvents schema validation and creation utilities"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional


def create_cloudevent(
    event_type: str,
    source: str,
    data: Dict[str, Any],
    subject: Optional[str] = None,
    data_content_type: str = "application/json"
) -> Dict[str, Any]:
    """
    Create a CloudEvents 1.0 compliant event

    Spec: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md
    """
    event = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "type": event_type,
        "source": source,
        "time": datetime.utcnow().isoformat() + "Z",
        "datacontenttype": data_content_type,
        "data": data
    }

    if subject:
        event["subject"] = subject

    return event


def validate_cloudevent(event: Dict[str, Any]) -> bool:
    """
    Validate CloudEvents 1.0 required fields

    Required: specversion, id, type, source
    """
    required_fields = ["specversion", "id", "type", "source"]

    for field in required_fields:
        if field not in event:
            print(f"CloudEvent missing required field: {field}")
            return False

    if event["specversion"] != "1.0":
        print(f"Unsupported CloudEvents version: {event['specversion']}")
        return False

    return True


def extract_correlation_id(event: Dict[str, Any]) -> Optional[str]:
    """Extract correlation ID from CloudEvent metadata or generate new one"""
    # Check for correlation ID in extensions
    if "correlationid" in event:
        return event["correlationid"]

    # Check in data
    if "data" in event and isinstance(event["data"], dict):
        if "correlation_id" in event["data"]:
            return event["data"]["correlation_id"]

    # Return event ID as fallback
    return event.get("id")
