import os
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

FEATURE_STORE_CSV = os.path.join("data", "feature_matrix.csv")

def inspect():
    df = pd.read_csv(FEATURE_STORE_CSV).dropna(
        subset=["wti_usd_bbl", "rbob_wholesale_usd_gal", "target_escanaba_retail_price"]
    )
    
    feature_cols = [
        "wti_usd_bbl", "brent_usd_bbl", "rbob_wholesale_usd_gal",
        "is_summer_blend", "tax_floor_usd", "traffic_index",
        "crude_to_rbob_crack_spread", "local_price_spread_usd",
        "whiting_refinery_outage_risk", "national_refinery_outage_risk", "green_bay_terminal_risk"
    ]
    
    # Calculate net margin target
    df["target_margin"] = df["target_escanaba_retail_price"] - df["rbob_wholesale_usd_gal"] - df["tax_floor_usd"]

    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:].copy()

    model = HistGradientBoostingRegressor(
        max_iter=40,
        min_samples_leaf=3,
        early_stopping=False,
        random_state=42
    )
    model.fit(train_df[feature_cols], train_df["target_margin"])

    # Pass-through reconstruction: Wholesale + Tax + Predicted Margin
    pred_margins = model.predict(test_df[feature_cols])
    test_df["predicted_retail"] = (
        test_df["rbob_wholesale_usd_gal"] + test_df["tax_floor_usd"] + pred_margins
    ).round(3)
    test_df["error_usd"] = (test_df["predicted_retail"] - test_df["target_escanaba_retail_price"]).round(3)

    print("\n--- Pass-Through Predictions Across Recent Price Surge ---")
    display_cols = [
        "timestamp", "wti_usd_bbl", "rbob_wholesale_usd_gal",
        "target_escanaba_retail_price", "predicted_retail", "error_usd"
    ]
    print(test_df[display_cols].to_string(index=False))

if __name__ == "__main__":
    inspect()