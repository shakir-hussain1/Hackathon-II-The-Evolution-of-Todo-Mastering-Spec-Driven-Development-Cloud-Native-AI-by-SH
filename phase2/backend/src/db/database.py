"""
Database connection and session management.

Sets up SQLModel engine and provides session dependency for route handlers.
"""

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from typing import Generator
from src.config import settings


# Determine database type and configure engine appropriately
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
is_neon = "neon" in settings.DATABASE_URL

# Build connect_args based on database type
connect_args = {}
if is_sqlite:
    # SQLite requires check_same_thread=False for FastAPI
    connect_args = {"check_same_thread": False}
elif is_neon:
    # PostgreSQL on Neon requires SSL
    connect_args = {"sslmode": "require"}

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
    # Use NullPool for Neon (serverless) to avoid connection pooling issues
    poolclass=NullPool if is_neon else None,
)


def create_db_and_tables():
    """
    Create all database tables.

    This should be called once on application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to provide database session to route handlers.

    Usage in route handler:
        @app.get("/tasks")
        async def get_tasks(session: Session = Depends(get_session)):
            # Use session here
            pass
    """
    with Session(engine) as session:
        yield session
