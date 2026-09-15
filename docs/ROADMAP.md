# Roadmap

- [x] Train regression model on FAO/World Bank crop yield dataset
- [x] FastAPI `/yield/predict` and `/yield/options` endpoints
- [x] Next.js prediction form + result UI
- [x] Docker Compose (API + frontend + nginx)
- [x] CI for backend (pytest) and frontend (build)
- [ ] Add more crops/regions by merging additional FAO datasets (current
      dataset covers 10 crops and stops at 2013)
- [ ] Proper prediction intervals (quantile regression or conformal
      prediction) instead of a symmetric MAE-based band
- [ ] Feature importance / explanation view ("why this estimate") in the UI
- [ ] Historical trend chart: predicted vs. actual yield over time for a
      given country/crop
- [ ] Multi-language UI (currently Indonesian only)
- [ ] Batch prediction (upload a CSV of scenarios, get yields back)
