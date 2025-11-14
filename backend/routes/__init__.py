"""
Routes Module
API endpoints for authentication, chat, patterns (HGT), mycelium network, consciousness optimization, and T5 E-Paper
"""

from .auth import router as auth_router
from .chat import router as chat_router
from .patterns import router as patterns_router
from .mycelium import router as mycelium_router
from .consciousness import router as consciousness_router
from .neurodiversity import router as neurodiversity_router
from .t5_api import router as t5_router

__all__ = ["auth_router", "chat_router", "patterns_router", "mycelium_router", "consciousness_router", "neurodiversity_router", "t5_router"]
