# Executive Fuel Market Analysis: Escanaba, MI (49829)
**Date:** 2026-10-14 | **Status:** ⚠️ **Margin Drift Alert**

## Daily Market Summary (Escanaba ZIP 49829)
*   **Retail Landscape:** 4 active stations within the local cluster.
*   **Target Retail Price:** $4.34/gal
*   **Local Spread:** $0.10 variance across the cluster.
*   **Station Pricing Breakdown:**
    *   **$4.39:** Kwik Trip, Holiday
    *   **$4.29:** Krist (Multiple locations)
*   **Market Sentiment:** Stable localized pricing despite upstream volatility.

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:** High-pressure environment with **WTI at $94.66/bbl** and **Brent at $106.21/bbl**.
*   **Refinery Supply Chain:** 
    *   **California:** Torrance refinery outages impacting regional distillate supply.
    *   **Midwest/Great Lakes:** Ongoing risk identified via the BP Whiting refinery lockout; Illinois supply chain remains pressured.
*   **Seasonal Factors:** Summer Blend mandate is **Inactive** (0.00 premium).
*   **Logistics & Infrastructure:** 
    *   **Chicago Spot Market:** $3.131/gal (Wholesale).
    *   **State Tax Floor:** $0.5154 (Includes $0.309 excise tax).
    *   **Traffic Index:** 1.0 (Stable flow on US-2/US-41 corridor).

## Model Performance & Margin Telemetry
*   **Prediction Accuracy:**
    *   **MAE:** $0.1518
    *   **RMSE:** $0.1648
    *   **R² Score:** -0.1166 (Note: Negative R² suggests model underperforming against baseline due to high volatility).
*   **Profitability & Drift Analysis:**
    *   **Current Gross Margin:** $1.209
    *   **Historical Average:** $0.8585
    *   **Margin Drift:** **+$0.3505**
    *   **Alert Status:** 🚩 **DRIFT_ALERT_FLAG: TRUE**
*   **MLOps Action Item:** The significant jump in gross margin relative to historical norms, combined with a negative R² score, suggests the current `PassThrough_HistGradientBoosting` model is struggling to reconcile high-volatility macro inputs with local retail pricing. Retraining or feature re-weighting is recommended.