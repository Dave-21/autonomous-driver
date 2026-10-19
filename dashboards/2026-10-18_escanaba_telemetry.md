# Fuel Market Analysis: Escanaba, MI (Zip 49829)
**Report Date:** 2026-10-18

## Daily Market Summary (Escanaba ZIP 49829)
*   **Current Retail Price:** $4.26
*   **Active Station Count:** 2 (Kwik Trip, Holiday)
*   **Market Coverage:** 50% of local cluster reporting.
*   **Price Stability:** Consistent pricing observed between reporting stations in the Delta County cluster.
*   **Logistics Note:** Local price spread is currently flat ($0.00) among reporting entities.

## Key Macro & Regional Indicators
*   **Crude Oil Index:** 
    *   WTI: $97.72/bbl 
    *   Brent: $108.09/bbl
*   **Refining & Supply:**
    *   **Midwest Outlook:** High alert on inventory levels. Midwest accounts for 22% of US refining capacity; current reports indicate lower-than-average regional inventories.
    *   **California Impact:** Torrance refinery outage (3rd largest in SoCal) is impacting regional distribution.
    *   **Whiting Refinery:** Operational status remains stable as a primary Midwest hub.
*   **Seasonality:** Summer Blend mandate is **Inactive** (Cost Premium: $0.00).
*   **Regional Hubs:** Chicago Spot Market currently sits at $3.0976/gal; Green Bay terminals show high activity for regional distribution.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `PassThrough_HistGradientBoosting`
*   **Accuracy Metrics:**
    *   **MAE:** $0.1778
    *   **RMSE:** $0.2048
*   **Critical Alerts:**
    *   **R² Score:** -1.6394 (Warning: Model predictive power is currently failing; inspection required).
    *   **Margin Drift:** **ALERT**
        *   *Current Gross Margin:* $1.1624
        *   *Historical Average:* $0.8717
        *   *Variance:* +$0.2907
*   **Action Item:** Investigation required into the "drift_alert_flag" status; the significant jump in gross margin suggests either a localized pricing anomaly or a decoupling from historical wholesale correlations.