"""
LUCA 369/370 - Meshtastic Integration
Dezentrales Mesh-Netzwerk für die "Vergessenen"
+ Satellite Bridge für globale Reichweite

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370

Features:
- LoRa Mesh Network (local)
- Satellite Bridge (global)
- AI-optimierte Provider-Auswahl
- Offline-First Design
"""

from luca_369_370.meshtastic.mesh_interface import LucaInterface, start_luca_mesh
from luca_369_370.meshtastic.mesh_network import LucaMeshNetwork
from luca_369_370.meshtastic.mesh_revolution import LucaRevolution

# Satellite Bridge (optional - requires paho-mqtt)
try:
    from luca_369_370.meshtastic.satellite_bridge import (
        AIOptimizer,
        SatelliteBridge,
        SatelliteMessageRelay,
        broadcast_globally,
        create_satellite_enabled_mesh,
    )

    SATELLITE_AVAILABLE = True
except ImportError:
    SATELLITE_AVAILABLE = False
    # Provide stub for better error messages
    SatelliteBridge = None
    AIOptimizer = None
    SatelliteMessageRelay = None
    broadcast_globally = None
    create_satellite_enabled_mesh = None

__all__ = [
    # Core Mesh
    "LucaMeshNetwork",
    "LucaInterface",
    "LucaRevolution",
    "start_luca_mesh",
    # Satellite Bridge
    "SatelliteBridge",
    "AIOptimizer",
    "SatelliteMessageRelay",
    "broadcast_globally",
    "create_satellite_enabled_mesh",
    "SATELLITE_AVAILABLE",
]
