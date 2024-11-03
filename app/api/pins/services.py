from .schemas import PinCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import Pin
from sqlmodel import select, desc

class PinService:
    async def create_pin(self, user_uid: str, data_model: PinCreateModel, session: AsyncSession):
        pin_data_dict = data_model.model_dump()

        new_pin = Pin(**pin_data_dict)
        new_pin.user_uid = user_uid

        session.add(new_pin)

        await session.commit()

        return new_pin
    

    async def get_pin_by_uid(self, pin_uid: str, session: AsyncSession):
        statement = select(Pin).where(Pin.uid == pin_uid)

        result = await session.exec(statement)

        pin = result.first()

        return pin
    

    async def update_pin(self, pin: Pin , pin_data: dict, session: AsyncSession):

        for k, v in pin_data.items():
            setattr(pin, k, v)

        await session.commit()

        return pin
    

    async def get_all_pins(self, session: AsyncSession):
        statement = select(Pin).order_by(desc(Pin.created_at))

        result = await session.exec(statement)

        return result.all()
    