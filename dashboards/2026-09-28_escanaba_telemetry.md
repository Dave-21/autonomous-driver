# 📊 Escanaba Fuel Market Intelligence Dashboard
**Date:** 2026-09-28 | **Region:** Delta County, MI (49829)

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.535
*   **Live Cluster Snapshot:**
    *   **Current Range:** $4.52 – $4.54
    *   **Local Price Spread:** $0.02 (Tight competition)
    *   **Active Stations:** 4
*   **Actionable Insight:** Prices are stabilized within a narrow band; local competition is high, resulting in minimal variance between neighboring stations (Kwik Trip, Krist, Holiday).

## 2. Key Macro & Regional Indicators
*   **Global Crude Context:** 
    *   WTI: $93.95/bbl | Brent: $99.48/bbl
*   **Refinery Supply Pressure:** 
    *   **Critical Risk:** U.S. refineries are experiencing significant volume reductions (450k bpd) due to the maintenance season. 
    *   **Regional Impact:** The **Whiting Refinery** remains a critical hub for the Midwest; however, global capacity losses and domestic maintenance are tightening the supply margin.
*   **Logistics & Infrastructure:**
    *   **Green Bay Terminals:** Active and providing competitive pricing via Sunoco LP.
    *   **Traffic Influence:** US-2/US-41 traffic index remains stable at 1.0.
    *   **Regulatory:** Summer blend mandates are currently inactive (no additional premium).

## 3. Model Performance & Margin Telemetry
*   **Model Status:** `PassThrough_HistGradientBoosting`
*   **Accuracy Metrics:**
    *   **MAE:** $0.4007
    *   **RMSE:** $0.4813
    *   **R² Score:** -3.3874 (**CRITICAL ALERT**)
*   **Margin Drift Analysis:**
    *   **Current Margin:** $1.363
    *   **Historical Avg:** $0.7946
    *   **Drift Delta:** +$0.5684
    *   **Alert Status:** ⚠️ **DRIFT_ALERT_FLAG_TRUE**

**MLOps Note:** The negative R² score and high margin drift indicate that the model is currently struggling to generalize against recent volatility. Investigation into the `HistGradientBoosting` weights is recommended to address the performance degradation caused by refinery maintenance fluctuations.