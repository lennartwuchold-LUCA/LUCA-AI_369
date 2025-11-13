#!/bin/bash
# LUCA AI 369 - Sicheres Setup Script
# Erstellt .env Datei und testet das System

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🌌 LUCA AI 369 - Automatischer UX/UI Design-Generator       ║"
echo "║  Tesla 3-6-9 Resonanz - Meta-Claude Aktiviert                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Prüfe ob .env existiert
if [ -f .env ]; then
    echo "✅ .env Datei existiert bereits"
    source .env
else
    echo "⚠️  Keine .env Datei gefunden"
    echo ""
    echo "Erstelle .env aus Template..."

    if [ -f .env.example ]; then
        cp .env.example .env
        chmod 600 .env
        echo "✅ .env erstellt (Berechtigungen: 600)"
        echo ""
        echo "📝 WICHTIG: Editiere jetzt die .env Datei und füge deinen echten API-Key ein:"
        echo "   nano .env"
        echo "   oder"
        echo "   vim .env"
        echo ""
        echo "Setze deinen Anthropic API-Key:"
        echo "   ANTHROPIC_API_KEY=sk-ant-your_real_key_here"
        echo ""
        read -p "Drücke Enter wenn du die .env Datei editiert hast..."

        source .env
    else
        echo "❌ .env.example nicht gefunden!"
        exit 1
    fi
fi

# Prüfe API-Key
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ]; then
    echo ""
    echo "⚠️  WARNING: ANTHROPIC_API_KEY nicht gesetzt oder ist Placeholder!"
    echo ""
    echo "Der Design-Generator wird im FALLBACK-Modus laufen."
    echo "Für vollständige Funktionalität, setze einen echten API-Key in .env"
    echo ""
    read -p "Trotzdem fortfahren? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    echo "✅ ANTHROPIC_API_KEY gesetzt"
fi

# Prüfe Python
echo ""
echo "🔧 Prüfe System-Requirements..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nicht gefunden!"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Prüfe Dependencies
echo ""
echo "📦 Prüfe Python-Dependencies..."
if ! python3 -c "import anthropic" 2>/dev/null; then
    echo "⚠️  anthropic nicht installiert"
    echo "Installiere Dependencies..."
    pip install anthropic numpy
fi
echo "✅ Dependencies OK"

# Optional: Flutter check
if command -v flutter &> /dev/null; then
    echo "✅ Flutter: $(flutter --version | head -1)"
else
    echo "⚠️  Flutter nicht installiert (optional für App-Entwicklung)"
fi

# Erstelle notwendige Verzeichnisse
echo ""
echo "📁 Erstelle Verzeichnisse..."
mkdir -p luca/generated/flutter
mkdir -p luca/generated/ios
mkdir -p luca/generated/android
mkdir -p .private
echo "✅ Verzeichnisse erstellt"

# Zeige Konfiguration
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🎨 LUCA Konfiguration                                        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo "Operator Seed: ${LUCA_OPERATOR_SEED:-nicht gesetzt}"
echo "Version: ${LUCA_VERSION:-nicht gesetzt}"
echo "Vector: ${LUCA_VECTOR:-nicht gesetzt}"
echo "Tag: ${LUCA_TAG:-nicht gesetzt}"
echo ""

# Frage ob Test ausführen
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🚀 Bereit zum Testen                                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
read -p "Design-Generator jetzt testen? (Y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "✅ Setup abgeschlossen!"
    echo "Starte den Test später mit: python test_generate_ui.py"
    exit 0
fi

# Test ausführen
echo ""
echo "🎨 Starte Design-Generator Test..."
echo "═══════════════════════════════════════════════════════════════"
python3 test_generate_ui.py

# Ergebnis
if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║  ✅ LUCA UX/UI Design-Generator erfolgreich getestet!        ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📱 Nächste Schritte:"
    echo ""
    echo "1. Flutter App starten:"
    echo "   cd luca/generated/flutter"
    echo "   flutter pub get"
    echo "   flutter run"
    echo ""
    echo "2. Generierte Dateien ansehen:"
    echo "   ls -la luca/generated/"
    echo ""
    echo "3. Design-Tokens prüfen:"
    echo "   cat luca/generated/design_tokens.json"
    echo ""
    echo "🌌 Das Feld designet sich selbst - Meta-Claude aktiviert!"
else
    echo ""
    echo "❌ Test fehlgeschlagen - siehe Fehler oben"
    exit 1
fi
