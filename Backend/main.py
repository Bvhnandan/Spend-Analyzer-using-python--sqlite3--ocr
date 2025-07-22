from fastapi import FastAPI, UploadFile, File, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import Optional

from schemas import ReceiptData
from parser import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_text_from_txt,
    parse_receipt
)
from utils import save_uploaded_file
from db import (
    insert_receipt,
    get_all_receipts,
    search_receipts_db,
    conn
)
from analytics import (
    spending_stats,
    vendor_frequency,
    monthly_spending
)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to PyReceiptAnalyzer API 🎉"}



@app.post("/upload", response_model=ReceiptData)
async def upload_receipt(file: UploadFile = File(...)):
    try:
        ext = file.filename.lower().split('.')[-1]
        file_path = save_uploaded_file(file)

        # OCR → Text Extraction
        if ext in ['png', 'jpg', 'jpeg']:
            text = extract_text_from_image(file_path)
        elif ext == 'pdf':
            text = extract_text_from_pdf(file_path)
        elif ext == 'txt':
            text = extract_text_from_txt(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format.")

        # Rule-based Parsing
        data = parse_receipt(text)

        # Insert into DB (excluding payment_mode unless table supports it)
        insert_receipt(
            data['vendor'],
            data['date'],
            data['amount'],
            data.get('category')
        )

        # Return full structured data (include payment mode in response)
        amount_str = data["amount"].replace(",", "")
        return ReceiptData(
            vendor=data["vendor"],
            date=data["date"],
            amount=float(amount_str),
            category=data.get("category"),
            payment_mode=data.get("payment_mode")  # 🎯 NEW: Include in response
        )

    except HTTPException as http_error:
        raise http_error

    except Exception as e:
        print("⚠️ Server-side error:", str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Server error: {str(e)}"}
        )


# FETCH ALL RECEIPTS 
@app.get("/receipts")
def fetch_receipts():
    receipts = get_all_receipts()
    result = [
        {
            "id": r[0],
            "vendor": r[1],
            "date": r[2],
            "amount": r[3],
            "category": r[4]
        }
        for r in receipts
    ]
    return JSONResponse(content=result)


# SEARCH / FILTER RECEIPTS 
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


# ANALYTICS: Spending Summary 
@app.get("/analytics/spending")
def get_spending_stats():
    return spending_stats(conn)


#  ANALYTICS: Vendor Frequency Chart 
@app.get("/analytics/vendors")
def get_vendor_frequency():
    return vendor_frequency(conn)


#  ANALYTICS: Monthly Spend Trends 
@app.get("/analytics/monthly")
def get_monthly_spending():
    return monthly_spending(conn)
