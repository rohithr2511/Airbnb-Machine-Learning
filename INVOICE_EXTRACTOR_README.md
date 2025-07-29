# Invoice Information Extractor using OCR + LLM

A comprehensive solution to extract client company details and receiver information from invoice images using OCR (Optical Character Recognition) and open-source Large Language Models.

## Features

- **Dual OCR Support**: Uses both Tesseract and EasyOCR for robust text extraction
- **Open Source LLM Integration**: Leverages models like Google's FLAN-T5 for intelligent text processing
- **Pattern Recognition**: Advanced regex patterns for extracting structured information
- **Multi-format Support**: Works with various image formats (PNG, JPG, JPEG, BMP, TIFF)
- **JSON Export**: Structured output in JSON format for easy integration

## Extracted Information

### Client Information
- Company Name
- Address
- GSTIN Number

### Receiver/Vendor Information
- Company Name
- Address
- GSTIN Number
- Phone Number
- Email Address

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR Engine**
   - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - Windows: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`

### Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Quick Start

### Using the Simple Extractor

```python
from simple_invoice_extractor import SimpleInvoiceExtractor

# Initialize extractor
extractor = SimpleInvoiceExtractor()

# Extract information from invoice
info = extractor.extract_invoice_info("path/to/your/invoice.png")

# Print results
extractor.print_results(info)

# Save to JSON
extractor.save_to_json(info, "extracted_data.json")
```

### Using the Advanced Extractor with LLM

```python
from invoice_extractor import InvoiceExtractor

# Initialize with LLM support
extractor = InvoiceExtractor(use_gpu=True)

# Extract information
results = extractor.extract_invoice_info("path/to/your/invoice.png")

# Save results
extractor.save_results(results)
```

### Command Line Usage

```bash
# Run the simple extractor
python simple_invoice_extractor.py

# Run the advanced extractor
python invoice_extractor.py
```

## Example Output

```json
{
  "client": {
    "company_name": "Client Company Private Limited",
    "address": "Plot no. 123, Phase 1, Industrial Area, Hyderabad, Telangana",
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
```

## Files Overview

- **`requirements.txt`**: Python dependencies
- **`simple_invoice_extractor.py`**: Lightweight OCR-only version
- **`invoice_extractor.py`**: Full-featured version with LLM support
- **`setup.py`**: Package installation script

## Supported Document Types

- **Purchase Orders**
- **Invoices**
- **Bills**
- **Tax Documents**
- **GST Documents**

## Architecture

### OCR Pipeline
1. **Image Preprocessing**: Denoising, thresholding, morphological operations
2. **Tesseract OCR**: Primary text extraction
3. **EasyOCR**: Secondary extraction for better accuracy
4. **Text Combination**: Merges results from both OCR engines

### Pattern Extraction
- **GSTIN Pattern**: `\d{2}[A-Z0-9]{13}` format validation
- **Phone Numbers**: Multiple patterns for Indian phone numbers
- **Email Addresses**: Standard email regex patterns
- **Company Names**: Keyword-based detection (LIMITED, PVT, etc.)
- **Addresses**: Location-based keyword detection

### LLM Enhancement (Optional)
- **Model**: Google FLAN-T5 Base (or configurable)
- **Purpose**: Intelligent field extraction and validation
- **Fallback**: Rule-based extraction if LLM unavailable

## Configuration

### OCR Settings
- **Tesseract PSM**: Page Segmentation Mode 6 (uniform text block)
- **Image Processing**: OTSU thresholding for optimal contrast
- **Language**: English (configurable)

### LLM Settings
- **Model**: `google/flan-t5-base` (lightweight, ~250MB)
- **Device**: Auto-detects CUDA/CPU
- **Max Length**: 512 tokens
- **Temperature**: 0.1 (deterministic)

## Performance Tips

1. **Image Quality**: Use high-resolution, well-lit images
2. **Document Condition**: Flat, unfolded documents work best
3. **GPU Acceleration**: Enable for LLM processing if available
4. **Batch Processing**: Process multiple invoices for efficiency

## Error Handling

- **Graceful Degradation**: Falls back to rule-based extraction if LLM fails
- **OCR Fallback**: Uses EasyOCR if Tesseract fails
- **Validation**: Checks extracted patterns for validity
- **Logging**: Comprehensive error reporting

## Customization

### Adding New Patterns

```python
# Extend the pattern extraction
def custom_pattern_extraction(self, text: str):
    # Add your custom regex patterns
    custom_pattern = r'your_regex_here'
    matches = re.findall(custom_pattern, text)
    return matches
```

### Using Different LLM Models

```python
# Initialize with different model
extractor = InvoiceExtractor()
extractor.model_name = "facebook/blenderbot-400M-distill"
extractor._initialize_llm()
```

## Troubleshooting

### Common Issues

1. **Tesseract not found**: Ensure Tesseract is installed and in PATH
2. **CUDA out of memory**: Use CPU mode or smaller LLM model
3. **Poor OCR results**: Check image quality and preprocessing
4. **Missing dependencies**: Run `pip install -r requirements.txt`

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Example Usage with the Provided Invoice

The code is specifically designed to handle the attached invoice image which contains:
- **Vendor**: CHARGEHOUSE MOBILITY PRIVATE LIMITED
- **Location**: Hyderabad, Telangana
- **Document Type**: Purchase Order Amendment/Cancellation

To process this image:

1. Save the image as `invoice_image.png`
2. Run: `python simple_invoice_extractor.py`
3. The system will extract all available company details, addresses, and GSTIN information

## License

MIT License - see LICENSE file for details

## Acknowledgments

- **Tesseract OCR**: Google's open-source OCR engine
- **EasyOCR**: JaidedAI's Python OCR library
- **Transformers**: Hugging Face's transformer library
- **OpenCV**: Computer vision preprocessing