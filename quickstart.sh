#!/bin/bash

echo "╔══════════════════════════════════════════════════════════╗"
echo "║            LLM OBSERVATORY - QUICK START                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python $python_version found"
elif command -v python &> /dev/null; then
    python_version=$(python --version 2>&1 | awk '{print $2}')
    echo "✓ Python $python_version found"
else
    echo "✗ Python not found!"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  macOS:        brew install python@3.12"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Windows:      Download from https://www.python.org/downloads/"
    exit 1
fi
echo ""

# Create virtual environment
echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
    else
        echo "✗ Failed to create virtual environment"
        exit 1
    fi
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
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi
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
echo ""
echo "3. Upload your CSV:"
echo "   • AWS Bedrock: example-bedrock-cloudwatch.csv"
echo "   • Anthropic: example-anthropic-usage.csv"
echo ""
echo "Happy analyzing! 🔭"
echo ""