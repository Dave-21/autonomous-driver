# Daily Market Summary (Escanaba ZIP 49829)
**Current Target Retail Average:** $3.49  
**Regional Context:** The Escanaba market is currently navigating the costs of the active **Summer Blend Mandate (+ $0.15)** and local Michigan tax structures. Despite local volatility in transport (Traffic Index: 1.15), the target retail price remains stable against the current Chicago Spot Market (RBOB) baseline.

# Key Macro & Regional Indicators
*   **Crude Dynamics:** WTI is trading at **$82.18/bbl**; Brent at **$87.93/bbl**.
*   **Refinery Supply Risk:** Ongoing maintenance outages at the Motiva Port Arthur and Marathon Galveston Bay refineries (representing ~7% of U.S. capacity) are exerting upward pressure on regional gasoline availability.
*   **Regional Infrastructure:** 
    *   **Whiting Refinery:** Remains a critical hub for Midwest supply stability.
    *   **Green Bay Terminals:** Serves as a vital logistics corridor; current pricing reflects localized distribution efficiency.
*   **Taxation:** Michigan excise taxes and local floors are factored into the $3.49 target, balancing against the RBOB wholesale price of **$2.8717**.

# Model Performance & Margin Telemetry
*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE/RMSE:** 0.0073 (High precision in prediction)
    *   **R² Score:** 0.0 (⚠️ *Warning: Model is currently tracking the mean; investigation into feature weight distribution required.*)
*   **Margin Analytics:**
    *   **Current Gross Margin:** $0.6183
    *   **Historical Average:** $0.6003
    *   **Margin Drift:** +$0.0180 (No alert triggered; variance remains within acceptable operational thresholds).