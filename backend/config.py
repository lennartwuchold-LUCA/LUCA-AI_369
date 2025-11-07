"""
LUCA AI Configuration
Loads environment variables and provides settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    ANTHROPIC_API_KEY: str
    SECRET_KEY: str

    # Database
    DATABASE_URL: str = "sqlite:///./luca.db"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Admin Account
    ADMIN_EMAIL: str = "admin@luca-ai.com"
    ADMIN_PASSWORD: str = "Ypsilon369Admin!"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Anthropic Settings
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    MAX_TOKENS_DEFAULT: int = 666  # Harmony signature

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
