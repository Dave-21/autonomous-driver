# Daily Market Analysis: Escanaba, MI (ZIP 49829)
**Date:** 2026-08-29 | **Status:** Active Monitoring

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Current Cluster Status:** 4 active stations identified in the local cluster.
*   **Retail Price Range:** $3.99 – $4.03 USD.
*   **Target Retail Average:** $4.005 (Current deviation: ±$0.015).
*   **Local Spread:** $0.04 variance between top and bottom performers.
*   **Traffic Impact:** High volume indicator (1.44) on US-2/US-41 corridor suggests high local demand.

## 2. Key Macro & Regional Indicators
*   **Global Crude:** WTI at $83.53 / Brent at $89.70.
*   **Regional Logistics:** 
    *   **Whiting Refinery:** Active status monitored; historical hub for regional supply.
    *   **Green Bay Terminals:** Infrastructure confirmed via West Shore Pipeline connectivity.
*   **Regulatory & Seasonality:**
    *   **Summer Blend:** **ACTIVE** (+ $0.15 premium applied).
    *   **State Taxation:** Michigan excise tax ($0.309) + fees totaling ~$0.5306.
*   **Wholesale Basis:** Chicago Spot (RBOB) currently trading at $3.3842.

## 3. Model Performance & Margin Telemetry
*   **Model Type:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:**
    *   **MAE:** $0.468
    *   **RMSE:** $0.4689
    *   **R² Score:** -263.974 (⚠️ **Alert:** Extremely low R² indicates high variance or model instability relative to current features).
*   **Margin Analysis:**
    *   **Current Gross Margin:** $0.6208
    *   **Historical Average:** $0.6890
    *   **Margin Drift:** -0.0682 (Trending downward, but below critical alert threshold).
*   **MLOps Note:** The negative R² score suggests the model is struggling to capture the current volatility in the Escanaba cluster. Recommend a hyperparameter re-tuning or feature engineering on the "Summer Blend" and "Refinery Outage" impact weights.