# Market Intelligence Dashboard | Escanaba, MI (49829)
**Date:** 2026-08-13 | **Status:** Monitoring Active

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $3.49 / gal
*   **Regional Outlook:** Stable but sensitive to mid-stream supply constraints.
*   **Primary Drivers:** High global crude pricing ($82.90 WTI) and the active Summer Blend Mandate (+0.15 USD premium) are currently underpinning local retail prices. 
*   **Logistics Note:** Local infrastructure remains anchored by the Whiting refinery hub and Green Bay terminal dynamics, which serve as critical buffers for Midwest fuel flow.

## 2. Key Macro & Regional Indicators
| Factor | Status/Value | Analysis |
| :--- | :--- | :--- |
| **Global Crude (WTI/Brent)** | $82.90 / $88.75 | Elevated global prices exerting upward pressure on spot markets. |
| **Refinery Capacity** | ⚠️ High Risk | Deferred maintenance at major refineries (e.g., Motiva) is tightening supply downstream. |
| **Summer Blend Mandate** | **Active** | Mandatory +$0.15 cost premium remains in effect for the season. |
| **Chicago Spot (RBOB)** | $2.8907 / gal | Regional benchmark indicates a moderate spread between wholesale and retail. |
| **Traffic Index (US-2/41)** | 1.15 | Elevated local traffic volume suggests high demand in the Escanaba corridor. |

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE / RMSE:** $0.0071 (High precision tracking)
    *   **R² Score:** 0.0 (Note: High accuracy but low variance explanation; monitor for overfitting).
*   **Margin Analytics:**
    *   **Current Gross Margin:** $0.5993
    *   **Historical Average:** $0.5857
    *   **Margin Drift:** +$0.0136 (Positive trend)
    *   **Alert Status:** ✅ **Stable** (No drift alerts triggered).

**Actionable Insight:** While current margins are slightly outperforming historical averages, the tightening of refinery capacity in the Gulf and Midwest suggests potential volatility if supply delays escalate over the next 30 days.