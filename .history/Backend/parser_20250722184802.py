import pytesseract
import re
import cv2
import fitz  # PyMuPDF for PDF


# OCR for image files
def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return pytesseract.image_to_string(image_rgb)


# Text extraction for PDF files
def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Text extraction for TXT files
def extract_text_from_txt(txt_path: str) -> str:
    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


# Rule-based parsing logic for vendor, date, amount
def parse_receipt(text: str) -> dict:
    lines = text.splitlines()
    
    # Get vendor (assume it's the first non-empty line)
    vendor = next((line.strip() for line in lines if line.strip()), "Unknown Vendor")

    # Get date (e.g., 2025-07-22 or 22/07/2025)
    date_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})', text)
    date = date_match.group(0) if date_match else 'Unknown'

    # Get amount (e.g., $123.45 or ₹123.45)
    amount_match = re.search(r'[₹$]?\s*(\d+[.,]?\d*)', text)
    amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0.0

    return {
        "vendor": vendor,
        "date": date,
        "amount": amount,
        "category": None  # You can add category detection logic later
    }
