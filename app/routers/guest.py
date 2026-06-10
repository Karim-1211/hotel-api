from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestUpdate, GuestOut
from app.core.security import get_current_user

router = APIRouter(prefix="/guests", tags=["Guests"])

@router.get("/", response_model=list[GuestOut])
def get_guests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return db.query(Guest).offset(skip).limit(limit).all()

@router.post("/", response_model=GuestOut)
def create_guest(data: GuestCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    guest = Guest(name=data.name, phone=data.phone)
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest

@router.get("/{guest_id}", response_model=GuestOut)
def get_guest(guest_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

@router.put("/{guest_id}", response_model=GuestOut)
def update_guest(guest_id: int, data: GuestUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    if data.name is not None: guest.name = data.name
    if data.phone is not None: guest.phone = data.phone
    db.commit()
    db.refresh(guest)
    return guest

@router.delete("/{guest_id}")
def delete_guest(guest_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    db.delete(guest)
    db.commit()
    return {"message": f"Guest {guest_id} deleted successfully"}
