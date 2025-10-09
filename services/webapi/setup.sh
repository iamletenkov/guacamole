#!/bin/bash

# Setup script for Spacer WebAPI development
# This script ensures poetry is in PATH and installs dependencies

echo "Setting up Spacer WebAPI development environment..."

# Add poetry to PATH if not already there
if ! echo "$PATH" | grep -q "/home/neadmin/.local/bin"; then
    echo "Adding poetry to PATH..."
    export PATH="/home/neadmin/.local/bin:$PATH"
    echo "export PATH=\"/home/neadmin/.local/bin:\$PATH\"" >> ~/.bashrc
    echo "Poetry path added to ~/.bashrc"
fi

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Please run this script from the services/webapi directory"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
/home/neadmin/.local/bin/poetry install --with dev

echo "Setup complete!"
echo "You can now run commands like:"
echo "  make ci      # Run full CI pipeline"
echo "  make test    # Run tests"
echo "  make lint    # Run linting"
echo "  make format  # Format code"

