from pydantic import BaseModel
from uuid import UUID


class PinCreateModel(BaseModel):
    title: str
    description: str

class PinUserModel(BaseModel):
    uid: UUID
    username: str
    profile: str
    

class TagName(BaseModel):
    uid: UUID
    name: str

class CommentText(BaseModel):
    uid: UUID
    text: str
    user_uid: UUID
    media: str | None = None

class PinResponseModel(BaseModel):
    uid: UUID
    title: str
    description: str
    media: str | None = None
    user: PinUserModel
    tags: list[TagName]
    comments: list[CommentText]
