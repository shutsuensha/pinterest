from typing import Annotated
from fastapi import Depends, Request, HTTPException
from .utils import encode_token


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="no token provided")
    return token


def get_current_user_uid(token: Annotated[str, Depends(get_token)]):
    data = encode_token(token)
    return data["user_uid"]