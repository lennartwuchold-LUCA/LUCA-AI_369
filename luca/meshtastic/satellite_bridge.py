"""
LUCA Satellite Bridge - Global Reach for ALL!
Satelliten-Integration für weltweite Kommunikation
Version 4.0: AI-Optimierung + Performance Metrics

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

try:
    import paho.mqtt.client as mqtt

    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

try:
    import torch
    import torch.nn as nn

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("LUCA_Satellite")


class AIOptimizer:
    """
    Simple AI für Provider-Wechsel basierend auf Signalqualität

    Features:
    - PyTorch-basierte Provider-Auswahl
    - Training basierend auf Performance-Metrics
    - Automatische Optimierung der Satellitenverbindung
    """

    def __init__(self):
        """Initialize AI Optimizer"""
        if not TORCH_AVAILABLE:
            logger.warning("PyTorch nicht verfügbar - AI-Optimierung deaktiviert")
            self.model = None
            self.optimizer = None
            self.history = []
            return

        # Simple Neural Network: [Signal, Latenz, Fehlerrate] → [Provider-Scores]
        self.model = nn.Sequential(
            nn.Linear(3, 10), nn.ReLU(), nn.Linear(10, 3)  # 3 Provider
        )
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        self.history = []  # Speichere Daten für Training

    def predict_best_provider(
        self, signal: float, latency: float, error_rate: float
    ) -> str:
        """
        Predict best satellite provider based on metrics

        Args:
            signal: Signal strength (0.0-1.0)
            latency: Latency in seconds
            error_rate: Error rate (0.0-1.0)

        Returns:
            Best provider name ('starlink', 'iridium', 'globalstar')
        """
        if self.model is None:
            return "starlink"  # Fallback wenn AI nicht verfügbar

        with torch.no_grad():
            input_tensor = torch.tensor(
                [[signal, latency, error_rate]], dtype=torch.float32
            )
            scores = self.model(input_tensor)
            providers = ["starlink", "iridium", "globalstar"]
            best_idx = torch.argmax(scores).item()
            return providers[best_idx]

    def train_on_data(self, data: List[Dict]):
        """
        Train AI model on performance data

        Args:
            data: List of dicts with 'signal', 'latency', 'error', 'provider'
        """
        if self.model is None:
            return

        logger.info(f"🧠 Training AI auf {len(data)} Datenpunkten...")

        for d in data:
            input_tensor = torch.tensor(
                [[d["signal"], d["latency"], d["error"]]], dtype=torch.float32
            )

            # One-hot target für Provider
            target = torch.tensor(
                [
                    [
                        1.0 if d["provider"] == "starlink" else 0.0,
                        1.0 if d["provider"] == "iridium" else 0.0,
                        1.0 if d["provider"] == "globalstar" else 0.0,
                    ]
                ]
            )

            # Training step
            output = self.model(input_tensor)
            loss = nn.MSELoss()(output, target)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        logger.info("✅ AI-Modell trainiert!")


class SatelliteBridge:
    """
    Satelliten-Bridge für globale Kommunikation

    Unterstützt:
    - Starlink
    - Iridium
    - Globalstar
    - Multi-Provider Fallback
    - AI-basierte Provider-Auswahl

    Features:
    - MQTT-basierte Kommunikation
    - Message Buffering bei Ausfall
    - Automatisches Retry
    - Provider-Switching mit AI
    - Performance Metrics Tracking
    """

    def __init__(self):
        """Initialize Satellite Bridge"""
        if not MQTT_AVAILABLE:
            logger.warning(
                "paho-mqtt nicht installiert - Satellite-Features nicht verfügbar"
            )

        self.satellite_providers = {
            "starlink": {"broker": "mqtt.starlink.com", "port": 1883},
            "iridium": {"broker": "mqtt.iridium.com", "port": 1883},
            "globalstar": {"broker": "mqtt.globalstar.com", "port": 1883},
        }
        self.active_provider: Optional[str] = None
        self.message_buffer: List[Dict] = []
        self.bridge_status = "disconnected"
        self.client = None

        # AI Optimization
        self.ai_optimizer = AIOptimizer()
        self.performance_metrics = {
            p: {"signal": 0.5, "latency": 0.0, "error_rate": 0.0}
            for p in self.satellite_providers
        }

    def connect_satellite(self, provider: str = "starlink") -> bool:
        """
        Verbinde zu Satelliten-Provider mit AI-Optimierung

        Args:
            provider: Provider-Name ('starlink', 'iridium', 'globalstar')

        Returns:
            True wenn erfolgreich verbunden
        """
        if not MQTT_AVAILABLE:
            logger.error("MQTT nicht verfügbar - installiere: pip install paho-mqtt")
            return False

        # AI-basierte Provider-Empfehlung
        if self.ai_optimizer.model:
            metrics = self.performance_metrics[provider]
            best = self.ai_optimizer.predict_best_provider(
                metrics["signal"], metrics["latency"], metrics["error_rate"]
            )
            if best != provider:
                logger.info(f"🧠 AI empfiehlt Wechsel: {provider} → {best}")
                provider = best

        if provider not in self.satellite_providers:
            logger.error(f"Unbekannter Provider: {provider}")
            return False

        try:
            config = self.satellite_providers[provider]
            self.client = mqtt.Client()
            self.client.on_connect = self._on_satellite_connect
            self.client.on_message = self._on_satellite_message
            self.client.on_disconnect = self._on_satellite_disconnect

            # Latenz messen
            start_time = time.time()
            self.client.connect(config["broker"], config["port"], 30)
            self.client.loop_start()
            latency = time.time() - start_time

            # Update Performance Metrics
            self.performance_metrics[provider]["latency"] = latency

            self.active_provider = provider
            logger.info(f"🛰️ Verbinde zu {provider} (Latenz: {latency:.2f}s)...")
            return True

        except Exception as e:
            # Update Error Rate
            self.performance_metrics[provider]["error_rate"] += 0.1
            logger.error(f"Satelliten-Verbindungsfehler: {e}")
            return False

    def _on_satellite_connect(self, client, userdata, flags, rc):
        """Callback für erfolgreiche Verbindung"""
        if rc == 0:
            self.bridge_status = "connected"
            logger.info(f"🌐 Verbunden mit {self.active_provider} Satellite")
            client.subscribe("luca/global/#")
            # Gebufferte Nachrichten senden
            self._flush_buffer()
        else:
            self.bridge_status = "failed"
            logger.error(f"Satelliten-Verbindung fehlgeschlagen: {rc}")
            if self.active_provider:
                self.performance_metrics[self.active_provider]["error_rate"] += 0.2

    def _on_satellite_message(self, client, userdata, msg):
        """
        Empfange Nachrichten von Satelliten-Netzwerk

        Args:
            client: MQTT client
            userdata: User data
            msg: MQTT message
        """
        try:
            message = json.loads(msg.payload.decode())
            logger.info(f"🛰️ Satelliten-Nachricht: {message.get('type', 'unknown')}")
            return message
        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten der Satelliten-Nachricht: {e}")

    def _on_satellite_disconnect(self, client, userdata, rc):
        """Callback für Verbindungsabbruch"""
        self.bridge_status = "disconnected"
        logger.warning("📡 Satelliten-Verbindung unterbrochen")

        # Update Error Rate
        if self.active_provider:
            self.performance_metrics[self.active_provider]["error_rate"] += 0.1

    def send_via_satellite(self, message: Dict) -> bool:
        """
        Sende Nachricht via Satellit mit Performance-Tracking

        Args:
            message: Message dictionary mit 'type', 'content', 'region' etc.

        Returns:
            True wenn erfolgreich gesendet
        """
        if not MQTT_AVAILABLE or not self.client:
            self.message_buffer.append(message)
            return False

        if self.bridge_status != "connected":
            self.message_buffer.append(message)
            logger.warning("🔴 Nicht verbunden - Nachricht gebuffert")
            return False

        try:
            topic = f"luca/global/{message.get('region', 'global')}"

            # Latenz messen
            start_time = time.time()
            self.client.publish(topic, json.dumps(message))
            latency = time.time() - start_time

            # Update Performance Metrics (gleitender Durchschnitt)
            if self.active_provider:
                current_latency = self.performance_metrics[self.active_provider][
                    "latency"
                ]
                self.performance_metrics[self.active_provider]["latency"] = (
                    current_latency + latency
                ) / 2

            logger.info(
                f"📡 Via {self.active_provider} gesendet: {message.get('type')} (Latenz: {latency:.3f}s)"
            )
            return True
        except Exception as e:
            logger.error(f"Satelliten-Sende-Fehler: {e}")
            if self.active_provider:
                self.performance_metrics[self.active_provider]["error_rate"] += 0.1
            self.message_buffer.append(message)
            return False

    def _flush_buffer(self):
        """Sende gebufferte Nachrichten"""
        if not self.message_buffer:
            return

        logger.info(f"📤 Sende {len(self.message_buffer)} gebufferte Nachrichten...")
        for message in self.message_buffer[:]:
            if self.send_via_satellite(message):
                self.message_buffer.remove(message)

    def disconnect(self):
        """Trenne Satelliten-Verbindung"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.bridge_status = "disconnected"
            logger.info("📡 Satelliten-Verbindung getrennt")

    def train_ai(self):
        """
        Trainiere AI-Optimizer mit aktuellen Performance-Daten
        """
        if not self.ai_optimizer.model:
            logger.warning("AI nicht verfügbar - kein Training möglich")
            return

        # Konvertiere Performance-Metrics zu Training-Daten
        training_data = []
        for provider, metrics in self.performance_metrics.items():
            training_data.append(
                {
                    "signal": metrics["signal"],
                    "latency": min(metrics["latency"], 10.0),  # Cap bei 10s
                    "error": min(metrics["error_rate"], 1.0),  # Cap bei 100%
                    "provider": provider,
                }
            )

        self.ai_optimizer.train_on_data(training_data)

    def get_status(self) -> Dict:
        """
        Hole Satellite-Status mit Performance-Metrics

        Returns:
            Dictionary mit Status-Informationen
        """
        status = {
            "provider": self.active_provider,
            "status": self.bridge_status,
            "buffered_messages": len(self.message_buffer),
            "mqtt_available": MQTT_AVAILABLE,
            "ai_available": TORCH_AVAILABLE,
            "performance_metrics": self.performance_metrics,
        }

        # AI-Empfehlung
        if self.ai_optimizer.model and self.active_provider:
            metrics = self.performance_metrics[self.active_provider]
            best = self.ai_optimizer.predict_best_provider(
                metrics["signal"], metrics["latency"], metrics["error_rate"]
            )
            status["ai_recommendation"] = best

        return status


class SatelliteMessageRelay:
    """
    Relay für automatische Satellite-Weiterleitung

    Features:
    - Automatisches Relay wichtiger Nachrichten
    - Priorisierung nach Message-Type
    - Batch-Processing für Effizienz
    - AI-Training im Hintergrund
    """

    def __init__(self, satellite_bridge: SatelliteBridge):
        """
        Initialize Message Relay

        Args:
            satellite_bridge: SatelliteBridge instance
        """
        self.bridge = satellite_bridge
        self.relay_queue: List[Dict] = []
        self.priority_types = ["emergency", "critical", "broadcast"]

        # Start relay thread
        self.relay_thread = threading.Thread(target=self._relay_loop, daemon=True)
        self.relay_thread.start()

    def queue_for_relay(self, message: Dict, priority: bool = False):
        """
        Queue message for satellite relay

        Args:
            message: Message dictionary
            priority: Whether message has high priority
        """
        message["relay_priority"] = priority
        message["queued_at"] = datetime.now().isoformat()

        if priority:
            self.relay_queue.insert(0, message)  # Priority at front
        else:
            self.relay_queue.append(message)

    def _relay_loop(self):
        """Background relay processing mit AI-Training"""
        ai_training_counter = 0

        while True:
            try:
                if self.relay_queue and self.bridge.bridge_status == "connected":
                    message = self.relay_queue.pop(0)
                    self.bridge.send_via_satellite(message)

                # AI-Training alle 100 Iterationen
                ai_training_counter += 1
                if ai_training_counter >= 100:
                    self.bridge.train_ai()
                    ai_training_counter = 0

                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Relay loop error: {e}")


# Convenience Functions


def create_satellite_enabled_mesh(node_name: str = "LUCA_Satellite_Node"):
    """
    Create mesh network with satellite capability

    Args:
        node_name: Name of the node

    Returns:
        Tuple of (mesh, satellite_bridge)

    Example:
        >>> mesh, satellite = create_satellite_enabled_mesh("MyNode")
        >>> satellite.connect_satellite("starlink")
        >>> # Send message via satellite
    """
    from luca_369_370.meshtastic.mesh_network import LucaMeshNetwork

    mesh = LucaMeshNetwork(node_name=node_name)
    satellite = SatelliteBridge()

    return mesh, satellite


def broadcast_globally(message: str, satellite_bridge: SatelliteBridge) -> bool:
    """
    Broadcast message globally via satellite

    Args:
        message: Message to broadcast
        satellite_bridge: SatelliteBridge instance

    Returns:
        True if broadcast successful
    """
    broadcast_msg = {
        "type": "global_broadcast",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "region": "global",
    }

    return satellite_bridge.send_via_satellite(broadcast_msg)
