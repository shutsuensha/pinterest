from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import desc, select
from app.database.models import Tag
from .schemas import AddTagsToPin
from app.api.pins.services import PinService
from fastapi import status, HTTPException

pin_service = PinService()

class TagService:
    async def get_tags(self, session: AsyncSession):
        statement = select(Tag).order_by(desc(Tag.created_at))

        result = await session.exec(statement)

        return result.all()
    
    async def add_tags_to_pin(self, pin_uid: str, tags_data: AddTagsToPin, session: AsyncSession):
        pin = await pin_service.get_pin_by_uid(pin_uid, session)

        if not pin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='pin not found'
            )
    
        for tag_item in tags_data.tags:
            result = await session.exec(
                select(Tag).where(Tag.name == tag_item)
            )

            tag = result.one_or_none()
            if not tag:
                tag = Tag(name=tag_item)

            if tag not in pin.tags:
                pin.tags.append(tag)
            
        await session.commit()
        
        return pin
    
    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        statement = select(Tag).where(Tag.uid == tag_uid)

        result = await session.exec(statement)

        tag = result.first()

        return tag