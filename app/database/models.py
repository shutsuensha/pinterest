from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import UUID, uuid4
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "user_accounts" 

    uid: UUID = Field(primary_key=True, default_factory=uuid4)

    email: str = Field(unique=True)
    password_hash: str

    username: str
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

    profile: str | None = None

    pins: list["Pin"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    comments: list["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    


class PinTag(SQLModel, table=True):
    pin_uid: UUID = Field(foreign_key="pins.uid", primary_key=True)
    tag_id: UUID = Field(foreign_key="tags.uid", primary_key=True)
    

class Pin(SQLModel , table=True):
    __tablename__ = "pins"

    uid: UUID = Field(primary_key=True, default_factory=uuid4)

    user_uid: UUID = Field(foreign_key="user_accounts.uid")

    title: str
    description: str

    media: str | None = None

    created_at: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="pins", sa_relationship_kwargs={"lazy": "selectin"})

    tags: list["Tag"] = Relationship(
        link_model=PinTag,
        back_populates="pins",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    
    comments: list["Comment"] = Relationship(
        back_populates="pin", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self) -> str:
        return f"<Pin {self.title}>"



class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: UUID = Field(primary_key=True, default_factory=uuid4)

    name: str

    created_at: datetime = Field(default_factory=datetime.now)

    pins: list["Pin"] = Relationship(
        link_model=PinTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    uid: UUID = Field(primary_key=True, default_factory=uuid4)

    text: str

    user_uid: UUID = Field(foreign_key="user_accounts.uid")
    pin_uid: UUID | None = Field(default=None, foreign_key="pins.uid")
    parent_uid: UUID | None = Field(default=None, foreign_key="comments.uid")

    media: str | None = None

    created_at: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="comments")
    pin: Pin = Relationship(back_populates="comments")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"