# Escanaba Fuel Market Intelligence Dashboard
**Date:** October 14, 2026 | **Location:** Escanaba, MI (ZIP 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.365 /gal
*   **Current Market Range:** $4.29 – $4.49
*   **Active Station Count:** 4
*   **Average Local Price:** ~$4.37
*   **Market Sentiment:** The retail cluster is currently tracking closely to the target average. However, a variance of $0.20 exists between the lowest (Krist) and highest (Kwik Trip) branded outlets, indicating localized competition is still influencing price floors.

## 2. Key Macro & Regional Indicators
*   **Global Crude Context:** 
    *   **WTI:** $94.01 /bbl | **Brent:** $104.43 /bbl
*   **Refining & Supply:** 
    *   **Utilization:** 92.7% (Stable, but approaching capacity constraints).
    *   **Impact:** Maintenance deferrals into 2027 suggest a tightened supply environment for 2026, potentially supporting higher floor prices in the Midwest.
*   **Regional Infrastructure:** 
    *   **Whiting Refinery:** Remains a vital anchor for Midwest transit fuels.
    *   **Logistics:** Green Bay terminal access remains stable for local distribution.
*   **Regulatory:** Summer Blend mandate is **Inactive**, removing the current seasonal premium.

## 3. Model Performance & Margin Telemetry
*   **Model Status:** `⚠️ ALERT: DRIFT DETECTED`
*   **Margin Analytics:**
    *   **Current Gross Margin:** $1.2731
    *   **Historical Average:** $0.8644
    *   **Margin Delta:** +$0.4087 (Significant upward drift)
*   **Predictive Accuracy:**
    *   **MAE:** $0.1996 | **RMSE:** $0.2091
    *   **R² Score:** -1.1767
*   **Actionable MLOps Note:** The negative $R^2$ score combined with the `drift_alert_flag` indicates the `PassThrough_HistGradientBoosting` model is failing to capture current market volatility. **Immediate retraining or hyperparameter recalibration is required** to align with the current $0.40+ margin deviation.