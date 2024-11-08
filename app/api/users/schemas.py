from pydantic import BaseModel
from uuid import UUID

class UserCreateModel(BaseModel):
    email: str
    password: str
    username: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "dankupr21@gmail.com",
                "password": "docent1315",
                "username": "evalshine"
            }
        }
    }


class UserSimpleCreateModel(BaseModel):
    password: str
    username: str


class UserPinsModel(BaseModel):
    uid: UUID
    title: str
    description: str
    media: str


class UserResponseModel(BaseModel):
    uid: UUID
    email: str | None = None
    username: str | None = None
    profile: str | None = None
    pins: list[UserPinsModel]



class UserSimpleModel(BaseModel):
    username: str
    profile: str | None = None


class UserLoginModel(BaseModel):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "dankupr21@gmail.com",
                "password": "docent1315",
            }
        }
    }


class UserSimpleLoginModel(BaseModel):
    username: str
    password: str


class PasswordResetRequestModel(BaseModel):
    email: str
    new_password: str
    confirm_new_password: str