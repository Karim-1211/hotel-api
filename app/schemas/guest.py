from pydantic import BaseModel
from typing import Optional


class GuestCreate(BaseModel):
    name:  str
    phone: str


class GuestUpdate(BaseModel):
    name:  Optional[str] = None
    phone: Optional[str] = None


class GuestOut(BaseModel):
    id:    int
    name:  str
    phone: str

    class Config:
        from_attributes = True