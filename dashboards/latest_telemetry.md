# Energy Market Analysis Dashboard: Escanaba, MI (ZIP 49829)
**Report Date:** 2026-08-26 | **Status:** ⚠️ DRIFT ALERT ACTIVE

## 1. Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.08 / gal
*   **Local Price Variance:** $0.04 (Tight spread indicating high local competition)
*   **Active Cluster:** 4 Stations (Kwik Trip, Krist, Holiday)
*   **Local Dynamics:** 
    *   The retail cluster is maintaining a consistent price floor of $4.05 at select locations, while the majority of the cluster is hovering at $4.09.
    *   **Traffic Impact:** The US-2/US-41 traffic index is elevated at **1.15**, suggesting high regional demand and potential logistical pressure on local distribution.

## 2. Key Macro & Regional Indicators
*   **Global Crude Context:** WTI at **$81.64** and Brent at **$86.40** provide a steady but volatile baseline for upstream costs.
*   **Refining Constraints:** 
    *   **High Utilization:** US refiners are operating at >95% capacity; high utilization and deferred maintenance are creating a "fragile" supply chain.
    *   **Regional Risk:** Specific outages in California and potential disruptions from Middle Eastern tensions are tightening the supply of gasoline and distillate.
*   **Mandates & Taxes:**
    *   **Summer Blend:** Active ($0.15 premium) is currently factored into retail pricing.
    *   **Michigan Tax Floor:** $0.5022 (including $0.309 excise tax) represents a significant fixed cost component.
*   **Midwest Logistics:** The Whiting Refinery remains a critical high-capacity hub, though the "fragile" status of global refining suggests localized bottlenecks may occur.

## 3. Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Core Metrics:**
    *   **MAE/RMSE:** 0.6193 / 0.6194 (Current error margin is stable)
    *   **R² Score:** **-2505.63** 🚨 *Critical Alert: The negative R² suggests the model is failing to capture the underlying variance of the current data trend.*
*   **Margin Analysis:**
    *   **Current Margin:** $1.1684
    *   **Historical Average:** $0.6377
    *   **Margin Drift:** +$0.5307 (**Alert Triggered**)
*   **Actionable Insight:** The significant margin drift and catastrophic R² score indicate that current market volatility (likely driven by refinery capacity issues and regional supply constraints) is outperforming the current model's predictive capabilities. **Immediate retraining or feature engineering on refinery capacity inputs is recommended.**