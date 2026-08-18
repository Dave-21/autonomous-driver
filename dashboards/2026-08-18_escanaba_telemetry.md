# Fuel Price Analytics Dashboard: Escanaba, MI (Zip 49829)
**Date:** 2026-08-18 | **Status:** Active Monitoring

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 /gal
*   **Current Market Sentiment:** Stable with upward pressure from seasonal factors and refinery constraints.
*   **Regional Context:** The local retail price reflects a combination of the Chicago spot market ($3.01), state-specific tax floors (~$0.51), and active summer blend mandates (+ $0.15).

## Key Macro & Regional Indicators
*   **Crude Oil Dynamics:** 
    *   WTI: **$84.45/bbl** | Brent: **$91.31/bbl** (Moderate volatility observed).
*   **Supply Chain & Infrastructure:**
    *   **Refinery Risk:** Active outages at Motiva Port Arthur and Marathon Galveston Bay are creating upward pressure on regional gasoline/diesel inventories.
    *   **Regional Logistics:** Green Bay terminals remain critical for supply chain flow to the Upper Peninsula; focus remains on pipeline reliability.
    *   **Whiting Refinery:** Maintained as a stable Michigan-region hub, though local availability continues to buffer against national shortages.
*   **Demand & Policy:**
    *   **Summer Blend Mandate:** **Active** (Adding $0.15/gal premium).
    *   **Traffic Index (US2/US41):** **1.15** (Moderate local demand).

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   MAE: 0.0 | RMSE: 0.0 | R² Score: 0.0 *(Note: Indicators suggest a live/training state or high-precision fit on current data points).*
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.4758
    *   **Historical Average:** $0.5629
    *   **Margin Drift:** **-0.0871** (Negative trend detected)
*   **Alert Status:** `False` (Drift is noted but currently remains within acceptable operational thresholds).

***
**Actionable Insight:** While retail prices remain stable at the $3.49 target, the **-0.0871 margin drift** indicates tightening profitability for local distributors due to increased procurement costs and refinery scarcity. Monitor regional supply levels closely over the next 48 hours.