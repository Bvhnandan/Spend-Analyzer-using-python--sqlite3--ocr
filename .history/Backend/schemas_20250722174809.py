from pydantic import BaseModel
from typing import Optional

class ReceiptData(BaseModel):
    vendor: str
    date: str
    amount: float
    category: Optional[str] = None