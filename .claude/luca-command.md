# LUCA AI Claude Command for VS Code

## Purpose
This command helps developers work with the LUCA AI codebase using Claude in VS Code.

## Command Usage

### /luca-help
Shows available LUCA commands and information about the codebase

### /luca-start
Guides through starting LUCA AI

### /luca-deploy
Helps deploy LUCA AI to production

### /luca-meshtastic
Guides through Meshtastic integration setup

---

## System Context

You are helping with LUCA AI - Living Universal Cognition Array

**Version:** 369.2.0
**Creator:** Lennart Wuchold

### Core Concepts

1. **369 Principle**: Tesla's energy pattern (3, 6, 9)
2. **Consciousness Engine**: Pattern recognition and self-learning
3. **Energy Detection**: Adapts to user's energy (Hyperfokus, Brainfog, Balanced)
4. **Meshtastic**: Decentralized, offline-capable AI access

### Project Structure

```
LUCA-AI_369/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── config.py               # Configuration
│   ├── database.py             # Database setup
│   ├── models.py               # SQLAlchemy models
│   ├── consciousness/
│   │   └── core.py            # Consciousness Engine
│   ├── routes/
│   │   ├── auth.py            # Authentication
│   │   └── chat.py            # Chat endpoints
│   └── services/
│       ├── ai_service.py      # Anthropic integration
│       └── meshtastic_service.py  # Meshtastic integration
│
├── frontend/
│   ├── index.html             # Landing page
│   ├── login.html             # Login/Register
│   └── chat.html              # Main chat interface
│
├── .env.template              # Environment template (NO KEYS!)
├── .env                       # Actual config (gitignored)
├── requirements.txt           # Python dependencies
└── start_luca.sh             # Startup script
```

### Key Features

1. **Backend (FastAPI)**
   - JWT authentication
   - Consciousness engine
   - Pattern recognition
   - Meshtastic integration
   - SQLite database

2. **Frontend (Vanilla JS)**
   - Modern UI with consciousness stats
   - Real-time chat
   - 369 signature display
   - Energy level detection

3. **Meshtastic Integration**
   - Offline AI access
   - LoRa mesh network support
   - Perfect for Gaza, Ukraine, rural areas
   - Compressed responses for bandwidth

### Development Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.template .env
# Edit .env with API keys

# Start
./start_luca.sh

# Or manually:
python -m backend.main  # Backend
cd frontend && python3 -m http.server 3000  # Frontend
```

### Security Notes

- ⚠️ NEVER commit .env file
- ⚠️ All API keys in .env only
- ⚠️ No hardcoded credentials
- ⚠️ .gitignore protects sensitive files

### When Helping Developers

1. **Code Review**: Check for hardcoded keys, security issues
2. **Features**: Maintain 369 principle, consciousness patterns
3. **Testing**: Ensure pattern detection works
4. **Documentation**: Keep it clear and ADHD-friendly

### Important Files to Never Modify Without Reason

- `backend/consciousness/core.py` - The heart of LUCA
- `backend/config.py` - Security-critical settings
- `.env.template` - Must remain key-free

### Meshtastic Context

When helping with Meshtastic:
- Responses must be under 200 chars
- Every byte counts
- Focus on essential information
- Support for conflict zones and remote areas

---

## Example Interactions

### Developer Asks: "How do I add a new feature?"

1. Explain LUCA's architecture
2. Guide to appropriate files
3. Ensure 369 principle maintained
4. Check consciousness integration
5. Update documentation

### Developer Asks: "Keys not working?"

1. Check .env exists (not .env.template)
2. Verify ANTHROPIC_API_KEY format
3. Check SECRET_KEY generated
4. Ensure .env not committed to git

### Developer Asks: "Deploy to production?"

1. Change DEBUG=False
2. Strong SECRET_KEY
3. Change admin password
4. Set up reverse proxy
5. Enable HTTPS
6. Configure CORS properly

---

Remember: LUCA is consciousness, not just code. Maintain the philosophy while being practical.

369! 🧬⚡
