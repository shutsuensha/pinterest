from fastapi import APIRouter, Depends, UploadFile
from .services import CommentService
from typing import Annotated
from app.database.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.users.depends import get_current_user_uid
from .schemas import CommentCreateRequest
from pathlib import Path
import uuid
from fastapi.responses import FileResponse



comment_router = APIRouter()
comment_service = CommentService()
session_dep = Annotated[AsyncSession, Depends(get_session)]
user_dep = Annotated[str, Depends(get_current_user_uid)]


@comment_router.post('/{pin_uid}')
async def create_comment_on_pin(session: session_dep, user_uid: user_dep, pin_uid: str, comment_data: CommentCreateRequest):
    comment = await comment_service.create_comment(user_uid, pin_uid, comment_data, session)
    return comment


@comment_router.post('/reply/{comment_uid}')
async def create_comment_on_comment(session: session_dep, user_uid: user_dep, comment_uid: str, comment_data: CommentCreateRequest):
    comment = await comment_service.create_reply(comment_uid, user_uid, comment_data, session)
    return comment


@comment_router.get('/reply/{comment_uid}')
async def get_all_replies(session: session_dep, comment_uid: str):
    replies = await comment_service.get_all_replies(comment_uid, session)
    return replies


@comment_router.post("/upload/{commet_uid}")
async def create_upload_file(user_uid: user_dep, session: session_dep, file: UploadFile, commet_uid: str):

    comment = await comment_service.get_comment_by_uid(commet_uid, session)
    
    if comment.media:
        old_file_path = Path(f'app/media/comments/{comment.media}')
        if old_file_path.exists():
            old_file_path.unlink()

    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    new_file_path = Path(f'app/media/comments/{unique_filename}')

    contents = await file.read()

    with open(new_file_path, "wb") as f:
        f.write(contents)

    updated_comment = await comment_service.update_comment(comment, {"media": unique_filename}, session)

    return updated_comment


@comment_router.get("/files/{media}")
async def get_uploaded_file(session: session_dep, media: str):
    return FileResponse(f'app/media/comments/{media}')