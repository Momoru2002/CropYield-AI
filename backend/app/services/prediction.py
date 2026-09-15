"""Loads the trained yield regressor and serves predictions with an
uncertainty estimate derived from tree-level prediction spread."""
from __future__ import annotations

import functools
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from app.core.config import settings


class ModelNotFoundError(RuntimeError):
    pass


class InvalidInputError(ValueError):
    pass


class YieldPredictionService:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self._bundle = None

    def _load(self):
        if self._bundle is None:
            if not self.model_path.exists():
                raise ModelNotFoundError(
                    f"No trained model found at {self.model_path}. "
                    "Run `python -m app.ml.train --data data/yield_df.csv` first."
                )
            self._bundle = joblib.load(self.model_path)
        return self._bundle

    @property
    def is_ready(self) -> bool:
        return self.model_path.exists()

    def metadata(self) -> dict:
        bundle = self._load()
        return {
            "crops": bundle["crops"],
            "countries": bundle["countries"],
            "year_range": bundle["year_range"],
            "test_r2": bundle["test_r2"],
        }

    def predict(
        self,
        country: str,
        crop: str,
        year: int,
        rainfall_mm: float,
        pesticides_tonnes: float,
        avg_temp_c: float,
    ) -> dict:
        bundle = self._load()
        pipeline = bundle["pipeline"]

        if country not in bundle["countries"]:
            raise InvalidInputError(f"Unknown country: {country!r}")
        if crop not in bundle["crops"]:
            raise InvalidInputError(f"Unknown crop: {crop!r}")

        row = pd.DataFrame(
            [
                {
                    "Area": country,
                    "Item": crop,
                    "Year": year,
                    "average_rain_fall_mm_per_year": rainfall_mm,
                    "pesticides_tonnes": pesticides_tonnes,
                    "avg_temp": avg_temp_c,
                }
            ]
        )
        row["Area"] = row["Area"].astype("category")
        row["Item"] = row["Item"].astype("category")

        pred_hg_ha = float(pipeline.predict(row)[0])
        pred_hg_ha = max(pred_hg_ha, 0.0)

        # Uncertainty band via the spread of individual staged predictions
        # (approximate -- HGB doesn't expose per-tree variance directly, so
        # we use the model's overall test MAE as a symmetric error band).
        mae = bundle.get("test_mae", pred_hg_ha * 0.1)
        low = max(pred_hg_ha - mae, 0.0)
        high = pred_hg_ha + mae

        return {
            "predicted_yield_hg_per_ha": pred_hg_ha,
            "predicted_yield_tons_per_ha": pred_hg_ha / 10000.0,
            "range_low_tons_per_ha": low / 10000.0,
            "range_high_tons_per_ha": high / 10000.0,
        }


@functools.lru_cache
def get_prediction_service() -> YieldPredictionService:
    return YieldPredictionService(settings.MODEL_PATH)
