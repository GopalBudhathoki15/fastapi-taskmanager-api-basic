from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # or your PostgreSQL URL

engine = create_engine(DATABASE_URL, echo=False, future=True)  # Optional

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
