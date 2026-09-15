from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "country": "Indonesia",
    "crop": "Rice, paddy",
    "year": 2024,
    "rainfall_mm": 2500,
    "pesticides_tonnes": 5000,
    "avg_temp_c": 27.5,
}


def test_options_returns_countries_and_crops():
    r = client.get("/yield/options")
    assert r.status_code == 200
    body = r.json()
    assert "Indonesia" in body["countries"]
    assert len(body["crops"]) == 10
    assert 0.9 < body["model_r2"] <= 1.0


def test_predict_returns_positive_yield():
    r = client.post("/yield/predict", json=VALID_PAYLOAD)
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_yield_tons_per_ha"] > 0
    assert body["range_low_tons_per_ha"] <= body["predicted_yield_tons_per_ha"] <= body["range_high_tons_per_ha"]


def test_predict_rejects_unknown_country():
    payload = {**VALID_PAYLOAD, "country": "Narnia"}
    r = client.post("/yield/predict", json=payload)
    assert r.status_code == 422


def test_predict_rejects_unknown_crop():
    payload = {**VALID_PAYLOAD, "crop": "Dragon Fruit"}
    r = client.post("/yield/predict", json=payload)
    assert r.status_code == 422


def test_predict_rejects_out_of_range_temperature():
    payload = {**VALID_PAYLOAD, "avg_temp_c": 999}
    r = client.post("/yield/predict", json=payload)
    assert r.status_code == 422  # pydantic validation error


def test_predict_different_crops_give_different_yields():
    rice = client.post("/yield/predict", json=VALID_PAYLOAD).json()
    maize_payload = {**VALID_PAYLOAD, "crop": "Maize"}
    maize = client.post("/yield/predict", json=maize_payload).json()
    assert rice["predicted_yield_tons_per_ha"] != maize["predicted_yield_tons_per_ha"]
