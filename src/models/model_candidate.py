import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# Model Architecture: Cost Pass-Through Margin Regressor with GradientBoosting
MODEL_TYPE = "PassThrough_GradientBoosting"

def train_and_forecast(df_train: pd.DataFrame, df_test: pd.DataFrame, tomorrow_features: dict) -> dict:
    feature_cols = [
        "wti_usd_bbl", "brent_usd_bbl", "rbob_wholesale_usd_gal",
        "is_summer_blend", "tax_floor_usd", "traffic_index",
        "crude_to_rbob_crack_spread", "local_price_spread_usd",
        "whiting_refinery_outage_risk", "national_refinery_outage_risk", "green_bay_terminal_risk"
    ]

    # Calculate target net margin: Retail - Wholesale - Taxes
    train_margin = df_train["target_escanaba_retail_price"] - df_train["rbob_wholesale_usd_gal"] - df_train["tax_floor_usd"]

    model = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        min_samples_split=2,
        random_state=42
    )
    model.fit(df_train[feature_cols], train_margin)

    # 1. Evaluate on test set (reconstructing retail prices)
    pred_test_margins = model.predict(df_test[feature_cols])
    pred_test_retail = df_test["rbob_wholesale_usd_gal"] + df_test["tax_floor_usd"] + pred_test_margins

    # 2. Forecast tomorrow's retail price
    df_tomorrow = pd.DataFrame([tomorrow_features])
    tomorrow_margin_pred = model.predict(df_tomorrow[feature_cols])[0]
    predicted_tomorrow_retail = float(tomorrow_features["rbob_wholesale_usd_gal"] + tomorrow_features["tax_floor_usd"] + tomorrow_margin_pred)

    # Calculate MAE on test set
    test_mae = mean_absolute_error(df_test["target_escanaba_retail_price"], pred_test_retail)

    return {
        "model_type": MODEL_TYPE,
        "test_predictions": pred_test_retail.tolist(),
        "predicted_tomorrow_retail": round(predicted_tomorrow_retail, 3),
        "test_mae": test_mae
    }