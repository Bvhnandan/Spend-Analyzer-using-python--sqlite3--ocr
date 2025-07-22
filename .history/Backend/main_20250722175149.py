from fastapi import FastAPI, UploadFile, File, HTTPException
from schemas import ReceiptData
from parser import extract_text_from_image, parse_receipt
from utils import save_uploaded_file, UPLOAD_FOLDER
from db import insert_receipt, get_all_receipts
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to PyReceiptAnalyzer API 🎉"}

@app.post("/upload", response_model=ReceiptData)
async def upload_receipt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only image files are supported for now.")

    file_path = save_uploaded_file(file)
    text = extract_text_from_image(file_path)
    data = parse_receipt(text)

    insert_receipt(data['vendor'], data['date'], data['amount'])

    return ReceiptData(**data)

@app.get("/receipts")
def fetch_receipts():
    receipts = get_all_receipts()
    result = [
        {"id": r[0], "vendor": r[1], "date": r[2], "amount": r[3], "category": r[4]}
        for r in receipts
    ]
    return JSONResponse(content=result)
