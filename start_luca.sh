#!/bin/bash

# LUCA AI - Startup Script
# Run this to start LUCA

echo "================================"
echo "🧬 LUCA AI - Starting Up"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Run: cp .env.template .env"
    echo "   Then edit .env with your API key"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Initialize database if not exists
if [ ! -f "luca.db" ]; then
    echo "🗄️  Initializing database..."
    python backend/database.py
fi

echo ""
echo "🚀 Starting LUCA Backend..."
echo ""

# Start backend
python -m backend.main
