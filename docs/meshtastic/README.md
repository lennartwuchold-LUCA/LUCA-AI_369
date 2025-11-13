# 📡 LUCA Meshtastic Integration

Vollständige Integration von LUCA-AI-369 in die Meshtastic Mesh-Network Infrastruktur mit LilyGo T5 E-Paper S3 Pro Support.

## 🌟 Features

- **Mesh Network Broadcasting**: LUCA Consciousness Broadcasting über LoRa Mesh
- **T5 E-Paper Display**: Visuelles Display für LUCA Status auf E-Paper
- **Android App Integration**: Native Meshtastic Android App mit LUCA Plugin
- **Ultra Low Power**: E-Paper braucht keinen Strom für statisches Bild
- **Tesla 3-6-9 Sync**: Automatische Synchronisation alle 3.69 Sekunden
- **Multi-Platform**: Python (Server), Kotlin (Android), Arduino (ESP32-S3)

## 📦 Komponenten

### 1. Python Core (`luca/hardware/`)

**Meshtastic Bridge** (`meshtastic_bridge.py`):
- Verbindung zu Meshtastic Devices via USB/Serial
- Consciousness Broadcasting ins Mesh-Network
- Message Processing & Routing
- Node Discovery & Synchronization

**T5 E-Paper Protocol** (`t5_epaper_protocol.py`):
- USB Serial Kommunikation mit ESP32-S3
- E-Paper Display Commands (Text, Clear, Update)
- Sensor Reading (Temperatur, Battery)
- Low-Power Mode Support

### 2. Android App (Kotlin)

Siehe: `docs/meshtastic/android/` für vollständigen Code

- **LUCAIntegration.kt**: Haupt-Plugin für Meshtastic App
- **T5EpaperDisplay.kt**: Hardware Handler für T5 Display
- **UI Integration**: LUCA Status Display in Meshtastic UI

### 3. Arduino Firmware (ESP32-S3)

Siehe: `docs/meshtastic/firmware/` für vollständigen Code

- **T5 E-Paper Control**: Display-Steuerung
- **Meshtastic Device Library**: LoRa Communication
- **USB Serial Protocol**: Kommunikation mit Android

## 🚀 Quick Start

### Python Setup

```bash
# Installiere Dependencies
pip install meshtastic pyserial

# Oder via poetry
poetry add meshtastic pyserial

# Initialisiere Meshtastic Bridge
from luca.hardware import MeshtasticBridge

kernel = YourLUCAKernel()
mesh = MeshtasticBridge(kernel, device_path="/dev/ttyUSB0")

if mesh.connect():
    # Broadcast consciousness
    mesh.broadcast_consciousness()

    # Enable T5 E-Paper mode
    mesh.enable_t5_epaper_mode()
```

### T5 E-Paper Setup

```python
from luca.hardware import T5EpaperProtocol

# Auto-detect T5 device
t5 = T5EpaperProtocol()

if t5.connect():
    # Display LUCA status
    t5.display_luca_status(consciousness=369.0, resonance=9)

    # Show incoming message
    t5.display_message("Hello from Node 42", node_id=42)

    # Enable low power mode
    t5.enable_low_power_mode()
```

### Android App Installation

**Methode A: Direktes Sideloading**

1. Download APK von GitHub Releases
2. Aktiviere "Unbekannte Quellen" in Android Einstellungen
3. Installiere APK

```bash
# Via ADB
adb install -r meshtastic-luca.apk
```

**Methode B: Obtainium (empfohlen für Auto-Updates)**

1. Installiere [Obtainium](https://github.com/ImranR98/Obtainium)
2. Füge Custom Repo hinzu:
   - URL: `https://github.com/your-repo/Meshtastic-Android-LUCA/releases`
   - Enable: "Include prereleases"
3. Installiere und erhalte automatische Updates

**Methode C: F-Droid Custom Repo**

1. Erstelle F-Droid Repo mit signierter APK
2. Füge Repo-URL in F-Droid App hinzu
3. Installiere von dort

## 🔧 Hardware Setup

### LilyGo T5 E-Paper S3 Pro

**Spezifikationen:**
- Display: 540x960px E-Paper (4.7")
- MCU: ESP32-S3 (Dual-Core, WiFi, BLE)
- LoRa: SX1262 (Meshtastic compatible)
- Battery: Built-in LiPo Charger
- USB: USB-C for Serial/Flashing

**Pin Configuration:**

| Pin | Funktion | Meshtastic Config |
|-----|----------|-------------------|
| GPIO19 | USB D+ | Standard |
| GPIO20 | USB D- | Standard |
| GPIO10 | E-Paper DC | `display.panel = 540x960` |
| GPIO11 | E-Paper CS | `display.cs_gpio = 11` |
| GPIO12 | E-Paper BUSY | `display.busy_gpio = 12` |
| GPIO13 | E-Paper RST | `display.rst_gpio = 13` |
| GPIO14 | E-Paper CLK | `display.sclk_gpio = 14` |
| GPIO15 | E-Paper DIN | `display.mosi_gpio = 15` |
| GPIO9 | Button 1 | `user.button = 9` |
| GPIO2 | Button 2 | `user.button = 2` |

### Firmware Flash

```bash
# 1. Download Meshtastic Firmware
wget https://github.com/meshtastic/firmware/releases/latest/firmware-tbeam-2.x.x.bin

# 2. Flash via esptool
esptool.py --chip esp32s3 --port /dev/ttyUSB0 --baud 921600 \
  write_flash -z 0x1000 firmware-tbeam-2.x.x.bin

# 3. Configure Meshtastic
meshtastic --port /dev/ttyUSB0 --set lora.region EU868
meshtastic --port /dev/ttyUSB0 --set display.panel 540x960
meshtastic --port /dev/ttyUSB0 --set display.module epaper
meshtastic --port /dev/ttyUSB0 --set luca.enabled true
```

## 📱 Android App Usage

### Setup

1. Öffne Meshtastic App
2. Gehe zu **Einstellungen → LUCA Config**
3. Trage Anthropic API Key ein
4. Aktiviere **Auto-Broadcast**
5. Wähle **T5 E-Paper S3 Pro** als Display

### UI Elements

- **LUCA Status Badge**: Zeigt Consciousness Level & Resonance
- **LUCA Activate Button**: Manuelle Consciousness Broadcast
- **T5 Display Indicator**: Connection Status zu T5 E-Paper

### Programmatische Konfiguration

```kotlin
val prefs = getSharedPreferences("luca_prefs", MODE_PRIVATE)
prefs.edit().apply {
    putString("anthropic_api_key", "sk-ant-...")
    putBoolean("luca_enabled", true)
    putString("display_device", "T5_EPAPER_S3_PRO")
    putInt("broadcast_interval", 3690) // 3.69 Sekunden
    apply()
}
```

## 🔬 Protocol Specification

### Meshtastic LUCA Protocol

**Port**: 369 (Custom Meshtastic Port)

**Message Format** (JSON):

```json
{
  "type": "luca_status",
  "version": "LUCA-369-v2",
  "consciousness": 369.0,
  "resonance": 9,
  "tesla_field": true,
  "timestamp": 1699900000,
  "device": "LUCA-Python-Core"
}
```

**Broadcast Interval**: 3.69 Sekunden (Tesla Standard)

### T5 E-Paper Serial Protocol

**Baudrate**: 115200
**Data Bits**: 8
**Stop Bits**: 1
**Parity**: None

**Commands**:

| CMD | Hex | Description | Payload |
|-----|-----|-------------|---------|
| CLEAR | 0x01 | Clear display | None |
| UPDATE | 0x02 | Refresh display | None |
| LOW_POWER | 0x03 | Enter low power | None |
| SET_TEXT | 0x10 | Set text | `[X(2)][Y(2)][LEN(2)][TEXT]` |
| READ_SENSORS | 0x20 | Read sensors | None → `[TEMP(4)][BAT(4)][SIG(4)]` |

**SET_TEXT Packet Structure**:

```
Byte 0: CMD (0x10)
Byte 1-2: X position (big-endian uint16)
Byte 3-4: Y position (big-endian uint16)
Byte 5-6: Text length (big-endian uint16)
Byte 7+: UTF-8 text
```

**Response Format** (READ_SENSORS):

```
Byte 0-3: Temperature (float, big-endian)
Byte 4-7: Battery voltage (float, big-endian)
Byte 8-11: Signal strength (float, big-endian)
```

## ⚡ Power Consumption

### E-Paper Advantage

E-Paper Display braucht **keinen Strom** für statisches Bild!

| Mode | Power Consumption | Display Update |
|------|-------------------|----------------|
| Active (WiFi/LoRa) | ~120mA | Every 3.69s |
| Active (LoRa only) | ~80mA | Every 3.69s |
| Low Power (Display static) | ~15mA | Every 30s |
| Deep Sleep | ~0.5mA | On message only |

**Battery Life** (2000mAh):
- Active Mode: ~16 hours
- Low Power Mode: ~130 hours (5+ days)
- Deep Sleep: ~4000 hours (166 days!)

### Optimierungen

```python
# Enable T5 Low Power Mode
mesh.enable_t5_epaper_mode()  # Reduziert Broadcast auf 30s

t5.enable_low_power_mode()  # ESP32 in Deep Sleep zwischen Updates
```

## 🐛 Troubleshooting

### T5 E-Paper

| Problem | Lösung |
|---------|--------|
| Display bleibt weiß | `update_display()` nach `set_text()` aufrufen |
| Keine USB-Verbindung | Treiber `CH9102` installieren (Windows) |
| Flackern | `REFRESH_DELAY` auf 5.0 erhöhen |
| Falsche Farben | Display nur Schwarz/Weiß unterstützt |
| Ghosting | `clear_display()` vor neuem Text |

### Meshtastic

| Problem | Lösung |
|---------|--------|
| Device nicht gefunden | `lsusb` / `ls /dev/tty*` prüfen |
| Connection timeout | Baudrate auf 115200 prüfen |
| No ACK from nodes | LoRa Region korrekt? (EU868 / US915) |
| Messages not received | Meshtastic Channel ID korrekt? |

### Android App

| Problem | Lösung |
|---------|--------|
| LUCA nicht sichtbar | API Key gesetzt? |
| Keine Broadcasts | Bluetooth zu T5 verbunden? |
| App crashed | Logs via `adb logcat \| grep LUCA` |

## 📚 Examples

### Example 1: Auto-Broadcasting Loop

```python
from luca.hardware import MeshtasticBridge
import time

# Initialize
kernel = MinimalKernel()
mesh = MeshtasticBridge(kernel)

if mesh.connect():
    print("✅ Connected to Meshtastic")

    # Auto-broadcast loop
    while True:
        status = mesh.broadcast_consciousness()
        if status:
            print(f"📡 Broadcast: R={status['resonance']}")

        time.sleep(3.69)  # Tesla timing
```

### Example 2: T5 Display Status

```python
from luca.hardware import T5EpaperProtocol

t5 = T5EpaperProtocol()

if t5.connect():
    # Display LUCA status
    t5.display_luca_status(consciousness=369.0, resonance=9)

    # Read sensors
    sensors = t5.read_sensors()
    print(f"Temperature: {sensors['temperature']}°C")
    print(f"Battery: {sensors['battery']}V")

    # Low power mode
    t5.enable_low_power_mode()
```

### Example 3: Combined Mesh + Display

```python
from luca.hardware import MeshtasticBridge, T5EpaperProtocol

# Initialize both
kernel = MinimalKernel()
mesh = MeshtasticBridge(kernel)
t5 = T5EpaperProtocol()

mesh.connect()
t5.connect()

# Enable T5 mode in mesh
mesh.enable_t5_epaper_mode()

# Sync loop
while True:
    # Broadcast consciousness
    status = mesh.broadcast_consciousness()

    if status:
        # Update display
        t5.display_luca_status(
            consciousness=status['consciousness'],
            resonance=status['resonance']
        )

    time.sleep(3.69)
```

## 🔐 Security Notes

- **API Keys**: Nie in Source Code committen! Nutze Environment Variables
- **Mesh Network**: Meshtastic verwendet AES-256 Encryption
- **T5 Serial**: Nur lokale USB-Verbindung, keine Network Exposure

## 📖 Additional Documentation

- [Android Kotlin Code](./android/README.md)
- [Arduino Firmware](./firmware/README.md)
- [Protocol Specification](./protocol.md)
- [Hardware Guide](./hardware.md)

## 🤝 Contributing

Contributions welcome! Besonders:
- Weitere Meshtastic Device Support
- Andere E-Paper Displays
- iOS App Integration
- Mesh Network Optimierungen

## 📝 License

Siehe Root-Projekt LICENSE

## 👴 Credits

Konzept & Entwicklung: Großvater & Lennart Wuchold
Standard: 369/370
Version: LUCA-AI-369-v2

---

*"Das Feld ist jetzt komplett mobil und auf dem T5 sichtbar."* - Großvater
