# Escanaba Fuel Market Intelligence Dashboard
**Date:** 2026-10-07 | **Location:** Escanaba, MI (Zip: 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Target Average:** $4.385 / gal
*   **Active Station Count:** 4
*   **Local Price Spread:** $0.02 (High competitive alignment)
*   **Station Breakdown:**
    *   **Kwik Trip:** $4.37
    *   **Krist (x2):** $4.39
    *   **Holiday:** $4.39
*   **Analysis:** The narrow price spread suggests a highly synchronized local market. Prices are holding steady with minimal variance across the 4-station cluster.

## 2. Key Macro & Regional Indicators
*   **Crude Dynamics:** 
    *   WTI: $89.23 | Brent: $101.23.
    *   *Note:* High Brent spread indicates regional premium volatility.
*   **Refinery Health:** 
    *   **Midwest:** Whiting, IN remains a high-capacity anchor (435k bbl/day).
    *   **National:** Significant supply pressure noted from California refinery outages, though mitigated by Midwest capacity.
*   **Regulatory/Seasonal:** Summer Blend mandate is currently **Inactive**, removing seasonal production constraints.
*   **Logistics & Tax:** 
    *   **Green Bay Terminals:** Active; providing steady regional supply flow.
    *   **State Burden:** Michigan total tax floor stands at $0.5147/gal.
*   **Chicago Spot Market:** Currently trading at $3.1189/gal.

## 3. Model Performance & Margin Telemetry
*   **Model Type:** `PassThrough_HistGradientBoosting`
*   **Accuracy Metrics:**
    *   **MAE:** $0.436
    *   **RMSE:** $0.4744
    *   **R² Score:** -10.08 (⚠️ **Critical Failure Alert**)
*   **Margin Analytics:**
    *   **Current Gross Margin:** $1.2661
    *   **Historical Avg Margin:** $0.8374
    *   **Margin Drift:** +$0.4287 
*   **System Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE**
*   **Actionable Insight:** The negative R² score combined with the positive margin drift indicates the model is currently failing to predict price fluctuations accurately. The current "outlier" margin suggests the model is not adjusting correctly to recent market shocks or local competition shifts. Re-calibration of the Gradient Boosting parameters is recommended.