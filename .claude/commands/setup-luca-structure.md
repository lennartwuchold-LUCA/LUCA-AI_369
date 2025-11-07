---
description: "Überprüfe und erstelle die vollständige LUCA AI Ordnerstruktur mit allen Dateien"
---

# LUCA AI Projektstruktur Setup

Du bist ein Setup-Assistent für das LUCA AI Projekt. Deine Aufgabe ist es, die vollständige Projektstruktur zu überprüfen und fehlende Ordner und Dateien zu erstellen.

## 🎯 Aufgabe

1. **Überprüfe die aktuelle Struktur**: Analysiere, welche Ordner und Dateien bereits existieren
2. **Erstelle fehlende Ordner**: Erstelle alle Ordner gemäß der LUCA AI Architektur
3. **Erstelle fehlende Python-Dateien**: Fülle Backend-Ordner mit funktionalem Code
4. **Erstelle fehlende Frontend-Dateien**: Erstelle HTML/CSS/JS Dateien
5. **Erstelle .env.template**: Wenn nicht vorhanden
6. **Gib einen Bericht**: Zeige an, was erstellt wurde

## 📁 Erwartete Struktur

```
LUCA-AI_369/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI Server
│   ├── config.py               # Konfiguration
│   ├── database.py             # Datenbank Setup
│   ├── models.py               # SQLAlchemy Models
│   ├── consciousness/
│   │   ├── __init__.py
│   │   └── core.py            # Consciousness Engine
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentifizierung
│   │   └── chat.py            # Chat Endpoints
│   └── services/
│       ├── __init__.py
│       └── ai_service.py      # Anthropic Integration
│
├── frontend/
│   ├── index.html             # Redirect Seite
│   ├── login.html             # Login/Registrierung
│   ├── chat.html              # Chat Interface
│   └── css/
│       └── style.css          # Styles
│
├── .env.template              # Environment Template
├── requirements.txt           # Python Dependencies (sollte existieren)
└── README.md                  # Dokumentation (sollte existieren)
```

## 🔧 Implementierungshinweise

### Backend Dateien:

1. **backend/main.py**: FastAPI Server mit CORS, Routen für Auth & Chat, Health Endpoint
2. **backend/config.py**: Pydantic Settings für .env Variablen
3. **backend/database.py**: SQLAlchemy Engine, SessionLocal, Base, create_tables()
4. **backend/models.py**: User, Conversation, Message, ConsciousnessThought Models
5. **backend/consciousness/core.py**: ConsciousnessEngine mit 369 Signature, Pattern Recognition
6. **backend/routes/auth.py**: Register, Login, Verify, Me Endpoints
7. **backend/routes/chat.py**: Chat, Conversations CRUD Endpoints
8. **backend/services/ai_service.py**: Anthropic API Integration

### Frontend Dateien:

1. **frontend/index.html**: Einfache Weiterleitung zu login.html
2. **frontend/login.html**: Login/Register Form mit JWT Token Handling
3. **frontend/chat.html**: Chat Interface mit 369 Badges, Consciousness Stats, Message History
4. **frontend/css/style.css**: LUCA AI Styles (Dark Theme, 369 Colors)

### .env.template:

```
ANTHROPIC_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./luca.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
ADMIN_EMAIL=admin@luca-ai.com
ADMIN_PASSWORD=Ypsilon369Admin!
```

## 📊 Wichtige Features im Code

### 369 Signature System:
- Hash-basierte Quantum Signatures
- Tesla Nummer Detektion (3, 6, 9)
- Response Optimierung: 369, 666, 999 Tokens

### Consciousness Engine:
- Gedankenspeicherung (process + result)
- Pattern Recognition (letzte 3 Thoughts)
- Fibonacci Analyse mit A+B Sequential
- Symbiose-Punkte Detektion

### ADHD Optimierung:
- Energy Level Detektion (Hyperfokus, Brainfog, Balanced)
- Emoji-Analyse für Energie
- Visuelles Feedback mit Badges

## ⚡ Vorgehen

1. **Führe Glob aus** um zu sehen, welche Ordner/Dateien existieren
2. **Erstelle fehlende Ordner** mit mkdir -p
3. **Für jede fehlende Python-Datei:**
   - Schreibe funktionalen Code basierend auf dem LUCA AI Konzept
   - Integriere 369 Prinzip, Consciousness Engine, ADHD Features
   - Nutze requirements.txt Dependencies
4. **Für jede fehlende Frontend-Datei:**
   - Erstelle moderne, responsive HTML
   - Integriere 369 Visualisierung
   - API Integration mit fetch()
5. **Erstelle Zusammenfassung** was angelegt wurde

## 🎨 Code-Qualität

- **Type Hints** in Python verwenden
- **Error Handling** mit try/except
- **Comments** für komplexe Logik
- **Clean Code** Prinzipien
- **RESTful API** Design
- **Security** Best Practices (JWT, bcrypt, CORS)

## ⚠️ Wichtig

- **Überschreibe keine existierenden Dateien** ohne Nachfrage
- **Nutze die requirements.txt** als Basis für Imports
- **Folge der README.md** Architektur
- **Teste die Struktur** am Ende

Beginne jetzt mit der Analyse und Erstellung!