#!/usr/bin/env python3
"""
Simplified Invoice Information Extractor using OCR
Extracts client company name, address, GSTIN, and receiver fields from invoice images.
"""

import os
import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass

try:
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
    import easyocr
    HAS_OCR = True
except ImportError:
    print("OCR libraries not installed. Please install: pip install opencv-python pytesseract easyocr pillow")
    HAS_OCR = False


@dataclass
class ExtractedInfo:
    """Data class to store all extracted information"""
    client_company: str = ""
    client_address: str = ""
    client_gstin: str = ""
    receiver_company: str = ""
    receiver_address: str = ""
    receiver_gstin: str = ""
    phone: str = ""
    email: str = ""


class SimpleInvoiceExtractor:
    """Simplified invoice extractor using OCR"""
    
    def __init__(self):
        """Initialize the extractor"""
        if HAS_OCR:
            self.easyocr_reader = easyocr.Reader(['en'])
        else:
            self.easyocr_reader = None
    
    def extract_text_simple(self, image_path: str) -> str:
        """
        Extract text using available OCR methods
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Extracted text
        """
        if not HAS_OCR:
            raise ImportError("OCR libraries not available")
        
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Try Tesseract first
        try:
            tesseract_text = pytesseract.image_to_string(thresh, config='--psm 6')
        except:
            tesseract_text = ""
        
        # Try EasyOCR
        try:
            easyocr_results = self.easyocr_reader.readtext(image_path)
            easyocr_text = " ".join([result[1] for result in easyocr_results])
        except:
            easyocr_text = ""
        
        # Combine results
        combined_text = f"{tesseract_text}\n{easyocr_text}"
        return combined_text
    
    def extract_patterns(self, text: str) -> Dict[str, List[str]]:
        """
        Extract various patterns from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with extracted patterns
        """
        patterns = {}
        
        # GSTIN pattern (15 characters: 2 digits + 10 alphanumeric + 1 digit + 1 alphabet + 1 alphanumeric)
        gstin_pattern = r'\b\d{2}[A-Z0-9]{13}\b'
        patterns['gstin'] = re.findall(gstin_pattern, text.upper())
        
        # Phone numbers
        phone_patterns = [
            r'\b\d{10}\b',
            r'\b\d{5}[-.\s]?\d{5}\b',
            r'\b\d{4}[-.\s]?\d{6}\b'
        ]
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        patterns['phone'] = list(set(phones))
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        patterns['email'] = re.findall(email_pattern, text)
        
        # Company names (lines containing company keywords)
        company_keywords = ['LIMITED', 'LTD', 'PRIVATE', 'PVT', 'COMPANY', 'CORP']
        companies = []
        for line in text.split('\n'):
            line = line.strip()
            if any(keyword in line.upper() for keyword in company_keywords):
                companies.append(line)
        patterns['companies'] = companies
        
        # Addresses (lines containing address keywords)
        address_keywords = ['PLOT', 'ROAD', 'STREET', 'PHASE', 'HYDERABAD', 'TELANGANA', 'SECTOR']
        addresses = []
        for line in text.split('\n'):
            line = line.strip()
            if any(keyword in line.upper() for keyword in address_keywords):
                addresses.append(line)
        patterns['addresses'] = addresses
        
        return patterns
    
    def extract_invoice_info(self, image_path: str) -> ExtractedInfo:
        """
        Extract invoice information from image
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            ExtractedInfo object with extracted data
        """
        print(f"Processing image: {image_path}")
        
        # Extract text
        print("Extracting text using OCR...")
        text = self.extract_text_simple(image_path)
        
        # Extract patterns
        print("Extracting patterns...")
        patterns = self.extract_patterns(text)
        
        # Create result object
        info = ExtractedInfo()
        
        # Assign GSTIN numbers
        if patterns['gstin']:
            info.client_gstin = patterns['gstin'][0]
            if len(patterns['gstin']) > 1:
                info.receiver_gstin = patterns['gstin'][1]
        
        # Assign phone numbers
        if patterns['phone']:
            info.phone = patterns['phone'][0]
        
        # Assign email addresses
        if patterns['email']:
            info.email = patterns['email'][0]
        
        # Assign company names
        if patterns['companies']:
            # Look for CHARGEHOUSE (appears to be receiver/vendor)
            chargehouse_companies = [comp for comp in patterns['companies'] 
                                   if 'CHARGEHOUSE' in comp.upper()]
            other_companies = [comp for comp in patterns['companies'] 
                             if 'CHARGEHOUSE' not in comp.upper()]
            
            if chargehouse_companies:
                info.receiver_company = chargehouse_companies[0]
            if other_companies:
                info.client_company = other_companies[0]
            
            # If we only have one company, it might be the receiver
            if not info.client_company and not info.receiver_company:
                info.receiver_company = patterns['companies'][0]
        
        # Assign addresses
        if patterns['addresses']:
            # Try to distinguish client vs receiver addresses
            info.client_address = patterns['addresses'][0]
            if len(patterns['addresses']) > 1:
                info.receiver_address = patterns['addresses'][1]
            else:
                info.receiver_address = patterns['addresses'][0]
        
        return info
    
    def print_results(self, info: ExtractedInfo):
        """Print extracted information in a formatted way"""
        print("\n" + "="*60)
        print("EXTRACTED INVOICE INFORMATION")
        print("="*60)
        
        print("\nCLIENT INFORMATION:")
        print(f"  Company Name: {info.client_company}")
        print(f"  Address: {info.client_address}")
        print(f"  GSTIN: {info.client_gstin}")
        
        print("\nRECEIVER/VENDOR INFORMATION:")
        print(f"  Company Name: {info.receiver_company}")
        print(f"  Address: {info.receiver_address}")
        print(f"  GSTIN: {info.receiver_gstin}")
        print(f"  Phone: {info.phone}")
        print(f"  Email: {info.email}")
        
        print("\n" + "="*60)
    
    def save_to_json(self, info: ExtractedInfo, output_path: str = "invoice_data.json"):
        """Save extracted information to JSON file"""
        data = {
            "client": {
                "company_name": info.client_company,
                "address": info.client_address,
                "gstin": info.client_gstin
            },
            "receiver": {
                "company_name": info.receiver_company,
                "address": info.receiver_address,
                "gstin": info.receiver_gstin,
                "phone": info.phone,
                "email": info.email
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {output_path}")


def main():
    """Main function"""
    if not HAS_OCR:
        print("Please install required dependencies:")
        print("pip install opencv-python pytesseract easyocr pillow")
        return
    
    # Initialize extractor
    extractor = SimpleInvoiceExtractor()
    
    # For the provided image, we'll save it first
    # You can modify this to use your own image path
    image_path = "invoice_image.png"  # Change this to your image path
    
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        print("Please ensure your invoice image is available at the specified path.")
        return
    
    try:
        # Extract information
        info = extractor.extract_invoice_info(image_path)
        
        # Display results
        extractor.print_results(info)
        
        # Save results
        extractor.save_to_json(info)
        
        print("\nExtraction completed successfully!")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()