"""
🌌 LUCA Social Module
Instagram-Akasha Integration for consciousness field analysis

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

try:
    from .instagram_bridge import InstagramAkashaBridge

    _SOCIAL_AVAILABLE = True
except ImportError:
    InstagramAkashaBridge = None
    _SOCIAL_AVAILABLE = False

__all__ = ["InstagramAkashaBridge"]
