# Escanaba Fuel Market Intelligence Report
**Date:** 2026-09-08 | **Location:** Escanaba, MI (ZIP 49829)

## Daily Market Summary (Escanaba ZIP 49829)
The local retail cluster shows a high variance in pricing across the four active stations, driven by regional logistics and specific brand positioning.

*   **Average Local Price:** $4.175 (Target: $4.15)
*   **Price Spread:** $0.42 (High variance between Kwik Trip and Krist)
*   **Active Stations:** 4
*   **Price Range:** $3.97 – $4.39
*   **Inventory Note:** Outlier detected at 501 N Lincoln Rd ($4.39), exceeding the target retail average by $0.24.

## Key Macro & Regional Indicators
The following factors are influencing the current price floor and regional volatility:

*   **Crude Dynamics:** WTI is trading at **$94.41/bbl**; Brent at **$99.55/bbl**. High crude prices are exerting upward pressure on local retail.
*   **Supply Constraints:** A significant refinery outage in California (Torrance) is impacting broader distribution networks, potentially tightening regional availability.
*   **Seasonal Factors:** Summer blend mandates remain **Active**, adding a **+$0.15** cost premium.
*   **Taxation & Logistics:** 
    *   Michigan Excise Tax: $0.309
    *   Estimated Total Tax Floor: $0.5133
    *   Chicago Spot Market: $3.0966 (Wholesale base)
*   **Regional Infrastructure:** Feed from Green Bay terminals remains a critical node for local supply consistency.

## Model Performance & Margin Telemetry
**System Status: ⚠️ ALERT - MODEL DRIFT DETECTED**

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.0609 | Stable |
| **RMSE** | $0.0887 | Stable |
| **R² Score** | -1.7857 | **CRITICAL FAILURE** |
| **Gross Margin (Actual)** | $1.0534 | High |
| **Gross Margin (Historical)** | $0.7407 | Baseline |
| **Margin Drift** | +$0.3127 | **ALERT TRIGGERED** |

**Analyst Notes:** 
The negative R² score indicates the current `HistGradientBoostingRegressor` model is failing to capture the underlying trend of the data effectively. This, coupled with a **$0.31 drift in margins**, suggests a fundamental shift in market dynamics or a requirement for model retraining/re-calibration to account for the current crude-to-retail pipeline.