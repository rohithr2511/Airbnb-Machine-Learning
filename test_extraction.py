#!/usr/bin/env python3
"""
Test script for Invoice Information Extractor
This script demonstrates the extraction capabilities using the provided invoice image.
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.append('.')

def test_simple_extractor():
    """Test the simple invoice extractor"""
    print("Testing Simple Invoice Extractor...")
    print("=" * 50)
    
    try:
        from simple_invoice_extractor import SimpleInvoiceExtractor
        
        # Initialize extractor
        extractor = SimpleInvoiceExtractor()
        
        # Test with a sample image (you need to provide the path)
        image_path = "invoice_image.png"  # Change this to your image path
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            print("Please save your invoice image as 'invoice_image.png' in the current directory")
            return False
        
        print(f"✅ Found image: {image_path}")
        
        # Extract information
        info = extractor.extract_invoice_info(image_path)
        
        # Display results
        extractor.print_results(info)
        
        # Save to JSON
        output_file = "test_extraction_results.json"
        extractor.save_to_json(info, output_file)
        
        print(f"\n✅ Test completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install opencv-python pytesseract easyocr pillow")
        return False
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return False

def test_advanced_extractor():
    """Test the advanced invoice extractor with LLM"""
    print("\nTesting Advanced Invoice Extractor (with LLM)...")
    print("=" * 50)
    
    try:
        from invoice_extractor import InvoiceExtractor
        
        # Initialize extractor without GPU for testing
        extractor = InvoiceExtractor(use_gpu=False)
        
        # Test with a sample image
        image_path = "invoice_image.png"
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return False
        
        print(f"✅ Found image: {image_path}")
        
        # Extract information
        results = extractor.extract_invoice_info(image_path)
        
        # Display results
        print("\n" + "="*60)
        print("ADVANCED EXTRACTION RESULTS")
        print("="*60)
        
        print("\nCLIENT INFORMATION:")
        client_info = results['client_info']
        print(f"  Company Name: {client_info['company_name']}")
        print(f"  Address: {client_info['address']}")
        print(f"  GSTIN: {client_info['gstin']}")
        
        print("\nRECEIVER INFORMATION:")
        receiver_info = results['receiver_info']
        print(f"  Company Name: {receiver_info['company_name']}")
        print(f"  Address: {receiver_info['address']}")
        print(f"  GSTIN: {receiver_info['gstin']}")
        print(f"  Phone: {receiver_info['phone']}")
        print(f"  Email: {receiver_info['email']}")
        
        print(f"\nOCR Confidence: {results['confidence_scores']['ocr_confidence']:.2f}")
        
        # Save results
        output_file = "advanced_extraction_results.json"
        extractor.save_results(results, output_file)
        
        print(f"\n✅ Advanced test completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("LLM libraries not available. This is optional.")
        return False
    except Exception as e:
        print(f"❌ Error during advanced extraction: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking Dependencies...")
    print("=" * 30)
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('PIL', 'Pillow'),
        ('pytesseract', 'pytesseract'),
        ('easyocr', 'easyocr'),
        ('numpy', 'numpy')
    ]
    
    optional_packages = [
        ('transformers', 'transformers'),
        ('torch', 'torch')
    ]
    
    missing_required = []
    missing_optional = []
    
    # Check required packages
    for package, pip_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} (required)")
        except ImportError:
            print(f"❌ {package} (required) - install with: pip install {pip_name}")
            missing_required.append(pip_name)
    
    # Check optional packages
    for package, pip_name in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} (optional - for LLM features)")
        except ImportError:
            print(f"⚠️  {package} (optional) - install with: pip install {pip_name}")
            missing_optional.append(pip_name)
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("Install with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("Install for LLM features: pip install " + " ".join(missing_optional))
    
    print("\n✅ All required dependencies are available!")
    return True

def create_sample_invoice_data():
    """Create sample data structure to show expected output format"""
    sample_data = {
        "client": {
            "company_name": "Sample Client Company Private Limited",
            "address": "Plot no. 123, Industrial Area, Phase 1, Sample City, State - 500001",
            "gstin": "36ABCDE1234F1Z5"
        },
        "receiver": {
            "company_name": "CHARGEHOUSE MOBILITY PRIVATE LIMITED",
            "address": "Plot no. 998/606, Phase 3, IDA Cherlapally, Hyderabad, Telangana",
            "gstin": "36ABCSS3311Z1Z5",
            "phone": "9966607317",
            "email": "info@chargehouse.com"
        }
    }
    
    # Save sample data
    with open("sample_extraction_format.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print("📄 Sample extraction format saved to: sample_extraction_format.json")

def main():
    """Main test function"""
    print("🔍 Invoice Information Extractor - Test Suite")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before running tests.")
        return
    
    print("\n")
    
    # Create sample data format
    create_sample_invoice_data()
    
    print("\n")
    
    # Test simple extractor
    simple_success = test_simple_extractor()
    
    # Test advanced extractor (optional)
    advanced_success = test_advanced_extractor()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Simple Extractor: {'✅ PASSED' if simple_success else '❌ FAILED'}")
    print(f"Advanced Extractor: {'✅ PASSED' if advanced_success else '❌ FAILED (Optional)'}")
    
    if simple_success:
        print("\n🎉 Basic extraction functionality is working!")
        print("\n📋 Next Steps:")
        print("1. Save your invoice image as 'invoice_image.png'")
        print("2. Run: python simple_invoice_extractor.py")
        print("3. Check the generated JSON output files")
    else:
        print("\n🔧 Please fix the issues above and try again.")

if __name__ == "__main__":
    main()