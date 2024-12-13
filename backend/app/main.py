from fastapi import FastAPI
from app.api.pins.routes import pin_router


app = FastAPI()

app.include_router(pin_router)