# Market Intelligence Report: Escanaba, MI (49829)
**Date:** August 31, 2026 | **Status:** ⚠️ High Alert (Model Drift Detected)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $3.97
*   **Active Stations:** 1 of 4 reporting (Kwik Trip @ $3.97)
*   **Market Dynamics:** High local price consistency. While three major competitors (Krist, Holiday) are currently reporting null values, the active Kwik Trip data sets the local floor for the 49829 zone.
*   **Trend Analysis:** Pricing remains steady, but regional volatility is expected due to seasonal mandates and refinery maintenance schedules.

## 2. Key Macro & Regional Indicators
*   **Global Commodities:** 
    *   **WTI:** $85.78/bbl | **Brent:** $88.36/bbl
*   **Supply Chain & Logistics:**
    *   **Refinery Pressure:** Upcoming maintenance schedules and the aging infrastructure at the Whiting Refinery indicate potential tightening of downstream supply.
    *   **Regional Hubs:** Green Bay terminal connectivity remains a primary logistics channel for Michigan's Upper Peninsula.
*   **Regulatory & Seasonal:** 
    *   **Summer Blend:** **ACTIVE**. Adds a calculated premium of **+$0.15/gal**.
*   **Taxation & Wholesale:**
    *   **Michigan Tax Floor:** $0.5124
    *   **Chicago Spot (RBOB):** $3.0803/gal
    *   **Midwest Traffic Index:** 1.15 (Reflects localized demand/logistics friction).

## 3. Model Performance & Margin Telemetry
*   **Accuracy Metrics:**
    *   **MAE:** $0.408 | **RMSE:** $0.4099
    *   **R² Score:** **-109.58** ⚠️ *(Critical Failure: Negative R² indicates the model is performing worse than a horizontal line; immediate retraining or feature re-engineering required).*
*   **Margin Analytics:**
    *   **Current Gross Margin:** $0.8897
    *   **Historical Average:** $0.7007
    *   **Margin Drift:** +$0.1890
*   **Alert Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE**
    *   *Action:* The model is currently experiencing significant variance from historical norms. Correlation between current feed features and actual pricing is currently degraded.