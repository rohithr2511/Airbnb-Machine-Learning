#!/usr/bin/env python3
"""
Installation Test Script for Document Information Extractor
Tests all dependencies and basic functionality
"""

import sys
import subprocess
import importlib
from pathlib import Path

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def test_dependencies():
    """Test Python package dependencies"""
    print("\n📦 Testing Python dependencies...")
    
    dependencies = [
        'cv2',
        'numpy', 
        'pytesseract',
        'PIL',
        'openai'
    ]
    
    all_passed = True
    
    for dep in dependencies:
        try:
            module = importlib.import_module(dep)
            print(f"✅ {dep} - OK")
            
            # Test specific functionality
            if dep == 'cv2':
                # Test OpenCV
                import cv2
                print(f"   OpenCV version: {cv2.__version__}")
            elif dep == 'numpy':
                import numpy as np
                print(f"   NumPy version: {np.__version__}")
            elif dep == 'pytesseract':
                import pytesseract
                print(f"   PyTesseract imported successfully")
            elif dep == 'PIL':
                from PIL import Image
                print(f"   PIL/Pillow imported successfully")
            elif dep == 'openai':
                import openai
                print(f"   OpenAI library imported successfully")
                
        except ImportError as e:
            print(f"❌ {dep} - MISSING: {e}")
            all_passed = False
        except Exception as e:
            print(f"⚠️  {dep} - ERROR: {e}")
            all_passed = False
    
    return all_passed

def test_tesseract():
    """Test Tesseract OCR installation"""
    print("\n🔍 Testing Tesseract OCR...")
    
    try:
        import pytesseract
        
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {version}")
        return True
        
    except pytesseract.TesseractNotFoundError:
        print("❌ Tesseract not found in PATH")
        print("   Install instructions:")
        print("   - Ubuntu/Debian: sudo apt install tesseract-ocr")
        print("   - MacOS: brew install tesseract")
        print("   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    except Exception as e:
        print(f"❌ Tesseract error: {e}")
        return False

def test_document_extractor():
    """Test document extractor import and basic functionality"""
    print("\n📄 Testing Document Extractor...")
    
    try:
        from document_extractor import DocumentExtractor, DocumentInfo
        print("✅ Document extractor imported successfully")
        
        # Test initialization
        extractor = DocumentExtractor()
        print("✅ DocumentExtractor initialized")
        
        # Test data structures
        doc_info = DocumentInfo()
        print("✅ DocumentInfo structure created")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_demo_script():
    """Test demo script availability"""
    print("\n🎮 Testing demo script...")
    
    if Path("demo.py").exists():
        print("✅ demo.py found")
        return True
    else:
        print("❌ demo.py not found")
        return False

def create_test_image():
    """Create a simple test image for OCR testing"""
    print("\n🖼️  Creating test image...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        
        # Create a simple white image with text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some test text
        test_text = """PURCHASE ORDER AMENDMENT/CANCELLATION
CHARGEHOUSE MOBILITY PRIVATE LIMITED
Plot no 99A/100, Phase 3, IDA Gadgigolly
Hyderabad, Telangana 500032
GSTIN: 36ABCCH1234D1Z5
PO: 9966667137
Date: 20/06/2023"""
        
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw text
        draw.text((10, 10), test_text, fill='black', font=font)
        
        # Save test image
        img.save('test_document.png')
        print("✅ Test image created: test_document.png")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test image: {e}")
        return False

def test_ocr_functionality():
    """Test basic OCR functionality"""
    print("\n🔍 Testing OCR functionality...")
    
    try:
        from document_extractor import DocumentExtractor
        import os
        
        if not os.path.exists('test_document.png'):
            print("⚠️  Test image not found, skipping OCR test")
            return True
        
        extractor = DocumentExtractor()
        
        # Test OCR text extraction
        text = extractor.extract_text_with_ocr('test_document.png')
        
        if text and len(text.strip()) > 0:
            print("✅ OCR text extraction successful")
            print(f"   Extracted text preview: {text[:100]}...")
            return True
        else:
            print("⚠️  OCR extracted empty text")
            return False
            
    except Exception as e:
        print(f"❌ OCR test error: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    test_files = ['test_document.png']
    
    for file in test_files:
        try:
            if Path(file).exists():
                Path(file).unlink()
                print(f"✅ Removed {file}")
        except Exception as e:
            print(f"⚠️  Could not remove {file}: {e}")

def main():
    """Run all installation tests"""
    print("🧪 Document Information Extractor - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Python Dependencies", test_dependencies),
        ("Tesseract OCR", test_tesseract),
        ("Document Extractor", test_document_extractor),
        ("Demo Script", test_demo_script),
        ("Test Image Creation", create_test_image),
        ("OCR Functionality", test_ocr_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - EXCEPTION: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Installation is successful.")
        print("\nNext steps:")
        print("1. Run 'python demo.py' to try the interactive demo")
        print("2. Process your first document with:")
        print("   python document_extractor.py your_document.jpg")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Install Tesseract OCR for your system")
        print("3. Check Python version (requires 3.7+)")
    
    # Cleanup
    cleanup_test_files()
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())