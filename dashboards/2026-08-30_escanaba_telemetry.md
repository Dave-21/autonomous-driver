# Executive Energy Market Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-08-30 | **Status:** ⚠️ ALERT - Model Drift Detected

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.997
*   **Active Stations:** 3 
*   **Local Price Variance:** ±$0.02 (Tight clustering)
*   **Live Pricing:**
    *   **Kwik Trip:** $3.99
    *   **Krist (102 N Lincoln):** $4.01
    *   **Holiday:** $3.99
*   **Actionable Insight:** Local competition is aggressive; pricing is currently holding steady near the $4.00 psychological threshold.

## 2. Key Macro & Regional Indicators
*   **Crude Fundamentals:** WTI at $83.40; Brent at $88.10. Prices are stable but remain in a high-cost environment.
*   **Supply & Logistics:** 
    *   **Summer Blend Mandate:** ACTIVE (Adding ~$0.15 to base cost).
    *   **Regional Hubs:** Whiting Refinery remains a critical midwest anchor; Green Bay terminals show ongoing logistics activity.
*   **Refinery Outlook:** High utilization expected through 2026 due to limited maintenance windows, likely supporting a higher floor for regional premiums.
*   **Traffic Influence:** High volume on US-2/US-41 (Index: 1.44) indicates significant local demand pressure.
*   **Taxation:** Michigan state/local tax floor of $0.5106 is currently factored into retail pricing.

## 3. Model Performance & Margin Telemetry
*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE/RMSE:** ~0.44 (Stable at current accuracy levels).
    *   **R² Score:** -195.43 (🚨 **CRITICAL FAILURE**; indicates a significant mismatch between model assumptions and incoming feature distribution).
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.9468
    *   **Historical Avg:** $0.6958
    *   **Margin Drift:** +$0.251
*   **Alert Status:** 🚩 **DRIFT ALERT ACTIVE**. The significant negative R² and positive margin drift indicate that the model is currently failing to predict price movements accurately. **Manual override or retraining on recent feature sets is recommended.**