#!/usr/bin/env python3
"""
Demo script for Document Information Extractor
Shows how to use the system to extract information from purchase orders/invoices
"""

import os
import json
from document_extractor import DocumentExtractor, DocumentInfo

def demo_basic_usage():
    """Demonstrate basic usage without OpenAI API"""
    print("="*60)
    print("DEMO: Basic Usage (Rule-based extraction)")
    print("="*60)
    
    # Initialize extractor without API key (will use rule-based extraction)
    extractor = DocumentExtractor()
    
    # Example with a sample image (you'll need to provide the actual image path)
    image_path = "sample_document.jpg"  # Replace with your document image path
    
    if not os.path.exists(image_path):
        print(f"⚠️  Image file not found: {image_path}")
        print("Please provide a valid document image path")
        return
    
    try:
        # Process the document
        doc_info = extractor.process_document(image_path, "extracted_info.json")
        
        # Display results
        print_results(doc_info)
        
    except Exception as e:
        print(f"❌ Error processing document: {e}")

def demo_with_openai():
    """Demonstrate usage with OpenAI API for better extraction"""
    print("="*60)
    print("DEMO: Advanced Usage (LLM-based extraction)")
    print("="*60)
    
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️  OpenAI API key not found in environment variables")
        print("Set OPENAI_API_KEY environment variable to use LLM-based extraction")
        print("Falling back to rule-based extraction...")
        demo_basic_usage()
        return
    
    # Initialize extractor with API key
    extractor = DocumentExtractor(openai_api_key=api_key)
    
    # Example with a sample image
    image_path = "sample_document.jpg"  # Replace with your document image path
    
    if not os.path.exists(image_path):
        print(f"⚠️  Image file not found: {image_path}")
        print("Please provide a valid document image path")
        return
    
    try:
        # Process the document
        doc_info = extractor.process_document(image_path, "extracted_info_llm.json")
        
        # Display results
        print_results(doc_info)
        
    except Exception as e:
        print(f"❌ Error processing document: {e}")

def print_results(doc_info: DocumentInfo):
    """Print extracted document information in a formatted way"""
    print("\n📄 EXTRACTED DOCUMENT INFORMATION")
    print("-" * 50)
    
    print(f"📋 Document Type: {doc_info.document_type or 'Not detected'}")
    print(f"🔢 Document Number: {doc_info.document_number or 'Not detected'}")
    print(f"📅 Date: {doc_info.date or 'Not detected'}")
    
    if doc_info.client_info and doc_info.client_info.company_name:
        print(f"\n🏢 CLIENT/VENDOR INFORMATION:")
        client = doc_info.client_info
        print(f"   Company: {client.company_name}")
        if client.address:
            print(f"   Address: {client.address}")
        if client.city:
            print(f"   City: {client.city}")
        if client.state:
            print(f"   State: {client.state}")
        if client.pincode:
            print(f"   Pincode: {client.pincode}")
        if client.gstin:
            print(f"   GSTIN: {client.gstin}")
        if client.phone:
            print(f"   Phone: {client.phone}")
    
    if doc_info.receiver_info and doc_info.receiver_info.company_name:
        print(f"\n🎯 RECEIVER/BILL-TO INFORMATION:")
        receiver = doc_info.receiver_info
        print(f"   Company: {receiver.company_name}")
        if receiver.address:
            print(f"   Address: {receiver.address}")
        if receiver.city:
            print(f"   City: {receiver.city}")
        if receiver.state:
            print(f"   State: {receiver.state}")
        if receiver.pincode:
            print(f"   Pincode: {receiver.pincode}")
        if receiver.gstin:
            print(f"   GSTIN: {receiver.gstin}")
    
    if doc_info.items:
        print(f"\n📦 ITEMS/PRODUCTS:")
        for i, item in enumerate(doc_info.items, 1):
            print(f"   {i}. HSN/SAC: {item.hsn_code or 'N/A'}")
            if item.description:
                print(f"      Description: {item.description}")
            if item.quantity:
                print(f"      Quantity: {item.quantity}")
            if item.unit:
                print(f"      Unit: {item.unit}")
            if item.rate:
                print(f"      Rate: {item.rate}")
            if item.amount:
                print(f"      Amount: {item.amount}")
            print()
    
    # Financial information
    print(f"💰 FINANCIAL SUMMARY:")
    if doc_info.subtotal:
        print(f"   Subtotal: {doc_info.subtotal}")
    if doc_info.cgst:
        print(f"   CGST: {doc_info.cgst}")
    if doc_info.sgst:
        print(f"   SGST: {doc_info.sgst}")
    if doc_info.igst:
        print(f"   IGST: {doc_info.igst}")
    print(f"   Total Amount: {doc_info.total_amount or 'Not detected'}")

def demo_batch_processing():
    """Demonstrate batch processing of multiple documents"""
    print("="*60)
    print("DEMO: Batch Processing")
    print("="*60)
    
    # List of document images to process
    document_paths = [
        "document1.jpg",
        "document2.png", 
        "document3.pdf"  # Note: PDF support would need additional handling
    ]
    
    extractor = DocumentExtractor()
    results = []
    
    for i, doc_path in enumerate(document_paths, 1):
        if not os.path.exists(doc_path):
            print(f"⚠️  Document {i} not found: {doc_path}")
            continue
        
        try:
            print(f"\n📄 Processing document {i}: {doc_path}")
            doc_info = extractor.process_document(doc_path, f"result_{i}.json")
            results.append(doc_info)
            print(f"✅ Successfully processed document {i}")
            
        except Exception as e:
            print(f"❌ Error processing document {i}: {e}")
    
    print(f"\n🎉 Batch processing completed. Processed {len(results)} documents successfully.")

def create_sample_config():
    """Create a sample configuration file"""
    config = {
        "ocr_settings": {
            "tesseract_config": "--oem 3 --psm 6",
            "preprocessing": {
                "denoise": True,
                "threshold": True,
                "morphology": True
            }
        },
        "extraction_settings": {
            "use_llm": True,
            "fallback_to_rules": True,
            "confidence_threshold": 0.8
        },
        "output_settings": {
            "save_json": True,
            "save_csv": False,
            "include_confidence_scores": True
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("📝 Sample configuration file created: config.json")

def main():
    """Main demo function"""
    print("🚀 Document Information Extractor - Demo")
    print("=" * 60)
    
    print("\nThis demo shows how to extract client information, receiver information,")
    print("and item information from purchase orders/invoices using OCR and LLM models.")
    
    print("\n📋 Available demos:")
    print("1. Basic usage (rule-based extraction)")
    print("2. Advanced usage (LLM-based extraction)")
    print("3. Batch processing")
    print("4. Create sample configuration")
    
    while True:
        choice = input("\nSelect demo (1-4) or 'q' to quit: ").strip()
        
        if choice == 'q':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            demo_basic_usage()
        elif choice == '2':
            demo_with_openai()
        elif choice == '3':
            demo_batch_processing()
        elif choice == '4':
            create_sample_config()
        else:
            print("❌ Invalid choice. Please select 1-4 or 'q'.")

if __name__ == "__main__":
    main()