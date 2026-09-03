# Executive Market Intelligence Report: Escanaba, MI

## Daily Market Summary (Escanaba ZIP 49829)
*   **Market Status:** Stable | **Local Cluster:** 4 Active Stations
*   **Target Retail Price:** $3.97/gal
*   **Local Price Spread:** $0.00 (Unified pricing across Kwik Trip, Krist, and Holiday stations)
*   **Geographic Context:** Delta County, MI (Zip 49829)

## Key Macro & Regional Indicators
*   **Crude Oil Benchmark:** 
    *   **WTI:** $91.84/bbl | **Brent:** $95.91/bbl (Reflecting high global demand/scarcity)
*   **Supply & Logistics:**
    *   **Refinery Capacity:** U.S. refineries are operating at 97% capacity; however, global geopolitical conflicts are tightening the refined product market.
    *   **Infrastructure:** Strong regional supply via Green Bay terminals (Sunoco LP) continues to support Midwest flow.
*   **Regulatory & Localized Factors:**
    *   **Summer Blend Mandate:** **Active** (Adding ~$0.15/gal cost premium).
    *   **Michigan Tax Floor:** Total estimated tax floor of $0.5172.
    *   **Chicago Spot Market:** Currently trading at $3.1603/gal.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.2858
    *   **RMSE:** $0.2860
    *   **R² Score:** -520.236 (⚠️ *Warning: Critical variance detected. Model fit is currently poor compared to a baseline mean.*)
*   **Margin Analysis:**
    *   **Current Margin:** $0.8097
    *   **Historical Avg:** $0.7228
    *   **Margin Drift:** +$0.0869 (Alert: **FALSE** - Variance remains within acceptable operational thresholds).