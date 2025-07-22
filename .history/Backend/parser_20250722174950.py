import pytesseract
import re
import cv2
import os

def extract_text_from_image(image_path: str):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(image_rgb)
    return text

def parse_receipt(text: str):
    # Simple rule-based parsing using regex

    # Vendor name = first line or from known vendor list
    lines = text.splitlines()
    vendor = lines[0].strip() if lines else "Unknown Vendor"

    # Date (formats like 2023-10-21, 21/07/2025, etc.)
    date_match = re.search(r'(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})', text)
    date = date_match.group(0) if date_match else 'Unknown'

    # Amount: Last matching “Total” or ₹/$ amount
    amount_match = re.search(r'Total\s*[:\-]?\s*\$?₹?\s*(\d+[\.,]?\d*)', text, re.IGNORECASE)
    if not amount_match:
        amount_match = re.search(r'₹\s*\d+[\.,]?\d*|\$\s*\d+[\.,]?\d*', text)
    amount = float(re.sub(r'[₹$,]', '', amount_match.group(0))) if amount_match else 0.0

    return {
        "vendor": vendor,
        "date": date,
        "amount": amount
    }
