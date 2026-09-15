import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CropYield-AI"
    MODEL_PATH: Path = Path(os.getenv("CROPYIELD_MODEL_PATH", "models/regressor.joblib"))
    CORS_ORIGINS: list = os.getenv("CROPYIELD_CORS_ORIGINS", "*").split(",")


settings = Settings()
