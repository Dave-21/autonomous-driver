# Daily Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** 2026-10-21 | **Status:** ⚠️ Margin Drift Alert

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local cluster shows high price homogeneity with a very tight spread of **$0.01** across active stations. 

*   **Target Retail Average:** $4.195/gal
*   **Active Station Count:** 4
*   **Primary Retailers:** Kwik Trip, Krist, Holiday
*   **Price Stability:** High. Local competition is currently uniform, suggesting a stable regional floor.

## 2. Key Macro & Regional Indicators
*   **Global Crude Trends:** 
    *   **WTI:** $97.71/bbl
    *   **Brent:** $109.73/bbl
*   **Refinery Infrastructure:** The **Whiting Refinery** remains a critical high-capacity asset (435k bpd) for the Great Lakes region. 
*   **Seasonal Factors:** Summer blend mandates are **Inactive**. The lack of a summer blend premium ($0.00) provides a tailwind for regional margins.
*   **Logistics Hubs:** Connectivity to the **Green Bay Terminals** remains stable, providing robust supply lines for Michigan and Wisconsin distribution.

## 3. Model Performance & Margin Telemetry
The model is currently flagging a significant deviation in operational margins.

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | $0.0787 | Stable |
| **RMSE (Root Mean Square Error)** | $0.0948 | Stable |
| **R² Score** | 0.1742 | **Low** (High Volatility) |

**Critical Alert: Margin Drift Detected**
*   **Current Gross Margin:** $1.1446
*   **Historical Average:** $0.8822
*   **Margin Drift:** +$0.2624
*   **Action Required:** The `drift_alert_flag` is **TRUE**. The jump in gross margin suggests a decoupling from historical norms—investigate whether this is due to sudden local supply constraints or an unexpected drop in procurement costs relative to retail prices.