"""
Routes Module
API endpoints for authentication, chat, and patterns (HGT)
"""

from .auth import router as auth_router
from .chat import router as chat_router
from .patterns import router as patterns_router

__all__ = ["auth_router", "chat_router", "patterns_router"]
