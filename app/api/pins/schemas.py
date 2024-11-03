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
    text: str
    user_uid: UUID

class PinResponseModel(BaseModel):
    uid: UUID
    title: str
    description: str
    media: str
    user: PinUserModel
    tags: list[TagName]
    comments: list[CommentText]
