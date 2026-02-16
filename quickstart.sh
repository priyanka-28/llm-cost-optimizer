#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║            LLM OBSERVATORY - QUICK START                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Choose python executable
echo "Step 1: Checking Python installation..."
PYTHON=python3
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python $python_version found (python3)"
elif command -v python &> /dev/null; then
    PYTHON=python
    python_version=$(python --version 2>&1 | awk '{print $2}')
    echo "✓ Python $python_version found (python)"
else
    echo "✗ Python not found!"
    echo ""
    echo "Please install Python 3.10+:"
    echo "  macOS:         brew install python"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Windows:       Download from https://www.python.org/downloads/"
    exit 1
fi
echo ""

# Create virtual environment
echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    $PYTHON -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Step 4: Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel -q
echo "✓ Tools upgraded"
echo ""

# Install dependencies
echo "Step 5: Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  SETUP COMPLETE! 🎉                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Start the app:"
echo "   python app.py"
echo ""
echo "2. Open in browser:"
echo "   http://localhost:8000"
echo "   (If localhost fails, try http://127.0.0.1:8000)"
echo ""
echo "Happy analyzing! 🔭"
echo ""