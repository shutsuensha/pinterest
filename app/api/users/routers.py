from fastapi import APIRouter, Depends, status, HTTPException, Response, Request, UploadFile
from typing import Annotated
from app.database.db_base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from .schemas import UserIn, UserOut
from app.database.models import UsersOrm
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone, date
from app.config import settings
import jwt
import shutil
from fastapi.responses import FileResponse


db = Annotated[AsyncSession, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def encode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(status_code=401, detail="wrong token or token expired")


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="not auth token")
    return token


def get_current_user_id(token: Annotated[str, Depends(get_token)]):
    data = encode_token(token)
    if datetime.now() > datetime.fromtimestamp(data["exp"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!")
    return data["user_id"]


user_id = Annotated[int, Depends(get_current_user_id)]


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserIn, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    user = await db.scalar(
        insert(UsersOrm)
        .values(username=user_in.username, hashed_password=hash_password(user_in.password))
        .returning(UsersOrm)
    )
    await db.commit()
    return user


@router.post("/login")
async def login_user(user_in: UserIn, response: Response, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.username == user_in.username))
    if not user:
        raise HTTPException(status_code=401, detail="invalid username")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="invalid password")
    access_token = create_access_token({"user_id": user.id, "username": user.username})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me", response_model=UserOut)
async def get_me(user_id: user_id, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.post("/upload/{user_id}")
async def upload_image(file: UploadFile, user_id: int, db: db):
    image_path = f"app/media/users/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    user = await db.scalar(
        update(UsersOrm)
        .where(UsersOrm.id == user_id)
        .values(profile_image=image_path)
        .returning(UsersOrm)
    )
    
    await db.commit()

    return {"status": "ok"}


@router.get("/upload/{user_id}")
async def get_image(user_id: int, db: db):
    user = await db.scalar(select(UsersOrm).where(UsersOrm.id == user_id))
    return FileResponse(user.profile_image)