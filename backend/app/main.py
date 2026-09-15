from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.yield_router import router as yield_router
from app.core.config import settings
from app.services.prediction import get_prediction_service

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yield_router)


@app.get("/health")
async def health():
    service = get_prediction_service()
    return {"status": "ok", "model_loaded": service.is_ready}


@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "docs": "/docs"}
