"""
Train the CropYield-AI regression model on the FAO/World Bank crop yield
dataset (data/yield_df.csv: Area, Item, Year, rainfall, pesticides, avg_temp
-> hg/ha_yield).

Usage:
    python -m app.ml.train --data data/yield_df.csv --out models/regressor.joblib
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

NUMERIC_FEATURES = ["Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp"]
CATEGORICAL_FEATURES = ["Area", "Item"]
TARGET = "hg/ha_yield"


def build_model(seed: int) -> HistGradientBoostingRegressor:
    # Native categorical support (no one-hot encoding needed) keeps the
    # serialized model small -- a few MB instead of hundreds of MB.
    return HistGradientBoostingRegressor(
        categorical_features=CATEGORICAL_FEATURES,
        max_iter=300,
        learning_rate=0.08,
        max_depth=8,
        random_state=seed,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/yield_df.csv"))
    parser.add_argument("--out", type=Path, default=Path("models/regressor.joblib"))
    parser.add_argument("--n-estimators", type=int, default=300)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Loading {args.data}...")
    df = pd.read_csv(args.data)
    df = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES + [TARGET]].dropna()
    for col in CATEGORICAL_FEATURES:
        df[col] = df[col].astype("category")
    print(f"Dataset: {df.shape[0]} rows, {df['Item'].nunique()} crops, {df['Area'].nunique()} countries")

    X = df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.seed
    )

    pipe = build_model(args.seed)
    print("Training HistGradientBoostingRegressor...")
    t0 = time.time()
    pipe.fit(X_train, y_train)
    print(f"Training done in {time.time() - t0:.1f}s")

    y_pred = pipe.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mae_pct = float(np.mean(np.abs((y_test - y_pred) / y_test))) * 100

    print(f"\nTest R^2:  {r2:.4f}")
    print(f"Test MAE:  {mae:,.0f} hg/ha")
    print(f"Test MAPE: {mae_pct:.1f}%")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipe,
            "crops": sorted(df["Item"].unique().tolist()),
            "countries": sorted(df["Area"].unique().tolist()),
            "year_range": [int(df["Year"].min()), int(df["Year"].max())],
            "test_r2": r2,
            "test_mae": mae,
        },
        args.out,
    )
    print(f"Saved model bundle to {args.out}")


if __name__ == "__main__":
    main()
