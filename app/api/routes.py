# app/api/routes.py

from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import TEMPLATE_DIR
from app.services.generate_service import process_generate

templates = Jinja2Templates(directory=TEMPLATE_DIR)
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate")
async def generate(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...),
    image3: UploadFile = File(...),
    input_mode: str = Form(...),
    clothes_type1: str = Form(...),
    clothes_type2: str = Form(...),
    gender: str = Form(...),
    body_type: str = Form(...)
):
    return await process_generate(image1, image2, image3, input_mode, clothes_type1, clothes_type2, gender, body_type)
