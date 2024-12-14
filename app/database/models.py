from .db_base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String



class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
    profile_image: Mapped[str | None] = mapped_column(String(200), default=None)