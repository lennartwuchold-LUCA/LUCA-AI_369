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
        print("/satellite <on/off/status> - Satellite-Bridge steuern")
        print("/sat_send <Nachricht> - Via Satellit senden")
        print("/ai_status - AI-Optimizer Status anzeigen")
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
                elif user_input.startswith("/satellite "):
                    sat_cmd = user_input[11:].strip()
                    self.handle_satellite_command(sat_cmd)
                elif user_input.startswith("/sat_send "):
                    sat_message = user_input[10:]
                    if self.mesh:
                        success = self.mesh.send_via_satellite(sat_message)
                        if success:
                            print("✅ Nachricht via Satellit gesendet!")
                        else:
                            print("❌ Satellite-Senden fehlgeschlagen")
                elif user_input == "/ai_status":
                    self.show_ai_status()
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

    def handle_satellite_command(self, cmd: str):
        """
        Handle satellite commands

        Args:
            cmd: Command (on/off/status)
        """
        if not self.mesh:
            print("❌ Mesh nicht verfügbar")
            return

        if cmd == "on":
            print("🛰️ Aktiviere Satellite-Bridge...")
            success = self.mesh.enable_satellite_bridge("starlink")
            if success:
                print("✅ Satellite-Bridge aktiv!")
            else:
                print("❌ Satellite-Aktivierung fehlgeschlagen")
        elif cmd == "off":
            if self.mesh.satellite_bridge:
                self.mesh.satellite_bridge.disconnect()
                print("📡 Satellite-Bridge deaktiviert")
            else:
                print("⚠️  Satellite-Bridge war nicht aktiv")
        elif cmd == "status":
            if self.mesh.satellite_bridge:
                status = self.mesh.satellite_bridge.get_status()
                print("\n🛰️ Satellite-Bridge Status:")
                print("=" * 40)
                print(f"Provider: {status['provider']}")
                print(f"Status: {status['status']}")
                print(f"Gebufferte Nachrichten: {status['buffered_messages']}")
                print(f"AI verfügbar: {'✅' if status['ai_available'] else '❌'}")
                if "ai_recommendation" in status:
                    print(f"AI-Empfehlung: {status['ai_recommendation']}")
                print("=" * 40)
            else:
                print("⚠️  Satellite-Bridge nicht aktiviert")
        else:
            print("❌ Unbekannter Befehl. Verwende: on/off/status")

    def show_ai_status(self):
        """Show AI optimizer status"""
        if not self.mesh or not self.mesh.satellite_bridge:
            print("⚠️  Satellite-Bridge nicht verfügbar")
            return

        if self.mesh.satellite_bridge.ai_optimizer.model:
            print("\n🧠 AI-Optimizer Status:")
            print("=" * 40)
            print("Status: ✅ Aktiv (PyTorch)")

            # Show metrics
            metrics = self.mesh.satellite_bridge.performance_metrics
            print("\nPerformance Metrics:")
            for provider, m in metrics.items():
                print(
                    f"  {provider}: Latenz={m['latency']:.2f}s, Fehler={m['error_rate']:.2%}"
                )

            # Best provider recommendation
            if self.mesh.satellite_bridge.active_provider:
                provider_metrics = metrics[self.mesh.satellite_bridge.active_provider]
                best = self.mesh.satellite_bridge.ai_optimizer.predict_best_provider(
                    provider_metrics["signal"],
                    provider_metrics["latency"],
                    provider_metrics["error_rate"],
                )
                print(f"\nAI-Empfehlung: {best}")
            print("=" * 40)
        else:
            print("⚠️  AI deaktiviert (PyTorch fehlt)")
            print("   Installiere mit: pip install torch")

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
• Satellite-Bridge für globale Reichweite

Befehle:
/msg <text>        - Nachricht senden
/emergency <text>  - Notfall-Nachricht (höchste Priorität)
/nodes             - Zeige verbundene Nodes
/stats             - Zeige Netzwerk-Statistiken
/satellite on      - Satellite-Bridge aktivieren
/satellite off     - Satellite-Bridge deaktivieren
/satellite status  - Satellite-Status anzeigen
/sat_send <text>   - Nachricht via Satellit senden
/ai_status         - AI-Optimizer Status
/help              - Diese Hilfe
/exit              - Beenden

Tipps:
• Stelle das Gerät erhöht auf für bessere Reichweite
• Mehr Nodes = bessere Abdeckung
• Notfall-Nachrichten werden priorisiert
• Funktioniert auch ohne Internet!
• Satellite-Bridge für weltweite Kommunikation

Hardware:
• Meshtastic T-Beam (~$30)
• Heltec LoRa32 (~$25)
• LILYGO T-Beam (~$35)

Reichweite:
• LoRa: Stadt bis 10km, Land bis 50km+
• Satellite: Weltweit!
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
