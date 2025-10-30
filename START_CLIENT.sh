#!/bin/bash
# Start the LAN Communication Client

echo "=========================================="
echo "   LAN Communication Client Launcher"
echo "=========================================="
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run client
python client.py

# Deactivate when done
deactivate
