# Market Analysis Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-09-02 | **Status:** Alert Active

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Retail Price:** $3.97 (Uniform across all active nodes)
*   **Local Cluster Health:** 100% Price Sync (0.00 USD spread across 4 stations)
*   **Active Stations:** 4 (Kwik Trip, Krist, Holiday)
*   **Logistics Hub:** Stable; Green Bay terminals confirmed as viable supply routes for regional distribution.

## 2. Key Macro & Regional Indicators
*   **Crude Oil Market:** WTI ($91.15) and Brent ($95.64) indicate a high-cost baseline for upstream procurement.
*   **Supply Constraints:** 
    *   **Regional:** Torrance (CA) refinery outages are creating upstream volatility for gasoline/distillate.
    *   **Local:** Whiting Refinery (Midwest) remains a high-capacity anchor ($440k bpd capacity) providing stability for local Midwest supply.
*   **Regulatory & Logistics:**
    *   **Summer Blend:** Active (+ $0.15 premium impact).
    *   **Taxation:** Michigan tax floor ($0.5139) contributes significantly to the regional price floor.
*   **Spot Market:** Chicago RBOB Wholesale currently at $3.1053.

## 3. Model Performance & Margin Telemetry
| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.2864 | Stable |
| **RMSE** | $0.2867 | Stable |
| **R² Score** | -483.633 | **CRITICAL FAILURE** |
| **Gross Margin (Latest)** | $0.8647 | **ALERT** |
| **Margin Drift** | +$0.1438 | **ALERT** |

**MLOps Action Items:**
*   **Critical Alert:** The $R^2$ score of -483.633 indicates a complete model breakdown; the model is performing significantly worse than a horizontal baseline. Immediate retraining or feature re-weighting is required.
*   **Drift Detected:** Margin drift of +$0.1438 over the historical average ($0.7209) suggests a decoupling between procurement costs and retail pricing models. Investigation into "Summer Blend" impact vs. local "Whiting" supply stability is recommended.