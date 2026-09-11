# Executive Market Analysis: Escanaba, MI (ZIP 49829)
**Report Date:** 2026-09-11 | **Status:** ⚠️ Alert - Margin Drift Detected

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local market shows moderate volatility with a variance of **$0.24** between the cheapest and most expensive stations.

*   **Target Retail Average:** $4.315
*   **Current Cluster Range:** $4.25 — $4.49
*   **Active Stations:** 4
*   **Key Outliers:** 
    *   *Kwik Trip* is currently trading at a premium ($4.49).
    *   *Krist* locations are currently the floor price ($4.25).
*   **Demand Indicator:** High traffic index (1.25) on US-2/US-41 suggests strong local demand, supporting current price floors.

## 2. Key Macro & Regional Indicators
*   **Crude Market:** High volatility environment with **WTI at $99.66** and **Brent at $105.04**.
*   **Supply Constraints:** 
    *   **Refinery Risk:** Torrance, CA outage impacts national gasoline/distillate supply chains.
    *   **Midwest Stability:** Whiting Refinery remains a primary hub for Midwest fuel stability.
*   **Regulatory Impact:** Summer Blend Mandate is **Active**, adding a **$0.15** estimated cost premium.
*   **Regional Logistics:** Green Bay terminals show robust capacity (approx. 2.4M bbls gasoline), providing a localized buffer against coastal supply shocks.
*   **Taxation:** Michigan state tax floor is currently set at **$0.5173**.

## 3. Model Performance & Margin Telemetry
**⚠️ CRITICAL ALERT: Model Degradation Detected**

*   **Accuracy Metrics:**
    *   **MAE:** $0.1763
    *   **RMSE:** $0.2005
    *   **R² Score:** **-3.4354** (Critical Failure: The negative R² indicates the model is currently unable to explain the variance in price data, likely due to extreme market volatility or feature drift).
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.1519
    *   **Historical Average:** $0.7958
    *   **Margin Drift:** **+0.3561**
*   **Action Items:** 
    1.  **Immediate Retraining:** The negative R² score necessitates an immediate review of the *HistGradientBoostingRegressor* hyperparameters.
    2.  **Drift Investigation:** Investigate the cause of the $0.35 margin drift; current profitability is significantly deviating from historical norms.