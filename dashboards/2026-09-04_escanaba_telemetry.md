# Market Intelligence Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-04 | **Status:** Active Monitoring

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local retail cluster shows a tiered pricing structure with a notable variance in premium positioning.

*   **Cluster Stats:** 4 Active Stations | **Target Retail Avg:** $4.025
*   **Price Spread:** $0.22
*   **Station Breakdown:**
    *   **Value Tier:** $3.97 (Krist, Holiday) - *Primary volume drivers.*
    *   **Premium Tier:** $4.19 (Kwik Trip) - *Outlier in local cluster.*
*   **Traffic Impact:** High demand signaled by a **1.25 Traffic Index** on the US-2/US-41 corridor.

## 2. Key Macro & Regional Indicators
Analysis of supply chain, regional logistics, and policy impacts.

*   **Refinery Dynamics:** U.S. refineries are operating at high capacity (**97%**). While current supply is stable, upcoming maintenance schedules and global conflict-related shortages are exerting upward pressure on regional prices.
*   **Midwest Logistics:** The **Whiting Refinery** remains a critical anchor for the Midwest, currently providing a stable primary source for the region.
*   **Policy & Tributes:** The **Summer Blend Mandate** is active, adding a calculated **$0.15 premium** to the baseline.
*   **Local Tax Environment:** Michigan excise taxes ($0.309) and the total tax floor ($0.5199) provide a consistent baseline for local retail calculations.
*   **Inbound Supply:** The **Green Bay Terminal** continues to serve as a primary distribution hub; its connectivity to regional markets remains a stabilizing factor for local inventory.

## 3. Model Performance & Margin Telemetry
MLOps performance audit of the `HistGradientBoostingRegressor` model.

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.2793 | Stable |
| **RMSE** | $0.2798 | Stable |
| **R² Score** | **-253.0595** | ⚠️ **CRITICAL ALERT** |
| **Current Gross Margin** | $0.819 | Healthy |
| **Margin Drift** | +$0.0941 | No Alert |

**MLOps Action Items:**
*   **Model Degradation:** The negative **R² Score** indicates a significant failure in the model's ability to explain variance (likely due to extreme outliers or a non-linear trend mismatch).
*   **Recommendation:** Immediate retraining of the `HistGradientBoostingRegressor` is required to address the negative R² before the next production cycle.
*   **Profitability:** Despite model instability, current margins remain **9.4% above** historical averages ($0.7249).