"""
🔧 LUCA Hardware Module
Meshtastic Integration & T5 E-Paper S3 Pro Support

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

try:
    from .meshtastic_bridge import MeshtasticBridge
    from .t5_epaper_protocol import T5EpaperProtocol

    _HARDWARE_AVAILABLE = True
except ImportError:
    MeshtasticBridge = None
    T5EpaperProtocol = None
    _HARDWARE_AVAILABLE = False

__all__ = ["MeshtasticBridge", "T5EpaperProtocol"]
