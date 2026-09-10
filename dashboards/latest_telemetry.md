# Energy Market Analysis Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-10 | **Status:** ⚠️ Alert - Margin Drift Detected

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.275
*   **Local Price Range:** $4.27 – $4.29 (Narrow spread of $0.02)
*   **Active Inventory:** 4 stations reporting in the Escanaba cluster.
*   **Market Dynamics:** Pricing remains stable across the immediate vicinity, with Kwik Trip, Krist, and Holiday stations maintaining consistent positioning relative to the local average.

## 2. Key Macro & Regional Indicators
*   **Crude Fundamentals:** High-pressure environment with **WTI at $100.23/bbl** and **Brent at $105.64/bbl**.
*   **Supply Constraints:** 
    *   **Refinery Risk:** Reports indicate significant refinery capacity strain and delayed maintenance (e.g., Motiva Port Arthur) to capture high margins.
    *   **Regulatory Impact:** Summer Blend mandates remain **Active**, adding a **$0.15/gal** cost premium.
*   **Regional Logistics:** 
    *   **Midwest Spot Market:** Chicago RBOB is currently at $3.169/gal.
    *   **Local Infrastructure:** Green Bay terminals (Sunoco LP) remain active, providing a stable regional distribution backbone despite upstream volatility.
*   **Taxation:** State/local tax floor remains at $0.5177, with a $0.309 excise component.

## 3. Model Performance & Margin Telemetry
*   **Model Health:** **CRITICAL.** The `HistGradientBoostingRegressor` is currently underperforming.
    *   **R² Score:** -1.5686 (Indicates model is failing to capture current trend variance).
    *   **MAE/RMSE:** 0.1205 / 0.1606.
*   **Drift Analysis:** 
    *   **Alert Status:** **ACTIVE**
    *   **Margin Variance:** Current gross margin is **$1.106**, significantly higher than the historical average of **$0.7695**.
    *   **Delta:** +$0.3365 deviation.
*   **Actionable Insight:** The positive margin drift and negative R² score suggest a significant decoupling between historical patterns and current market volatility (likely driven by refinery outages and high crude prices). **Immediate model retraining/re-weighting of "Refinery Outage" and "Summer Blend" features is recommended.**