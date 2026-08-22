# Fuel Market Analysis: Escanaba, MI (Zip 49829)
**Date:** August 21, 2026

## Daily Market Summary (Escanaba ZIP 49829)
*   **Target Retail Average:** $3.49 / gal
*   **Regional Demand Indicator:** The US-2/US-41 traffic index is currently **1.44**, suggesting high localized transit volume and sustained demand for the Escanaba cluster.
*   **Seasonal Impact:** The Summer Blend mandate remains active, contributing a projected cost premium of **+$0.15** per gallon to the baseline.

## Key Macro & Regional Indicators
*   **Crude Dynamics:** 
    *   WTI: $86.64 | Brent: $93.87
*   **Supply Chain Risks:**
    *   **Refinery Outages:** Significant capacity pressure is observed. Maintenance at the Port Arthur refinery has been delayed to preserve margins, but a structural risk remains due to global infrastructure issues, potentially pushing outage volume toward **9.0–9.2 Mbd**.
    *   **Midwest Logistics:** The Whiting Refinery remains a critical cornerstone for regional supply; however, high-volume lanes (Green Bay) remain vital for maintaining local stock levels.
*   **Taxation & Policy:** Michigan’s tax floor of **$0.5089** is factored into the local price architecture.

## Model Performance & Margin Telemetry
*   **Model Architecture:** `HistGradientBoostingRegressor`
*   **Margin Analysis:** 
    *   **Current Gross Margin:** $0.4677
    *   **Historical Average:** $0.5391
    *   **Observed Drift:** **-0.0714**
*   **Alert Status:** `FALSE` (Warning: While no automated alert is triggered, the downward margin drift of ~7% indicates tightening profitability compared to historical seasonal norms).