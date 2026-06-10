from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.base import Base

class Booking(Base):
    __tablename__ = "bookings"
    id        = Column(Integer, primary_key=True, index=True)
    guest_id  = Column(Integer, ForeignKey("guests.id"))
    room_id   = Column(Integer, ForeignKey("rooms.id"))
    check_in  = Column(Date)
    check_out = Column(Date)
    guest     = relationship("Guest", back_populates="bookings")
    room      = relationship("Room", back_populates="bookings")
    payments  = relationship("Payment", back_populates="booking")
