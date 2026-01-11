"""
Configuration management for Phase II backend.

Loads environment variables from .env file and validates required settings.
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")

    # Better Auth
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

    # Server
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **data):
        """Initialize settings and validate required fields."""
        super().__init__(**data)
        self._validate_required_fields()

    def _validate_required_fields(self):
        """Validate that all required settings are provided."""
        required_fields = {
            "DATABASE_URL": self.DATABASE_URL,
            "JWT_SECRET": self.JWT_SECRET,
            "BETTER_AUTH_SECRET": self.BETTER_AUTH_SECRET,
        }

        missing_fields = [
            field for field, value in required_fields.items() if not value
        ]

        if missing_fields:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_fields)}. "
                f"Please copy .env.example to .env and fill in the values."
            )

        # Validate JWT_SECRET minimum length
        if len(self.JWT_SECRET) < 32:
            raise ValueError(
                "JWT_SECRET must be at least 32 characters long. "
                "Generate a strong secret: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )


# Initialize settings
try:
    settings = Settings()
except ValueError as e:
    print(f"Configuration Error: {e}")
    raise
