from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ml.reference import CROP_DISPLAY_NAMES
from app.services.prediction import InvalidInputError, ModelNotFoundError, get_prediction_service

router = APIRouter(prefix="/yield", tags=["yield"])


class PredictRequest(BaseModel):
    country: str
    crop: str
    year: int = Field(ge=1900, le=2100)
    rainfall_mm: float = Field(ge=0, le=10000, description="Average annual rainfall in mm")
    pesticides_tonnes: float = Field(ge=0, le=1_000_000)
    avg_temp_c: float = Field(ge=-30, le=50)


@router.post("/predict")
async def predict(req: PredictRequest):
    service = get_prediction_service()
    try:
        result = service.predict(
            country=req.country,
            crop=req.crop,
            year=req.year,
            rainfall_mm=req.rainfall_mm,
            pesticides_tonnes=req.pesticides_tonnes,
            avg_temp_c=req.avg_temp_c,
        )
    except ModelNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except InvalidInputError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return result


@router.get("/options")
async def options():
    service = get_prediction_service()
    if not service.is_ready:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")
    meta = service.metadata()
    return {
        "countries": meta["countries"],
        "crops": [
            {"value": c, "label": CROP_DISPLAY_NAMES.get(c, c)} for c in meta["crops"]
        ],
        "year_range": meta["year_range"],
        "model_r2": meta["test_r2"],
    }
