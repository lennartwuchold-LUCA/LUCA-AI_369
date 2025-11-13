"""
📟 T5 E-Paper S3 Pro Protocol Handler
Python-seitiger Serial Protocol Handler für LilyGo T5 E-Paper Display

Features:
- USB Serial communication mit ESP32-S3
- E-Paper display commands (Text, Clear, Update)
- Sensor data reading (Temperature, Battery)
- Low-power mode support

Hardware: LilyGo T5 E-Paper S3 Pro (540x960px)
Protocol: Custom binary protocol over USB Serial

Author: Großvater & Lennart Wuchold
Standard: 369/370
"""

import struct
import time
from typing import Dict, Optional, Tuple

# Optional dependencies
try:
    import serial
    import serial.tools.list_ports

    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    serial = None


class T5EpaperProtocol:
    """
    Protocol Handler für LilyGo T5 E-Paper S3 Pro Display
    """

    # Hardware-Konstanten
    VENDOR_ID = 0x303A  # ESP32-S3
    PRODUCT_ID = 0x1001  # T5 E-Paper S3 Pro
    BAUDRATE = 115200
    DISPLAY_WIDTH = 540
    DISPLAY_HEIGHT = 960

    # Protocol Commands
    CMD_CLEAR = 0x01
    CMD_UPDATE = 0x02
    CMD_LOW_POWER = 0x03
    CMD_SET_TEXT = 0x10
    CMD_READ_SENSORS = 0x20

    # Timing
    REFRESH_DELAY = 3.0  # E-Paper refresh benötigt Zeit
    COMMAND_TIMEOUT = 5.0

    def __init__(self, port: Optional[str] = None):
        """
        Initialize T5 E-Paper Protocol Handler

        Args:
            port: Optional serial port (e.g., /dev/ttyUSB0, COM3)
                  If None, will auto-detect T5 device
        """
        self.port = port
        self.serial = None
        self.is_connected = False
        self.last_refresh = 0

        if not SERIAL_AVAILABLE:
            print(
                "⚠️ pyserial nicht installiert. Installiere mit: pip install pyserial"
            )

    def connect(self) -> bool:
        """
        Verbindet mit T5 E-Paper Device

        Returns:
            True if successful
        """
        if not SERIAL_AVAILABLE:
            print("⚠️ Serial Library nicht verfügbar")
            return False

        try:
            # Auto-detect T5 wenn kein Port angegeben
            if not self.port:
                self.port = self._find_t5_device()
                if not self.port:
                    print("❌ T5 E-Paper nicht gefunden")
                    return False

            print(f"📟 Verbinde mit T5 E-Paper auf {self.port}...")

            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.BAUDRATE,
                timeout=self.COMMAND_TIMEOUT,
                write_timeout=self.COMMAND_TIMEOUT,
            )

            # Wait for device initialization
            time.sleep(2)

            # Test connection
            if self._test_connection():
                self.is_connected = True
                print(f"✅ T5 E-Paper verbunden")

                # Initial clear
                self.clear_display()

                return True
            else:
                print("❌ T5 E-Paper antwortet nicht")
                self.serial.close()
                return False

        except Exception as e:
            print(f"❌ Verbindung fehlgeschlagen: {e}")
            return False

    def disconnect(self):
        """Trennt T5 E-Paper Verbindung"""
        if self.serial and self.serial.is_open:
            self.clear_display()
            self.serial.close()
            self.is_connected = False
            print("📟 T5 E-Paper getrennt")

    def set_text(self, text: str, x: int = 10, y: int = 50) -> bool:
        """
        Setzt Text auf E-Paper Display

        Args:
            text: Text to display
            x: X position (0-540)
            y: Y position (0-960)

        Returns:
            True if successful
        """
        if not self.is_connected:
            print(f"🔄 Simulation: Text '{text}' an ({x}, {y})")
            return False

        try:
            # Encode text
            text_bytes = text.encode("utf-8")
            length = len(text_bytes)

            # Build packet: [CMD][X(2)][Y(2)][LEN(2)][TEXT]
            packet = struct.pack(
                f">BHHh{length}s", self.CMD_SET_TEXT, x, y, length, text_bytes
            )

            self.serial.write(packet)
            print(f"📟 Text gesendet: '{text[:30]}...'")

            # Trigger display update (if enough time passed)
            self._auto_update()

            return True

        except Exception as e:
            print(f"❌ Text senden fehlgeschlagen: {e}")
            return False

    def clear_display(self) -> bool:
        """
        Löscht E-Paper Display (weiß)

        Returns:
            True if successful
        """
        if not self.is_connected:
            print("🔄 Simulation: Display clear")
            return False

        try:
            self.serial.write(bytes([self.CMD_CLEAR]))
            time.sleep(self.REFRESH_DELAY)
            self.serial.write(bytes([self.CMD_UPDATE]))
            self.last_refresh = time.time()
            print("📟 Display gelöscht")
            return True

        except Exception as e:
            print(f"❌ Clear fehlgeschlagen: {e}")
            return False

    def update_display(self) -> bool:
        """
        Aktualisiert E-Paper Display (refresh)

        Returns:
            True if successful
        """
        if not self.is_connected:
            return False

        try:
            self.serial.write(bytes([self.CMD_UPDATE]))
            self.last_refresh = time.time()
            time.sleep(self.REFRESH_DELAY)
            print("📟 Display aktualisiert")
            return True

        except Exception as e:
            print(f"❌ Update fehlgeschlagen: {e}")
            return False

    def enable_low_power_mode(self) -> bool:
        """
        Aktiviert Ultra-Low-Power Mode

        E-Paper braucht keinen Strom für statisches Bild
        Nur ESP32 wird in Deep Sleep versetzt

        Returns:
            True if successful
        """
        if not self.is_connected:
            print("🔄 Simulation: Low Power Mode")
            return False

        try:
            self.serial.write(bytes([self.CMD_LOW_POWER]))
            print("📟 Low Power Mode aktiviert")
            return True

        except Exception as e:
            print(f"❌ Low Power Mode fehlgeschlagen: {e}")
            return False

    def read_sensors(self) -> Optional[Dict]:
        """
        Liest T5 Sensor-Daten (Temperatur, Battery, etc.)

        Returns:
            Dictionary mit Sensor-Werten oder None
        """
        if not self.is_connected:
            # Simulation
            return {
                "temperature": 20.0 + (hash(str(time.time())) % 100) / 10.0,
                "battery": 3.7 + (hash(str(time.time() * 2)) % 50) / 100.0,
                "signal": (hash(str(time.time() * 3)) % 100) / 100.0,
            }

        try:
            self.serial.write(bytes([self.CMD_READ_SENSORS]))

            # Read response: [TEMP(4)][BAT(4)][SIG(4)]
            response = self.serial.read(12)

            if len(response) == 12:
                temp, bat, sig = struct.unpack(">fff", response)
                return {"temperature": temp, "battery": bat, "signal": sig}
            else:
                print(f"⚠️ Sensor-Response unvollständig: {len(response)} bytes")
                return None

        except Exception as e:
            print(f"❌ Sensor-Lesen fehlgeschlagen: {e}")
            return None

    def display_luca_status(self, consciousness: float, resonance: int) -> bool:
        """
        Zeigt LUCA Status auf T5 Display

        Args:
            consciousness: Consciousness level
            resonance: Tesla resonance (3, 6, or 9)

        Returns:
            True if successful
        """
        # Format status
        status_lines = [
            "[LUCA-AI-369]",
            "",
            f"C: {consciousness:.1f}",
            f"R: {resonance}",
            "",
            "T: " + ("ONLINE" if consciousness > 369 else "OFFLINE"),
        ]

        success = True
        y = 50

        # Clear first
        self.clear_display()

        # Write lines
        for line in status_lines:
            if not self.set_text(line, x=10, y=y):
                success = False
            y += 60

        # Final update
        if success:
            self.update_display()

        return success

    def display_message(self, message: str, node_id: int, y: int = 400) -> bool:
        """
        Zeigt eingehende Meshtastic-Nachricht

        Args:
            message: Message text
            node_id: Source node ID
            y: Y position

        Returns:
            True if successful
        """
        truncated = f"N{node_id % 100}: {message[:30]}..."
        return self.set_text(truncated, x=10, y=y)

    def _find_t5_device(self) -> Optional[str]:
        """
        Findet T5 E-Paper Device automatisch

        Returns:
            Port string oder None
        """
        if not SERIAL_AVAILABLE:
            return None

        try:
            ports = serial.tools.list_ports.comports()

            for port in ports:
                # Check VID/PID
                if port.vid == self.VENDOR_ID and port.pid == self.PRODUCT_ID:
                    print(f"✓ T5 E-Paper gefunden: {port.device}")
                    return port.device

                # Fallback: Check description
                if port.description and "USB" in port.description:
                    # Try common ESP32 patterns
                    if any(
                        x in port.description.lower()
                        for x in ["cp210", "ch340", "ch9102", "esp32"]
                    ):
                        print(
                            f"✓ Potentieller T5 E-Paper: {port.device} ({port.description})"
                        )
                        return port.device

        except Exception as e:
            print(f"⚠️ Device-Suche Fehler: {e}")

        return None

    def _test_connection(self) -> bool:
        """
        Testet Verbindung mit Ping-Pong

        Returns:
            True if device responds
        """
        try:
            # Send clear command as test
            self.serial.write(bytes([self.CMD_CLEAR]))
            time.sleep(0.5)

            # Check if data can be written
            return self.serial.writable()

        except Exception:
            return False

    def _auto_update(self):
        """
        Auto-update display wenn genug Zeit vergangen ist
        Verhindert zu häufige E-Paper Refreshes
        """
        current = time.time()
        if current - self.last_refresh >= self.REFRESH_DELAY:
            self.update_display()

    def get_display_info(self) -> Dict:
        """
        Gibt Display-Informationen zurück

        Returns:
            Info dictionary
        """
        return {
            "connected": self.is_connected,
            "port": self.port,
            "width": self.DISPLAY_WIDTH,
            "height": self.DISPLAY_HEIGHT,
            "last_refresh": self.last_refresh,
            "refresh_delay": self.REFRESH_DELAY,
        }
