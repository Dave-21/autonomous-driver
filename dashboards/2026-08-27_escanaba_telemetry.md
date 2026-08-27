# Executive Market Dashboard: Escanaba, MI (ZIP 49829)
**Date:** 2026-08-27 | **Status:** ⚠️ **ALERT: Margin Drift Detected**

## Daily Market Summary (Escanaba ZIP 49829)
*   **Retail Average:** $4.08 / gal
*   **Local Price Spread:** $0.04 (Low variance across local cluster)
*   **Active Cluster Size:** 4 Stations
*   **Station Breakdown:**
    *   **Kwik Trip:** $4.09
    *   **Krist (Unit 1):** $4.09
    *   **Krist (Unit 2):** $4.05 (Local floor)
    *   **Holiday:** $4.09

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:**
    *   **WTI:** $82.63 | **Brent:** $87.55
    *   **Impact:** High regional volatility expected due to global supply constraints.
*   **Supply Chain & Refining Risk:**
    *   **Refinery Constraints:** Significant pressure on US refining capacity (>95% utilization). Critical outages in California (Torrance) and potential disruption from regional geopolitical tensions are tightening the distillate supply.
    *   **Midwest Hub:** Whiting Refinery (high capacity) remains a primary regional pivot, but high utilization levels indicate a fragile buffer.
*   **Regulatory & Logistics:**
    *   **Summer Blend:** Active (+$0.15 premium).
    *   **Michigan Tax Floor:** $0.5048.
    *   **Traffic Index (US-2/US-41):** 1.15 (Elevated local movement).
*   **Wholesale Spot:** RBOB currently trading at $2.954.

## Model Performance & Margin Telemetry
*   **Model Integrity:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE:** 0.5603 | **RMSE:** 0.5605
    *   **R² Score:** -1197.12 (**Critical Warning:** Model showing extreme variance/under-fitting; immediate retraining or feature re-engineering recommended).
*   **Margin Analytics:**
    *   **Current Margin:** $1.126
    *   **Historical Average:** $0.6687
    *   **Margin Drift:** +$0.4573
*   **Alert Status:** 🚩 **DRIFT_ALERT_FLAG: TRUE** 
    *   *Action Item: Immediate review of pricing strategy and margin impact due to significant deviation from historical baselines.*