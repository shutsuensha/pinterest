from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with async_session_maker() as session:
        yield session