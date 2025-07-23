from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.main import templates
from app.utils.helper import get_random_seed

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index():
    return templates.TemplateResponse("index.html")
