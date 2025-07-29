#!/bin/bash

# Document Information Extractor - Setup Script
# Installs system dependencies and Python packages

set -e  # Exit on any error

echo "🚀 Document Information Extractor - Setup Script"
echo "================================================="

# Check if running on supported OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "📱 Detected OS: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    echo "📱 Detected OS: macOS"
else
    echo "❌ Unsupported OS: $OSTYPE"
    echo "Please install dependencies manually."
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."

if [[ "$OS" == "linux" ]]; then
    # Update package list
    echo "Updating package list..."
    sudo apt update
    
    # Install Tesseract OCR
    if ! command_exists tesseract; then
        echo "Installing Tesseract OCR..."
        sudo apt install -y tesseract-ocr libtesseract-dev
    else
        echo "✅ Tesseract already installed"
    fi
    
    # Install additional dependencies
    sudo apt install -y python3-pip python3-dev
    
elif [[ "$OS" == "macos" ]]; then
    # Check if Homebrew is installed
    if ! command_exists brew; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install Tesseract OCR
    if ! command_exists tesseract; then
        echo "Installing Tesseract OCR..."
        brew install tesseract
    else
        echo "✅ Tesseract already installed"
    fi
fi

# Verify Tesseract installation
echo ""
echo "🔍 Verifying Tesseract installation..."
if command_exists tesseract; then
    tesseract_version=$(tesseract --version | head -n1)
    echo "✅ $tesseract_version"
else
    echo "❌ Tesseract installation failed"
    exit 1
fi

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."

# Check if pip is available
if ! command_exists pip && ! command_exists pip3; then
    echo "❌ pip not found. Please install pip first."
    exit 1
fi

# Use pip3 if available, otherwise pip
if command_exists pip3; then
    PIP_CMD="pip3"
else
    PIP_CMD="pip"
fi

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    $PIP_CMD install -r requirements.txt
else
    echo "Installing individual packages..."
    $PIP_CMD install opencv-python==4.8.1.78
    $PIP_CMD install pytesseract==0.3.10
    $PIP_CMD install Pillow==10.0.1
    $PIP_CMD install numpy==1.24.3
    $PIP_CMD install openai==0.28.1
fi

# Run installation test
echo ""
echo "🧪 Running installation test..."
python3 test_installation.py

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Optional: Set OpenAI API key for better accuracy:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Run the interactive demo:"
echo "   python3 demo.py"
echo ""
echo "3. Process your first document:"
echo "   python3 document_extractor.py your_document.jpg"
echo ""
echo "📖 For detailed documentation, see README_document_extractor.md"