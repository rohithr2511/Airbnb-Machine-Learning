#!/usr/bin/env python3
"""
Invoice Extraction System - Usage Guide
Shows how to use the invoice extraction system in different ways.
"""

import os
import sys

def show_usage():
    """Display usage information for the invoice extraction system"""
    
    print("🚀 Invoice Information Extractor - Usage Guide")
    print("=" * 60)
    
    print("\n📋 WHAT THIS SYSTEM DOES:")
    print("-" * 30)
    print("✅ Extracts client company name, address, and GSTIN")
    print("✅ Extracts receiver/vendor information")
    print("✅ Finds phone numbers and email addresses")
    print("✅ Supports both Tesseract and EasyOCR for text extraction")
    print("✅ Outputs structured JSON data")
    
    print("\n📁 FILES IN THIS SYSTEM:")
    print("-" * 30)
    print("📄 simple_invoice_extractor.py   - Main extraction script")
    print("📄 invoice_extractor.py          - Advanced version with LLM")
    print("📄 demo_extraction.py            - Demonstration script")
    print("📄 test_extraction.py            - Test suite")
    print("📄 requirements.txt              - Python dependencies")
    print("📄 install.sh                    - Installation script")
    print("📄 INVOICE_EXTRACTOR_README.md   - Detailed documentation")
    
    print("\n🔧 INSTALLATION:")
    print("-" * 30)
    print("1. Run the installation script:")
    print("   chmod +x install.sh")
    print("   ./install.sh")
    print("\n2. Or install manually:")
    print("   python3 -m venv invoice_env")
    print("   source invoice_env/bin/activate")
    print("   pip install -r requirements.txt")
    
    print("\n📝 USAGE METHODS:")
    print("-" * 30)
    
    print("\n1️⃣  Command Line (Simple):")
    print("   # Save your invoice image as 'invoice_image.png'")
    print("   python3 simple_invoice_extractor.py")
    
    print("\n2️⃣  Python Script Usage:")
    print("   ```python")
    print("   from simple_invoice_extractor import SimpleInvoiceExtractor")
    print("   ")
    print("   # Initialize extractor")
    print("   extractor = SimpleInvoiceExtractor()")
    print("   ")
    print("   # Extract from image")
    print("   result = extractor.extract_invoice_info('your_image.png')")
    print("   ")
    print("   # Display results")
    print("   extractor.print_results(result)")
    print("   ")
    print("   # Save to JSON")
    print("   extractor.save_to_json(result, 'output.json')")
    print("   ```")
    
    print("\n3️⃣  Test with Demo:")
    print("   python3 demo_extraction.py")
    
    print("\n4️⃣  Run Full Test Suite:")
    print("   python3 test_extraction.py")
    
    print("\n📊 EXPECTED OUTPUT FORMAT:")
    print("-" * 30)
    print("   {")
    print('     "client": {')
    print('       "company_name": "ABC TECHNOLOGIES PVT LTD",')
    print('       "address": "123 Tech Park, Bangalore",')
    print('       "gstin": "29ABCDE1234F1Z5"')
    print("     },")
    print('     "receiver": {')
    print('       "company_name": "XYZ SOLUTIONS PVT LTD",')
    print('       "address": "456 Business Center, Gurgaon",')
    print('       "gstin": "27XYZAB5678C1D9",')
    print('       "phone": "+91-124-9876543",')
    print('       "email": "billing@xyzsolutions.com"')
    print("     }")
    print("   }")
    
    print("\n🔍 SUPPORTED IMAGE FORMATS:")
    print("-" * 30)
    print("✅ PNG (.png)")
    print("✅ JPEG (.jpg, .jpeg)")
    print("✅ BMP (.bmp)")
    print("✅ TIFF (.tiff, .tif)")
    
    print("\n⚙️  SYSTEM REQUIREMENTS:")
    print("-" * 30)
    print("✅ Python 3.8+")
    print("✅ Tesseract OCR engine")
    print("✅ OpenCV")
    print("✅ EasyOCR")
    print("✅ PIL/Pillow")
    
    print("\n🚨 TROUBLESHOOTING:")
    print("-" * 30)
    print("❌ 'Image not found' → Check image path and format")
    print("❌ 'OCR libraries not installed' → Run: pip install opencv-python pytesseract easyocr pillow")
    print("❌ 'Tesseract not found' → Install: sudo apt install tesseract-ocr")
    print("❌ Poor extraction quality → Try image preprocessing or different OCR engine")
    
    print("\n📞 PATTERN RECOGNITION:")
    print("-" * 30)
    print("🔸 GSTIN: 15-digit alphanumeric (e.g., 29ABCDE1234F1Z5)")
    print("🔸 Phone: 10-digit numbers, with/without country code")
    print("🔸 Email: Standard email format (name@domain.com)")
    print("🔸 Company: Lines after 'FROM:' or 'TO:' sections")
    
    print("\n🎯 TIPS FOR BEST RESULTS:")
    print("-" * 30)
    print("• Use high-resolution, clear images")
    print("• Ensure good contrast and lighting")
    print("• Avoid skewed or rotated images")
    print("• Clean images work better than scanned copies")
    print("• Standard invoice formats yield better results")
    
    print("\n" + "=" * 60)
    print("✨ Ready to extract invoice information!")
    print("Start with: python3 demo_extraction.py")

def main():
    """Main function"""
    show_usage()

if __name__ == "__main__":
    main()