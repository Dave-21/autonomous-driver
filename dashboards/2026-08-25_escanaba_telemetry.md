# Fuel Market Analysis Dashboard: Escanaba, MI (ZIP 49829)
**Date:** August 25, 2026

## Daily Market Summary (Escanaba ZIP 49829)
*   **Retail Average:** $4.115 USD/gal
*   **Cluster Performance:** High consistency across the local cluster; 3 of 4 stations are priced at a floor of $4.11, with one outlier (Holiday) at $4.13.
*   **Market Spread:** Local variance is narrow ($0.02), indicating high competition and price synchronization within the Delta County zone.
*   **Traffic Impact:** The region is currently experiencing a traffic index of 1.15, suggesting moderate movement volume influencing regional demand.

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:** WTI is trading at $85.01/bbl; Brent at $92.17/bbl.
*   **Supply Constraints:** 
    *   **Refinery Risk:** High risk of supply tightening due to deferred maintenance at Motiva (Texas) and ongoing capacity pressures.
    *   **Summer Mandate:** Active status adds a calculated premium of +$0.15/gal to regional costs.
*   **Midwest Logistics:** 
    *   Whiting Refinery remains the primary Midwest hub, but supply volatility is being mitigated by Green Bay's established terminal infrastructure.
    *   Chicago Spot Market (RBOB) currently sits at $3.2708/gal.
*   **Taxation Overlay:** Michigan-specific tax floors are calculated at $0.5238/gal, with a specific excise component of $0.309.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE:** $0.4175 | **RMSE:** $0.5113
    *   **R² Score:** -1.9999 (⚠️ *Critical Warning: Model indicates severe variance/poor fit in current market conditions.*)
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.8442
    *   **Historical Avg:** $0.5771
    *   **Drift Alert:** **ACTIVE** (+$0.2671 deviation). 

**Analyst Note:** The significant margin drift and negative R² score suggest that current macro pressures (refinery outages + summer blends) are deviating from historical training patterns. Manual override or model retraining is recommended to account for non-linear volatility in the Midwest corridor.