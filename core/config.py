from dotenv import load_dotenv
import os
from jose import jwt

load_dotenv()

SECRET_KEY: str = os.environ["SECRET_KEY"]  # raises KeyError if missing
ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)
