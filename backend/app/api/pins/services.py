from app.api.dependencies import db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.database.models import PinsOrm
from .schemas import CreatePinModel, FullUpdatePinModel, PartialUpdatePinModel


class PinService():
    async def get_all(self, db: AsyncSession):
        pins = await db.scalars(select(PinsOrm))
        return pins
    

    async def add(self, db: AsyncSession, model: CreatePinModel):
        pin = await db.scalar(
            insert(PinsOrm).values(**model.model_dump()).returning(PinsOrm)
        )
        await db.commit()
        return pin
    

    async def get_by_id(self, db: AsyncSession, id: int):
        pin = await db.scalar(select(PinsOrm).where(PinsOrm.id == id))
        return pin
    

    async def edit_pin(self, db: AsyncSession, id: int, model: FullUpdatePinModel):
        pin = await db.scalar(
            update(PinsOrm)
            .where(PinsOrm.id == id)
            .values(**model.model_dump())
            .returning(PinsOrm)
        )
        await db.commit()
        return pin
    

    async def edit_partial_pin(self, db: AsyncSession, id: int, model: PartialUpdatePinModel):
        pin = await db.scalar(
            update(PinsOrm)
            .where(PinsOrm.id == id)
            .values(**model.model_dump(exclude_unset=True))
            .returning(PinsOrm)
        )
        await db.commit()
        return pin
    

    async def delete(self, db: AsyncSession, id: int):
        await db.execute(delete(PinsOrm).where(PinsOrm.id == id))
        await db.commit()