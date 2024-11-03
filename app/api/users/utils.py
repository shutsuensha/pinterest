from passlib.context import CryptContext
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from app.config import settings
from fastapi import HTTPException
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(secret_key=settings.JWT_SECRET)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def create_url_safe_token(data: dict):
    return serializer.dumps(data)


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token, max_age=3600) # 1 hour
        return token_data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")
    

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def encode_token(token: str):
    try:
        token_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return token_data
    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=400, detail="Invalid token")
    