"""
FastAPI application entry point for Phase III Todo Chatbot.
Configures CORS, authentication, error handling, and routes.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import settings
from .db.connection import init_db, close_db
from .api import auth, chat, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Initialize database connection on startup, close on shutdown.
    """
    # Startup
    print("[STARTUP] Starting Phase III Todo Chatbot API...")
    settings.validate()  # Validate required environment variables
    await init_db()
    print("[OK] Database connected")
    yield
    # Shutdown
    print("[SHUTDOWN] Shutting down...")
    await close_db()
    print("[OK] Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="Phase III Todo Chatbot API",
    description="AI-powered todo chatbot using OpenAI Agents SDK and MCP",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with user-friendly messages."""
    print(f"[ERROR] Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tasks.router)
