from fastapi import FastAPI
from app.api.users.routes import users_router
from app.api.pins.routes import pin_router
from app.api.tags.routers import tag_router
from app.api.comments.routers import comment_router

version = "v1"

description = """
A REST API for pinterest like app.

This REST API is able to:
- user registration
- user verification via email
- user authentication via JWT and Cookies
- user logout
- user reset password via email
- user avatars
- users create pins with media - images/videos
- users add tags to pin
- users get all pins
- users get detail pin and related pins by tags
- users can view profiles with pins created by user
- users can add comments to pin
- users can add image to comment
- users can reply to comments
"""

version_prefix =f"/api/{version}"

app = FastAPI(
    title="Pinterest",
    description=description,
    version=version,
    contact={
        "name": "Daniil Kupryianchyk",
        "url": "https://github.com/shutsuensha",
        "email": "dankupr21@gmail.com",
    },
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

app.include_router(pin_router, prefix=f'{version_prefix}/pins', tags=['pins'])
app.include_router(comment_router, prefix=f'{version_prefix}/comments', tags=['comments'])
app.include_router(tag_router, prefix=f'{version_prefix}/tags', tags=['tags'])
app.include_router(users_router, prefix=f'{version_prefix}/users', tags=['users'])