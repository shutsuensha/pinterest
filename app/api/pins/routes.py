from fastapi import APIRouter, Depends, status, UploadFile, HTTPException
from .services import PinService
from typing import Annotated
from app.database.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.users.depends import get_current_user_uid
from .schemas import PinCreateModel, PinResponseModel
from fastapi.responses import FileResponse
from pathlib import Path
import uuid



pin_router = APIRouter(prefix='/pins', tags=['pins'])
pin_service = PinService()
session_dep = Annotated[AsyncSession, Depends(get_session)]
user_dep = Annotated[str, Depends(get_current_user_uid)]


@pin_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_pin(session: session_dep, user_uid: user_dep, data_model: PinCreateModel):
    pin = await pin_service.create_pin(user_uid, data_model, session)

    return {
        "message": "Created pin",
        "pin": pin
    }


@pin_router.get('/', response_model=list[PinResponseModel])
async def get_pins(session: session_dep, page: int, limit: int):
    pins = await pin_service.get_all_pins(session, page, limit)
    return pins


@pin_router.get('/{pin_uid}', response_model=PinResponseModel)
async def get_pins(session: session_dep, pin_uid: str):
    pin = await pin_service.get_pin_by_uid(pin_uid, session)
    return pin



@pin_router.post("/upload/{pin_uid}")
async def create_upload_file(user_uid: user_dep, session: session_dep, file: UploadFile, pin_uid: str):

    pin = await pin_service.get_pin_by_uid(pin_uid, session)
    if str(pin.user_uid) != str(user_uid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='u dont have permisions'
        )
    
    if pin.media:
        old_file_path = Path(f'app/media/pins/{pin.media}')
        if old_file_path.exists():
            old_file_path.unlink()

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    new_file_path = Path(f'app/media/pins/{unique_filename}')

    contents = await file.read()

    with open(new_file_path, "wb") as f:
        f.write(contents)

    updated_pin = await pin_service.update_pin(pin, {"media": unique_filename}, session)

    return updated_pin


@pin_router.get("/files/{media}")
async def get_uploaded_file(session: session_dep, media: str):
    return FileResponse(f'app/media/pins/{media}')