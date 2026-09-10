# Escanaba, MI Fuel Market Intelligence Report
**Date:** 2026-09-10 | **Location:** Escanaba, MI (ZIP 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Cluster Status:** Active
*   **Target Retail Average:** $4.27
*   **Local Price Spread:** $0.04 (Low volatility)
*   **Active Stations:** 4
*   **Retailer Breakdown:**
    *   **Kwik Trip:** $4.27
    *   **Holiday:** $4.27
    *   **Krist (6344 US-2-41):** $4.29 (Premium)
    *   **Krist (102 N Lincoln Rd):** $4.25 (Discount)

## 2. Key Macro & Regional Indicators
*   **Global Crude Outlook:** Brent ($107.26) and WTI ($101.99) remain elevated, driven by global refinery capacity constraints.
*   **Refinery Infrastructure:** U.S. refineries are operating at **97% capacity**. While the 2026 maintenance season is approaching, current geopolitical conflicts are tightening the supply of refined products.
*   **Midwest Stability:** The **Whiting Refinery** remains a critical anchor for the Midwest economy, maintaining high throughput to offset regional volatility.
*   **Policy & Logistics:**
    *   **Summer Blend:** Active (Current impact: +$0.15/gal).
    *   **Chicago Spot Market:** Currently trading at $3.1976/gal.
    *   **Taxation:** Michigan excise tax of $0.309 applies; total tax floor estimated at $0.5194.

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.1457
    *   **RMSE:** $0.1765
*   **Critical Alert Status:** 
    *   **R² Score:** **-2.1832** (⚠️ *Critical Warning: Negative R² indicates the model is performing significantly worse than a horizontal baseline. Immediate retraining or feature engineering required.*)
    *   **Margin Drift:** **+0.2865** (🚨 *Alert Triggered: Current gross margin of $1.0724 deviates significantly from the historical average of $0.7859.*)

**Action Items:**
1.  **MLOps:** Investigate the negative R² score; investigate feature weights for `summer_blend_mandate` and `wholesale_price`.
2.  **Procurement:** Monitor margin drift to determine if the $0.28 increase is due to localized supply spikes or model error.