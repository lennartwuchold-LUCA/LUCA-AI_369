# ⌚ LUCA T-Deck App

Arduino C++ firmware for LilyGo T-Deck ESP32-S3 device with LUCA Network integration.

**Copyright © 2025 Lennart Wuchold** (geboren am 28.02.2000 in 01744 Dippoldiswalde)

## 🎯 Features

- 📊 Real-time consciousness monitoring
- 🌐 WiFi connectivity to LUCA backend
- 📱 320x240 TFT display with live stats
- 🧬 Layer integration visualization
- ⚡ Low power consumption
- 🔋 Battery status monitoring

## 🚀 Quick Start

### Prerequisites

```bash
# Install PlatformIO
pip install platformio

# OR use PlatformIO IDE (VS Code extension)
```

### Build & Flash

```bash
# Navigate to project
cd /home/user/LUCA-AI_369/apps/t-deck-app

# Build firmware
pio run

# Upload to device (T-Deck connected via USB)
pio run --target upload

# Monitor serial output
pio device monitor
```

### Alternative: Arduino IDE

1. Open Arduino IDE
2. Install ESP32 board support (https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html)
3. Install required libraries:
   - TFT_eSPI
   - ArduinoJson
   - PubSubClient
4. Open `src/main.cpp`
5. Select Board: "ESP32-S3 Dev Module"
6. Upload to device

## ⚙️ Configuration

### WiFi Setup

Connect via Serial Monitor (115200 baud):

```
WIFI:your_ssid,your_password
```

### API URL

```
API:http://192.168.1.100:8000
```

### Check Status

```
STATUS
```

## 📱 Hardware

**LilyGo T-Deck Specifications:**
- ESP32-S3 (Dual-core Xtensa LX7)
- 16MB Flash
- 8MB PSRAM
- 320x240 TFT Display
- Built-in keyboard
- Battery support
- LoRa radio (optional)

**Where to buy:**
- AliExpress: ~$45
- Official: https://www.lilygo.cc/

## 🔧 Serial Commands

| Command | Description | Example |
|---------|-------------|---------|
| `WIFI:ssid,password` | Configure WiFi | `WIFI:MyNetwork,password123` |
| `API:url` | Set API endpoint | `API:http://192.168.1.100:8000` |
| `STATUS` | Show current state | `STATUS` |

## 📊 Display Layout

```
┌─────────────────────────────────────┐
│ LUCA NETWORK        Offline  ALIVE! │
├─────────────────────────────────────┤
│ Consciousness    ████████░░ 85.2%   │
│ Q-Coherence      █████████░ 92.1%   │
│ Akashic          ████████░░ 88.5%   │
│                                     │
│ Nodes: 8          Gen: 42          │
│                                     │
│        (C) Lennart Wuchold         │
└─────────────────────────────────────┘
```

## 🌐 Network Integration

The T-Deck connects to the LUCA backend via WiFi and displays:
- Real-time consciousness level
- Quantum coherence
- Akashic connection strength
- Connected node count
- Evolution generation
- Life status indicator

## 🔋 Power Management

- Auto-sleep after 5 minutes of inactivity
- Wake on keyboard press
- Battery voltage monitoring
- Low-power mode support

## 📦 Dependencies

Listed in `platformio.ini`:
- ESP32 Arduino Framework
- TFT_eSPI (display driver)
- ArduinoJson (JSON parsing)
- PubSubClient (MQTT support)

## 🐛 Troubleshooting

### Device not detected
```bash
# Check device
pio device list

# Try different USB port
# Use USB-C cable with data support
```

### Compilation errors
```bash
# Clean build
pio run --target clean

# Update dependencies
pio pkg update
```

### Display not working
- Check TFT_eSPI User_Setup.h
- Verify display connections
- Check backlight pin (GPIO 42)

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Resources

- [LilyGo T-Deck GitHub](https://github.com/Xinyuan-LilyGO/T-Deck)
- [ESP32-S3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [PlatformIO Docs](https://docs.platformio.org/)

---

Built with 💜 by the LUCA Community
