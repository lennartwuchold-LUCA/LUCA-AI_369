#!/usr/bin/env python3
"""
LUCA Mesh CLI - Dezentrales Netzwerk für ALLE
Interactive Command Line Interface für LUCA Meshtastic Integration

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from luca_369_370.meshtastic import LucaInterface

    MESH_AVAILABLE = True
except ImportError:
    MESH_AVAILABLE = False


def main():
    """Main entry point für LUCA Mesh CLI"""
    print(
        """
    🌐 LUCA MESH - Lokales Unabhängiges Kommunikationsnetzwerk für Alle
    ═══════════════════════════════════════════════════════════════════

    "Für die Vergessenen, für die Unverbundenen, für die Menschheit!"

    Dezentral • Robust • Gemeinschaftlich • Offline-First
    ═══════════════════════════════════════════════════════════════════
    """
    )

    if not MESH_AVAILABLE:
        print("❌ Meshtastic Integration nicht verfügbar!")
        print("   Installiere Dependencies:")
        print("   pip install meshtastic cryptography pyserial")
        print()
        sys.exit(1)

    # Starte LUCA Mesh Interface
    try:
        luca_mesh = LucaInterface()
        luca_mesh.easy_setup()
    except KeyboardInterrupt:
        print("\n\n👋 LUCA Mesh wird beendet...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fehler beim Start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
