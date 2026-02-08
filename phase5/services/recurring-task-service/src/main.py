"""Recurring Task Service - Generates recurring task instances"""

import os
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
from .routes.bindings import bindings_router

APP_NAME = "recurring-task-service"
APP_VERSION = "5.0.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Recurring task generation service"
)

dapr_app = DaprApp(app)

app.include_router(bindings_router, prefix="/bindings", tags=["bindings"])

@app.get("/health")
async def health():
    return {"status": "healthy", "service": APP_NAME}

@app.get("/ready")
async def ready():
    return {"status": "ready", "service": APP_NAME}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
