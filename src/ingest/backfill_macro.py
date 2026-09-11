import os
import pandas as pd
import yfinance as yf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FEATURE_STORE = os.path.join(BASE_DIR, "data", "feature_matrix.csv")

def backfill_historical_macro():
    print("[BACKFILL] Downloading historical WTI, RBOB, and Brent futures...")
    
    # Tickers: WTI Crude (CL=F), RBOB Gasoline (RB=F), Brent Crude (BZ=F)
    tickers = ["CL=F", "RB=F", "BZ=F"]
    data = yf.download(tickers, start="2023-01-01", interval="1d", progress=False)["Close"]

    macro_df = pd.DataFrame({
        "date": data.index.strftime("%Y-%m-%d"),
        "wti_usd_bbl": data["CL=F"].values,
        "rbob_wholesale_usd_gal": data["RB=F"].values,
        "brent_usd_bbl": data["BZ=F"].values,
    }).dropna()

    # Calculate fundamental refinery crack spread ($/bbl: 42 gallons per barrel)
    macro_df["crude_to_rbob_crack_spread"] = (
        (macro_df["rbob_wholesale_usd_gal"] * 42.0) - macro_df["wti_usd_bbl"]
    ).round(3)

    print(f"[BACKFILL] Retrieved {len(macro_df)} daily trading records.")

    # Load existing feature matrix containing Wayback retail prices
    df_existing = pd.read_csv(FEATURE_STORE)
    
    # Extract date string from timestamp (supports ISO format)
    df_existing["date"] = pd.to_datetime(df_existing["timestamp"]).dt.strftime("%Y-%m-%d")

    # Merge retail prices with the complete historical macro ledger
    merged = pd.merge(
        df_existing.drop(columns=["wti_usd_bbl", "rbob_wholesale_usd_gal", "brent_usd_bbl", "crude_to_rbob_crack_spread"], errors="ignore"),
        macro_df,
        on="date",
        how="inner"
    )

    # Re-apply constant baseline features for historical dates if null
    merged["tax_floor_usd"] = merged["tax_floor_usd"].fillna(0.51)
    merged["is_summer_blend"] = pd.to_datetime(merged["date"]).dt.month.between(6, 8).astype(int)
    merged["traffic_index"] = merged["traffic_index"].fillna(1.0)
    merged["local_price_spread_usd"] = merged["local_price_spread_usd"].fillna(0.12)
    merged["whiting_refinery_outage_risk"] = merged["whiting_refinery_outage_risk"].fillna(0.0)
    merged["national_refinery_outage_risk"] = merged["national_refinery_outage_risk"].fillna(0.0)
    merged["green_bay_terminal_risk"] = merged["green_bay_terminal_risk"].fillna(0.0)

    # Sort chronologically and save
    merged = merged.sort_values("date").reset_index(drop=True)
    merged.to_csv(FEATURE_STORE, index=False)
    
    valid_rows = len(merged.dropna(subset=["target_escanaba_retail_price", "rbob_wholesale_usd_gal"]))
    print(f"[SUCCESS] Feature store updated! Total verified historical samples: {valid_rows}")

if __name__ == "__main__":
    backfill_historical_macro()