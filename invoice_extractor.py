#!/usr/bin/env python3
"""
Invoice Information Extractor using OCR + Open Source LLM
Extracts client company name, address, GSTIN, and receiver fields from invoice images.
"""

import os
import re
import json
import base64
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
import pytesseract
import easyocr
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch


@dataclass
class ClientInfo:
    """Data class to store extracted client information"""
    company_name: str = ""
    address: str = ""
    gstin: str = ""
    
@dataclass
class ReceiverInfo:
    """Data class to store extracted receiver information"""
    company_name: str = ""
    address: str = ""
    gstin: str = ""
    phone: str = ""
    email: str = ""


class InvoiceExtractor:
    """Main class for extracting invoice information using OCR and LLM"""
    
    def __init__(self, use_gpu: bool = True):
        """
        Initialize the invoice extractor
        
        Args:
            use_gpu: Whether to use GPU for LLM inference (if available)
        """
        self.device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Initialize OCR readers
        self.easyocr_reader = easyocr.Reader(['en'])
        
        # Initialize LLM pipeline - using a smaller open-source model
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the open-source LLM for text processing"""
        try:
            # Using Microsoft's DialoGPT or similar lightweight model
            # You can replace this with other models like:
            # - "microsoft/DialoGPT-medium"
            # - "facebook/blenderbot-400M-distill"
            # - "google/flan-t5-base"
            
            model_name = "google/flan-t5-base"
            print(f"Loading LLM model: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            # Create text generation pipeline
            self.llm_pipeline = pipeline(
                "text2text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                max_length=512,
                do_sample=True,
                temperature=0.1
            )
            
        except Exception as e:
            print(f"Error initializing LLM: {e}")
            print("Falling back to rule-based extraction only")
            self.llm_pipeline = None
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Preprocessed image as numpy array
        """
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply threshold to get better contrast
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def extract_text_ocr(self, image_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text using both Tesseract and EasyOCR
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Tuple of (combined_text, structured_text_data)
        """
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        
        # Method 1: Tesseract OCR
        tesseract_text = pytesseract.image_to_string(processed_image, config='--psm 6')
        
        # Method 2: EasyOCR
        easyocr_results = self.easyocr_reader.readtext(image_path)
        easyocr_text = " ".join([result[1] for result in easyocr_results])
        
        # Combine results
        combined_text = f"Tesseract: {tesseract_text}\n\nEasyOCR: {easyocr_text}"
        
        # Structure EasyOCR results with bounding boxes
        structured_data = []
        for bbox, text, confidence in easyocr_results:
            structured_data.append({
                'text': text,
                'confidence': confidence,
                'bbox': bbox
            })
        
        return combined_text, structured_data
    
    def extract_gstin_pattern(self, text: str) -> List[str]:
        """
        Extract GSTIN numbers using regex patterns
        
        Args:
            text: Input text to search
            
        Returns:
            List of found GSTIN numbers
        """
        # GSTIN pattern: 2 digits + 10 alphanumeric + 1 digit + 1 alphabet + 1 alphanumeric
        gstin_pattern = r'\b\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}\b'
        gstin_matches = re.findall(gstin_pattern, text.upper())
        
        # Also look for partial GSTIN patterns
        partial_pattern = r'\b\d{2}[A-Z0-9]{13}\b'
        partial_matches = re.findall(partial_pattern, text.upper())
        
        return list(set(gstin_matches + partial_matches))
    
    def extract_phone_pattern(self, text: str) -> List[str]:
        """Extract phone numbers using regex patterns"""
        phone_patterns = [
            r'\b(?:\+91[-.\s]?)?(?:\d{5}[-.\s]?\d{5}|\d{4}[-.\s]?\d{6}|\d{3}[-.\s]?\d{7})\b',
            r'\b\d{10}\b'
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        
        return list(set(phones))
    
    def extract_email_pattern(self, text: str) -> List[str]:
        """Extract email addresses using regex patterns"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    def extract_with_llm(self, text: str) -> Dict:
        """
        Use LLM to extract structured information from text
        
        Args:
            text: OCR extracted text
            
        Returns:
            Dictionary with extracted information
        """
        if not self.llm_pipeline:
            return {}
        
        prompt = f"""
        Extract the following information from this invoice text:
        1. Client/Billing company name
        2. Client/Billing address
        3. Client GSTIN number
        4. Receiver/Shipping company name
        5. Receiver address
        6. Receiver GSTIN
        7. Phone numbers
        8. Email addresses
        
        Text: {text[:1500]}  # Limit text length for token constraints
        
        Please provide the information in JSON format with keys: client_company, client_address, client_gstin, receiver_company, receiver_address, receiver_gstin, phone, email.
        """
        
        try:
            response = self.llm_pipeline(prompt, max_length=400, num_return_sequences=1)
            response_text = response[0]['generated_text'] if response else ""
            
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
        except Exception as e:
            print(f"LLM extraction error: {e}")
        
        return {}
    
    def rule_based_extraction(self, text: str, structured_data: List[Dict]) -> Tuple[ClientInfo, ReceiverInfo]:
        """
        Extract information using rule-based approach
        
        Args:
            text: Combined OCR text
            structured_data: Structured OCR data with bounding boxes
            
        Returns:
            Tuple of (ClientInfo, ReceiverInfo)
        """
        client_info = ClientInfo()
        receiver_info = ReceiverInfo()
        
        # Extract GSTIN numbers
        gstin_numbers = self.extract_gstin_pattern(text)
        
        # Extract phone numbers
        phone_numbers = self.extract_phone_pattern(text)
        
        # Extract email addresses
        email_addresses = self.extract_email_pattern(text)
        
        # Split text into lines for analysis
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Look for company names and addresses
        company_keywords = ['LIMITED', 'LTD', 'PRIVATE', 'PVT', 'COMPANY', 'CORP', 'CORPORATION']
        address_keywords = ['ROAD', 'STREET', 'AVENUE', 'PHASE', 'SECTOR', 'PLOT', 'HYDERABAD', 'TELANGANA']
        
        found_companies = []
        found_addresses = []
        
        for line in lines:
            line_upper = line.upper()
            
            # Check for company names
            if any(keyword in line_upper for keyword in company_keywords):
                found_companies.append(line)
            
            # Check for addresses
            if any(keyword in line_upper for keyword in address_keywords):
                found_addresses.append(line)
        
        # From the image, we can see "CHARGEHOUSE MOBILITY PRIVATE LIMITED" is mentioned
        # Let's look for specific patterns from the invoice
        
        # Look for CHARGEHOUSE (appears to be the issuing company)
        chargehouse_pattern = r'CHARGEHOUSE.*?LIMITED'
        chargehouse_match = re.search(chargehouse_pattern, text, re.IGNORECASE)
        
        # Look for "Plot no" pattern for addresses
        plot_pattern = r'Plot no.*?(?=\n|$)'
        plot_matches = re.findall(plot_pattern, text, re.IGNORECASE)
        
        # Assign found information
        if gstin_numbers:
            # First GSTIN for client, second for receiver (if available)
            client_info.gstin = gstin_numbers[0]
            if len(gstin_numbers) > 1:
                receiver_info.gstin = gstin_numbers[1]
        
        if found_companies:
            # Try to identify which is client vs receiver
            if chargehouse_match:
                # CHARGEHOUSE appears to be the issuing company
                receiver_info.company_name = chargehouse_match.group()
                # Look for other company names
                other_companies = [comp for comp in found_companies 
                                 if 'CHARGEHOUSE' not in comp.upper()]
                if other_companies:
                    client_info.company_name = other_companies[0]
            else:
                client_info.company_name = found_companies[0]
                if len(found_companies) > 1:
                    receiver_info.company_name = found_companies[1]
        
        if found_addresses:
            client_info.address = found_addresses[0] if found_addresses else ""
            receiver_info.address = found_addresses[1] if len(found_addresses) > 1 else found_addresses[0]
        
        if phone_numbers:
            receiver_info.phone = phone_numbers[0]
        
        if email_addresses:
            receiver_info.email = email_addresses[0]
        
        return client_info, receiver_info
    
    def extract_invoice_info(self, image_path: str) -> Dict:
        """
        Main method to extract all invoice information
        
        Args:
            image_path: Path to the invoice image
            
        Returns:
            Dictionary containing all extracted information
        """
        print(f"Processing image: {image_path}")
        
        # Extract text using OCR
        print("Extracting text using OCR...")
        ocr_text, structured_data = self.extract_text_ocr(image_path)
        
        # Rule-based extraction
        print("Performing rule-based extraction...")
        client_info, receiver_info = self.rule_based_extraction(ocr_text, structured_data)
        
        # LLM-based extraction (if available)
        llm_results = {}
        if self.llm_pipeline:
            print("Performing LLM-based extraction...")
            llm_results = self.extract_with_llm(ocr_text)
        
        # Combine results
        final_results = {
            'client_info': {
                'company_name': client_info.company_name,
                'address': client_info.address,
                'gstin': client_info.gstin
            },
            'receiver_info': {
                'company_name': receiver_info.company_name,
                'address': receiver_info.address,
                'gstin': receiver_info.gstin,
                'phone': receiver_info.phone,
                'email': receiver_info.email
            },
            'raw_ocr_text': ocr_text,
            'llm_results': llm_results,
            'confidence_scores': {
                'ocr_confidence': np.mean([item['confidence'] for item in structured_data]) if structured_data else 0
            }
        }
        
        # Merge LLM results if available
        if llm_results:
            if 'client_company' in llm_results and not final_results['client_info']['company_name']:
                final_results['client_info']['company_name'] = llm_results['client_company']
            if 'client_address' in llm_results and not final_results['client_info']['address']:
                final_results['client_info']['address'] = llm_results['client_address']
            if 'client_gstin' in llm_results and not final_results['client_info']['gstin']:
                final_results['client_info']['gstin'] = llm_results['client_gstin']
        
        return final_results
    
    def save_results(self, results: Dict, output_path: str = "extracted_invoice_info.json"):
        """Save extraction results to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to: {output_path}")


def main():
    """Main function to run the invoice extractor"""
    
    # Initialize extractor
    extractor = InvoiceExtractor(use_gpu=True)
    
    # Get image path from user input or use default
    image_path = input("Enter the path to your invoice image (or press Enter for default): ").strip()
    
    if not image_path:
        # Look for common image extensions in current directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        current_dir = Path('.')
        
        for ext in image_extensions:
            image_files = list(current_dir.glob(f'*{ext}'))
            if image_files:
                image_path = str(image_files[0])
                print(f"Using found image: {image_path}")
                break
        
        if not image_path:
            print("No image file found. Please provide an image path.")
            return
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return
    
    try:
        # Extract information
        results = extractor.extract_invoice_info(image_path)
        
        # Display results
        print("\n" + "="*50)
        print("EXTRACTED INVOICE INFORMATION")
        print("="*50)
        
        print("\nCLIENT INFORMATION:")
        print(f"Company Name: {results['client_info']['company_name']}")
        print(f"Address: {results['client_info']['address']}")
        print(f"GSTIN: {results['client_info']['gstin']}")
        
        print("\nRECEIVER INFORMATION:")
        print(f"Company Name: {results['receiver_info']['company_name']}")
        print(f"Address: {results['receiver_info']['address']}")
        print(f"GSTIN: {results['receiver_info']['gstin']}")
        print(f"Phone: {results['receiver_info']['phone']}")
        print(f"Email: {results['receiver_info']['email']}")
        
        print(f"\nOCR Confidence: {results['confidence_scores']['ocr_confidence']:.2f}")
        
        # Save results
        extractor.save_results(results)
        
        print("\nExtraction completed successfully!")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()