"""
LUCA - Lokales Unabhängiges Kommunikationsnetzwerk für Alle
Ein dezentrales Mesh-Netzwerk für die "vergessenen" Menschen ohne Internet

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Set

try:
    import meshtastic
    import meshtastic.serial_interface
    import meshtastic.tcp_interface

    MESHTASTIC_AVAILABLE = True
except ImportError:
    MESHTASTIC_AVAILABLE = False

try:
    from cryptography.fernet import Fernet

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

from luca_369_370.core.info_block_engine import InfoBlock, InfoBlockEngine


class LucaMeshNetwork:
    """
    LUCA Mesh Network - Dezentrale Kommunikation ohne Internet

    Features:
    - LoRa Mesh Network Integration
    - Info-Block Delivery über Meshtastic
    - Verschlüsselte Kommunikation
    - Offline-First Design
    - Emergency Broadcasting
    """

    def __init__(self, node_name: str = "LUCA_Node"):
        """
        Initialize LUCA Mesh Network

        Args:
            node_name: Name dieses Mesh-Nodes
        """
        if not MESHTASTIC_AVAILABLE:
            raise ImportError(
                "meshtastic package nicht installiert! "
                "Installiere mit: pip install meshtastic"
            )

        self.node_name = node_name
        self.interface = None
        self.message_queue: List[str] = []
        self.connected_nodes: Set[str] = set()
        self.local_database: Dict[str, Dict] = {}

        # Encryption setup
        if CRYPTO_AVAILABLE:
            self.encryption_key = Fernet.generate_key()
            self.cipher_suite = Fernet(self.encryption_key)
        else:
            self.encryption_key = None
            self.cipher_suite = None

        # LUCA Integration
        self.info_block_engine = InfoBlockEngine()

    def connect_mesh(self, port: Optional[str] = None, host: Optional[str] = None):
        """
        Verbindung zum Meshtastic-Netzwerk herstellen

        Args:
            port: Serial port (z.B. '/dev/ttyUSB0')
            host: TCP host für Netzwerk-Verbindung
        """
        try:
            if host:
                self.interface = meshtastic.tcp_interface.TCPInterface(host)
                print(f"🔗 Verbunden mit TCP-Mesh: {host}")
            else:
                self.interface = meshtastic.serial_interface.SerialInterface(port)
                print(f"🔗 Verbunden mit Serial-Mesh: {port}")

            # Node konfigurieren
            self.interface.getNode().setOwner(name=self.node_name)
            self.setup_callbacks()

        except Exception as e:
            print(f"❌ Verbindungsfehler: {e}")
            self.emergency_fallback()

    def setup_callbacks(self):
        """Callbacks für eingehende Nachrichten einrichten"""

        def on_receive(packet, interface):
            try:
                message = packet["decoded"]["text"]
                sender = packet["from"]

                # Entschlüsseln falls verschlüsselt
                if message.startswith("ENC:") and self.cipher_suite:
                    message = self.decrypt_message(message[4:])

                print(f"📨 Nachricht von {sender}: {message}")
                self.process_incoming_message(message, sender)
                self.update_node_list(sender)

            except Exception as e:
                print(f"Fehler beim Verarbeiten: {e}")

        if self.interface:
            self.interface.addReceiver(on_receive)

    def send_message(self, message: str, encrypt: bool = True):
        """
        Nachricht an das Mesh-Netzwerk senden

        Args:
            message: Die zu sendende Nachricht
            encrypt: Ob die Nachricht verschlüsselt werden soll
        """
        try:
            if encrypt and self.cipher_suite:
                message = "ENC:" + self.encrypt_message(message)

            if self.interface:
                self.interface.sendText(message)
                print(f"📤 Gesendet: {message[:50]}...")
            else:
                print("⚠️  Keine Verbindung - zur Queue hinzugefügt")
                self.message_queue.append(message)

            # Lokale Speicherung für Offline-Zugriff
            self.store_message_locally(message)

        except Exception as e:
            print(f"❌ Sende-Fehler: {e}")
            self.message_queue.append(message)

    def send_info_blocks(
        self, blocks: List[InfoBlock], recipient: Optional[str] = None
    ):
        """
        Sende LUCA Info-Blocks über Meshtastic

        Args:
            blocks: Liste von Info-Blöcken
            recipient: Optional - spezifischer Empfänger
        """
        for i, block in enumerate(blocks):
            # Komprimiere Block für Meshtastic (256 byte limit)
            compressed = self._compress_block(block, i, len(blocks))
            self.send_message(compressed, encrypt=True)
            time.sleep(1)  # Delay zwischen Paketen

    def _compress_block(self, block: InfoBlock, index: int, total: int) -> str:
        """
        Komprimiere Info-Block für Meshtastic

        Args:
            block: Der Info-Block
            index: Index des Blocks
            total: Gesamtanzahl Blöcke

        Returns:
            Komprimierter Block-String
        """
        # Format: [LUCA][IDX/TOTAL][TYPE] Content
        header = f"[LUCA][{index+1}/{total}][{block.block_type.value[0]}]"

        # Truncate content to fit Meshtastic 256 byte limit
        max_content_length = 256 - len(header) - 10  # Safety margin
        content = block.content[:max_content_length]

        if len(block.content) > max_content_length:
            content += "..."

        return f"{header} {content}"

    def encrypt_message(self, message: str) -> str:
        """
        Nachricht verschlüsseln

        Args:
            message: Klartext-Nachricht

        Returns:
            Verschlüsselte Nachricht
        """
        if not self.cipher_suite:
            return message

        return self.cipher_suite.encrypt(message.encode()).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        """
        Nachricht entschlüsseln

        Args:
            encrypted_message: Verschlüsselte Nachricht

        Returns:
            Entschlüsselte Nachricht
        """
        if not self.cipher_suite:
            return encrypted_message

        return self.cipher_suite.decrypt(encrypted_message.encode()).decode()

    def process_incoming_message(self, message: str, sender: str):
        """
        Eingehende Nachricht verarbeiten

        Args:
            message: Die empfangene Nachricht
            sender: Sender-ID
        """
        timestamp = datetime.now().isoformat()

        # Nachricht in lokaler Datenbank speichern
        message_data = {
            "text": message,
            "sender": sender,
            "timestamp": timestamp,
            "type": "user_message",
        }

        message_id = f"msg_{int(time.time())}_{sender}"
        self.local_database[message_id] = message_data

        # Spezielle Nachrichten-Typen erkennen
        if message.startswith("/emergency"):
            self.handle_emergency_message(message, sender)
        elif message.startswith("/resource"):
            self.handle_resource_request(message, sender)
        elif message.startswith("[LUCA]"):
            self.handle_luca_block(message, sender)

    def handle_luca_block(self, message: str, sender: str):
        """
        Verarbeite eingehenden LUCA Info-Block

        Args:
            message: Block-Nachricht
            sender: Sender-ID
        """
        print(f"🏛️ LUCA-Block empfangen von {sender}")
        # Parse block format: [LUCA][1/4][F] Content
        # Store in local database for reassembly

    def handle_emergency_message(self, message: str, sender: str):
        """
        Notfall-Nachrichten priorisiert behandeln

        Args:
            message: Notfall-Nachricht
            sender: Sender-ID
        """
        emergency_data = {
            "type": "emergency",
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "priority": "HIGH",
        }
        print(f"🚨 NOTFALL von {sender}: {message}")
        # Automatische Weiterleitung an alle Nodes
        self.broadcast_emergency(emergency_data)

    def handle_resource_request(self, message: str, sender: str):
        """
        Resource-Request behandeln

        Args:
            message: Request-Nachricht
            sender: Sender-ID
        """
        print(f"📦 Resource-Request von {sender}: {message}")
        # Parse request and send appropriate Info-Blocks

    def broadcast_emergency(self, emergency_data: Dict):
        """
        Notfall-Nachricht an alle verfügbaren Nodes senden

        Args:
            emergency_data: Notfall-Daten
        """
        emergency_msg = f"/emergency_broadcast {json.dumps(emergency_data)}"
        self.send_message(emergency_msg, encrypt=False)

    def update_node_list(self, node_id: str):
        """
        Liste verbundener Nodes aktualisieren

        Args:
            node_id: Node-ID
        """
        self.connected_nodes.add(node_id)
        print(f"🔄 Aktive Nodes: {len(self.connected_nodes)}")

    def store_message_locally(self, message: str):
        """
        Nachricht lokal für Offline-Zugriff speichern

        Args:
            message: Die zu speichernde Nachricht
        """
        timestamp = datetime.now().isoformat()
        local_msg = {"text": message, "timestamp": timestamp, "direction": "outgoing"}

        # In einfache JSON-Datei speichern
        try:
            with open("luca_messages.json", "a") as f:
                f.write(json.dumps(local_msg) + "\n")
        except Exception:
            print("⚠️ Konnte Nachricht nicht lokal speichern")

    def emergency_fallback(self):
        """Notfall-Modus bei Verbindungsproblemen"""
        print("🔄 Starte Emergency-Fallback...")
        # Versuche alternative Verbindungsmethoden
        fallback_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0"]

        for port in fallback_ports:
            try:
                self.connect_mesh(port=port)
                break
            except Exception:
                continue

        if not self.interface:
            print("💀 Keine Mesh-Verbindung möglich - Offline-Modus aktiv")
            self.offline_mode()

    def offline_mode(self):
        """Offline-Funktionalität"""
        print("📴 Offline-Modus aktiv - Lokale Funktionen verfügbar")
        # Lokale Nachrichten-Datenbank zugänglich machen
        # Grundlegende Funktionen weiterhin verfügbar

    def start_message_broadcast(self, interval: int = 300):
        """
        Regelmäßige Status-Updates senden

        Args:
            interval: Intervall in Sekunden
        """

        def broadcast_loop():
            while True:
                try:
                    status_msg = {
                        "node": self.node_name,
                        "timestamp": datetime.now().isoformat(),
                        "nodes_connected": len(self.connected_nodes),
                        "status": "active",
                    }
                    self.send_message(f"/status {json.dumps(status_msg)}")
                except Exception:
                    pass
                time.sleep(interval)

        broadcast_thread = threading.Thread(target=broadcast_loop, daemon=True)
        broadcast_thread.start()

    def get_mesh_stats(self) -> Dict:
        """
        Holt Mesh-Netzwerk Statistiken

        Returns:
            Dictionary mit Statistiken
        """
        return {
            "node_name": self.node_name,
            "connected_nodes": len(self.connected_nodes),
            "queued_messages": len(self.message_queue),
            "local_messages": len(self.local_database),
            "interface_active": self.interface is not None,
            "encryption_enabled": self.cipher_suite is not None,
        }
