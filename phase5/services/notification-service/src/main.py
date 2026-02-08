"""Notification Service - Handles reminders and notifications"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dapr.ext.fastapi import DaprApp
from .routes.bindings import bindings_router
from .routes.health import health_router

APP_NAME = "notification-service"
APP_VERSION = "5.0.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Reminder and notification service"
)

# Initialize Dapr
dapr_app = DaprApp(app)

# Register routes
app.include_router(bindings_router, prefix="/bindings", tags=["bindings"])
app.include_router(health_router, tags=["health"])

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "service": APP_NAME}

@app.get("/ready")
async def ready():
    return {"status": "ready", "service": APP_NAME}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
