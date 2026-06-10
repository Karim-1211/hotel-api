from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

DATABASE_URL = settings.get_db_url()

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # 🔥 IMPORTANT FIX
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()