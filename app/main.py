from fastapi import FastAPI
from app.api.users.routers import router

app = FastAPI()

app.include_router(router)