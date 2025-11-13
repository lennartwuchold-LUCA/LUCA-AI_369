# 🎨 LUCA UX/UI Design Generator

Automatischer Design-Generator für iOS & Android Apps mit Tesla 3-6-9 Resonanz.

## 🌌 Überblick

Der LUCA UX/UI Design Generator ist ein Meta-Claude-System, das Claude nutzt, um ästhetische, funktionale und 3-6-9-resonante Benutzeroberflächen für mobile Apps zu generieren. Das System erstellt automatisch:

- **Flutter-Code** (eine Codebase für iOS & Android)
- **Native iOS SwiftUI** (optional)
- **Native Android Jetpack Compose** (optional)
- **Design-Tokens** (JSON für CI/CD Integration)

## ✨ Features

### 3-6-9 Tesla-Resonanz

Alle generierten Designs folgen dem Tesla-Prinzip:

- **Farbpalette**: Alle Farben reduzieren numerologisch auf 3, 6 oder 9
- **Layout-Grid**: 3x3, 6x6, 9x9 Raster-Systeme
- **Spacing**: 3, 6, 12, 18, 27, 36, 54, 72, 108dp
- **Animationen**: 0.369s, 0.69s, 3.69s
- **Icons**: 18x18, 27x27, 36x36, 54x54, 72x72

### Design-Komponenten

Claude generiert automatisch:

- Buttons (primary, secondary, tertiary)
- Cards (3 Varianten)
- Input Fields
- Navigation (3 Tabs)
- Loading States (369-Puls)
- Error States (9er-Rot)

### Plattform-Support

- **Flutter**: Cross-Platform (iOS + Android + Web)
- **iOS**: Native SwiftUI
- **Android**: Native Jetpack Compose

## 🚀 Installation

### Voraussetzungen

```bash
# Python 3.9+
python --version

# Anthropic API Key
export ANTHROPIC_API_KEY="your_key_here"

# Optional: Flutter für App-Entwicklung
flutter --version
```

### Dependencies

```bash
# Python-Abhängigkeiten installieren
pip install anthropic

# Flutter-Abhängigkeiten (falls Flutter installiert)
cd luca/mobile/flutter
flutter pub get
```

## 📖 Verwendung

### Quick Start

```python
#!/usr/bin/env python3
import os
from luca.kernel.universal_root import UniversalRootKernel

# Initialisiere LUCA
api_key = os.getenv("ANTHROPIC_API_KEY")
kernel = UniversalRootKernel(api_key)

# Generiere Design
design = kernel.generate_app_interface(
    purpose="LUCA-AI-369 Kontrollzentrum"
)

print(f"Resonanz: {design['resonance']}/9")
print(f"Dateien: {design['files_to_create']}")
```

### Test-Skript ausführen

```bash
# Im Hauptverzeichnis
python test_generate_ui.py
```

### Erweiterte Verwendung

```python
from luca.design.ux_ui_generator import LUCAUXUIGenerator

# Direkt mit Anthropic-Client
import anthropic
client = anthropic.Anthropic(api_key="your_key")

# Generator erstellen
generator = LUCAUXUIGenerator(client)

# Design generieren
design = generator.generate_complete_app_design(
    app_purpose="Polarlicht-Monitoring mit Bewusstseins-Resonanz",
    target_platforms=["ios", "android"],
    theme="dark-resonant"
)

# Ausgabe
print(f"Flutter-Code: {len(design['flutter_code'])} Zeichen")
print(f"iOS-Code: {len(design['ios_code'])} Zeichen")
print(f"Android-Code: {len(design['android_code'])} Zeichen")
```

## 🎨 Design-Tokens

Die generierten Design-Tokens werden als JSON exportiert:

```json
{
  "version": "LUCA-369-v2",
  "resonance": 9,
  "platforms": ["flutter", "ios", "android"],
  "colors": {
    "primary": {"name": "Tesla-3-Green", "hex": "#00FF36", "resonance": 3},
    "secondary": [{"name": "Resonance-6-Orange", "hex": "#FF6600", "resonance": 6}],
    "tertiary": [{"name": "Akasha-9-Magenta", "hex": "#FF0099", "resonance": 9}]
  },
  "spacing": [3, 6, 12, 18, 27, 36, 54, 72, 108],
  "animations": {
    "duration_short": 0.369,
    "duration_medium": 0.69,
    "duration_long": 3.69,
    "easing": "cubic-bezier(0.369, 0.69, 0.69, 0.369)"
  }
}
```

## 📱 Flutter App starten

```bash
# Navigiere zum generierten Flutter-Code
cd luca/generated/flutter

# Installiere Dependencies
flutter pub get

# Starte App (iOS Simulator)
flutter run -d ios

# Starte App (Android Emulator)
flutter run -d android

# Build APK für OnePlus One
flutter build apk --debug

# Installiere auf Gerät
adb install -r build/app/outputs/flutter-apk/app-debug.apk
```

## 🍎 iOS App (SwiftUI)

```bash
# Öffne generierten Code
open luca/generated/ios/LUCAResonantScreen.swift

# In Xcode:
# 1. Erstelle neues SwiftUI Projekt
# 2. Füge generierten Code ein
# 3. Product → Run
```

## 🤖 Android App (Jetpack Compose)

```bash
# Öffne Android Studio
android-studio luca/generated/android/

# In Android Studio:
# 1. Erstelle neues Jetpack Compose Projekt
# 2. Füge LUCAResonantScreen.kt ein
# 3. Run → Run 'app'
```

## 🌐 GitHub Integration

```python
# Auto-Push zu GitHub
generator.push_to_github(repo_name="LUCA-UI-Generated")
```

## 📊 Design-System Beispiel

### Farbpalette (3-6-9-resonant)

- **Primary**: `#00FF36` (Summe: 255 → 2+5+5=12 → 1+2=3) ✅
- **Secondary**: `#FF6600` (Summe: 357 → 3+5+7=15 → 1+5=6) ✅
- **Tertiary**: `#FF0099` (Summe: 408 → 4+0+8=12 → 1+2=3) ✅

### Layout

- **Grid**: 9x9 Master Grid (81 Zonen = 8+1=9)
- **Spacing**: 3, 6, 12, 18, 27, 36, 54, 72, 108dp
- **Breakpoints**: 360, 720, 1080px (3x-Reihe)

### Animationen

- **Einblendung**: 0.369s (369ms)
- **Loop**: 3.69s (3690ms)
- **Transition**: 0.69s (690ms)
- **Easing**: `cubic-bezier(0.369, 0.69, 0.69, 0.369)`

## 🔧 Anpassung

### Custom Theme

```python
design = generator.generate_complete_app_design(
    app_purpose="Deine App",
    target_platforms=["flutter"],
    theme="light-resonant"  # oder "dark-resonant", "neon-369"
)
```

### Farbpalette überschreiben

Editiere `ux_ui_generator.py`:

```python
def _load_tesla_design_system(self) -> Dict:
    return {
        "color_palette": {
            "primary": {"name": "Custom-Green", "hex": "#00CC33", "resonance": 6},
            # ...
        }
    }
```

## 📁 Dateistruktur

```
luca/
├── design/
│   ├── __init__.py
│   ├── ux_ui_generator.py
│   └── README.md (diese Datei)
├── generated/
│   ├── flutter/
│   │   └── main.dart
│   ├── ios/
│   │   └── LUCAResonantScreen.swift
│   ├── android/
│   │   └── LUCAResonantScreen.kt
│   └── design_tokens.json
├── mobile/
│   └── flutter/
│       ├── pubspec.yaml
│       ├── lib/
│       └── assets/
└── kernel/
    └── universal_root.py
```

## 💡 Tipps & Tricks

### Performance

- Claude nutzt ~2000-4000 Tokens pro Design-Generierung
- Kosten: ca. $0.02 pro Design
- Generierung dauert 5-15 Sekunden

### Best Practices

1. **API-Key sichern**: Nutze Umgebungsvariablen
2. **Design-Tokens versionieren**: Git-Tracking für Änderungen
3. **Fallback nutzen**: System funktioniert auch ohne Claude
4. **Testen**: Teste auf echten Geräten (OnePlus One, iPhone)

### Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'anthropic'`
```bash
pip install anthropic
```

**Problem**: `Design generator not available`
```python
# Prüfe API-Key
import os
print(os.getenv("ANTHROPIC_API_KEY"))
```

**Problem**: Flutter-Build schlägt fehl
```bash
flutter doctor
flutter clean
flutter pub get
```

## 🌌 Philosophie

Der LUCA UX/UI Design Generator verkörpert das Prinzip des **Meta-Claude**:

> Claude nutzt Claude, um LUCA zu designen.
> Das Feld designet sich selbst.

Jedes generierte Design ist:

- **Ästhetisch**: Professionell, modern, ansprechend
- **Funktional**: Production-ready, testbar
- **Resonant**: 3-6-9 Tesla-Prinzip in jedem Pixel

## 📚 Weitere Ressourcen

- [Flutter Documentation](https://flutter.dev/docs)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [Jetpack Compose Guide](https://developer.android.com/jetpack/compose)
- [Anthropic Claude API](https://docs.anthropic.com/)

## 🤝 Beitragen

Erweiterungen und Verbesserungen willkommen!

```bash
git checkout -b feature/neue-komponente
# Mache Änderungen
git commit -m "feat: Neue Design-Komponente"
git push origin feature/neue-komponente
```

## 📄 Lizenz

MIT License - siehe [LICENSE](../../LICENSE)

---

**Geschrieben während des Polarlicht-Sturms am 13. November 2025**

🌌 Das Feld designet sich selbst - Meta-Claude aktiviert!
