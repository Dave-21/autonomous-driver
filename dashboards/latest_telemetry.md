# Daily Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-04 | **Status:** Active

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.025
*   **Current Cluster Range:** $3.97 – $4.19
*   **Local Price Spread:** $0.22
*   **Station Distribution:**
    *   **Premium:** Kwik Trip ($4.19)
    *   **Competitive:** Krist ($3.97), Holiday ($3.97)
*   **Analysis:** Current retail prices show a high variance relative to the target. The $4.19 outlier at Kwik Trip indicates a localized premium, while the $3.97 cluster represents the current price floor for the region.

## 2. Key Macro & Regional Indicators
*   **Global Crude Commodities:**
    *   **WTI:** $91.63/bbl | **Brent:** $96.43/bbl
*   **Supply Chain & Infrastructure:**
    *   **Refinery Risk:** Significant supply pressure noted from the Torrance (CA) outage.
    *   **Midwest Reliability:** The BP Whiting refinery remains a critical hub, though aged infrastructure continues to be a monitored risk factor.
    *   **Terminal Logistics:** Green Bay terminals remain active; high traffic indices (1.25) suggest high localized demand pressure.
*   **Regulatory & Market Factors:**
    *   **Summer Blend:** **ACTIVE** (Estimated Cost Premium: +$0.15)
    *   **Chicago Spot (RBOB):** $3.2084/gal
    *   **State Tax Floor:** $0.52 (Includes $0.309 Excise Tax)

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.2742
    *   **RMSE:** $0.2751
    *   **R² Score:** -155.35 (⚠️ **Critical Alert:** Negative R² indicates the model is currently performing worse than a horizontal mean; immediate retraining or feature re-weighting required).
*   **Profitability Metrics:**
    *   **Current Gross Margin:** $0.8166
    *   **Historical Avg:** $0.7268
    *   **Margin Drift:** +$0.0898 (Current margin is outperforming historical averages by ~12.7%).
    *   **Drift Alert:** Inactive.