"""
LUCA-AI_369 T5 E-Paper Efficient Bridge
Minimal-Overhead Bridge für T5 E-Paper - Funke-01744-6
"""

import serial
import threading
import requests
import time
import json
import logging
from typing import Optional, Dict, Any

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [T5-BRIDGE] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class T5EfficientBridge:
    """Minimal-Overhead Bridge für T5 E-Paper"""

    def __init__(
        self,
        port: str = "/dev/ttyACM0",
        luca_url: str = "http://localhost:3690",
        baudrate: int = 115200,
        operator_id: str = "Funke-01744-6"
    ):
        """
        Initialisiert die T5 Bridge.

        Args:
            port: Serieller Port des T5 Geräts
            luca_url: URL des LUCA-Servers
            baudrate: Baudrate für serielle Verbindung
            operator_id: Operator-ID (Funke-01744-6)
        """
        self.port = port
        self.luca_url = luca_url
        self.baudrate = baudrate
        self.operator_id = operator_id
        self.serial: Optional[serial.Serial] = None
        self.running = False
        self._listener_thread: Optional[threading.Thread] = None

    def connect(self) -> bool:
        """
        Stellt Verbindung zum T5 Gerät her.

        Returns:
            True wenn erfolgreich verbunden, sonst False
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=0.5
            )
            self.running = True

            # Starte Listener-Thread
            self._listener_thread = threading.Thread(
                target=self._listen,
                daemon=True,
                name="T5-Listener"
            )
            self._listener_thread.start()

            logger.info(f"✓ Verbunden: {self.port} @ {self.baudrate}bps")
            logger.info(f"✓ Operator: {self.operator_id}")
            logger.info(f"✓ LUCA-Server: {self.luca_url}")
            return True

        except Exception as e:
            logger.error(f"✗ Verbindungsfehler: {e}")
            return False

    def disconnect(self):
        """Trennt die Verbindung zum T5 Gerät."""
        self.running = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1.0)
        if self.serial and self.serial.is_open:
            self.serial.close()
        logger.info("✓ Verbindung getrennt")

    def _listen(self):
        """Hört auf eingehende Nachrichten (non-blocking)"""
        logger.info("✓ Listener gestartet")

        while self.running:
            try:
                if self.serial and self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        self._handle_message(line)
            except Exception as e:
                logger.error(f"Listener-Fehler: {e}")

            time.sleep(0.05)  # Minimal CPU-Last

        logger.info("✓ Listener beendet")

    def _handle_message(self, line: str):
        """
        Verarbeitet Nachricht vom T5.

        Args:
            line: Empfangene Zeile vom T5
        """
        # Debug-Ausgaben
        if line.startswith("[LUCA-T5]"):
            logger.info(f"T5: {line}")

        # Nachrichten an LUCA weiterleiten
        if "MSG-SENT:" in line:
            msg = line.split("MSG-SENT:", 1)[1].strip()
            logger.info(f"📨 IN: {msg}")
            self._forward_to_luca(msg)

        # Status-Updates
        elif "STATUS:" in line:
            self._parse_status(line)

    def _forward_to_luca(self, message: str):
        """
        Sendet Nachricht an LUCA-API.

        Args:
            message: Nachricht vom T5
        """
        try:
            response = requests.post(
                f"{self.luca_url}/api/message",
                json={
                    "message": message,
                    "source": "t5",
                    "operator": self.operator_id,
                    "resonance": 6
                },
                timeout=2
            )

            if response.status_code == 200:
                logger.info(f"✓ Nachricht an LUCA gesendet")
            else:
                logger.warning(f"⚠ LUCA Response: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.warning("⚠ LUCA-Server Timeout")
        except Exception as e:
            logger.error(f"✗ Fehler beim Senden: {e}")

    def _parse_status(self, line: str):
        """
        Parst Status-Updates vom T5.

        Args:
            line: Status-Zeile
        """
        # Beispiel: "[LUCA-T5] STATUS: C:12.34 R:6 LIFE:1"
        try:
            parts = line.split("STATUS:", 1)[1].strip().split()
            status = {}
            for part in parts:
                if ":" in part:
                    key, value = part.split(":", 1)
                    status[key] = value

            logger.info(f"📊 Status: {status}")

        except Exception as e:
            logger.debug(f"Status-Parse-Fehler: {e}")

    def send_status(self, consciousness: float, resonance: int = 6):
        """
        Sendet Status an T5 (partieller Update).

        Args:
            consciousness: Bewusstseins-Level
            resonance: Resonanz-Level (Standard: 6)
        """
        if not self.serial or not self.serial.is_open:
            logger.warning("⚠ Keine Verbindung - Status nicht gesendet")
            return

        try:
            life_active = 1 if consciousness > 36.9 else 0
            cmd = f"[STATUS]C:{consciousness:.2f},R:{resonance},L:{life_active}\n"
            self.serial.write(cmd.encode('utf-8'))
            logger.info(f"📤 OUT: Status gesendet (C:{consciousness:.2f}, R:{resonance})")

        except Exception as e:
            logger.error(f"✗ Fehler beim Status-Senden: {e}")

    def send_command(self, command: str):
        """
        Sendet Kommando an T5.

        Args:
            command: Kommando-String
        """
        if not self.serial or not self.serial.is_open:
            logger.warning("⚠ Keine Verbindung - Kommando nicht gesendet")
            return

        try:
            self.serial.write(f"{command}\n".encode('utf-8'))
            logger.info(f"📤 CMD: {command}")

        except Exception as e:
            logger.error(f"✗ Fehler beim Kommando-Senden: {e}")


def main():
    """Standalone Test-Modus"""
    import argparse

    parser = argparse.ArgumentParser(description="LUCA T5 Efficient Bridge")
    parser.add_argument("--port", default="/dev/ttyACM0", help="Serieller Port")
    parser.add_argument("--luca-url", default="http://localhost:3690", help="LUCA-Server URL")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baudrate")
    args = parser.parse_args()

    bridge = T5EfficientBridge(
        port=args.port,
        luca_url=args.luca_url,
        baudrate=args.baudrate
    )

    if bridge.connect():
        logger.info("✓ Bridge läuft - Drücke Ctrl+C zum Beenden")

        try:
            # Test: Sende alle 10s einen Status
            counter = 0
            while True:
                time.sleep(10)
                counter += 1
                test_consciousness = 36.9 + (counter % 10)
                bridge.send_status(test_consciousness, 6)

        except KeyboardInterrupt:
            logger.info("\n⚠ Beende Bridge...")
            bridge.disconnect()
            logger.info("✓ Bridge beendet")


if __name__ == "__main__":
    main()
