# Document Information Extractor

A comprehensive Python solution for extracting client information, receiver information, and item details from purchase orders, invoices, and bills using OCR (Optical Character Recognition) and LLM (Large Language Model) technologies.

## 🌟 Features

### Core Capabilities
- **OCR Text Extraction**: Advanced image preprocessing and text extraction using Tesseract OCR
- **LLM-powered Analysis**: Optional integration with OpenAI GPT models for intelligent information extraction
- **Rule-based Fallback**: Robust regex-based extraction when LLM is not available
- **Structured Output**: Well-defined data structures for all extracted information

### Information Extraction
- **Client/Vendor Information**: Company name, address, GSTIN, PAN, contact details
- **Receiver/Bill-to Information**: Complete recipient details
- **Item Details**: HSN/SAC codes, descriptions, quantities, rates, amounts
- **Financial Summary**: Subtotal, taxes (CGST, SGST, IGST), total amount
- **Document Metadata**: Type, number, date

### Document Support
- **Image Formats**: JPG, PNG, TIFF, BMP
- **Document Types**: Purchase Orders, Invoices, Bills
- **Multi-language**: Supports documents in English (extensible to other languages)

## 📋 Requirements

### System Dependencies
- Python 3.7+
- Tesseract OCR engine
- OpenCV-compatible system

### Python Dependencies
```
opencv-python==4.8.1.78
pytesseract==0.3.10
Pillow==10.0.1
numpy==1.24.3
openai==0.28.1
```

## 🚀 Installation

### 1. Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

#### MacOS
```bash
brew install tesseract
```

#### Windows
Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional: Set up OpenAI API
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Basic Command Line Usage

```bash
# Basic extraction (rule-based)
python document_extractor.py path/to/document.jpg

# With output file
python document_extractor.py path/to/document.jpg --output results.json

# With OpenAI API for better accuracy
python document_extractor.py path/to/document.jpg --api-key your-openai-key --output results.json
```

### Python API Usage

#### Simple Example
```python
from document_extractor import DocumentExtractor

# Initialize extractor
extractor = DocumentExtractor()

# Process document
doc_info = extractor.process_document("invoice.jpg", "output.json")

# Access extracted information
print(f"Company: {doc_info.client_info.company_name}")
print(f"Total Amount: {doc_info.total_amount}")
```

#### Advanced Example with OpenAI
```python
from document_extractor import DocumentExtractor

# Initialize with OpenAI API key for better accuracy
extractor = DocumentExtractor(openai_api_key="your-api-key")

# Process document with LLM-powered extraction
doc_info = extractor.process_document("purchase_order.jpg")

# Access structured data
if doc_info.client_info:
    print(f"Client: {doc_info.client_info.company_name}")
    print(f"GSTIN: {doc_info.client_info.gstin}")

if doc_info.items:
    for item in doc_info.items:
        print(f"Item: {item.description}")
        print(f"HSN: {item.hsn_code}")
        print(f"Amount: {item.amount}")
```

#### Batch Processing
```python
from document_extractor import DocumentExtractor
import os

extractor = DocumentExtractor()
documents = ["doc1.jpg", "doc2.png", "doc3.jpg"]

for i, doc_path in enumerate(documents):
    if os.path.exists(doc_path):
        doc_info = extractor.process_document(doc_path, f"result_{i}.json")
        print(f"Processed: {doc_path}")
```

## 🏗️ Data Structures

### ClientInfo
```python
@dataclass
class ClientInfo:
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
```

### ReceiverInfo
```python
@dataclass
class ReceiverInfo:
    company_name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    pincode: str = ""
    country: str = ""
    phone: str = ""
    email: str = ""
    gstin: str = ""
```

### ItemInfo
```python
@dataclass
class ItemInfo:
    hsn_code: str = ""
    description: str = ""
    quantity: str = ""
    unit: str = ""
    rate: str = ""
    amount: str = ""
```

### Complete Document Structure
```python
@dataclass
class DocumentInfo:
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
```

## 🎯 Example Output

### JSON Output Structure
```json
{
  "document_type": "Purchase Order",
  "document_number": "PO123456",
  "date": "20/06/2023",
  "client_info": {
    "company_name": "CHARGEHOUSE MOBILITY PRIVATE LIMITED",
    "address": "Plot no 99A/100, Phase 3, IDA Gadgilgoly, Hyderabad, Telangana",
    "city": "Hyderabad",
    "state": "Telangana",
    "pincode": "500032",
    "gstin": "36ABCCH1234D1Z5",
    "phone": "+91-9966667137",
    "email": "",
    "country": "India",
    "pan": ""
  },
  "receiver_info": {
    "company_name": "MAGNETICS",
    "address": "GROUND AND FIRST FLOOR, PLOT NO.250 ROAD, INDUSTRIAL AREA PHASE-II",
    "city": "",
    "state": "",
    "pincode": "",
    "gstin": "",
    "phone": "",
    "email": "",
    "country": ""
  },
  "items": [
    {
      "hsn_code": "26062025",
      "description": "Fieldstone Analyzer For L-2/4A, PFC, BLDC, HYBRID Etc motor",
      "quantity": "1",
      "unit": "nos",
      "rate": "475.00",
      "amount": "475.00"
    }
  ],
  "subtotal": "8631.00",
  "cgst": "8631.00",
  "sgst": "475.00",
  "igst": "",
  "total_amount": "17737.00"
}
```

## 🎮 Interactive Demo

Run the interactive demo to explore features:

```bash
python demo.py
```

The demo provides:
1. Basic usage demonstration
2. Advanced LLM-powered extraction
3. Batch processing example
4. Configuration file generation

## ⚙️ Configuration

### OCR Settings
- **Image Preprocessing**: Denoising, thresholding, morphological operations
- **Tesseract Configuration**: Customizable OCR engine settings
- **Character Whitelist**: Optimized for business documents

### LLM Integration
- **Model Selection**: Compatible with OpenAI GPT models
- **Fallback Strategy**: Automatic fallback to rule-based extraction
- **Prompt Engineering**: Optimized prompts for document analysis

### Output Options
- **JSON Export**: Structured data in JSON format
- **Custom Formatting**: Extensible output formatting
- **Confidence Scoring**: Optional confidence metrics

## 🔧 Customization

### Adding New Document Types
```python
# Extend the extraction rules
def extract_custom_document(self, text: str) -> DocumentInfo:
    # Custom extraction logic
    pass
```

### Custom OCR Preprocessing
```python
def custom_preprocess(self, image_path: str) -> np.ndarray:
    # Custom image preprocessing
    pass
```

### Integration with Other LLMs
```python
def extract_with_custom_llm(self, text: str) -> DocumentInfo:
    # Integration with other language models
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract not found**
   ```bash
   # Linux/Mac
   which tesseract
   
   # Windows - ensure tesseract.exe is in PATH
   ```

2. **Poor OCR quality**
   - Ensure high-resolution input images (300+ DPI)
   - Check image preprocessing settings
   - Verify document orientation

3. **OpenAI API errors**
   - Verify API key validity
   - Check rate limits and quotas
   - Ensure internet connectivity

4. **Missing dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

### Performance Optimization

1. **Image Quality**: Use high-resolution, well-lit documents
2. **Preprocessing**: Adjust preprocessing parameters for specific document types
3. **LLM Usage**: Use OpenAI API for complex documents, rule-based for simple ones
4. **Batch Processing**: Process multiple documents efficiently

## 📊 Accuracy Improvements

### Best Practices
1. **Image Quality**: Scan at 300 DPI or higher
2. **Document Orientation**: Ensure proper document alignment
3. **Lighting**: Use consistent, adequate lighting
4. **Format**: Prefer original digital documents when possible

### LLM vs Rule-based Comparison
- **LLM Approach**: Higher accuracy, better context understanding, requires API key
- **Rule-based**: Faster processing, no external dependencies, good for standard formats

## 🛡️ Security Considerations

1. **API Keys**: Store OpenAI API keys securely using environment variables
2. **Data Privacy**: Process sensitive documents locally when possible
3. **File Handling**: Validate input files and sanitize outputs
4. **Network Security**: Use HTTPS for API communications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

### Development Setup
```bash
git clone <repository>
cd document-extractor
pip install -r requirements.txt
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with:
   - Error messages
   - Sample input (sanitized)
   - Expected vs actual output
   - System information

## 🔄 Version History

- **v1.0.0**: Initial release with OCR and LLM integration
- **v1.1.0**: Added batch processing and improved accuracy
- **v1.2.0**: Enhanced rule-based extraction and configuration options

---

**Note**: This system is designed for business document processing. Ensure compliance with data privacy regulations when processing sensitive documents.