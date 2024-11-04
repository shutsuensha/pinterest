from fastapi import APIRouter, status, Depends, HTTPException, Response, UploadFile
from .services import UserService
from typing import Annotated
from app.database.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import (
    UserCreateModel, 
    UserLoginModel, 
    PasswordResetRequestModel, 
    UserResponseModel, 
    UserSimpleModel, 
    UserSimpleCreateModel, UserSimpleLoginModel)
from .utils import create_access_token
from datetime import timedelta
from .depends import get_current_user_uid
from fastapi.responses import FileResponse
from pathlib import Path
import uuid



users_router = APIRouter(prefix='/users', tags=['users'])
user_service = UserService()
session_dep = Annotated[AsyncSession, Depends(get_session)]
user_dep = Annotated[str, Depends(get_current_user_uid)]



@users_router.post(
    "/signup", status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    session: session_dep,
    user_data: UserCreateModel
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='user already exists'
        )

    new_user = await user_service.create_user(user_data, session)

    user_service.send_verification(email)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user    
    }


@users_router.post(
    "/simple/signup", status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    session: session_dep,
    user_data: UserSimpleCreateModel
):
    user = await user_service.get_user_by_username(user_data.username, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='user already exists'
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@users_router.get("/verify/{token}")
async def verify_user_account(token: str, session: session_dep):

    verified_user = await user_service.verify_user(token, session)

    return {
        "message": "Account verified successfully",
        "user": verified_user    
    }


@users_router.post("/login")
async def login_users(
    login_data: UserLoginModel, 
    session: session_dep,
    response: Response
):
    email = login_data.email
    password = login_data.password

    user = await user_service.authenticate_user(session, email, password)

    access_token = create_access_token({"user_uid": str(user.uid)}, expires_delta=timedelta(days=5))
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@users_router.post("/simple/login")
async def login_users(
    login_data: UserSimpleLoginModel, 
    session: session_dep,
    response: Response
):
    username = login_data.username
    password = login_data.password

    user = await user_service.simple_authenticate_user(session, username, password)

    access_token = create_access_token({"user_uid": str(user.uid), "username": user.username}, expires_delta=timedelta(days=5))
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@users_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@users_router.get("/me", response_model=UserResponseModel)
async def get_me(user_uid: user_dep, session: session_dep):
    user = await user_service.get_user_by_uid(user_uid, session)
    return user

@users_router.get('/username/{username}', response_model=UserResponseModel)
async def get_user_by_username(session: session_dep, username: str):
    user = await user_service.get_user_by_username(username, session)
    return user

@users_router.get('/uid/{user_uid}', response_model=UserSimpleModel)
async def get_user(session: session_dep, user_uid: str):
    user = await user_service.get_user_by_uid(user_uid, session)
    return user


@users_router.post("/upload")
async def create_upload_file(user_uid: user_dep, session: session_dep, file: UploadFile):

    user = await user_service.get_user_by_uid(user_uid, session)

    if user.profile:
        old_file_path = Path(f'app/media/users/{user.profile}')
        if old_file_path.exists():
            old_file_path.unlink()

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    new_file_path = Path(f'app/media/users/{unique_filename}')

    contents = await file.read()

    with open(new_file_path, "wb") as f:
        f.write(contents)


    updated_user = await user_service.update_user(user, {"profile": unique_filename}, session)

    return updated_user


@users_router.get("/files/{profile}")
async def get_uploaded_file(session: session_dep, profile: str):
    return FileResponse(f'app/media/users/{profile}')


@users_router.post("/pasword-reset-rsequest")
async def password_reset_request(reset_data: PasswordResetRequestModel):
    email = reset_data.email
    new_password = reset_data.new_password
    confirm_new_password = reset_data.confirm_new_password

    if new_password != confirm_new_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    user_service.send_password_reset(email, new_password)

    return {
        "message": "Please check your email for instructions to reset your password",   
    }


@users_router.get("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    session: session_dep,
):
    
    updated_user = await user_service.confirm_password_reset(token, session)

    return {
        "message": "Password reset Successfully",
        "user": updated_user    
    }