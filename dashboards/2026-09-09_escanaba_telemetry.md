# Executive Market Dashboard: Escanaba, MI Fuel Analysis
**Date:** 2026-09-09 | **Region:** Delta County (ZIP 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.12/gal
*   **Current Price Range:** $3.97 – $4.27
*   **Local Spread:** $0.30
*   **Active Station Count:** 4
*   **Station Breakdown:**
    *   **Lowest:** $3.97 (Krist - 6344 US-2-41 MI-35)
    *   **Mid:** $4.07 (Krist - 102 N Lincoln Rd)
    *   **Mid:** $4.17 (Holiday - 700 N Lincoln Rd)
    *   **Highest:** $4.27 (Kwik Trip - 501 N Lincoln Rd)

## 2. Key Macro & Regional Indicators
*   **Global Crude Basis:**
    *   **WTI:** $95.15/bbl | **Brent:** $100.65/bbl
*   **Refining & Supply:**
    *   **Midwest Stability:** BP Whiting Refinery remains a primary regional anchor with 440k BPD capacity.
    *   **West Coast Impact:** Torrance refinery outage noted (limited direct impact on MI supply, but increasing national price pressure).
*   **Regulatory & Localized Factors:**
    *   **Summer Blend Mandate:** **ACTIVE** (Estimated premium: +$0.15).
    *   **Chicago Spot (RBOB):** $3.0979/gal.
    *   **Michigan State Tax:** $0.309 excise; $0.5134 total tax floor.
*   **Traffic Index (US-2/US-41):** 1.0 (Stable).

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.0769 | **RMSE:** $0.1032
    *   **R² Score:** -1.3036 (**CRITICAL ALERT**: Negative R2 indicates the model is performing worse than a horizontal mean baseline).
*   **Margin Analytics:**
    *   **Current Gross Margin:** $1.0221
    *   **Historical Avg:** $0.7570
    *   **Margin Drift:** +$0.2651
*   **Alert Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE**
    *   *Action Required:* The significant margin drift and negative R2 score suggest a decoupling between the training features and current market realities (likely driven by the Summer Blend premium and regional crude volatility). Model retraining/re-calibration is recommended.