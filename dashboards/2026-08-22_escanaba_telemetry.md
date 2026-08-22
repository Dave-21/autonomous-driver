# Daily Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** August 22, 2026 | **Status:** Alert Issued

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 / gal
*   **Regional Spot Price (RBOB):** $3.35 / gal
*   **Estimated Tax Floor:** $0.53 / gal
*   **Market Dynamics:** Current retail pricing in the Lincoln Rd cluster is facing compression. While the Chicago spot market remains stable, local factors including a **$0.15 summer blend premium** and ongoing refinery maintenance are creating upward pressure on upstream costs that may not be fully captured by current regional competition.

## Key Macro & Regional Indicators
*   **Global Crude Benchmarks:** 
    *   WTI: $87.06/bbl | Brent: $94.39/bbl
*   **Supply Constraints:** Significant risk identified due to maintenance shutdowns at the **Motiva Port Arthur** and **Marathon Galveston Bay** refineries (approx. 1M bpd capacity reduction).
*   **Regional Infrastructure:** 
    *   **Whiting Refinery:** Confirmed as a critical Midwest hub; stability here is vital for local supply chains.
    *   **Green Bay Terminals:** Active logistics monitoring continues to stabilize regional flows from the Wisconsin corridor.
*   **Demand Proxy:** The **US-2/US-41 Traffic Index (1.44)** indicates elevated local vehicle activity, supporting consistent volume despite price volatility.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   $R^2$: 1.0 | MAE: 0.0 | RMSE: 0.0 (High confidence in point-estimate accuracy).
*   **⚠️ ALERT: Margin Drift Detected**
    *   **Current Gross Margin:** $0.1421
    *   **Historical Average:** $0.5193
    *   **Margin Variance:** **-0.3772** (Significant Deviation)
*   **Actionable Insight:** The `drift_alert_flag` is **TRUE**. The sharp decline in gross margin suggests a significant misalignment between procurement costs and local retail pricing, or an aggressive localized price war in the Escanaba cluster. Immediate review of logistics overheads vs. regional competition is recommended.