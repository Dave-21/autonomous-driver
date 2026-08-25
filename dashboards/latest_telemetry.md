# Escanaba Fuel Market Intelligence Report
**Date:** 2026-08-25 | **Location:** Escanaba, MI (Zip: 49829)

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.11/gal
*   **Active Cluster Status:** Stable. Current pricing at primary nodes (Kwik Trip, Krist) aligns with the target average of **$4.11**.
*   **Local Inventory Note:** High local demand concentrated along the Lincoln Rd corridor; active price spread is currently 0.00, indicating uniform pricing across the immediate cluster.

## Key Macro & Regional Indicators
*   **Crude & Spot Markets:** WTI holds at **$81.01/bbl** with Brent at **$85.86**. The RBOB Chicago spot market is currently at **$2.8935/gal**.
*   **Refinery Health & Supply Chain:** 
    *   **Whiting Refinery:** Remains a critical Midwest anchor; infrastructure remains stable but is noted for high-impact utilization rates ahead of the 2026 maintenance cycle.
    *   **Summer Blend Mandate:** **ACTIVE** (+ $0.15 premium).
*   **Logistics & Taxation:** Michigan tax floor ($0.50) and a regional traffic index (1.15) are factored into localer transport costs from the Green Bay terminal hub.

## Model Performance & Margin Telemetry
*   **Prediction Accuracy:** 
    *   MAE: $0.52 | RMSE: $0.57
    *   **Critical Alert:** The **R² Score of -4.99** indicates a significant model divergence; the current regression is failing to capture local volatility effectively.
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.2165 
    *   **Historical Average:** $0.5991
    *   **Drift Alert: [ACTIVE]** The margin drift of **+0.6174** signifies a significant deviation from standard operational margins, likely driven by regional supply constraints or logistical premiums.

**Action Items:** 
1. Re-calibrate the `HistGradientBoostingRegressor` to address the negative R² score.
2. Investigate the source of the $0.61 margin drift in the Delta County region to determine if it is a transient logistics spike or a structural shift.