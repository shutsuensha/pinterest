from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database.db_base import get_db

db = Annotated[AsyncSession, Depends(get_db)]