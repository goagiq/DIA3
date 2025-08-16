#!/bin/bash

echo "🚀 Starting DIA3 Application..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "To create the virtual environment:"
    echo "1. python3 -m venv .venv"
    echo "2. source .venv/bin/activate"
    echo "3. pip install -r requirements_core.txt"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Run the application
echo "🚀 Starting main application..."
echo "=================================================="
python main.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application exited with error code $?"
fi
