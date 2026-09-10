# Executive Market Dashboard: Escanaba, MI (Zip 49829)
**Date:** 2026-09-10 | **Status:** ⚠️ DRIFT ALERT

## 1. Daily Market Summary (Escanaba ZIP 49829)
The Escanaba cluster currently shows high price stability with a minimal spread, aligning closely with the target retail average.

*   **Current Cluster Status:** 4 active stations | **Target Avg:** $4.275
*   **Retail Price Inventory:**
    *   **Kwik Trip:** $4.27
    *   **Krist (US-2-41):** $4.29
    *   **Krist (Lincoln Rd):** $4.27
    *   **Holiday:** $4.27
*   **Local Spread:** $0.02 (Low variance)

## 2. Key Macro & Regional Indicators
*   **Crude Market:** WTI is trading at **$101.70/bbl**; Brent at **$106.99/bbl**.
*   **Refinery Logistics:** 
    *   **Capacity Squeeze:** U.S. refineries are operating at **97% capacity**. Global supply constraints and upcoming maintenance cycles are creating a tightening refined products market.
    *   **Regional Stability:** The **Whiting Refinery** remains a critical infrastructure anchor for the Midwest.
*   **Regulatory & Seasonal:**
    *   **Summer Blend:** Active (adds approx. **$0.15** to base cost).
    *   **Taxation:** State/Local floor sits at **$0.5181** (including $0.309 excise).
*   **Regional Feed:** Green Bay terminal operations remain active, stabilizing downstream supply.

## 3. Model Performance & Margin Telemetry
**Model Type:** `HistGradientBoostingRegressor`

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.1245 | ✅ Stable |
| **RMSE** | $0.1602 | ✅ Acceptable |
| **R² Score** | **-1.5243** | ❌ **CRITICAL** |
| **Gross Margin (Current)** | $1.0992 | ⚠️ Elevated |
| **Margin Drift** | **$0.3183** | ⚠️ **ALERT** |

**MLOps Action Items:**
1.  **Model Retraining Required:** The negative $R^2$ score indicates the model is performing significantly worse than a baseline mean, likely due to sudden volatility in the "Refinery Outage" and "Summer Blend" features.
2.  **Drift Investigation:** A $0.3183$ margin drift (significantly above the $0.7809$ historical average) suggests a decoupling between current macro inputs and retail price outcomes.
3.  **Feature Re-weighting:** Recommend auditing the weight of `factor_2_national_refinery_outages` to better capture the current supply squeeze.