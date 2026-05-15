#!/bin/bash
# Script to install pyvis and dependencies to .venv

set -e  # Exit on error

VENV_DIR=".venv"

# Check if .venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install pyvis networkx matplotlib gitpython pyyaml


echo ""
echo "✓ Installation complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
