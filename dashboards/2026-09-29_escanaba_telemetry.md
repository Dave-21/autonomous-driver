# Executive Market Dashboard: Escanaba, MI (Zip 49829)
**Date:** 2026-09-29 | **Status:** ⚠️ DRIFT ALERT DETECTED

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Retail Price:** $4.52
*   **Local Price Variance:** $0.00 (Unified pricing across all tracked stations)
*   **Active Clusters:** 4 stations (Kwik Trip, Krist, Holiday)
*   **Market Sentiment:** High stability in local retail pricing despite macro fluctuations.

## 2. Key Macro & Regional Indicators
*   **Crude Oil Foundation:** 
    *   WTI: $89.58 | Brent: $96.35
*   **Supply Chain Logistics:**
    *   **Midwest Refinery Status:** High risk. Current outages in the Midwest are exceeding 10-year averages, potentially tightening regional supply.
    *   **Whiting Refinery:** Maintaining high output (400k+ bpd), providing a critical buffer for the Chicago/Detroit corridor.
*   **Regulatory/Seasonality:**
    *   **Summer Blend:** Inactive (No premium cost currently applied).
    *   **Taxation:** Michigan excise tax $0.309 (Total floor: $0.5148).
*   **Wholesale Context:** Chicago RBOB spot price is currently $3.1218.

## 3. Model Performance & Margin Telemetry
*   **Model Status:** 🚨 **CRITICAL ALERT**
*   **Margin Analysis:**
    *   **Current Margin:** $1.3982
    *   **Historical Average:** $0.8046
    *   **Margin Drift:** +$0.5936 (Significant upward variance)
*   **Model Accuracy Metrics:**
    *   **MAE:** $0.4464
    *   **RMSE:** $0.5069
    *   **R² Score:** -4.5686 (⚠️ **Failure State**: Negative R² indicates the model is performing worse than a horizontal mean; immediate retraining or data pipeline audit required).

**Action Items:**
1.  **Investigate Drift:** Investigate the source of the $0.59 margin jump.
2.  **Model Recalibration:** The negative R² score indicates a significant breakdown in the `PassThrough_HistGradientBoosting` logic; review features related to Midwest refinery outages.
3.  **Supply Monitoring:** Monitor local inventory closely due to elevated Midwest refinery outage risks.