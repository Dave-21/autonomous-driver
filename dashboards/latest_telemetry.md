# Fuel Market Intelligence Dashboard: Escanaba, MI (49829)
**Date:** 2026-08-11 | **Status:** Active Monitoring

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $3.49 / gal
*   **Current Demand Index:** 1.15 (Elevated traffic volume)
*   **Seasonality Adjustment:** Summer Blend mandate is **ACTIVE**, adding a +$0.15 premium to local pricing structures.
*   **Market Positioning:** Prices are currently supported by high regional demand and the active summer blend overlay, despite stable commodity inputs.

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:** 
    *   WTI: $83.40 | Brent: $89.13 (Stable/High range)
*   **Refining & Supply Chain:**
    *   **Midwest Strength:** The Whiting Refinery remains a high-capacity anchor for the region, maintaining "above average" value positioning.
    *   **Regional Hubs:** Green Bay terminals remain operational; local infrastructure supports steady flow despite regional supply constraints noted in West Coast hubs.
*   **Local Economics:** 
    *   Chicago Spot Market: $2.8938 (Wholesale)
    *   Michigan Tax Floor: $0.5012 (Currenter estimated tax impact included)

## Model Performance & Margin Telemetry
| Metric | Value | Status |
| :--- | :--- | :--- |
| **Model Type** | HistGradientBoostingRegressor | ✅ Operational |
| **MAE (Mean Absolute Error)** | $0.0069 | ✅ High Precision |
| **RMSE (Root Mean Square Error)** | $0.0071 | ✅ Low Variance |
| **R² Score** | -3.5714 | ⚠️ **Warning: Poor Fit** |
| **Gross Margin Drift** | +$0.0148 | ✅ Nominal |
| **Drift Alert** | **FALSE** | ✅ Stable |

**Analyst Note:** While point-prediction accuracy (MAE/RMSE) is exceptionally high, the negative $R^2$ score suggests a significant mismatch between model logic and historical variance. Recommend reviewing feature weights for *factor_8* (Traffic Index) and *factor_3* (Summer Blend) to stabilize the correlation coefficient.