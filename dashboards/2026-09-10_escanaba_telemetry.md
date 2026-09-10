# Market Analysis Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-10 | **Status:** ⚠️ Alert - Model Drift Detected

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.27
*   **Current Cluster Status:** 4 active stations identified.
*   **Local Price Spread:** $0.04 (Low volatility within the immediate cluster).
*   **Station Inventory:**
    *   **Kwik Trip:** $4.27
    *   **Holiday:** $4.27
    *   **Krist (102 N Lincoln):** $4.25 (Price Leader)
    *   **Krist (6344 US-2-41):** $4.29

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:** High volatility noted with WTI at $103.93/bbl and Brent at $108.95/bbl.
*   **Regulatory & Seasonal:** Summer Blend Mandate is **Active**, contributing a +$0.15 cost premium.
*   **Supply Chain Health:** 
    *   **Regional Stability:** The Whiting Refinery (Lake Michigan) remains a key regional pillar for Midwest supply.
    *   **National Risk:** Ongoing refinery outages in California (Torrance) are tightening national distillate supply, potentially increasing pressure on downstream markets.
*   **Logistics & Tax:** Michigan state tax floor is estimated at $0.5223. Chicago spot market currently trading at $3.2453/gal.

## Model Performance & Margin Telemetry
*   **Accuracy Metrics:**
    *   **MAE:** $0.1664 | **RMSE:** $0.1907
*   **Critical Alerts:**
    *   **Margin Drift:** **$0.2349** (Exceeds historical threshold).
    *   **Drift Alert Flag:** **TRUE**.
    *   **R² Score:** **-3.241** (Model is currently underperforming compared to a simple mean baseline).
*   **MLOps Recommendation:** The negative R² score and high margin drift indicate that the current `HistGradientBoostingRegressor` is struggling to adapt to recent macro fluctuations (likely due to the high crude prices/summer blend overlap). **Immediate retraining or hyperparameter tuning is recommended.**