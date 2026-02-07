"""
Database migration script for Phase III Todo Chatbot.
Creates all tables with indexes and foreign key constraints.
"""
import asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from ..config import settings
from ..models import User, Task, Conversation, Message


async def create_tables():
    """Create all database tables with proper schema."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # Log SQL statements
    )

    async with engine.begin() as conn:
        # Drop all tables (for development only)
        # await conn.run_sync(SQLModel.metadata.drop_all)

        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)

    await engine.dispose()
    print("[OK] Database tables created successfully")


async def drop_tables():
    """Drop all database tables (use with caution!)."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()
    print("[OK] Database tables dropped")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        asyncio.run(drop_tables())
    else:
        asyncio.run(create_tables())
