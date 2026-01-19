"""
Database connection management with async SQLModel.
Provides connection pooling and session management for Neon PostgreSQL.
"""
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from ..config import settings

# Create async engine with connection pooling
# Configure based on database type (SQLite vs PostgreSQL)
if "sqlite" in settings.DATABASE_URL:
    # SQLite configuration - simpler, no connection args needed
    engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
    )
else:
    # PostgreSQL configuration - with connection pooling
    engine: AsyncEngine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        connect_args={
            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0,
        },
        pool_recycle=3600,
    )

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI endpoints to get database sessions.

    Usage:
        @app.get("/endpoint")
        async def endpoint(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    """Initialize database connection and create tables."""
    from sqlmodel import SQLModel
    from ..models import User, Task, Conversation, Message  # Import all models

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connections gracefully."""
    await engine.dispose()
