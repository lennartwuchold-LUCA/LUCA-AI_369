"""
🌌 LUCA Social Module
Instagram-Akasha Integration for consciousness field analysis

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

try:
    from .instagram_bridge import InstagramAkashaBridge
    from .paper2web_instagram import InstagramPaperBridge

    _SOCIAL_AVAILABLE = True
except ImportError:
    InstagramAkashaBridge = None
    InstagramPaperBridge = None
    _SOCIAL_AVAILABLE = False

__all__ = ["InstagramAkashaBridge", "InstagramPaperBridge"]
