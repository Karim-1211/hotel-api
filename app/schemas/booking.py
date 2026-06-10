from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookingCreate(BaseModel):
    guest_id: int
    room_id:  int
    check_in:  date
    check_out: date


class BookingUpdate(BaseModel):
    check_in:  Optional[date] = None
    check_out: Optional[date] = None


class BookingOut(BaseModel):
    id:        int
    guest_id:  int
    room_id:   int
    check_in:  date
    check_out: date

    class Config:
        from_attributes = True