#!/bin/bash

# Invoice Information Extractor - Installation Script
# This script installs all necessary dependencies for OCR and LLM-based invoice extraction

echo "🔧 Installing Invoice Information Extractor Dependencies"
echo "========================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Install Tesseract OCR engine based on OS
echo ""
echo "📦 Installing Tesseract OCR engine..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "🐧 Detected Ubuntu/Debian - installing tesseract-ocr"
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
    elif command -v yum &> /dev/null; then
        echo "🎩 Detected CentOS/RHEL - installing tesseract"
        sudo yum install -y tesseract tesseract-langpack-eng
    elif command -v dnf &> /dev/null; then
        echo "🎩 Detected Fedora - installing tesseract"
        sudo dnf install -y tesseract tesseract-langpack-eng
    else
        echo "⚠️  Could not detect package manager. Please install tesseract manually."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        echo "🍎 Detected macOS - installing tesseract via Homebrew"
        brew install tesseract
    else
        echo "⚠️  Homebrew not found. Please install Homebrew first or install tesseract manually."
    fi
else
    echo "⚠️  Unsupported OS. Please install tesseract manually:"
    echo "   - Windows: https://github.com/UB-Mannheim/tesseract/wiki"
    echo "   - Other: Check tesseract documentation"
fi

# Install Python packages
echo ""
echo "🐍 Installing Python dependencies..."

# Core OCR packages
echo "Installing core OCR packages..."
pip3 install opencv-python==4.8.1.78
pip3 install pytesseract==0.3.10
pip3 install easyocr==1.7.0
pip3 install Pillow==10.0.1
pip3 install numpy==1.24.3

# Additional utilities
echo "Installing additional utilities..."
pip3 install pandas==2.1.3
pip3 install requests==2.31.0

# Optional LLM packages (may take longer to install)
echo ""
read -p "🤖 Install LLM packages for advanced extraction? (y/N): " install_llm

if [[ $install_llm =~ ^[Yy]$ ]]; then
    echo "Installing LLM packages (this may take a while)..."
    pip3 install transformers==4.35.2
    pip3 install torch==2.1.1
    pip3 install huggingface-hub==0.19.4
    echo "✅ LLM packages installed"
else
    echo "⏭️  Skipping LLM packages (you can install later with: pip install transformers torch)"
fi

# Verify installation
echo ""
echo "🔍 Verifying installation..."

python3 -c "
import sys
packages = ['cv2', 'PIL', 'pytesseract', 'easyocr', 'numpy']
failed = []

for package in packages:
    try:
        __import__(package)
        print(f'✅ {package}')
    except ImportError:
        print(f'❌ {package}')
        failed.append(package)

if failed:
    print(f'\\n❌ Failed to import: {failed}')
    sys.exit(1)
else:
    print('\\n🎉 All core packages imported successfully!')
"

# Check if tesseract is accessible
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR: $(tesseract --version | head -n1)"
else
    echo "❌ Tesseract OCR not found in PATH"
fi

echo ""
echo "🎯 Installation Summary"
echo "======================"
echo "✅ Core OCR packages installed"
echo "✅ Python dependencies installed"

if [[ $install_llm =~ ^[Yy]$ ]]; then
    echo "✅ LLM packages installed"
else
    echo "⏭️  LLM packages skipped"
fi

echo ""
echo "🚀 Ready to use!"
echo "Next steps:"
echo "1. Save your invoice image as 'invoice_image.png'"
echo "2. Run: python3 test_extraction.py"
echo "3. Or run: python3 simple_invoice_extractor.py"
echo ""
echo "📚 Check INVOICE_EXTRACTOR_README.md for detailed usage instructions"