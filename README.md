<h1 align="center">🌾 CropYield-AI</h1>

<p align="center">
  <b>Prediksi hasil panen dari data iklim & lahan</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Working%20MVP-brightgreen?style=flat-square">
  <img src="https://img.shields.io/badge/Test%20R²-0.984-1F3D2B?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.12-1F3D2B?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-Backend-1F3D2B?style=flat-square&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Next.js-Frontend-1F3D2B?style=flat-square&logo=nextdotjs&logoColor=white">
  <img src="https://img.shields.io/badge/License-MIT-1F3D2B?style=flat-square">
</p>

<br>

## About

**CropYield-AI** estimates crop yield (tons/hectare) from a handful of
inputs — country, crop, year, rainfall, pesticide use, and average
temperature — using a model trained on real historical FAO and World Bank
data. Useful for quick what-if planning: "if rainfall drops 20% this
season, what yield should I expect?"

> ✅ **Status: working end-to-end.** Fill in the form in the UI and get a
> real prediction from a model trained on 28,242 historical records across
> 101 countries and 10 crops. See [Roadmap](./docs/ROADMAP.md) for
> expanding coverage and adding proper prediction intervals.

<br>

## How it works

1. **Pick** a country, crop, and year, then enter rainfall, pesticide use,
   and average temperature.
2. The API runs the inputs through a **HistGradientBoostingRegressor**
   trained on historical FAO/World Bank data.
3. Get back a **predicted yield in tons/hectare**, plus a range reflecting
   the model's typical error margin.

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for the full request
flow and why a gradient-boosted tree model (with native categorical
support) was chosen over one-hot-encoded RandomForest.

<br>

## Model

- **Dataset:** merged FAO (yield, pesticide use) + World Bank (rainfall,
  average temperature) data, 1990–2013 — 28,242 rows, 101 countries, 10
  crops (Maize, Potatoes, Rice, Sorghum, Soybeans, Wheat, Cassava, Sweet
  Potatoes, Plantains, Yams). Source notebook/data:
  [rashisoni8642-rgb/Crop-Yield-Prediction-Using-Machine-Learning](https://github.com/rashisoni8642-rgb/Crop-Yield-Prediction-Using-Machine-Learning).
- **Model:** `HistGradientBoostingRegressor` (scikit-learn) with native
  categorical support for country/crop — no one-hot blowup.
- **Test R²:** **0.984** · **Test MAPE:** ~13%.

Retrain with more data or different hyperparameters:

```bash
cd backend
python -m app.ml.train --data data/yield_df.csv --out models/regressor.joblib
```

<br>

## Tech Stack

`FastAPI` `scikit-learn` `pandas` `Next.js` `TypeScript` `Docker` `Nginx`

<br>

## Project Structure

```text
CropYield-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # yield_router.py — FastAPI router
│   │   ├── core/         # config.py — app settings
│   │   ├── ml/            # train.py, reference.py
│   │   ├── services/     # prediction.py — inference service
│   │   └── main.py       # FastAPI app entrypoint
│   ├── data/               # yield_df.csv — training data
│   ├── models/             # trained regressor.joblib
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/                # Next.js App Router page + styles
│   ├── components/         # PredictForm.tsx
│   └── lib/                 # api.ts — API client
├── infra/
│   └── nginx/                # reverse proxy config
├── docs/
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── .github/workflows/        # backend-ci, frontend-ci
├── docker-compose.yml
└── LICENSE
```

<br>

## Getting Started

### Backend (FastAPI)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API available at `http://localhost:8000` (docs at `/docs`). A pretrained
model bundle is already included at `backend/models/regressor.joblib`.

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend available at `http://localhost:3000`. Set `NEXT_PUBLIC_API_URL` if
the API isn't running on `http://localhost:8000`.

### Full stack (Docker)

```bash
docker-compose up --build
```

### Tests

```bash
cd backend
pytest -q
```

<br>

## Roadmap

See [docs/ROADMAP.md](./docs/ROADMAP.md) — next up: proper prediction
intervals, more crops/regions, and a historical trend chart.

<br>

## Disclaimer

CropYield-AI gives a statistical estimate based on historical patterns, not
a guarantee. Actual yield depends on many field-level factors (soil health,
pest pressure, farming practices) not captured in this model.

<br>

## License

Released under the [MIT License](./LICENSE).
