# Market Intelligence Report: Escanaba (ZIP 49829)
**Date:** 2026-08-11 | **Status:** Active Monitoring

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Price:** $3.49 / gal
*   **Regional Demand Factor:** 1.15 (Traffic Index Adjustment)
*   **Regulatory Load:** Summer Blend Mandate is **ACTIVE**, contributing a +$0.15 premium to regional pricing.
*   **Taxation Impact:** Michigan State tax floor stands at $0.501, with specific excise taxes contributing an additional $0.309 to the local cost basis.

## Key Macro & Regional Indicators
*   **Global Crude Baseline:** WTI trading at **$83.23/bbl**; Brent at **$88.95/bbl**.
*   **Supply Chain Risks:** 
    *   **Refinery Infrastructure:** Ongoing monitoring of Whiting Refinery (IL) and regional Green Bay terminals indicates high sensitivity to Midwest supply chain stability.
    *   **Outage Impacts:** Historical patterns suggest potential volatility during scheduled refinery turnarounds; current data suggests a stable but monitored capacity profile.
*   **Spot Market Dynamics:** Chicago RBOB Spot is currently **$2.8915/gal**, providing the base for regional retail calculations.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE:** $0.0067 | **RMSE:** $0.0068 (High precision in point estimation)
    *   **R² Score:** **-3.282** (**CRITICAL ALERT**: Negative R² indicates the model is failing to capture variance or that current features are poorly correlated with target price volatility. Investigation into feature engineering required.)
*   **Margin Analysis:** 
    *   **Current Gross Margin:** $0.5985
    *   **Historical Avg:** $0.5838
    *   **Delta:** +$0.0147 (Upward trend)
    *   **Drift Status:** `False` (No immediate action required, but variance is increasing).