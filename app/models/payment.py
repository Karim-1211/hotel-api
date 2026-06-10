from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id         = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    amount     = Column(Float, nullable=False)
    method     = Column(String, nullable=False)
    status     = Column(String, default="paid")
    paid_at    = Column(DateTime, default=datetime.utcnow)
    booking    = relationship("Booking", back_populates="payments")
