from fastapi import FastAPI, Request
from app.api.users.routers import router
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")


app = FastAPI()

app.include_router(router)

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")