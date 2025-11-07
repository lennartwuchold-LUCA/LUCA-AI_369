#!/bin/bash

# LUCA-AI_369 Ordnerstruktur Reorganisation Script
# Verschiebt alle Dateien in den Luca_3.6.9.alpha Ordner für GitHub Upload

set -e  # Beende bei Fehler

echo "================================================"
echo "  LUCA-AI_369 Struktur Reorganisation"
echo "================================================"
echo ""

# Definiere Farben für bessere Lesbarkeit
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Arbeitsverzeichnis
REPO_ROOT="/home/user/LUCA-AI_369"
TARGET_FOLDER="Luca_3.6.9.alpha"

cd "$REPO_ROOT"

# Prüfe ob Git Repository
if [ ! -d ".git" ]; then
    echo "❌ Fehler: Kein Git Repository gefunden!"
    exit 1
fi

echo -e "${BLUE}📁 Schritt 1: Erstelle Zielordner${NC}"
if [ -d "$TARGET_FOLDER" ]; then
    echo -e "${YELLOW}⚠️  Ordner '$TARGET_FOLDER' existiert bereits${NC}"
else
    mkdir -p "$TARGET_FOLDER"
    echo -e "${GREEN}✓ Ordner '$TARGET_FOLDER' erstellt${NC}"
fi
echo ""

echo -e "${BLUE}📦 Schritt 2: Verschiebe Dateien${NC}"
moved_count=0

# Liste alle Dateien und Ordner im Root (außer versteckte und Target)
for item in *; do
    # Überspringe den Zielordner selbst
    if [ "$item" == "$TARGET_FOLDER" ]; then
        continue
    fi

    # Verschiebe mit git mv
    if [ -e "$item" ]; then
        echo "  → Verschiebe: $item"
        git mv "$item" "$TARGET_FOLDER/"
        ((moved_count++))
    fi
done

echo -e "${GREEN}✓ $moved_count Dateien/Ordner verschoben${NC}"
echo ""

echo -e "${BLUE}📋 Schritt 3: Zeige neue Struktur${NC}"
echo ""
echo "Root-Verzeichnis:"
ls -la | grep -v "^total" | head -10
echo ""
echo "$TARGET_FOLDER Inhalt:"
ls -la "$TARGET_FOLDER/" | grep -v "^total" | head -15
echo ""

echo -e "${BLUE}📊 Schritt 4: Git Status${NC}"
git status
echo ""

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  ✓ Reorganisation abgeschlossen!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Nächste Schritte:"
echo "1. Überprüfe die Änderungen: git status"
echo "2. Committe die Änderungen: git add . && git commit -m 'Reorganize structure into $TARGET_FOLDER'"
echo "3. Pushe zum Repository: git push -u origin claude/claude-command-folder-setup-011CUu2nq2mPr7zzcV7fGZXk"
echo ""
echo "Danach kannst du den Ordner '$TARGET_FOLDER' einfach zu GitHub hochladen!"
