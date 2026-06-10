from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.session import engine
import app.models.user
import app.models.guest
import app.models.room
import app.models.booking
import app.models.payment
from app.routers import guest, room, booking, auth, payment

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hotel Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
app.include_router(auth.router)
app.include_router(guest.router)
app.include_router(room.router)
app.include_router(booking.router)
app.include_router(payment.router)
