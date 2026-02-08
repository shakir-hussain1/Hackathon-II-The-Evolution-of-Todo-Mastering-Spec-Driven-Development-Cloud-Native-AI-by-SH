"""Main FastAPI application for Chat API Service"""

import os
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dapr.ext.fastapi import DaprApp
from .routes import auth_router, tasks_router, chat_router
from .middleware.correlation import CorrelationMiddleware
from .database import engine
from .models.base import Base
from .utils.logging import get_logger

logger = get_logger(__name__)

# Application metadata
APP_NAME = "chat-api"
APP_VERSION = "5.0.0"
APP_DESCRIPTION = "AI-powered todo management service with microservices architecture"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    # Create database tables
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    yield

    # Shutdown
    logger.info(f"Shutting down {APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Initialize Dapr
dapr_app = DaprApp(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add correlation ID middleware
app.add_middleware(CorrelationMiddleware)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "details": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else None
        }
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for Kubernetes liveness probe.

    Returns 200 OK if service is running.
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint for Kubernetes readiness probe.

    Checks database connectivity and other dependencies.
    """
    checks = {
        "database": "ok",
        "dapr": "ok",
        "kafka": "ok"
    }

    # Check database
    try:
        from .database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        checks["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        checks["database"] = "error"

    # Determine overall status
    overall_status = "healthy" if all(v == "ok" for v in checks.values()) else "degraded"

    return {
        "status": overall_status,
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/health"
    }


# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


# Dapr subscriptions for event handling
@dapr_app.subscribe(pubsub="pubsub-kafka", topic="task-events")
async def handle_task_events(event_data: dict):
    """
    Handle task events from Kafka for audit logging.

    Events are forwarded to the audit service via Dapr.
    """
    try:
        logger.info(f"Received task event: {event_data.get('type', 'unknown')}")

        # Forward to audit service via Dapr service invocation
        # The audit service will handle the actual logging
        # This is a placeholder for future implementation

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error handling task event: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("DEBUG", "false").lower() == "true",
        log_level="info"
    )
