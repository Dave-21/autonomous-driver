# Executive Market Intelligence Report: Escanaba, MI (ZIP 49829)
**Date:** 2026-10-04 | **Status:** ⚠️ **Margin Drift Alert**

## 1. Daily Market Summary (Escanaba ZIP 49829)
The local market reflects a steady retail environment with a target average of **$4.46**. 

*   **Target Retail Average:** $4.457
*   **Local Price Spread:** $0.08
*   **Active Retailer Pricing:**
    *   **Kwik Trip (501 N Lincoln Rd):** $4.43
    *   **Holiday (700 N Lincoln Rd):** $4.43
    *   **Krist (102 N Lincoln Rd):** $4.51
*   **Market Observation:** Prices are currently hovering near the target average, with Kwik Trip and Holiday providing the lower-bound entry points for the cluster.

## 2. Key Macro & Regional Indicators
*   **Crude & Commodity Feed:** 
    *   **WTI:** $91.11/bbl | **Brent:** $102.25/bbl
    *   **Chicago RBOB Spot:** $3.3124/gal
*   **Supply Chain Risks:**
    *   **Refinery Outages:** High activity in California (Torrance) and heightened Midwest outage levels (exceeding 10-year averages). 
    *   **Regional Stability:** The Whiting Refinery remains a critical high-volume hub for the Midwest, providing significant buffer for regional demand.
*   **Regulatory/Seasonal:** 
    *   **Summer Blend:** Inactive (No cost premium).
    *   **MI Tax Burden:** $0.5263 total estimated tax floor.

## 3. Model Performance & Margin Telemetry
The current `PassThrough_HistGradientBoosting` model indicates a significant divergence in operational margins.

| Metric | Value | Status |
| :--- | :--- | :--- |
| **MAE (Mean Absolute Error)** | 0.4312 | Stable |
| **RMSE** | 0.474 | Stable |
| **R² Score** | -8.6825 | Poor Fit |
| **Gross Margin (Current)** | $1.1446 | ⚠️ **High** |
| **Historical Margin Avg** | $0.8307 | Baseline |
| **Margin Drift** | **+0.3139** | 🚨 **Alert Triggered** |

**Analyst Note:** The `drift_alert_flag` is active due to a **37.7% increase** over the historical average margin. While higher margins may seem positive, the high variance and negative R² suggest the model is struggling to reconcile current price volatility with historical patterns. Immediate review of local procurement costs vs. spot market shifts is recommended.