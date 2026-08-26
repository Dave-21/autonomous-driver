# Fuel Market Intelligence Report: Escanaba, MI (49829)
**Date:** 2026-08-26 | **Status:** Alert Active

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.11
*   **Active Cluster Count:** 2 stations reporting active pricing in the Lincoln Rd corridor.
*   **Local Dynamics:** Price parity observed across available retail points ($4.11). High consistency noted despite regional volatility.

## Key Macro & Regional Indicators
*   **Crude Feed_Prices:** WTI at **$80.36/bbl** | Brent at **$85.30/bbl**.
*   **Supply Constraints:** 
    *   **Summer Blend Mandate:** Active (+ $0.15 premium).
    *   **Refinery Impact:** California outages (Torrance) and Midwest hub stability (Whiting Refinery) are the primary drivers for regional supply volume.
*   **Regional Logistics:** High traffic index (**1.15**) suggests moderate local demand pressure. 
*   **Fiscal Load:** Michigan excise tax floor remains at **$0.5006**.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Error Metrics:** MAE/RMSE: **0.6242** (Moderate precision).
*   **Alert Status:** ⚠️ **CRITICAL DRIFT DETECTED**
    *   **R² Score:** -33,000.05 (Indicates severe model degradation or input outlier).
    *   **Margin Drift:** $0.6064 above historical average ($0.6201). 
    *   **Action Required:** Investigate training data for "out of distribution" samples; retrain/recalibrate model due to significant drift alert flag.