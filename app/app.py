from fastapi import FastAPI, Request
from app.api.users.routes import users_router
from app.api.pins.routes import pin_router
from app.api.tags.routers import tag_router
from app.api.comments.routers import comment_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(pin_router)
app.include_router(comment_router)
app.include_router(tag_router)
app.include_router(users_router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/pin/{pin_uid}")
async def read_item(request: Request, pin_uid: str):
    return templates.TemplateResponse(
        request=request, name="pin.html", context={'pin_uid': pin_uid}
    )


@app.get("/{username}")
async def read_item(request: Request, username: str):
    return templates.TemplateResponse(
        request=request, name="user.html", context={'username': username}
    )