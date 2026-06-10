from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    method: str  # cash, card, online

class PaymentOut(BaseModel):
    id: int
    booking_id: int
    amount: float
    method: str
    status: str
    paid_at: datetime

    class Config:
        from_attributes = True
