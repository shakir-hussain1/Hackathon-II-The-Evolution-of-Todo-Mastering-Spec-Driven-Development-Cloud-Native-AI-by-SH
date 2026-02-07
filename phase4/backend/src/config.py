"""
Configuration management for Phase III Todo Chatbot.
Loads environment variables and provides typed configuration access.
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file (force reload to get latest values)
load_dotenv(override=True)


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/phase3_todo"
    )

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Authentication
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # CORS
    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    ]

    @classmethod
    def validate(cls) -> None:
        """Validate required settings are present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not cls.JWT_SECRET:
            raise ValueError("JWT_SECRET environment variable is required")
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")


# Global settings instance
settings = Settings()
