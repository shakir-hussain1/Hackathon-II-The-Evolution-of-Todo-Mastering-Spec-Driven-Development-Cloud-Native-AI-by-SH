"""WebSocket Sync Service - Real-time task synchronization"""

import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dapr.ext.fastapi import DaprApp
from .connection_manager import ConnectionManager
from .routes.subscriptions import subscriptions_router

APP_NAME = "websocket-sync-service"
APP_VERSION = "5.0.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Real-time WebSocket synchronization service"
)

dapr_app = DaprApp(app)

# Connection manager for WebSocket connections
manager = ConnectionManager()

app.include_router(subscriptions_router, prefix="/subscriptions", tags=["subscriptions"])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    """
    WebSocket endpoint for real-time task updates
    Query param: token (JWT token for authentication)
    """
    # TODO: Validate JWT token and extract user_id
    user_id = "temp-user-id"  # Extract from token

    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive with ping/pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": APP_NAME, "active_connections": manager.get_connection_count()}

@app.get("/ready")
async def ready():
    return {"status": "ready", "service": APP_NAME}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "8004"))
    uvicorn.run(app, host="0.0.0.0", port=port)
