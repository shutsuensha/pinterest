from pydantic import BaseModel
from uuid import UUID


class TagResponseModel(BaseModel):
    uid: UUID
    name: str


class AddTagsToPin(BaseModel):
    tags: list[str]


class TagName(BaseModel):
    name: str


class PinWithTags(BaseModel):
    uid: UUID
    tags: list[TagName]