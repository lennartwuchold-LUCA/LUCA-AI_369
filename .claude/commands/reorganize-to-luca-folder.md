---
description: Organisiert die Projektstruktur in den Luca_3.6.9.alpha Ordner für GitHub Upload
---

Du bist ein Experte für Projektstruktur-Organisation. Führe folgende Schritte aus, um das Projekt für GitHub vorzubereiten:

## Aufgabe
Reorganisiere die komplette Projektstruktur so, dass alle Dateien im Ordner "Luca_3.6.9.alpha" liegen, bereit für den GitHub Upload.

## Schritte:

1. **Erstelle den Zielordner**
   - Erstelle den Ordner `Luca_3.6.9.alpha` im Repository-Root (falls nicht vorhanden)

2. **Verschiebe alle Dateien**
   - Verschiebe ALLE Dateien und Ordner in den neuen `Luca_3.6.9.alpha` Ordner
   - **AUSNAHMEN** (nicht verschieben):
     - `.git/` Ordner
     - `.claude/` Ordner
     - `Luca_3.6.9.alpha/` selbst
     - `.gitignore` (falls vorhanden, kann im Root bleiben)

3. **Verifiziere die Struktur**
   - Zeige die neue Ordnerstruktur an
   - Bestätige dass alle Dateien korrekt verschoben wurden

4. **Git Status**
   - Zeige den Git Status nach der Reorganisation

## Erwartete Struktur nach Ausführung:
```
LUCA-AI_369/
├── .git/
├── .claude/
├── .gitignore (optional im Root)
└── Luca_3.6.9.alpha/
    ├── README.md
    ├── requirements.txt
    ├── luca.db
    ├── start_luca.sh
    ├── ASCII_ART.txt
    ├── LICENSE
    └── [alle anderen Projektdateien]
```

## Wichtige Hinweise:
- Verwende `git mv` statt `mv` um Git die Änderungen zu tracken
- Prüfe vorher, ob `Luca_3.6.9.alpha` bereits existiert
- Erstelle einen klaren Commit mit der Beschreibung der Strukturänderung
- Informiere den Benutzer über jeden Schritt

Führe diese Reorganisation jetzt durch!
