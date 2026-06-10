from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base

class Room(Base):
    __tablename__ = "rooms"
    id           = Column(Integer, primary_key=True, index=True)
    room_number  = Column(Integer, unique=True, nullable=False)
    room_type    = Column(String, nullable=False)
    price        = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    image        = Column(String, nullable=True)
    bookings     = relationship("Booking", back_populates="room")
