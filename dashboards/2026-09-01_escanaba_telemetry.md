# Executive Market Dashboard: Escanaba, MI Fuel Analysis
**Date:** 2026-09-01 | **Location:** Escanaba (ZIP 49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Retail Target:** $3.97
*   **Reporting Status:** 50% (2 of 4) stations reporting data.
*   **Local Price Consistency:** Stable at $3.97 where reported.
*   **Data Gaps:** "Krist" and "Holiday" stations are currently returning null values; manual verification may be required to determine if these are out-of-market or simply offline.

## 2. Key Macro & Regional Indicators
*   **Global Crude Baseline:** 
    *   WTI: $86.80 | Brent: $88.90
*   **Supply & Refinery Dynamics:** 
    *   **Outage Risk:** High. Reports indicate refineries are stretching capacity to avoid maintenance shutdowns; Motiva's postponement of the Port Arthur unit indicates a strategy to maximize volume.
    *   **Regulatory Load:** Summer Blend mandates are **ACTIVE**, adding an estimated **$0.15** premium to the base cost.
*   **Regional Logistics:**
    *   **Chicago Spot Market:** $3.1219/gal.
    *   **Midwest Transit:** Traffic index for US-2/US-41 is stable (1.0).
    *   **Taxation:** Total tax floor sits at **$0.5149** (inclusive of $0.309 excise).
*   **Strategic Insight:** The combination of active Summer Blend premiums and reported refinery capacity constraints suggests a tightened margin for error in local regional distribution.

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE:** $0.3742 | **RMSE:** $0.3766
    *   **R² Score:** -78.38 *(Warning: Negative R² indicates significant variance or model mismatch with current market conditions).*
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.8481
    *   **Historical Average:** $0.7079
    *   **Margin Drift:** +$0.1402
*   **⚠️ ALERT:** **Drift_Alert_Flag is TRUE.** The model is detecting significant deviation from historical norms. The current margin spike and poor R² score suggest heavy influence from volatile refinery outage variables or "Summer Blend" cost-push inflation. 

**Action Item:** Re-calibrate model weights on "Refinery Outage" and "Summer Blend" features to address the high drift and low R² score.