from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.booking import Booking
from app.models.room import Room
from app.models.guest import Guest
from app.schemas.booking import BookingCreate, BookingUpdate, BookingOut
from app.core.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not db.query(Guest).filter(Guest.id == data.guest_id).first():
        raise HTTPException(status_code=404, detail="Guest not found")
    if not db.query(Room).filter(Room.id == data.room_id).first():
        raise HTTPException(status_code=404, detail="Room not found")
    existing = db.query(Booking).filter(
        Booking.room_id  == data.room_id,
        Booking.check_out >= data.check_in,
        Booking.check_in  <= data.check_out
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Room already booked for these dates")
    booking = Booking(guest_id=data.guest_id, room_id=data.room_id, check_in=data.check_in, check_out=data.check_out)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/", response_model=list[BookingOut])
def get_bookings(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Booking).all()

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if data.check_in is not None: booking.check_in = data.check_in
    if data.check_out is not None: booking.check_out = data.check_out
    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message": f"Booking {booking_id} deleted successfully"}
