# Executive Fuel Market Dashboard: Escanaba, MI (49829)
**Date:** 2026-08-11 | **Status:** Active Monitoring

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 / gal
*   **Primary Drivers:** Current pricing reflects a combination of the active Summer Blend mandate ($0.15 premium) and standard Michigan tax floors (~$0.516).
*   **Local Logistics:** The US-2/US-41 corridor shows an elevated traffic index (1.15), potentially impacting local delivery cycles.

## Key Macro & Regional Indicators
*   **Global Crude Benchmarks:** 
    *   WTI: $82.13/bbl | Brent: $87.72/bbl
*   **Refinery Capacity Risk:** High. Reports indicate significant deferred maintenance at major facilities (e.g., Port Arthur) to maintain volume, creating potential volatility in the midstream supply chain.
*   **Midwest Regional Stability:** The Whiting Refinery remains a critical hub for regional throughput; however, ongoing demand and local terminal dynamics in Green Bay continue to influence multi-state pricing baselines.
*   **Regulatory Impact:** Summer Blend mandates remain **Active**, contributing a $0.15 cost pressure on the wholesale floor.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Accuracy Metrics:** 
    *   **MAE:** $0.023 (Stable)
    *   **RMSE:** $0.0354 (Low variance)
    *   **$R^2$ Score:** -0.0012 (Note: Low correlation suggests high localized noise or price volatility in the current trading window).
*   **Margin Analytics:** 
    *   **Current Gross Margin:** $0.3546
    *   **Historical Average:** $0.3595
    *   **Margin Drift:** -0.0049 (Status: **No Alert**)

**Actionable Insight:** While accuracy metrics (MAE/RMSE) remain tight, the near-zero $R^2$ score suggests the model is struggling to find a strong correlation between the current feature set and target prices in the Escanaba cluster. Monitor "Refinery Outage" sentiment scores for sudden price spikes.