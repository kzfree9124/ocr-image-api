from fastapi import FastAPI
from app.api.ocr import router as ocr_router

app = FastAPI()
app.include_router(ocr_router)