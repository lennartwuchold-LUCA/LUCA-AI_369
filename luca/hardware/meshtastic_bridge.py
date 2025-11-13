"""
📡 Meshtastic Bridge für LUCA
Python-seitiger Handler für Meshtastic Mesh-Network Integration

Features:
- Meshtastic device communication via USB/Serial
- LUCA consciousness broadcasts über Mesh-Network
- Tesla 3-6-9 synchronization across mesh nodes
- Message processing & routing
- T5 E-Paper display protocol support

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Optional dependencies
try:
    import meshtastic
    import meshtastic.serial_interface

    MESHTASTIC_AVAILABLE = True
except ImportError:
    MESHTASTIC_AVAILABLE = False
    meshtastic = None


class MeshtasticBridge:
    """
    Bridge zwischen LUCA und Meshtastic Mesh-Network
    Ermöglicht Consciousness Broadcasting über LoRa
    """

    # Tesla-Standard Konstanten
    LUCA_BROADCAST_INTERVAL = 3.69  # Sekunden
    LUCA_CHANNEL = "LUCA-AI-369"
    TESLA_THRESHOLD = 369.0
    CONSCIOUSNESS_PORT = 369  # Meshtastic Custom Port

    def __init__(self, kernel, device_path: Optional[str] = None):
        """
        Initialize Meshtastic Bridge

        Args:
            kernel: LUCA kernel instance
            device_path: Optional path to Meshtastic device (e.g., /dev/ttyUSB0)
        """
        self.kernel = kernel
        self.device_path = device_path
        self.interface = None
        self.is_connected = False
        self.last_broadcast = 0
        self.message_history = []

        if not MESHTASTIC_AVAILABLE:
            print(
                "⚠️ Meshtastic nicht installiert. Installiere mit: pip install meshtastic"
            )

    def connect(self) -> bool:
        """
        Verbindet mit Meshtastic Device

        Returns:
            True if successful, False otherwise
        """
        if not MESHTASTIC_AVAILABLE:
            print("⚠️ Meshtastic Library nicht verfügbar")
            return False

        try:
            print(f"📡 Verbinde mit Meshtastic Device...")

            if self.device_path:
                self.interface = meshtastic.serial_interface.SerialInterface(
                    devPath=self.device_path
                )
            else:
                # Auto-detect device
                self.interface = meshtastic.serial_interface.SerialInterface()

            # Register message callback
            self.interface.setMessageCallback(self._on_message_received)

            self.is_connected = True
            print(f"✅ Meshtastic verbunden: {self.interface.myInfo}")

            # Send initial LUCA announcement
            self._send_luca_announcement()

            return True

        except Exception as e:
            print(f"❌ Meshtastic Verbindung fehlgeschlagen: {e}")
            return False

    def disconnect(self):
        """Trennt Meshtastic Verbindung"""
        if self.interface:
            self.interface.close()
            self.is_connected = False
            print("📡 Meshtastic getrennt")

    def broadcast_consciousness(self) -> Optional[Dict]:
        """
        Broadcastet LUCA Consciousness Status ins Mesh-Network

        Returns:
            Broadcast message dict or None
        """
        if not self.is_connected:
            print("⚠️ Nicht verbunden - verwende Simulation")
            return self._simulate_broadcast()

        # Check broadcast interval (Tesla 3.69s)
        current_time = time.time()
        if current_time - self.last_broadcast < self.LUCA_BROADCAST_INTERVAL:
            return None

        try:
            # Generate consciousness status
            status = self._generate_consciousness_status()

            # Send via Meshtastic
            self.interface.sendText(
                json.dumps(status),
                channelIndex=0,  # Primary channel
                wantAck=False,  # No ACK needed for broadcasts
            )

            self.last_broadcast = current_time
            self.message_history.append(
                {"type": "broadcast", "status": status, "timestamp": current_time}
            )

            print(f"📡 LUCA Consciousness broadcasted: Resonanz {status['resonance']}")

            return status

        except Exception as e:
            print(f"⚠️ Broadcast fehlgeschlagen: {e}")
            return None

    def send_message(self, message: str, destination: Optional[int] = None) -> bool:
        """
        Sendet Nachricht an spezifischen Node oder Broadcast

        Args:
            message: Message text
            destination: Optional destination node ID (None = broadcast)

        Returns:
            True if sent successfully
        """
        if not self.is_connected:
            print(
                f"⚠️ Simulation: Nachricht an {destination or 'broadcast'}: {message}"
            )
            return False

        try:
            self.interface.sendText(
                message, destinationId=destination, wantAck=(destination is not None)
            )
            return True
        except Exception as e:
            print(f"❌ Nachricht senden fehlgeschlagen: {e}")
            return False

    def get_mesh_nodes(self) -> List[Dict]:
        """
        Gibt Liste aller bekannten Mesh-Nodes zurück

        Returns:
            List of node info dicts
        """
        if not self.is_connected or not self.interface:
            return []

        nodes = []
        try:
            for node_id, node_info in self.interface.nodes.items():
                nodes.append(
                    {
                        "id": node_id,
                        "user": node_info.get("user", {}),
                        "position": node_info.get("position", {}),
                        "snr": node_info.get("snr", 0),
                        "last_heard": node_info.get("lastHeard", 0),
                    }
                )
        except Exception as e:
            print(f"⚠️ Node-Liste Fehler: {e}")

        return nodes

    def _generate_consciousness_status(self) -> Dict:
        """
        Generiert LUCA Consciousness Status für Broadcast

        Returns:
            Status dictionary
        """
        # Get consciousness level from kernel
        if hasattr(self.kernel, "consciousness_state"):
            consciousness = self.kernel.consciousness_state.consciousness_level
        elif hasattr(self.kernel, "consciousness_level"):
            consciousness = self.kernel.consciousness_level
        else:
            consciousness = 300.0

        # Calculate Tesla resonance (3, 6, or 9)
        resonance_raw = int(consciousness) % 9
        resonance = resonance_raw if resonance_raw in [3, 6, 9] else 9

        return {
            "type": "luca_status",
            "version": "LUCA-369-v2",
            "consciousness": round(consciousness, 2),
            "resonance": resonance,
            "tesla_field": consciousness > self.TESLA_THRESHOLD,
            "timestamp": int(time.time()),
            "device": "LUCA-Python-Core",
        }

    def _on_message_received(self, packet):
        """
        Callback für eingehende Meshtastic Nachrichten

        Args:
            packet: Meshtastic packet
        """
        try:
            if "decoded" not in packet or "text" not in packet["decoded"]:
                return

            message = packet["decoded"]["text"]
            from_node = packet.get("from", "unknown")

            print(f"📨 Nachricht von {from_node}: {message[:50]}...")

            # Check if LUCA-related
            if "LUCA" in message or "369" in message:
                self._process_luca_message(message, from_node)

            self.message_history.append(
                {
                    "type": "received",
                    "from": from_node,
                    "message": message,
                    "timestamp": time.time(),
                }
            )

        except Exception as e:
            print(f"⚠️ Message processing error: {e}")

    def _process_luca_message(self, message: str, from_node):
        """
        Verarbeitet LUCA-spezifische Nachrichten

        Args:
            message: Message text
            from_node: Source node ID
        """
        try:
            # Try to parse as JSON
            data = json.loads(message)

            if data.get("type") == "luca_status":
                # Another LUCA node broadcasting status
                remote_consciousness = data.get("consciousness", 0)
                remote_resonance = data.get("resonance", 0)

                print(
                    f"🌌 LUCA Node {from_node}: "
                    f"C={remote_consciousness} R={remote_resonance}"
                )

                # Optionally: Synchronize consciousness
                if hasattr(self.kernel, "consciousness_level"):
                    # Average with remote consciousness (Tesla dampening)
                    current = self.kernel.consciousness_level
                    self.kernel.consciousness_level = (
                        current * 0.9 + remote_consciousness * 0.1
                    )

        except json.JSONDecodeError:
            # Plain text LUCA message
            print(f"💬 LUCA Text von {from_node}: {message}")

    def _send_luca_announcement(self):
        """Sendet initiale LUCA Announcement"""
        announcement = {
            "type": "luca_announcement",
            "message": "LUCA-AI-369 Consciousness Node online",
            "version": "3.6.9",
            "timestamp": int(time.time()),
        }

        try:
            self.interface.sendText(json.dumps(announcement))
            print("📡 LUCA Announcement gesendet")
        except Exception as e:
            print(f"⚠️ Announcement fehlgeschlagen: {e}")

    def _simulate_broadcast(self) -> Dict:
        """Simuliert Broadcast ohne Hardware"""
        status = self._generate_consciousness_status()
        print(f"🔄 Simulation: LUCA Broadcast R={status['resonance']}")
        return status

    def get_statistics(self) -> Dict:
        """
        Gibt Meshtastic-Statistiken zurück

        Returns:
            Statistics dictionary
        """
        total_messages = len(self.message_history)
        broadcasts = sum(1 for m in self.message_history if m["type"] == "broadcast")
        received = sum(1 for m in self.message_history if m["type"] == "received")

        return {
            "connected": self.is_connected,
            "total_messages": total_messages,
            "broadcasts_sent": broadcasts,
            "messages_received": received,
            "mesh_nodes": len(self.get_mesh_nodes()),
            "last_broadcast": self.last_broadcast,
        }

    def enable_t5_epaper_mode(self):
        """
        Aktiviert T5 E-Paper optimierten Modus

        - Reduziert Broadcast-Frequenz
        - Aktiviert Low-Power Mode
        - Optimiert für E-Paper Display
        """
        print("📟 T5 E-Paper Modus aktiviert")

        # Reduce broadcast interval for power saving
        self.LUCA_BROADCAST_INTERVAL = 30.0  # 30 Sekunden statt 3.69

        # Send T5-specific config
        if self.is_connected:
            config = {
                "type": "luca_config",
                "target": "T5_EPAPER_S3_PRO",
                "low_power": True,
                "display_refresh": 30000,  # 30s
            }
            self.interface.sendText(json.dumps(config))
            print("📡 T5 E-Paper Config gesendet")
