from fastapi import APIRouter, Depends
from .services import CommentService
from typing import Annotated
from app.database.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.users.depends import get_current_user_uid
from .schemas import CommentCreateRequest


comment_router = APIRouter(prefix='/comment', tags=['comments'])
comment_service = CommentService()
session_dep = Annotated[AsyncSession, Depends(get_session)]
user_dep = Annotated[str, Depends(get_current_user_uid)]


@comment_router.post('/{pin_uid}')
async def create_comment(session: session_dep, user_uid: user_dep, pin_uid: str, comment_data: CommentCreateRequest):
    comment = await comment_service.create_comment(user_uid, pin_uid, comment_data, session)
    return comment