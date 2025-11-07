# Claude Commands für LUCA-AI_369

## Verfügbare Commands

### 🔄 `/reorganize-to-luca-folder`

**Beschreibung:** Organisiert automatisch die gesamte Projektstruktur in den `Luca_3.6.9.alpha` Ordner für den GitHub Upload.

**Verwendung:**
```
/reorganize-to-luca-folder
```

**Was macht dieser Command:**
1. Erstellt den Ordner `Luca_3.6.9.alpha` (falls nicht vorhanden)
2. Verschiebt alle Projektdateien in diesen Ordner
3. Behält `.git/` und `.claude/` im Root
4. Verwendet `git mv` für sauberes Tracking
5. Zeigt die neue Struktur an
6. Erstellt einen Commit mit den Änderungen

**Ergebnis:**
```
LUCA-AI_369/
├── .git/
├── .claude/
└── Luca_3.6.9.alpha/
    ├── README.md
    ├── requirements.txt
    ├── luca.db
    └── [alle anderen Dateien]
```

---

## Alternative: Bash Script

Wenn du die Reorganisation manuell durchführen möchtest, kannst du auch das bereitgestellte Bash-Script verwenden:

```bash
./reorganize_structure.sh
```

Dieses Script macht das Gleiche, kann aber unabhängig von Claude ausgeführt werden.

---

## Nach der Reorganisation

1. **Überprüfen:**
   ```bash
   git status
   ls -la Luca_3.6.9.alpha/
   ```

2. **Committen:**
   ```bash
   git add .
   git commit -m "Reorganize project structure into Luca_3.6.9.alpha folder"
   ```

3. **Pushen:**
   ```bash
   git push -u origin claude/claude-command-folder-setup-011CUu2nq2mPr7zzcV7fGZXk
   ```

4. **GitHub Upload:**
   - Jetzt kannst du einfach den `Luca_3.6.9.alpha` Ordner zu GitHub hochladen
   - Die Struktur entspricht genau dem, was auf GitHub sein soll

---

## Hinweise

- 🔒 `.git/` und `.claude/` bleiben immer im Root
- ✅ Alle Dateiverschiebungen werden mit `git mv` durchgeführt
- 📊 Git tracked alle Änderungen automatisch
- 🚀 Bereit für direkten GitHub Upload

**Viel Erfolg! 🎉**

*Erstellt für: LUCA-AI_369 Project*
*Autor: Lenny*
