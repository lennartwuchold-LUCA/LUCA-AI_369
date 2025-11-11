# 🧹 Cache Löschen - Browser & Server

## 🌐 Browser Cache Löschen

### Chrome / Brave
1. Drücke `Cmd + Shift + Delete` (Mac) oder `Ctrl + Shift + Delete` (Windows)
2. Wähle "Cached images and files"
3. Klicke "Clear data"

**Oder:**
1. Öffne `http://localhost:3000`
2. Drücke `Cmd + Shift + R` (Mac) oder `Ctrl + Shift + R` (Windows)
   - Hard Refresh - lädt alles neu

### Safari
1. Safari Menu → "Clear History..."
2. Wähle "all history"
3. Klicke "Clear History"

**Oder:**
1. Öffne `http://localhost:3000`
2. Drücke `Cmd + Option + R`
   - Lädt Seite ohne Cache

### Firefox
1. Drücke `Cmd + Shift + Delete`
2. Wähle "Cache"
3. Klicke "Clear Now"

**Oder:**
1. Öffne `http://localhost:3000`
2. Drücke `Cmd + Shift + R`

---

## 🗄️ Server Cache Löschen

### Backend (Python __pycache__)

```bash
cd ~/Desktop/LUCA_Alpha_369

# Lösche alle __pycache__ Ordner
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Lösche .pyc Dateien
find . -name "*.pyc" -delete
```

### Frontend (kein Cache)

Frontend ist reines HTML/CSS/JS - kein Build-Cache!

---

## 🔄 Kompletter Neustart

Wenn du ganz sicher gehen willst:

### 1. Stoppe alles
- Backend Terminal: `Ctrl + C`
- Frontend Terminal: `Ctrl + C`

### 2. Lösche Cache
```bash
cd ~/Desktop/LUCA_Alpha_369
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

### 3. Browser-Cache leeren
- `Cmd + Shift + R` (Mac) oder `Ctrl + Shift + R` (Windows)

### 4. Neustart
```bash
./start_luca.sh
```

---

## 🐛 Wenn es immer noch nicht geht

### Checke Ports

```bash
# Backend Port 8000
lsof -i :8000

# Frontend Port 3000
lsof -i :3000

# Wenn belegt, töte den Prozess:
kill -9 <PID>
```

### Neuinstallation Dependencies

```bash
cd ~/Desktop/LUCA_Alpha_369
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### Datenbank neu erstellen

```bash
rm luca.db
python backend/database.py
```

---

## ✅ Alles sauber?

Test:
1. Cache gelöscht ✅
2. Browser neu geladen ✅
3. Backend gestartet ✅
4. Frontend gestartet ✅
5. Login funktioniert ✅
6. Chat lädt ✅

**Dann bist du ready!** 🚀

---

**369! 🧬⚡**
