from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

url = "sqlite:///./taskmanager.db"

engine = create_engine(url, connect_args={"check_same_thread": False}, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
