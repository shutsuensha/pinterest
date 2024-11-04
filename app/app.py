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
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/signup")
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="signup.html"
    )

@app.get("/login")
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )


@app.get("/pin/{pin_uid}")
async def pin_detail(request: Request, pin_uid: str):
    return templates.TemplateResponse(
        request=request, name="pin.html", context={'pin_uid': pin_uid}
    )


@app.get('/pin-creation-tool')
async def create_pin(request: Request):
    return templates.TemplateResponse(
        request=request, name="createPin.html"
    )


@app.get("/{username}")
async def user_detail(request: Request, username: str):
    return templates.TemplateResponse(
        request=request, name="user.html", context={'username': username}
    )