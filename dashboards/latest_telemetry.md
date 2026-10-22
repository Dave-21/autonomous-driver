# 📊 Escanaba Fuel Market Intelligence Report
**Date:** 2026-10-22 | **Location:** Escanaba, MI (Zip: 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Average Retail:** $4.5675 (Target: $4.565)
*   **Market Spread:** $0.10 USD
*   **Cluster Density:** 4 active stations within the primary retail zone.
*   **Price Points:**
    *   **Premium/Standard:** $4.59 (Kwik Trip, Krist, Holiday)
    *   **Competitive Entry:** $4.49 (Krist - 6344 US-2-41 MI-35)
*   **Actionable Insight:** Retail prices are currently tracking accurately against target benchmarks; however, the $0.10 spread indicates a tight competitive window among local vendors.

## 2. Key Macro & Regional Indicators
*   **Global Crude Dynamics:**
    *   **WTI:** $99.07/bbl | **Brent:** $112.79/bbl
    *   *Observation:* High global crude prices are exerting upward pressure on regional margins.
*   **Refinery & Supply Chain:**
    *   **Whiting Refinery:** Status stable; remains a critical high-capacity hub for Midwest transit (Detroit/Chicago).
    *   **West Coast Influence:** California refinery outages are currently localized; no immediate impact on Midwest infrastructure.
*   **Seasonal/Regulatory:**
    *   **Summer Blend:** Inactive (No premium applied).
    *   **Taxes:** Michigan Excise Tax ($0.309) + Estimated Floor ($0.5122) are factored into retail pricing.
*   **Logistics:** Green Bay terminals remain a stable hub for regional distribution with consistent access for heavy-duty and fleet accounts.

## 3. Model Performance & Margin Telemetry
*   **Prediction Accuracy:**
    *   **MAE:** $0.0905 | **RMSE:** $0.1135
    *   **R² Score:** -0.0107 (Indicates high volatility or noise in the PassThrough_HistGradientBoosting model).
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.4868
    *   **Historical Avg Margin:** $0.8901
    *   **Margin Drift:** +$0.5967
*   **🚨 Alert Status:** **DRIFT_ALERT_FLAG: TRUE**
*   **Technical Note:** The significant margin drift indicates a disconnect between wholesale costs and retail behavior. The model is flagging a high-volatility period—likely due to the price gap between the Chicago Spot ($3.078) and the local retail environment. Immediate retraining or parameter adjustment on the "PassThrough" logic is recommended.