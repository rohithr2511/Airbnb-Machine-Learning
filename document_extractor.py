#!/usr/bin/env python3
"""
Document Information Extractor
Extracts client information, receiver information, and item information 
from purchase orders/invoices using OCR and LLM models.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import openai
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClientInfo:
    """Client/Vendor information structure"""
    company_name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    pincode: str = ""
    country: str = ""
    phone: str = ""
    email: str = ""
    gstin: str = ""
    pan: str = ""

@dataclass
class ReceiverInfo:
    """Receiver/Bill-to information structure"""
    company_name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    pincode: str = ""
    country: str = ""
    phone: str = ""
    email: str = ""
    gstin: str = ""

@dataclass
class ItemInfo:
    """Item/Product information structure"""
    hsn_code: str = ""
    description: str = ""
    quantity: str = ""
    unit: str = ""
    rate: str = ""
    amount: str = ""

@dataclass
class DocumentInfo:
    """Complete document information structure"""
    document_type: str = ""
    document_number: str = ""
    date: str = ""
    client_info: ClientInfo = None
    receiver_info: ReceiverInfo = None
    items: List[ItemInfo] = None
    subtotal: str = ""
    cgst: str = ""
    sgst: str = ""
    igst: str = ""
    total_amount: str = ""

class DocumentExtractor:
    """Main class for document information extraction"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the document extractor
        
        Args:
            openai_api_key: OpenAI API key for LLM processing
        """
        self.openai_api_key = openai_api_key
        if openai_api_key:
            openai.api_key = openai_api_key
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            
            if img is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply threshold to get binary image
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Morphological operations to remove noise
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def extract_text_with_ocr(self, image_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text as string
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Configure tesseract
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:-/()[]{}@#$%&*+=|\\~`!?;"\' '
            
            # Extract text
            text = pytesseract.image_to_string(processed_img, config=custom_config)
            
            # Clean text
            text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
            text = re.sub(r' +', ' ', text)    # Remove multiple spaces
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text with OCR: {e}")
            raise
    
    def extract_with_llm(self, ocr_text: str) -> DocumentInfo:
        """
        Extract structured information using LLM
        
        Args:
            ocr_text: Raw OCR extracted text
            
        Returns:
            Structured document information
        """
        try:
            if not self.openai_api_key:
                logger.warning("No OpenAI API key provided, using rule-based extraction")
                return self.extract_with_rules(ocr_text)
            
            prompt = f"""
            Extract the following information from this purchase order/invoice text:

            TEXT:
            {ocr_text}

            Please extract and structure the information in the following JSON format:

            {{
                "document_type": "Purchase Order" or "Invoice" or "Bill",
                "document_number": "document number",
                "date": "document date",
                "client_info": {{
                    "company_name": "client/vendor company name",
                    "address": "client address",
                    "city": "client city", 
                    "state": "client state",
                    "pincode": "client pincode",
                    "country": "client country",
                    "phone": "client phone",
                    "email": "client email",
                    "gstin": "client GSTIN",
                    "pan": "client PAN"
                }},
                "receiver_info": {{
                    "company_name": "receiver/bill-to company name",
                    "address": "receiver address",
                    "city": "receiver city",
                    "state": "receiver state", 
                    "pincode": "receiver pincode",
                    "country": "receiver country",
                    "phone": "receiver phone",
                    "email": "receiver email",
                    "gstin": "receiver GSTIN"
                }},
                "items": [
                    {{
                        "hsn_code": "HSN/SAC code",
                        "description": "item description",
                        "quantity": "quantity",
                        "unit": "unit of measurement",
                        "rate": "rate per unit",
                        "amount": "total amount for item"
                    }}
                ],
                "subtotal": "subtotal amount",
                "cgst": "CGST amount",
                "sgst": "SGST amount", 
                "igst": "IGST amount",
                "total_amount": "final total amount"
            }}

            Extract only the information that is clearly visible in the text. Use empty strings for missing information.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured information from business documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON response
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            json_str = result_text[json_start:json_end]
            
            data = json.loads(json_str)
            
            # Convert to DocumentInfo structure
            return self._dict_to_document_info(data)
            
        except Exception as e:
            logger.error(f"Error extracting with LLM: {e}")
            logger.info("Falling back to rule-based extraction")
            return self.extract_with_rules(ocr_text)
    
    def extract_with_rules(self, text: str) -> DocumentInfo:
        """
        Extract information using rule-based approach as fallback
        
        Args:
            text: Raw OCR extracted text
            
        Returns:
            Structured document information
        """
        try:
            doc_info = DocumentInfo()
            
            # Extract document type and number
            if re.search(r'purchase.*order', text, re.IGNORECASE):
                doc_info.document_type = "Purchase Order"
            elif re.search(r'invoice', text, re.IGNORECASE):
                doc_info.document_type = "Invoice"
            elif re.search(r'bill', text, re.IGNORECASE):
                doc_info.document_type = "Bill"
            
            # Extract document number
            po_match = re.search(r'(?:PO|Purchase Order|Invoice).*?[:#]?\s*([A-Z0-9]+)', text, re.IGNORECASE)
            if po_match:
                doc_info.document_number = po_match.group(1)
            
            # Extract date
            date_match = re.search(r'(?:Date|Dated)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
            if date_match:
                doc_info.date = date_match.group(1)
            
            # Extract GSTIN numbers
            gstin_pattern = r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b'
            gstin_matches = re.findall(gstin_pattern, text)
            
            # Extract company information (basic extraction)
            lines = text.split('\n')
            company_lines = []
            
            for i, line in enumerate(lines):
                if any(keyword in line.upper() for keyword in ['PRIVATE LIMITED', 'PVT LTD', 'LIMITED', 'LTD']):
                    company_lines.append((i, line.strip()))
            
            # Simple heuristic: first company is usually the client/vendor
            if company_lines:
                doc_info.client_info = ClientInfo()
                doc_info.client_info.company_name = company_lines[0][1]
                
                if gstin_matches:
                    doc_info.client_info.gstin = gstin_matches[0]
            
            # Extract items (basic pattern matching)
            doc_info.items = []
            
            # Look for HSN codes and item descriptions
            hsn_pattern = r'\b\d{4,8}\b'
            amount_pattern = r'\b\d+(?:,\d{3})*(?:\.\d{2})?\b'
            
            for line in lines:
                if re.search(hsn_pattern, line) and re.search(amount_pattern, line):
                    item = ItemInfo()
                    
                    hsn_match = re.search(hsn_pattern, line)
                    if hsn_match:
                        item.hsn_code = hsn_match.group()
                    
                    amounts = re.findall(amount_pattern, line)
                    if amounts:
                        item.amount = amounts[-1]  # Usually the last amount is the total
                    
                    item.description = line.strip()
                    doc_info.items.append(item)
            
            # Extract total amount
            total_pattern = r'(?:Total|Grand Total|Final Total)[:\s]*([0-9,]+(?:\.\d{2})?)'
            total_match = re.search(total_pattern, text, re.IGNORECASE)
            if total_match:
                doc_info.total_amount = total_match.group(1)
            
            return doc_info
            
        except Exception as e:
            logger.error(f"Error in rule-based extraction: {e}")
            return DocumentInfo()
    
    def _dict_to_document_info(self, data: Dict[str, Any]) -> DocumentInfo:
        """Convert dictionary to DocumentInfo structure"""
        try:
            doc_info = DocumentInfo()
            
            doc_info.document_type = data.get('document_type', '')
            doc_info.document_number = data.get('document_number', '')
            doc_info.date = data.get('date', '')
            doc_info.subtotal = data.get('subtotal', '')
            doc_info.cgst = data.get('cgst', '')
            doc_info.sgst = data.get('sgst', '')
            doc_info.igst = data.get('igst', '')
            doc_info.total_amount = data.get('total_amount', '')
            
            # Client info
            if 'client_info' in data:
                client_data = data['client_info']
                doc_info.client_info = ClientInfo(**client_data)
            
            # Receiver info
            if 'receiver_info' in data:
                receiver_data = data['receiver_info']
                doc_info.receiver_info = ReceiverInfo(**receiver_data)
            
            # Items
            doc_info.items = []
            if 'items' in data and isinstance(data['items'], list):
                for item_data in data['items']:
                    item = ItemInfo(**item_data)
                    doc_info.items.append(item)
            
            return doc_info
            
        except Exception as e:
            logger.error(f"Error converting dict to DocumentInfo: {e}")
            return DocumentInfo()
    
    def process_document(self, image_path: str, output_path: Optional[str] = None) -> DocumentInfo:
        """
        Main method to process a document image and extract information
        
        Args:
            image_path: Path to the document image
            output_path: Optional path to save extracted information as JSON
            
        Returns:
            Extracted document information
        """
        try:
            logger.info(f"Processing document: {image_path}")
            
            # Step 1: Extract text using OCR
            logger.info("Extracting text with OCR...")
            ocr_text = self.extract_text_with_ocr(image_path)
            
            # Step 2: Extract structured information using LLM/rules
            logger.info("Extracting structured information...")
            doc_info = self.extract_with_llm(ocr_text)
            
            # Step 3: Save results if output path provided
            if output_path:
                self.save_results(doc_info, output_path)
            
            logger.info("Document processing completed successfully")
            return doc_info
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise
    
    def save_results(self, doc_info: DocumentInfo, output_path: str):
        """Save extracted information to JSON file"""
        try:
            # Convert to dictionary
            result_dict = asdict(doc_info)
            
            # Save to JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract information from purchase orders/invoices')
    parser.add_argument('image_path', help='Path to the document image')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--api-key', help='OpenAI API key for LLM processing')
    
    args = parser.parse_args()
    
    try:
        # Initialize extractor
        extractor = DocumentExtractor(openai_api_key=args.api_key)
        
        # Process document
        doc_info = extractor.process_document(args.image_path, args.output)
        
        # Print results
        print("\n" + "="*60)
        print("EXTRACTED DOCUMENT INFORMATION")
        print("="*60)
        
        print(f"\nDocument Type: {doc_info.document_type}")
        print(f"Document Number: {doc_info.document_number}")
        print(f"Date: {doc_info.date}")
        
        if doc_info.client_info:
            print(f"\nCLIENT INFORMATION:")
            print(f"Company: {doc_info.client_info.company_name}")
            print(f"Address: {doc_info.client_info.address}")
            print(f"GSTIN: {doc_info.client_info.gstin}")
        
        if doc_info.receiver_info:
            print(f"\nRECEIVER INFORMATION:")
            print(f"Company: {doc_info.receiver_info.company_name}")
            print(f"Address: {doc_info.receiver_info.address}")
            print(f"GSTIN: {doc_info.receiver_info.gstin}")
        
        if doc_info.items:
            print(f"\nITEMS:")
            for i, item in enumerate(doc_info.items, 1):
                print(f"  {i}. HSN: {item.hsn_code}")
                print(f"     Description: {item.description}")
                print(f"     Quantity: {item.quantity}")
                print(f"     Rate: {item.rate}")
                print(f"     Amount: {item.amount}")
        
        print(f"\nTotal Amount: {doc_info.total_amount}")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())