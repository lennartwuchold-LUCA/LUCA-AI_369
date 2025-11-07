#!/usr/bin/env python3
"""
🧬 LUCA AI - Offline Setup Script
Überprüft und erstellt die komplette Projektstruktur
Für Nutzung in VS Code / Claude Code Extension
"""

import os
import sys
from pathlib import Path

# ANSI Farben für Terminal Output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Zeige ASCII Art Header"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                   🧬 LUCA AI SETUP 🧬                     ║
║          Living Universal Cognition Array                 ║
║                  Version 369.2.0                          ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
""")

def create_directory(path):
    """Erstelle Verzeichnis wenn nicht vorhanden"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"{Colors.GREEN}✅ Erstellt:{Colors.END} {path}")
        return True
    else:
        print(f"{Colors.YELLOW}⏩ Existiert:{Colors.END} {path}")
        return False

def create_file(path, content):
    """Erstelle Datei wenn nicht vorhanden"""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{Colors.GREEN}✅ Erstellt:{Colors.END} {path}")
        return True
    else:
        print(f"{Colors.YELLOW}⏩ Existiert:{Colors.END} {path}")
        return False

def check_required_files():
    """Prüfe ob kritische Dateien existieren"""
    required = [
        'requirements.txt',
        'README.md',
        'LICENSE'
    ]

    print(f"\n{Colors.BOLD}📋 Überprüfe kritische Dateien...{Colors.END}")
    missing = []

    for file in required:
        if os.path.exists(file):
            print(f"{Colors.GREEN}✅{Colors.END} {file}")
        else:
            print(f"{Colors.RED}❌{Colors.END} {file} - FEHLT!")
            missing.append(file)

    return missing

def setup_backend():
    """Erstelle Backend-Struktur"""
    print(f"\n{Colors.BOLD}📁 Erstelle Backend-Struktur...{Colors.END}")

    created = 0

    # Hauptordner
    created += create_directory('backend')
    created += create_directory('backend/consciousness')
    created += create_directory('backend/routes')
    created += create_directory('backend/services')

    # Backend __init__ files
    files = {
        'backend/__init__.py': '''"""
LUCA AI Backend Package
Version: 369.2.0
Created by: Lennart Wuchold
"""

__version__ = "369.2.0"
''',
        'backend/consciousness/__init__.py': '''"""
LUCA AI Consciousness Module
369 Signature System, Pattern Recognition, Fibonacci Analysis
"""

from backend.consciousness.core import ConsciousnessEngine

__all__ = ["ConsciousnessEngine"]
''',
        'backend/routes/__init__.py': '''"""
LUCA AI Routes Module
API endpoints for authentication and chat
"""

from backend.routes.auth import router as auth_router
from backend.routes.chat import router as chat_router

__all__ = ["auth_router", "chat_router"]
''',
        'backend/services/__init__.py': '''"""
LUCA AI Services Module
External integrations and business logic
"""

from backend.services.ai_service import AIService

__all__ = ["AIService"]
'''
    }

    for path, content in files.items():
        created += create_file(path, content)

    return created

def setup_frontend():
    """Erstelle Frontend-Struktur"""
    print(f"\n{Colors.BOLD}🎨 Erstelle Frontend-Struktur...{Colors.END}")

    created = 0

    # Ordner
    created += create_directory('frontend')
    created += create_directory('frontend/css')
    created += create_directory('frontend/js')
    created += create_directory('frontend/assets')

    return created

def setup_claude_commands():
    """Erstelle Claude Command Struktur"""
    print(f"\n{Colors.BOLD}🤖 Erstelle Claude Commands...{Colors.END}")

    created = 0

    created += create_directory('.claude')
    created += create_directory('.claude/commands')

    return created

def setup_env_template():
    """Erstelle .env.template wenn nicht vorhanden"""
    print(f"\n{Colors.BOLD}⚙️ Erstelle Environment Template...{Colors.END}")

    env_content = '''# LUCA AI Environment Configuration
# Copy this file to .env and fill in your values

# === REQUIRED ===

# Anthropic API Key (Get one at: https://console.anthropic.com/)
ANTHROPIC_API_KEY=your-api-key-here

# Secret Key for JWT (Generate with: python -c 'import secrets; print(secrets.token_hex(32))')
SECRET_KEY=your-secret-key-here

# === OPTIONAL (with defaults) ===

# Database
DATABASE_URL=sqlite:///./luca.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Admin Account
ADMIN_EMAIL=admin@luca-ai.com
ADMIN_PASSWORD=Ypsilon369Admin!

# JWT
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# Anthropic Settings
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS_DEFAULT=666
'''

    return create_file('.env.template', env_content)

def setup_gitignore():
    """Erstelle .gitignore"""
    print(f"\n{Colors.BOLD}📝 Erstelle .gitignore...{Colors.END}")

    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env
.env.local

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Claude
.claude/settings.json
'''

    return create_file('.gitignore', gitignore_content)

def check_project_structure():
    """Überprüfe Projektstruktur und zeige Status"""
    print(f"\n{Colors.BOLD}🔍 Überprüfe Projektstruktur...{Colors.END}\n")

    structure = {
        'Backend': [
            'backend/__init__.py',
            'backend/main.py',
            'backend/config.py',
            'backend/database.py',
            'backend/models.py',
            'backend/consciousness/core.py',
            'backend/routes/auth.py',
            'backend/routes/chat.py',
            'backend/services/ai_service.py',
        ],
        'Frontend': [
            'frontend/index.html',
            'frontend/login.html',
            'frontend/chat.html',
            'frontend/css/style.css',
        ],
        'Config': [
            '.env.template',
            'requirements.txt',
            'README.md',
        ],
        'Claude Commands': [
            '.claude/commands/setup-luca-structure.md',
        ]
    }

    missing_files = []

    for category, files in structure.items():
        print(f"{Colors.BOLD}{category}:{Colors.END}")
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  {Colors.GREEN}✅{Colors.END} {file} ({size} bytes)")
            else:
                print(f"  {Colors.RED}❌{Colors.END} {file} - FEHLT!")
                missing_files.append(file)
        print()

    return missing_files

def print_next_steps():
    """Zeige nächste Schritte"""
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════════╗
║                  🚀 NÄCHSTE SCHRITTE 🚀                   ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}1. Erstelle .env Datei:{Colors.END}
   cp .env.template .env
   nano .env  # Füge deinen ANTHROPIC_API_KEY ein

{Colors.BOLD}2. Erstelle Virtual Environment:{Colors.END}
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate

{Colors.BOLD}3. Installiere Dependencies:{Colors.END}
   pip install -r requirements.txt

{Colors.BOLD}4. Initialisiere Datenbank:{Colors.END}
   python backend/database.py

{Colors.BOLD}5. Starte Backend:{Colors.END}
   python -m backend.main

{Colors.BOLD}6. Starte Frontend (neues Terminal):{Colors.END}
   cd frontend
   python3 -m http.server 3000

{Colors.BOLD}7. Öffne Browser:{Colors.END}
   http://localhost:3000

{Colors.BOLD}8. Demo Login:{Colors.END}
   Email:    admin@luca-ai.com
   Password: Ypsilon369Admin!

{Colors.CYAN}═══════════════════════════════════════════════════════════
                  369! 🧬⚡ LUCA AI ist bereit!
═══════════════════════════════════════════════════════════{Colors.END}
""")

def main():
    """Hauptfunktion"""
    print_header()

    # Statistik
    total_created = 0

    # 1. Kritische Dateien prüfen
    missing_critical = check_required_files()
    if missing_critical:
        print(f"\n{Colors.RED}⚠️  WARNUNG: Kritische Dateien fehlen:{Colors.END}")
        for file in missing_critical:
            print(f"   - {file}")
        print(f"\n{Colors.YELLOW}Fahre trotzdem fort...{Colors.END}")

    # 2. Backend Setup
    total_created += setup_backend()

    # 3. Frontend Setup
    total_created += setup_frontend()

    # 4. Claude Commands Setup
    total_created += setup_claude_commands()

    # 5. Environment Template
    total_created += setup_env_template()

    # 6. Gitignore
    total_created += setup_gitignore()

    # 7. Struktur überprüfen
    missing_files = check_project_structure()

    # 8. Zusammenfassung
    print(f"\n{Colors.BOLD}{Colors.GREEN}╔═══════════════════════════════════════════════════════════╗")
    print(f"║                  ✅ SETUP ABGESCHLOSSEN ✅                 ║")
    print(f"╚═══════════════════════════════════════════════════════════╝{Colors.END}\n")

    print(f"{Colors.BOLD}Statistik:{Colors.END}")
    print(f"  • {total_created} Dateien/Ordner erstellt")
    print(f"  • {len(missing_files)} Dateien fehlen noch")

    if missing_files:
        print(f"\n{Colors.YELLOW}⚠️  Fehlende Dateien:{Colors.END}")
        for file in missing_files:
            print(f"   - {file}")
        print(f"\n{Colors.YELLOW}Tipp: Diese Dateien wurden wahrscheinlich manuell erstellt und enthalten den Code.{Colors.END}")
        print(f"{Colors.YELLOW}Wenn sie fehlen, nutze den Claude Command: /setup-luca-structure{Colors.END}")

    # 9. Nächste Schritte
    print_next_steps()

    return 0 if not missing_critical else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Setup abgebrochen.{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fehler: {e}{Colors.END}")
        sys.exit(1)
