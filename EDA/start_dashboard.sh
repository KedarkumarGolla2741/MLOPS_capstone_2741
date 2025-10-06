#!/bin/bash
# Startup script for MLOPS Analytics Dashboard on Linux/Mac

echo "================================================"
echo "  MLOPS Analytics Dashboard - Unix Launcher"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
else
    echo "Dependencies already installed."
fi

echo ""
echo "[2/3] Checking data files..."
if [ ! -f "customer_shopping_data.csv" ]; then
    echo "Error: customer_shopping_data.csv not found!"
    echo "Please ensure the data file is in the current directory."
    exit 1
fi

if [ ! -f "Region_detail_table.csv" ]; then
    echo "Error: Region_detail_table.csv not found!"
    echo "Please ensure the data file is in the current directory."
    exit 1
fi

echo ""
echo "[3/3] Starting dashboard..."
echo ""
echo "================================================"
echo "  Dashboard will be available at:"
echo "  http://localhost:8000"
echo ""
echo "  Press CTRL+C to stop the server"
echo "================================================"
echo ""

python3 run_dashboard.py