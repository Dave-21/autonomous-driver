import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURE_STORE_CSV = os.path.join("data", "feature_matrix.csv")
TELEMETRY_JSON = os.path.join("data", "telemetry.json")

def train_and_evaluate():
    if not os.path.exists(FEATURE_STORE_CSV):
        raise FileNotFoundError(f"Feature store missing at {FEATURE_STORE_CSV}. Run engineer.py first.")

    # Drop any weekend/holiday NaNs
    df = pd.read_csv(FEATURE_STORE_CSV).dropna(subset=["wti_usd_bbl", "rbob_wholesale_usd_gal", "target_escanaba_retail_price"])
    
    # 1. Feature selection: Remove gross_rack_to_retail_margin & net_margin_after_tax to eliminate target leakage
    feature_cols = [
        "wti_usd_bbl", "brent_usd_bbl", "rbob_wholesale_usd_gal",
        "is_summer_blend", "tax_floor_usd", "traffic_index",
        "crude_to_rbob_crack_spread", "local_price_spread_usd",
        "whiting_refinery_outage_risk", "national_refinery_outage_risk", "green_bay_terminal_risk"
    ]
    
    # 2. Local margin target: (Retail Price - Wholesale - Tax Floor)
    df["target_margin"] = df["target_escanaba_retail_price"] - df["rbob_wholesale_usd_gal"] - df["tax_floor_usd"]

    split_idx = int(len(df) * 0.8)
    X_train, X_test = df[feature_cols].iloc[:split_idx], df[feature_cols].iloc[split_idx:]
    y_train_margin = df["target_margin"].iloc[:split_idx]
    y_test_retail = df["target_escanaba_retail_price"].iloc[split_idx:]
    
    # 3. Hyperparameters tuned for small sample datasets
    model = HistGradientBoostingRegressor(
        max_iter=40,
        min_samples_leaf=3,
        early_stopping=False,
        random_state=42
    )
    model.fit(X_train, y_train_margin)

    # 4. Predict margin, then pass wholesale and tax floor through directly
    pred_margins = model.predict(X_test)
    pred_retail = X_test["rbob_wholesale_usd_gal"] + X_test["tax_floor_usd"] + pred_margins

    mae = float(mean_absolute_error(y_test_retail, pred_retail))
    rmse = float(np.sqrt(mean_squared_error(y_test_retail, pred_retail)))
    r2 = float(r2_score(y_test_retail, pred_retail)) if len(y_test_retail) > 1 else 1.0

    # Margin drift monitoring
    latest_margin = float(df['gross_rack_to_retail_margin'].iloc[-1])
    historical_avg_margin = float(df['gross_rack_to_retail_margin'].mean())
    margin_drift = round(latest_margin - historical_avg_margin, 4)

    telemetry = {
        "timestamp": df['timestamp'].iloc[-1],
        "total_sample_count": len(df),
        "model_type": "PassThrough_HistGradientBoosting",
        "metrics": {
            "mae_usd": round(mae, 4),
            "rmse_usd": round(rmse, 4),
            "r2_score": round(r2, 4)
        },
        "drift_telemetry": {
            "latest_gross_margin_usd": latest_margin,
            "historical_avg_margin_usd": round(historical_avg_margin, 4),
            "margin_drift_usd": margin_drift,
            "drift_alert_flag": abs(margin_drift) > 0.15
        }
    }

    os.makedirs("data", exist_ok=True)
    with open(TELEMETRY_JSON, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print(f"[SUCCESS] Model evaluation complete. Telemetry saved to {TELEMETRY_JSON}")
    print(json.dumps(telemetry, indent=2))

if __name__ == "__main__":
    train_and_evaluate()