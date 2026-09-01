# Executive Market Dashboard: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-01 | **Status:** ⚠️ Margin Drift Alert

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.97
*   **Local Price Spread:** $0.00 (Uniform pricing observed across active stations)
*   **Cluster Status:** Active monitoring on Lincoln Rd corridor.
*   **Station Insights:** 
    *   Kwik Trip and Krist are currently aligned with the target average.
    *   Data gaps exist for select stations (Holiday/Krist), potentially masking micro-variations in the local cluster.

## Key Macro & Regional Indicators
*   **Global Crude Basis:**
    *   **WTI:** $87.84/bbl
    *   **Brent:** $92.31/bbl
*   **Supply Constraints:**
    *   **Refinery Outages:** Significant impact noted from Torrance refinery outage (California) and general EIA-reported unplanned shutdowns.
    *   **Regulatory:** Summer Blend mandate is **Active**, adding an estimated **+$0.15** premium to regional overhead.
*   **Logistics & Regional Feed:**
    *   **Chicago Spot Market (RBOB):** $3.0932/gal.
    *   **Midwest Pipeline:** Whiting refinery notes indicate heavy reliance on Western Canadian Select processing.
    *   **Distribution:** Green Bay terminals remain the primary regional supply hub.
*   **Taxation:** Michigan tax floor remains at **$0.5131**, contributing to the final retail floor.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Current Performance Metrics:**
    *   **MAE:** $0.3266
    *   **RMSE:** $0.3284
*   **Critical MLOps Alerts:**
    *   **Margin Drift:** **ALERT** (Current: $0.8768 | Historical Avg: $0.7152) — A deviation of **+$0.1616** detected.
    *   **Model Integrity:** **CRITICAL.** The $R^2$ score of **-92.17** indicates severe model degradation or extreme data volatility. 
*   **Action Item:** Re-calibrate the `HistGradientBoostingRegressor` to address the negative $R^2$ and investigate the source of the margin drift.