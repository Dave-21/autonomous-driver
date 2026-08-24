# Fuel Market Analysis Dashboard: Escanaba, MI (49829)
**Date:** 2026-08-24 | **Status:** ⚠️ DRIFT ALERT DETECTED

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.12 / gal
*   **Local Cluster Performance:** Stable; current cluster average aligns with target.
*   **Price Spread:** Minimal ($0.02), indicating highly competitive and uniform pricing among local providers (Kwik Trip, Krist, Holiday).
*   **Traffic Impact:** Higher-than-average traffic index (1.15) suggests sustained demand volumes across the US-2/US-41 corridor.

## Key Macro & Regional Indicators
*   **Crude Dynamics:** 
    *   WTI: $84.94 | Brent: $92.02. Current figures reflect a volatile baseline for regional downstream pricing.
*   **Supply Constraints:** Significant upward pressure is expected due to maintenance shutdowns at the **Motiva Port Arthur** and **Marathon Galveston Bay** refineries (7% of U.S. capacity).
*   **Regulatory Loading:** The **Summer Blend Mandate** is currently active, contributing a calculated cost premium of **+$0.15/gal**.
*   **Regional Logistics:** 
    *   The **Whiting Refinery** remains the dominant Midwest hub (440k bpd), but supply security is heavily influenced by the **Green Bay Terminal** corridor. 
    *   Michigan-specific taxes are contributing a baseline of ~$0.51 to final retail pricing.

## Model Performance & Margin Telemetry
*   **Model Architecture:** HistGradientBoostingRegressor
*   **Accuracy Metrics:**
    *   MAE: $0.126 | RMSE: $0.2817
    *   **R² Score: -0.25** (Warning: Model is currently underperforming relative to a simple mean baseline).
*   **Margin Analytics:**
    *   **Current Gross Margin:** $1.1566 
    *   **Historical Average:** $0.5224
    *   **Margin Drift:** +$0.6342 (Significant variance detected).
*   **Alert Status:** 🚨 **DRIFT_ALERT_FLAG: TRUE** 
    *   *Actionable Insight:* The significant margin drift and negative R² score indicate that the current model is failing to capture new volatility in the energy market. Retraining or feature engineering on refinery outage impacts is recommended.