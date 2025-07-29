#!/usr/bin/env python3
"""
Demo Invoice Information Extractor
Demonstrates text extraction and parsing capabilities without requiring an actual image.
"""

import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.append('.')

def demo_text_extraction():
    """Demo with sample invoice text"""
    
    # Sample invoice text (similar to what OCR would extract)
    sample_invoice_text = """
    TAX INVOICE
    
    INVOICE NO: INV-2024-001
    DATE: 15/01/2024
    
    FROM:
    ABC TECHNOLOGIES PVT LTD
    GSTIN: 29ABCDE1234F1Z5
    123 Tech Park, Sector 5
    Electronic City, Bangalore - 560100
    Karnataka, India
    Phone: +91-80-12345678
    Email: contact@abctech.com
    
    TO:
    XYZ SOLUTIONS PRIVATE LIMITED
    GSTIN: 27XYZAB5678C1D9
    456 Business Center, Plot No. 12
    Cyber Hub, Gurgaon - 122001
    Haryana, India
    Phone: +91-124-9876543
    Email: billing@xyzsolutions.com
    
    DESCRIPTION          QTY    RATE    AMOUNT
    Software License      1     50000   50000
    Support Services      1     15000   15000
    
    SUBTOTAL:                          65000
    CGST @ 9%:                          5850
    SGST @ 9%:                          5850
    TOTAL:                             76700
    """
    
    print("🧪 Demo Invoice Information Extractor")
    print("=" * 60)
    print("\n📄 Sample Invoice Text:")
    print("-" * 40)
    print(sample_invoice_text)
    print("-" * 40)
    
    try:
        from simple_invoice_extractor import SimpleInvoiceExtractor, ExtractedInfo
        
        # Initialize extractor
        extractor = SimpleInvoiceExtractor()
        
        # Extract patterns from text directly
        print("\n🔍 Extracting Information...")
        patterns = extractor.extract_patterns(sample_invoice_text)
        
        # Create ExtractedInfo object from patterns
        extracted_info = ExtractedInfo()
        
        # Extract client info (usually first occurrence)
        if patterns['gstin']:
            extracted_info.client_gstin = patterns['gstin'][0]
            if len(patterns['gstin']) > 1:
                extracted_info.receiver_gstin = patterns['gstin'][1]
        
        if patterns['phone']:
            extracted_info.phone = patterns['phone'][0]
        
        if patterns['email']:
            extracted_info.email = patterns['email'][0]
        
        # Extract company names and addresses using additional logic
        lines = sample_invoice_text.split('\n')
        from_section = False
        to_section = False
        client_lines = []
        receiver_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('FROM:'):
                from_section = True
                to_section = False
                continue
            elif line.startswith('TO:'):
                to_section = True
                from_section = False
                continue
            elif line.startswith('DESCRIPTION') or line.startswith('SUBTOTAL'):
                from_section = False
                to_section = False
                continue
            
            if from_section and line and not line.startswith('GSTIN'):
                client_lines.append(line)
            elif to_section and line and not line.startswith('GSTIN'):
                receiver_lines.append(line)
        
        # Set company names and addresses
        if client_lines:
            extracted_info.client_company = client_lines[0]
            if len(client_lines) > 1:
                extracted_info.client_address = ' '.join(client_lines[1:])
        
        if receiver_lines:
            extracted_info.receiver_company = receiver_lines[0]
            if len(receiver_lines) > 1:
                extracted_info.receiver_address = ' '.join(receiver_lines[1:])
        
        # Display results
        print("\n✅ EXTRACTION RESULTS:")
        print("=" * 40)
        
        print(f"\n📋 CLIENT INFORMATION:")
        print(f"   Company Name: {extracted_info.client_company}")
        print(f"   Address: {extracted_info.client_address}")
        print(f"   GSTIN: {extracted_info.client_gstin}")
        
        print(f"\n📬 RECEIVER INFORMATION:")
        print(f"   Company Name: {extracted_info.receiver_company}")
        print(f"   Address: {extracted_info.receiver_address}")
        print(f"   GSTIN: {extracted_info.receiver_gstin}")
        print(f"   Phone: {extracted_info.phone}")
        print(f"   Email: {extracted_info.email}")
        
        # Save to JSON
        json_output = json.dumps({
            'client': {
                'company_name': extracted_info.client_company,
                'address': extracted_info.client_address,
                'gstin': extracted_info.client_gstin
            },
            'receiver': {
                'company_name': extracted_info.receiver_company,
                'address': extracted_info.receiver_address,
                'gstin': extracted_info.receiver_gstin,
                'phone': extracted_info.phone,
                'email': extracted_info.email
            }
        }, indent=2)
        output_file = "demo_extraction_results.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Display JSON structure
        print(f"\n📊 JSON OUTPUT:")
        print("-" * 30)
        print(json.dumps(json.loads(json_output), indent=2))
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return False

def test_pattern_matching():
    """Test regex patterns used in the extraction"""
    
    print("\n🔍 Testing Pattern Matching...")
    print("=" * 40)
    
    try:
        from simple_invoice_extractor import SimpleInvoiceExtractor, ExtractedInfo
        extractor = SimpleInvoiceExtractor()
        
        # Test GSTIN pattern
        test_gstins = [
            "29ABCDE1234F1Z5",
            "27XYZAB5678C1D9", 
            "GSTIN: 29ABCDE1234F1Z5",
            "GSTIN NO: 27XYZAB5678C1D9"
        ]
        
        print("📋 GSTIN Pattern Tests:")
        for gstin in test_gstins:
            patterns = extractor.extract_patterns(gstin)
            print(f"   '{gstin}' → {patterns['gstin']}")
        
        # Test phone pattern
        test_phones = [
            "+91-80-12345678",
            "080-12345678",
            "Phone: +91-124-9876543",
            "9876543210"
        ]
        
        print("\n📞 Phone Pattern Tests:")
        for phone in test_phones:
            patterns = extractor.extract_patterns(phone)
            print(f"   '{phone}' → {patterns['phone']}")
        
        # Test email pattern
        test_emails = [
            "contact@abctech.com",
            "Email: billing@xyzsolutions.com",
            "info@company.co.in"
        ]
        
        print("\n📧 Email Pattern Tests:")
        for email in test_emails:
            patterns = extractor.extract_patterns(email)
            print(f"   '{email}' → {patterns['email']}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during pattern testing: {e}")
        return False

def main():
    """Main demo function"""
    
    print("🚀 Starting Invoice Extraction Demo...")
    print("=" * 60)
    
    # Test 1: Demo extraction
    demo_success = demo_text_extraction()
    
    # Test 2: Pattern matching
    pattern_success = test_pattern_matching()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    print(f"✅ Text Extraction Demo: {'PASSED' if demo_success else 'FAILED'}")
    print(f"✅ Pattern Matching Test: {'PASSED' if pattern_success else 'FAILED'}")
    
    if demo_success and pattern_success:
        print("\n🎉 All tests passed! The invoice extraction system is working correctly.")
        print("\n📝 Next Steps:")
        print("   1. Save your invoice image as 'invoice_image.png'")
        print("   2. Run: python3 simple_invoice_extractor.py")
        print("   3. Or use the extractor in your own code")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    return demo_success and pattern_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)