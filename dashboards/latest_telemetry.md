# Executive Market Dashboard: Escanaba, MI (ZIP 49829)
**Date:** 2026-10-13 | **Status:** ⚠️ **Alert - Margin Drift Detected**

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Cluster Average:** $4.34
*   **Local Price Spread:** $0.10
*   **Active Retailer Count:** 4
*   **Station Breakdown:**
    *   **Kwik Trip / Holiday:** $4.39 (Market High)
    *   **Krist (Multiple Locations):** $4.29 (Market Low)
*   **Analysis:** The local market shows a tight, stable spread. Retailers are currently pricing within a 10-cent window, suggesting high competition and synchronized pricing in the Delta County cluster.

## 2. Key Macro & Regional Indicators
*   **Refinery Supply Risk (High):** Significant headwinds identified in PADD 2 (Great Lakes region). Planned maintenance and deferred maintenance reductions (144,000 bpd) are expected to tighten regional supply.
*   **Crude Market Context:** Brent is trading at a significant premium over WTI ($105.61 vs $94.15), indicating global supply constraints and high demand.
*   **Regional Logistics:** Chicago Spot Market is currently at $3.1275/gal. With Michigan's tax floor at ~$0.5152, the remaining margin for transport and retail overhead is compressed.
*   **Regulatory Note:** Summer Blend Mandate is currently **Inactive**, removing a seasonal cost premium from the calculation.

## 3. Model Performance & Margin Telemetry
*   **Current Margin:** $1.2125
*   **Historical Average:** $0.8533
*   **Margin Drift:** +$0.3592 (**ALERT TRIGGERED**)
*   **Model Metrics:**
    *   **MAE:** $0.2211
    *   **RMSE:** 0.318
    *   **R² Score:** -2.8553 ⚠️
*   **MLOps Action Items:**
    1.  **Model Degradation:** The negative R² score indicates the `PassThrough_HistGradientBoosting` model is currently performing worse than a simple mean baseline.
    2.  **Drift Investigation:** The significant margin drift (+42% over historical average) suggests a decouple between wholesale inputs and retail premiums. 
    3.  **Recommendation:** Immediate retraining or feature re-weighting is required, specifically focusing on the PADD 2 refinery outage impact on local regional premiums.