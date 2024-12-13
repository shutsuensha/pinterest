from pydantic import BaseModel


class CreatePinModel(BaseModel):
    title: str | None
    description: str | None
    image: str | None


class OutPinModel(BaseModel):
    id: int
    title: str | None
    description: str | None
    image: str | None


class FullUpdatePinModel(BaseModel):
    title: str | None
    description: str | None
    image: str | None


class PartialUpdatePinModel(BaseModel):
    title: str | None = None
    description: str | None = None
    image: str | None = None


class UploadModelPin(BaseModel):
    image: str