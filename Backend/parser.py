import pytesseract
import re
import cv2
import fitz  # PyMuPDF for PDF

# Set the tesseract command path manually (for Windows support)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === OCR Functions ===

# Extract text from image using Tesseract
def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_string(image_rgb)

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from .txt file
def extract_text_from_txt(txt_path: str) -> str:
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

# === Rule-Based Parsing Logic ===

def parse_receipt(text: str) -> dict:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    vendor = None
    date = None
    amount = None
    payment_mode = None
    category = None

    # Rule 1: Vendor Extraction
    for line in lines[:7]:
        if line.isupper() and not re.search(r'RECEIPT|INVOICE|BILL|STATEMENT', line):
            vendor = line
            break
    if not vendor:
        # Fallback to first non-empty line
        vendor = next((line for line in lines if line.strip()), "Unknown Vendor")

    # Rule 2: Date Extraction
    date_regex = r"(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4})"
    for line in lines:
        if re.search(r'date|bill date|invoice date|due date|statement date|dated', line, re.I):
            m = re.search(date_regex, line)
            if m:
                date = m.group()
                break
    if not date:
        # Generic date fallback
        for line in lines:
            m = re.search(date_regex, line)
            if m:
                date = m.group()
                break
    if not date:
        date = "Unknown"

    # Rule 3: Amount Extraction
    for line in reversed(lines):
        if re.search(r'total|grand total|amount due|final price|paid amount|balance', line, re.I):
            m = re.search(r'(₹|Rs\.|\$|PHP|€)?\s*([\d,]+(?:\.\d{1,2})?)', line)
            if m:
                amount = m.group().replace(' ', '').replace(',', '')
                break
    if not amount:
        amount = "0.0"

    # Rule 4: Payment Method (optional if available)
    for line in lines:
        if re.search(r'payment mode|paid by|method', line, re.I):
            payment_mode = line.split(':', 1)[-1].strip()
            break

    # Rule 5: Category Inference from Vendor Name
    category_map = {
        "utility": "Utilities", "electric": "Utilities", "gas": "Gas",
        "internet": "Internet", "restaurant": "Dining", "retail": "Shopping",
        "bank": "Financial", "salon": "Personal Care", "gym": "Fitness",
        "grocery": "Groceries", "insurance": "Insurance", "mobile": "Telecom"
    }
    for keyword, cat in category_map.items():
        if vendor and keyword in vendor.lower():
            category = cat
            break

    return {
        "vendor": vendor or "Unknown",
        "date": date,
        "amount": amount,
        "payment_mode": payment_mode,
        "category": category
    }
