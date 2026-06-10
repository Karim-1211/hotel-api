from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.room import Room
from app.schemas.room import RoomOut
from app.core.security import get_current_user
import shutil, uuid, os

router = APIRouter(prefix="/rooms", tags=["Rooms"])
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[RoomOut])
def get_rooms(
    skip: int = 0,
    limit: int = 10,
    available: Optional[bool] = None,
    room_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    query = db.query(Room)
    if available is not None: query = query.filter(Room.is_available == available)
    if room_type is not None: query = query.filter(Room.room_type == room_type)
    if max_price is not None: query = query.filter(Room.price <= max_price)
    if min_price is not None: query = query.filter(Room.price >= min_price)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=RoomOut)
def create_room(
    room_number: int = Form(...),
    room_type: str = Form(...),
    price: float = Form(...),
    is_available: bool = Form(True),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    image_filename = None
    if image:
        ext = os.path.splitext(image.filename)[1]
        image_filename = f"{uuid.uuid4()}{ext}"
        with open(f"{UPLOAD_DIR}/{image_filename}", "wb") as f:
            shutil.copyfileobj(image.file, f)
    room = Room(room_number=room_number, room_type=room_type, price=price, is_available=is_available, image=image_filename)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/{room_id}", response_model=RoomOut)
def update_room(
    room_id: int,
    room_type: str = Form(None),
    price: float = Form(None),
    is_available: bool = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room_type is not None: room.room_type = room_type
    if price is not None: room.price = price
    if is_available is not None: room.is_available = is_available
    if image:
        ext = os.path.splitext(image.filename)[1]
        image_filename = f"{uuid.uuid4()}{ext}"
        with open(f"{UPLOAD_DIR}/{image_filename}", "wb") as f:
            shutil.copyfileobj(image.file, f)
        room.image = image_filename
    db.commit()
    db.refresh(room)
    return room

@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()
    return {"message": f"Room {room_id} deleted successfully"}
