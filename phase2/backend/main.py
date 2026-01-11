"""
Phase II Backend - FastAPI Application Entry Point

Main FastAPI application with middleware, route configuration, and startup/shutdown events.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.config import settings
from src.db.database import create_db_and_tables, get_session
from src.middleware.auth import auth_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up FastAPI application...")
    try:
        create_db_and_tables()
        print("[OK] Database tables created")
    except Exception as e:
        print(f"[ERROR] Error creating database tables: {e}")
        raise

    yield

    # Shutdown
    print("Shutting down FastAPI application...")


# Create FastAPI application
app = FastAPI(
    title="Phase II Todo API",
    description="Full-Stack Todo Application - Phase II",
    version="1.0.0",
    lifespan=lifespan,
)

# Note: CORS headers are handled directly in the auth middleware
# to ensure they're present on all responses including errors


# Add JWT validation middleware (also handles CORS)
@app.middleware("http")
async def auth_check(request, call_next):
    """
    Middleware to validate JWT on protected routes and handle CORS.

    Calls auth_middleware from src.middleware.auth
    """
    return await auth_middleware(request, call_next)


# Health check endpoint (public)
@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Simple status response
    """
    return {"status": "ok", "message": "API is running"}


# Route imports
from src.api.routes import tasks, auth

# Include routers
app.include_router(auth.router)    # /auth/signup, /auth/login, /auth/logout
app.include_router(tasks.router)   # /api/users/{user_id}/tasks/*


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
