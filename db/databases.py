from sqlalchemy.orm import DeclarativeBase
from .session import SessionLocal


class Base(DeclarativeBase):
    """Shared SQLAlchemy Base class for all models"""

    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
