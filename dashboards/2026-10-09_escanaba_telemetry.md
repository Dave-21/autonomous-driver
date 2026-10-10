# Daily Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** 2026-10-09

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.35
*   **Current Cluster Performance:**
    *   **Low:** $4.33 (Krist)
    *   **High:** $4.39 (Kwik Trip)
    *   **Price Spread:** $0.06 (Highly competitive local environment)
*   **Station Count:** 4 active stations in the Lincoln Rd cluster.
*   **Actionable Insight:** Price consistency is high across the cluster; however, the Kwik Trip location is currently positioned at a $0.06 premium above the neighborhood average.

## Key Macro & Regional Indicators
*   **Global Crude Context:** WTI is trading at $91.66/bbl; Brent at $104.43/bbl.
*   **Refinery Supply Chain:** 
    *   **High Risk:** Maintenance in PADD 2 (Great Lakes region) is active. This seasonally reduces supply and may exert upward pressure on Midwest regional prices.
    *   **Mitigant:** Summer blend mandate is currently **inactive**, removing the $0.00 premium normally seen in warmer months.
*   **Local Logistics:** 
    *   **Whiting Refinery:** Stable capacity (435k bpd) remains a critical anchor for the region.
    *   **Chicago Spot Market:** RBOB is holding at $3.1361/gal.
*   **Taxation Layer:** Michigan excise and state taxes are contributing a ~0.5157 floor to the retail price.

## Model Performance & Margin Telemetry
*   **Accuracy Metrics:**
    *   **MAE:** 0.4237
    *   **RMSE:** 0.4625
*   **Model Health Alert:** 
    *   **R² Score:** -8.0101 (Critical Failure)
    *   **Margin Drift:** $0.3708 (ALERT: TRUE)
*   **MLOps Note:** The negative R² score and significant margin drift indicate the model is currently struggling to correlate macro factors with local pricing accurately. A manual review of the `PassThrough_HistGradientBoosting` weights is recommended to account for the PADD 2 refinery maintenance impact.