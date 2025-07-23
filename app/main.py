# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import STATIC_DIR
from app.api.routes import router

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
