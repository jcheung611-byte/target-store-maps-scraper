#!/bin/bash

# Target Store Maps Scraper - Quick Start Script
# This script helps you get started with the setup process

set -e

echo "🎯 Target Store Maps Scraper - Quick Start"
echo "=========================================="
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is optimized for macOS"
    echo ""
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
echo "Checking Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
else
    echo "✗ Python 3 not found"
    echo "  Install from: https://www.python.org/downloads/"
    exit 1
fi

# Check if adb exists
echo ""
echo "Checking Android Debug Bridge (adb)..."
if command_exists adb; then
    echo "✓ adb installed"
else
    echo "✗ adb not found"
    echo "  Install Android Studio or run:"
    echo "  brew install --cask android-platform-tools"
fi

# Check if emulator exists
echo ""
echo "Checking Android Emulator..."
if command_exists emulator; then
    echo "✓ emulator installed"
else
    echo "✗ emulator not found"
    echo "  Install Android Studio and configure AVD"
fi

# Check if mitmproxy exists
echo ""
echo "Checking mitmproxy..."
if command_exists mitmproxy; then
    MITM_VERSION=$(mitmproxy --version | head -n 1)
    echo "✓ $MITM_VERSION"
else
    echo "✗ mitmproxy not found"
    echo "  Installing mitmproxy..."
    if command_exists brew; then
        brew install mitmproxy
        echo "✓ mitmproxy installed"
    else
        echo "  Run: brew install mitmproxy"
        echo "  Or visit: https://mitmproxy.org/"
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --quiet
    echo "✓ Python packages installed"
else
    echo "✗ requirements.txt not found"
fi

# Verify setup
echo ""
echo "Running setup verification..."
python3 scripts/verify_setup.py

echo ""
echo "=========================================="
echo "📚 Next Steps:"
echo ""
echo "1. Set up Android Emulator:"
echo "   • Open Android Studio → Tools → Device Manager"
echo "   • Create new device (Pixel 5, Android 13 - Google APIs)"
echo ""
echo "2. Read the detailed setup guide:"
echo "   cat SETUP_GUIDE.md"
echo ""
echo "3. Start capturing API traffic:"
echo "   # Terminal 1: Start emulator"
echo "   emulator -avd target_scraper -writable-system &"
echo ""
echo "   # Terminal 2: Start mitmproxy"
echo "   mitmweb --listen-port 8080 --web-port 8081"
echo ""
echo "   # Terminal 3: Capture traffic"
echo "   python3 scripts/capture_api_traffic.py"
echo ""
echo "=========================================="






