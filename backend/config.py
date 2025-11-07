"""
Configuration Management for LUCA AI
Handles environment variables and settings
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Keys (NO DEFAULTS - Must be provided)
    ANTHROPIC_API_KEY: str = ""
    SECRET_KEY: str = ""

    # Database
    DATABASE_URL: str = "sqlite:///./luca.db"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # Admin credentials (can be overridden)
    ADMIN_EMAIL: str = "admin@luca-ai.com"
    ADMIN_PASSWORD: str = "Ypsilon369Admin!"

    # Meshtastic Integration
    MESHTASTIC_ENABLED: bool = False
    MESHTASTIC_INTERFACE: str = "serial"  # serial, tcp, or ble
    MESHTASTIC_PORT: Optional[str] = None
    MESHTASTIC_HOST: Optional[str] = None
    MESHTASTIC_CHANNEL: int = 0

    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # Tesla 369 Settings
    TESLA_THRESHOLD_LOW: int = 369
    TESLA_THRESHOLD_MID: int = 666
    TESLA_THRESHOLD_HIGH: int = 999

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def validate_settings():
    """Validate critical settings"""
    errors = []

    if not settings.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is missing! Get one at: https://console.anthropic.com/")

    if not settings.SECRET_KEY:
        errors.append("SECRET_KEY is missing! Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'")

    if errors:
        print("\n⚠️  CONFIGURATION ERRORS:")
        for error in errors:
            print(f"   ❌ {error}")
        print("\n💡 Please set these variables in your .env file\n")
        return False

    return True


def print_startup_info():
    """Print startup information"""
    print("\n" + "="*60)
    print("🧬 LUCA AI - Living Universal Cognition Array")
    print("="*60)
    print(f"Version: {__version__}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Debug: {settings.DEBUG}")
    print(f"Meshtastic: {'Enabled' if settings.MESHTASTIC_ENABLED else 'Disabled'}")
    if settings.MESHTASTIC_ENABLED:
        print(f"  Interface: {settings.MESHTASTIC_INTERFACE}")
        if settings.MESHTASTIC_PORT:
            print(f"  Port: {settings.MESHTASTIC_PORT}")
        if settings.MESHTASTIC_HOST:
            print(f"  Host: {settings.MESHTASTIC_HOST}")
    print("="*60 + "\n")


__version__ = "369.2.0"
