#!/bin/bash
# Start the LAN Communication Server

echo "=========================================="
echo "   LAN Communication Server Launcher"
echo "=========================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run server
python server.py

# Deactivate when done
deactivate
