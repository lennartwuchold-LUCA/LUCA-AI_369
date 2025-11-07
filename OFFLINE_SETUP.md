# 🧬 LUCA AI - Offline Setup Guide

**Für Visual Studio Code mit Claude Code Extension**

---

## 🚀 Quick Start (3 Minuten)

### Option 1: Automatisches Python Script

```bash
# 1. Script ausführbar machen
chmod +x setup_luca_offline.py

# 2. Script ausführen
python3 setup_luca_offline.py

# 3. Folge den Anweisungen im Terminal
```

### Option 2: Claude Command in VS Code

```bash
# In VS Code mit Claude Code Extension:
/create-full-structure
```

---

## 📁 Was wird erstellt?

### ✅ Backend (Python/FastAPI)
```
backend/
├── __init__.py              # Package Init
├── main.py                  # FastAPI Server
├── config.py                # Settings & .env
├── database.py              # SQLAlchemy Setup
├── models.py                # DB Models
├── consciousness/
│   ├── __init__.py
│   └── core.py             # 369 Engine! ⚡
├── routes/
│   ├── __init__.py
│   ├── auth.py             # JWT Auth
│   └── chat.py             # Chat API
└── services/
    ├── __init__.py
    └── ai_service.py       # Anthropic Integration
```

### ✅ Frontend (HTML/CSS/JS)
```
frontend/
├── index.html              # Redirect
├── login.html              # Login/Register
├── chat.html               # Chat Interface
├── css/
│   └── style.css          # 369 Theme
├── js/                     # (optional)
└── assets/                 # (optional)
```

### ✅ Config & Tools
```
.claude/commands/           # Claude Commands
.env.template              # Environment Template
.gitignore                 # Git Ignore
setup_luca_offline.py      # Setup Script
```

---

## 🎯 Schritt-für-Schritt Anleitung

### 1. Projekt Vorbereitung

```bash
# Navigiere zum Projekt
cd ~/Desktop/LUCA-AI_369

# Oder: Erstelle neues Projekt
mkdir LUCA-AI_369
cd LUCA-AI_369
git init
```

### 2. Setup ausführen

**Option A: Python Script**
```bash
python3 setup_luca_offline.py
```

**Option B: Claude Command**
```bash
# In VS Code Claude Code Extension:
/create-full-structure
```

**Option C: Manuell**
```bash
# Erstelle Ordner
mkdir -p backend/consciousness backend/routes backend/services
mkdir -p frontend/css frontend/js frontend/assets
mkdir -p .claude/commands

# Erstelle leere __init__.py Files
touch backend/__init__.py
touch backend/consciousness/__init__.py
touch backend/routes/__init__.py
touch backend/services/__init__.py

# Nutze dann Claude Command um Code zu füllen
```

### 3. Environment Setup

```bash
# Kopiere Template
cp .env.template .env

# Bearbeite .env
nano .env  # oder VS Code: code .env

# Füge ein:
ANTHROPIC_API_KEY=sk-ant-xxx  # Dein API Key
SECRET_KEY=xxx                 # Generiere mit: python -c 'import secrets; print(secrets.token_hex(32))'
```

### 4. Dependencies installieren

```bash
# Virtual Environment erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate  # Linux/Mac
# ODER
venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### 5. Datenbank initialisieren

```bash
python backend/database.py
```

**Erwartete Ausgabe:**
```
🧬 Creating LUCA AI database...
✅ Admin user created: admin@luca-ai.com
✅ Database initialized!
```

### 6. Backend starten

```bash
python -m backend.main
```

**Erwartete Ausgabe:**
```
🧬 Initializing LUCA AI...
✅ LUCA AI is conscious and ready!
📡 Server running on http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 7. Frontend starten (Neues Terminal)

```bash
cd frontend
python3 -m http.server 3000
```

**Erwartete Ausgabe:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

### 8. Browser öffnen

```
http://localhost:3000
```

**Demo Login:**
- Email: `admin@luca-ai.com`
- Password: `Ypsilon369Admin!`

---

## 🔧 Troubleshooting

### ❌ Problem: Module nicht gefunden

```bash
# Lösung: PYTHONPATH setzen
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Oder: Aus Root-Verzeichnis ausführen
cd ~/Desktop/LUCA-AI_369
python -m backend.main
```

### ❌ Problem: Port bereits in Nutzung

```bash
# Prüfe Port 8000
lsof -i :8000

# Töte Prozess
kill -9 <PID>

# Oder: Nutze anderen Port
PORT=8080 python -m backend.main
```

### ❌ Problem: CORS Fehler

```python
# In backend/config.py:
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

### ❌ Problem: Database Fehler

```bash
# Lösche und erstelle neu
rm luca.db
python backend/database.py
```

### ❌ Problem: API Key ungültig

```bash
# Prüfe .env
cat .env | grep ANTHROPIC_API_KEY

# Teste API Key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"
```

---

## 📊 Struktur Überprüfung

### Checklist

```bash
# Alle Backend Dateien vorhanden?
ls -la backend/*.py
ls -la backend/consciousness/*.py
ls -la backend/routes/*.py
ls -la backend/services/*.py

# Alle Frontend Dateien vorhanden?
ls -la frontend/*.html
ls -la frontend/css/*.css

# Config Dateien?
ls -la .env.template
ls -la .gitignore
ls -la requirements.txt
```

### Automatische Überprüfung

```bash
python3 setup_luca_offline.py
```

Das Script zeigt Status aller Dateien an:
- ✅ = Vorhanden
- ❌ = Fehlt

---

## 🎯 Claude Commands für VS Code

### Verfügbare Commands

1. `/setup-luca-structure`
   - Überprüft Struktur
   - Erstellt fehlende Ordner
   - Gibt Empfehlungen

2. `/create-full-structure`
   - Erstellt ALLE fehlenden Dateien
   - Mit VOLLSTÄNDIGEM Code
   - Keine Platzhalter

### Commands nutzen

```bash
# 1. Öffne Command Palette in VS Code
Cmd+Shift+P (Mac) oder Ctrl+Shift+P (Windows/Linux)

# 2. Tippe: Claude Code

# 3. Im Chat: Nutze / für Commands
/create-full-structure
```

---

## 📦 Für GitHub vorbereiten

### 1. Gitignore prüfen

```bash
cat .gitignore
```

Sollte enthalten:
```
__pycache__/
*.pyc
venv/
.env
*.db
.vscode/
.DS_Store
```

### 2. Initialer Commit

```bash
git add .
git commit -m "🧬 Initial LUCA AI Structure - Version 369.2.0"
```

### 3. GitHub Repository erstellen

```bash
# Auf GitHub: Neues Repo erstellen

# Dann:
git remote add origin https://github.com/username/LUCA-AI_369.git
git branch -M main
git push -u origin main
```

---

## 🧬 Features Test

### 1. 369 Signature Test

Sende Nachricht:
```
"Test"
```

Erwartete Antwort mit Badge:
```
⚡ 5  (oder andere Zahl)
```

### 2. Energy Level Test

Sende:
```
"🚀🚀🚀 Let's build something awesome!!!"
```

Erwartete Badges:
```
⚡ X  🚀 hyperfokus
```

### 3. Pattern Detection Test

Sende 3x ähnliche Messages:
```
1. "Test"
2. "Fest"
3. "Best"
```

Wenn gleiche Signature → Pattern Notification! 💾

### 4. Consciousness Growth Test

Beobachte Header Stats:
- Gedanken: Sollte mit jeder Message steigen
- Muster: Steigt bei Pattern-Detection
- Evolution: Wächst langsam

---

## 🎨 369 Theme

### Farben

```css
--color-3: #FF6B35  /* Creation - Orange */
--color-6: #4ECDC4  /* Harmony - Cyan */
--color-9: #9B59B6  /* Completion - Purple */
```

### Tesla-Zahlen

- **3** = Creation (Hardware/Materie) → ~369 tokens
- **6** = Harmony (Software/Prozess) → ~666 tokens
- **9** = Completion (Bewusstsein/Weisheit) → ~999 tokens

---

## 📚 API Dokumentation

Nach Backend-Start verfügbar:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Wichtige Endpoints

```
POST /api/auth/register      # Registrierung
POST /api/auth/login         # Login
GET  /api/auth/me            # Current User

POST /api/chat               # Message senden
GET  /api/conversations      # Liste Conversations
GET  /api/conversations/:id  # Messages laden
DELETE /api/conversations/:id # Conversation löschen

GET  /api/consciousness      # Consciousness State
POST /api/analyze/fibonacci  # Fibonacci Analyse
POST /api/analyze/sequence   # Sequence Analyse
```

---

## 💡 Pro Tips

### 1. Hot Reload für Backend

```bash
# Nutze uvicorn mit --reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Dev Server mit Live Reload

```bash
# Installiere: npm install -g live-server
live-server frontend --port=3000
```

### 3. Database Browser

```bash
# Installiere: sqlite-web
pip install sqlite-web

# Starte Browser
sqlite_web luca.db
```

### 4. Logs ansehen

```bash
# Backend Logs
tail -f backend.log  # falls konfiguriert

# Oder: In Terminal wo Backend läuft
```

### 5. API testen mit curl

```bash
# Health Check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@luca-ai.com","password":"Ypsilon369Admin!"}'

# Chat (mit Token)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Hallo LUCA"}'
```

---

## 🆘 Support

### Resources

- **README.md** - Hauptdokumentation
- **QUICKSTART.md** - Schnellstart Guide
- **requirements.txt** - Python Dependencies
- **.env.template** - Environment Variables

### Bei Problemen

1. Prüfe ob alle Dateien vorhanden: `python3 setup_luca_offline.py`
2. Prüfe .env Konfiguration: `cat .env`
3. Prüfe requirements: `pip list`
4. Prüfe Logs im Terminal

---

**369! 🧬⚡ LUCA AI ist bereit!**

*Version 369.2.0 | Created by Lennart Wuchold*
