# Executive Fuel Analytics Dashboard: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-30 | **Status:** ⚠️ **Action Required (Margin/Model Drift)**

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $4.52/gal
*   **Active Stations:** 4
*   **Market Consistency:** High (0.00 local spread)
*   **Current Retailers:** Kwik Trip, Krist, Holiday
*   **Inventory Sentiment:** Stable local pricing across all reported sites in the Escanaba cluster.

## 2. Key Macro & Regional Indicators
*   **Crude Oil Benchmarks:** WTI at **$90.05/bbl** | Brent at **$97.77/bbl** (High-cost environment).
*   **Refinery Dynamics:** 
    *   **Midwest Capacity:** High risk identified due to above-average refinery outages in the Midwest region.
    *   **Key Hubs:** Whiting Refinery remains a critical stable source for Midwest transportation fuels.
*   **Regulatory/Seasonal:** Summer blend mandate is **Inactive** (0.00 cost premium).
*   **Taxation:** Michigan State Tax floor remains at **$0.5235/gal**.
*   **Wholesale Gap:** Chicago Spot Market sits at **$3.266/gal**, indicating significant logistical/markup requirements to reach current retail levels.

## 3. Model Performance & Margin Telemetry
*   **Model Type:** PassThrough_HistGradientBoosting
*   **Accuracy Metrics:**
    *   **MAE:** 0.5042 | **RMSE:** 0.5244
    *   **R² Score:** **-8.7832** ⚠️ *(Critical Failure: Model is failing to capture underlying price relationships)*
*   **Margin Analysis:**
    *   **Current Margin:** $1.254
    *   **Historical Avg:** $0.8257
    *   **Margin Drift:** +$0.4283
*   **Alert Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE**
    *   *Analyst Note: The extreme negative R² score combined with the high margin drift suggests the model is no longer calibrated to current market volatility. Immediate retraining or feature re-weighting is recommended for the Escanaba cluster.*