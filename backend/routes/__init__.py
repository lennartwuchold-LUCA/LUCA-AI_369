"""
LUCA AI Routes Module
API endpoints for authentication and chat
"""

from backend.routes.auth import router as auth_router
from backend.routes.chat import router as chat_router

__all__ = ["auth_router", "chat_router"]
