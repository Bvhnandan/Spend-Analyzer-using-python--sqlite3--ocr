from fastapi import FastAPI, UploadFile, File, HTTPException
from schemas import ReceiptData
from parser import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_txt,
    parse_receipt
)
from utils import save_uploaded_file, UPLOAD_FOLDER
from db import (
    insert_receipt, 
    get_all_receipts,
    search_receipts_db  # 🔥 import the new function
)
from typing import Optional
from fastapi import Query

from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to PyReceiptAnalyzer API 🎉"}


@app.post("/upload", response_model=ReceiptData)
async def upload_receipt(file: UploadFile = File(...)):
    ext = file.filename.lower().split('.')[-1]
    file_path = save_uploaded_file(file)

    # Extract and parse text based on file type
    if ext in ['png', 'jpg', 'jpeg']:
        text = extract_text_from_image(file_path)
    elif ext == 'pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == 'txt':
        text = extract_text_from_txt(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Parse data and store in database
    data = parse_receipt(text)
    insert_receipt(data['vendor'], data['date'], data['amount'], data.get('category'))

    return ReceiptData(**data)


@app.get("/receipts")
def fetch_receipts():
    receipts = get_all_receipts()
    result = [
        {"id": r[0], "vendor": r[1], "date": r[2], "amount": r[3], "category": r[4]}
        for r in receipts
    ]
    return JSONResponse(content=result)
