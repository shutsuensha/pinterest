from fastapi import APIRouter, Depends
from typing import  Annotated
from .services import TagService
from app.database.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TagResponseModel, AddTagsToPin, PinWithTags
from app.api.pins.schemas import PinResponseModel

tag_router = APIRouter(prefix='/tags', tags=['tags'])
tag_service = TagService()
session_dep = Annotated[AsyncSession, Depends(get_session)]


@tag_router.get('/', response_model=list[TagResponseModel])
async def get_tags(session: session_dep):
    tags = await tag_service.get_tags(session)
    return tags


@tag_router.post('/{pin_uid}', response_model=PinWithTags)
async def add_tags_to_pin(session: session_dep, tags_data: AddTagsToPin, pin_uid: str):
    pin_with_tags = await tag_service.add_tags_to_pin(pin_uid, tags_data, session)

    return pin_with_tags

@tag_router.get('/{tag_uid}/pins')
async def get_tag_pins(session: session_dep, tag_uid: str):
    tag = await tag_service.get_tag_by_uid(tag_uid, session)
    return tag.pins