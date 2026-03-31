# auth.py
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))  # ensure int

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    if not password:
        raise ValueError("Password cannot be empty")
    password = str(password).strip()        # ensure string and strip spaces
    password = password[:72]                # truncate to 72 bytes
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    if not password or not hashed:
        return False
    password = str(password).strip()
    password = password[:72]
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    data = data.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")