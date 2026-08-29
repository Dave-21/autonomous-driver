# Daily Market Summary (Escanaba ZIP 49829)

*   **Target Retail Average:** $4.005
*   **Local Price Spread:** $0.04
*   **Active Cluster Count:** 4 Stations
*   **Traffic Index (US-2/US-41):** 1.44
*   **Station Breakdown:**
    *   **Kwik Trip:** $3.99
    *   **Holiday:** $3.99
    *   **Krist (Loc 1):** $4.01
    *   **Krist (Loc 2):** $4.03

---

## Key Macro & Regional Indicators

*   **Seasonal Factors:** Summer Blend Mandate is **Active** (Estimated Premium: +$0.15).
*   **Refinery Outlook:** High utilization projected for 2026; maintenance cycles are impacting supply dynamics.
*   **Taxation:** Michigan Excise Tax floor is set at $0.309.
*   **Regional Supply:** Green Bay terminal remains a critical logistics node for the region.
*   **Data Gaps:** 
    *   Global Crude (WTI/Brent) data is currently **NULL**.
    *   Chicago Spot Market (RBOB) data is currently **NULL**.

---

## Model Performance & Margin Telemetry

*   **Model Type:** HistGradientBoostingRegressor
*   **Accuracy Metrics:**
    *   **MAE:** $0.468
    *   **RMSE:** $0.4689
    *   **R² Score:** -263.974 (**CRITICAL_FAILURE**: Model fit is non-functional/divergent)
*   **Margin Analysis:**
    *   **Current Margin:** $0.00
    *   **Historical Avg:** $0.6722
    *   **Margin Drift:** -0.6722
*   **Alert Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE** 
    *   *Note: Immediate retraining or feature engineering required due to negative R² and significant margin degradation.*