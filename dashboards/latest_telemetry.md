# Escanaba Market Intelligence Report | 2026-08-24

## Daily Market Summary (Escanaba ZIP 49829)
**Current Status:** Stable Localized Pricing | **Cluster Size:** 4 Active Stations
*   **Retail Snapshot:** The local cluster exhibits a tight price spread of **$0.02**, with pricing anchored at **$4.11** (Kwik Trip, Krist) and a slight premium of **$4.13** (Holiday).
*   **Target Alignment:** Actual prices are performing near the target average of **$4.115**. 
*   **Local Dynamics:** The "Lincoln Rd" corridor shows high competition; with three stations priced at $4.11, price sensitivity is high and brand loyalty is secondary to proximity.

## Key Macro & Regional Indicators
*   **Crude Market Sentiment:** WTI sits at **$85.38/bbl**, while Brent holds at **$92.38/bbl**. High crude values are being compounded by refinery supply constraints.
*   **Supply Constraints (High Risk):** 
    *   **Refinery Outages:** Significant volume risks identified in the Gulf (Motiva Port Arthur) and structural risks from Russian infrastructure impacts. Expected outages rising to ~9.0 Mbd in October.
    *   **Regional Hubs:** The Whiting Refinery remains a critical Midwest stabilizer, but its capacity is under pressure from these downstream constraints.
*   **Regulatory & Logistics Impact:** 
    *   **Summer Blend Mandate:** **ACTIVE** (Est. Premium: +$0.15).
    *   **Taxation Floor:** Michigan state/local taxes are estimated at **$0.5068**.
    *   **Wholesale Gap:** Current RBOB wholesale of **$2.9876** against the retail price suggests a compressed margin, heavily squeezed by summer blends and tax overhead.

## Model Performance & Margin Telemetry
*   **Prediction Accuracy:** 
    *   **MAE:** $0.2092 | **RMSE:** $0.3623.
    *   **R² Score:** -0.5 (Warning: Current model features are failing to explain variance in local volatility; retraining recommended).
*   **Margin Drift Alert:** ⚠️ **CRITICAL ALERT**
    *   **Current Gross Margin:** $1.1274
    *   **Historical Average:** $0.5456
    *   **Delta:** +$0.5817 (Significant Deviation)
*   **Analyst Note:** The high margin drift and negative R² suggest that the current model is struggling with extreme volatility in refinery availability and federal mandates. Immediate recalibration of weightings for `factor_2` (Outages) and `factor_3` (Summer Blend) is advised to stabilize forecast accuracy.