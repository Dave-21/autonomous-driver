import json
import os
import pandas as pd
from datetime import datetime

RAW_DATA_PATH = os.path.join("data", "raw", "latest_ingest.json")
FEATURE_STORE_CSV = os.path.join("data", "feature_matrix.csv")

def extract_news_alert_score(text: str) -> int:
    """Keyword-based NLP feature extraction for supply disruption risk."""
    risk_keywords = ["outage", "shutdown", "maintenance", "fire", "disruption", "capacity drop"]
    text_lower = text.lower()
    return sum(1 for kw in risk_keywords if kw in text_lower)

def transform_raw_to_features(raw_data: dict) -> dict:
    timestamp = raw_data.get("timestamp", datetime.now().isoformat())
    macro = raw_data.get("factor_1_global_crude", {})
    rules = raw_data.get("factor_3_summer_blend_mandate", {})
    spot = raw_data.get("factor_5_chicago_spot_market", {})
    taxes = raw_data.get("factor_6_michigan_taxes", {})
    traffic = raw_data.get("factor_8_us2_us41_traffic_index", 1.0)
    local = raw_data.get("factor_9_escanaba_lincoln_rd_cluster", {})

    wti = macro.get("wti_usd_bbl", 0.0)
    brent = macro.get("brent_usd_bbl", 0.0)
    rbob = spot.get("rbob_wholesale_usd_gal", 0.0)
    tax_floor = taxes.get("est_total_tax_floor_usd", 0.309)
    
    # Extract live scraped retail target and cluster price spread
    retail_price = float(local.get("target_retail_avg", 4.12))
    local_spread = float(local.get("local_price_spread_usd", 0.0))

    # Derived Economic Spreads & Margins
    gross_rack_to_retail_margin = round(retail_price - rbob, 4) if rbob > 0 else 0.0
    net_margin_after_tax = round(gross_rack_to_retail_margin - tax_floor, 4)
    crude_to_rbob_crack_spread = round(rbob - (wti / 42.0), 4) if wti > 0 else 0.0

    # Text Risk Features from Factors 2, 4, and 7
    nat_outage_risk = extract_news_alert_score(raw_data.get("factor_2_national_refinery_outages", ""))
    whiting_outage_risk = extract_news_alert_score(raw_data.get("factor_4_midwest_whiting_health", ""))
    terminal_risk = extract_news_alert_score(raw_data.get("factor_7_green_bay_terminals", ""))

    feature_row = {
        "timestamp": timestamp,
        "wti_usd_bbl": wti,
        "brent_usd_bbl": brent,
        "rbob_wholesale_usd_gal": rbob,
        "is_summer_blend": 1 if rules.get("is_active", False) else 0,
        "tax_floor_usd": tax_floor,
        "traffic_index": traffic,
        "crude_to_rbob_crack_spread": crude_to_rbob_crack_spread,
        "gross_rack_to_retail_margin": gross_rack_to_retail_margin,
        "net_margin_after_tax": net_margin_after_tax,
        "local_price_spread_usd": local_spread,
        "whiting_refinery_outage_risk": whiting_outage_risk,
        "national_refinery_outage_risk": nat_outage_risk,
        "green_bay_terminal_risk": terminal_risk,
        "target_escanaba_retail_price": retail_price  # Target variable (y)
    }
    
    return feature_row

def update_feature_matrix():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}. Run fetch_all.py first.")

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    row = transform_raw_to_features(raw_data)
    df_new = pd.DataFrame([row])

    os.makedirs("data", exist_ok=True)
    if os.path.exists(FEATURE_STORE_CSV):
        df_existing = pd.read_csv(FEATURE_STORE_CSV)
        # Avoid duplicate row insertion for identical timestamps
        df_combined = pd.concat([df_existing, df_new], ignore_index=True).drop_duplicates(subset=["timestamp"])
    else:
        df_combined = df_new

    df_combined.to_csv(FEATURE_STORE_CSV, index=False)
    print(f"[SUCCESS] Updated Feature Store at {FEATURE_STORE_CSV} ({len(df_combined)} total rows)")
    print("\nCalculated Feature Row:")
    print(json.dumps(row, indent=2))

if __name__ == "__main__":
    update_feature_matrix()