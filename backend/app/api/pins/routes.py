from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from .services import PinService
from app.api.dependencies import db
from .schemas import CreatePinModel, OutPinModel, FullUpdatePinModel, PartialUpdatePinModel, UploadModelPin
from app.api.utils import save_image


pin_router = APIRouter(prefix="/pins", tags=["pins"])
pin_service = PinService()


@pin_router.get("/", response_model=list[OutPinModel])
async def get_pins(db: db):
    pins = await pin_service.get_all(db)
    return pins


@pin_router.post("/", response_model=OutPinModel)
async def create_pin(db: db, model: CreatePinModel):
    pin = await pin_service.add(db, model)
    return pin


@pin_router.get("/{pin_id}", response_model=OutPinModel)
async def get_pin(db: db, pin_id: int):
    pin = await pin_service.get_by_id(db, pin_id)
    return pin


@pin_router.put("/{pin_id}", response_model=OutPinModel)
async def update_pin(db: db, pin_id: int, model: FullUpdatePinModel):
    pin = await pin_service.edit_pin(db, pin_id, model)
    return pin


@pin_router.patch("/{pin_id}", response_model=OutPinModel)
async def partial_update_pin(db: db, pin_id: int, model: PartialUpdatePinModel):
    pin = await pin_service.edit_partial_pin(db, pin_id, model)
    return pin


@pin_router.delete("/{pin_id}")
async def delete_pin(db: db, pin_id: int):
    await pin_service.delete(db, pin_id)
    return {"deleted": "ok"}


@pin_router.post("/upload/{pin_id}")
async def upload_image(db: db, pin_id: int, file: UploadFile):
    image_path = f"app/media/pins/{file.filename}"
    save_image(image_path, file.file)
    pin = await pin_service.edit_partial_pin(db, pin_id, UploadModelPin(image=image_path))
    return {"uploaded": "ok", "pin": pin}


@pin_router.get('/upload/{pin_id}')
async def get_image(db: db, pin_id: int):
    pin = await get_pin(db, pin_id)
    return FileResponse(pin.image)
