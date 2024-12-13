from .db_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class PinsOrm(Base):
    __tablename__ = "pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), default=None)
    description: Mapped[str] = mapped_column(String(255), default=None)
    image: Mapped[str] = mapped_column(String(100), default=None)