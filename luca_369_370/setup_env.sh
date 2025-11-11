#!/bin/bash

# LUCA 369/370 - Environment Setup Script
# Architekt: Lennart Wuchold
# Datum: 11.11.2025
# Standard: 369/370

echo "🏛️  Setting up LUCA 369/370 Environment..."
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found! Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Python found: $PYTHON_VERSION"

# Check if we're already in a virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Already in virtual environment: $VIRTUAL_ENV"
    echo "   Using existing environment..."
else
    # Create virtual environment
    echo "📦 Creating virtual environment..."
    python3 -m venv luca_venv

    # Activate
    echo "🔄 Activating virtual environment..."
    source luca_venv/bin/activate
fi

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for API Key
echo ""
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "   To use LLM Integration:"
    echo "   1. Get your key from: https://console.anthropic.com/"
    echo "   2. Run: export ANTHROPIC_API_KEY='sk-ant-your-key-here'"
    echo "   3. Add to ~/.bashrc or ~/.zshrc for persistence"
    echo ""
    echo "   Without API key, LUCA will run in static mode."
else
    echo "✅ ANTHROPIC_API_KEY found"
    # Show only first and last 4 chars for security
    KEY_START="${ANTHROPIC_API_KEY:0:7}"
    KEY_END="${ANTHROPIC_API_KEY: -4}"
    echo "   Key: ${KEY_START}...${KEY_END}"
fi

echo ""
echo "========================================"
echo "✅ Setup complete!"
echo "========================================"
echo ""
echo "🚀 To use LUCA:"
echo ""
echo "  1. Activate environment (if not already active):"
echo "     source luca_venv/bin/activate"
echo ""
echo "  2. Set API Key (for LLM integration):"
echo "     export ANTHROPIC_API_KEY='sk-ant-your-key'"
echo ""
echo "  3. Run LUCA CLI:"
echo "     python luca_cli.py"
echo ""
echo "  4. Or run tests:"
echo "     pytest tests/ -v"
echo ""
echo "🏛️  Ready to build with LUCA 369/370!"
echo "========================================"
