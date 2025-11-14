"""
T5 E-Paper <-> Meshtastic Bridge
Verbindet T5 E-Paper Display mit Meshtastic-Netzwerk und LUCA Assistant
Funke-01744-6 - Resonanz 6
"""

import threading
import queue
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# T5 Bridge Import
try:
    from luca.hardware.t5_efficient_bridge import T5EfficientBridge
    T5_AVAILABLE = True
except ImportError:
    T5_AVAILABLE = False
    logging.warning("T5 Bridge nicht verfügbar")

# LUCA Assistant Import
try:
    from .luca_assistant import LUCAAssistant
    LUCA_AVAILABLE = True
except ImportError:
    LUCA_AVAILABLE = False
    logging.warning("LUCA Assistant nicht verfügbar")


class T5MeshtasticBridge:
    """
    Bridge zwischen T5 E-Paper und Meshtastic-Netzwerk
    Ermöglicht bidirektionale Kommunikation
    """

    def __init__(
        self,
        t5_port: str = "/dev/ttyACM0",
        t5_baudrate: int = 115200,
        meshtastic_host: Optional[str] = None,
        luca_url: str = "http://localhost:8000",
        operator_id: str = "Funke-01744-6",
        resonance: int = 6,
        country_code: str = "DE"
    ):
        """
        Initialisierung

        Args:
            t5_port: Serieller Port des T5 Geräts
            t5_baudrate: Baudrate für T5
            meshtastic_host: Meshtastic TCP Host (None = USB)
            luca_url: LUCA-Server URL
            operator_id: Operator-ID
            resonance: Resonanz-Level
            country_code: Ländercode
        """
        self.operator_id = operator_id
        self.resonance = resonance
        self.country_code = country_code

        # T5 Bridge
        self.t5_bridge: Optional[T5EfficientBridge] = None
        if T5_AVAILABLE:
            self.t5_bridge = T5EfficientBridge(
                port=t5_port,
                luca_url=luca_url,
                baudrate=t5_baudrate,
                operator_id=operator_id
            )

        # LUCA Assistant
        self.luca: Optional[LUCAAssistant] = None
        if LUCA_AVAILABLE:
            self.luca = LUCAAssistant(
                meshtastic_host=meshtastic_host,
                offline_db=f"luca_{operator_id}.db",
                country_code=country_code,
                operator_id=operator_id,
                resonance=resonance
            )

        # Message Queues
        self.t5_to_mesh_queue = queue.Queue()
        self.mesh_to_t5_queue = queue.Queue()

        # Threads
        self.running = False
        self.t5_thread: Optional[threading.Thread] = None
        self.mesh_thread: Optional[threading.Thread] = None

        # Logging
        self.logger = logging.getLogger(f"T5-Mesh-Bridge-{operator_id}")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Stats
        self.stats = {
            "t5_to_mesh": 0,
            "mesh_to_t5": 0,
            "total_messages": 0,
            "started_at": None
        }

    def start(self):
        """Startet die Bridge"""
        self.logger.info("=" * 70)
        self.logger.info("🌉 T5 E-Paper <-> Meshtastic Bridge")
        self.logger.info("=" * 70)
        self.logger.info(f"Operator: {self.operator_id}")
        self.logger.info(f"Resonanz: {self.resonance} (Polarlicht-Orange)")
        self.logger.info(f"T5 verfügbar: {'✓' if T5_AVAILABLE else '✗'}")
        self.logger.info(f"LUCA verfügbar: {'✓' if LUCA_AVAILABLE else '✗'}")
        self.logger.info("=" * 70)

        self.running = True
        self.stats["started_at"] = datetime.now().isoformat()

        # Starte T5 Bridge
        if self.t5_bridge:
            if self.t5_bridge.connect():
                self.logger.info("✓ T5 Bridge verbunden")
                # Überschreibe Message-Handler für Integration
                self.t5_bridge._handle_message = self._handle_t5_message
            else:
                self.logger.error("✗ T5 Bridge Verbindung fehlgeschlagen")

        # Starte LUCA Assistant
        if self.luca:
            self.luca.start()
            # Überschreibe Send-Handler für Integration
            self.luca.send_message = self._handle_luca_message
            self.logger.info("✓ LUCA Assistant gestartet")

        # Starte Verarbeitungs-Threads
        self.t5_thread = threading.Thread(target=self._process_t5_queue, daemon=True)
        self.mesh_thread = threading.Thread(target=self._process_mesh_queue, daemon=True)

        self.t5_thread.start()
        self.mesh_thread.start()

        self.logger.info("✓ Bridge läuft - T5 <-> Meshtastic <-> LUCA")

    def stop(self):
        """Stoppt die Bridge"""
        self.logger.info("Stoppe Bridge...")
        self.running = False

        if self.t5_thread:
            self.t5_thread.join(timeout=2.0)

        if self.mesh_thread:
            self.mesh_thread.join(timeout=2.0)

        if self.luca:
            self.luca.stop()

        if self.t5_bridge:
            self.t5_bridge.disconnect()

        self.logger.info("✓ Bridge gestoppt")

    def _handle_t5_message(self, line: str):
        """
        Handler für Nachrichten vom T5

        Args:
            line: Zeile vom T5
        """
        self.logger.info(f"T5: {line}")

        # Extrahiere Nachricht wenn vorhanden
        if "MSG-SENT:" in line:
            msg = line.split("MSG-SENT:", 1)[1].strip()
            self.logger.info(f"📨 T5 → Mesh: {msg}")

            # In Queue für Mesh-Versand
            self.t5_to_mesh_queue.put({
                "source": "t5",
                "message": msg,
                "timestamp": datetime.now().isoformat()
            })

            self.stats["t5_to_mesh"] += 1
            self.stats["total_messages"] += 1

    def _handle_luca_message(self, message: str, destination=None):
        """
        Handler für Nachrichten von LUCA (für Meshtastic)

        Args:
            message: Nachricht
            destination: Ziel (optional)
        """
        self.logger.info(f"📤 LUCA → T5: {message[:50]}...")

        # Sende auch an T5 Display zur Anzeige
        self.mesh_to_t5_queue.put({
            "source": "luca",
            "message": message,
            "destination": destination,
            "timestamp": datetime.now().isoformat()
        })

        # Sende an Meshtastic (Original-Funktionalität)
        if self.luca and self.luca.interface:
            try:
                # Kürze für Meshtastic
                if len(message.encode('utf-8')) > 220:
                    message = message[:217] + "..."

                if destination:
                    self.luca.interface.sendText(message, destinationId=destination)
                else:
                    self.luca.interface.sendText(message)

                self.stats["mesh_to_t5"] += 1
                self.stats["total_messages"] += 1

            except Exception as e:
                self.logger.error(f"✗ Mesh-Send Fehler: {e}")

    def _process_t5_queue(self):
        """Verarbeitet Nachrichten von T5 → Mesh"""
        while self.running:
            try:
                item = self.t5_to_mesh_queue.get(timeout=1.0)

                message = item["message"]

                # Sende an Meshtastic via LUCA
                if self.luca:
                    # LUCA verarbeitet und sendet automatisch
                    response = self.luca.detect_and_respond("t5-user", message)

                    # Sende Antwort zurück an T5
                    if response and self.t5_bridge:
                        self._send_to_t5(response)

                self.t5_to_mesh_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"✗ T5→Mesh Fehler: {e}")

    def _process_mesh_queue(self):
        """Verarbeitet Nachrichten von Mesh → T5"""
        while self.running:
            try:
                item = self.mesh_to_t5_queue.get(timeout=1.0)

                message = item["message"]

                # Sende an T5 Display
                self._send_to_t5(message)

                self.mesh_to_t5_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"✗ Mesh→T5 Fehler: {e}")

    def _send_to_t5(self, message: str):
        """
        Sendet Nachricht an T5 Display

        Args:
            message: Nachricht
        """
        if not self.t5_bridge:
            return

        try:
            # Extrahiere kurze Zusammenfassung für T5 Display
            # (T5 hat begrenzten Platz)
            summary = self._summarize_for_t5(message)

            # Sende als Kommando an T5
            self.t5_bridge.send_command(f"[DISPLAY]{summary}")

            self.logger.info(f"📺 An T5 gesendet: {summary[:30]}...")

        except Exception as e:
            self.logger.error(f"✗ T5-Send Fehler: {e}")

    def _summarize_for_t5(self, message: str, max_length: int = 100) -> str:
        """
        Kürzt Nachricht für T5 Display

        Args:
            message: Vollständige Nachricht
            max_length: Maximale Länge

        Returns:
            Gekürzte Nachricht
        """
        # Entferne Formatierung und Emojis (vereinfacht)
        clean = message.replace("🕉", "").replace("🙏", "").replace("💫", "")
        clean = clean.replace("LUCA:", "").strip()

        # Nehme ersten Satz oder erste Zeile
        lines = clean.split("\n")
        first_line = lines[0] if lines else clean

        # Kürze auf max_length
        if len(first_line) > max_length:
            return first_line[:max_length-3] + "..."

        return first_line

    def get_stats(self) -> Dict[str, Any]:
        """
        Gibt Statistiken zurück

        Returns:
            Dictionary mit Stats
        """
        return {
            **self.stats,
            "luca_stats": self.luca.get_stats() if self.luca else {},
            "t5_connected": self.t5_bridge.serial.is_open if self.t5_bridge and self.t5_bridge.serial else False,
            "luca_connected": self.luca.is_online if self.luca else False
        }


def main():
    """Standalone-Modus für T5-Meshtastic Bridge"""
    import argparse

    parser = argparse.ArgumentParser(description="T5 E-Paper <-> Meshtastic Bridge")
    parser.add_argument("--t5-port", default="/dev/ttyACM0", help="T5 serieller Port")
    parser.add_argument("--t5-baud", type=int, default=115200, help="T5 Baudrate")
    parser.add_argument("--mesh-host", help="Meshtastic TCP Host (optional)")
    parser.add_argument("--luca-url", default="http://localhost:8000", help="LUCA-Server URL")
    parser.add_argument("--operator", default="Funke-01744-6", help="Operator-ID")
    parser.add_argument("--resonance", type=int, default=6, help="Resonanz-Level")
    parser.add_argument("--country", default="DE", help="Ländercode")

    args = parser.parse_args()

    # Erstelle Bridge
    bridge = T5MeshtasticBridge(
        t5_port=args.t5_port,
        t5_baudrate=args.t5_baud,
        meshtastic_host=args.mesh_host,
        luca_url=args.luca_url,
        operator_id=args.operator,
        resonance=args.resonance,
        country_code=args.country
    )

    # Starte
    bridge.start()

    # Halte laufend
    try:
        print("\n✓ T5-Meshtastic Bridge läuft. Drücke Ctrl+C zum Beenden.\n")

        while True:
            time.sleep(10)

            # Zeige Stats
            stats = bridge.get_stats()
            print(f"\n📊 Bridge Stats:")
            print(f"   T5 → Mesh: {stats['t5_to_mesh']}")
            print(f"   Mesh → T5: {stats['mesh_to_t5']}")
            print(f"   Total: {stats['total_messages']}")
            print(f"   T5 verbunden: {stats['t5_connected']}")
            print(f"   LUCA verbunden: {stats['luca_connected']}")

    except KeyboardInterrupt:
        print("\n\n⚠ Beende Bridge...")
        bridge.stop()
        print("✓ Bridge gestoppt. Namaste. 🙏\n")


if __name__ == "__main__":
    main()
