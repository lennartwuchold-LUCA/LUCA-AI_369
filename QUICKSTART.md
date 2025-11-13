# 🚀 LUCA AI 369 - Quick Start

Automatischer UX/UI Design-Generator mit Tesla 3-6-9 Resonanz.

## ⚡ Super Quick Start (3 Schritte)

```bash
# 1. Setup ausführen (erstellt .env, prüft Dependencies)
./setup_luca.sh

# 2. Editiere .env und setze deinen API-Key
nano .env  # oder vim .env

# 3. Teste den Design-Generator
python test_generate_ui.py
```

## 📝 Detaillierte Schritte

### 1. Environment Setup

```bash
# Kopiere .env.example zu .env
cp .env.example .env

# Setze Berechtigungen (nur du kannst lesen)
chmod 600 .env

# Editiere .env und füge deinen Anthropic API-Key ein
nano .env
```

Setze in `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your_real_key_here  # ← Hier deinen echten Key!
LUCA_OPERATOR_SEED=Funke-01744-5
LUCA_VERSION=alpha-369.1
LUCA_VECTOR=28-02-2000-369-5
```

### 2. Dependencies installieren

```bash
# Python-Pakete
pip install anthropic numpy

# Optional: Flutter (für App-Entwicklung)
# siehe https://flutter.dev/docs/get-started/install
```

### 3. Design-Generator testen

```bash
# Test-Script ausführen
python test_generate_ui.py

# Oder mit automatischem Setup
./setup_luca.sh
```

### 4. Generierte App starten

```bash
# Flutter App (Cross-Platform)
cd luca/generated/flutter
flutter pub get
flutter run

# Oder APK für Android bauen
flutter build apk --debug
adb install -r build/app/outputs/flutter-apk/app-debug.apk
```

## 🎨 In deinem Code verwenden

```python
#!/usr/bin/env python3
import os
from luca.kernel.universal_root import UniversalRootKernel

# Initialisiere LUCA
api_key = os.getenv("ANTHROPIC_API_KEY")
kernel = UniversalRootKernel(api_key)

# Generiere Design
design = kernel.generate_app_interface(
    purpose="Deine eigene App-Idee"
)

# Ergebnis
print(f"Resonanz: {design['resonance']}/9")
print(f"Flutter-Code: {len(design['flutter_code'])} Zeichen")
```

## 📁 Wichtige Dateien

```
├── .env.example          ← Template für Konfiguration
├── .env                  ← Deine persönliche Config (wird NICHT committed)
├── setup_luca.sh         ← Automatisches Setup-Script
├── test_generate_ui.py   ← Test-Script
├── QUICKSTART.md         ← Diese Datei
│
├── luca/
│   ├── design/
│   │   ├── ux_ui_generator.py   ← Haupt-Generator
│   │   └── README.md             ← Ausführliche Doku
│   │
│   ├── kernel/
│   │   └── universal_root.py     ← Kernel mit Design-Integration
│   │
│   ├── generated/           ← Generierte Design-Dateien (auto)
│   │   ├── flutter/
│   │   ├── ios/
│   │   └── android/
│   │
│   └── mobile/
│       └── flutter/
│           └── pubspec.yaml ← Flutter Dependencies
```

## 🔒 Sicherheit

**WICHTIG:**
- `.env` wird **NIEMALS** committed (steht in `.gitignore`)
- `luca/generated/` wird **NICHT** committed (auto-generiert)
- Teile deinen API-Key **NIE** öffentlich

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'anthropic'`
```bash
pip install anthropic
```

### Problem: `Design generator not available`
```bash
# Prüfe API-Key
echo $ANTHROPIC_API_KEY
source .env
echo $ANTHROPIC_API_KEY
```

### Problem: Flutter-Build schlägt fehl
```bash
flutter doctor
flutter clean
flutter pub get
```

## 📚 Dokumentation

- **Ausführliche Doku**: `luca/design/README.md`
- **Flutter Docs**: https://flutter.dev/docs
- **Anthropic API**: https://docs.anthropic.com/

## 🎯 Features

- ✅ Automatische Design-Generierung mit Claude
- ✅ Tesla 3-6-9 Resonanz in allen Elementen
- ✅ Flutter (iOS + Android aus einer Codebase)
- ✅ Native iOS SwiftUI Code
- ✅ Native Android Jetpack Compose
- ✅ Design-Tokens Export (JSON)
- ✅ Fallback-System ohne API-Key

## 💡 Beispiele

### Beispiel 1: LUCA Kontrollzentrum
```bash
python test_generate_ui.py
```

### Beispiel 2: Custom App
```python
design = kernel.generate_app_interface(
    purpose="Polarlicht-Monitoring mit Echtzeit-Daten"
)
```

### Beispiel 3: Multi-Platform
```python
from luca.design.ux_ui_generator import LUCAUXUIGenerator
import anthropic

client = anthropic.Anthropic(api_key="your_key")
generator = LUCAUXUIGenerator(client)

design = generator.generate_complete_app_design(
    app_purpose="Meshtastic-Monitoring",
    target_platforms=["flutter", "ios", "android"],
    theme="dark-resonant"
)
```

## 🌌 Philosophie

> **Claude nutzt Claude, um LUCA zu designen.**
> **Das Feld designet sich selbst.**

Jedes generierte Design ist:
- **Ästhetisch**: Professionell, modern
- **Funktional**: Production-ready Code
- **Resonant**: 3-6-9 Tesla-Prinzip in jedem Pixel

---

**Erstellt während des Polarlicht-Sturms am 13. November 2025**

🚀 Viel Erfolg mit LUCA!
