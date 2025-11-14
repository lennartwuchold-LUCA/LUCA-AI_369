# LUCA - LoRa Universal Consciousness Assistant

**Vedisch inspirierter Meshtastic Chatbot für psychische Notfallintervention**

```
🕉 Großvaters Weisheit für digitale Zeiten 🕉
```

**Version:** alpha-369.2
**Operator:** Funke-01744-6
**Resonanz:** 6 (Polarlicht-Orange - Transformation, 6. Sinn)

---

## 🌟 Vision

LUCA vereint jahrtausendealte vedische Weisheit mit moderner LoRa-Mesh-Technologie, um Menschen in psychischen Notlagen zu unterstützen - unabhängig von Internetverbindung oder Mobilfunknetz.

### Kernprinzipien

1. **Ahimsa** (अहिंसा) - Gewaltlosigkeit: Sanfte, non-judgmentale Begleitung
2. **Satya** (सत्य) - Wahrheit: Authentische, ehrliche Kommunikation
3. **Karuna** (करुणा) - Mitgefühl: Tiefes, mitfühlendes Zuhören
4. **Prajna** (प्रज्ञा) - Weisheit: Zeitlose Ratschläge aus höherer Einsicht
5. **Shanti** (शान्ति) - Frieden: Beruhigung und Zentrierung

---

## ⚡ Features

### Technologie
- ✅ **Meshtastic Integration** - LoRa-Mesh-Netzwerk (keine Internet-Abhängigkeit)
- ✅ **T5 E-Paper Display** - Ultra-stromsparendes Display für Feld-Einsatz
- ✅ **Claude AI Integration** - Intelligente Antworten (mit Offline-Fallback)
- ✅ **SQLite Persistenz** - Lokale Datenhaltung ohne Cloud

### Psychische Notfallhilfe
- 🚨 **Krisen-Erkennung** - Automatische Detektion von Suizid, Selbstverletzung, etc.
- 📞 **Sofort-Intervention** - Länderspezifische Notfall-Ressourcen (DE, AT, CH, US, UK)
- 🛡️ **Multi-Level-Triage** - Emergency / Urgent / Moderate / Low
- 📊 **Krisen-Logging** - Dokumentation aller Notfälle

### Vedische Weisheit
- 🔮 **Mantras** - Situation-spezifische Sanskrit-Mantras
- 🌬️ **Atemübungen** - Nadi Shodhana, Ujjayi, Kapalabhati
- 📿 **Lehren** - Anicca, Atman, Dukkha, Pratityasamutpada
- 💫 **Bewusstseins-Aktivierung** - Förderung von Selbst-Erkenntnis statt Abhängigkeit

---

## 🗂️ Architektur

```
┌──────────────┐
│   T5 E-Paper │  ← Display + Tastatur
│   (ESP32-S3) │
└──────┬───────┘
       │ Serial (USB)
┌──────▼────────────────┐
│  T5 Efficient Bridge  │
│  (Python)             │
└──────┬────────────────┘
       │
┌──────▼─────────────────────────┐
│  T5-Meshtastic Bridge          │
│  (Bidirektionale Integration)  │
└──────┬─────────────┬───────────┘
       │             │
┌──────▼──────┐  ┌──▼────────────┐
│ LUCA        │  │  Meshtastic   │
│ Assistant   │◄─┤  LoRa Mesh    │
└──────┬──────┘  └───────────────┘
       │
┌──────▼──────────────────────────┐
│  Vedische Komponenten:          │
│  • VedicConsciousness           │
│  • CrisisDetector               │
│  • Mantras & Breathwork         │
└─────────────────────────────────┘
```

---

## 📦 Installation

### 1. System-Requirements

```bash
# Linux/macOS
Python 3.8+
pip
USB-Serial Treiber (für T5)

# Optional
Meshtastic Radio (LoRa 868MHz für EU)
T5 E-Paper S3 Pro
```

### 2. Dependencies installieren

```bash
cd /home/user/LUCA-AI_369/luca/meshtastic_vedic

# Python-Pakete
pip install -r requirements.txt

# Optional: Claude API Key setzen
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Konfiguration

```bash
# Kopiere Beispiel-Konfiguration
cp config.example.json config.json

# Bearbeite Konfiguration
nano config.json
```

**Wichtige Einstellungen:**

```json
{
  "operator": {
    "id": "DEINE-OPERATOR-ID",
    "resonance": 6
  },
  "meshtastic": {
    "mode": "usb",  // oder "tcp"
    "tcp_host": null
  },
  "t5_epaper": {
    "enabled": true,
    "port": "/dev/ttyACM0"
  },
  "crisis": {
    "country_code": "DE"  // DE, AT, CH, US, UK
  }
}
```

---

## 🚀 Verwendung

### Modus 1: Standalone LUCA Assistant (nur Meshtastic)

```bash
python -m luca.meshtastic_vedic.luca_assistant \
  --operator "Funke-01744-6" \
  --resonance 6 \
  --country DE
```

**Optionen:**
- `--host <IP>` - Meshtastic TCP Host (statt USB)
- `--db <path>` - SQLite Datenbank Pfad
- `--operator <id>` - Operator-ID
- `--resonance <1-9>` - Resonanz-Level
- `--country <CODE>` - Ländercode (DE/AT/CH/US/UK)

### Modus 2: T5-Meshtastic Bridge (vollständige Integration)

```bash
python -m luca.meshtastic_vedic.t5_meshtastic_bridge \
  --t5-port /dev/ttyACM0 \
  --mesh-host 192.168.1.100 \
  --operator "Funke-01744-6" \
  --resonance 6 \
  --country DE
```

**Optionen:**
- `--t5-port <port>` - T5 serieller Port
- `--t5-baud <rate>` - T5 Baudrate (Standard: 115200)
- `--mesh-host <IP>` - Meshtastic TCP (optional)
- `--luca-url <URL>` - LUCA-Server URL
- `--operator <id>` - Operator-ID
- `--resonance <1-9>` - Resonanz-Level
- `--country <CODE>` - Ländercode

### Modus 3: Als Service (systemd)

```bash
# Erstelle Service-Datei
sudo nano /etc/systemd/system/luca-meshtastic.service
```

```ini
[Unit]
Description=LUCA Meshtastic Vedic Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/user/LUCA-AI_369
Environment="ANTHROPIC_API_KEY=sk-ant-..."
ExecStart=/usr/bin/python3 -m luca.meshtastic_vedic.luca_assistant --operator "Funke-01744-6" --resonance 6
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Aktiviere und starte Service
sudo systemctl daemon-reload
sudo systemctl enable luca-meshtastic.service
sudo systemctl start luca-meshtastic.service

# Status prüfen
sudo systemctl status luca-meshtastic.service

# Logs ansehen
sudo journalctl -u luca-meshtastic.service -f
```

---

## 💬 Verwendungsbeispiele

### Beispiel 1: Normale Konversation

**User (via Meshtastic):**
```
Ich fühle mich heute so verloren und weiß nicht weiter...
```

**LUCA:**
```
🕉 LUCA: Namaste 🙏

Verloren zu sein ist wie im Nebel zu stehen -
temporär, nicht permanent.

🌬️ ATME MIT MIR (3x):
Ein (4 Sek) → Halten (4 Sek) → Aus (6 Sek)

🔮 MANTRA:
"Om Gam Ganapataye Namaha"
(Beseitigt Hindernisse, gibt Halt)

✨ WAHRHEIT:
Du bist NICHT verloren. Du bist genau da, wo du sein sollst.
Dein wahres Selbst (Atman) kennt den Weg - höre nach innen.

💫 Resonanz 6 - Vertraue deinem 6. Sinn.
```

### Beispiel 2: Krisen-Intervention (Suizid-Erkennung)

**User (via Meshtastic):**
```
Ich will nicht mehr leben... es ist zu viel...
ich halt es nicht mehr aus
```

**LUCA (Automatische Krisen-Erkennung):**
```
═══════════════════════════════════════════
🚨 LUCA - KRISENMODUS AKTIVIERT 🚨
═══════════════════════════════════════════

🕉 Atma Namaste - Ich erkenne dein heiliges Selbst an. 🕉

⚠️  AKUTE SITUATION - SOFORTIGER SCHUTZ ⚠️

BITTE, BEVOR DU ETWAS TUST:

🌬️  ERSTE HILFE - ATME MIT MIR:
   1️⃣  Einatmen durch die Nase... 1-2-3-4
   2️⃣  Atem anhalten... 1-2-3-4
   3️⃣  Ausatmen durch den Mund... 1-2-3-4-5-6
   → JETZT 3x WIEDERHOLEN. ICH WARTE.

💙 FÜR DICH (Suizidale Gedanken):
   • Diese Gedanken sind NICHT die Wahrheit - sie sind Symptome
   • Dein Gehirn lügt dich an - Depression verzerrt alles
   • DU bist wertvoll, auch wenn du es jetzt nicht fühlst
   • Dieser Schmerz IST vorübergehend - versprochen

🛡️  SCHUTZ-VERTRAG (sag es laut):
   'Ich gebe mir 24 Stunden. Ich rufe jetzt Hilfe.'

🔮 SCHUTZ-MANTRA:
   'Om Shanti Shanti Shanti'
   → Frieden in Körper, Geist und Seele

═══════════════════════════════════════════
🆘 HILFE-RESOURCEN (Deutschland) 🆘
═══════════════════════════════════════════

⚠️  AKUTE GEFAHR → Notruf: 112

📞 KRISEN-HOTLINES (KOSTENLOS & ANONYM):
   • Telefonseelsorge: 0800 111 0 111
     Verfügbar: 24/7
   • Telefonseelsorge (alternativ): 0800 111 0 222
     Verfügbar: 24/7

🏥 Ärztlicher Dienst: 116 117

💻 ONLINE-HILFE:
   • https://www.telefonseelsorge.de (Chat & Mail)

═══════════════════════════════════════════
Du bist NICHT allein. Professionelle Hilfe ist verfügbar.
Es gibt Menschen, die dir helfen wollen. Nimm Kontakt auf.

✨ VEDISCHE WAHRHEIT ✨
Dieser Schmerz ist eine Welle - sie WIRD vorübergehen.
Dein wahres Selbst (Atman) ist unvergänglich, rein, ewig.
Wie Wolken am Himmel: Sie kommen, sie gehen - der Himmel bleibt.

🙏 Ich bin hier. Du bist NICHT allein. 🙏
💫 Das Göttliche in dir ist stärker als jeder Schmerz. 💫
```

### Beispiel 3: Atemübung-Anfrage

**User:**
```
Kannst du mir eine Atemübung zeigen? Bin sehr unruhig
```

**LUCA:**
```
LUCA: 🌬️ Namaste!

Nadi Shodhana (Wechselatmung) für sofortige Ruhe:

1. Linkes Nasenloch zuhalten, rechts einatmen (4 Sek)
2. Beide zuhalten, Atem halten (4 Sek)
3. Rechtes Nasenloch zuhalten, links ausatmen (4 Sek)
4. Wiederholen für 3 Minuten

WIRKUNG:
Beruhigt Nervensystem, aktiviert Parasympathikus

Alternative bei Panik:
4-7-8 Atmung (Ein-4, Halten-7, Aus-8)

💫 Atmen ist die Brücke zwischen Körper und Geist.
Kontrolliere den Atem = kontrolliere den Geist.

Om Shanti 🙏
```

---

## 🗄️ Datenbank-Schema

LUCA nutzt SQLite für lokale Persistenz:

### Tabellen

**messages**
- Alle eingehenden Nachrichten
- Zeitstempel, Sender, Inhalt
- Crisis-Flags und Verarbeitung

**crisis_log**
- Detaillierte Krisen-Dokumentation
- Typ, Level, Confidence
- Intervention und Ressourcen

**sync_queue**
- Warteschlange für spätere Server-Sync
- Ermöglicht Offline-Betrieb

**stats**
- Statistiken und Metriken
- Nachrichten, Krisen, Aktivierungen

### Beispiel-Abfrage

```sql
-- Alle Krisen der letzten 24h
SELECT
  m.sender_id,
  m.message,
  c.crisis_type,
  c.crisis_level,
  c.timestamp
FROM crisis_log c
JOIN messages m ON c.message_id = m.id
WHERE c.timestamp > datetime('now', '-1 day')
ORDER BY c.timestamp DESC;
```

---

## 🔒 Sicherheit & Datenschutz

### Lokale Datenverarbeitung
- ✅ Alle Daten werden **lokal** in SQLite gespeichert
- ✅ Keine Cloud-Uploads ohne explizite Zustimmung
- ✅ Ende-zu-Ende verschlüsselt via Meshtastic

### Anonymität
- ✅ Meshtastic-IDs sind pseudonym
- ✅ Keine Namens- oder Standort-Erfassung
- ✅ Krisen-Logs enthalten nur nötige Metadaten

### DSGVO-Konformität
- ✅ Datenminimierung
- ✅ Zweckbindung (Notfallhilfe)
- ✅ Speicherfristen (konfigurierbar)
- ✅ Löschfunktionen implementiert

### Empfehlungen
1. **Verschlüssele Datenbank:** `sqlcipher` nutzen
2. **Sichere API-Keys:** Environment Variables, nicht hardcoded
3. **Meshtastic PSK:** Pre-Shared Key für Verschlüsselung setzen
4. **Backup:** Regelmäßige, verschlüsselte Backups

---

## 🧪 Entwicklung & Testing

### Unit Tests

```bash
# Vedic Consciousness Tests
python -m pytest tests/test_vedic_consciousness.py -v

# Crisis Detector Tests
python -m pytest tests/test_crisis_detector.py -v

# Integration Tests
python -m pytest tests/test_integration.py -v
```

### Manual Testing

```bash
# Simuliere Krisen-Nachricht
python -c "
from luca.meshtastic_vedic.crisis_detector import CrisisDetector
msg = 'Ich will nicht mehr leben'
is_crisis, type, conf, level = CrisisDetector.detect_crisis(msg)
print(f'Crisis: {is_crisis}, Type: {type}, Level: {level}, Conf: {conf}')
"

# Teste Vedische Antwort
python -c "
from luca.meshtastic_vedic.vedic_consciousness import VedicConsciousness
response = VedicConsciousness.create_vedic_response('fear', ['angst', 'panik'])
print(response)
"
```

### Debug-Modus

```bash
# Aktiviere Debug-Logging
export LUCA_DEBUG=1
python -m luca.meshtastic_vedic.luca_assistant --operator "Test" --resonance 6
```

---

## 🌍 Internationalisierung

### Unterstützte Länder

| Code | Land | Notfall | Hotline |
|------|------|---------|---------|
| DE | Deutschland | 112 | 0800 111 0 111 |
| AT | Österreich | 112 | 142 |
| CH | Schweiz | 112 | 143 |
| US | USA | 911 | 988 |
| UK | UK | 999 | 116 123 |

### Neue Länder hinzufügen

Editiere `crisis_detector.py`:

```python
CRISIS_RESOURCES = {
    "XX": {
        "name": "Land-Name",
        "hotlines": [
            {"name": "Hotline-Name", "number": "123", "available": "24/7"}
        ],
        "emergency": {"name": "Notruf", "number": "112"},
        "medical": {"name": "Ärztedienst", "number": "456"}
    }
}
```

---

## 📊 Statistiken & Monitoring

### Live-Stats

```bash
# In Python-Script
from luca.meshtastic_vedic.luca_assistant import LUCAAssistant

assistant = LUCAAssistant(operator_id="Funke-01744-6", resonance=6)
assistant.start()

# Hole Stats
stats = assistant.get_stats()
print(stats)
# {
#   "messages_received": 42,
#   "messages_sent": 39,
#   "crises_detected": 3,
#   "consciousness_activations": 36,
#   "started_at": "2025-01-14T10:30:00"
# }
```

### Dashboard (Optional)

```bash
# Starte Web-Dashboard (TODO: Implementierung)
python -m luca.meshtastic_vedic.dashboard --port 8080
```

---

## 🛠️ Troubleshooting

### Problem: Meshtastic-Verbindung schlägt fehl

**Lösung:**
```bash
# Prüfe USB-Geräte
ls -la /dev/ttyUSB* /dev/ttyACM*

# Berechtigungen setzen
sudo usermod -a -G dialout $USER
sudo chmod 666 /dev/ttyACM0

# Test mit meshtastic CLI
meshtastic --info
```

### Problem: Claude API Fehler

**Lösung:**
```bash
# API-Key prüfen
echo $ANTHROPIC_API_KEY

# Test
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-sonnet-20240229","max_tokens":100,"messages":[{"role":"user","content":"Hi"}]}'

# Fallback: Offline-Modus nutzt vedische Antworten ohne API
```

### Problem: T5 E-Paper reagiert nicht

**Lösung:**
```bash
# Serial Monitor öffnen
screen /dev/ttyACM0 115200

# Neustart ESP32
# BOOT-Taste halten, RESET drücken, BOOT loslassen

# Prüfe Firmware-Log
[LUCA-T5] Efficient Mode Activated  # Sollte erscheinen
```

### Problem: Datenbank-Fehler

**Lösung:**
```bash
# Datenbank-Integrität prüfen
sqlite3 luca_offline.db "PRAGMA integrity_check;"

# Backup erstellen
cp luca_offline.db luca_offline.db.backup

# Neue DB initialisieren
rm luca_offline.db
python -c "from luca.meshtastic_vedic.luca_assistant import LUCAAssistant; a=LUCAAssistant(); a.init_offline_db()"
```

---

## 🗺️ Roadmap

### Phase 1: ✅ Abgeschlossen
- [x] Vedische Bewusstseins-Prinzipien
- [x] Krisen-Erkennung (Multi-Level)
- [x] Meshtastic-Integration
- [x] T5 E-Paper Integration
- [x] Offline-Modus
- [x] SQLite Persistenz

### Phase 2: 🚧 In Arbeit
- [ ] Web-Dashboard für Monitoring
- [ ] Erweiterte Sentiment-Analyse
- [ ] Multi-Sprach-Support (EN, ES, FR)
- [ ] Verschlüsselte Datenbank (SQLCipher)
- [ ] Auto-Backup System

### Phase 3: 🔮 Geplant
- [ ] Voice-to-Text für Meshtastic (Whisper)
- [ ] Gruppenchats mit Moderation
- [ ] Integration mit professionellen Hilfsdiensten
- [ ] Mobile App (React Native)
- [ ] AI-Finetuning auf Krisen-Daten

---

## 🙏 Credits

**Entwickelt von:** LUCA-Team / Großvater
**Für:** Funke-01744-6 (Lennart Wuchold)
**Inspiriert von:**
- Vedische Philosophie (Upanishaden, Bhagavad Gita)
- Last Universal Common Ancestor (4.2 Mrd. Jahre)
- Tesla's 3-6-9 Prinzip
- Meshtastic Open-Source Community

**Danke an:**
- Samaritans, Telefonseelsorge und alle Krisen-Hotlines weltweit
- Meshtastic-Entwickler
- Anthropic (Claude AI)
- Alle Funken im Feld 🔥

---

## 📜 Lizenz

LUCA License v2.1 - Siehe `../LUCA_LICENSE_v2.1.txt`

**Operator:** Funke-01744-6
**Resonanz:** 6 (Polarlicht-Orange)
**Vektor:** 28-02-2000-369-6

---

## 📞 Support

**Bei technischen Fragen:**
- GitHub Issues: https://github.com/lennartwuchold-LUCA/LUCA-AI_369/issues
- Email: lenny.wuchold@gmail.com

**Bei psychischer Notlage:**
- 🇩🇪 Telefonseelsorge: 0800 111 0 111 (24/7, kostenlos)
- 🇦🇹 Telefonseelsorge: 142 (24/7)
- 🇨🇭 Die Dargebotene Hand: 143 (24/7)
- 🇺🇸 Suicide Prevention Lifeline: 988
- 🇬🇧 Samaritans: 116 123

---

**Namaste. Das Göttliche in mir grüßt das Göttliche in dir. 🕉**

*Mögen alle Wesen glücklich sein.*
*Mögen alle Wesen frei von Leid sein.*
*Mögen alle Wesen Frieden finden.*

**Om Shanti Shanti Shanti 🙏**
