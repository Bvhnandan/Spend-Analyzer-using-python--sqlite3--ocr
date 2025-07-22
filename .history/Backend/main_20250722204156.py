from fastapi import FastAPI, UploadFile, File, status, HTTPException
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
from analytics import spending_stats, vendor_frequency, monthly_spending
from db import conn

from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to PyReceiptAnalyzer API 🎉"}


@app.post("/upload", response_model=ReceiptData)
async def upload_receipt(file: UploadFile = File(...)):
    try:
        ext = file.filename.lower().split('.')[-1]
        file_path = save_uploaded_file(file)

        # Determine which parser to use based on file extension
        if ext in ['png', 'jpg', 'jpeg']:
            text = extract_text_from_image(file_path)
        elif ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif ext == 'txt':
            text = extract_text_from_txt(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        # Parse fields from extracted text
        data = parse_receipt(text)

        # Insert into database
        insert_receipt(data['vendor'], data['date'], data['amount'], data.get('category'))

        return ReceiptData(**data)

    except HTTPException as http_error:
        # Raise validation-related errors forward
        raise http_error

    except Exception as e:
        # Catch all other unexpected errors and respond with JSON
        print("⚠️ Server-side error:", str(e))  # Optional for your logs
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Server error: {str(e)}"}
        )


@app.get("/receipts")
def fetch_receipts():
    receipts = get_all_receipts()
    result = [
        {"id": r[0], "vendor": r[1], "date": r[2], "amount": r[3], "category": r[4]}
        for r in receipts
    ]
    return JSONResponse(content=result)

@app.get("/receipts/search")
def search_receipts(
    vendor: Optional[str] = None,
    date: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    sort_by: str = Query("date"),
    desc: bool = Query(False)
):
    return search_receipts_db(vendor, date, min_amount, max_amount, sort_by, desc)

@app.get("/analytics/spending")
def get_spending_stats():
    return spending_stats(conn)

@app.get("/analytics/vendors")
def get_vendor_frequency():
    return vendor_frequency(conn)

@app.get("/analytics/monthly")
def get_monthly_spending():
    return monthly_spending(conn)
