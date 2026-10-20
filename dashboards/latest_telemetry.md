# Fuel Market Analysis: Escanaba, MI (ZIP 49829)
**Report Date:** 2026-10-19

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.233
*   **Local Price Spread:** $0.02
*   **Active Station Cluster:** 3 Stations (4 reporting)
*   **Retailer Performance:**
    *   **Kwik Trip:** $4.24
    *   **Holiday:** $4.24
    *   **Krist (US-2-41):** $4.22
*   **Analysis:** Current retail pricing in the 49829 zone is stable with a tight spread. Two primary retailers are aligned with the upper bound of the target, while one offers a marginal discount.

## Key Macro & Regional Indicators
*   **Crude Oil Benchmarks:**
    *   **WTI:** $98.79 / bbl
    *   **Brent:** $109.82 / bbl
*   **Refinery Dynamics:** 
    *   **Utilization:** 93.5% (High). Refinery capacity is nearing peak operational limits, suggesting potential for supply-side volatility if utilization continues to climb.
    *   **Whiting Refinery:** Operational status remains a critical Midwest supply pillar.
*   **Regulatory/Seasonal:** 
    *   **Summer Blend:** Inactive (No premium cost currently applied).
*   **Logistics:** 
    *   **Terminals:** Green Bay Terminal (410 Prairie Ave) remains a primary downstream node for the region.

## Model Performance & Margin Telemetry
*   **Accuracy Metrics:**
    *   **MAE:** $0.1896
    *   **RMSE:** $0.2267
*   **Model Health Alert:**
    *   **R² Score:** -4.1918 (Warning: Negative R² indicates the model is currently performing worse than a horizontal baseline; retraining recommended).
*   **Margin Analytics:**
    *   **Current Gross Margin:** $1.1203
    *   **Historical Avg:** $0.8751
    *   **Margin Drift:** +0.2452
    *   **Alert Status:** 🚩 **DRIFT_ALERT_ACTIVE**
*   **Action Item:** Immediate investigation of the `PassThrough_HistGradientBoosting` model is required due to extreme R² degradation and significant margin drift.