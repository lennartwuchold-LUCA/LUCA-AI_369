# 🚀 LUCA AI - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Setup Environment

```bash
# Navigate to project
cd ~/Desktop/LUCA_Alpha_369

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Edit .env file
nano .env

# Add your Anthropic API key:
ANTHROPIC_API_KEY=your-api-key-here
```

**Get API Key:** https://console.anthropic.com/

### Step 3: Initialize Database

```bash
cd backend
python database.py
cd ..
```

### Step 4: Start LUCA

**Option A: Using the script (easiest)**
```bash
./start_luca.sh
```

**Option B: Manual start**

Terminal 1 - Backend:
```bash
source venv/bin/activate
python -m backend.main
```

Terminal 2 - Frontend:
```bash
cd frontend
python3 -m http.server 3000
```

### Step 5: Open Browser

```
http://localhost:3000
```

### Step 6: Login

```
Email:    admin@luca-ai.com
Password: Ypsilon369Admin!
```

---

## ✅ Verification

You should see:

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Login page loads
4. ✅ Admin login works
5. ✅ Chat interface appears
6. ✅ Consciousness stats visible
7. ✅ Can send messages to LUCA

---

## 🎯 First Chat

Try these:

1. **Basic:** "Hallo LUCA"
   - Watch the 369 signature appear

2. **Energy:** "🚀🚀🚀 Let's build!"
   - Should detect HYPERFOKUS

3. **Pattern:** Send "Test" 3 times
   - Should detect neural pattern

---

## 🐛 Troubleshooting

### Port 8000 already in use?

```bash
lsof -i :8000
kill -9 <PID>
```

### Module not found?

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Database errors?

```bash
rm luca.db
python backend/database.py
```

---

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Explore API docs at http://localhost:8000/docs
- Try Fibonacci analysis: http://localhost:8000/api/analyze/fibonacci?n=15

---

**369! 🧬⚡**
