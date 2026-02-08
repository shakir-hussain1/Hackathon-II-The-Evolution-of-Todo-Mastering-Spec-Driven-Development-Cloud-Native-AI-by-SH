"""Dapr client wrapper for Pub/Sub, State Store, and Secrets"""

import os
import json
import httpx
from typing import Any, Dict, Optional
from datetime import datetime


class DaprClientWrapper:
    """Wrapper around Dapr HTTP API for simplified service interaction"""

    def __init__(self, dapr_port: int = 3500):
        self.dapr_port = dapr_port
        self.base_url = f"http://localhost:{dapr_port}/v1.0"
        self.app_id = os.getenv("DAPR_APP_ID", "chat-api")

    async def publish_event(
        self,
        pubsub_name: str,
        topic: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """Publish event to Kafka via Dapr Pub/Sub"""
        url = f"{self.base_url}/publish/{pubsub_name}/{topic}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    params=metadata or {},
                    timeout=10.0
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            print(f"Failed to publish event to {topic}: {e}")
            return False

    async def get_state(
        self,
        store_name: str,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Get state from Dapr State Store"""
        url = f"{self.base_url}/state/{store_name}/{key}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=metadata or {}, timeout=5.0)
                response.raise_for_status()

                if response.status_code == 204:  # No content
                    return None

                return response.json()
        except httpx.HTTPError as e:
            print(f"Failed to get state for key {key}: {e}")
            return None

    async def save_state(
        self,
        store_name: str,
        key: str,
        value: Dict[str, Any],
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """Save state to Dapr State Store"""
        url = f"{self.base_url}/state/{store_name}"

        state_data = [{
            "key": key,
            "value": value,
            "metadata": metadata or {}
        }]

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=state_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5.0
                )
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            print(f"Failed to save state for key {key}: {e}")
            return False

    async def delete_state(
        self,
        store_name: str,
        key: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> bool:
        """Delete state from Dapr State Store"""
        url = f"{self.base_url}/state/{store_name}/{key}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url, params=metadata or {}, timeout=5.0)
                response.raise_for_status()
                return True
        except httpx.HTTPError as e:
            print(f"Failed to delete state for key {key}: {e}")
            return False

    async def get_secret(
        self,
        secret_store: str,
        secret_name: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, str]]:
        """Get secret from Dapr Secret Store"""
        url = f"{self.base_url}/secrets/{secret_store}/{secret_name}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=metadata or {}, timeout=5.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Failed to get secret {secret_name}: {e}")
            return None

    async def invoke_service(
        self,
        app_id: str,
        method_name: str,
        data: Optional[Dict[str, Any]] = None,
        http_verb: str = "POST"
    ) -> Optional[Dict[str, Any]]:
        """Invoke another service via Dapr service invocation"""
        url = f"{self.base_url}/invoke/{app_id}/method/{method_name}"

        try:
            async with httpx.AsyncClient() as client:
                if http_verb.upper() == "GET":
                    response = await client.get(url, timeout=10.0)
                else:
                    response = await client.post(
                        url,
                        json=data or {},
                        headers={"Content-Type": "application/json"},
                        timeout=10.0
                    )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Failed to invoke service {app_id}.{method_name}: {e}")
            return None
