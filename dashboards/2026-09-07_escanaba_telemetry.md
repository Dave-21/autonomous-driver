# Market Analysis Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-07 | **Status:** ⚠️ Drift Alert Active

## Daily Market Summary (Escanaba ZIP 49829)
*   **Current Retail Landscape:** 4 active stations in the local cluster.
*   **Price Range:** $3.97 – $4.07 USD/gal.
*   **Target Retail Average:** $4.045.
*   **Price Spread:** $0.10 (indicates minor competition variance).
*   **Key Retailers:** Kwik Trip, Krist, and Holiday dominate the local cluster.

## Key Macro & Regional Indicators
*   **Crude Commodities:** 
    *   **WTI:** $92.38/bbl | **Brent:** $97.05/bbl (Strong upward pressure on downstream costs).
*   **Supply Dynamics:** 
    *   **Refinery Capacity:** US refineries operating at 97% capacity. 
    *   **Constraints:** Global conflict and scheduled maintenance are tightening the refined products market.
*   **Regional Infrastructure:** 
    *   **Whiting Refinery:** Currently serving as a critical Midwest hub (440k bpd capacity).
    *   **Midwest Logistics:** Green Bay terminals (Sunoco LP) provide the primary regional distribution backbone.
*   **Regulatory/Mandates:** 
    *   **Summer Blend:** Active (+0.15 USD estimate).
    *   **State Tax Floor:** Michigan excise tax of 0.309 (Total tax floor: 0.5089).
*   **Wholesale Index:** Chicago Spot Market (RBOB) is currently at $3.0232/gal.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** 0.0431
    *   **RMSE:** 0.0540
*   **Critical Alert:** **R² Score: -2.2635** 
    *   *Note: A negative R² indicates the model's predictions are performing significantly worse than a simple horizontal mean. Immediate retraining or feature re-engineering is required.*
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.0218
    *   **Historical Average:** $0.7345
    *   **Margin Drift:** +0.2873 (**ALERT_FLAG: TRUE**)
    *   *Action: Drift detection indicates a significant decoupling between wholesale costs and retail pricing, likely caused by local supply constraints or specific regional premiums.*