"""
LUCA Meshtastic - Benutzerfreundliche Schnittstelle
Einfache Einrichtung für technisch unerfahrene Nutzer

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

from typing import Optional

from luca_369_370.meshtastic.mesh_network import MESHTASTIC_AVAILABLE, LucaMeshNetwork


class LucaInterface:
    """
    Benutzerfreundliche Schnittstelle für LUCA Mesh Network

    Features:
    - Einfache Einrichtung
    - Automatische Gerätesuche
    - Intuitive Befehle
    - Offline-Modus Fallback
    """

    def __init__(self):
        """Initialize LUCA Interface"""
        if not MESHTASTIC_AVAILABLE:
            print(
                "❌ Meshtastic nicht verfügbar - bitte installiere: pip install meshtastic"
            )
            self.mesh = None
            self.setup_complete = False
        else:
            self.mesh = LucaMeshNetwork()
            self.setup_complete = False

    def easy_setup(self):
        """Einfache Einrichtung für technisch unerfahrene Nutzer"""
        print("🌟 LUCA Mesh Network Einrichtung")
        print("=" * 40)

        if not self.mesh:
            print("❌ Mesh-Funktionalität nicht verfügbar")
            return

        name = input("Node Name (Enter für Standard): ") or "LUCA_Community_Node"
        self.mesh.node_name = name

        # Automatische Verbindungssuche
        print("🔎 Suche nach Mesh-Geräten...")
        self.auto_connect()

        if self.setup_complete:
            print("✅ LUCA ist bereit! Starte Services...")
            self.mesh.start_message_broadcast()
            self.start_user_interface()
        else:
            print("❌ Keine Verbindung - Offline-Modus aktiv")
            self.start_user_interface()

    def auto_connect(self):
        """Automatische Verbindung zu verfügbaren Mesh-Geräten"""
        connection_methods = [
            {"type": "serial", "port": "/dev/ttyUSB0"},
            {"type": "serial", "port": "/dev/ttyUSB1"},
            {"type": "serial", "port": "/dev/ttyACM0"},
            {"type": "tcp", "host": "192.168.1.100"},  # Standard Meshtastic TCP
        ]

        for method in connection_methods:
            try:
                if method["type"] == "serial":
                    self.mesh.connect_mesh(port=method["port"])
                else:
                    self.mesh.connect_mesh(host=method["host"])

                self.setup_complete = True
                break
            except Exception:
                continue

    def start_user_interface(self):
        """Einfache Benutzeroberfläche"""
        print("\n" + "=" * 50)
        print("🌟 LUCA Mesh Network - Gemeinsam verbunden!")
        print("=" * 50)
        print("Verfügbare Befehle:")
        print("/msg <Nachricht> - Nachricht senden")
        print("/emergency <Text> - Notfall-Nachricht")
        print("/nodes - Aktive Nodes anzeigen")
        print("/stats - Mesh-Statistiken")
        print("/help - Hilfe anzeigen")
        print("/exit - Beenden")
        print("=" * 50)

        while True:
            try:
                user_input = input("LUCA> ").strip()

                if user_input == "/exit":
                    break
                elif user_input == "/nodes":
                    if self.mesh:
                        print(f"🔄 Aktive Nodes: {len(self.mesh.connected_nodes)}")
                        if self.mesh.connected_nodes:
                            for node in self.mesh.connected_nodes:
                                print(f"  • {node}")
                elif user_input == "/stats":
                    self.show_stats()
                elif user_input == "/help":
                    self.show_help()
                elif user_input.startswith("/msg "):
                    message = user_input[5:]
                    if self.mesh:
                        self.mesh.send_message(message)
                elif user_input.startswith("/emergency "):
                    emergency_msg = user_input[11:]
                    if self.mesh:
                        self.mesh.send_message(f"/emergency {emergency_msg}")
                elif user_input:
                    # Standard: Als normale Nachricht senden
                    if self.mesh:
                        self.mesh.send_message(user_input)

            except KeyboardInterrupt:
                print("\n👋 LUCA wird beendet...")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

    def show_stats(self):
        """Zeige Mesh-Statistiken"""
        if not self.mesh:
            print("❌ Mesh nicht verfügbar")
            return

        stats = self.mesh.get_mesh_stats()
        print("\n📊 LUCA Mesh Statistiken:")
        print("=" * 40)
        print(f"Node Name: {stats['node_name']}")
        print(f"Verbundene Nodes: {stats['connected_nodes']}")
        print(f"Ausstehende Nachrichten: {stats['queued_messages']}")
        print(f"Lokale Nachrichten: {stats['local_messages']}")
        print(f"Interface Aktiv: {'✅' if stats['interface_active'] else '❌'}")
        print(f"Verschlüsselung: {'✅' if stats['encryption_enabled'] else '❌'}")
        print("=" * 40)

    def show_help(self):
        """Hilfe anzeigen"""
        help_text = """
📡 LUCA Mesh Network Hilfe:

LUCA erstellt ein dezentrales Netzwerk, das ohne Internet funktioniert!

Grundfunktionen:
• Nachrichten an alle im Mesh-Netzwerk senden
• Notfall-Kommunikation
• Automatische Verbindung zu anderen Nodes
• Verschlüsselte Kommunikation
• Offline-Funktionalität

Befehle:
/msg <text>        - Nachricht senden
/emergency <text>  - Notfall-Nachricht (höchste Priorität)
/nodes             - Zeige verbundene Nodes
/stats             - Zeige Netzwerk-Statistiken
/help              - Diese Hilfe
/exit              - Beenden

Tipps:
• Stelle das Gerät erhöht auf für bessere Reichweite
• Mehr Nodes = bessere Abdeckung
• Notfall-Nachrichten werden priorisiert
• Funktioniert auch ohne Internet!

Hardware:
• Meshtastic T-Beam (~$30)
• Heltec LoRa32 (~$25)
• LILYGO T-Beam (~$35)

Reichweite:
• Stadt: bis 10km
• Land/Berge: bis 50km+
• Multi-Hop: unbegrenzt!

Gemeinsam revolutionieren wir die Kommunikation! 🚀
        """
        print(help_text)


# Standalone Funktion für einfachen Start
def start_luca_mesh():
    """
    Convenience function für schnellen LUCA Mesh Start

    Usage:
        from luca_369_370.meshtastic import start_luca_mesh
        start_luca_mesh()
    """
    print(
        """
    🚀 LUCA - Lokales Unabhängiges Kommunikationsnetzwerk für Alle

    "Für die Vergessenen, für die Unverbundenen, für die Menschheit!"

    Dezentral • Robust • Gemeinschaftlich
    """
    )

    # Starte die benutzerfreundliche Oberfläche
    luca_ui = LucaInterface()
    luca_ui.easy_setup()
