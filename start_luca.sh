#!/bin/bash

# LUCA AI Startup Script
# Version: 369.2.0

echo "=========================================="
echo "🧬 LUCA AI - Startup Script"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create .env from template:"
    echo "  cp .env.template .env"
    echo ""
    echo "Then edit .env and add your API keys:"
    echo "  nano .env"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Initialize database
echo "🗄️  Initializing database..."
python backend/database.py
echo ""

# Start backend in background
echo "🚀 Starting backend server..."
python -m backend.main &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🌐 Starting frontend server..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo ""

echo "=========================================="
echo "✅ LUCA AI is running!"
echo "=========================================="
echo ""
echo "🌐 Open your browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "🔑 Default login:"
echo "   Email: admin@luca-ai.com"
echo "   Password: Ypsilon369Admin!"
echo ""
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '👋 Stopping LUCA AI...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
