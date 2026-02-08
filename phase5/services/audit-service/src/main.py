"""Audit Service - Logs all events for compliance and debugging"""

import os
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
from .routes.subscriptions import subscriptions_router
from .routes.audit import audit_router

APP_NAME = "audit-service"
APP_VERSION = "5.0.0"

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Event audit logging service"
)

dapr_app = DaprApp(app)

app.include_router(subscriptions_router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(audit_router, prefix="/api/v1/audit", tags=["audit"])

@app.get("/health")
async def health():
    return {"status": "healthy", "service": APP_NAME}

@app.get("/ready")
async def ready():
    return {"status": "ready", "service": APP_NAME}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", "8003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
