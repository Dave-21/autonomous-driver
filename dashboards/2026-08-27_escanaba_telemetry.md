# Escanaba, MI Fuel Market Intelligence Report
**Date:** 2026-08-27 | **Location:** Escanaba (ZIP 49829)

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $4.062
*   **Active Local Cluster:** 4 Stations (Kwik Trip, Krist, Holiday)
*   **Local Price Spread:** $0.04 (High competition, low variance)
*   **Retail Floor:** $4.05 (Kwik Trip, Holiday)
*   **Premium Retail:** $4.09 (Krist)
*   **Market Sentiment:** Stable local pricing with minimal variance across the immediate 49829 corridor.

## Key Macro & Regional Indicators
*   **Global Crude Dynamics:** 
    *   WTI: $83.12/bbl | Brent: $88.21/bbl
*   **Refinery Outlook:** High-risk period identified for 2026 due to heavy maintenance schedules; anticipated supply tightness may impact downstream pricing.
*   **Seasonality:** Summer Blend Mandate is **ACTIVE** (+ $0.15 premium).
*   **Regional Supply Chain:**
    *   **Green Bay Hub:** Logistics remains stable; regional terminal infrastructure continues to support the Midwest corridor.
    *   **Traffic Impact:** US-2/US-41 Corridor Index is high (1.15), indicating elevated local demand/transportation activity.
*   **Wholesale Baseline:** RBOB spot market currently at $2.9802/gal.

## Model Performance & Margin Telemetry
*   **Model Status:** `HistGradientBoostingRegressor`
*   **Error Metrics:** MAE: $0.5314 | RMSE: $0.5317
*   **Confidence Alert:** **CRITICAL.** R² Score is -789.96. The model is currently experiencing extreme variance or is failing to correlate with input features.
*   **Margin Analysis:**
    *   **Current Gross Margin:** $1.0818
    *   **Historical Average:** $0.6809
    *   **Margin Drift:** +$0.4009
    *   **Alert Status:** ⚠️ **DRIFT_ALERT_ACTIVE**. Significant deviation from historical norms suggests sudden volatility in logistics costs or wholesale procurement premiums.