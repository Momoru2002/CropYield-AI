# Architecture

```text
┌────────────┐      ┌────────────┐      ┌───────────────┐
│  Frontend   │─────▶│  API        │─────▶│  Model bundle  │
│  (Next.js)  │      │  (FastAPI)  │      │  (joblib)      │
└────────────┘      └────────────┘      └───────────────┘
```

- **Frontend** (`frontend/`) — Next.js form for country/crop/year plus
  rainfall, pesticide, and temperature inputs. Renders the predicted yield
  (tons/ha) and an error-band range.
- **API** (`backend/app/api/yield_router.py`) — `POST /yield/predict` and
  `GET /yield/options` (valid countries/crops/year range + model R²).
- **Service** (`backend/app/services/prediction.py`) — loads the trained
  model bundle once and turns a request into a prediction, including a
  symmetric uncertainty band derived from the model's test-set MAE.
- **Model** (`backend/app/ml/`):
  - `train.py`: trains a `HistGradientBoostingRegressor` with native
    categorical support (Area/Item) directly on `data/yield_df.csv`.
  - `reference.py`: crop display-name metadata for the UI.

## Dataset

`data/yield_df.csv` — 28,242 rows covering 101 countries and 10 crops
(1990–2013), merged from FAO (yield, pesticide use) and World Bank
(rainfall, average temperature) public data. Columns: `Area`, `Item`,
`Year`, `hg/ha_yield`, `average_rain_fall_mm_per_year`, `pesticides_tonnes`,
`avg_temp`.

## Why HistGradientBoostingRegressor?

An initial RandomForest + one-hot-encoded categoricals pipeline reached
similar accuracy but serialized to ~360MB (too large to comfortably version
in git). Switching to `HistGradientBoostingRegressor` with native
categorical-feature support removes the one-hot blowup entirely — the
trained model bundle is ~1.4MB — while keeping test R² at 0.984 (vs. 0.988
for the RandomForest version).

## Request flow

1. Frontend loads `/yield/options` on mount to populate the country/crop
   dropdowns and show the model's year range and R².
2. User fills in the form and submits.
3. Frontend `POST`s JSON to `/yield/predict`.
4. API validates the payload (pydantic), checks the country/crop against
   the model's known categories, and calls `YieldPredictionService.predict`.
5. Service builds a single-row DataFrame, runs `pipeline.predict`, converts
   hg/ha to tons/ha, and returns a prediction plus an uncertainty range.
