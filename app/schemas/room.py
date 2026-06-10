from pydantic import BaseModel
from typing import Optional


class RoomCreate(BaseModel):
    room_number:  int
    room_type:    str
    price:        float
    is_available: bool = True


class RoomUpdate(BaseModel):
    room_number:  Optional[int]   = None
    room_type:    Optional[str]   = None
    price:        Optional[float] = None
    is_available: Optional[bool]  = None


class RoomOut(BaseModel):
    id:           int
    room_number:  int
    room_type:    str
    price:        float
    is_available: bool
    image:        Optional[str] = None

    class Config:
        from_attributes = True